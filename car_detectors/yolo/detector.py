import cv2
import numpy as np
from os import getenv
from dotenv import load_dotenv, find_dotenv
from distance_estimator.estimator import Estimator


load_dotenv(find_dotenv(".env"))
yolo_weights = getenv("YOLO_WEIGHTS")
yolo_config = getenv("YOLO_CONFIG")
labels = open(getenv("LABELS_PATH")).read().strip().split("\n")


class Detector:
    def __init__(self, detection_probability_threshold=0.3, non_maxima_suppression_threshold=0.3):
        self.detection_probability_threshold = detection_probability_threshold
        self.non_maxima_suppression_threshold = non_maxima_suppression_threshold
        self.distance_estimator = Estimator()
        self.colour = (0, 255, 0)
        self.net = cv2.dnn.readNetFromDarknet(yolo_config, yolo_weights)
        ln = self.net.getLayerNames()
        self.ln = [ln[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def visualiser(self, image, detections):
        for detection in detections:
            x, y, w, h = detection[0]
            distance = float(detection[1])
            cv2.rectangle(image, (x, y), (x + w, y + h), self.colour, 2)
            cv2.putText(image, f"{distance:.2f}m", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colour, 2)
        return image

    def detect(self, input_image):
        input_height, input_weight = input_image.shape[:2]
        blob = cv2.dnn.blobFromImage(input_image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        layer_outputs = self.net.forward(self.ln)
        boxes = []
        confidences = []
        class_ids = []
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.detection_probability_threshold:
                    box = detection[0:4] * np.array([input_weight, input_height, input_weight, input_height])
                    (center_x, center_y, width, height) = box.astype("int")
                    x = int(center_x - (width / 2))
                    y = int(center_y - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.detection_probability_threshold, self.non_maxima_suppression_threshold)
        detections = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                label = labels[class_ids[i]]
                if "dont_show" not in label:
                    dimensions = [boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]]
                    distance = self.distance_estimator.estimate_exponential_distance(dimensions[0], dimensions[2], (input_height - dimensions[1]) - dimensions[3])
                    detections.append([dimensions, distance])
        return detections
