# K230 SDK CanMV Board Demo使用指南

## 概述

## Demo介绍

### GPU

源码路径在 `buildroot-overlay/package/vg_lite`，包含 5 个示例程序

- tiger: 渲染一张 640x480 的老虎图片并保存为 tiger.png

![tiger](https://www.kendryte.com/api/post/attachment?id=422)

- linearGrad: 渲染一张渐变图案并保存为 linearGrad.png

![linearGrad](https://www.kendryte.com/api/post/attachment?id=423)

- imgIndex: 渲染四张使用颜色查找表的图像并保存为 png 文件

- vglite_drm: 在屏幕上显示使用 GPU 绘制的图案

- vglite_cube: 在屏幕上显示使用 GPU 绘制的一个正方体边框

### 人脸检测

人脸检测demo输入源为摄像头，并将结果显示在屏幕上，此demo仅用于演示KPU、nncase有关AI方面的功能。

源码位置`buildroot-overlay\package\face_detect`，可执行程序放置在`output/k230_canmv_defconfig/target/app/face_detect`，在板子上进入 `/app/face_detct`，执行 `./face_detect.elf face_detection_320.kmodel` 即可。会在屏幕上框出人脸的位置。

![结果](https://www.kendryte.com/api/post/attachment?id=429)

### 摄像头采图显示

v4l2-drm 从摄像头采集图像并显示到屏幕上，源码路径在 `buildroot-overlay/package/vvcam/v4l2-drm`

使用命令行 `v4l2-drm -d 1 -w 480 -h 320` 即可运行

`-d` 指定 video 设备

`-w` 指定图像宽度

`-h` 指定图像高度

`-f` 指定图像格式，支持 `NV12/NV16/BGR3/BG3P`，目前仅 `NV12` 和 `BGR3` 支持显示

`-s` 禁用显示（只采图），程序运行后按 `q` 退出，按 `d` 保存一张图片。可以同时打开多个设备，例如 `v4l2-drm -d 1 -w 480 -h 320 -d 2 -w 1920 -h 1080 -f BGR3 -s`.

### 摄像头采图推流

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

![ffplay](https://www.kendryte.com/api/post/attachment?id=430)

### Audio

#### 使用 `audio_demo` 实现音频录制和播放

`audio_demo` 是一个运行在 K230 开发板上的示例程序，通过调用 ALSA（Advanced Linux Sound Architecture）API，实现音频的录制和播放功能。该示例程序不仅展示了如何在 K230 开发板上进行音频处理，还为开发者提供了使用 ALSA API 接口实现音频功能的参考代码。

##### 录制 WAV 文件

使用以下命令录制一个 WAV 格式的音频文件：

```sh
audio_demo -type 2 -filename test.wav -channels 2 -samplerate 16000
```

参数说明：

- `-type 2`：指定操作类型为录制。
- `-filename`：设置输出文件名。
- `-channels`：录制通道数，`2` 为双声道。
- `-samplerate`：设置采样率，单位为 Hz。

录制15s后进程会自动退出(请勿录制过程中杀掉进程，否则会导致录制的文件异常)，音频文件保存在当前目录下的 `test.wav` 中。

##### 播放 WAV 文件

使用以下命令播放录制的 WAV 文件：

```sh
audio_demo -type 0 -filename test.wav
```

参数说明：

- `-type 0`：指定操作类型为播放 WAV 文件。
- `-filename`：要播放的文件名。

##### 播放 MP3 文件

`audio_demo` 也支持播放 MP3 格式的音频文件：

```sh
audio_demo -type 1 -filename example.mp3
```

参数说明：

- `-type 1`：指定操作类型为播放 MP3 文件。
- `-filename`：要播放的 MP3 文件名。

#### 使用 FFmpeg 实现音频录制和播放

##### 音频录制

使用以下命令，通过FFmpeg调用ALSA接口录制声音，并保存为WAV文件：

```bash
ffmpeg -f alsa -i hw:0 -t 15 -ac 2 -ar 44100 -y test.wav
```

其中：

- `-f alsa`：指定音频输入格式为ALSA。
- `-i hw:0`：指定音频输入设备，`hw:0`表示默认音频设备。
- `-t 15`：设置录制时长为15秒。
- `-ac 2`：设置录制通道数为2（立体声）。
- `-ar 44100`：设置采样率为44100Hz。
- `-y test.wav`：输出文件名为`test.wav`。

执行上述命令后，录制的声音将保存为WAV格式的音频文件`test.wav`。

##### 音频播放

使用 `ffmpeg` 播放音频文件：

```sh
ffmpeg -i test.wav -f alsa hw:0,0
```

#### 使用 `arecord` 和 `aplay` 实现音频录制和播放

##### 录制音频

```sh
arecord -Dhw:0,0 -d 10 -f cd -r 44100 -c 2 -t wav test.wav
```

##### 播放音频

```sh
aplay -Dhw:0,0 -v test.wav
```

#### 音量控制

使用 `amixer` 命令进行音量调节和静音控制：

##### 音量控制

- 查看控件列表：

    ```sh
    amixer controls
    ```

- 获取当前音量：

    ```sh
    amixer cget numid=1
    ```

- 设置音量为 12：

    ```sh
    amixer cset numid=1 12
    ```

##### 静音控制

- 静音：

    ```sh
    amixer cset numid=2 0
    ```

- 取消静音：

    ```sh
    amixer cset numid=2 1
    ```
