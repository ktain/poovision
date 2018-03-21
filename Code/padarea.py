# Import modules
import time
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera


# Initialize the camera
camera = PiCamera()
camera.resolution = (320,240)
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=(320,240))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	image = frame.array
	#image = cv2.edgePreservingFilter(image, flags=1, sigma_s=60,
	#sigma_r=0.4)
	cv2.namedWindow("image");
	cv2.imshow("image", image)
	
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# make black and white
	blur = cv2.blur(gray,(5,5))
	bw = cv2.adaptiveThreshold(blur, 255,
	cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

	bw = cv2.edgePreservingFilter(bw, flags=1, sigma_s=60, sigma_r=0.4)
	
	# find contours
	image2, contours, hierarchy = cv2.findContours(bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	if len(contours) > 0:
		largest = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
		contour = cv2.drawContours(image, largest, -1, (0,0,255), 3)
	else:
		contour = image
	
	print "%d contours found" %(len(contours))
	
	for cnt in contours:
		area = cv2.contourArea(cnt)
#		print (area)

	# Display images
	
#	cv2.namedWindow("grayscale");
#	cv2.namedWindow("bw");
#	cv2.namedWindow("largest contour");
	
	#cv2.imshow("grayscale", gray)
	#cv2.imshow("bw", bw)
	cv2.imshow("largest contour", contour);
	cv2.imwrite("largeContour.png", contour)

	allcontours = cv2.drawContours(image, contours, -1, (0,0,255), 3)

	cv2.imshow("all contours", allcontours)
	cv2.imwrite("allcontors.png", allcontours)
	
	key = cv2.waitKey(1) & 0xFF

	rawCapture.truncate(0)

	if key == ord("q"):
		break
