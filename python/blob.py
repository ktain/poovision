
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

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array

	# add white border to enclose blobs
	image = cv2.copyMakeBorder(image,2,2,2,2,cv2.BORDER_CONSTANT,value=[255,255,255])

	keypoints = detector.detect(image)

	soil_level = 0
	#print "---------------------------"
	for kp in keypoints:
		"""
    		print "(%d, %d) size=%.1f resp=%.1f" % (kp.pt[0], kp.pt[1], kp.size, kp.response)
		"""
		
		#Add blob areas		
		soil_level += kp.size		

		cv2.circle(image, (int(kp.pt[0]), int(kp.pt[1])), int(kp.size/2), (0, 0, 255))
	
	print "soil level = %d%%" %(soil_level/1000*100)	


	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF

	rawCapture.truncate(0)

	if key == ord("q"):
		break

