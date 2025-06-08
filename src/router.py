# src/router.py
# router.py is basically a simple switchboard that decides which backend to use based on the config setting.
# It helps me keep the rest of the code agnostic to whether the project is running locally on the Pi or remotely.
import os
import config 
from components.local_model import LocalModel
from components.remote_model import RemoteModel

# switchboard that decides which backend to use
# local: instantiates local model with the correct model path
# remote: instantiates remote model with the correct endpoint
def get_backend(selected_mode, selected_model):
    if selected_mode == "local":
        model_path = os.path.join(config.MODELS_DIR, config.LOCAL_MODELS[selected_model])
        print("model path: ", model_path)
        return LocalModel(model_path, config.MODELS_DIR)
    elif selected_mode == "remote":
        model_config = config.REMOTE_MODELS[selected_model]
        return RemoteModel(model_config)
    else:
        raise ValueError("Invalid MODE setting")