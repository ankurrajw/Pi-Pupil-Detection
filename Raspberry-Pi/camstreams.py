# show both camera streams 

import cv2
pcap = cv2.VideoCapture('libcamerasrc ! video/x-raw,width=640,height=480 ! videoflip method=clockwise ! videoconvert ! appsink drop=True')
wcap = cv2.VideoCapture(0)
if wcap.isOpened():
        print(f'World camera available:')
if pcap.isOpened():
        print(f'Puil camera available:')
        
while True:
	pret, pframe = pcap.read()
	pframe = pframe[0:480, 0:480]
	wret, wframe = wcap.read()
	wframe = wframe[0:2048:2, 0:2048:2]
	cv2.imshow('pframe', pframe)
	cv2.imshow('wframe', wframe)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

pcap.release()
wcap.release()
cv2.destroyAllWindows()
