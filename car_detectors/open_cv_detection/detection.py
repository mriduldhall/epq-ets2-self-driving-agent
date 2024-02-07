import cv2
import numpy as np
from os import getenv
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env"))

video = cv2.VideoCapture(getenv("OPEN_CV_VIDEO"))

car_cascade = cv2.CascadeClassifier('haarcascade_cars.xml')

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    dilated = cv2.dilate(blur, np.ones((3, 3)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    cars = car_cascade.detectMultiScale(closing, 1.05, 7)

    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('video', frame)
        crop_img = frame[y:y+h, x:x+w]
    if len(cars) == 0:
        cv2.imshow('video', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
