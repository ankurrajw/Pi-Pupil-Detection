import cv2
import numpy as np
import glob

print("Program Start")
#frame = cv2.imread(r"Results\imPi18.png")

folder_images = glob.glob(r"Results/imPi*.png")
folder_images = sorted(folder_images)
count = 0
for image_path in folder_images:
    #print(image_path)
    frame = cv2.imread(image_path)

    roi = frame[220:600, 0:480]
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (3, 3), 30)
    gray_frame = gray_frame[220:600, 0:480]

    _, threshold = cv2.threshold(gray_frame, 45 , 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=lambda x : cv2.contourArea(x), reverse=True)
    if not contours:
        count += 1
        print(image_path)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)

        cv2.rectangle(roi, (x,y) , (x+w,y+h), (255, 0, 0), 2)
        #cv2.drawContours(roi, cnt, -1, (0,255,0), 2)
        break

    cv2.imshow("threshold", threshold)
    cv2.imshow("demo Image", roi)
    cv2.imshow("gray image", gray_frame)
    key = cv2.waitKey(500)
    if key == 27:
        break
    """
        if cv2.waitKey(0) & 0xFF == ord('q'):
        print("Closing Windows")
        break
    """

print(f"Images with no contour {count}")
cv2.destroyAllWindows()
