from picamera.array import PiRGBArray
from picamera import PiCamera 
import time
import cv2
import RPi.GPIO as GPIO

ledPin = 7
showimages = False
showoutput = True

# Setup GPIO for LED
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.LOW)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 0
params.maxThreshold = 200
 
# Filter by Area.
params.filterByArea = True
params.minArea = 200
 
# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.01
 
# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.87
 
# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.005
 
# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
else :
    detector = cv2.SimpleBlobDetector_create(params)

# For Control
maxBlob = 800
user_threshold = 25
prevTime = 0
deadTime_s = 10 # time to determine if dog present within last X seconds
timeOfLastMovement = time.time()

# Output information
isMotionDetected = False
isDogPresent = False
checkImages = False
soilLevel = 0


# Settings
resolutionX = 320
resolutionY = 240

camera = PiCamera()
camera.resolution = (resolutionX, resolutionY)
# Original Framerate = 15
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=(resolutionX, resolutionY))

# Test functions for movement detection
def diffImg(t0, t1, t2):
	d1 = cv2.absdiff(t2, t1)
	d2 = cv2.absdiff(t1, t0)
	return cv2.bitwise_and(d1, d2)

threshold = 31000
def movementDetection(prev, cur, new):
	# Calculate total amount of white pixels
	totDiff = cv2.countNonZero(diffImg(prev, cur, new))

	if(totDiff > threshold):
##		cv2.imwrite("isMotionDetected.png", diffImg(prev, cur, new))
##		cv2.imwrite("dogFound.png", new)

		if showimages:
			cv2.imshow(winName, diffImg(prev, cur, new))
		return diffImg(prev, cur, new), time.time()
	else:
		if showimages:
			cv2.imshow(winName, diffImg(prev, cur, new))
		return diffImg(prev, cur, new), 0
##	print "Total Movement: " + str(totDiff)

winName = "Movement Indicator"
firstIter = True

time.sleep(0.1)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	
	# Grayscale image
	image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	if firstIter:
		t_minus = image_gray
		t = image_gray
		curImg = image_gray
		firstIter = False
	else:
		t_minus = t
		t = t_plus
		
	t_plus = image_gray

	# Dog Detection
	_, outputTime = movementDetection(t_minus, t, t_plus) 
	# For determining whether or not to advance the pad
	if outputTime == 0:
		outputTime = prevTime
	else:
		prevTime = outputTime
	# Threshold for deciding whether or not dog is present
	if time.time() - outputTime > 1:
		# If current time - time of movement > 1, no motion detected
		isMotionDetected = False
	else:
		isMotionDetected = True
		timeOfLastMovement = time.time()

	# if not isDogPresent and not isMotionDetected and not checkImages:
	# 	curImg = image_gray
	# 	cv2.imshow('curImg', curImg)
	# 	print 'saved cur image'

	if checkImages and not isDogPresent:
		afterImg = image_gray
		wasteImg = cv2.absdiff(curImg, afterImg)
		cv2.imshow('newWaste', wasteImg) 
		print 'saved after image'
		curImg = image_gray
		cv2.imshow('curImg', curImg)
		print 'saved cur image'

		checkImages = False

	# add white border to enclose blobs
	image = cv2.copyMakeBorder(image,2,2,2,2,cv2.BORDER_CONSTANT,value=[255,255,255])

	
	# detect blob centers
	keypoints = detector.detect(image)

	# if no motion detected, update soil level, otherwise keep prev soil
	# level 
	if not isMotionDetected:
		soilLevel = 0
		for kp in keypoints:
			"""
    			print "(%d, %d) size=%.1f resp=%.1f" % (kp.pt[0], kp.pt[1], kp.size, kp.response)
			"""
			
			# Sum blob areas with weights based on location along y-axis
			# Far back weight is 10.0
			# Close up weight is 1.0
			soilLevel += kp.size + 20 * kp.size * kp.pt[1]/resolutionY

			#print "y-axis = %d  weight = %.2f" %((kp.pt[1], 0.25*(kp.pt[1]+resolutionY)/resolutionY))
		
			# Draw outlines
			if (showimages):
				cv2.circle(image, (int(kp.pt[0]), int(kp.pt[1])), int(kp.size/2), (0, 0, 255))
		
		soilLevel = float(soilLevel)/float(maxBlob)*100
	
	
	# Determine if dog was present within last X seconds
	# If no movement detected, and time since last movement is greater than dead time, assume dog is no longer present
	if not isMotionDetected and time.time() - timeOfLastMovement > deadTime_s:
		isDogPresent = False
	elif time.time() - timeOfLastMovement < deadTime_s:
		isDogPresent = True
		checkImages = True
	
	if showoutput:
		print "soil = %0.1f%%  motion = %s  dog = %s" %(soilLevel,
		isMotionDetected, isDogPresent)
	
	# Simulated Control System	
	if soilLevel > user_threshold and not isMotionDetected:
		GPIO.output(ledPin, GPIO.HIGH)
	else:
		GPIO.output(ledPin, GPIO.LOW) 

	if showimages:
		cv2.imshow("Soil detection", image)
	
	rawCapture.truncate(0)
	
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

