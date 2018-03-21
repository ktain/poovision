from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

#from scipy import ndimage
#import imageio

#initializing the camera
camera = PiCamera()
camera.resolution = (320,240)
camera.framerate = 15

rawCapture = PiRGBArray(camera, size=(320,240))

#warming up the camera
time.sleep(0.1)

#used to hold the colors of the picture
colorMap = {}

camera.capture('pic.png')
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array

	dst = cv2.edgePreservingFilter(image, flags=1, sigma_s=60,
	sigma_r=0.4)

	cv2.imshow("edgePreservingFilter", dst)


	for rows in range(0,320):
		for cols in range(0,240):
			color = image[rows,cols]
			print(color)
			
			#if colorMap.get(color,"none") == "none":
			#	colorMap[color] = 1
			#else:
				#colorMap[color] = colorMap[color] + 1



	rawCapture.truncate(0)

	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break


