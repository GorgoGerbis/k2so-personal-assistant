# components/local_model.py

class LocalModel:
    def __init__(self, model_path):
        self.llm = Llama(model_path=model_path, n_threads=4)
