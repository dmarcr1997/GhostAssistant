import requests
import os
import json

def load_config(path="config.json"):
    with open(path) as f:
        return json.load(f)

def send_zigbee_command(event="scene.game_mode"):
    config = load_config()
    HA_URL = config["home_assist_url"]
    TOKEN = config["home_assist_token"]
    HEADERS = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type":  "application/json",
    }
    url = f"{HA_URL}/api/services/scene/toggle"
    try:
        resp = requests.post(url, headers=HEADERS, json={"entity_id": event})
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Error sending Zigbee command: {e}")
        return None