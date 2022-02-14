import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


def reloadImage():
    img = cv.imread("imPi8.png")
    img = img[220:640, 0:480]
    return img


def trackbarCallback(x):
    print(f"threshold value {x}")


cv.namedWindow("test")
cv.resizeWindow("test", (500, 500))
cv.createTrackbar("threshold 1", "test", 0, 1000, trackbarCallback)
cv.createTrackbar("threshold 2", "test", 0, 1000, trackbarCallback)

# roi = cv.dilate(roi, None,iterations = 1)
# roi = cv.erode(roi, None,iterations = 1)

while True:
    img_copy = cv.imread("imPi8.png")
    img = cv.imread('imPi8.png', 0)
    img = cv.GaussianBlur(img, (3, 3), 30)
    roi = img[220:640, 0:480]
    roi_copy = img_copy[220:640, 0:480]
    th1 = cv.getTrackbarPos("threshold 1", "test")
    th2 = cv.getTrackbarPos("threshold 2", "test")
    edges = cv.Canny(roi, th1, 2 * th1, apertureSize=3)

    contours, _ = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # cv.drawContours(roi_copy, contours, -1, (0, 0, 255), 3)

    print(contours)
    # cv.imshow("original",roi_copy)
    # cv.imshow("canny",edges)
    # cv.imshow("gray",roi)

    key = cv.waitKey(1)
    if key == 27:
        break

cv.destroyAllWindows()
