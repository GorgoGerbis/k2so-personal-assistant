# src/config.py
# Responsible for runtime settings (mode, model path, ... etc)

MODE = "local"  # or "remote" # Run locally or remotely

MODELS_DIR = None # Will be set at runtime by setup() funciton in main.py

# WIP @ToDo
# Dictionary of available local models
# Key -> model name
# Val -> model path (relative to MODELS_DIR) name only
LOCAL_MODELS = {
    "testLocal": "",
    "tinyllama": "tinyllama-1.1b-chat.q4_0.gguf",
    "phi2": "phi-2.q4_0.gguf"
}

# WIP @ToDo
# Dictionary of available remote models
# Key -> model name
# Val -> url & api_key_env
#       url - API endpoint where user input is sent (via an HTTP POST or GET request) and received
#       api_key_env - Environment variable name for the API key in the .env file
REMOTE_MODELS = {
    "testRemote": {
        "url": "http://192.168.1.10:8000/chat",
        "api_key_env": None  # or omit if not needed
    },
    "openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "api_key_env": "OPENAI_API_KEY"
    },
    "tinyllama": {
        "url": "http://192.168.1.10:5000/chat",
        "api_key_env": None  # or omit if not needed
    },
    "deepseek": {
        "url": "http://192.168.1.20:5000/chat",
        "api_key_env": "DEEPSEEK_API_KEY"
    }
}

# Set which model to use
SELECTED_MODEL = "testLocal"

# Set whether to use text-to-speech
TTS_ENABLED = True  # set to False to disable text-to-speech
