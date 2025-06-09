import os
import json
import requests

with open("config.json") as f:
    config = json.load(f)

def send_discord_audio(file_path, message="Audio response"):
    url = config["discord_webhook_url"]
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f, 'audio/mpeg')}
        payload = {'payload_json': json.dumps({'content': message})}
        r = requests.post(url, data=payload, files=files)
        if r.status_code in (200, 204):
            print("✅ Discord: Sent")
        else:
            print(f"❌ Discord error {r.status_code}: {r.text}")
