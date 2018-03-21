from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import imageio

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
image_gray = cv2.imread('pic.png',0)
image = imageio.imread('pic.png')
if len(image.shape) > 2 and image.shape[2] == 4:
	image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)


filtered = cv2.edgePreservingFilter(image,flags=1,sigma_s=60 , sigma_r=.4)
cv2.imwrite("filtered.png", filtered)

blur = cv2.blur(filtered,(5,5))
cv2.imwrite("blur2.png",blur)

filtered = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

hist_image = cv2.equalizeHist(filtered)
cv2.imwrite("equalized.png", hist_image)

clahe = cv2.createCLAHE()
cl1 = clahe.apply(filtered)
cv2.imwrite("AHequalized.png", cl1)

filtered2 = cv2.edgePreservingFilter(blur,flags=1,sigma_s =60, sigma_r=.1)
cv2.imwrite("filtered2.png", filtered2)

blur2 = cv2.blur(filtered2,(5,5))
cv2.imwrite("blur3.png",blur2)

filtered3 = cv2.edgePreservingFilter(blur,flags=1,sigma_s =80, sigma_r=.05)
cv2.imwrite("filtered3.png", filtered2)

gray = cv2.cvtColor(filtered3, cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray.png",gray)
