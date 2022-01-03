"""
Author : Ankur Raj

This approach of pupil detection is based on detection using threshold.

Input An image of pupil (480*640)
Output An image with pupil marked in addition to auxiliary images
"""

import cv2
import math


def trackbarCallback(x):
    print(f"threshold value {x}")


cv2.namedWindow("test")
cv2.createTrackbar("threshold", "test", 0, 255, trackbarCallback)

while True:
    frame = cv2.imread("Results/imPi8.png")  # input image

    roi = frame[220:640, 0:480]
    gray_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    #gray_frame = cv2.GaussianBlur(gray_frame, (3, 3), 40)


    value_threshold = cv2.getTrackbarPos("threshold", "test")
    #value_threshold = 40  # it works best for this value

    _, threshold = cv2.threshold(gray_frame, value_threshold, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    print("Start Here")
    for cnt in contours:
        area = cv2.contourArea(cnt)

        #cnt = cv2.convexHull(cnt)

        if area < 1000:
            continue
        circumference = cv2.arcLength(cnt, True)
        try:
            circularity = circumference ** 2 / (4 * math.pi * area)
            print(f"circularity {circularity}")
        except ZeroDivisionError:
            print("Zero Division Error")
        print(f"area {area}")

        # Calculate centre of the contour
        m = cv2.moments(cnt)
        if m['m00'] != 0:
            center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
            print(center)
            centerFrame = (int(m['m10'] / m['m00']) + 220, int(m['m01'] / m['m00']))
            cv2.circle(roi, center, 3, (0, 0, 255), -1)
            #cv2.circle(frame, centerFrame, 5, (0, 0, 255), -1)

        # fit an ellipse around the contour and draw it into the image
        try:
            ellipse = cv2.fitEllipse(cnt)
            cv2.ellipse(roi, ellipse, color=(0, 255, 0))
        except:
            pass

        break

    #cv2.imshow("image", frame)
    cv2.imshow("gray frame", gray_frame)
    cv2.imshow("threshold image", threshold)
    cv2.imshow("roi", roi)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()

