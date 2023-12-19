

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

**Chuyển đổi từ các thư viện sang inference engine với TensorRT.**

![Chuyển đổi từ các thư viện sang inference engine với TensorRT](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/01c0779b-11cd-4fec-860a-ee61b4c7fde4)


Để sử dụng YOLO trên GPU của Jetson Nano, chúng tôi thực hiện quá trình tổng hợp “YOLO engine” cho mô hình đã được huấn luyện [15]. Quá trình này gồm các bước sau: tạo tệp trọng số WTS (Weight Tensor Serialization), cài đặt CMake và Make, tạo engine và kiểm thử. Kết quả của quá trình này là việc sử dụng được mô hình đã huấn luyện trên GPU của Jetson Nano, từ đó sử dụng mô hình để phát hiện các đối tượng cỏ hoặc cây.
Các bạn có thể tham khảo kênh ![Rocker Systems](https://www.youtube.com/watch?v=n9BSrfqpVFA&t=177s) cho việc setup yolov7 trên jetson nano

### Tích hợp thị giác máy tính và lập trình điều khiển 
Sơ đồ nguyên lý tích hợp thị giác máy tính và điều khiển động cơ cho robot diệt cỏ được minh họa trong . Về nguyên lý, thị giác máy tính được xử lý thông qua camera gắn trên robot và YOLOv8n trên Jetson nano. Kết quả trả về bao gồm có loại vật thể (cỏ hoặc cây), độ tin cậy, và tọa độ của các hộp bao quanh vật thể. Tọa độ gồm có 4 thông số x, y, w, h đại diện cho tọa độ tâm (x, y) của hộp, w là chiều rộng, và h là chiều cao. Tọa độ và loại vật thể sẽ được sử dụng là đầu vào cho việc điều khiển các cơ cấu chấp hành của robot bao gồm 4 động cơ DC để di chuyển, 3 động cơ bước để di chuyển đầu laser theo phương (X, Y), và bật tắt đầu laser. Các động cơ bước sẽ di chuyển từ vị trí ban đầu, đến từng vị trí cỏ dại, bật đầu laser để tiêu diệt cỏ, sau đó di chuyển đến vị trí kế tiếp cho đến khi cỏ dại không còn ghi nhận bởi camera thì kết thúc quá trình và di chuyển đến vị trí tiếp theo. 

![image](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/238d0fab-9a68-4921-8264-57596c65db17)

Về cơ bản thì khi bạnbạn clone project của chúng tôi đã được cài sẵn yolov7 nếu bản muốn biết thêm thông tin về yolov7 thì bạn có xem qua 
source code của [Yolov7](https://github.com/WongKinYiu/yolov7)
