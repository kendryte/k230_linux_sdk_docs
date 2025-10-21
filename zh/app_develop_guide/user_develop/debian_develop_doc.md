# K230 debian 系统指南

```c

快速入门

用户配置使用
    网络,软件安装等；

c/c++开发参考
    外设/多媒体/ai

python开发参考
    外设/多媒体/ai

```

## 快速入门

### 镜像获取

镜像的名字类似如下：CanMV-K230_01studio_debian_v0.6.4_nncase_v2.9.0.img.gz
用户可在嘉楠开发者社区 下载镜像，或者参考如下命令自己编译镜像

```bash
git clone git@github.com:kendryte/k230_linux_sdk.git
# git clone git@gitee.com:kendryte/k230_linux_sdk.git
cd k230_linux_sdk
make CONF=k230_canmv_01studio_defconfig # 01studio
# make CONF=k230_canmv_defconfig #k230_canmv
sudo make debian   # genration debian image
```

生成的debian镜像名字类似如下：
output/k230_canmv_01studio_defconfig/images/CanMV-K230_01studio_debian_v0.6.4_nncase_v2.9.0.img.gz

### 镜像烧录

请参考固件下载指南 将固件烧录到开发板。

### 连接串口

cpu串口默认参数:115200 8 1 无流控；
部分开发板自带usb转串口芯片(ch34x)，这类开发板直接把对应usb连接到电脑，电脑上安装对应驱动(ch34x)后，putty串口参数设置正确，按下reset按键就可以看到cpu的输出。
如果板子不带usb转串口芯片，需要外接usb转串口小板，电脑上安装串口小板驱动，才能看到cpu的串口输出。
需要外接usb转串口小板芯片的开发板：01studio，嘉立创

### 串口登录系统

在串口上看到登录提示后，用户名root和密码root后，可以进入系统；

## 配置使用

说明：用户和密码均为root,可以通过apt install安装软件；

### 有线网络配置

如果有线网络通过dhcp上网，参考命令如下:

```bash
#使用systemd-networkd 配置网络；dhcp
cat >/etc/systemd/network/10-eth0.network <<EOF
[Match]
Name=en*

[Network]
DHCP=yes
EOF

systemctl disable networking
systemctl enable --now systemd-networkd
systemctl restart systemd-networkd
#net.ifnames=0 biosdevname=0
#ip route show default 查看默认网关；
#ip route
```

如果有线网络需要静态ip，请参考如下命令进行配置：

```bash
#使用systemd-networkd 配置网络；静态ip
cat >/etc/systemd/network/10-eth0.network    <<EOF
[Match]
Name=en*

[Network]
Address=10.100.228.118/24
Gateway=10.100.228.254
DNS=10.253.0.1
EOF
systemctl disable networking
systemctl stop  systemd-networkd
systemctl restart systemd-networkd
```

### 无线网络配置

如果需要通过无线上网，请参考如下命令：

```bash
#date -s "2025-04-14 11:15:20"
apt install wpasupplicant
#执行sta.sh脚本可以连接wifi,例如:
sta.sh wlan0  canaan_wifi  123456789
#ssid是canaan_wifi,密码是123456789
```

### ntp开机自动校时和时区配置

开机自带校时和时区配置参考如下：

```bash
apt install systemd-timesyncd
rm -rf /etc/localtime; ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime;
systemctl enable  systemd-timesyncd
```

### 普通软件安装

安装软件的apt命令依赖网络和时间，如果时间不对，请手动调整下时间。

```bash
#先date 看下时间是否正确，如果时间不对请参考下面命令设置下时间
#date -s "2025-04-14 11:15:20"
apt-get update
apt install wpasupplicant
```

### ssh远程终端

如果需要通过ssh登录设备，请参考如下命令在板子上安装ssh server：

```bash
apt install  -y   openssh-server
echo "PermitRootLogin yes" >> etc/ssh/sshd_config
systemctl restart ssh
```

### 开机自动运行脚本

如果需要实现开机自启动某个脚本，请参考如下命令：

```bash
#参考如下命令设置开机自启动
cat << 'EOF' > /opt/mount_boot.sh
#!/bin/bash
bootddev=$(cat /proc/cmdline  | sed  -n  "s#root=\(\/dev\/mmcblk[0-9]\).*#\1#p" )
sd_size=$(parted ${bootddev} print | grep ${bootddev} | cut -d: -f2)
parted ${bootddev} resizepart 2 ${sd_size}; resize2fs ${bootddev}p2
mount ${bootddev}p1 /boot
EOF
chmod a+x /opt/mount_boot.sh

cat >/etc/systemd/system/mount_boot.service <<EOF
#大模型搜索 debian系统如何 开机自动运行脚本 systemd 就可以了；
[Unit]
Description=mount_boot_part
After=rc-local.service

[Service]
Type=oneshot
ExecStart=/opt/mount_boot.sh
RemainAfterExit=no

[Install]
WantedBy=basic.target
EOF

systemctl enable mount_boot.service
```

### sensor及显示测试

sensor及显示相关命令如下，具体含义见注释

