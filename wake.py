import time
import threading
import queue
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json
import wave
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model")
WAKE_WORDS = ["ghost", "hey ghost", "wake up"]
SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 5
AUDIO_FILE = "wake_temp.wav"

model = Model(MODEL_PATH)

def record_audio(duration=DURATION):
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype='int16'
    )
    sd.wait()
    return audio

def save_audio(audio):
    with wave.open(AUDIO_FILE, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

def transcribe_audio():
    wf = wave.open(AUDIO_FILE, 'rb')
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    result = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            result.append(res.get("text", ""))
    final = json.loads(rec.FinalResult())
    result.append(final.get("text", ""))
    return " ".join(result).strip().lower()

def detect_wake_word():
    audio = record_audio()
    save_audio(audio)
    transcript = transcribe_audio()
    for phrase in WAKE_WORDS:
        if phrase in transcript:
            print(f"👻 Wake word detected: '{phrase}'")
            return True
    return False

def should_wake():
    from vision import is_person_detected_for
    if is_person_detected_for(2.0):
        print("👁️  Person detected for more than 2 seconds. Waking up.")
        return True
    if detect_wake_word():
        return True
    return False
