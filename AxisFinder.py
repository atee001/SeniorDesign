import cv2
import random
from random import randint
import math
import numpy as np
from picamera import PiCamera
from time import sleep
from picamera.array import PiRGBArray
import sys

camera = PiCamera(
    resolution=(1280, 720),
)
sleep(2)
cnt = 1000

rawCapture = PiRGBArray(camera) 
camera.capture(rawCapture,format="bgr", use_video_port=True)
img = rawCapture.array
img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
original_image = img;
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

cv2.imwrite("Calibration_Image.jpg", gray)

pts1 = np.float32([[172, 270], [710, 275], [165, 800], [690, 820]])
pts2 = np.float32([[0, 0], [525, 0], [0, 525], [525, 525]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(gray, matrix, (525, 525))
cv2.imshow("Warp Perspective",  result)
cv2.imwrite("Warp_Perspective.jpg", result)

dst = cv2.cornerHarris(result,2,3,0.07)
dst = cv2.dilate(dst,None)
result[dst > 0.01*dst.max()] = 255
ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
dst = np.uint8(dst)

ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

x_sort = np.zeros(len(corners))
y_sort = np.zeros(len(corners))
for j in range(len(corners)):
    x_sort[j] = (corners[j][0])
    y_sort[j] = (corners[j][1])

x_sort = (np.sort(x_sort))
y_sort = (np.sort(y_sort))

origin = (int(x_sort[4]), int(y_sort[4]))
print("origin.x", origin[0])
print("origin.y", origin[1])
print("origin", origin)
x_end = (int(x_sort[len(x_sort)-4]), int(y_sort[4]))
y_end = (int(x_sort[4]), int(y_sort[len(x_sort)-4]))

print("x_end", x_end)
print("y_end", y_end)

cv2.line(result, origin, x_end, 255, 2)
cv2.line(result, origin, y_end, 255, 2)
for i in (range(0,9)):
    cv2.circle(result, (origin[0] + int(x_end[0]*i/8.25), origin[1]), 2, 0, 3)
for i in (range(0,9)):
    cv2.circle(result, (origin[0], origin[1] + int(y_end[1]*i/8.35)), 2, 0, 3)

cv2.imshow("Axis",result)
cv2.waitKey(0)
cv2.destroyAllWindows()


