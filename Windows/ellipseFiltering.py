import cv2 as cv
import numpy as np
import random as rng

rng.seed(12345)
print("START")
print("*" * 30)


def filter_contour(contours):
    '''TODO filter contours to get ellipses based on area and circularity
    DOCUMENTATION : Why we need to do a convex hull operation on the contour instead of finding the circularity directly
    from contour ?
    ANS: Since pixels of contour leads to a higher value of circularity > 200. Doing a convex hull leads to a lower
    value since we don't deal with discritised pixels '''
    contours_filtered = []
    print("Initial Contours : {}".format(len(contours)))
    print("Filtered Contours")
    for i, c in enumerate(contours):
        try:
            convex_hull = cv.convexHull(c)
            area_hull = cv.contourArea(convex_hull)
            # print("{} area convex hull {}".format(i, area_hull))
            if 600 < area_hull:  # filtering based on area
                circumference_hull = cv.arcLength(convex_hull, True)
                circularity_hull = (4 * np.pi * area_hull) /circumference_hull ** 2
                if 0.8 < circularity_hull :  # filtering based on circularity
                    print("convex hull :{} Circularity :{} Area : {}".format(i, circularity_hull, area_hull))
                    contours_filtered.append(convex_hull)
        except ZeroDivisionError:
            print("Division by zero for contour {}".format(i))
    return contours_filtered

    # print("Circularity {} {}".format(i, circularity))


# src_image = cv.imread(r"C:\Users\Ankur\Desktop\Uni Siegen\SEM5\Eye Detection\Project-code-Ankur\master-thesis-eye-tracking\Results\infrared\imPi21.png")
#src_image = cv.imread(r"C:\Users\Ankur\Desktop\Uni Siegen\SEM5\Eye Detection\Project-code-Ankur\master-thesis-eye-tracking\Results\Inference\SidePupilImages\hough_circle338.png")
src_image = cv.imread( r"C:\Users\Ankur\Desktop\Uni Siegen\SEM5\Eye Detection\Project-code-Ankur\master-thesis-eye-tracking\Results\Hough21_01_2022_16_01_18\hough_circle380.png")

roi = src_image[220:640, 0:480]
output = roi.copy()
src_gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
src_gray = cv.bitwise_not(src_gray)

# CLAHE operation is not helpful for canny edge detection
# cl1 = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
# clahe = cl1.apply(src_gray)

src_gray = cv.medianBlur(src_gray, 9)
kernel = np.ones((5, 5), np.uint8)
# _, src_gray = cv.threshold_canny(src_gray, 120, 255, cv.THRESH_BINARY_INV)
opening = cv.morphologyEx(src_gray, cv.MORPH_OPEN, kernel)
#Kristof Van Laerhoven
threshold_canny = 15
#Ankur
#threshold_canny = 20
canny_output = cv.Canny(src_gray, threshold_canny, threshold_canny * 2)
contours, _ = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contours_filtered = filter_contour(contours)

# blank canvas
drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

print('*' * 30)
print("Drawing Ellipses")
minEllipse = [None] * len(contours_filtered)
for i, c in enumerate(contours_filtered):
    color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
    minEllipse[i] = cv.fitEllipse(c)
    cv.drawContours(drawing, contours_filtered, i, color)
    (x, y), (MA, ma), angle = minEllipse[i]
    area_contour_hull = cv.contourArea(c)
    area_ellipse = (np.pi/4) * MA * ma
    print("Area Ellipse :{} Area Contour Hull :{}".format(area_ellipse, area_contour_hull))
    cv.ellipse(drawing, minEllipse[i], color, 2)

source_window = 'Source'
cv.namedWindow(source_window)
gray_window = 'Gray'
cv.namedWindow(source_window)
drawing_window = 'Drawing'
cv.namedWindow(drawing_window)

cv.imshow(source_window, roi)
# cv.imshow(gray_window, src_gray)
cv.imshow(drawing_window, drawing)
# cv.imshow("opening", opening)
cv.imshow("canny", canny_output)
cv.waitKey()

print("*" * 30)
print("STOP")

'''
TODO: Eccentricity calculation
(x, y), (MA, ma), angle = minEllipse[i]
c_e = np.sqrt(np.square(ma) - np.square(MA))
ecc = c_e / MA
'''
