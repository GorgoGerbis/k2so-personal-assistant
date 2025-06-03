# components/remote_model.py
import os
import requests

# TODO: Needs to be rewritten to use the new model backend interface
# TODO: May need to have a specialized ChatSession class for local & remote models
from components.chat_session import ChatSession

# TODO: Needs to be rewritten to use the new model backend interface
class RemoteModel:
    def __init__(self, model_config):
        self.url = model_config["url"]
        self.api_key_env = model_config.get("api_key_env")
        self.model_name = self.url.split("/")[-1] # extract model name from the URL

        # get model name from the config key rather than parsing url
        # self.model_name = next(key for key, config in config.REMOTE_MODELS.items() if config["url"] == self.url)

    def generate_response(self, prompt):
        # Try to contact the remote API sending the prompt and get a response back
        try:
            api_key = os.getenv(self.api_key_env) if self.api_key_env else None
            headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
            payload = {
                "model": "gpt-3.5-turbo",  # @TODO make it easy to change models
                "messages": [{"role": "user", "content": prompt}]
            }
            response = requests.post(self.url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"] # parsing and returning the response from the API
        except Exception as e: 
            return f"Error contacting remote model: {e}"
    
    # TODO: Only for testing purposes now remove later...
    # Prototype for chat interface
    def start_chat(self):
        # TODO: Implement chat interface
        return ChatSession(self)
