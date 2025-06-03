# src/components/text_to_speech.py
import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text):
        if not text or not text.strip():
            return
        # Optionally, limit length to avoid reading huge outputs
        if len(text) > 1000:
            text = text[:1000] + " ... (truncated)"
        self.engine.say(text)
        self.engine.runAndWait()


# create a single instance to reuse
tts = TextToSpeech()