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



GPIO.setup(31, GPIO.OUT)  #en2
GPIO.setup(29, GPIO.OUT)  #step2
GPIO.setup(32, GPIO.OUT)  #dir2

# step13 = StepMotor13()

step13 = StepMotor13()
step13.move(GPIO.LOW, GPIO.HIGH,1000)
step2 = StepMotor2()
step2.move(GPIO.LOW, GPIO.HIGH,1000)
Laser1=Laser()
# Laser1.CHECK()
GPIO.output(31,GPIO.LOW)
GPIO.output(29,GPIO.LOW)
GPIO.output(32,GPIO.LOW)

GPIO.cleanup()

# Laser_pointer 0.5127 [338.7491    45.079235 354.29092   61.825974]
# Weed 0.59705824 [356.3794   95.99462 366.51022 106.52562]
# dy = weed[0][0] - laser_point[0][0]
# dy = weed[0][1] - laser_point[0][1]
# dy = 95.99462 - 45.079235
# dx = 356.3794 - 338.7491