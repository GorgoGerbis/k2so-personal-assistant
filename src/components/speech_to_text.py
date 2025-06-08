import whisper
import sounddevice as sd
import numpy as np

class WhisperSTT:
    def __init__(self, model_size="tiny"):
        self.model = whisper.load_model(model_size)

    def record_and_transcribe(self, duration=5, samplerate=16000):
        print(f"Recording for {duration} seconds...")
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
        sd.wait()
        audio = np.squeeze(audio)
        print("Transcribing...")
        result = self.model.transcribe(audio, fp16=False)
        return result["text"].strip()

# Example usage:
# stt = WhisperSTT()
# print(stt.record_and_transcribe())