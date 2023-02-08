import cv2
import numpy as np
from datetime import datetime
import time
import os
import logging

srcPiCam = 'libcamerasrc ! video/x-raw,width=640,height=480,framerate=90/1 ! videoflip method=clockwise ! videoconvert ! appsink'
cap = cv2.VideoCapture(srcPiCam)


def create_workspace():
    base_path = "PATH_FOLDER"
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
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        cl1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe = cl1.apply(gray)
        gray = cv2.medianBlur(clahe, 9)
        _, threshold = cv2.threshold(gray, 132, 255, cv2.THRESH_BINARY_INV)

        circles = cv2.HoughCircles(threshold, cv2.HOUGH_GRADIENT, 1, 100, param1=40, param2=15, minRadius=20,
                                   maxRadius=40)
        if circles is not None:
            detected_circles = np.uint16(np.around(circles))
            print(detected_circles)
            print(max(detected_circles[0, :, 2]))
            print(np.shape(detected_circles))
            # var = detected_circles[detected_circles[0,:, 2].argsort()]
            # print(var)
            # detected_circles = sorted(detected_circles[0], reverse=True)
            # print(detected_circles)

            test = []
            for idx, data in enumerate(detected_circles[0, :]):
                # Dirty implementation
                if data[0] > np.shape(roi)[0] - 1 or data[1] > np.shape(roi)[1] - 1:
                    test.append(idx)
                if data[2] > 120:
                    test.append(idx)

            print(test)
            detected_circles = np.reshape(detected_circles,
                                          (np.shape(detected_circles)[1], np.shape(detected_circles)[2]))
            detected_circles = np.delete(detected_circles, tuple(test), 0)
            print(detected_circles)
            for idx, (x, y, r) in enumerate(detected_circles):
                count = count + 1
                # if r == max(detected_circles[0,:,2]):
                print(f"{idx}")
                print(f"Value X {x} Y {y} R {r}")
                print("center pixel color BGR : ", output[x, y, :])
                print("center pixel color GRAY : ", gray[x, y])
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(output, f"{idx}", (x, y), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(output, fps_text, (5, 30), font, 1, (255, 255, 255), 1)
                cv2.circle(output, (x, y), r, (0, 255, 0), 3)
                cv2.circle(output, (x, y), 2, (255, 255, 0), 3)
                cv2.imwrite(folder_name + "hough_circle" + str(count) + ".png", output)
        else:
            font = cv2.FONT_HERSHEY_SIMPLEX
            count = count + 1
            cv2.putText(frame, fps_text, (5, 30), font, 1, (255, 255, 255), 1)
            cv2.imwrite(folder_name + "hough_circle" + str(count) + ".png", frame)

# cv2.imshow("Image", output)
# cv2.imshow("gray",gray)
# cv2.imshow("threshold_canny", threshold_canny)
cv2.waitKey(0)
cv2.destroyAllWindows()
