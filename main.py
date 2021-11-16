import cv2
import time
cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
cap2.set(3,640)
cap2.set(4,480)
cap.set(3,640)
cap.set(4,480)

count_pics = 0

while True:
    success, img = cap.read()
    success2, img2 = cap2.read()
    time.sleep(1)
    cv2.imwrite("Results\\im"+str(count_pics)+".png",img)
    cv2.imwrite("Results\\im02" + str(count_pics) + ".png", img2)
    count_pics = count_pics+1
    print(f"Pic Captured :{count_pics}")
    if count_pics == 10:
        break