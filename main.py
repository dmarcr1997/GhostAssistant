from face import start_face, get_face
from wake import should_wake_up
from transcribe import record_audio_and_transcribe
from brain import process_prompt
from speak import speak_text
from act import perform_action
from vision import constantly_check_detections

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
        if should_wake_up():
            print("👻 Wake trigger detected!")
            face_state = {"emotion": "happy", "duration": 3, "talking": True}
            queue_expression(face_state)
            last_interaction_time = time.time()

            transcript = record_audio_and_transcribe()
            if transcript:
                face_state = {"emotion": "neutral", "duration": 2, "talking": True}
                queue_expression(face_state)
                response, action = process_prompt(transcript)
                speak_text(response)
                if action:
                    perform_action(action)

            last_interaction_time = time.time()
        time.sleep(1)

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
    threading.Thread(target=constantly_check_detections, daemon=True).start()
    threading.Thread(target=monitor_wake, daemon=True).start()
    threading.Thread(target=monitor_inactivity, daemon=True).start()

    start_face()
