import cv2
import numpy as np
from os import getenv
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv(".env"))
yolo_weights = getenv("YOLO_WEIGHTS")
yolo_config = getenv("YOLO_CONFIG")
labels = open(getenv("LABELS_PATH")).read().strip().split("\n")
colour = (0, 255, 0)

net = cv2.dnn.readNetFromDarknet(yolo_config, yolo_weights)
ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]


class Detection:
    def __init__(self, detection_probability_threshold=0.3, non_maxima_suppression_threshold=0.3):
        self.detection_probability_threshold = detection_probability_threshold
        self.non_maxima_suppression_threshold = non_maxima_suppression_threshold

    def detect(self, input_image):
        H, W = input_image.shape[:2]
        blob = cv2.dnn.blobFromImage(input_image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
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
                if confidence > self.detection_probability_threshold:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (center_x, center_y, width, height) = box.astype("int")
                    x = int(center_x - (width / 2))
                    y = int(center_y - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.detection_probability_threshold, self.non_maxima_suppression_threshold)
        if len(idxs) > 0:
            for i in idxs.flatten():
                label = labels[class_ids[i]]
                if "dont_show" not in label:
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])
                    cv2.rectangle(input_image, (x, y), (x + w, y + h), colour, 2)
        return input_image
