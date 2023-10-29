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
laser1.CHECK()
# Initial setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.cleanup()

def DC_motor():
    for i in range(3):
        dc1 = Dc_Motor()
        dc1.stop()
        dc1.move_forward(800)
        time.sleep(2)
        dc1.move_backward(800)
        time.sleep(2)

def St_motor():
    step13 = StepMotor13()
    step2 = StepMotor2()
    step13.move(GPIO.LOW, GPIO.HIGH, 400, 0.00001)
    time.sleep(1)
    step13.move(GPIO.LOW, GPIO.LOW, 400, 0.00001)
    time.sleep(1)
    step2.move(GPIO.LOW, GPIO.HIGH, 400, 0.00001)
    time.sleep(1)
    step2.move(GPIO.LOW, GPIO.LOW, 400, 0.00001)
    time.sleep(1)

def Yolo_live():


# use path for library and engine file
    model = YoloTRT(library="yolov7/build/libmyplugins.so", engine="yolov7/build/best_3_laser.engine", conf=0.5, yolo_ver="v7")

    cap = cv2.VideoCapture("data/output_4_3_classes.mp4")

    while True:
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=600)
        detections, t = model.Inference(frame)
    # for obj in detections:
    #    print(obj['class'], obj['conf'], obj['box'])
    # print("FPS: {} sec".format(1/t))
        cv2.imshow("Output", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()



def Yolo_detect():
    list1 = []
    list2 = []
    list3 = []
# use path for library and engine file
    model = YoloTRT(library="yolov7/build/libmyplugins.so", engine="yolov7/build/best_3_laser.engine", conf=0.5, yolo_ver="v7")

    cap = cv2.VideoCapture("data/output3.png")

   

    ret, frame = cap.read()
    frame = imutils.resize(frame, width=600)
    detections, t = model.Inference(frame)
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
    print(list2)  
    print(list3) 





if __name__ =="__main__":
    # t1 = threading.Thread(target=St_motor)
    # t2 = threading.Thread(target=DC_motor)
    t3 = threading.Thread(target=Yolo_detect)
   # starting thread 1
    # t1.start()
    # starting thread 2
    # t2.start()
    t3.start()
    # wait until thread 1 is completely executed
    # t1.join()
    # wait until thread 2 is completely executed
    # t2.join()
    t3.join()
    # both threads completely executed
    print("Done!")
    GPIO.cleanup()



# DC_motor()
# St_motor()

