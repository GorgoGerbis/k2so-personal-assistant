# components/remote_model.py

# TODO: Needs to be rewritten to use the new model backend interface
class RemoteModel:
    def __init__(self, endpoint):
        self.url = endpoint
