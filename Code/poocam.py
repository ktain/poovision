# Import modules
import time
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera


def drawPadArea():
	camera = PiCamera()
	camera.resolution = (320,240)
	camera.framerate = 5
	rawCapture = PiRGBArray(camera, size=(320,240))

	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

		image = frame.array
		
		# make grayscale
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# make black and white
		blur = cv2.blur(gray,(5,5))
		ret,bw = cv2.threshold(blur,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		
		# find contours
		image2, contours, hierarchy = cv2.findContours(bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		# draw largest contour
		if len(contours) > 0:
			largest = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
			contour = cv2.drawContours(image, largest, -1, (0,0,255), 3)
		else:
			contour = image
		
		print "%d contours found" %(len(contours))
		
		# Display contour
		cv2.namedWindow("largest contour");
		cv2.imshow("largest contour", contour);
		
		rawCapture.truncate(0)
		
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
			
		break
