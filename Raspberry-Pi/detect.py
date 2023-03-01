# show both camera streams 

import cv2
import numpy as np
import random as rng

'''Change the parameters to conduct a real time detection'''
CANNY_THRESHOLD = 100
MEDIAN_BLUR_K_SIZE = 9
MORPH_K_SIZE = 1


def filter_contour(_contours):
    _contours_filtered = []
    #print("Initial Contours : {}".format(len(_contours)))
    #print("Filtered Contours:")
    for i, c in enumerate(_contours):
        try:
            convex_hull = cv2.convexHull(c)
            area_hull = cv2.contourArea(convex_hull)
            # print("{} area convex hull {}".format(i, area_hull))
            if 600 < area_hull:  # filtering based on area
                circumference_hull = cv2.arcLength(convex_hull, True)
                circularity_hull = (4 * np.pi * area_hull) / circumference_hull ** 2
                if 0.8 < circularity_hull:  # filtering based on circularity
                    #print("convex hull :{} Circularity :{} Area : {}".format(i, circularity_hull, area_hull))
                    _contours_filtered.append(convex_hull)
        except ZeroDivisionError:
            print("Division by zero for contour {}".format(i))
    return _contours_filtered


def draw_ellipse(_drawing, _contours_filtered):
    minEllipse = [None] * len(_contours_filtered)
    for i, c in enumerate(_contours_filtered):
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        minEllipse[i] = cv2.fitEllipse(c)
        cv2.drawContours(_drawing, _contours_filtered, i, color)
        (x, y), (MA, ma), angle = minEllipse[i]
        area_contour_hull = cv2.contourArea(c)
        area_ellipse = (np.pi / 4) * MA * ma
        #print("Area Ellipse :{} Area Contour Hull :{}".format(area_ellipse, area_contour_hull))
        cv.ellipse(_drawing, minEllipse[i], color=color, thickness=2)
    return _drawing


def draw_ellipse_rgb(_image, _contours):
    minEllipse = [None] * len(_contours)
    for i, c in enumerate(_contours):
        minEllipse[i] = cv.fitEllipse(c)
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        cv.drawContours(_image, _contours, i, color)
        cv.ellipse(_image, minEllipse[i], color=color, thickness=2)
    return _image



srcPiCam = 'libcamerasrc ! video/x-raw,width=640,height=480 ! videoflip method=clockwise ! videoconvert ! appsink drop=True'
pcap = cv2.VideoCapture(srcPiCam)
wcap = cv2.VideoCapture(0)
if wcap.isOpened():
        print(f'World camera available:')
if pcap.isOpened():
        print(f'Puil camera available:')
        
kernel = np.ones((MORPH_K_SIZE, MORPH_K_SIZE), np.uint8)

while True:
	pret, pframe = pcap.read()
	wret, wframe = wcap.read()
	if pret: # and wret:
		pframe = pframe[0:480, 0:480]
		wframe = wframe[0:2048:2, 0:2048:2]
		output = pframe.copy()
		src_gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
		src_gray = cv2.medianBlur(src_gray, MEDIAN_BLUR_K_SIZE)
		opening = cv2.morphologyEx(src_gray, cv2.MORPH_OPEN, kernel)
		canny = cv2.Canny(opening, CANNY_THRESHOLD, CANNY_THRESHOLD * 2)
		contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		contours_filtered = filter_contour(contours)
		drawing = np.zeros((canny.shape[0], canny.shape[1], 3), dtype=np.uint8)
		drawing = draw_ellipse(drawing, contours_filtered)
		cv2.imshow('pframe', src_gray)
		cv2.imshow('wframe', wframe)
		
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

pcap.release()
wcap.release()
cv2.destroyAllWindows()
