import cv2
import numpy as np
from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))

input_video = getenv("INPUT_VIDEO_PATH")
output_video = getenv("OUTPUT_VIDEO_PATH")
yolo_weights = getenv("YOLO_WEIGHTS")
yolo_config = getenv("YOLO_CONFIG")
detection_probability_threshold = float(getenv("DETECTION_THRESHOLD"))
non_maxima_suppression_threshold = float(getenv("NON_MAXIMA_SUPPRESSION_THRESHOLD"))

LABELS = open(getenv("LABELS_PATH")).read().strip().split("\n")

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

net = cv2.dnn.readNetFromDarknet(yolo_config, yolo_weights)
ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

video = cv2.VideoCapture(input_video)
writer = None
(W, H) = (None, None)

while True:
    grabbed, frame = video.read()

    if not grabbed:
        break

    if W is None and H is None:
        (H, W) = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(ln)
    boxes = []
    confidences = []
    class_ids = []
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > detection_probability_threshold:
                box = detection[0:4] * np.array([W, H, W, H])
                (center_x, center_y, width, height) = box.astype("int")
                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, detection_probability_threshold, non_maxima_suppression_threshold)
    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            color = [int(c) for c in COLORS[class_ids[i]]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(LABELS[class_ids[i]], confidences[i])
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    if writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(output_video, fourcc, 30, (frame.shape[1], frame.shape[0]), True)
    writer.write(frame)

writer.release()
video.release()
