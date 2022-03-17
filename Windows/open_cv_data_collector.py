import cv2 as cv
import numpy as np

window_name = "Window"
window_size = [1920, 1080]
cv.namedWindow(window_name)
cv.resizeWindow(window_name, window_size[1], window_size[0])

drawing = np.zeros((window_size[1], window_size[0], 3), dtype=np.uint8)


class data_collector:
    landmarks = [0.1, 0.5, 0.9]
    length = 20

    def __init__(self, window):
        self.black_window = window
        self.window_width = window.shape[0]
        self.window_height = window.shape[1]
        pass

    def add_cross(self):
        for i in data_collector.landmarks:
            cv.line(self.black_window, (round(i*self.window_height)-data_collector.length, round(i*self.window_width)-data_collector.length),
                    (round(i*self.window_height)+data_collector.length, round(i*self.window_width)+data_collector.length), (0, 0, 255), 5)
            cv.line(self.black_window, (round(i * self.window_height) + data_collector.length, round(i * self.window_width) - data_collector.length),
                    (round(i * self.window_height) - data_collector.length, round(i * self.window_width) + data_collector.length), (0, 0, 255), 5)
        return self.black_window


test = data_collector(window=drawing).add_cross()
cv.imshow(window_name, test)

cv.waitKey()
cv.destroyAllWindows()
