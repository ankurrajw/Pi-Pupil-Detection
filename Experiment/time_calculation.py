import time
import cv2 as cv
import glob
import pandas as pd
import numpy as np
np.set_printoptions(suppress=True)
folder_name = r"C:\Users\Ankur\Desktop\Uni Siegen\SEM5\Eye Detection\Project-code-Ankur\master-thesis-eye-tracking\Results\infrared\*.png"
# folder_name = r"C:\Users\Ankur\Desktop\Uni Siegen\SEM5\Eye Detection\Project-code-Ankur\master-thesis-eye-tracking\Results\Inference\SidePupilImages\*.png"
folder_images = glob.glob(folder_name)
folder_images = sorted(folder_images)
columns = ('values', 'mean_time_taken(s)', 'std(s)')

df_experiment = pd.DataFrame(columns=columns)
operation_file_open = []
for i in folder_images:
    start = time.process_time()
    img = cv.imread(i)
    roi = img[220:640, 0:480].copy()
    end = time.process_time()
    operation_file_open.append(end - start)

s2 = pd.DataFrame(
    {'values': 'test', 'mean_time_taken(s)': np.mean(operation_file_open), 'std(s)': np.std(operation_file_open)}, index=[0])
df_experiment = pd.concat([df_experiment, s2], ignore_index=True)
print(df_experiment)
