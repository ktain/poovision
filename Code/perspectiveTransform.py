import cv2
import numpy as np

img = cv2.imread('pic.png')
rows,cols,ch = img.shape

pts1 = np.float32([[53,44],[546,58],[0,394],[640,390]])
pts2 = np.float32([[0,0],[640,0],[0,480],[640,480]])

M = cv2.getPerspectiveTransform(pts1,pts2)

dst = cv2.warpPerspective(img,M,(640,480))

cv2.imwrite("newperspective.png", dst)
