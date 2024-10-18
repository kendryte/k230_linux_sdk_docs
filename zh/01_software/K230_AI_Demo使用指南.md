# K230 AI Demo使用指南

## AI Demo

### 概述

AI Demo集成了人脸、人体、手部、车牌、单词续写等模块，包含了分类、检测、分割、识别、单目测距等多种功能，给客户提供如何使用K230开发基于k230_linux_sdk的AI相关应用的参考。

### 硬件环境

- `CanMV-K230-V1.x`

### 源码位置

源码路径位于`k230_linux_sdk/buildroot-overlay/package/ai_demo`，目录结构如下：

```shell
# AI Demo子目录（eg：bytetrack、face_detection等）中有详细的Demo说明文档
├── anomaly_det
├── build.sh
├── bytetrack
├── CMakeLists.txt
├── common
├── Config.in
├── crosswalk_detect
├── dynamic_gesture
├── eye_gaze
├── face_alignment
├── face_detection
├── face_emotion
├── face_gender
├── face_glasses
├── face_landmark
├── face_mask
├── face_mesh
├── face_parse
├── face_pose
├── face_verification
├── falldown_detect
├── finger_guessing
├── fitness
├── head_detection
├── helmet_detect
├── licence_det
├── licence_det_rec
├── llamac
├── object_detect_yolov8n
├── person_attr
├── person_detect
├── person_distance
├── pose_detect
├── pphumanseg
├── puzzle_game
├── segment_yolov8n
├── shell
├── smoke_detect
├── space_resize
├── sq_hand_det
├── sq_handkp_class
├── sq_handkp_det
├── sq_handkp_flower
├── sq_handkp_ocr
├── sq_handreco
├── traffic_light_detect
├── vehicle_attr
├── virtual_keyboard
└── yolop_lane_seg
```

### 编译及运行程序

（1）docker环境获取

获取docker编译镜像，推荐在docker环境中编译K230 Linux SDK，可直接使用如下docker镜像：

```shell
docker pull ghcr.io/kendryte/k230_sdk
```

可使用如下命令确认docker镜像拉取成功：

```shell
docker images | grep k230_sdk
```

如下载速度较慢或无法成功，可使用`tools/docker/Dockerfile`自行编译docker image。

```shell
#先下载k230_linux_sdk，然后在k230_linux_sdk目录执行以下操作
docker build -f tools/docker/Dockerfile -t k230_docker tools/docker
```

（2）从`https://www.xrvm.cn/community/download?id=4333581795569242112`下载Xuantie-900-gcc-linux-6.6.0-glibc-x86_64-V2.10.1-20240712.tar.gz，然后解压到/opt/toolchain（其它目录也行，docker run时指定相应目录即可）。

```shell
#参考命令，若是已经之前已经执行，请忽略
mkdir -p /opt/toolchain;
tar -zxvf Xuantie-900-gcc-linux-6.6.0-glibc-x86_64-V2.10.1-20240712.tar.gz -C /opt/toolchain;
```

（3）运行docker

```shell
#参考命令
docker run -it --rm -v /etc/passwd:/etc/passwd -v /opt/toolchain/Xuantie-900-gcc-linux-6.6.0-glibc-x86_64-V2.10.1:/opt/toolchain/Xuantie-900-gcc-linux-6.6.0-glibc-x86_64-V2.10.1 -v $PWD:/work/k230_linux_sdk -u $UID ghcr.io/kendryte/k230_sdk
```

（4）编译依赖

```shell
#参考命令
cd /work/k230_linux_sdk
#以下命令{二选一}
#选择一（快速，只为编译ai demo提供基础依赖）：选择不编译整个镜像
make CONF=k230_canmv_defconfig face_detect
#选择二（慢，可以手动编译出sysimage-sdcard.img.gz）：选择编译整个镜像
make CONF=k230_canmv_defconfig
```

注：

a.若是make时报错，退出docker后，删除k230_linux_sdk，重新下载k230_linux_sdk，并重新执行（3）、（4）即可，之后会优化该问题。

b.手动构建的sysimage-sdcard.img.gz，/app默认挂载是256M，若是256M不够用，可以通过修改k230_linux_sdk/buildroot-overlay/configs/k230_canmv_defconfig 下面的 BR2_TARGET_ROOTFS_EXT2_SIZE，然后重新 make CONF=k230_canmv_defconfig

```shell
#修改为2G
BR2_TARGET_ROOTFS_EXT2_SIZE="2048M"
```

（5）编译单个ai demo

```shell
cd buildroot-overlay/package/ai_demo
#编译单个ai_demo（以人脸检测为例）
./build.sh face_detection
```

编译产物：

```bash
k230_bin/
├── face_detection
│   ├── 1024x624.jpg
│   ├── face_detect_image.sh
│   ├── face_detection_320.kmodel
│   ├── face_detection_640.kmodel
│   ├── face_detection.elf
│   └── face_detect_isp.sh
```

将k230_bin/整个文件夹拷贝到板子，在板子上执行sh脚本即可运行相应AI demo

```shell
#进入开发板/app目录
scp -r username@ip:/xxx/k230_linux_sdk/buildroot-overlay/package/ai_demo/k230_bin .

#执行相应脚本即可运行人脸检测
#详细人脸检测说明可以参考k230_linux_sdk/buildroot-overlay/package/ai_demo/face_detection/README.md
./face_detect_isp.sh
```

（6）（可选）编译所有AI Demo（若只需编译某个demo，无需执行该步骤）

```shell
cd buildroot-overlay/package/ai_demo
./build.sh
```

生成以下文件：

```bash
k230_bin/
......
├── face_detection
│   ├── 1024x624.jpg
│   ├── face_detect_image.sh
│   ├── face_detection_320.kmodel
│   ├── face_detection_640.kmodel
│   ├── face_detection.elf
│   └── face_detect_isp.sh
......
└── llamac
    ├── llama.bin
    ├── llama_build.sh
    ├── llama_run
    └── tokenizer.bin
......
```
