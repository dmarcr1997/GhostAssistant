# act.py
# Action module for Ghost Assistant
# Currently supports stubs for future automation and interactions

import time
import cv2
import os
from datetime import datetime
from vision import get_recent_detections
from picamera2 import Picamera2

# Initialize camera for snapshot actions
camera = Picamera2()
camera.preview_configuration.main.size = (1024, 600)
camera.preview_configuration.main.format = "RGB888"
camera.preview_configuration.align()
camera.start()
time.sleep(1)

def capture_image(label="snapshot"):
    """Capture a still image from camera and save it."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"images/{label}_{timestamp}.jpg"
    frame = camera.capture_array()
    if not os.path.exists("images"):
        os.makedirs("images")
    cv2.imwrite(filename, frame)
    print(f"📸 Image saved: {filename}")
    return filename

def describe_current_scene():
    """Return a string summarizing what's currently visible."""
    objects = get_recent_detections()
    if not objects:
        return "I don't see anything unusual right now."
    elif len(objects) == 1:
        return f"I currently see a {objects[0]}."
    else:
        return f"I see: {', '.join(objects)}."

# Reserved for future smart home or Discord integrations
def perform_action(action_name):
    """Perform a generic action, placeholder for future expansion."""
    print(f"⚙️ Performing action: {action_name}")
    if action_name == "capture":
        return capture_image()
    elif action_name == "describe":
        return describe_current_scene()
    else:
        return f"Action '{action_name}' is not implemented yet."
