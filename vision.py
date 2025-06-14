from picamera2 import Picamera2
import cv2
import numpy as np
import time
from tflite_runtime.interpreter import Interpreter

# Load TFLite model
interpreter = Interpreter("ssd_model/detect.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

# TF1 vs TF2 model output index handling
def check_tf_version(output_details):
    outname = output_details[0]['name']
    if 'StatefulPartitionedCall' in outname:
        return 1, 3, 0
    return 0, 1, 2

boxes_idx, classes_idx, scores_idx = check_tf_version(output_details)

# Load label map
with open("ssd_model/labelmap.txt", 'r') as f:
    labels = [line.strip() for line in f.readlines()]
if labels[0] == '???':
    labels.pop(0)

#start camera   
frame_height = 1024
frame_width = 600
picam2 = Picamera2()
picam2.preview_configuration.main.size = (frame_height, frame_width)
picam2.preview_configuration.main.format = "RGB888"

# Align configuration parameters based on camera sensor details.
picam2.preview_configuration.align()
picam2.start()

time.sleep(1) 

# Detection state
last_detection_time = 0
last_detected_classes = []
person_detected_duration = 0

# Main detection function

def detect_objects(frame):
    global last_detection_time, last_detected_classes, person_detected_duration

    image = cv2.resize(frame.copy(), (width, height))
    input_data = np.expand_dims(image, axis=0)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0]
    classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0]
    scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0]

    frame_height, frame_width, _ = frame.shape
    detected_classes = []
    person_detected = False

    for i in range(len(scores)):
        if scores[i] > 0.5:
            label = labels[int(classes[i])]
            detected_classes.append(label)

            ymin = int(boxes[i][0] * frame_height)
            xmin = int(boxes[i][1] * frame_width)
            ymax = int(boxes[i][2] * frame_height)
            xmax = int(boxes[i][3] * frame_width)

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if label == "person":
                person_detected = True

    now = time.time()
    if person_detected:
        person_detected_duration += now - last_detection_time
    else:
        person_detected_duration = 0

    last_detection_time = now
    last_detected_classes = detected_classes

    return frame

# Function: constantly run detection in background (for wake triggers)
def constantly_check_detections():
    while True:
        frame = picam2.capture_array()
        detect_objects(frame)
        time.sleep(0.1)

# Function: return most recent detected labels
def get_recent_detections():
    return list(set(last_detected_classes))

# Function: return person detection state
def is_person_detected_for(seconds=2.0):
    return person_detected_duration >= seconds

# Function: open live annotated feed manually
def open_live_feed():
    print("📹 Starting live feed. Press Q to quit.")
    try:
        while True:
            frame = picam2.capture_array()
            annotated = detect_objects(frame)
            cv2.imshow("Ghost Vision", annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cv2.destroyAllWindows()
