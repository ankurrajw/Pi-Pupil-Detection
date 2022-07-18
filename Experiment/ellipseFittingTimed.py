import cv2 as cv
import numpy as np
from datetime import datetime
import time
import os
import random as rng
import logging
import pandas as pd

srcPiCam = 'libcamerasrc ! video/x-raw,width=640,height=480,framerate=90/1 ! videoflip method=clockwise ! videoconvert ! appsink'
cap = cv.VideoCapture(srcPiCam)

'''Change the parameters to conduct a real time detection'''
CANNY_THRESHOLD = 24
MEDIAN_BLUR_K_SIZE = 17
MORPH_K_SIZE = 1

RES_H = 640
RES_W = 480
ROI_FACTOR = 0.6

'''
RES_H = 640
RES_W = 480
ROI_FACTOR = 0.6
'''

# Time calculation
# columns = ('values', 'mean_time_taken(s)', 'std(s)')
columns = ('bluring','pre_process', 'find_contours', 'filter_contours', 'post_process', 'operation_complete')
df_experiment = pd.DataFrame(columns=columns)


def create_workspace():
    base_path = "/home/ubicomp/Desktop/master-thesis-eye-tracking/Results/Ellipse/"
    time_right_now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    name_workspace = base_path + "Ellipse" + time_right_now + '/'
    if not os.path.exists(name_workspace):
        os.makedirs(name_workspace)
        print("folder name", name_workspace)
    return name_workspace


def create_directory_timing():
    base_path = "./Timed_Experiment/"
    path_dir = base_path + 'resolution'+str(RES_H)+str(RES_W)+"/"
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
        print("folder name", path_dir)
    return path_dir


count = 0
ellipse_detected = 0
multiple_ellipses = 0
fps_start_time = 0
fps = 0
total_images = 60
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
    """TODO filter contours to get ellipses based on area and circularity
    DOCUMENTATION : Why we need to do a convex hull operation on the contour instead of finding the circularity directly
    from contour ?
    ANS: Since pixels of contour leads to a higher th_value of circularity > 200. Doing a convex hull leads to a lower
    th_value since we don't deal with discritised pixels """
    _contours_filtered = []
    print("Initial Contours : {}".format(len(_contours)))
    print("Filtered Contours:")
    for i, c in enumerate(_contours):
        try:
            convex_hull = cv.convexHull(c)
            area_hull = cv.contourArea(convex_hull)
            # print("{} area convex hull {}".format(i, area_hull))
            if 900 < area_hull < 3000:  # filtering based on area
                circumference_hull = cv.arcLength(convex_hull, True)
                circularity_hull = (4 * np.pi * area_hull) / circumference_hull ** 2
                if 0.9 < circularity_hull:  # filtering based on circularity
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
        #print("Area Ellipse :{} Area Contour Hull :{}".format(area_ellipse, area_contour_hull))
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

def find_centre_pupil(_pupil_locations, _contours):
    for i, c in enumerate(_contours):
        M = cv.moments(c)
        pupilX = int(M["m10"]/M["m00"])
        pupilY = int(M["m01"]/M["m00"])
        _pupil_locations.append(f'{pupilX},{pupilY}')
    return _pupil_locations

