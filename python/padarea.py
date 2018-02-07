from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

#initializing the camera
camera = PiCamera()
camera.resolution = (320,240)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(320,240))

#warming up the camera
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	image = frame.array
	cv2.namedWindow("image");
	cv2.imshow("image", image)
	
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# make black and white
	blur = cv2.blur(gray,(5,5))
	ret,bw = cv2.threshold(blur,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	
	# find contours
	image2, contours, hierarchy = cv2.findContours(bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	if len(contours) > 0:
		largest = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
		contour = cv2.drawContours(image, largest, -1, (0,0,255), 3)
	else:
		contour = image
	
	print "%d contours found" %(len(contours))
	
	# Display images
	
	cv2.namedWindow("grayscale");
	cv2.namedWindow("bw");
	cv2.namedWindow("largest contour");
	
	cv2.imshow("grayscale", gray)
	cv2.imshow("bw", bw)
	cv2.imshow("largest contour", contour);
	
	key = cv2.waitKey(1) & 0xFF

	rawCapture.truncate(0)

	if key == ord("q"):
		break
