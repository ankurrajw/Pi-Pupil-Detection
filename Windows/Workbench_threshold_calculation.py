import cv2 as cv
import numpy as np
import random as rng
import os
import pandas as pd
import logging
import glob
from datetime import datetime


# create a logger with name of the file
def create_logger():
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)
    ch = logging.FileHandler("../log_threshold_determination.log")
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    _logger.addHandler(ch)

    _logger.info("*" * 50)
    _logger.info("EXPERIMENT START")
    return _logger


logger = create_logger()
MEDIAN_BLUR_K_SIZE_VALUES = [7, 9, 11, 13, 15, 17, 19, 21, 23]

MORPH_VALUES = 1
MIN_AREA_HULL = 400
MAX_AREA_HULL = 1000
MIN_CIRCULARITY = 0.9

CANNY_THRESHOLD_VALUES = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 35, 40, 55, 60, 65,
                          70]  # list for canny values
columns = ('image_name', 'threshold_canny', 'kernel_size_blur', 'area_convex_hull', 'area_ellipse',
           'circularity_hull')

# dataframe experiment
df_experiment = pd.DataFrame(columns=columns)


def filter_contour(contours):
    _contours_filtered = []
    # print("Initial Contours : {}".format(len(contours)))
    # print("Filtered Contours:")
    for i, c in enumerate(contours):
        try:
            convex_hull = cv.convexHull(c)
            area_hull = cv.contourArea(convex_hull)
            # print("{} area convex hull {}".format(i, area_hull))
            if MIN_AREA_HULL < area_hull < MAX_AREA_HULL:  # filtering based on area
                circumference_hull = cv.arcLength(convex_hull, True)
                circularity_hull = (4 * np.pi * area_hull) / circumference_hull ** 2
                if MIN_CIRCULARITY < circularity_hull:  # filtering based on circularity
                    # print("convex hull :{} Circularity :{} Area : {}".format(i, circularity_hull, area_hull))
                    _contours_filtered.append(c)
        except ZeroDivisionError:
            print("Division by zero for contour {}".format(i))
    return _contours_filtered


def draw_ellipse(drawing, _contours_filtered):
    minEllipse = [None] * len(_contours_filtered)
    for i, c in enumerate(_contours_filtered):
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        minEllipse[i] = cv.fitEllipse(c)
        cv.drawContours(drawing, _contours_filtered, i, color)
        (x, y), (MA, ma), angle = minEllipse[i]
        area_contour_hull = cv.contourArea(c)
        area_ellipse = (np.pi / 4) * MA * ma
        # print("Area Ellipse :{} Area Contour Hull :{}".format(area_ellipse, area_contour_hull))
        cv.ellipse(drawing, minEllipse[i], color, 2)


def fill_df(contours, **kwargs):
    data_list_ = []
    for i, c in enumerate(contours):
        try:
            convex_hull = cv.convexHull(c)
            area_hull = cv.contourArea(convex_hull)
            # area_contour = cv.contourArea(c)
            # print("{} area convex hull {}".format(i, area_hull))
            if MIN_AREA_HULL < area_hull < MAX_AREA_HULL:  # filtering based on area
                circumference_hull = cv.arcLength(convex_hull, True)
                circumference_contour = cv.arcLength(c, True)
                circularity_hull = (4 * np.pi * area_hull) / circumference_hull ** 2
                # circularity_contour = (4 * np.pi * area_contour) / circumference_hull ** 2
                if MIN_CIRCULARITY < circularity_hull:  # filtering based on circularity
                    minEllipse = cv.fitEllipse(c)
                    (x, y), (MA, ma), angle = minEllipse
                    area_contour_hull = cv.contourArea(c)
                    area_ellipse = (np.pi / 4) * MA * ma

                    '''Fill Dataframe'''
                    series = {'image_name': kwargs['image_name'],
                              'threshold_canny': kwargs['canny_threshold'],
                              'kernel_size_blur': kwargs['blur_k_size'],
                              'area_convex_hull': area_hull,  # 'area_contour': area_contour_hull,
                              'area_ellipse': area_ellipse, 'circularity_hull': circularity_hull,
                              'circularity_contour': circumference_contour
                              }

                    data_list_.append(series)
        except ZeroDivisionError:
            print("Division by zero for contour {}".format(i))
    return data_list_