logger.info(f"Values for Canny -{CANNY_THRESHOLD} Blur K size -{MEDIAN_BLUR_K_SIZE} Morph -{MORPH_K_SIZE}")
operation_find_contours = []
operation_filter_contours = []
operation_complete = []
operation_pre_process = []
operation_post_process = []
operation_bluring = []
pupil_locations = []
while count < total_images:
    start_operation_complete_timer = time.process_time()
    ret, frame = cap.read()
    '''fps_end_time = time.time()
    time_diff = fps_end_time - fps_start_time
    fps = 1 / time_diff
    fps_start_time = fps_end_time
    fps_text = "FPS: {:.2f}".format(fps)
    '''
    if ret:
        # pre process
        start_pre_process_timer = time.process_time()
        roi = frame[0:round(ROI_FACTOR*RES_H), 0:RES_W]
        output = roi.copy()
        src_gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
        start_bluring_timer = time.process_time()
        src_gray = cv.medianBlur(src_gray, MEDIAN_BLUR_K_SIZE)
        end_bluring_timer = time.process_time()
        operation_bluring.append(end_bluring_timer - start_bluring_timer)
        
        kernel = np.ones((MORPH_K_SIZE, MORPH_K_SIZE), np.uint8)
        opening = cv.morphologyEx(src_gray, cv.MORPH_OPEN, kernel)
        canny_output = cv.Canny(opening, CANNY_THRESHOLD, CANNY_THRESHOLD * 2)
        end_pre_process_timer = time.process_time()
        operation_pre_process.append(end_pre_process_timer - start_pre_process_timer)

        start_contour_timer = time.process_time()
        contours, _ = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        end_contour_timer = time.process_time()
        operation_find_contours.append(end_contour_timer - start_contour_timer)

        start_filter_timer = time.process_time()
        contours_filtered = filter_contour(contours)
        end_filter_timer = time.process_time()
        operation_filter_contours.append(end_filter_timer - start_filter_timer)

        # post process
        start_post_process_timer = time.process_time()
        #drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
        #drawing = draw_ellipse(drawing, contours_filtered)
        #cv.imwrite(folder_name + "ellipse" + str(count) + ".png", drawing)

        '''Comment if colour images are not needed'''
        #colour_image = draw_ellipse_rgb(roi, contours_filtered)
        #cv.imwrite(folder_name + "colour" + str(count) + ".png", colour_image)
        pupil_locations = find_centre_pupil(pupil_locations, contours_filtered)

        ellipse_detected += len(contours_filtered)
        if len(contours_filtered) > 1:
            multiple_ellipses += len(contours_filtered) - 1
        end_post_process_timer = time.process_time()
        operation_post_process.append(end_post_process_timer - start_post_process_timer)
        end_operation_complete_timer = time.process_time()
        operation_complete.append(end_operation_complete_timer - start_operation_complete_timer)
        count += 1

cap.release()
cv.destroyAllWindows()

logger.info("Ellipse Single Detected {}, Multiple Ellipse {}, Total Images {}, Percentage Detection {}".format(
    (ellipse_detected - multiple_ellipses), multiple_ellipses, total_images,
    (ellipse_detected - multiple_ellipses) / total_images))
logger.info("EXPERIMENT END")
logger.info("*" * 50)


# Filling time values
df_experiment['pre_process'] = operation_pre_process
df_experiment['find_contours'] = operation_find_contours
df_experiment['filter_contours'] = operation_filter_contours
df_experiment['post_process'] = operation_post_process
df_experiment['operation_complete'] = operation_complete
df_experiment['bluring'] = operation_bluring

directory_timing = create_directory_timing()
time_right_now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
df_experiment.to_csv(directory_timing + f"Experiment_{time_right_now}_{CANNY_THRESHOLD}_{MEDIAN_BLUR_K_SIZE}.csv", sep=',', index=False)

with open(directory_timing+f"Experiment_{time_right_now}_{CANNY_THRESHOLD}_{MEDIAN_BLUR_K_SIZE}_pupil_location.csv", 'w') as file:
    for location in pupil_locations:
        file.write(f'{location}\n')

'''
# Time Calculation
df_find_contours = pd.DataFrame(
    {'values': 'find_contours', 'mean_time_taken(s)': np.mean(operation_find_contours),
     'std(s)': np.std(operation_find_contours)}, index=[0])
df_filter_contours = pd.DataFrame(
    {'values': 'filter_contours', 'mean_time_taken(s)': np.mean(operation_filter_contours),
     'std(s)': np.std(operation_filter_contours)}, index=[0])
df_operation_complete = pd.DataFrame(
    {'values': 'operation_complete', 'mean_time_taken(s)': np.mean(operation_complete),
     'std(s)': np.std(operation_complete)}, index=[0])
df_operation_pre_process = pd.DataFrame(
    {'values': 'pre_process', 'mean_time_taken(s)': np.mean(operation_pre_process),
     'std(s)': np.std(operation_pre_process)}, index=[0])
df_operation_post_process = pd.DataFrame(
    {'values': 'post_process', 'mean_time_taken(s)': np.mean(operation_post_process),
     'std(s)': np.std(operation_post_process)}, index=[0])
df_experiment = pd.concat([df_experiment, df_find_contours], ignore_index=True)
df_experiment = pd.concat([df_experiment, df_filter_contours], ignore_index=True)
df_experiment = pd.concat([df_experiment, df_operation_complete], ignore_index=True)
df_experiment = pd.concat([df_experiment, df_operation_pre_process], ignore_index=True)
df_experiment = pd.concat([df_experiment, df_operation_post_process], ignore_index=True)
print(df_experiment)
'''
