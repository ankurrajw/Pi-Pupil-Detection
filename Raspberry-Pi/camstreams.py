# show both camera streams 
import cv2
cap = cv2.VideoCapture('libcamerasrc ! video/x-raw,width=640,height=480 ! videoflip method=clockwise ! videoconvert ! appsink drop=True')
#fourcc = cv2.VideoWriter_fourcc(*'XVID')

while True:
	ret, frame = cap.read()
	frame = frame[0:480, 0:480]
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
