# K230 SDK K230D Zero Board Demo使用指南

## 概述

## Demo介绍

### LVGL

源码路径在 `buildroot-overlay/package/lvgl`，使用的 LVGL 版本为 8.3.7，编译后产生名为 `lvgl_demo_music` 的可执行程序放置在 `output/k230_canmv_defconfig/target/usr/bin/lvgl_demo_music`，在板子上可以直接输入 `lvgl_demo_music` 执行

![LVGL](https://www.kendryte.com/api/post/attachment?id=424)

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

人脸检测demo输入源为sesnor的输入图像。此demo用于演示isp + ai 整个通路的demo。

源码位置`buildroot-overlay\package\face_detect`，可执行程序放置在`output/k230_canmv_defconfig/target/app/face_detect`，在板子上进入 `/app/face_detct`，执行下边命令：

```shell
./face_detect.elf face_detection_320.kmodel
```

显示效果如下：

![linearGrad](https://www.kendryte.com/api/post/attachment?id=503)
