# 多媒体使用指南

## 概述

本指南旨在帮助用户了解和使用K230 Linux多媒体功能。主要内容包括如何使用V4L2 VPU（视频处理单元）和ALSA音频接口。指南中提供了直接调用V4L2和ALSA接口的示例代码，并介绍了如何使用FFmpeg工具进行多媒体处理，包括调用VPU和ALSA方法的详细步骤。

通过本指南，用户将能够：

- 掌握V4L2 VPU的使用方法，包括视频捕获、编码和解码，并提供v4l2视频编解码示例演示
- 学习ALSA音频接口的使用，包括音频采集和播放，并提供alsa音频采集播放示例演示
- 使用FFmpeg进行多媒体文件的转换和处理，并介绍如何调用VPU和ALSA方法

## V4L2 VPU使用指南

### 视频编码

在本节中，我们将演示如何使用VPU（视频处理单元）对NV12格式的图像进行编码。图像来源可以是从摄像头采集到的画面，也可以是其他文件作为编码器的视频输入源。

#### 编码器demo介绍

`mvx_encoder` 是一款利用 VPU（视频处理单元）进行硬件加速的视频编码命令行工具。它支持 H.264、H.265 和 JPEG 等编码格式，通过 V4L2（Video for Linux 2）接口与硬件设备交互，实现高效的编码性能。源码位于 `k230_linux_sdk/buildroot-overlay/package/mvx_player`。

使用以下命令将raw编码：

```bash
mvx_encoder --dev <vpu_device> -i <input_format> -w <width> -h <height> -o <output_format> <input_file> <output_file>
```

其中：

- `--dev <vpu_device>`：指定 vpu 设备路径。
- `-i <input_format>`：指定输入图像格式。
- `-w <width> -h <height>`：设置图像分辨率。
- `-o <output_format>`：指定输出视频格式。
- `<input_file>`：输入的图像文件。
- `<output_file>`：输出的视频文件。

执行上述命令后，输入的图像文件 `<input_file>` 将被编码为指定格式的视频文件 `<output_file>`。

除了基本用法，`mvx_encoder` 还支持调整编码质量、设置比特率、指定编码帧率等高级功能。使用以下命令可查看完整的参数列表：

```bash
mvx_encoder -help
```

#### 查找VPU设备

在使用VPU进行视频处理之前，需要先查找摄像头设备和VPU设备。可以使用以下命令列出所有视频设备：

```bash
v4l2-ctl --list-devices
```

示例输出：

```bash
Linlon Video device (platform:mvx):
    /dev/video0

vvcam-isp-subdev.0 (platform:vvcam-isp-subdev.0):
    /dev/v4l-subdev0

verisilicon_media (platform:vvcam-video.0):
    /dev/media0

vvcam-video.0.0 (platform:vvcam-video.0.0):
    /dev/video1

vvcam-video.0.1 (platform:vvcam-video.0.1):
    /dev/video2

vvcam-video.0.2 (platform:vvcam-video.0.2):
    /dev/video3

vvcam-video.0.3 (platform:vvcam-video.0.3):
    /dev/video4
```

在上述输出中：

- `/dev/video0` 为编解码器设备。
- `/dev/video1` 为摄像头设备。

通过这些信息，您可以确定要使用的设备路径，以便在后续步骤中进行视频捕获和编码操作。

通过以下命令验证摄像头是否正常工作（需要通过HDMI接口外接显示器）：

```bash
v4l2-drm -d 1 -w 480 -h 320
```

如果显示器上可以看到摄像头的实时画面，则说明摄像头工作正常。

#### 使用摄像头采集画面并进行编码

首先，我们将使用摄像头采集画面并保存为NV12格式的图像。接着，通过VPU对这些图像进行编码。请确保有足够的存储空间来保存图像，建议通过NFS挂载外部存储设备。

##### 视频采集

使用以下命令捕获摄像头画面并保存为NV12格式的图像，分辨率为1080p，捕获25帧图像。
请确保数据写入速度快于摄像头的采集速度，否则请降低摄像头的分辨率。

