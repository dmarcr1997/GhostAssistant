from face import start_face, get_face
import threading
import time
import sys
from PyQt5.QtCore import QTimer

def queue_expression(face_state):
    get_face().show_expression_signal.emit(face_state)
    return

def queue_shutdown():
    get_face().shutdown_signal.emit()

def user_input_loop():
    while get_face() is None:
        time.sleep(0.1)

    while True:
        print("Emotion (or 'shutdown' to exit): ", end='', flush=True)
        user_input = sys.stdin.readline().strip().lower()   
        if user_input == "shutdown":
            queue_shutdown()
            time.sleep(3)
            print("👻 Ghost shutting down...")
            sys.exit(0)

        print("Duration (seconds): ", end='', flush=True)
        duration_input = sys.stdin.readline().strip().lower()
        print("Talking? (T/F): ", end='', flush=True)
        talking_input = sys.stdin.readline().strip().upper()

        face_state = {
            "emotion": user_input,
            "duration": int(duration_input),
            "talking": talking_input == "T"
        }

        queue_expression(face_state)

if __name__ == "__main__":
    threading.Thread(target=user_input_loop, daemon=True).start()
    start_face()
