import os
import json
import requests

with open("config.json") as f:
    config = json.load(f)

def send_discord(file_path, message="Audio response", is_image=False):
    url = config["discord_webhook_url"]
    with open(file_path, 'rb') as f:
        codes = None
        if is_image:
            files = {
                'file': (os.path.basename(file_path), f, 'application/octet-stream')
            }
            payload = {
                'payload_json': json.dumps({
                    'content': message
                })
            }
            r = requests.post(url, data=payload, files=files)
            codes = r.status_code
        else:
            files = {'file': (os.path.basename(file_path), f, 'audio/mpeg')}
            payload = {'payload_json': json.dumps({'content': message})}
            r = requests.post(url, data=payload, files=files)
            codes = r.status_code
        if codes in (200, 204):
            print("✅ Discord: Sent")
        else:
            print(f"❌ Discord error {r.status_code}: {r.text}")