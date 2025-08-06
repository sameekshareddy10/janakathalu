from transformers import pipeline
import tempfile
import os

asr = pipeline("automatic-speech-recognition", model="openai/whisper-small")

def transcribe_audio_whisper(file, language=None):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(file.getvalue())
        tmp_path = tmp.name

    result = asr(tmp_path)
    os.remove(tmp_path)
    return result["text"]
