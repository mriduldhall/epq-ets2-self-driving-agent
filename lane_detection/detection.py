import cv2
import numpy as np


class Detector:
    def __init__(self):
        self.warp_size = [150, 300]
        self.binary_threshold = (220, 255)
        self.number_of_windows = 50
        self.window_margin = 10
        self.min_pixel_detection = 5
        self.image_size = (400, 225)
        self.left_lane_colour = (255, 0, 255)
        self.right_lane_colour = (0, 255, 255)

    def perspective_transform(self, image):
        source = np.float32([[40, 85], [300, 85], [0, 220], [400, 220]])
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

    def detect_lanes_sliding_window(self, image):
        histogram = np.sum(image[image.shape[0] // 2:, :], axis=0)
        midpoint = int(histogram.shape[0] // 2)
        quarter_point = int(midpoint // 2)
        leftx_base = np.argmax(histogram[quarter_point:midpoint]) + quarter_point
        rightx_base = np.argmax(histogram[midpoint:(midpoint + (2 * quarter_point))]) + midpoint

        window_height = int(image.shape[0] / self.number_of_windows)
        nonzero = image.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        leftx_current = leftx_base
        rightx_current = rightx_base

        left_lane_inds = []
        right_lane_inds = []

        for window in range(self.number_of_windows):
            win_y_low = image.shape[0] - (window + 1) * window_height
            win_y_high = image.shape[0] - window * window_height
            win_xleft_low = leftx_current - self.window_margin
            win_xleft_high = leftx_current + self.window_margin
            win_xright_low = rightx_current - self.window_margin
            win_xright_high = rightx_current + self.window_margin
            good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) &
                              (nonzerox < win_xleft_high)).nonzero()[0]
            good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) &
                               (nonzerox < win_xright_high)).nonzero()[0]
            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)
            if len(good_left_inds) > self.min_pixel_detection:
                leftx_current = int(np.mean(nonzerox[good_left_inds]))
            if len(good_right_inds) > self.min_pixel_detection:
                rightx_current = int(np.mean(nonzerox[good_right_inds]))

        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)

        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds]
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds]

        left_lane, right_lane = (None, None)
        if len(leftx) != 0:
            left_lane = np.polyfit(lefty, leftx, 2)
        if len(rightx) != 0:
            right_lane = np.polyfit(righty, rightx, 2)

        return left_lane, right_lane

    def draw_lane(self, thresholded, left_lane, right_lane, inverse_matrix):
        warp_zero = np.zeros_like(thresholded).astype(np.uint8)
        color_warp = np.dstack((warp_zero, warp_zero, warp_zero))
        if left_lane is None or right_lane is None:
            return cv2.warpPerspective(color_warp, inverse_matrix, self.image_size)
        h, w = thresholded.shape
        ploty = np.linspace(0, h - 1, num=h)
        left_fitx = left_lane[0] * ploty ** 2 + left_lane[1] * ploty + left_lane[2]
        right_fitx = right_lane[0] * ploty ** 2 + right_lane[1] * ploty + right_lane[2]
        pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
        pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
        cv2.polylines(color_warp, np.int32([pts_left]), isClosed=False, color=self.left_lane_colour, thickness=1)
        cv2.polylines(color_warp, np.int32([pts_right]), isClosed=False, color=self.right_lane_colour, thickness=1)
        detected_lanes_image = cv2.warpPerspective(color_warp, inverse_matrix, self.image_size)
        return detected_lanes_image

    @staticmethod
    def visualiser(image, detected):
        combined_image = cv2.addWeighted(image, 0.8, detected, 0.7, 0)
        return combined_image

    def detect(self, image):
        thresholded, inverse_matrix = self.process_image(image)
        left_fit, right_fit = self.detect_lanes_sliding_window(thresholded)
        detected = self.draw_lane(thresholded, left_fit, right_fit, inverse_matrix)
        return detected
