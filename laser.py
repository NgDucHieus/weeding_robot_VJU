import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Laser:
    GPIO.setup(33, GPIO.OUT)  #in PWM

    def ON(self):
        GPIO.output(33,GPIO.HIGH)

    def OFF(self):
        GPIO.output(33,GPIO.LOW)

    def CHECK(self):
        for i in range(3):
            GPIO.output(33,GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(33,GPIO.LOW)
            time.sleep(0.5)