```bash
v4l2-ctl --device=/dev/video1 --set-fmt-video=width=1920,height=1080,pixelformat=NV12 --stream-mmap --stream-count=25 --stream-to=output.yuv
```

其中：

- `--device=/dev/video1`：指定摄像头设备，可以根据实际情况调整。
- `--set-fmt-video=width=1920,height=1080,pixelformat=NV12`：设置视频格式为1080p分辨率和NV12像素格式。
- `--stream-mmap`：使用内存映射方式进行视频流处理。
- `--stream-count=25`：指定捕获25帧图像。
- `--stream-to=output.yuv`：将捕获的图像保存到`output.yuv`文件中。

##### 视频编码

使用以下命令将捕获的NV12格式图像通过VPU进行编码为H.264格式的视频文件：

```bash
mvx_encoder --dev /dev/video0 -i yuv420_nv12 -w 1920 -h 1080 -o h264 ./output.yuv ./test.264
#mvx_encoder --dev /dev/video0 -i yuv420_nv12 -w 1920 -h 1080 -o h265 ./output.yuv ./test.265
#mvx_encoder --dev /dev/video0 -i yuv420_nv12 -w 1920 -h 1080 -o jpeg ./output.yuv ./test.jpg
```

其中：

- `--dev /dev/video0`：指定VPU设备。
- `-i yuv420_nv12`：指定输入图像格式为NV12。
- `-w 1920 -h 1080`：设置图像分辨率为1920x1080。
- `-o h264`：指定输出视频格式为H.264。
- `./output.yuv`：输入的NV12格式图像文件。
- `./test.264`：输出的H.264格式视频文件。

执行上述命令后，摄像头捕获的25帧NV12格式图像将被编码为H.264格式的视频文件`test.264`。可将该文件复制到PC上，使用播放器（如PotPlayer）验证编码效果。

#### 使用本地文件进行编码

如果您有本地的NV12格式图像文件，也可以使用VPU进行编码。只需将上述命令中的输入文件路径替换为本地文件路径即可。

通过这些步骤，您可以轻松地使用VPU对NV12格式的图像进行编码，无论图像来源是摄像头还是本地文件。

### 视频解码

在本节中，我们将演示如何使用VPU（视频处理单元）对NV12格式的H.264文件进行解码。图像来源可以是视频编码章节生成的文件，也可以是您自己准备的文件。

#### 解码器demo介绍

`mvx_decoder` 是一款利用 VPU（视频处理单元）进行硬件加速的视频解码命令行工具。它支持 H.264、H.265 和 JPEG 等解码格式，通过 V4L2（Video for Linux 2）接口与硬件设备交互，实现高效的解码性能。源码位于 `k230_linux_sdk/buildroot-overlay/package/mvx_player`。

使用以下命令将视频文件解码为图像：

```bash
mvx_decoder --dev <vpu_device> -i <input_format> -o <output_format> <input_file> <output_file>
```

其中：

- `--dev <vpu_device>`：指定 VPU 设备路径。
- `-i <input_format>`：指定输入图像格式。
- `-o <output_format>`：指定输出图像格式。
- `<input_file>`：输入的视频文件。
- `<output_file>`：输出的图像文件。

执行上述命令后，输入的视频文件 `<input_file>` 将被解码为指定格式的图像文件 `<output_file>`。

除了基本用法，`mvx_decoder` 还支持调整解码参数等高级功能。使用以下命令可查看完整的参数列表：

```bash
mvx_decoder -help
```

#### 视频解码

