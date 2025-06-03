# src/main.py
from config import LOCAL_MODELS, REMOTE_MODELS
import platform
import sys

# FIRST
# setup whatever is needed to run the program...
def run_setup():
    print("Running setup...\n")
    print(f"Python version: {platform.python_version()}")
    print(f"Platform: {platform.system()} {platform.machine()}")
    print("Setup complete\n")


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
    models = LOCAL_MODELS if mode == "local" else REMOTE_MODELS
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

if __name__ == "__main__":
    run_setup()

     # TODO: Replace with CLI args or GUI later
    # Mode and model selection
    # MODE must be selected first
    # MODEL must be selected AFTER MODE
    selected_mode = select_mode()
    selected_model = select_model(selected_mode)