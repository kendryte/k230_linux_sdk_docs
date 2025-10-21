# Opencv调用UVC指南

## 概述

本文将讲解如何在k230开发板Linux侧驱动USB摄像头，并通过opencv调用uvc。sdk默认镜像已经包含向量加速的opencv。本文档以01studio板子为例。

### 检查uvc设备状态及信息

```sh
lsusb #查看usb设备信息
v4l2-ctl --list-devices  #命令查看所有支持v4l2的摄像头信息
v4l2-ctl -d /dev/video1 --all #查看摄像头所有信息
v4l2-ctl --list-formats-ext --device /dev/video1 #查询可输出的图像格式
```

#### 使用 ` lsusb ` 命令查看usb设备信息

```sh
[    2.350021] usb 1-1: New USB device found, idVendor=0bda, idProduct=8152, bcdDevice=20.00
[    2.358228] usb 1-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[    2.365370] usb 1-1: Product: USB 10/100 LAN
[    2.369647] usb 1-1: Manufacturer: Realtek
[    2.373748] usb 1-1: SerialNumber: 00E04C421C8E
[    2.410027] usb 2-1: config 1 interface 0 altsetting 0 endpoint 0x83 has an invalid bInterval 32, changing to 9
[    2.420336] usb 2-1: New USB device found, idVendor=1b3f, idProduct=2247, bcdDevice= 1.00
[    2.428541] usb 2-1: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[    2.435690] usb 2-1: Product: GENERAL WEBCAM
[    2.439973] usb 2-1: Manufacturer: GENERAL
[    2.444796] usb 2-1: Found UVC 1.00 device GENERAL WEBCAM (1b3f:2247)
[    2.453534] usb 2-1: UVC non compliance - GET_DEF(PROBE) not supported. Enabling workaround.


[root@canaan ~ ]#lsusb
Bus 002 Device 002: ID 1b3f:2247
Bus 001 Device 001: ID 1d6b:0002
Bus 001 Device 002: ID 0bda:8152
Bus 002 Device 001: ID 1d6b:0002
[root@canaan ~ ]#

```

#### 使用`v4l2-ctl --list-devices`命令查看所有支持v4l2的摄像头信息

```sh
[root@canaan ~ ]#v4l2-ctl --list-devices
Linlon Video device (platform:mvx):
        /dev/video0

vvcam-isp-subdev.0 (platform:vvcam-isp-subdev.0):
        /dev/v4l-subdev0

verisilicon_media (platform:vvcam-video.0):
        /dev/media1

vvcam-video.0.0 (platform:vvcam-video.0.0):
        /dev/video3

vvcam-video.0.1 (platform:vvcam-video.0.1):
        /dev/video4

vvcam-video.0.2 (platform:vvcam-video.0.2):
        /dev/video5

vvcam-video.0.3 (platform:vvcam-video.0.3):
        /dev/video6

GENERAL WEBCAM: GENERAL WEBCAM (usb-91540000.usb-1):
        /dev/video1
        /dev/video2
        /dev/media0

[root@canaan ~ ]#

```

#### 使用` v4l2-ctl -d /dev/video1 --all `查看摄像头的所有信息

```sh
[root@canaan ~ ]#v4l2-ctl -d /dev/video1 --all
Driver Info:
        Driver name      : uvcvideo
        Card type        : GENERAL WEBCAM: GENERAL WEBCAM
        Bus info         : usb-91540000.usb-1
        Driver version   : 6.6.36
        Capabilities     : 0x84a00001
                Video Capture
                Metadata Capture
                Streaming
                Extended Pix Format
                Device Capabilities
        Device Caps      : 0x04200001
                Video Capture
                Streaming
                Extended Pix Format
Media Driver Info:
        Driver name      : uvcvideo
        Model            : GENERAL WEBCAM: GENERAL WEBCAM
        Serial           :
        Bus info         : usb-91540000.usb-1
        Media version    : 6.6.36
        Hardware revision: 0x00000100 (256)
        Driver version   : 6.6.36
Interface Info:
        ID               : 0x03000002
        Type             : V4L Video
Entity Info:
        ID               : 0x00000001 (1)
        Name             : GENERAL WEBCAM: GENERAL WEBCAM
        Function         : V4L2 I/O
        Flags            : default
        Pad 0x01000007   : 0: Sink
          Link 0x02000013: from remote pad 0x100000a of entity 'Extension 7' (Video Pixel Formatter): Data, Enabled, Immutable
Priority: 2
Video input : 0 (Camera 1: ok)
Format Video Capture:
        Width/Height      : 1920/1080
        Pixel Format      : 'MJPG' (Motion-JPEG)
        Field             : None
        Bytes per Line    : 0
        Size Image        : 1843200
        Colorspace        : sRGB
        Transfer Function : Rec. 709
        YCbCr/HSV Encoding: ITU-R 601
        Quantization      : Default (maps to Full Range)
        Flags             :
Crop Capability Video Capture:
        Bounds      : Left 0, Top 0, Width 1920, Height 1080
        Default     : Left 0, Top 0, Width 1920, Height 1080
        Pixel Aspect: 1/1
Selection Video Capture: crop_default, Left 0, Top 0, Width 1920, Height 1080, Flags:
Selection Video Capture: crop_bounds, Left 0, Top 0, Width 1920, Height 1080, Flags:
Streaming Parameters Video Capture:
        Capabilities     : timeperframe
        Frames per second: 30.000 (30/1)
        Read buffers     : 0

User Controls

                     brightness 0x00980900 (int)    : min=1 max=255 step=1 default=-8193 value=16
                       contrast 0x00980901 (int)    : min=1 max=255 step=1 default=57343 value=16
                            hue 0x00980903 (int)    : min=-128 max=127 step=1 default=-8193 value=16
           power_line_frequency 0x00980918 (menu)   : min=0 max=2 default=2 value=2 (60 Hz)
                                0: Disabled
                                1: 50 Hz
                                2: 60 Hz

Camera Controls

[root@canaan ~ ]#

```

