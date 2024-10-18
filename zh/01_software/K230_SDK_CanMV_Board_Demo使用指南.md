# K230 SDK CanMV Board Demo使用指南

## 1. 概述

## 2. Demo介绍

### 2.1 GPU

源码路径在 `buildroot-overlay/package/vg_lite`，包含 5 个示例程序

- tiger: 渲染一张 640x480 的老虎图片并保存为 tiger.png ![tiger](https://developer.canaan-creative.com/api/post/attachment?id=422)
- linearGrad: 渲染一张渐变图案并保存为 linearGrad.png ![linearGrad](https://developer.canaan-creative.com/api/post/attachment?id=423)
- imgIndex: 渲染四张使用颜色查找表的图像并保存为 png 文件
- vglite_drm: 在屏幕上显示使用 GPU 绘制的图案
- vglite_cube: 在屏幕上显示使用 GPU 绘制的一个正方体边框

### 2.2 人脸检测

人脸检测demo输入源为摄像头，并将结果显示在屏幕上，此demo仅用于演示KPU、nncase有关AI方面的功能。

源码位置`buildroot-overlay\package\face_detect`，可执行程序放置在`output/k230_canmv_defconfig/target/app/face_detect`，在板子上进入 `/app/face_detct`，执行 `./face_detect.elf face_detection_320.kmodel` 即可。会在屏幕上框出人脸的位置。

![结果](https://developer.canaan-creative.com/api/post/attachment?id=429)

### 2.3 摄像头采图显示

v4l2-drm 从摄像头采集图像并显示到屏幕上，源码路径在 `buildroot-overlay/package/vvcam/v4l2-drm`，使用命令行 `v4l2-drm -d 1 -w 480 -h 320` 即可运行，`-d` 指定 video 设备，`-w` 指定图像宽度，`-h` 指定图像高度，`-f` 指定图像格式，支持 `NV12/NV16/BGR3/BG3P`，目前仅 `NV12` 和 `BGR3` 支持显示，`-s` 禁用显示（只采图），程序运行后按 `q` 退出，按 `d` 保存一张图片。可以同时打开多个设备，例如 `v4l2-drm -d 1 -w 480 -h 320 -d 2 -w 1920 -h 1080 -f BGR3 -s`.

### 2.4 摄像头采图推流

可以使用 ffmpeg 打开 `/dev/video1` 设备进行编码和推流到 PC，首先在PC上安装 ffmpeg，然后创建一个 `test.sdp` 文件，填入如下内容

```sdp
SDP:
v=0
o=- 0 0 IN IP4 127.0.0.1
s=No Name
c=IN IP4 10.100.228.227
t=0 0
a=tool:libavformat 58.76.100
m=video 1233 RTP/AVP 96
b=AS:20000
a=rtpmap:96 H264/90000
a=fmtp:96 packetization-mode=1
```

其中 `10.100.228.227` 改为 PC 的 IP 地址，然后在 PC 上运行

```shell
ffplay -protocol_whitelist "file,udp,rtp,tcp" -i test.sdp -fflags nobuffer -analyzeduration 1000000 -flags low_delay
```

之后在板子上运行

```shell
ffmpeg -f v4l2 -i /dev/video1 -video_size 1920x1080 -vsync pass
through -vcodec h264_v4l2m2m -b:v 10M -f rtp rtp://10.100.228.227:1233
```

注意将其中的 `10.100.228.227` 改为 PC 的 IP 地址。

![ffplay](https://developer.canaan-creative.com/api/post/attachment?id=430)
