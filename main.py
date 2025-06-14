from face import start_face, get_face
from wake import should_wake
from transcribe import audio_to_text
from listen import record_audio
from brain import init_llm, generate_reply
from speak import talk_back
# from act import perform_action
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
        if should_wake():
            print("👻 Wake trigger detected!")
            face_state = {"emotion": "happy", "duration": 3, "talking": True}
            queue_expression(face_state)
            last_interaction_time = time.time()

            audio = record_audio()
            transcript = audio_to_text(audio)
            if transcript:
                face_state = {"emotion": "neutral", "duration": 2, "talking": True}
                queue_expression(face_state)
                response = generate_reply(transcript)
                talk_back(response)

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
    init_llm()
    threading.Thread(target=constantly_check_detections, daemon=True).start()
    threading.Thread(target=monitor_wake, daemon=True).start()
    threading.Thread(target=monitor_inactivity, daemon=True).start()

    start_face()
