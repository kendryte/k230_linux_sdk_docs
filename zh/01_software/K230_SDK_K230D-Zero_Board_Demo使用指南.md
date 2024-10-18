# K230 SDK K230D Zero Board Demo使用指南

## 1. 概述

## 2. Demo介绍

### 2.1 LVGL

源码路径在 `buildroot-overlay/package/lvgl`，使用的 LVGL 版本为 8.3.7，编译后产生名为 `lvgl_demo_music` 的可执行程序放置在 `output/k230_canmv_defconfig/target/usr/bin/lvgl_demo_music`，在板子上可以直接输入 `lvgl_demo_music` 执行

![LVGL](https://developer.canaan-creative.com/api/post/attachment?id=424)

### 2.2 GPU

源码路径在 `buildroot-overlay/package/vg_lite`，包含 5 个示例程序

- tiger: 渲染一张 640x480 的老虎图片并保存为 tiger.png ![tiger](https://developer.canaan-creative.com/api/post/attachment?id=422)
- linearGrad: 渲染一张渐变图案并保存为 linearGrad.png ![linearGrad](https://developer.canaan-creative.com/api/post/attachment?id=423)
- imgIndex: 渲染四张使用颜色查找表的图像并保存为 png 文件
- vglite_drm: 在屏幕上显示使用 GPU 绘制的图案
- vglite_cube: 在屏幕上显示使用 GPU 绘制的一个正方体边框

### 2.3 人脸检测

人脸检测demo输入源为RGB planner的图片。此demo仅用于演示KPU、nncase有关AI方面的功能。

源码位置`buildroot-overlay\package\face_detect`，可执行程序放置在`output/k230_canmv_defconfig/target/app/face_detect`，在板子上进入 `/app/face_detct`，执行 run.sh即可。会打印识别的人脸及五点信息。

```shell
[root@canaan /app/face_detect ]#./run.sh
case ./face_detect.elf built at Aug  5 2024 11:07:25
output tensor idx: 0
output tensor idx: 1
output tensor idx: 2
output tensor idx: 3
output tensor idx: 4
output tensor idx: 5
output tensor idx: 6
output tensor idx: 7
output tensor idx: 8
Detection results for image: ai2d_input.bin
Number of faces detected: 19
Face 1:
  Bounding box: (596, 215) to (652, 286)
  Landmarks:
    Point 1: (613, 241)
    Point 2: (639, 241)
    Point 3: (627, 254)
    Point 4: (616, 267)
    Point 5: (638, 266)
...
```
