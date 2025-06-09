import json
import wave
from vosk import Model, KaldiRecognizer
import os

model = Model("Vosk_model")

def audio_to_text(filename):
    """
    Uses Vosk TTS model to transcribe audio file to text.
    Returns transcribed text
    """

    wf = wave.open(filename, "rb")
    recognizer = KaldiRecognizer(model, wf.getframerate())

    results = []
    while True:
        data = wf.readframes(4000)
        if not data:
            break
        if recognizer.AcceptWaveform(data):
            results.append(json.loads(recognizer.Result()).get("text", ""))
    final_res = json.loads(recognizer.FinalResult())
    results.append(final_res.get("text", ""))
    return " ".join(filter(None, results)).strip()
