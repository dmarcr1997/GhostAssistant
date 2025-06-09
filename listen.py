import sounddevice as sd
import soundfile as sf

FILENAME = "temp-audio.wav"

def record_audio(duration=10, samplerate=16000, channels=1):
    """Records audio to temp-audio file for duration
       Returns filename
    """
    print(f"🎙️ Recording for {duration}s...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
    sd.wait()
    sf.write(FILENAME, audio, samplerate)
    return FILENAME