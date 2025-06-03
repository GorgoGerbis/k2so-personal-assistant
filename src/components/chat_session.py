# src/components/chat_session.py

class ChatSession:
    def __init__(self, backend):
        self.backend = backend

    def send_message(self, prompt):
        return self.backend.generate_response(prompt)