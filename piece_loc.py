import cv2
import random
from random import randint
import math
import numpy as np

def location(origin, x_end, y_end, obj_x, obj_y):
    if (obj_x > origin[0]) and (obj_y > origin[1]) and (obj_x < x_end[0]) and (obj_y < y_end[1]):
        x_axis = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        y_axis = range(8,0,-1)
        x_step = x_end[0]/8
        y_step = y_end[1]/8
        if obj_x > (x_end[0]/2):
            x_calib = 10
        else:
            x_calib = -2
        if obj_y > (y_end[1]/2):
            y_calib = 6
        else:
            y_calib = -1
        x_offset = origin[0]
        y_offset = origin[1]
        x_index = math.floor(abs(obj_x - x_offset + x_calib)/x_step)
        print("value", x_index)
        y_index = math.floor(abs(obj_y - y_offset + y_calib)/y_step)
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
        pos = str(temp[0]) + ", " + str(temp[1])
        image = cv2.putText(image, pos, (randx+1, randy+1), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2, cv2.LINE_AA)

def ind_test(image, one_test, origin, x_end, y_end):
    h, w = image.shape
    for i in range(len(one_test)):
        randx = one_test[i][0]
        randy = one_test[i][1]
        image = cv2.circle(image, (randx, randy), 2, 0, 2)
        temp = location(origin, x_end, y_end, randx, randy)
        pos = str(temp[0]) + ", " + str(temp[1])
        image = cv2.putText(image, pos, (randx+1, randy+1), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2, cv2.LINE_AA)



random.seed()
path = "C:/Users/atche/OneDrive/Desktop/Winter2023/EE146/Chess Dataset/22-39-10.jpg";
img = cv2.imread(path);
original_image = img;
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
kernel = np.ones((5,5),np.float32)/25
img_blur = cv2.filter2D(gray,-1,kernel)
edges= cv2.Canny(gray, 50,200)

contours, hierarchy= cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
all_areas = []
for cnt in contours:
    x1,y1 = cnt[0][0]
    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    if len(approx) == 4:
      x, y, w, h = cv2.boundingRect(cnt)
      ratio = float(w)/h
      if ratio >= 0.9 and ratio <= 1.1:
         area = cv2.contourArea(cnt)
         all_areas.append(area)

sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
max_square = sorted_contours[0]
x, y, w, h = cv2.boundingRect(max_square)

pts1 = np.float32([[x+4, y+4], [x+w-5, y+4], [x+4, y+h-5], [x+w-5, y+h-5]])
pts2 = np.float32([[0, 0], [525, 0], [0, 525], [525, 525]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(gray, matrix, (525, 525))
cv2.imshow("Warp Perspective",  result)
dst = cv2.cornerHarris(result,2,3,0.04)
dst = cv2.dilate(dst,None)
ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
dst = np.uint8(dst)

ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

x_sort = np.zeros(len(corners))
y_sort = np.zeros(len(corners))
for i in range(len(corners)):
    x_sort[i] = (corners[i][0])
    y_sort[i] = (corners[i][1])

x_sort = (np.sort(x_sort))
y_sort = (np.sort(y_sort))

origin = (int(x_sort[0]), int(y_sort[0]))
x_end = (int(x_sort[len(corners)-1]), int(y_sort[0]))
y_end = (int(x_sort[0]), int(y_sort[len(corners)-1]))

cv2.line(result, origin, x_end, 255, 2)
cv2.line(result, origin, y_end, 255, 2)

test_bench = [(450,50), (75,440)]
# ind_test(result, test_bench, origin, x_end, y_end)
test(result, 15, origin, x_end, y_end)
cv2.imshow("Axis",result)
cv2.waitKey(0)
cv2.destroyAllWindows()