在解码之前，请先确认VPU设备，具体参考[查找VPU设备](#查找vpu设备)章节。

使用以下命令将H.264格式的视频文件解码为NV12格式的图像文件：

```bash
mvx_decoder --dev /dev/video0 -i h264 -o yuv420_nv12 test.264 output.yuv
```

其中：

- `--dev /dev/video0`：指定VPU设备。
- `-i h264`：指定输入视频格式为H.264。
- `-o yuv420_nv12`：指定输出图像格式为NV12。
- `test.264`：输入的H.264格式视频文件。
- `output.yuv`：输出的NV12格式图像文件。

执行上述命令后，输入的H.264格式视频文件`test.264`将被解码为NV12格式的图像文件`output.yuv`。可以将该文件复制到PC上，使用支持NV12格式的播放器（如YUVView）验证解码效果。

## ALSA音频使用指南

### audio demo介绍

`audio_demo` 是一个运行在 K230 开发板上的示例程序，通过调用 ALSA（Advanced Linux Sound Architecture）API，实现音频的录制和播放功能。该示例程序不仅展示了如何在 K230 开发板上进行音频处理，还为开发者提供了使用 ALSA API 接口实现音频功能的参考代码。

#### 录制 WAV 文件

使用以下命令录制一个 WAV 格式的音频文件：

```sh
audio_demo -type 2 -filename test.wav -channels 2 -samplerate 16000
```

参数说明：

- `-type 2`：指定操作类型为录制。
- `-filename`：设置输出文件名。
- `-channels`：录制通道数，`2` 为双声道。
- `-samplerate`：设置采样率，单位为 Hz。

录制完成后，音频文件保存在当前目录下的 `test.wav` 中。

#### 播放 WAV 文件

使用以下命令播放录制的 WAV 文件：

```sh
audio_demo -type 0 -filename test.wav
```

参数说明：

- `-type 0`：指定操作类型为播放 WAV 文件。
- `-filename`：要播放的文件名。

#### 播放 MP3 文件

`audio_demo` 也支持播放 MP3 格式的音频文件：

```sh
audio_demo -type 1 -filename example.mp3
```

参数说明：

- `-type 1`：指定操作类型为播放 MP3 文件。
- `-filename`：要播放的 MP3 文件名。

#### 声音采集和播放

`audio_rec_play` 是一个用于声音采集和播放的示例程序，模拟 K230 端的语音通话场景，并通过 `audio3a` 实现声音质量增强。该程序在前 30 秒启动录音和播放本地文件（可以通过耳机接口连接外部扬声器或功放设备），在后 30 秒将录制的声音播放，以检测声音效果。

使用以下命令运行 `audio_rec_play`：

```sh
audio_rec_play
```

默认情况下，程序会播放 `/usr/bin/audio.pcm` 文件。

程序运行流程如下：

1. 前 30 秒：启动录音并播放本地文件 `/usr/bin/audio.pcm`。
1. 后 30 秒：停止播放本地文件，将前 30 秒录制的声音进行播放，以检测声音效果。

通过该示例程序，用户可以体验 K230 端的声音采集和播放功能，并验证 `audio3a` 的声音质量增强效果。

## 使用FFmpeg进行多媒体处理

在本节中，我们将演示如何使用FFmpeg调用VPU实现硬件编解码，以及如何使用FFmpeg调用ALSA接口实现音频录制和播放。

### 采集摄像头视频并编码

使用以下命令，通过FFmpeg采集摄像头视频，并调用VPU编码保存为MP4文件：

```bash
ffmpeg -f v4l2 -input_format nv12 -r 30 -s 1920x1080 -i /dev/video1 -c:v h264_v4l2m2m -b:v 4M -vsync passthrough -y test.mp4
```

其中：

- `-f v4l2`：指定视频输入格式为V4L2。
- `-input_format nv12`：指定输入图像格式为NV12。
- `-r 30`：设置帧率为30fps。
- `-s 1920x1080`：指定分辨率为1920x1080。
- `-i /dev/video1`：指定摄像头设备路径。
- `-c:v h264_v4l2m2m`：使用VPU进行H.264编码
- `-b:v 4M`：设置视频码率为4Mbps。
- `-vsync passthrough`：同步视频帧。
- `-y test.mp4`：输出文件名为`test.mp4`。

`h264_v4l2m2m/hevc_v4l2m2m/mjpeg_v4l2m2m` 是 FFmpeg 中的一个硬件加速视频编码器，利用 V4L2（Video for Linux 2）和 M2M（Memory-to-Memory）接口实现高效的视频编码。通过与硬件设备交互，提供更高的编码性能和效率。

执行上述命令后，摄像头采集的视频将被编码为H.264格式并保存为`test.mp4`文件。

### 抓拍摄像头图像

使用以下命令，通过FFmpeg采集摄像头图像，并调用VPU编码保存为JPEG文件：

```bash
ffmpeg -f v4l2 -input_format nv12 -s 1920x1080 -i /dev/video1 -vframes 10 -vf format=nv12 -c:v mjpeg_v4l2m2m -vsync passthrough -y output_%03d.jpg
```

其中：

- `-f v4l2`：指定视频输入格式为V4L2。
- `-input_format nv12`：指定输入图像格式为NV12。
- `-s 1920x1080`：指定分辨率为1920x1080。
- `-i /dev/video1`：指定摄像头设备路径。
- `-vframes 10`：设置抓拍的帧数为10帧。
- `-vf format=nv12`：设置图像格式为NV12。
- `-c:v mjpeg_v4l2m2m`：使用VPU进行JPEG编码。
- `-vsync passthrough`：同步视频帧。
- `-y output_%03d.jpg`：输出文件名格式为`output_001.jpg`、`output_002.jpg`等。

执行上述命令后，摄像头采集的图像将被编码为JPEG格式，并保存为多个文件，如`output_001.jpg`、`output_002.jpg`等。

### 抓拍摄像头图像并保存为MJPEG文件

使用以下命令，通过FFmpeg采集摄像头图像，并调用VPU编码保存为MJPEG文件：

```bash
ffmpeg -f v4l2 -input_format nv12 -s 1920x1080 -i /dev/video1 -vframes 100 -vf format=nv12 -c:v mjpeg_v4l2m2m -vsync passthrough -y output.mjpeg
```

其中：

- `-f v4l2`：指定视频输入格式为V4L2。
- `-input_format nv12`：指定输入图像格式为NV12。
- `-s 1920x1080`：指定分辨率为1920x1080。
- `-i /dev/video1`：指定摄像头设备路径。
- `-vframes 100`：设置抓拍的帧数为100帧。
- `-vf format=nv12`：设置图像格式为NV12。
- `-c:v mjpeg_v4l2m2m`：使用VPU进行MJPEG编码。
- `-vsync passthrough`：同步视频帧。
- `-y output.mjpeg`：输出文件名为`output.mjpeg`。

执行上述命令后，摄像头采集的图像将被编码为MJPEG格式，并保存为`output.mjpeg`文件。

### 解码视频并保存为图像

使用以下命令，通过FFmpeg解码H.264格式的视频文件，并保存为NV12格式的图像：

```bash
ffmpeg -c:v h264_v4l2m2m -i test.mp4 -pix_fmt nv12 -f rawvideo -vsync passthrough -y output.yuv
```

其中：

- `-c:v h264_v4l2m2m`：使用VPU进行H.264解码。
- `-i input.mp4`：指定输入的视频文件。
- `-pix_fmt nv12`：指定输出图像格式为NV12。
- `-f rawvideo`：指定输出格式为原始视频流。
- `output.yuv`：输出文件名为`output.yuv`。

执行上述命令后，输入的H.264格式视频文件`input.mp4`将被解码为NV12格式的图像文件`output.yuv`。可以将该文件复制到PC上，使用支持NV12格式的播放器（如YUVView）验证解码效果。

### 录制声音

使用以下命令，通过FFmpeg调用ALSA接口录制声音，并保存为WAV文件：

```bash
ffmpeg -f alsa -i hw:0 -t 30 -ac 2 -ar 44100 -y output.wav
```

其中：

- `-f alsa`：指定音频输入格式为ALSA。
- `-i hw:0`：指定音频输入设备，`hw:0`表示默认音频设备。
- `-t 30`：设置录制时长为30秒。
- `-ac 2`：设置录制通道数为2（立体声）。
- `-ar 44100`：设置采样率为44100Hz。
- `-y output.wav`：输出文件名为`output.wav`。

执行上述命令后，录制的声音将保存为WAV格式的音频文件`output.wav`。

### 播放声音

使用以下命令，通过FFmpeg调用ALSA接口播放录制的WAV文件：

```bash
ffmpeg -f wav -i output.wav -f alsa hw:0
```

其中：

- `-f wav`：指定音频输入格式为WAV。
- `-i output.wav`：指定输入的WAV文件。
- `-f alsa`：指定音频输出格式为ALSA。
- `hw:0`：指定音频输出设备，`hw:0`表示默认音频设备。

执行上述命令后，录制的WAV文件`output.wav`将通过ALSA接口播放。

### 调整音量

#### 调整录制音量

使用以下命令，通过FFmpeg调用ALSA接口录制声音，并调整采集音量：

```bash
ffmpeg -f alsa -i hw:0 -t 30 -ac 2 -ar 44100 -filter:a "volume=2.0" -y output.wav
```

其中：

- `-f alsa`：指定音频输入格式为ALSA。
- `-i hw:0`：指定音频输入设备，`hw:0`表示默认音频设备。
- `-t 30`：设置录制时长为30秒。
- `-ac 2`：设置录制通道数为2（立体声）。
- `-ar 44100`：设置采样率为44100Hz。
- `-filter:a "volume=2.0"`：调整采集音量，`2.0`表示音量增大一倍。
- `-y output.wav`：输出文件名为`output.wav`。

执行上述命令后，录制的声音将保存为WAV格式的音频文件`output.wav`，并且音量将增大一倍。

#### 调整播放音量

使用以下命令，通过FFmpeg调用ALSA接口播放声音，并调整播放音量：

```bash
ffmpeg -f wav -i output.wav -filter:a "volume=2.0" -f alsa hw:0
```

其中：

- `-f wav`：指定音频输入格式为WAV。
- `-i output.wav`：指定输入的WAV文件。
- `-filter:a "volume=2.0"`：调整播放音量，`2.0`表示音量增大一倍。
- `-f alsa`：指定音频输出格式为ALSA。
- `hw:0`：指定音频输出设备，`hw:0`表示默认音频设备。

执行上述命令后，WAV文件`output.wav`将通过ALSA接口播放，并且音量将增大一倍。

#### 静音

以下命令将使用 FFmpeg 调用 ALSA 播放音频文件 `output.wav`，并且静音输出，使用硬件设备 `hw:0`。

```sh
ffmpeg -i output.wav -f alsa -ac 2 -ar 44100 -vol 0 hw:0
```

其中:

- `-i output.wav`：指定输入文件为 `output.wav`。
- `-f alsa`：指定输出格式为 ALSA。
- `-ac 2`：指定音频通道数为 2。
- `-ar 44100`：指定音频采样率为 44100 Hz。
- `-vol 0`：将音量设置为 0，实现静音播放。
- `hw:0`：指定使用硬件设备 `hw:0`。

## 摄像头rtsp推流demo

`camera_rtsp_demo` 是一个示例程序，用于通过 RTSP 协议传输摄像头视频流。该程序能够将摄像头捕获的视频编码为 H.264 或 H.265 格式，并通过 RTSP 协议进行实时传输。它展示了如何使用 FFmpeg API 获取摄像头数据并进行编码，以及如何使用 live555 API 输出 RTSP 流。

### 使用方法

使用以下命令运行 `camera_rtsp_demo`：

```sh
./camera_rtsp_demo [-H] [-t <codec_type>] [-w <width>] [-h <height>] [-b <bitrate_kbps>]
```

参数说明：

- `-H`：显示帮助信息。
- `-t <codec_type>`：指定视频编码类型，可选值为 `h264` 或 `h265`，默认值为 `h264`。
- `-w <width>`：指定视频编码宽度，默认值为 `1280`。
- `-h <height>`：指定视频编码高度，默认值为 `720`。
- `-b <bitrate_kbps>`：指定视频编码比特率（kbps），默认值为 `2000`。

示例命令：

```sh
./camera_rtsp_demo -t h264 -w 1920 -h 1080 -b 4000
```

执行上述命令后，程序将启动摄像头并将视频流编码为 H.264 格式，分辨率为 1920x1080，比特率为 4000 kbps，通过 RTSP 协议进行传输。

在串口输出中找到 RTSP URL，例如："Play this stream using the URL: rtsp://<your_device_ip>:8554/test"，并使用支持 RTSP 协议的播放器（如 VLC）打开该 URL 以查看视频流。
