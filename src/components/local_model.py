# components/local_model.py

# TODO: Needs to be rewritten to use the new model backend interface
# TODO: May need to have a specialized ChatSession class for local & remote models
from components.chat_session import ChatSession


class LocalModel:
    def __init__(self, model_path):
        # Model path is stored for future use
        self.model_path = model_path

        self.model_name = model_path.split("/")[-1] # extract model name from path
        # Model loading logic will go here

    def generate_response(self, prompt):
        # Replace with actual inference logic
        return "Local model (stub): " + prompt

    # TODO: Only for testing purposes now remove later...
    # Prototype for chat interface
    def start_chat(self):
        # TODO: Implement chat interface
        return ChatSession(self)
