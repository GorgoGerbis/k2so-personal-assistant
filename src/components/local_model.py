# components/local_model.py

# TODO: Needs to be rewritten to use the new model backend interface
# TODO: May need to have a specialized ChatSession class for local & remote models
import os
import subprocess
from pathlib import Path
from typing import Optional
from components.chat_session import ChatSession


class LocalModel:
    def __init__(self, model_path: str, models_dir: Optional[str] = None):
        self.models_dir = models_dir or "models"
        self.model_filename = model_path
        self.full_model_path = os.path.join(self.models_dir, model_path) if models_dir else model_path
        self.model_name = Path(model_path).stem
        
        # check if this looks like a gguf file or if we should use ollama
        self.use_ollama = not model_path.endswith('.gguf')
        self.ollama_model = None
        self.llm = None
        self.is_loaded = False
        
        # figure out what kind of model we're dealing with
        if self.use_ollama:
            self._setup_ollama()
        else:
            self._setup_gguf()
    
    def _setup_ollama(self):
        # try to use ollama if the model path doesn't look like a file
        try:
            # check if ollama is available
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print("ollama not found, falling back to gguf")
                self.use_ollama = False
                return
            
            # see what models are available
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, text=True, timeout=10)
            
            # try to find a phi model if the filename suggests it
            if 'phi' in self.model_filename.lower():
                if 'phi3-local' in result.stdout:
                    self.ollama_model = 'phi3-local'
                elif 'phi3' in result.stdout:
                    self.ollama_model = 'phi3'
                else:
                    print("no phi model found in ollama, trying to use gguf")
                    self.use_ollama = False
                    return
            else:
                print("couldn't figure out ollama model name")
                self.use_ollama = False
                return
            
            self.is_loaded = True
            print(f"using ollama model: {self.ollama_model}")
            
        except Exception as e:
            print(f"ollama setup failed: {e}")
            self.use_ollama = False
    
    def _setup_gguf(self):
        # try to load gguf file with llama-cpp-python
        try:
            from llama_cpp import Llama
            
            if not os.path.exists(self.full_model_path):
                print(f"model file not found: {self.full_model_path}")
                print("trying ollama fallback")
                self.use_ollama = True
                self._setup_ollama()
                return
            
            print(f"loading {self.model_name}...")
            
            self.llm = Llama(
                model_path=self.full_model_path,
                n_ctx=4096,
                n_threads=4,
                n_gpu_layers=0,
                verbose=False,
                use_mmap=True,
                use_mlock=False,
            )
            
            self.is_loaded = True
            print(f"loaded {self.model_name}")
            
        except ImportError:
            print("llama-cpp-python not available, trying ollama fallback")
            self.use_ollama = True
            self._setup_ollama()
        except Exception as e:
            print(f"failed to load model: {e}")
            print("trying ollama fallback")
            self.use_ollama = True
            self._setup_ollama()
    
    def _format_prompt(self, user_input: str, conversation_history: Optional[list] = None) -> str:
        # format for phi-3 chat if it looks like phi, otherwise generic format
        is_phi = "phi" in self.model_name.lower() or (self.ollama_model and "phi" in self.ollama_model)
        
        if is_phi:
            if conversation_history:
                formatted = ""
                for turn in conversation_history:
                    formatted += f"<|user|>\n{turn['user']}<|end|>\n"
                    formatted += f"<|assistant|>\n{turn['assistant']}<|end|>\n"
                formatted += f"<|user|>\n{user_input}<|end|>\n<|assistant|>"
                return formatted
            else:
                return f"<|user|>\n{user_input}<|end|>\n<|assistant|>"
        else:
            if conversation_history:
                formatted = ""
                for turn in conversation_history:
                    formatted += f"Human: {turn['user']}\nAssistant: {turn['assistant']}\n"
                formatted += f"Human: {user_input}\nAssistant:"
                return formatted
            else:
                return f"Human: {user_input}\nAssistant:"
    
    def generate_response(self, prompt: str, max_tokens: int = 256) -> str:
        if not self.is_loaded:
            return "model not loaded"
        
        try:
            formatted_prompt = self._format_prompt(prompt)
            
            if self.use_ollama:
                # use ollama cli
                cmd = ['ollama', 'run', self.ollama_model, formatted_prompt]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    encoding='utf-8',
                    errors='replace'
                )
                
                if result.returncode != 0:
                    return f"ollama error: {result.stderr}"
                
                response = result.stdout.strip()
                if response.endswith("<|end|>"):
                    response = response[:-7].strip()
                
                return response if response else "need more info"
                
            else:
                # use llama-cpp-python
                response = self.llm(
                    formatted_prompt,
                    max_tokens=max_tokens,
                    temperature=0.7,
                    top_p=0.9,
                    stop=["<|end|>", "Human:", "\nHuman:"],
                    echo=False
                )
                
                generated_text = response['choices'][0]['text'].strip()
                
                if generated_text.endswith("<|end|>"):
                    generated_text = generated_text[:-7].strip()
                
                return generated_text if generated_text else "need more info"
                
        except subprocess.TimeoutExpired:
            return "request timed out"
        except Exception as e:
            return f"error: {str(e)}"
    
    def start_chat(self):
        return ChatSession(self)
