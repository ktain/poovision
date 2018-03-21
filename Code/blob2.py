
from picamera.array import PiRGBArray
from picamera import PiCamera 
import time
import cv2


# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 0
params.maxThreshold = 200
 
# Filter by Area.
params.filterByArea = True
params.minArea = 200
 
# Filter by Circularity
params.filterByCircularity = True
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


camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(320, 240))

# Test functions for movement detection
def diffImg(t0, t1, t2):
	d1 = cv2.absdiff(t2, t1)
	d2 = cv2.absdiff(t1, t0)
	return cv2.bitwise_and(d1, d2)

threshold = 35000
def movementDetection(prev, cur, new):
	# Calculate total amount of white pixels
	totDiff = cv2.countNonZero(diffImg(prev, cur, new))

	if(totDiff > threshold):
##		cv2.imwrite("motionDetected.png", diffImg(prev, cur, new))
##		cv2.imwrite("dogFound.png", new)
		print "Motion Detected: YES"		

	cv2.imshow(winName, diffImg(prev, cur, new))
##	print "Total Movement: " + str(totDiff)

winName = "Movement Indicator"
firstIter = True

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	image = cv2.stylization(image, sigma_s=60, sigma_r = 0.07)

	if firstIter:
		t_minus = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		t = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		firstIter = False
	else:
		t_minus = t
		t = t_plus
		
	t_plus = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	movementDetection(t_minus, t, t_plus)

	# add white border to enclose blobs
	image = cv2.copyMakeBorder(image,2,2,2,2,cv2.BORDER_CONSTANT,value=[255,255,255])

	# detect blob centers
	keypoints = detector.detect(image)

	# output soil level
	soil_level = 0
	for kp in keypoints:
		"""
    		print "(%d, %d) size=%.1f resp=%.1f" % (kp.pt[0], kp.pt[1], kp.size, kp.response)
		"""
		
		# Sum blob areas
		soil_level += kp.size		

		# Draw outlines
		cv2.circle(image, (int(kp.pt[0]), int(kp.pt[1])), int(kp.size/2), (0, 0, 255))
	
	print "soil level = %d%%" %(soil_level/1000*100)	


	cv2.imshow("Soil detection", image)
	
	rawCapture.truncate(0)
	
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

