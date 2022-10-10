import cv2 as cv
import time
from datetime import datetime
import os

SRCPICAM = 'libcamerasrc ! video/x-raw,width=640,height=480 ! videoflip method=clockwise ! videoconvert ! appsink'
cap = cv.VideoCapture(SRCPICAM)

""" change device parameter by checking the device id in v4l2
command v4l2-ctl --list-devices
"""
SRCUSBCAM = 'v4l2src device = /dev/video2 ! video/x-raw,width=640,height=480 ! videoconvert ! appsink'
cap2 = cv.VideoCapture(SRCUSBCAM)


def create_workspace():
    base_path = "CHANGE PATH/"
    time_right_now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    name_workspace = base_path + "Data_Pupil_Capture" + time_right_now + '/'
    if not os.path.exists(name_workspace):
        os.makedirs(name_workspace)
        print("folder name", name_workspace)
    return name_workspace


if __name__ == '__main__':
    folder_path = create_workspace()
    count_pics = 0
    while True:
        success, img = cap.read()
        # success2, img2 = cap2.read()
        # time.sleep(1)

        cv.imwrite(folder_path + "imPi" + str(count_pics) + ".png", img)
        # cv.imwrite("Results/imUSB" + str(count_pics) + ".png", img2)
        count_pics = count_pics + 1
        print(f"Pic Captured :{count_pics}")
        if count_pics == 100:  # change according to num pics needed
            print("Completed")
            break
    cap.release()
