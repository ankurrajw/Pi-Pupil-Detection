import cv2 as cv
import numpy as np
import argparse
import time
from datetime import datetime
import os
import RPi.GPIO as GPIO




class data_collector:
    landmarks = [(0.1, 0.1), (0.1, 0.9), (0.5, 0.5), (0.9, 0.9), (0.9, 0.1)]
    length = 20
    PIN = 4

    def __init__(self, window, num_pics):
        self.black_window = window
        self.window_width = window.shape[0]
        self.window_height = window.shape[1]
        self.num_pics_per_land_mark = num_pics
        self.cap_pi = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(data_collector.PIN,GPIO.OUT)
        pass

    def add_cross(self):
        """ Add cross to the frame on specified landmarks """
        for i, j in data_collector.landmarks:
            cv.line(self.black_window, (round(i * self.window_height) + data_collector.length,
                                        round(j * self.window_width) + data_collector.length),
                    (round(i * self.window_height) - data_collector.length,
                     round(j * self.window_width) - data_collector.length), color=(0, 0, 255), thickness=5)

            cv.line(self.black_window, (round(i * self.window_height) - data_collector.length,
                                        round(j * self.window_width) + data_collector.length),
                    (round(i * self.window_height) + data_collector.length,
                     round(j * self.window_width) - data_collector.length), color=(0, 0, 255), thickness=5)
        return self.black_window

    def loc_to_pixel(self, loc):
        return (round(loc[1] * self.window_width) - data_collector.length,
                round(loc[0] * self.window_height) + data_collector.length)

    def collect_pics_experiment(self):
        name_workspace = data_collector.create_workspace(
            r"/home/ubicomp/Desktop/master-thesis-eye-tracking/data-collection/")
        count = 0
        max_len_experiment = len(data_collector.landmarks)
        while count < max_len_experiment:
            key = cv.waitKey()
            if key == 27 or key == ord("q"):
                cv.destroyAllWindows()
                break
            elif key == ord("n"):
                self.collect_pictures(name_workspace)
                count += 1
        print("Program Exit!!")

    def collect_pictures(self, name_workspace):
        self.cap_pi, _ = data_collector.open_video_feed()
        count_pics = 0
        while self.cap_pi.isOpened():  # or cap_usb
            self.led_on(True)
            ret, img = self.cap_pi.read()
            # success2, img2 = cap2.read()
            time.sleep(0.01)
            time_right_now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")[:-3]
            if ret:
                cv.imwrite(name_workspace + "imPi" + time_right_now + ".png", img)
                # cv.imwrite("Results/imUSB" + str(count_pics) + ".png", img2)
                count_pics = count_pics + 1
                print(f"Pic Captured :{count_pics}")
                if count_pics == self.num_pics_per_land_mark:  # change according to num pics needed
                    print("Completed")
                    self.led_on(False)
                    self.cap_pi.release()
                    break
                    
                    # cap_usb.release()
            if not ret:
                print("frame empty")
                continue
    @staticmethod
    def open_video_feed():
        SRCPICAM = 'libcamerasrc ! video/x-raw,width=640,height=480 ! videoflip method=clockwise ! videoconvert ! appsink drop=True'
        cap_pi = cv.VideoCapture(SRCPICAM)  # cv.CAP_GSTREAMER for linux
        cap_pi.set(cv.CAP_PROP_FPS, 90)
        
        """ change device parameter by checking the device id in v4l2
        command v4l2-ctl --list-devices
        """
        # SRCUSBCAM = 'v4l2src device = /dev/video2 ! video/x-raw,width=640,height=480 ! videoconvert ! appsink'
        # cap_usb = cv.VideoCapture(SRCUSBCAM)
        return cap_pi, "RETURN_SRC_USB"

    @staticmethod
    def create_workspace(path):
        base_path = path
        time_right_now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        name_workspace = base_path + "Data_Pupil_Capture" + time_right_now + '/'
        if not os.path.exists(name_workspace):
            os.makedirs(name_workspace)
            print("folder name", name_workspace)
        return name_workspace
    
    def led_on(self,status):
        
        if (status):
            GPIO.output(data_collector.PIN,GPIO.HIGH)
        else:
            GPIO.output(data_collector.PIN,GPIO.LOW)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    """TODO : Find a way to not accept negative numbers as arguments"""
    parser.add_argument("-np", "--num_pics", help="Number of pictures that must be collected per land mark", type=int,
                        default=30)
    args = parser.parse_args()

    print("{} pics should be collected".format(args.num_pics * len(data_collector.landmarks)))

    window_name = "Data_Collector"
    window_size = [1920, 1080]
    cv.namedWindow(window_name)
    cv.resizeWindow(window_name, window_size[1], window_size[0])
    drawing = np.zeros((window_size[1], window_size[0], 3), dtype=np.uint8)

    experiment = data_collector(window=drawing, num_pics=args.num_pics)
    test = experiment.add_cross()

    cv.imshow(window_name, test)
    experiment.collect_pics_experiment()
    cv.destroyAllWindows()
