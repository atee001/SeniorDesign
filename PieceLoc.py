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
# Give the camera a good long time to set gains and
# measure AWB (you may wish to use fixed AWB instead)
sleep(2)
cnt = 1000

def location(origin, x_end, y_end, obj_x, obj_y):
    if (obj_x > origin[0]) and (obj_y > origin[1]) and (obj_x < x_end[0]) and (obj_y < y_end[1]):
        x_axis = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        y_axis = range(8,0,-1)
        x_step = x_end[0]/(8.25)
        y_step = y_end[1]/(8.25)
        x_calib = 0
        y_calib = 0
#         if obj_x > (x_end[0]/2):
#             x_calib = 0
#         else:
#             x_calib = 0
#         if obj_y > (y_end[1]/2):
#             y_calib = 0
#         else:
#             y_calib = 0
        x_offset = origin[0]
        y_offset = origin[1]
        x_index = math.floor((obj_x - x_offset + x_calib)/x_step)
        y_index = math.floor((obj_y - y_offset + y_calib)/y_step)
        
        if(x_index < 0):
            x_index = 0
        elif(x_index > 7):
            x_index = 7
            
        if(y_index < 0):
            y_index = 0
        elif(y_index > 7):
            y_index = 7
            
        print("x_ind",x_axis[x_index])
        print("y_ind",y_axis[y_index])
        print("x", obj_x)
        print("y", obj_y)
        return (x_axis[x_index], y_axis[y_index])
    else:
        print("x", obj_x)
        print("y", obj_y)
        return (-1,-1)

def test(image, numtests, origin, x_end, y_end):
    h, w = image.shape
    for i in range(numtests):
        randx = randint(1, w-1)
        randy = randint(1, h-1)
        image = cv2.circle(image, (randx, randy), 2, 0, 2)
        temp = location(origin, x_end, y_end, randx, randy)
        pos = str(temp[0]) + "," + str(temp[1])
        image = cv2.putText(image, pos, (randx+1, randy+1), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 1, cv2.LINE_AA)

def ind_test(image, one_test, origin, x_end, y_end):
    h, w = image.shape
    for i in range(len(one_test)):
        randx = one_test[i][0]
        randy = one_test[i][1]
        image = cv2.circle(image, (randx, randy), 2, 0, 2)
        temp = location(origin, x_end, y_end, randx, randy)
        pos = str(temp[0]) + "," + str(temp[1])
        image = cv2.putText(image, pos, (randx+1, randy+1), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2, cv2.LINE_AA)



random.seed()
rawCapture = PiRGBArray(camera) 
camera.capture(rawCapture,format="bgr", use_video_port=True)
img = rawCapture.array
img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
original_image = img;
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

cv2.imwrite("Calibration_Image.jpg", gray)

pts1 = np.float32([[118, 288], [647, 291], [111, 809], [629, 827]])
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

# cv2.line(result, origin, x_end, 255, 2)
# cv2.line(result, origin, y_end, 255, 2)
for i in (range(0,9)):
    cv2.circle(result, (origin[0] + int(x_end[0]*i/8.30), origin[0]), 2, 0, 2)
for i in (range(0,9)):
    cv2.circle(result, (origin[0], origin[1] + int(y_end[1]*i/8.30)), 2, 0, 2)

test_bench = [(450,460), (75,460)]
# ind_test(result, test_bench, origin, x_end, y_end)
test(result, 15, origin, x_end, y_end)
cv2.imshow("Axis",result)
cv2.waitKey(0)
cv2.destroyAllWindows()

