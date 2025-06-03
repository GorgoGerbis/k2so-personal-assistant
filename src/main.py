# src/main.py
import platform
import sys
import os
import json 

# MUST LOAD ENV VARS FIRST
from dotenv import load_dotenv
load_dotenv()  # make sure this is called!

# Project Modules
import config
from router import get_backend
from components.text_to_speech import tts

# User config file
CONFIG_PATH = os.path.join(os.getcwd(), "user_config.json") # remembers users choice for future runs so setup is not repeated every time

# FIRST
# setup whatever is needed to run the program...
def run_setup():
    print("Running setup...\n")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python version: {platform.python_version()}") 
    print(f"Platform: {platform.system()} {platform.machine()}")
    
    # Load or prompt for models directory, saving choice to user_config.json for future runs
    models_dir = load_models_dir()  # Load the models directory from the config file user_config.json
    if not models_dir: # if the models directory is not set, select it
        models_dir = select_models_dir()
        save_models_dir(models_dir)
    config.MODELS_DIR = models_dir

    print("Setup complete\n")

# FIRST - HELPER A
def load_models_dir():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
            return data.get("models_dir")
    return None

# FIRST - Helper B
# Select the directory where the models are stored
def select_models_dir():
    default_dir = os.path.join(os.getcwd(), "models")
    print("Select the directory where your local AI models are stored.")
    print("Press Enter to use the default location: {default_dir}")
    print("  " + default_dir)
    user_input = input("Models directory: ").strip()
    models_dir = user_input if user_input else default_dir

    if not os.path.exists(models_dir):
        create = input(f"Directory '{models_dir}' does not exist. Create it? (y/n): ").strip().lower()
        if create == "y":
            os.makedirs(models_dir)
            print(f"Created directory: {models_dir}")
        else:
            print("Please create the directory and restart setup.")
            exit(1)
    return models_dir

# FIRST - HELPER C
def save_models_dir(models_dir):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"models_dir": models_dir}, f)

# SECOND
# Ask the user whether they want to run locally or connect remotely
def select_mode():
    while True: # Loop until valid input
        print("Select mode:")
        print("1. Local (run model on this device)")
        print("2. Remote (connect to a model server)")
        mode_input = input("Enter 1 or 2: ").strip()
        if mode_input == "1":
            return "local"
        elif mode_input == "2":
            return "remote"
        else:
            if mode_input == "q":
                print("Quitting...")
                sys.exit(0)
            else:
                print("Invalid input. Try again.\n")

# THIRD
# Show available models based on the selected mode
def select_model(mode):
    models = config.LOCAL_MODELS if mode == "local" else config.REMOTE_MODELS
    model_keys = list(models.keys())

    print("\nAvailable models:")
    for idx, name in enumerate(model_keys, start=1):
        print(f"{idx}. {name}")

    while True:
        selection = input("Select a model by number: ").strip()
        if selection.isdigit() and 1 <= int(selection) <= len(model_keys):
            return model_keys[int(selection) - 1]
        else:
            print("Invalid choice. Try again.\n")

# TODO: Add voice input later
# TODO: Add chat history later
# TODO: Add error handling later
# TODO: Add GUI later
# FOURTH
# Start the chat session using the model backend object
def run_chat_session(model_backend_obj):
    # We don't call .run() directly since the model backend should expose methods
    # for chat interaction rather than a generic run command
    try:
        chat_session = model_backend_obj.start_chat()
        while True:
            # TODO: Add voice input later
            # Text input for now
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                break
            
            # Send message to model
            response = chat_session.send_message(user_input)
            

            # Print response
            print(f"\nAssistant: {response}")
            if config.TTS_ENABLED: # TODO: Add command line arg for user text to speech...
                tts.speak(response)

            # TODO: Add voice output later
            # TODO: Add chat history later
    
    # TODO: Add more specific error handling later
    # Exception handling for chat session errors
    # Example error is if the model is not connected
    except Exception as e:
        print(f"Error during chat session: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_setup()

     # TODO: Replace with CLI args or GUI later
    # Mode and model selection
    # MODE must be selected first
    # MODEL must be selected AFTER MODE
    selected_mode = select_mode()
    selected_model = select_model(selected_mode)

    # Initialize the model
    model_backend_obj = get_backend(selected_mode, selected_model)

    # Initialize chat session and start conversation loop
    run_chat_session(model_backend_obj)
    
