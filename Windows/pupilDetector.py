import cv2
import numpy as np


class pupilDetector:
    def __init__(self, frame, debugging=False):
        """ TODO: give input to the class"""
        self.frame = frame
        self.debugging = debugging
        # default parameters
        self.params = {
            "roi_x_min": 0,
            "roi_x_max": 480,
            "roi_y_min": 220,
            "roi_y_max": 640
        }

    '''function for hough circle implementation'''

    def houghCircle(self):
        """ TODO: Add implementation for existing hough circle approach """
        roi = self.frame[self.params["roi_y_min"]:self.params["roi_y_max"],
              self.params["roi_x_min"]:self.params["roi_x_max"]]
        # output = roi.copy()
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        cl1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe = cl1.apply(gray)
        gray = cv2.medianBlur(clahe, 9)
        _, threshold = cv2.threshold(gray, 132, 255, cv2.THRESH_BINARY_INV)

        circles = cv2.HoughCircles(threshold, cv2.HOUGH_GRADIENT, 1, 100, param1=40, param2=15, minRadius=20,
                                   maxRadius=40)
        detected_circles = np.array([])
        if circles is not None:
            detected_circles = np.uint16(np.around(circles))

            test = []
            for idx, data in enumerate(detected_circles[0, :]):
                # Dirty implementation
                if data[0] > np.shape(roi)[0] - 1 or data[1] > np.shape(roi)[1] - 1:
                    test.append(idx)
                if data[2] > 120:
                    test.append(idx)
            detected_circles = np.reshape(detected_circles,
                                          (np.shape(detected_circles)[1], np.shape(detected_circles)[2]))
            detected_circles = np.delete(detected_circles, tuple(test), 0)
            print(detected_circles)
        return detected_circles, roi


if __name__ == "__main__":
    frame = cv2.imread(
        r"PATH_FOLDER_IMAGE")
    detector = pupilDetector(frame=frame)
    circle, output_image = detector.houghCircle()
    if circle is not None:
        for idx, (x, y, r) in enumerate(circle):
            cv2.circle(output_image, (x, y), r, (0, 255, 0), 3)
        cv2.imshow("output", output_image)
    cv2.waitKey(0)
