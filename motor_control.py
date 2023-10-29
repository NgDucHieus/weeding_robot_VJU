import Jetson.GPIO as GPIO
import time
from step_motor import StepMotor13, StepMotor2
from dc_motor import Dc_Motor
from laser import Laser


# Chọn chế độ của GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

dc1 = Dc_Motor()
dc1.stop()
dc1.move_forward()





# step13 = StepMotor13()
# step2 = StepMotor2()

# dc1 = Dc_Motor()
# dc1.stop()

# laser1 = Laser() 
# killer1 = Weeding_Killer()



# laser1.ON()


# laser1.OFF()
# for i in range(100):
#     GPIO.output(18,GPIO.HIGH)
#     time.sleep(0.001)
#     GPIO.output(18,GPIO.LOW)
#     time.sleep(0.01)




# dc1.move_forward(500, 0.001)
# time.sleep(1)
# dc1.move_backward(500, 0.001)


# step13.move(GPIO.LOW, GPIO.HIGH, 1500, 0.00001)
# time.sleep(1)
# step13.move(GPIO.LOW, GPIO.LOW, 1500, 0.000001)

# laser1.ON()
# killer1.kill(100,0.0001)
# laser1.OFF()


# # step2.move(GPIO.HIGH, GPIO.HIGH, 3000, 0.00001)



GPIO.cleanup()