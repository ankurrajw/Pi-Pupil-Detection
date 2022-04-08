import cv2 as cv
import numpy as np
from datetime import datetime
import time
import os
import random as rng


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

def filter_contour(contours):
    """TODO filter contours to get ellipses based on area and circularity
    DOCUMENTATION : Why we need to do a convex hull operation on the contour instead of finding the circularity directly
    from contour ?
    ANS: Since pixels of contour leads to a higher th_value of circularity > 200. Doing a convex hull leads to a lower
    th_value since we don't deal with discritised pixels """
    contours_filtered = []
    print("Initial Contours : {}".format(len(contours)))
    print("Filtered Contours:")
    for i, c in enumerate(contours):
        try:
            convex_hull = cv.convexHull(c)
            area_hull = cv.contourArea(convex_hull)
            # print("{} area convex hull {}".format(i, area_hull))
            if 600 < area_hull:  # filtering based on area
                circumference_hull = cv.arcLength(convex_hull, True)
                circularity_hull = (4 * np.pi * area_hull) / circumference_hull ** 2
                if 0.8 < circularity_hull:  # filtering based on circularity
                    print("convex hull :{} Circularity :{} Area : {}".format(i, circularity_hull, area_hull))
                    contours_filtered.append(convex_hull)
        except ZeroDivisionError:
            print("Division by zero for contour {}".format(i))
    return contours_filtered


def draw_ellipse(drawing, contours_filtered):
    minEllipse = [None] * len(contours_filtered)
    for i, c in enumerate(contours_filtered):
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        minEllipse[i] = cv.fitEllipse(c)
        cv.drawContours(drawing, contours_filtered, i, color)
        (x, y), (MA, ma), angle = minEllipse[i]
        area_contour_hull = cv.contourArea(c)
        area_ellipse = (np.pi / 4) * MA * ma
        print("Area Ellipse :{} Area Contour Hull :{}".format(area_ellipse, area_contour_hull))
        cv.ellipse(drawing, minEllipse[i], color, 2)


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
    if ret:
        roi = frame[220:640, 0:480]
        output = roi.copy()
        src_gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
        #cl1 = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        #clahe = cl1.apply(src_gray)

        src_gray = cv.medianBlur(src_gray, MEDIAN_BLUR_K_SIZE)
        kernel = np.ones((MORPH_K_SIZE, MORPH_K_SIZE), np.uint8)
        # _, src_gray = cv.threshold(src_gray, 100, 255, cv.THRESH_BINARY_INV)
        opening = cv.morphologyEx(src_gray, cv.MORPH_OPEN, kernel)

        canny_output = cv.Canny(opening, CANNY_THRESHOLD, CANNY_THRESHOLD * 2)
        contours, _ = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours_filtered = filter_contour(contours)

        drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
        draw_ellipse(drawing, contours_filtered)

        cv.imwrite(folder_name + "ellipse" + str(count) + ".png", drawing)
'''
        if contours is not None:
            count += 1
            minEllipse = [None] * len(contours)
            """TODO: Why the for loop is done twice?"""
            for i, c in enumerate(contours):
                if 50 < c.shape[0] < 150:
                    minEllipse[i] = cv.fitEllipse(c)
                    print(minEllipse[i])
            # drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

            for i, c in enumerate(contours):
                color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
                # contour
                # cv.drawContours(drawing, contours, i, color)
                # ellipse
                if 50 < c.shape[0] < 150:
                    cv.ellipse(roi, minEllipse[i], color=color, thickness=2)
                    cv.imwrite(folder_name + "ellipse" + str(count) + ".png", roi)

        else:
            count += 1
            cv.imwrite(folder_name + "ellipse" + str(count) + ".png", frame)
'''

cap.release()
