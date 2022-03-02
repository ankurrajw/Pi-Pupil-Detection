import cv2
import numpy as np

frame = cv2.imread(r"C:\Users\Ankur\Desktop\Uni Siegen\SEM5\Eye Detection\Project-code-Ankur\master-thesis-eye-tracking\Results\infrared\imPi0.png")
#frame = cv2.imread(r"C:\Users\Ankur\Desktop\Uni Siegen\SEM5\Eye Detection\Project-code-Ankur\master-thesis-eye-tracking\Results\Inference\SidePupilImages\hough_circle337.png")
roi = frame[220:640, 0:480]
output = roi.copy()
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
cl1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
clahe = cl1.apply(gray)
gray = cv2.medianBlur(clahe, 9)
kernel = np.ones((3,3), np.uint8)

img_erosion = cv2.erode(gray, kernel, iterations=2)
_, threshold = cv2.threshold(gray, 132, 255, cv2.THRESH_BINARY_INV)
#th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            #cv2.THRESH_BINARY_INV, 29, 10)
circles = cv2.HoughCircles(threshold, cv2.HOUGH_GRADIENT, 1, 100, param1=40, param2=15, minRadius=20,
                                   maxRadius=40)

print(circles)
cv2.imshow("Image", output)
cv2.imshow("gray", gray)
cv2.imshow("threshold_canny", threshold)
cv2.imshow("img_erosion", img_erosion)
cv2.waitKey(0)
cv2.destroyAllWindows()
