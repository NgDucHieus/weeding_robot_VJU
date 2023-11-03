

# Robot diệt cỏ bằng laser sử dụng YOLOv7
Bùi Huy Kiên, Đặng Minh Hiếu, Nguyễn Đức Hiếu
Vietnam National University - Vietnam Japan University

## Phần cứng
## Thiết kế cơ khí robot
![image](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/b06b9b51-81ca-4d7b-93e1-a3907dbaaed6)
![image](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/387167cd-3ce1-4838-8fcb-3947122b7848)

Khung robot được xây dựng bằng nhôm định hình với kích thước dài rộng cao là 440x500x500 mm như trong trên. Động cơ bước sử dụng bộ truyền đai cung cấp khả năng trượt theo hai phương X và Y của đầu laser. Động cơ một chiều có thể điều chỉnh tốc độ và chiều quay để định hướng di chuyển. Các phần đồ gá, mặt bích, được thiết kế và gia công trên máy CNC để đảm bảo độ chính xác các vị trí của các thành phần của robot. 

## Jetson Nano 
Chúng tôi đã chọn Jetson Nano vì các lợi ích của nó trong việc thực hiện tác vụ xử lý hình ảnh và học máy. Jetson Nano cung cấp hiệu suất đủ mạnh để thực hiện các nhiệm vụ phức tạp như nhận diện đối tượng trong thời gian thực và có khả năng tích hợp cùng với TensorRT để tối ưu hóa hiệu suất trên GPU.

![Jetson Nano](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/cb74fe7e-9f46-47e6-b75f-34ba33065e3e)

## Thiết kế và lập trình nhúng trên nền tảng Jetson Nano
### Điều khiển tín hiệu vào ra với Jetson GPIO
Jetson GPIO là một giao diện GPIO (General Purpose Input/Output) được tích hợp sẵn trong dòng sản phẩm NVIDIA Jetson, chủ yếu dùng cho việc tương tác với các thiết bị ngoại vi hoặc cảm biến thông qua các chân GPIO trên mạch. Jetson GPIO cung cấp khả năng điều khiển và đọc tín hiệu từ các chân GPIO này, cho phép các ứng dụng và dự án sử dụng Jetson tận dụng các tính năng và kết nối phần cứng đa dạng.
Ở đây chúng tui sử dụng thư viện [Jetson.GPIO](https://github.com/NVIDIA/jetson-gpio) cho việc điều khiển tín hiệu In/Out. 

**Cổng IN/OUT với thư viện GPIO cho Jetson nano**

![Cổng IN/OUT với thư viện GPIO cho Jetson nano](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/0c86d889-10a6-411b-939b-e5e7563db116)

Trong dự án này, thư viện GPIO của Jetson nano được sử dụng để điều khiển 4 động cơ một chiều cho di chuyển tiến lùi của robot, 3 động cơ bước cho điều khiển vị trí của đầu laser, và bật tắt laser với nguyên lý độ rộng xung PWM (Pulse Width Modulation).

## Điều khiển động cơ
Đầu tiên hãy chắc chắn rằng bạn đã clone weedding_robot_VJU thông qua lệnh git clone
```bash
git clone https://github.com/hieucoolngau/weeding_robot_VJU.git
```
Tạo 1 file python mới trong folder weeding_robot_VJU sai đó import các class sau
```bash

### Cấu hình sử dụng trên GPU với Nvidia Tensor RT
[TensorRT](https://developer.nvidia.com/tensorrt) là một thư viện được phát triển bởi NVIDIA nhằm cải thiện tốc độ suy diễn ảnh, giảm độ trì truệ trên các thiết bị đồ ahọa NVIDIA (GPU). Nó có thể cải thiện tốc độ suy luận lên đến 2-4 lần so với các dịch vụ thời gian thực (real-time) và nhanh hơn gấp 30 lần so với hiệu suất của CPU. Về nguyên lý, TensorRT được sử dụng để triển khai các thư viện phục vụ cho học máy, học sâu cần đến xử lý đồ họa trên các phần cứng nhúng như mô tả trong hình dưới.

**Chuyển đổi từ các thư viện sang inference engine với TensorRT.**
![Chuyển đổi từ các thư viện sang inference engine với TensorRT](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/01c0779b-11cd-4fec-860a-ee61b4c7fde4)




Để sử dụng YOLO trên GPU của Jetson Nano, chúng tôi thực hiện quá trình tổng hợp “YOLO engine” cho mô hình đã được huấn luyện [15]. Quá trình này gồm các bước sau: tạo tệp trọng số WTS (Weight Tensor Serialization), cài đặt CMake và Make, tạo engine và kiểm thử. Kết quả của quá trình này là việc sử dụng được mô hình đã huấn luyện trên GPU của Jetson Nano, từ đó sử dụng mô hình để phát hiện các đối tượng cỏ hoặc cây.


### Tích hợp thị giác máy tính và lập trình điều khiển 
Sơ đồ nguyên lý tích hợp thị giác máy tính và điều khiển động cơ cho robot diệt cỏ được minh họa trong . Về nguyên lý, thị giác máy tính được xử lý thông qua camera gắn trên robot và YOLOv8n trên Jetson nano. Kết quả trả về bao gồm có loại vật thể (cỏ hoặc cây), độ tin cậy, và tọa độ của các hộp bao quanh vật thể. Tọa độ gồm có 4 thông số x, y, w, h đại diện cho tọa độ tâm (x, y) của hộp, w là chiều rộng, và h là chiều cao. Tọa độ và loại vật thể sẽ được sử dụng là đầu vào cho việc điều khiển các cơ cấu chấp hành của robot bao gồm 4 động cơ DC để di chuyển, 3 động cơ bước để di chuyển đầu laser theo phương (X, Y), và bật tắt đầu laser. Các động cơ bước sẽ di chuyển từ vị trí ban đầu, đến từng vị trí cỏ dại, bật đầu laser để tiêu diệt cỏ, sau đó di chuyển đến vị trí kế tiếp cho đến khi cỏ dại không còn ghi nhận bởi camera thì kết thúc quá trình và di chuyển đến vị trí tiếp theo. 

![image](https://github.com/hieucoolngau/weeding_robot_VJU/assets/116575807/238d0fab-9a68-4921-8264-57596c65db17)


```bash
git clone https://github.com/WongKinYiu/yolov7.git
