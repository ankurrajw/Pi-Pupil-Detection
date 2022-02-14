import cv2
import numpy as np


def click_mouse_button(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print('X ' + str(x) + ' Y ' + str(y))

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x, y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('adaptive mean th', th2)


img = cv2.imread("../Results/Inference/SidePupilImages/hough_circle326.png")

roi = img[220:640, 0:480].copy()
output = roi.copy()
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
cl1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(5, 5))
clahe = cl1.apply(gray)
gray = cv2.medianBlur(clahe, 5)
_, threshold = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
# th2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
#                            cv2.THRESH_BINARY_INV, 49, 10)
# ret3,th3 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            cv2.THRESH_BINARY_INV, 15, 5)

circles = cv2.HoughCircles(th3, cv2.HOUGH_GRADIENT, 1, 400, param1=40, param2=15, minRadius=10,
                           maxRadius=40)

print(circles)
cv2.imshow("Input Image", roi)
cv2.imshow("Gray Image", gray)
cv2.imshow("simple threshold", threshold)
# cv2.imshow("adaptive mean th", th2)
cv2.imshow("gaussian  th", th3)
cv2.setMouseCallback('adaptive mean th', click_mouse_button)
cv2.waitKey(0)
cv2.destroyAllWindows()
