import sys
import time
import threading
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor, QPainter
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

EMOTION_FACE_MAP = {
    "sleep": 21,
    "neutral": 1,
    "happy": 1,
    "sad": 2,
    "excited": 3,
    "angry": 11,
    "tired": 15,
    "love": 25,
    "dead": 20,
    "talking_frames": [1, 3, 7, 3, 14, 16, 3, 7, 3 ],
    "shutdown_frames": [22, 23, 24, 19, 24, 20]
}

class GhostFace(QWidget):
    show_expression_signal = pyqtSignal(dict)
    shutdown_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ghost Assistant Face")
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("background-color: #222222;")

        # Layout
        layout = QVBoxLayout()
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Load default sleeping face
        self.update_face(EMOTION_FACE_MAP["sleep"])
        self.talking = False
        self.timer = QTimer()

        self.sleep_timeout = 10  # seconds to return to sleep
        self.sleep_timer = QTimer()
        self.sleep_timer.timeout.connect(self.go_to_sleep)
        self.sleep_timer.setSingleShot(True)
        self.show_expression_signal.connect(self.show_expression)
        self.shutdown_signal.connect(self.shutdown)

    def update_face(self, face_id):
        path = f"assets/faces/Face_{face_id}.png"
        base = QPixmap(300, 300)
        base.fill(Qt.transparent)

        face = QPixmap(path)
        if face.isNull():
            print(f"❌ Failed to load face image: {path}")
            return

        face = face.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Paint the aura and then the face
        painter = QPainter(base)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#eeeeee"))  # light gray aura
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 300, 300)  # ghost head aura
        painter.drawPixmap(0, 0, face)       # face image on top
        painter.end()

        self.label.setPixmap(base)


    def show_expression(self, state):
        print(f"STATE: {state}")
        emotion = state.get("emotion", "neutral")
        duration = state.get("duration", 3)
        self.talking = state.get("talking", False)

        self.sleep_timer.stop()  # Reset sleep timer if active

        if self.talking:
            self.animate_talking(duration, end_emotion=emotion)
        else:
            face_id = EMOTION_FACE_MAP.get(emotion, EMOTION_FACE_MAP["neutral"])
            self.update_face(face_id)
            self.sleep_timer.start(self.sleep_timeout * 1000)  # Start timeout to go back to sleep

    def animate_talking(self, duration, end_emotion="neutral"):
        self.talking_index = 0
        self.talking_start_time = time.time()
        self.talking_duration = duration
        self.talking_end_emotion = end_emotion

        self.talking_timer = QTimer()
        self.talking_timer.timeout.connect(self.update_talking_frame)
        self.talking_timer.start(300)  # ms between face frames

    def update_talking_frame(self):
        if time.time() - self.talking_start_time >= self.talking_duration:
            self.talking_timer.stop()
            final_face = EMOTION_FACE_MAP.get(self.talking_end_emotion, EMOTION_FACE_MAP["neutral"])
            self.update_face(final_face)
            self.sleep_timer.start(self.sleep_timeout * 1000)
        else:
            frames = EMOTION_FACE_MAP["talking_frames"]
            self.update_face(frames[self.talking_index % len(frames)])
            self.talking_index += 1

    def go_to_sleep(self):
        self.update_face(EMOTION_FACE_MAP["sleep"])

    def shutdown(self):
        self.shutdown_index = 0
        self.shutdown_frames = EMOTION_FACE_MAP["shutdown_frames"]

        self.shutdown_timer = QTimer()
        self.shutdown_timer.timeout.connect(self.update_shutdown_frame)
        self.shutdown_timer.start(400)

    def update_shutdown_frame(self):
        if self.shutdown_index >= len(self.shutdown_frames):
            self.shutdown_timer.stop()
            self.close()
        else:
            self.update_face(self.shutdown_frames[self.shutdown_index])
            self.shutdown_index += 1

face_app = QApplication(sys.argv)
face_instance = GhostFace()

def start_face():
    face_instance.show()
    return face_app.exec_()

def get_face():
    return face_instance


# Example usage
if __name__ == '__main__':
    start_face()

