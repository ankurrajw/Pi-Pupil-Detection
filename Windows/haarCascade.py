import numpy as np
import cv2
import time
import glob

# Video capture from the raspberry pi


image = cv2.imread("../Results/infrared/hough_circle229.png")
frame = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
eyes = cv2.CascadeClassifier('haarcascade_eye_right2split.xml')
detected = eyes.detectMultiScale(frame, scaleFactor=1.0006, minSize=(100,100), minNeighbors=1)
print(detected)
pupilFrame = frame
for (ex, ey, eh, ew) in detected:
    cv2.rectangle(frame, (ex,ey), (ex+eh, ey+ew), (255,0,0), 3)
    cv2.line(frame, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 1)  # draw cross
    cv2.line(frame, (ex + ew, ey), (ex, ey + eh), (0, 0, 255), 1)
    pupilFrame = cv2.equalizeHist(
        frame[ey + int(eh * .25):(ey + eh), ex:(ex + ew)])
    cl1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe = cl1.apply(pupilFrame)  # clahe
    blur = cv2.medianBlur(clahe, 7)  # median blur
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 100, param1=40, param2=10, minRadius=60,
                               maxRadius=150)
    if circles is not None:  # if at least 1 is detected
        circles = np.round(circles[0, :]).astype("int")  # change float to integer
        print('integer', circles)
        for (x, y, r) in circles:
            cv2.circle(pupilFrame, (x, y), r, (0, 255, 255), 2)
            print("circle drawn")
            cv2.rectangle(pupilFrame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

cv2.imshow('original image', image)
cv2.imshow('frame', pupilFrame)

if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