```bash
apt-get install libdrm2
#安装k230 isp驱动包
dpkg -i /root/deb/k230-vvcam.deb
#在显示器上显示东西，可以测试gpu和显示器是否正常
vglite_drm
#在显示器上显示东西，可以测试gpu和显示器是否正常
vglite_cube
#在显示器上显示摄像头实时画面
v4l2-drm -d 1 -n 5 -w 640 -h 480
```

### 人脸识别demo安装及测试

```bash
#安装人脸识别demo相关包
apt-get install  -y libdrm2  libgomp1 libwebp7  libpng-dev  libopus-dev
dpkg -i /root/deb/k230-vvcam.deb    /root/deb/k230-opencv4.deb  /root/deb/k230-ffmpeg.deb   /root/deb/k230-face-detect.deb
#运行人脸识别demo
cd /app/face_detect;./run_cv.sh
```

### 多媒体测试

```bash
#适配编码
dpkg -i deb/k230-mvx-player.deb
#查找vpu设备    video0 为编解码器设备 video1为摄像头设备。
v4l2-ctl --list-devices
#使用以下命令捕获摄像头画面并保存为NV12格式的图像，分辨率为1080p，捕获25帧图像。可以使用yuvview软件查看视频
#请确保数据写入速度快于摄像头的采集速度，否则请降低摄像头的分辨率。
v4l2-ctl --device=/dev/video1 --set-fmt-video=width=1920,height=1080,pixelformat=NV12 --stream-mmap --stream-count=25 --stream-to=output.yuv
#视频解码使用以下命令将H.264格式的视频文件解码为NV12格式的图像文件：
mvx_decoder --dev /dev/video0 -i h264 -o yuv420_nv12 test.264 output1.yuv
#使用以下命令，通过FFmpeg采集摄像头视频，并调用VPU编码保存为MP4文件：
ffmpeg -f v4l2 -input_format nv12 -r 30 -s 1920x1080 -i /dev/video1 -c:v h264_v4l2m2m -b:v 4M -vsync passthrough -y test.mp4
#如下命令有错误，通过FFmpeg采集摄像头图像，并调用VPU编码保存为JPEG文件
ffmpeg -f v4l2 -input_format nv12 -s 1920x1080 -i /dev/video1 -vframes 10 -vf format=nv12 -c:v mjpeg_v4l2m2m -vsync passthrough -y output_%03d.jpg
#如下命令也有错误
ffmpeg -f v4l2 -input_format nv12 -s 1920x1080 -i /dev/video1 -vframes 100 -vf format=nv12 -c:v mjpeg_v4l2m2m -vsync passthrough -y output.mjpeg
#有问题
ffmpeg -c:v h264_v4l2m2m -i test.mp4 -pix_fmt nv12 -f rawvideo -vsync passthrough -y output.yuv
```

### uvc摄像头测试

```bash
apt install v4l-utils ffmpeg usbutils
#列出系统中所有可用的 V4L2 设备及其相关信息
v4l2-ctl --list-devices
#要查看特定设备（例如 /dev/video0）的详细信息
v4l2-ctl -d /dev/video0 --all
#列出所有支持的格式和详细信息
v4l2-ctl -d /dev/video1 --list-formats-ext
#ffmpeg抓取一张图片；
ffmpeg -f v4l2 -i /dev/video1 -frames:v 1 -s 640x480 camera_capture.jpg
#视频文件录制 使用 H.264 编码器，分辨率 640x480，帧率 30fps，录制 10 秒到 record_10s.mp4
#纯cpu编码，非常慢，文件可以复制到电脑上使用vlc播放器播放；
ffmpeg -f v4l2 -i /dev/video1 -c:v libx264 -s 640x480 -r 15 -t 3 record_10s.mp4
#有问题
ffmpeg -f v4l2 -i /dev/video1 -c:v mpeg4_v4l2m2m -s 640x480 -r 15 -t 3 record_10s.mp4
#查看 ffmpeg 支持的编码器
ffmpeg -encoders | grep v4l2
```

### pyqt安装及测试

参考如下脚本安装pyqt5

```bash
apt update;apt  install  -y  qtbase5-dev qtbase5-examples python3-pyqt5
cat << EOF > /etc/profile.d/qt_env.sh
export QT_QPA_PLATFORM=linuxfb
export QT_QPA_FB_DRM=1
export QT_QPA_EGLFS_KMS_CONFIG="/root/kms_config.json"
EOF




cat << EOF > /root/kms_config.json
{
"device": "/dev/dri/card0",
"outputs": [
    { "name": "HDMI1", "format": "argb8888" }
]
}
EOF

```

参考如下命令测试pyqt5

