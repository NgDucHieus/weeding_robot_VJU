
import Jetson.GPIO as GPIO
import time
from step_motor import StepMotor13, StepMotor2
from dc_motor import Dc_Motor
from laser import Laser
import threading
import sys
import cv2 
import imutils
from yoloDet import YoloTRT


laser1 = Laser()
laser1.ON()
list1 = []
list2 = []
list3 = []
# use path for library and engine file
model = YoloTRT(library="yolov7/build/libmyplugins.so", engine="yolov7/build/best_3_laser.engine", conf=0.5, yolo_ver="v7")

cap = cv2.VideoCapture(0)



while True:

    ret, frame = cap.read()
    frame = imutils.resize(frame, width=600)
    detections, t = model.Inference(frame)
    laser1.CHECK ()
    # for obj in detections:
    #    print(obj['class'], obj['conf'], obj['box'])
    # print("FPS: {} sec".format(1/t))
    for obj in detections:
        print(obj['class'], obj['conf'], obj['box'])
        x,y,w,h = obj['box']
        # print("FPS: {} sec".format(1/t))
        if obj['class'] == "Crop":

            list1.append([x,y])
        elif obj['class'] == 'Weed':
            list2.append([x,y])
        elif obj['class'] == 'Laser_pointer':
            list3.append([x,y])
    cv2.imshow("Output", frame)

    key = cv2.waitKey(1)
    if key == ord('q') or (len(list3) !=0 and len(list2)!=0 ):
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
step13 = StepMotor13()
step2 = StepMotor2()

scalex = (327.57727- 299.96945)/1000
scaley = (97.85041 - 73.80898) /1000
dx =list2[0][0] - list3[0][0]
dy=list2[0][1] - list3[0][1]
print(round(dx/scalex))
print(round(dy/scaley))




def recur(list2,list3):
    dx =list2[0][0] - list3[0][0]
    dy=list2[0][1] - list3[0][1]
    x1 = round(dx/scalex)
    x2 = round(dy/scaley)
    return x1,x2
    

    

def cal(list2):
    lx =[]
    ly =[]
    for i in range(len(list2)-1):
        dx =list2[i][0] - list2[i+1][0]
        dy=list2[i][1] - list2[i+1][1]
        lx.append(round(dx/scalex))
        ly.append(round(dy/scaley))
    return lx,ly

def motor(x1,x2):
    if x2 > 0 :
        step13.move(GPIO.LOW, GPIO.HIGH,x2)
    else:
        step13.move(GPIO.LOW, GPIO.HIGH,abs(x2))

    if x1 > 0 :
        step2.move(GPIO.LOW, GPIO.HIGH,x1)
    else:
        step2.move(GPIO.LOW, GPIO.HIGH,abs(x1))
    
def main():
    x1,x2 = recur(list2,list3)
    motor(x1,x2)
    time.sleep(2)
    lx,ly = cal(list2)
    for i in range(len(lx)):
        motor(lx[i],ly[i])
        time.sleep(2)


main()

GPIO.cleanup()

#y Laser_pointer 0.65205187 [314.8315    21.252878 338.3528    45.913006]
#y #Laser_pointer 0.52887183 [324.29306   96.672485 341.71585  115.43915 ]