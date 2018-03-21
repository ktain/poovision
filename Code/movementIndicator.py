import cv2

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

cam = cv2.videoCapture(0)

winName = "Movement Indicator"
cv2.namedWindow(winName, cv2.CV_WINDOW