```bash
cat << EOF >helloworld_pyqt.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QFont

def main():
    app = QApplication(sys.argv)  # 创建一个 QApplication 实例
    window = QWidget()  # 创建一个 QWidget 实例作为主窗口
    window.setWindowTitle('Hello World')  # 设置窗口标题
    label = QLabel('Hello World', window)  # 创建一个 QLabel 实例显示文本
    label.move(50, 50)  # 移动标签到窗口中的位置

    label = QLabel('王建新，，测试', window)  # 创建一个 QLabel 实例显示文本
    label.move(300, 400)  # 移动标签到窗口中的位置

    label.setFont(QFont('Arial', 30, QFont.Bold))
    label.setStyleSheet("QLabel { color: red; }")  # 设置字体颜色为红色


    label = QLabel('k230 pyqt5 测试', window)  # 创建一个 QLabel 实例显示文本
    label.move(500, 500)  # 移动标签到窗口中的位置

    label.setFont(QFont('Arial', 50, QFont.Bold))
    label.setStyleSheet("QLabel { color: red; }")  # 设置字体颜色为红色



    window.show()  # 显示窗口
    sys.exit(app.exec_())  # 进入 Qt 事件循环

if __name__ == '__main__':
    main()
EOF
python3 helloworld_pyqt.py
```

## C/c++ 语言开发参考

helloworld
向量测试
人脸识别

## pyhton开发参考

### 环境搭建

参考如下命令搭建验证python环境

```bash
apt update; apt install -y  python3 python3-pip
python3 --version
pip3 --version
cat << EOF >t.py
print("Hello, World!")
EOF
python3 t.py
```

### python opencv例子

参考如下命令搭建验证python opencv 环境

```bash
apt install -y  python3-opencv

cat << EOF >t.py
#把摄像头图像通过opencv显示在显示器上
import cv2
import time
import sys
import select
import os

# 指定要使用的摄像头索引。通常，内置摄像头是 0，外接 USB 摄像头可能是 1 或其他数字。
camera_index = 1
# 打开摄像头
cap = cv2.VideoCapture(camera_index)
# 检查摄像头是否成功打开
if not cap.isOpened():
    print(f"无法打开摄像头 {camera_index}")
    exit()

prev_time = 0
new_time = 0

while True:
    # 从摄像头读取一帧
    ret, frame = cap.read()
    # 检查是否成功读取帧
    if not ret:
        print("无法读取帧")
        break

    new_time = time.time()
    fps = 1 / (new_time - prev_time)
    prev_time = new_time
    fps = int(fps)

    # 在标准输出上打印帧率
    print(f"FPS: {fps}\r\n", end='\r')  # 使用 '\r' 回车符，使新的帧率覆盖旧的

    # 在窗口中显示帧
    cv2.imshow('Camera Feed', frame)

    # 等待按键 (按下 'q' 键退出循环)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n退出程序。")
        break
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        print("\n标准输入接收到字符退出！")
        break
    time.sleep(0.01)

# 释放摄像头资源
cap.release()
cv2.destroyAllWindows()

EOF
python3 t.py
```

### opencv检测人脸图片例子

```bash
 wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
wget -c  https://www.kendryte.com/api/post/attachment?id=602 -O 1.jpg
cat << EOF >t.py
import cv2
import sys

# 加载人脸检测器模型
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 加载图像
image_path = '1.jpg'  # 将 'your_image.jpg' 替换为你的图像文件路径
img = cv2.imread(image_path)

# 检查图像是否成功加载
if img is None:
    print(f"无法加载图像: {image_path}")
    sys.exit()

# 将图像转换为灰度图 (人脸检测通常在灰度图上进行)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 检测人脸
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

print(f"检测到 {len(faces)} 张人脸")

# 在检测到的人脸周围绘制矩形框
for (x, y, w, h) in faces:
    print(f"x={x}, y={y}, w={w}, h={h}")
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 绿色矩形，线宽为 2

# 显示结果图像
cv2.imshow('Face Detection', img)

# 等待按键 (按下任意键关闭窗口)
cv2.waitKey(0)
cv2.destroyAllWindows()
EOF
python3 t.py
```

### opencv检测人脸摄像头例子

```bash
 wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
#wget -c  https://www.kendryte.com/api/post/attachment?id=602 -O 1.jpg
cat << EOF >t.py
import cv2
import time

# 加载人脸检测器模型
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 打开摄像头 (通常内置摄像头是 0，外接 USB 摄像头可能是 1 或其他数字)
cap = cv2.VideoCapture(1)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 定义检测间隔帧数
detection_interval = 5
frame_count = 0
faces = []

# 初始化时间变量
prev_time = 0

while True:
    # 记录当前时间
    current_time = time.time()

    # 从摄像头读取一帧
    ret, frame = cap.read()

    # 检查是否成功读取帧
    if not ret:
        print("无法读取帧")
        break

    if frame_count % detection_interval == 0:
        # 将帧转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 检测人脸
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 在检测到的人脸周围绘制矩形框
    for (x, y, w, h) in faces:
        print(f"x={x}, y={y}, w={w}, h={h}")
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 计算帧率
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # 打印帧率
    print(f"FPS: {fps:.2f}")

    # 显示结果帧
    cv2.imshow('Live Face Detection', frame)

    # 等待按键 (按下 'q' 键退出循环)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

# 释放摄像头资源
cap.release()
cv2.destroyAllWindows()

EOF
python3 t.py
```