#### 使用 ` v4l2-ctl --list-formats-ext --device /dev/video1 ` 查询可输出的图像格式

```sh
[root@canaan ~ ]#v4l2-ctl --list-formats-ext --device /dev/video1
ioctl: VIDIOC_ENUM_FMT
        Type: Video Capture

        [0]: 'MJPG' (Motion-JPEG, compressed)
                Size: Discrete 1920x1080
                        Interval: Discrete 0.033s (30.000 fps)
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 1440x1080
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 1280x720
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 800x600
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 800x480
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 720x480
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 640x480
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 640x360
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 480x270
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 320x240
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 176x144
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 1920x1080
                        Interval: Discrete 0.033s (30.000 fps)
                        Interval: Discrete 0.033s (30.000 fps)
        [1]: 'YUYV' (YUYV 4:2:2)
                Size: Discrete 800x480
                        Interval: Discrete 0.033s (30.000 fps)
                        Interval: Discrete 0.033s (30.000 fps)
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 720x480
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 640x480
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 640x360
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 480x270
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 320x240
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 176x144
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 800x480
                        Interval: Discrete 0.033s (30.000 fps)
                        Interval: Discrete 0.033s (30.000 fps)
                        Interval: Discrete 0.033s (30.000 fps)
[root@canaan ~ ]#
```

### 使用v4l获取图像

使用`v4l2-ctl --device /dev/video1 --stream-mmap --stream-to=video0-output.jpg --stream-count=1`命令采集一张jpg图片

```sh
[root@canaan ~ ]#v4l2-ctl --device /dev/video0 --stream-mmap --stream-to=video0-
output.jpg --stream-count=1
<
[root@canaan ~ ]#ls -lh
total 222K
-rw-r--r--    1 root     root      221.7K Jan  1 00:11 video0-output.jpg
```

### opencv获取图像

#### c语言版本

拷贝`video_cap`测试应用到文件系统中并执行，会生成一个test.jpg文件

```sh
[root@canaan ~ ]#./video_cap
[root@canaan ~ ]#ls
nfs        test.jpg   video_cap
```

video_cap可通过命令` /opt/toolchain/Xuantie-900-gcc-linux-6.6.0-glibc-x86_64-V2.10.1/bin/riscv64-unknown-linux-gnu-g++  --sysroot=output/k230_canmv_01studio_defconfig/host/riscv64-buildroot-linux-gnu/sysroot video_cap.cpp  -lopencv_videoio -lopencv_core -lopencv_imgcodecs -o video_cap `来编译生成，video_cap.cpp源码如下：

```cpp
#include "opencv2/opencv.hpp"
using namespace cv;

int main()
{
    VideoCapture capture(1);
    Mat frame;
    capture>>frame;
    imwrite("test.jpg", frame);
    return 0;
}
```

#### python版本

使用如下python脚本可以获取一张图像

```python
import cv2

# 初始化摄像头
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

# 抓取一帧图像
ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame from video device.")
    cap.release()
    exit()

# 保存图像
image_filename = 'captured_image.jpg'
cv2.imwrite(image_filename, frame)
print(f"Image saved as {image_filename}")

# 释放摄像头资源
cap.release()

```

### 用户应用

1. 通过v4l接口去采集图像，具体请参考`v4l用户编程API`或`v4l-utils源码`
1. 通过opencv接口去采集图像，具体请参考`opencv编程`

### 参考连接

[K230_Opencv调用UVC指南](https://www.kendryte.com/k230/zh/dev/02_applications/tutorials/K230_Opencv%E8%B0%83%E7%94%A8UVC%E6%8C%87%E5%8D%97.html#id1)
