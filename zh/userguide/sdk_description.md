# sdk构建说明

本sdk基于2025.02版本的buildroot进行构建，

## `k230_linux_sdk`目录结构

```shell
k230_linux_sdk/
├── buildroot-overlay  #buildroot 有修改的文件，会用这个目录覆盖原始的buildroot目录。
│   ├── board
│   │   └── canaan  #嘉楠k230相关板子的私有脚本 配置文件等
│   ├── boot
│   │   ├── opensbi  #opensbi有修改的文件
│   │   └── uboot  #uboot有修改的文件
│   ├── configs
│   │   ├── k230d_canmv_defconfig  #k230d canmv板子配置文件
│   │   ├── k230_canmv_defconfig  #k230 canmv板子配置文件
│   │   ├── k230_canmv_v3_defconfig  #k230 canmv v3 板子配置文件
│   │   ├── k230d_canmv_01studio_defconfig  #k230d 01studio canmv板子配置文件
│   │   ├── k230_canmv_lckfb_defconfig  #k230 canmv 庐山派板子配置文件
│   │   ├── k230_canmv_dongshanpi_defconfig  #k230 canmv 东山派板子配置文件
│   │   ├── BPI-CanMV-K230D-Zero_defconfig  #BPI-CanMV-K230D-Zero 板子配置文件
│   │   └── ... # 其他板子配置文件
│   └── package
│       ├── ai_demo  #ai_demo 提供了丰富的ai应用
│       ├── ai2d_kpu  #ai2d_kpu 提供了kpu相关的应用
│       ├── audio_demo  #audio_demo 提供了音频播放录音等应用
│       ├── audio_play_rec  #audio_play_rec 提供了音频播放录音等应用
│       ├── camera_rtsp_demo  #camera_rtsp_demo 提供了rtsp视频流播放等应用
│       ├── face_detect  #face_detect 提供了人脸检测的示例应用
│       ├── display  #display 提供了显示相关的应用
│       ├── k230_assistant  #k230_assistant k230的webrtc语音助手应用
│       ├── cloudplat_deploy_code_linux  #cloudplat_deploy_code_linux 云平台部署代码
│       ├── usage_ai2d  #usage_ai2d 提供了ai2d的使用示例
│       ├── yolo  #yolo 提供了yolo模型部署代码
│       ├── libdrm  #libdrm有修改的文件
│       ├── lvgl  #lvgl有修改的文件
│       ├── vg_lite
│       └── vvcam
├── docs  #文档目录
├── output   #输出目录，包含最终使用的源码，及所有的输出文件
│   ├── buildroot-2024.02.1  #最后使用的buildroot目录
│   └── k230d_canmv_defconfig  #编译输出目录，所有源代及编译输出文件
├── Makefile  #主makefile文件
├── README.md  #readme文件
└── tools  #一些脚本工具
```

## sdk编译过程概述

>本节以make CONF=k230d_canmv_defconfig 命令执行过程为例。

1、从buildroot官网下载buildroot-2025.02.1.gz压缩包，并解压缩为output/buildroot-2025.02.1/

2、用buildroot-overlay目录覆盖output/buildroot-2025.02.1/目录

```shell
rsync -a  buildroot-overlay/ output/buildroot-2025.02.1/
```

3、进入output/buildroot-2025.02.1/目录，使用k230d_canmv_defconfig配置buildroot，并指定输出目录为output/k230d_canmv_defconfig

```bash
make -C output/buildroot-2025.02.1 k230d_canmv_defconfig O=/home/wangjianxin/k230_linux_sdk/output/k230d_canmv_defconfig
```

4、 进入output/k230d_canmv_defconfig 目录并进行编译

```shell
make -C /home/wangjianxin/k230_linux_sdk/output/k230d_canmv_defconfig all
```

>更多编译说明请参考<https://buildroot.org/downloads/manual/manual.html>
