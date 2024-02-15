import cv2
import numpy as np


class Detector:
    def __init__(self):
        self.warp_size = [150, 300]
        self.binary_threshold = (220, 255)
        self.number_of_windows = 50
        self.window_margin = 10
        self.min_pixel_detection = 5

    def perspective_transform(self, image):
        source = np.float32([[40, 90], [300, 90], [0, 220], [400, 220]])
        destination = np.float32([[0, 0], [self.warp_size[0], 0], [0, self.warp_size[1]], self.warp_size])
        matrix = cv2.getPerspectiveTransform(source, destination)
        inverse_matrix = cv2.getPerspectiveTransform(destination, source)
        warped = cv2.warpPerspective(image, matrix, self.warp_size)
        return warped, inverse_matrix

    def threshold(self, image):
        image_hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
        image_hls = image_hls[:, :, 1]
        image_hls = image_hls * (255 / np.max(image_hls))
        binary_output = np.zeros_like(image_hls)
        binary_output[(image_hls > self.binary_threshold[0]) & (image_hls <= self.binary_threshold[1])] = 1
        return binary_output

    def process_image(self, image):
        warped, inverse_matrix = self.perspective_transform(image)
        thresholded = self.threshold(warped)
        return thresholded, inverse_matrix

    def detect(self):
        images = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        # images = ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]
        counter = 0
        for image in images:
            image = cv2.imread('../Test-Data/Lane Detection/field_of_view_' + image + '.png')
            detected, inverse_matrix = self.process_image(image)
            if counter == 0:
                numpy_horizontal_concat = detected
            else:
                numpy_horizontal_concat = np.concatenate((numpy_horizontal_concat, detected), axis=1)
            counter += 1
        cv2.imshow('Detected', numpy_horizontal_concat)
        cv2.waitKey(0)


if __name__ == '__main__':
    detector = Detector()
    detector.detect()
