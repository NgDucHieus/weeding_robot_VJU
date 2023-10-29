
import Jetson.GPIO as GPIO
import time
from step_motor import StepMotor13, StepMotor2
from dc_motor import Dc_Motor
from laser import Laser
# import threading
import sys
import cv2 
import imutils
from yoloDet import YoloTRT
# from mov import reset
GPIO.setup(31, GPIO.OUT)  #en2
GPIO.setup(29, GPIO.OUT)  #step2
GPIO.setup(32, GPIO.OUT)  #dir2
GPIO.output(31,GPIO.LOW)
GPIO.output(29,GPIO.LOW)
GPIO.output(32,GPIO.LOW)

laser1 = Laser()
laser1.CHECK()


laser_point = []
# use path for library and engine file
model = YoloTRT(library="yolov7/build/libmyplugins.so", engine="yolov7/build/best_3_laser.engine", conf=0.5, yolo_ver="v7")

cap = cv2.VideoCapture(0)
# reset()



while True:
    laser1.ON()
    weed = []
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=600)
    detections, t = model.Inference(frame)
    # for obj in detections:
    #    print(obj['class'], obj['conf'], obj['box'])
    # print("FPS: {} sec".format(1/t))
    for obj in detections:
        print(obj['class'], obj['conf'], obj['box'])
        x,y,w,h = obj['box']
        # print("FPS: {} sec".format(1/t))
        if obj['class'] == 'Crop':
            weed.append([x,y])
        elif obj['class'] == 'Laser_pointer' or 'Weed':
            laser_point.append([x,y])

    
    laser1.ON()

    key = cv2.waitKey(1)
    if key == ord('q') or (len(laser_point) !=0 and len(weed)!=0 ):
        print(weed)        
        cv2.imshow("Output", frame)
        break

cap.release()
cv2.destroyAllWindows()

# Laser_pointer 0.84302235 [272.2298    12.422732 302.7812    49.003826]
# Weed 0.8403213 [178.18454  60.72977 195.01007  73.08044]
# def calcu(x1,x2,y1,y2):
#     return abs(x2 -x1) ,abs(y2-y1)
# # 
#Laser_pointer 0.5107642 [375.23993  97.97803 393.2577  115.98263]
#Laser_pointer 0.72981226 [323.11017  97.87994 341.2736  117.77532]
stepY = StepMotor13()
stepX = StepMotor2()
new_weed1 = weed[0]
new_weed2 = weed[1]
# scalex = 0.93*(327.57727- 299.96945)/1000
# scaley = 1.149*(97.85041 - 73.80898) /1000

scalex = 0.5*0.93*(327.57727- 299.96945)/1000
scaley = 0.5*1.149*(97.85041 - 73.80898) /1000

dx =new_weed1[0] - laser_point[0][0]
dy= new_weed1[1] - laser_point[0][1]
# print(dx)
# print(dy)
def motor(dx,dy):

    if dx >= 0 and dy >= 0:
        stepY.move(GPIO.LOW,GPIO.LOW,round(dy/scaley))
        stepX.move(GPIO.LOW,GPIO.LOW,round(dx/scalex))
    if dx >= 0 and dy <=0:
        stepY.move(GPIO.LOW,GPIO.HIGH,round(abs(dy/scaley)))
        stepX.move(GPIO.LOW,GPIO.LOW,round(dx/scalex))
    if dy >= 0 and dx <=0:
        stepY.move(GPIO.LOW,GPIO.LOW,round(dy/scaley))
        stepX.move(GPIO.LOW,GPIO.HIGH,round(abs(dx/scalex)))
    if dx <= 0 and dy <=0:
        stepY.move(GPIO.LOW,GPIO.HIGH,round(abs(dy/scaley)))
        stepX.move(GPIO.LOW,GPIO.HIGH,round(abs(dx/scalex)))

motor(dx,dy)

time.sleep(1)
dx =new_weed2[0] - new_weed1[0]+10
dy= new_weed2[1] - new_weed1[1]+10
motor(dx,dy)
time.sleep(2)

# def distance(weed):
#     dis = []
#     for i in range(len(weed) -1):
#         dx = weed[i+1][0]-weed[i][0]
#         dy = weed[i+1][1]-weed[i][1]
#         dis.append([dx,dy])
#     return dis

# dis = distance(new_weed)
# for i in range(len(dis)):
#     motor(dis[i][0],dis[i][1])
               







# time.sleep(3)
laser1.OFF()

GPIO.output(31,GPIO.LOW)
GPIO.output(29,GPIO.LOW)
GPIO.output(32,GPIO.LOW)
GPIO.cleanup()

#y Laser_pointer 0.65205187 [314.8315    21.252878 338.3528    45.913006]
#y #Laser_pointer 0.52887183 [324.29306   96.672485 341.71585  115.43915 ]