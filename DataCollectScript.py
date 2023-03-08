import cv2
import sys
import numpy as np
from picamera import PiCamera
from time import sleep
from picamera.array import PiRGBArray

camera = PiCamera(
    resolution=(1280, 720),
)
# Give the camera a good long time to set gains and
# measure AWB (you may wish to use fixed AWB instead)
sleep(2)
cnt = 1000

while True:
        rawCapture = PiRGBArray(camera) 
        camera.capture(rawCapture,format="bgr", use_video_port=True)        
        frame = rawCapture.array
        result = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imshow("Previous Image", result)
        if (cv2.waitKey() & 0xFF == ord('q')):
            print("Quitting...")
            break
        elif cv2.waitKey() & 0xFF == ord('p'):
            rawCapture = PiRGBArray(camera) 
            camera.capture(rawCapture,format="bgr", use_video_port=True)
            frame = rawCapture.array
            result = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            board_pts = np.float32([[118, 288], [647, 291], [111, 809], [629, 827]])
            board_fin = np.float32([[0, 0], [525, 0], [0, 525], [525, 525]])
            matrix = cv2.getPerspectiveTransform(board_pts, board_fin)
            result = cv2.warpPerspective(result, matrix, (525, 525))    
            img_name = "chessdata_{}.jpg".format(cnt)
            cv2.imshow("Img_{}".format(cnt), result)
            cv2.imwrite(img_name, result)
            print("{} written!".format(img_name))
            cnt = cnt + 1

cv2.destroyAllWindows()

# while(True):
# #     if not(ret):
# #         print("Error retaining image")
# #         break
#     
#         frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         
#         cv2.imshow("Data", frame)      
#                 
#         #blur = cv2.GaussianBlur(frame, [5,5], 0)
#         #edges = cv2.Canny(blur, 30, 50)
#         #cedges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR);
#         #cv2.imshow("ImgBlur",blur)
#         #cv2.imshow("Edges", cedges)

