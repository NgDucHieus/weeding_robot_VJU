

# Wedding Robot using laser and YOLOv7
Bui Huy Kien, Dang Minh Hieu, Nguyen Duc Hieu
Vietnam National University - Vietnam Japan University

## HardWare
## Mechanical design
![image](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/b06b9b51-81ca-4d7b-93e1-a3907dbaaed6)
![image](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/387167cd-3ce1-4838-8fcb-3947122b7848)

The robot frame is crafted from profiled aluminum, measuring 440x500x500 mm as specified. Stepper motors are utilized with a belt transmission system, enabling smooth movement along both the X and Y axes for the laser head. The unidirectional motor is adjustable in speed and rotation direction to dictate the motion. Mounting components, including brackets and flanges, are intricately designed and precision-machined using CNC technology to ensure accurate positioning of the robot's elements.

## Jetson Nano 
We chose Jetson Nano for its benefits in image processing and machine learning tasks. The Jetson Nano offers sufficient power to handle complex tasks such as real-time object detection, and it comes with the capability to integrate seamlessly with TensorRT for optimizing performance on the GPU.

![Jetson Nano](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/cb74fe7e-9f46-47e6-b75f-34ba33065e3e)

## Designing and Programming on the Jetson Nano Platform
### Controlling Input and Output Signals with Jetson GPIO
Jetson GPIO is a GPIO (General Purpose Input/Output) interface integrated into the NVIDIA Jetson product line, primarily used for interacting with peripheral devices or sensors through GPIO pins on the board. Jetson GPIO provides the capability to control and read signals from these GPIO pins, allowing applications and projects utilizing Jetson to leverage a variety of hardware features and connections.
We use the [Jetson.GPIO](https://github.com/NVIDIA/jetson-gpio) for controlling input and outut signals. 

**Input/Output Ports with the GPIO Library for Jetson Nano**

![Input/Output Ports with the GPIO Library for Jetson Nano](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/0c86d889-10a6-411b-939b-e5e7563db116)

In this project, the GPIO library is used to control 4 DC motors for the forward and backward movement of the robot, 3 stepper motors for controlling the position of the laser , and toggling the laser using the Pulse Width Modulation (PWM) principle for pulse width control.

## Motor Control
Make sure that you have cloned the weedding_robot_VJU repository using the git clone command.
```bash
git clone https://github.com/hieucoolngau/weeding_robot_VJU.git
```
Create a new Python file in the weeding_robot_VJU folder and then import the following classes.Tạo 1 file python mới trong folder weeding_robot_VJU sai đó import các class sau
```bash
import Jetson.GPIO as GPIO
import time
from step_motor import  StepMotor13, StepMotor2
from dc_motor import Dc_Motor
from laser import Laser
```
Create an object StepMotor13():
```bash
stepMotor13 =  StepMotor13() #điều khiển hai step motor theo trục Y
stepMotor2 = StepMotor2() #điều khiên step motor cho phép dịch chuyển laser đến vị trí chọn
laser = laser() #tạo object laser
```
After initializing the object, you can use the methods as follows.
```bash
stepMotor13.move(GPIO.LOW,GPIO.HIGH,200) #thuộc tính đầu tiên mặc định là LOW, thuộc tính thứ là HIGH đại diện cho direction bạn có thể đổi chiều quay bằng cách chuyển HIGH thành LOW,
                                    #thuộc tính cuối cùng là số vòng lặp,vòng lặp càng lớn thì step motor quay cảng lâu
#tương tự với step_Motor2
stepMotor2.move(GPIO.LOW,GPIO.HIGH,200)
#với laser
laser.ON() #tức là bật laser
laser.OFF()#tức là tắt laser
laser.CHECK()#lúc này laser sẽ chớp tắt liên tục, bạn có thể điều chỉnh thời gian chớp tắt của laser
```


### Configure GPU with Nvidia TensorRT
[TensorRT](https://developer.nvidia.com/tensorrt) is a library developed by NVIDIA to enhance the inference speed of deep learning models, reducing latency on NVIDIA graphics processing units (GPUs). It can improve inference speed by up to 2-4 times compared to real-time services and is over 30 times faster than CPU performance. In principle, TensorRT is used to deploy libraries that serve machine learning and deep learning, requiring graphics processing for embedded hardware, as illustrated in the diagram below.

**Converting libraries to an inference engine with TensorRT**

![Converting libraries to an inference engine with TensorRT](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/01c0779b-11cd-4fec-860a-ee61b4c7fde4)


To use YOLO on the Jetson Nano GPU, we perform the synthesis process of the "YOLO engine" for the pre-trained model [15]. This process involves the following steps: creating a Weight Tensor Serialization (WTS) file, installing CMake and Make, building the engine, and testing. The result of this process is the ability to use the trained model on the Jetson Nano GPU, allowing the model to detect objects such as weeds or trees.
You can refer to this channel ![Rocker Systems](https://www.youtube.com/watch?v=n9BSrfqpVFA&t=177s) for setup YOLOv7 on JETSON NANO

### Integrating computer vision and control programming
The conceptual diagram for the integration of computer vision and motion control in a weed-killing robot is depicted as follows. In essence, computer vision is executed through a camera affixed to the robot and YOLOv8n on Jetson Nano. The outcomes include object categorization (weed or plant), confidence level, and the coordinates of bounding boxes around the detected objects. These coordinates consist of 4 parameters: x, y, w, h, representing the central coordinates (x, y) of the box, where w is the width, and h is the height.

These coordinates, along with the object type, are utilized as inputs for managing the robot's actuators. This includes 4 DC motors for locomotion, 3 stepper motors for positioning the laser head in both the (X, Y) directions, and toggling the laser head on/off. The stepper motors will traverse from the initial position to each weed location, activate the laser head to eradicate the weed, and then move on to the subsequent position. This process repeats until no more weeds are detected by the camera, signaling the end of the operation, after which the robot proceeds to the next designated location.

![image](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/238d0fab-9a68-4921-8264-57596c65db17)

Basically, when you clone our project, YOLOv7 is pre-installed. If you want to learn more about YOLOv7, you can review the source code [Yolov7](https://github.com/WongKinYiu/yolov7)
