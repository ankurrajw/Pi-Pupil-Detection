import cv2
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def trackbarCallback(x):
    print(f"threshold value {x}")
cv.namedWindow("test")
cv.createTrackbar("threshold", "test", 0, 255, trackbarCallback)
# image read
img = cv.imread("../Results/Inference/Hough27_01_2022_12_45_37/hough_circle2.png")
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img = img[220:640, 0:480]
#hist, bins = np.histogram(img.flatten(), 256, [0, 256])
#cdf = hist.cumsum()
#cdf_normalized = cdf * float(hist.max()) / cdf.max()
#plt.plot(cdf_normalized, color='b')
#plt.hist(img.flatten(), 256, [0, 256], color='r')
#plt.xlim([0, 256])
#plt.legend(('cdf', 'histogram'), loc='upper left')

while True:
    #equ = cv.equalizeHist(img)
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(img)
    value_threshold = cv.getTrackbarPos("threshold", "test")
    gray = cv2.medianBlur(cl1, 9)
    _, threshold = cv.threshold(cl1, 133, 255, cv.THRESH_BINARY_INV)
    circles = cv2.HoughCircles(threshold, cv2.HOUGH_GRADIENT, 1, 100, param1=40, param2=15, minRadius=20,
                               maxRadius=45)

    if circles is not None:
        detected_circles = np.uint16(np.around(circles))
        print(detected_circles)


        test = []
        for idx, data in enumerate(detected_circles[0, :]):
            # Dirty implementaion
            if data[0] > np.shape(img)[0] - 1 or data[1] > np.shape(img)[1] - 1:
                test.append(idx)
            if data[2] > 120:
                test.append(idx)

        print(test)
        detected_circles = np.reshape(detected_circles,
                                      (np.shape(detected_circles)[1], np.shape(detected_circles)[2]))
        detected_circles = np.delete(detected_circles, tuple(test), 0)
        print(detected_circles)
        for idx, (x, y, r) in enumerate(detected_circles):
            print(f"{idx}")
            print(f"Value X {x} Y {y} R {r}")
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, f"{idx}", (x, y), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.circle(img, (x, y), r, (0, 255, 0), 3)
            cv2.circle(img, (x, y), 2, (255, 255, 0), 3)

    #res = np.hstack((img, equ, cl1))  # stacking images side-by-side
    cv.imshow("original image", img)
    #cv.imshow("histogram equ image", equ)
    cv.imshow("CLAHE image", cl1)
    cv.imshow("threshold image", threshold)
    key = cv.waitKey(1)
    if key == 27:
        break
'''
    cv.imwrite("Results/Report Images/result.png", res)
    fig, (ax1,ax2,ax3) = plt.subplots(1,3,sharex=True,sharey=True)
    ax1.imshow(img, cmap = "gray")
    ax1.set_title("Original Image")
    ax2.imshow(equ, cmap = "gray")
    ax2.set_title("Histogram Equalisation")
    ax3.imshow(cl1, cmap = "gray")
    ax3.set_title("CLAHE")'''

#plt.imshow(res, cmap='gray')
#plt.show()

cv.waitKey(0)
cv.destroyAllWindows()