def morphology_operations(*args, **kwargs):
    """Get Trackbar positions
    :param *args:
    :param **kwargs:
    """

    roi = src_image[0:420, 0:480]
    output = roi.copy()
    src_gray_original = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    src_gray = src_gray_original.copy()
    # Blur Operation

    src_gray = cv.medianBlur(src_gray, kwargs['blur_k_size'])

    # Opening operation
    kernel = np.ones((kwargs['morph_k_size'], kwargs['morph_k_size']), np.uint8)
    opening = cv.morphologyEx(src_gray, cv.MORPH_OPEN, kernel)

    # Canny
    canny_output = cv.Canny(opening, kwargs['canny_threshold'], kwargs['canny_threshold'] * 2)

    # Contour
    contours, _ = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # print(kwargs)
    _data_list = fill_df(contours, **kwargs)

    _contours_filtered = filter_contour(contours)

    # blank canvas
    # drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    # draw_ellipse(drawing, _contours_filtered)

    # cv.imshow("source", output)
    # cv.imshow("drawing", drawing)
    # cv.imshow(result_window, canny_output)
    # print("*" * 30)
    # print(
    #    "Values: Median Blur Kernel Size : {} Opening Kernel Size : {} Canny : {}".format(kwargs['blur_k_size'],
    #                                                                                      kwargs['morph_k_size'],
    #                                                                                     kwargs['canny_threshold']))
    # print("*" * 30)
    return _contours_filtered, _data_list, len(contours)


result_window = "results"

folder_path = r"C:\Users\Ankur\Desktop\Data_Pupil_Capture09_04_2022_12_23_51"

logger.info("Folder Name :{}".format(folder_path))
ellipse_detected = 0
total_images = len(os.listdir(folder_path))


def calculate_minimum_area(contours):
    """multiple contours min area calculation for best fitting"""
    if len(contours) == 0:
        return 0

    _area_diff_min = []
    for _, c in enumerate(contours):
        try:
            convex_hull = cv.convexHull(c)
            area_hull = cv.contourArea(convex_hull)
            minEllipse = cv.fitEllipse(c)
            (_, _), (MA, ma), angle = minEllipse
            area_ellipse = (np.pi / 4) * MA * ma
            area_diff_contour = np.abs(area_hull - area_ellipse)
            # print("hull area - {}, ellipse area - {}, area_diff - {}".format(area_hull,area_ellipse,area_diff_contour))
            _area_diff_min.append(area_diff_contour)
        except ZeroDivisionError:
            print("Division by zero for contour {}, {}".format(i, c))

    return min(_area_diff_min)


if __name__ == '__main__':
    time_right_now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    threshold_values = []
    k_size_values = []

    image_names = []
    loss_list_mean = pd.DataFrame(index=MEDIAN_BLUR_K_SIZE_VALUES, columns=CANNY_THRESHOLD_VALUES)
    loss_list_sigma = pd.DataFrame(index=MEDIAN_BLUR_K_SIZE_VALUES, columns=CANNY_THRESHOLD_VALUES)

    for i, th_value in enumerate(CANNY_THRESHOLD_VALUES):
        print("loop {} of {}".format(i, len(CANNY_THRESHOLD_VALUES)))
        for _, k_size_value in enumerate(MEDIAN_BLUR_K_SIZE_VALUES):
            loss_list = []
            src_image_folder_path = os.path.join(folder_path, "*.png")
            for image_name in glob.iglob(src_image_folder_path):

                # print("Image Name {}".format(src_image_folder_path))
                src_image = cv.imread(image_name)

                """min area for set of threshold and k_size values"""

                contours_filtered, data_list, num_initial_contours = morphology_operations(0, image_name=image_name,
                                                                                           canny_threshold=th_value,
                                                                                           blur_k_size=k_size_value,
                                                                                           morph_k_size=MORPH_VALUES,
                                                                                           data_frame=df_experiment)
                area_diff_min_contour = calculate_minimum_area(contours_filtered)
                # if area_diff_min_contour 200:
                # pass

                """ loss  calculation
                num_initial_contours/4 => penality increases if number of contour is greater than 4
                np.exp(num_initial_contours / 25)
                
                constant for no circle identification
                
                area_best_fit
                """

                loss = num_initial_contours + area_diff_min_contour + (1000 if (area_diff_min_contour == 0) else 0)
                # print("num_initial_contour - {} loss - {}".format(num_initial_contours,loss))
                loss_list.append(loss)

                for data in data_list:
                    df_experiment = df_experiment.append(data, ignore_index=True)

                key = cv.waitKey(1)
                if key == 27:
                    exit(0)
            loss_list_mean.loc[k_size_value, th_value] = np.mean(loss_list)
            loss_list_sigma.loc[k_size_value, th_value] = np.std(loss_list)
    df_experiment.to_csv(folder_path + "\{}_test_{}.csv".format(os.path.basename(folder_path), time_right_now), sep=',',
                         index=False)
    loss_list_mean.to_csv(folder_path + "\{}_loss_mean_{}.csv".format(os.path.basename(folder_path), time_right_now),
                          sep=',')
    loss_list_sigma.to_csv(folder_path + "\{}_loss_sigma_{}.csv".format(os.path.basename(folder_path), time_right_now),
                           sep=',')
    cv.destroyAllWindows()
    logger.info("EXPERIMENT END")
    logger.info("*" * 50)
