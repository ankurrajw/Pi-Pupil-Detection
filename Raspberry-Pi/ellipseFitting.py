import cv2 as cv
import numpy as np
from datetime import datetime
import time
import os
import random as rng
import logging

srcPiCam = 'libcamerasrc ! video/x-raw,width=640,height=480,framerate=90/1 ! videoflip method=clockwise ! videoconvert ! appsink'
cap = cv.VideoCapture(srcPiCam)


def create_workspace():
    base_path = "/home/pi/Desktop/master-thesis-eye-tracking/Results/Ellipse/"
    time_right_now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    name_workspace = base_path + "Hough" + time_right_now + '/'
    if not os.path.exists(name_workspace):
        os.makedirs(name_workspace)
        print("folder name", name_workspace)

    return name_workspace


count = 0
folder_name = create_workspace()

fps_start_time = 0
fps = 0

while count < 600:
    ret, frame = cap.read()
    fps_end_time = time.time()
    time_diff = fps_end_time - fps_start_time
    fps = 1 / time_diff
    fps_start_time = fps_end_time
    fps_text = "FPS: {:.2f}".format(fps)
    if ret == True:
        roi = frame[220:640, 0:480]
        output = roi.copy()
        src_gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
        cl1 = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe = cl1.apply(src_gray)

        src_gray = cv.medianBlur(clahe, 9)
        kernel = np.ones((5, 5), np.uint8)
        _, src_gray = cv.threshold(src_gray, 100, 255, cv.THRESH_BINARY_INV)
        opening = cv.morphologyEx(src_gray, cv.MORPH_OPEN, kernel)

        threshold = 100
        canny_output = cv.Canny(opening, threshold, threshold * 2)
        contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        if contours is not None:
            minEllipse = [None] * len(contours)
            for i, c in enumerate(contours):
                if 50 < c.shape[0] < 100:
                    minEllipse[i] = cv.fitEllipse(c)
                    print(minEllipse[i])
            # drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

            for i, c in enumerate(contours):
                color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
                # contour
                # cv.drawContours(drawing, contours, i, color)
                # ellipse
                if 50 < c.shape[0] < 100:
                    cv.ellipse(roi, minEllipse[i], color, 2)
                    cv.imwrite(folder_name + "hough_circle" + str(count) + ".png", output)

        else:
            cv.imwrite(folder_name + "hough_circle" + str(count) + ".png", frame)

cap.release()

