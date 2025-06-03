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
# Val -> model endpoint
REMOTE_MODELS = {
    "testRemote": "http://192.168.1.10:8000/chat",
    "tinyllama": "http://192.168.1.10:5000/chat",
    "deepseek": "http://192.168.1.20:5000/chat"
}

# Set which model to use
SELECTED_MODEL = "testLocal"

