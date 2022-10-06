import cv2
import numpy as np
import glob


def demo(x):
    print(x)
print("Program Start")

# frame = cv2.imread(r"Results\imPi18.png")
cv2.namedWindow("image")

cv2.createTrackbar("Value : threshold", "image", 0, 255, demo)
#cv2.createTrackbar("Value : threshold_canny canny 1","image", 0, 300, demo)
#cv2.createTrackbar("Value : threshold_canny canny 2","image", 0, 500, demo)


folder_images = glob.glob(r"C:\Users\Ankur\Desktop\Uni Siegen\SEM5\Eye Detection\Project-code-Ankur\master-thesis-eye-tracking\Results/OldImages/imPi*.png")
folder_images = sorted(folder_images)
count = 0
print(folder_images)
for image_path in folder_images:
    print(image_path)
    frame = cv2.imread(image_path)

    roi = frame[220:600, 0:480]
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #gray_frame = cv2.GaussianBlur(gray_frame, (3, 3), 20)
    gray_frame = gray_frame[220:600, 0:480]

    value_threshold = cv2.getTrackbarPos("Value : threshold", "image")
    #canny_1 = cv2.getTrackbarPos("Value : threshold_canny canny 1", 'image')
    #canny_2 = cv2.getTrackbarPos("Value : threshold_canny canny 2", 'image')
    #canny = cv2.Canny(roi, canny_1, canny_2)

    _, threshold = cv2.threshold(gray_frame, value_threshold, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=lambda x : cv2.contourArea(x), reverse=True)
    print(contours)
    if not contours:
        count += 1
        print(image_path)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(roi, (x,y) , (x+w,y+h), (255, 0, 0), 2)
        cv2.drawContours(roi, cnt, -1, (0,255,0), 2)

    cv2.imshow("threshold_canny", threshold)
    cv2.imshow(f"demo Image ", roi)
    cv2.imshow("gray image", gray_frame)

    #cv2.imshow("canny", canny)
    key = cv2.waitKey(0)
    if key == 27:
        break
    """
        if cv2.waitKey(0) & 0xFF == ord('q'):
        print("Closing Windows")
        break
    """

print(f"Images with no contour {count}")
cv2.destroyAllWindows()
