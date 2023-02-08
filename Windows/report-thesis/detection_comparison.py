import glob

import cv2 as cv
import numpy as np
import random as rng
import pandas as pd
from pathlib import Path

#folder_path = r'C:\Users\Ankur\Downloads\LPW'
# 25 canny original 23 blur
CANNY_THRESHOLD = 10
MEDIAN_BLUR_K_SIZE = 23
MORPH_K_SIZE = 1

folder_path = r"C:\Users\Ankur\Desktop\Uni Siegen\SEM5\Eye Detection\Project-code-Ankur\master-thesis-eye-tracking\Windows\report-thesis\evaluation\without_glasses\7"
file_path = glob.glob(folder_path+r"\*avi")


def filter_contour(_contours):
    _contours_filtered = []
    #print("Initial Contours : {}".format(len(_contours)))
    #print("Filtered Contours:")
    for i, c in enumerate(_contours):
        try:
            convex_hull = cv.convexHull(c)
            area_hull = cv.contourArea(convex_hull)
            # print("{} area convex hull {}".format(i, area_hull))
            if 2000 < area_hull < 30000:  # filtering based on area
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
        # print("Area Ellipse :{} Area Contour Hull :{}".format(area_ellipse, area_contour_hull))
        cv.ellipse(_drawing, minEllipse[i], color=color, thickness=2)
    return _drawing


def calculate_centre(_contours_filtered):
    _location = []
    for i, c in enumerate(_contours_filtered):
        moments = cv.moments(c)

        area = moments['m00']
        x = moments['m10'] / area + 1e-5
        y = moments['m01'] / area + 1e-5
        _location.append((x, y))
    return _location


for file in file_path:
    cap = cv.VideoCapture(file)
    print(file)
    column = ('x', 'y', 'extra')
    df_pupil_location = pd.DataFrame(columns=column)
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            src_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            src_gray = cv.medianBlur(src_gray, MEDIAN_BLUR_K_SIZE)
            kernel = np.ones((MORPH_K_SIZE, MORPH_K_SIZE), np.uint8)
            opening = cv.morphologyEx(src_gray, cv.MORPH_OPEN, kernel)

            canny_output = cv.Canny(opening, CANNY_THRESHOLD, CANNY_THRESHOLD * 2)
            contours, _ = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours_filtered = filter_contour(contours)

            drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
            drawing = draw_ellipse(drawing, contours_filtered)

            location = calculate_centre(contours_filtered)
            if not location:
                data_entry = pd.DataFrame.from_dict({
                    'x': [0],
                    'y': [0],
                    'extra': [0]})
                df_pupil_location = pd.concat([df_pupil_location, data_entry], ignore_index=True)
                # print("empty array")
            else:
                data_entry = pd.DataFrame.from_dict({
                    'x': [location[0][0]],
                    'y': [location[0][1]],
                    'extra': [location[1:]]})

                #print(f"location - {data_entry}")
                df_pupil_location = pd.concat([df_pupil_location, data_entry], ignore_index=True)

            cv.imshow("output", frame)
            cv.imshow("canny", canny_output)
            cv.imshow("pupil", drawing)
            key = cv.waitKey(10000)
            if key == 27:
                break
        else:
            break
    file_name = Path(file).stem
    # df_pupil_location.to_csv(folder_path + rf"\Experiment_{int(file_name)}_canny_{CANNY_THRESHOLD}_blur_{MEDIAN_BLUR_K_SIZE}.csv", sep='\t', index=False)
    cap.release()

cv.destroyAllWindows()