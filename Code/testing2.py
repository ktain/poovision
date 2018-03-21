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
camera.start_preview()

rawCapture = PiRGBArray(camera, size=(320,240))

#warming up the camera
time.sleep(2)

#used to hold the colors of the picture
colorMap = {}

camera.capture('pic.png')


image = cv2.imread('pic.png')
dst = cv2.stylization(image, sigma_s=60,sigma_r=0.07)



cv2.imwrite("dst.png", dst)

blur = cv2.GaussianBlur(dst,(5,5),0)

cv2.imwrite("dstBlur.png", blur)


for rows in range(0,240):
	for cols in range(0,320):
		#this comes out as [r,g,b]
		color = blur[rows,cols]
		color = "#{:02x}{:02x}{:02x}".format(color[0],color[1],color[2])

		if colorMap.get(color,"none") == "none":
			colorMap[color] = 1
		else:
			colorMap[color] = colorMap[color] + 1

area = 320*240

for key,value  in colorMap.items():
	if value > 80:
		print "color: %s, %d " % (key, value)
	


