import subprocess

def talk_back(text, filename="output.wav", voice="en+m3", speed=120, pitch=30, amplitude=70):
    # Generate WAV with espeak-ng
    subprocess.run([
        "espeak-ng", "-v", voice,
        "-s", str(speed),
        "-p", str(pitch),
        "-a", str(amplitude),
        "--stdout"
    ], input=text.encode("utf-8"), stdout=open(filename, "wb"))

    # Play the sound
    subprocess.run(["pw-play", filename])

