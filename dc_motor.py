import Jetson.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Dc_Motor:

# GPIO.setup(21, GPIO.OUT)  #en1
    GPIO.setup(11, GPIO.OUT)  #in1
    GPIO.setup(12, GPIO.OUT)  #in2 
# GPIO.setup(22, GPIO.OUT)  #en2-//*-
    GPIO.setup(15, GPIO.OUT)  #in3
    GPIO.setup(16, GPIO.OUT)  #in4

    def stop(self):
        GPIO.output(11,GPIO.LOW)
        GPIO.output(12,GPIO.LOW)
        GPIO.output(15,GPIO.LOW)
        GPIO.output(16,GPIO.LOW)

    def move_forward(self,x=5,m=0.00001):
        for i in range(x):
            GPIO.output(11,GPIO.HIGH)
            GPIO.output(15,GPIO.HIGH)
            time.sleep(m)
            GPIO.output(11,GPIO.LOW)
            GPIO.output(15,GPIO.LOW)
    def move_backward(self,x=5,m=0.00001):
        for i in range(x):
            GPIO.output(12,GPIO.HIGH)
            GPIO.output(16,GPIO.HIGH)
            time.sleep(m)
            GPIO.output(12,GPIO.LOW)
            GPIO.output(16,GPIO.LOW)
   
    