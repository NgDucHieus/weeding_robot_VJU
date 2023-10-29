import Jetson.GPIO as GPIO
import time
import cv2
import imutils
from step_motor import StepMotor13, StepMotor2
from dc_motor import Dc_Motor
from laser import Laser
from yoloDet import YoloTRT

def setup_gpio():
    GPIO.setup(31, GPIO.OUT)  # EN2
    GPIO.setup(29, GPIO.OUT)  # Step2
    GPIO.setup(32, GPIO.OUT)  # Dir2
    GPIO.output(31, GPIO.LOW)
    GPIO.output(29, GPIO.LOW)
    GPIO.output(32, GPIO.LOW)

def detect_weed(cap, model):
    weed = []
    while True:
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=600)
        detections, t = model.Inference(frame)
        for obj in detections:
            print(obj['class'], obj['conf'], obj['box'])
            x, y, w, h = obj['box']
            if obj['class'] == 'Weed':
                weed.append([x, y])
        key = cv2.waitKey(1)
        if key == ord('q') or len(weed) != 0:
            break
    return weed

def detect_laser(cap, model):
    laser_point = []
    while True:
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=600)
        detections, t = model.Inference(frame)
        for obj in detections:
            print(obj['class'], obj['conf'], obj['box'])
            x, y, w, h = obj['box']
            if obj['class'] == 'Laser_pointer':
                laser_point.append([x, y])
        cv2.imshow("Output", frame)
        key = cv2.waitKey(1)
        if key == ord('q') or (len(laser_point) != 0):
            break
    return laser_point

def motor_control(stepX, stepY, scalex, scaley, dx, dy):
    if dx >= 0 and dy >= 0:
        stepY.move(GPIO.LOW, GPIO.LOW, round(dy / scaley))
        stepX.move(GPIO.LOW, GPIO.LOW, round(dx / scalex))
    # Add other motor control cases here

def calculate_distance(weed):
    dis = []
    for i in range(len(weed) - 1):
        dx = weed[i + 1][0] - weed[i][0]
        dy = weed[i + 1][1] - weed[i + 1][1]
        dis.append([dx, dy])
    return dis

def main():
    setup_gpio()
    laser1 = Laser()
    laser1.ON()
    model = YoloTRT(library="yolov7/build/libmyplugins.so", engine="yolov7/build/best_3_laser.engine", conf=0.5, yolo_ver="v7")
    cap = cv2.VideoCapture(0)

    weed = detect_weed(cap, model)
    laser_point = detect_laser(cap, model)

    stepY = StepMotor13()
    stepX = StepMotor2()

    scalex = 0.93 * (327.57727 - 299.96945) / 1000
    scaley = 1.149 * (97.85041 - 73.80898) / 1000

    dx = weed[0][0] - laser_point[0][0]
    dy = weed[0][1] - laser_point[0][1]

    motor_control(stepX, stepY, scalex, scaley, dx, dy)
    dis = calculate_distance(weed)
    for i in range(len(dis)):
        motor_control(stepX, stepY, scalex, scaley, dis[i][0], dis[i][1])

    time.sleep(3)
    laser1.OFF()

    GPIO.output(31, GPIO.LOW)
    GPIO.output(29, GPIO.LOW)
    GPIO.output(32, GPIO.LOW)
    GPIO.cleanup()

if __name__ == "__main__":
    main()
