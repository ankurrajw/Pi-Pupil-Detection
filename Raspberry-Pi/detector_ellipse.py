import cv2 as cv
import numpy as np
from datetime import datetime
import time
import os
import random as rng
import logging


srcPiCam = 'libcamerasrc ! video/x-raw,width=640,height=480,framerate=90/1 ! videoflip method=clockwise ! videoconvert ! appsink'
cap = cv.VideoCapture(srcPiCam)

'''Change the parameters to conduct a real time detection'''
CANNY_THRESHOLD = 100
MEDIAN_BLUR_K_SIZE = 10
MORPH_K_SIZE = 1


def create_workspace():
    base_path = "/home/pi/Desktop/master-thesis-eye-tracking/Results/Ellipse/"
    time_right_now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    name_workspace = base_path + "Ellipse" + time_right_now + '/'
    if not os.path.exists(name_workspace):
        os.makedirs(name_workspace)
        print("folder name", name_workspace)

    return name_workspace


count = 0
ellipse_detected = 0
multiple_ellipses = 0
fps_start_time = 0
fps = 0
total_images = 600
folder_name = create_workspace()


'''logger setup'''
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.FileHandler(f"{folder_name}/log_ellipse_fitting.log")
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.info("*" * 50)
logger.info("EXPERIMENT START")


def filter_contour(_contours):
    _contours_filtered = []
    print("Initial Contours : {}".format(len(_contours)))
    print("Filtered Contours:")
    for i, c in enumerate(_contours):
        try:
            convex_hull = cv.convexHull(c)
            area_hull = cv.contourArea(convex_hull)
            # print("{} area convex hull {}".format(i, area_hull))
            if 600 < area_hull:  # filtering based on area
                circumference_hull = cv.arcLength(convex_hull, True)
                circularity_hull = (4 * np.pi * area_hull) / circumference_hull ** 2
                if 0.8 < circularity_hull:  # filtering based on circularity
                    print("convex hull :{} Circularity :{} Area : {}".format(i, circularity_hull, area_hull))
                    _contours_filtered.append(convex_hull)
        except ZeroDivisionError:
            print("Division by zero for contour {}".format(i))
    return _contours_filtered


def draw_ellipse(_drawing, _contours_filtered):
    minEllipse = [None] * len(_contours_filtered)
    for i, c in enumerate(_contours_filtered):
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        minEllipse[i] = cv.fitEllipse(c)
        cv.drawContours(_drawing, _contours_filtered, i, color)
        (x, y), (MA, ma), angle = minEllipse[i]
        area_contour_hull = cv.contourArea(c)
        area_ellipse = (np.pi / 4) * MA * ma
        print("Area Ellipse :{} Area Contour Hull :{}".format(area_ellipse, area_contour_hull))
        cv.ellipse(_drawing, minEllipse[i], color=color, thickness=2)
    return _drawing


def draw_ellipse_rgb(_image, _contours):
    minEllipse = [None] * len(_contours)
    for i, c in enumerate(_contours):
        minEllipse[i] = cv.fitEllipse(c)
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        cv.drawContours(_image, _contours, i, color)
        cv.ellipse(_image, minEllipse[i], color=color, thickness=2)
    return _image


logger.info(f"Values for Canny -{CANNY_THRESHOLD} Blur K size -{MEDIAN_BLUR_K_SIZE} Morph -{MORPH_K_SIZE}")
while count < total_images:
    ret, frame = cap.read()
    fps_end_time = time.time()
    time_diff = fps_end_time - fps_start_time
    fps = 1 / time_diff
    fps_start_time = fps_end_time
    fps_text = "FPS: {:.2f}".format(fps)
    if ret:
        roi = frame[220:640, 0:480] # 0:420 if the eye is in upper portion of the frame
        output = roi.copy()
        src_gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)

        src_gray = cv.medianBlur(src_gray, MEDIAN_BLUR_K_SIZE)
        kernel = np.ones((MORPH_K_SIZE, MORPH_K_SIZE), np.uint8)
        opening = cv.morphologyEx(src_gray, cv.MORPH_OPEN, kernel)

        canny_output = cv.Canny(opening, CANNY_THRESHOLD, CANNY_THRESHOLD * 2)
        contours, _ = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours_filtered = filter_contour(contours)

        drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
        drawing = draw_ellipse(drawing, contours_filtered)
        cv.imwrite(folder_name + "ellipse" + str(count) + ".png", drawing)

        '''Comment if colour images are not needed'''
        colour_image = draw_ellipse_rgb(roi, contours_filtered)
        cv.imwrite(folder_name + "colour" + str(count) + ".png", colour_image)

        ellipse_detected += len(contours_filtered)
        if len(contours_filtered) > 1:
            multiple_ellipses += len(contours_filtered) - 1

        count += 1

cap.release()
cv.destroyAllWindows()

logger.info("Ellipse Single Detected {}, Multiple Ellipse {}, Total Images {}, Percentage Detection {}".format(
    (ellipse_detected - multiple_ellipses), multiple_ellipses, total_images,
    (ellipse_detected - multiple_ellipses) / total_images))
logger.info("EXPERIMENT END")
logger.info("*" * 50)
