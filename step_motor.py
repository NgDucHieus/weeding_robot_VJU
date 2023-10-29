import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(31, GPIO.OUT)  #en1
GPIO.setup(38, GPIO.OUT)  #step1&3
GPIO.setup(36, GPIO.OUT)  #dir1 

GPIO.setup(29, GPIO.OUT)  #en3
GPIO.setup(38, GPIO.OUT)  #step1&3
GPIO.setup(40, GPIO.OUT)  #dir3

GPIO.setup(32, GPIO.OUT)  #en2
GPIO.setup(37, GPIO.OUT)  #step2
GPIO.setup(35, GPIO.OUT)  #dir2

class StepMotor13:
    
    def move(self,EN, DIR, x, m=0.000001):

        GPIO.output(31,EN)
        GPIO.output(29,EN)

        GPIO.output(36,DIR)
        GPIO.output(40,not DIR)

        for i in range(x):
            GPIO.output(38, GPIO.HIGH)
            time.sleep(m)
            GPIO.output(38, GPIO.LOW)
            time.sleep(m)
      
    
    
        


class StepMotor2:
    def move(self,EN, DIR, x, m=0.000001):
        GPIO.output(32,EN)
        GPIO.output(35,DIR)
        for i in range(x):
            GPIO.output(37, GPIO.HIGH)
            time.sleep(m)
            GPIO.output(37, GPIO.LOW)
            time.sleep(m)
       
    



