# components/local_model.py

# TODO: Needs to be rewritten to use the new model backend interface
class LocalModel:
    def __init__(self, model_path):
        # Model path is stored for future use
        self.model_path = model_path
        # Model loading logic will go here

    def generate_response(self, prompt):
        # Replace with actual inference logic
        return "Local model (stub): " + prompt
