import subprocess
import platform

class TextToSpeech:
    def __init__(self):
        self.backends = []
        self.ai_indicator = None  # will be set by main.py
        self._initialize_backends()
        print(f"TTS backends available: {[b['name'] for b in self.backends]}")
    
    def set_ai_indicator(self, indicator):
        """set the AI indicator for visual feedback"""
        self.ai_indicator = indicator

    def _initialize_backends(self):
        """Initialize available TTS backends in order of preference"""
        
        # Backend 1: Windows SAPI (reliable for Windows dev)
        if platform.system() == "Windows":
            self._try_windows_sapi()
        
        # Backend 2: espeak (cross-platform, basic)
        self._try_espeak()

    def _try_windows_sapi(self):
        """Try to initialize Windows Speech API"""
        try:
            # test if PowerShell TTS works
            test_cmd = ['powershell', '-Command', 
                       'Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Dispose()']
            result = subprocess.run(test_cmd, capture_output=True, timeout=5)
            if result.returncode == 0:
                self.backends.append({'name': 'windows_sapi'})
                print("✓ Windows SAPI TTS initialized")
        except Exception as e:
            print(f"✗ Windows SAPI not available: {e}")

    def _try_espeak(self):
        """Try to initialize espeak"""
        try:
            result = subprocess.run(['espeak', '--version'], capture_output=True, timeout=5)
            if result.returncode == 0:
                self.backends.append({'name': 'espeak'})
                print("✓ espeak TTS initialized")
        except Exception as e:
            print(f"✗ espeak not available: {e}")

    def speak(self, text):
        """Speak text using the first available backend"""
        if not text or not text.strip():
            return
        
        if len(text) > 1000:
            text = text[:1000] + " ...truncated"
        
        if not self.backends:
            print(f"No TTS backends available. Text: {text}")
            return
        
        # notify AI indicator that speaking started
        if self.ai_indicator:
            self.ai_indicator.set_speaking()
        
        # try each backend until one works
        success = False
        for backend in self.backends:
            try:
                if backend['name'] == 'windows_sapi':
                    if self._speak_windows_sapi(text):
                        success = True
                        break
                elif backend['name'] == 'espeak':
                    if self._speak_espeak(text):
                        success = True
                        break
            except Exception as e:
                print(f"TTS backend {backend['name']} failed: {e}")
                continue
        
        # notify AI indicator that speaking finished
        if self.ai_indicator:
            self.ai_indicator.set_idle()
        
        if not success:
            print(f"All TTS backends failed. Text: {text}")

    def _speak_windows_sapi(self, text):
        """Speak using Windows Speech API via PowerShell"""
        # escape quotes in text
        escaped_text = text.replace('"', '""')
        
        cmd = [
            'powershell', '-Command',
            f'Add-Type -AssemblyName System.Speech; '
            f'$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
            f'$synth.Rate = 0; '  # normal speed
            f'$synth.Speak("{escaped_text}"); '
            f'$synth.Dispose()'
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=15)
        return result.returncode == 0

    def _speak_espeak(self, text):
        """Speak using espeak"""
        cmd = ['espeak', text]
        result = subprocess.run(cmd, capture_output=True, timeout=10)
        return result.returncode == 0

# create a single instance to reuse
tts = TextToSpeech()