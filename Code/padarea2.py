# Import modules
import time
import numpy as np
import imageio
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2


# Initialize the camera
camera = PiCamera()
camera.resolution = (320,240)
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=(320,240))

time.sleep(0.1)

camera.capture('image.png')

image = cv2.imread('image.png')


blur = cv2.blur(image,(3,3))
cv2.imwrite("blur.png",blur)

blur = cv2.stylization(blur, sigma_s=80,sigma_r=0.4)

gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray.png",gray)

# make black and white


ret,bw = cv2.threshold(gray, 100,255,cv2.THRESH_BINARY)
#bw = cv2.adaptiveThreshold(blur, 255,
#cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
cv2.imwrite("BW.png", bw)

image2 = imageio.imread('BW.png')
cv2.imwrite("imageio.png",image2)


start = 0;
end = 0;

#for row in range (0,240):
#	for col in range (0,320):
#		if start != end :
#change colors to black



#bw = cv2.edgePreservingFilter(bw, flags=1, sigma_s=60, sigma_r=0.4)

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

cv2.imshow("bw", bw)
cv2.imwrite("largeContour.png", contour)

allcontours = cv2.drawContours(image, contours, -1, (0,0,255), 3)
cv2.imwrite("allcontors.png", allcontours)

