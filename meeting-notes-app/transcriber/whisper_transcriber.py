import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> str:
    result = model.transcribe(audio_path)
    return result["text"]

#Internally, it uses audio preprocessing (like FFT), speech recognition, and decoding with the transformer model.
