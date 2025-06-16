import time
import cv2
import os
from datetime import datetime
from vision import get_recent_detections, get_camera
from log import send_discord
from speak import talk_back

def capture_image(label="snapshot"):
    """Capture a still image from camera and save it."""
    camera = get_camera()
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
        image = capture_image()
        send_discord(image, "Captured Image", True)
        return
    elif action_name == "describe":
        talk_back(describe_current_scene())
        return
    else:
        return f"Action '{action_name}' is not implemented yet."
