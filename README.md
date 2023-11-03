

# Robot diệt cỏ bằng laser sử dụng YOLOv7
Bùi Huy Kiên, Đặng Minh Hiếu, Nguyễn Đức Hiếu
Vietnam National University - Vietnam Japan University

## Phần cứng
## Jetson Nano 
Chúng tôi đã chọn Jetson Nano vì các lợi ích của nó trong việc thực hiện tác vụ xử lý hình ảnh và học máy. Jetson Nano cung cấp hiệu suất đủ mạnh để thực hiện các nhiệm vụ phức tạp như nhận diện đối tượng trong thời gian thực và có khả năng tích hợp cùng với TensorRT để tối ưu hóa hiệu suất trên GPU.

![Jetson Nano](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/cb74fe7e-9f46-47e6-b75f-34ba33065e3e)

## Thiết kế và lập trình nhúng trên nền tảng Jetson Nano
### Điều khiển tín hiệu vào ra với Jetson GPIO
Jetson GPIO là một giao diện GPIO (General Purpose Input/Output) được tích hợp sẵn trong dòng sản phẩm NVIDIA Jetson, chủ yếu dùng cho việc tương tác với các thiết bị ngoại vi hoặc cảm biến thông qua các chân GPIO trên mạch. Jetson GPIO cung cấp khả năng điều khiển và đọc tín hiệu từ các chân GPIO này, cho phép các ứng dụng và dự án sử dụng Jetson tận dụng các tính năng và kết nối phần cứng đa dạng.
[TensorRT](https://developer.nvidia.com/tensorrt)

TensorRT là một thư viện được phát triển bởi NVIDIA nhằm cải thiện tốc độ suy diễn ảnh, giảm độ trì truệ trên các thiết bị đồ ahọa NVIDIA (GPU). Nó có thể cải thiện tốc độ suy luận lên đến 2-4 lần so với các dịch vụ thời gian thực (real-time) và nhanh hơn gấp 30 lần so với hiệu suất của CPU. Về nguyên lý, TensorRT được sử dụng để triển khai các thư viện phục vụ cho học máy, học sâu cần đến xử lý đồ họa trên các phần cứng nhúng như mô tả trong Hình 6.

![Chuyển đổi từ các thư viện sang inference engine với TensorRT](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/01c0779b-11cd-4fec-860a-ee61b4c7fde4)


**Hình 6. Chuyển đổi từ các thư viện sang inference engine với TensorRT [14].**

Để sử dụng YOLO trên GPU của Jetson Nano, chúng tôi thực hiện quá trình tổng hợp “YOLO engine” cho mô hình đã được huấn luyện [15]. Quá trình này gồm các bước sau: tạo tệp trọng số WTS (Weight Tensor Serialization), cài đặt CMake và Make, tạo engine và kiểm thử. Kết quả của quá trình này là việc sử dụng được mô hình đã huấn luyện trên GPU của Jetson Nano, từ đó sử dụng mô hình để phát hiện các đối tượng cỏ hoặc cây.


### Hướng dẫn sử dụng YOLOv7 trên Jetson Nano
Trước tiên, download YOLOv7 thông qua lệnh git clone:

```bash
git clone https://github.com/WongKinYiu/yolov7.git
