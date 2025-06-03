# src/router.py
# router.py is basically a simple switchboard that decides which backend to use based on the config setting.
# It helps me keep the rest of the code agnostic to whether the project is running locally on the Pi or remotely.
from config import* 
from components.local_model import LocalModel
from components.remote_model import RemoteModel

# Switchboard that decides which backend to use
def get_backend():
    if MODE == "local":
        model_path = LOCAL_MODELS[SELECTED_MODEL]
        return LocalModel(model_path)
    elif MODE == "remote":
        endpoint = REMOTE_MODELS[SELECTED_MODEL]
        return RemoteModel(endpoint)
    else:
        raise ValueError("Invalid MODE setting")