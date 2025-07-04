from face import start_face, get_face
from wake import should_wake
from transcribe import audio_to_text
from listen import record_audio
from brain import init_llm, generate_reply
from speak import talk_back
from act import perform_action
import json
import re

from vision import constantly_check_detections
from local_assist import send_zigbee_command

import threading
import time
from PyQt5.QtCore import QTimer

# Time tracking
last_interaction_time = time.time()

# Helper: show emotion on face
def queue_expression(face_state):
    get_face().show_expression_signal.emit(face_state)

# Helper: shut down the face
def queue_shutdown():
    get_face().shutdown_signal.emit()

# Background check for wake triggers

def monitor_wake():
    global last_interaction_time
    while True:
        if should_wake():
            send_zigbee_command()
            print("👻 Wake trigger detected!")
            face_state = {"emotion": "happy", "duration": 3, "talking": True}
            queue_expression(face_state)
            talk_back("Hello! What's up?")
            last_interaction_time = time.time()

            audio = record_audio()
            transcript = audio_to_text(audio)
            print(transcript)
            if 'picture' in transcript:
                face_state = {"emotion": "excited", "duration": 3, "talking": True}
                queue_expression(face_state)
                talk_back("Sending over a picture!")
                perform_action('capture')
            elif 'describe' in transcript and 'frame' in transcript:
                face_state = {"emotion": "love", "duration": 3, "talking": True}
                queue_expression(face_state)
                talk_back("Let me see...")
                perform_action('describe')
            elif 'shutdown' in transcript or 'shut down' in transcript:
                talk_back('SHUTTING DOWN...')
                talk_back(
                    "AAEEEEAAEEEEE AAEEEEAAEEEEE AAEEEEAAEEEEE!",
                    "output.wav",
                    "en+m1", 
                    500, 
                    99, 
                    200
                )
                queue_shutdown()
                time.sleep(2000)
                break
            elif transcript:
                face_state = {"emotion": "neutral", "duration": 2, "talking": True}
                queue_expression(face_state)
                talk_back("Let me see...")
                response = clean_json_response(generate_reply(transcript))
                talk_text = response
                try:
                    data = json.loads(response)
                    if 'emotion' in data:
                        face_state = {"emotion": data['emotion'], "duration": 2, "talking": True}
                    if 'text' in data:
                        talk_text = data['text']
                except json.JSONDecodeError:
                    print("🛑 LLM response not in JSON format. Raw output:", response)
                    talk_back("I had a brain fart. Try again.")
                    continue
                queue_expression(face_state)
                talk_back(talk_text)

            last_interaction_time = time.time()
        time.sleep(1)

def clean_json_response(raw_response):
    # Strip markdown/code block syntax
    raw_response = raw_response.replace("```json", "").replace("```", "").strip()
    # Try to extract JSON if anything wraps it
    match = re.search(r'\{.*?\}', raw_response, re.DOTALL)
    if match:
        return match.group(0)
    return raw_response


# Background inactivity monitor

def monitor_inactivity():
    global last_interaction_time
    while True:
        if time.time() - last_interaction_time > 60:
            print("😴 Going to sleep due to inactivity.")
            queue_expression({"emotion": "sleep", "duration": 1, "talking": False})
            last_interaction_time = time.time()
        time.sleep(10)

# Start threads
if __name__ == "__main__":
    init_llm()
    threading.Thread(target=constantly_check_detections, daemon=True).start()
    threading.Thread(target=monitor_wake, daemon=True).start()
    threading.Thread(target=monitor_inactivity, daemon=True).start()

    start_face()
