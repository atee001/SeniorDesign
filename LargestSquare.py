from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep
import numpy as np
import cv2

def takePic():
    rawCapture = PiRGBArray(camera) 
    camera.capture(rawCapture,format="bgr", use_video_port=True)
    img = rawCapture.array
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img

def preProc(img):
    pts1 = np.float32([[172, 270], [710, 275], [165, 800], [690, 820]])
    pts2 = np.float32([[0, 0], [525, 0], [0, 525], [525, 525]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (525, 525))
    return result

camera = PiCamera(
    resolution=(1280, 720),
)
sleep(2)

gray = takePic()
# gray = preProc(gray)
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
pts1 = np.float32([[x, y], [x+w, y], [x, y+h], [x+w, y+h]])
pts2 = np.float32([[0, 0], [525, 0], [0, 525], [525, 525]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(gray, matrix, (525, 525))
cv2.imshow("ChessBoard", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Top Left x: ", x)
print("Top Left y: ", y)
print("Top Right x: ", x+w)
print("Top Right y: ", y)
print("Bottom Left x: ", x)
print("Bottom Left y: ", y+h)
print("Bottom Right x: ", x+w)
print("Bottom Right y: ", y+h)

