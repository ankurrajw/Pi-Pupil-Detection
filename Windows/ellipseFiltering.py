import cv2 as cv
import numpy as np
import random as rng

rng.seed(12345)

src_image = cv.imread(
    r"C:\Users\Ankur\Desktop\Uni Siegen\SEM5\Eye Detection\Project-code-Ankur\master-thesis-eye-tracking\Results\infrared\imPi21.png")
# src_image = cv.imread(r"C:\Users\Ankur\Desktop\Uni Siegen\SEM5\Eye Detection\Project-code-Ankur\master-thesis-eye-tracking\Results\Inference\SidePupilImages\hough_circle342.png")
# src_image = cv.imread(r"C:\Users\Ankur\Desktop\Uni Siegen\SEM5\Eye Detection\Project-code-Ankur\master-thesis-eye-tracking\Results\Hough21_01_2022_16_01_18\hough_circle281.png")

roi = src_image[220:640, 0:480]
output = roi.copy()
src_gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
cl1 = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
clahe = cl1.apply(src_gray)

src_gray = cv.medianBlur(clahe, 9)
kernel = np.ones((5, 5), np.uint8)
_, src_gray = cv.threshold(src_gray, 100, 255, cv.THRESH_BINARY_INV)
opening = cv.morphologyEx(src_gray, cv.MORPH_OPEN, kernel)

threshold = 100
canny_output = cv.Canny(opening, threshold, threshold * 2)
contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

minEllipse = [None] * len(contours)
for i, c in enumerate(contours):
    if 50 < c.shape[0] < 100:
        minEllipse[i] = cv.fitEllipse(c)
        print(minEllipse[i])
drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

for i, c in enumerate(contours):
    color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
    # contour
    # cv.drawContours(drawing, contours, i, color)
    # ellipse
    if 50 < c.shape[0] < 100:
        cv.ellipse(drawing, minEllipse[i], color, 2)

source_window = 'Source'
cv.namedWindow(source_window)
gray_window = 'Gray'
cv.namedWindow(source_window)
drawing_window = 'Drawing'
cv.namedWindow(drawing_window)

cv.imshow(source_window, roi)
cv.imshow(gray_window, src_gray)
cv.imshow(drawing_window, drawing)
cv.imshow("opening", opening)
cv.waitKey()
