import subprocess
from log import send_discord_audio

def talk_back(text, filename="output.wav", voice="en-us", speed=175, pitch=50):
    cmd = ["espeak-ng", "-v", voice, "-s", str(speed), "-p", str(pitch), "--stdout"]
    with open(filename, "wb") as f:
        subprocess.run(cmd, input=text.encode("utf-8"), stdout=f, check=True)
    send_discord_audio(filename)
