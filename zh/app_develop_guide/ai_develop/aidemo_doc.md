# K230 AI Demo使用指南

## AI Demo

### 概述

K230 AI Demo集成了人脸、人体、手部、车牌等应用，包含了分类、检测、分割、识别、跟踪、单目测距等多种功能，给客户提供如何使用K230开发AI相关应用的参考。上述应用用于验证K230的能力，丰富应用场景，实际应用场景需要有针对性的进行优化，以达到更好的效果。参考优化方向包括调整阈值、代码优化、量化优化、模型优化、训练数据优化等方向。

## 支持开发板

- CanMV-K230-V1.1 / CanMV-K230-V3.0 / 01Studio CanMV K230/ Bpi-CanMV-K230D-Zero/ lckfb-K230 / dongshanpi-k230

## 源码说明

### 文件树

源码路径位于`k230_linux_sdk/buildroot-overlay/package/ai_demo`，目录结构如下：

```shell
# AI Demo子目录（eg：bytetrack、face_detection等）中有详细的Demo说明文档
.
├── anomaly_det
├── bytetrack
├── common
├── crosswalk_detect
├── demo_mix
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
├── ocr
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
├── yolop_lane_seg
├── CMakeLists.txt
├── ai_demo.mk
├── build.sh
└── Config.in
```

其中`common_files`目录下的文件是所有Demo共有的文件，目录下的文件结构如下：

```shell
.
├── ai_base.cc        # 模型推理封装类实现，封装了nncase的基本操作，包括kmodel加载，设置输入，获取输出，后续应用开发只需关注模型前后处理
├── ai_base.h         # 模型推理封装类头文件，定义了模型推理的基本接口
├── utils.cc          # 工具方法和工具类，提供获取颜色盘、保存图片、不同预处理方法的实现
├── utils.h           # 工具方法和工具类头文件，定义了工具方法和工具类的接口
├── scoped_timing.hpp # 时间测量类，用于测量代码执行时间
├── setting.h         # 配置头文件，主要实现设置AI推理出图分辨率
├── sensor_buf_manager.cc # 摄像头缓冲获取数据管理实现方法，可以从中获取推理使用的tensor
├── sensor_buf_manager.h  # 摄像头缓冲获取数据管理头文件
├── ai_demo_cml_common  # 当使用buildroot编译时，所有aidemo的共用编译设置
├── ai_demo_mk_common   # 当使用buildroot编译时，所有aidemo特有编译配置的模板，和应用目录名称相关
├── ai_demo_commonConfig.cmake.in # CMake包配置文件，ai_demo_common库编译安装后，使得其他应用可以通过find_package找到该库
├── CMakeLists.txt    # ai_demo_common编译配置文件，ai_demo_common部分被编译成独立的库给其他aidemo使用，是编译其他ai_demo的依赖
├── common.mk         # common部分buildroot自定义构建片段，实现自动下载（或本地同步）模型包、设置依赖关系，并通过 CMake 打包/安装
└── Config.in         # Buildroot 的包配置项
```

kmodel及相关依赖路径位于会在编译的时候自动下载到当前目录，提供ai_demo运行所必须的kmodel、测试图片以及其他必要文件。在ai_demo编译过程中，会由`build.sh`脚本按照demo名称自动拷贝到产物目录下。

### Demo 说明

| Demo 子目录           | 场景                     |      说明                  |链接|
| :-------------------- | ------------------------ |--------------------------- |---|
| anomaly_det           | 异常检测                 | 异常检测示例提供的模型使用patchcore异常检测方法训练得到，能够从输入图片中辨别出玻璃瓶口是否存在异常。异常检测通常会被应用在工业图像检测、医疗图像分析、安防监控等领域。                            |[anomaly_det](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/anomaly_det)|
| bytetrack             | 多目标跟踪               | ByteTrack多目标追踪示例使用YOLOv5作为目标检测算法，应用卡尔曼滤波算法进行边界框预测，应用匈牙利算法进行目标和轨迹间的匹配。  |[bytetrack](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/bytetrack)|
| crosswalk_detect      | 人行横道检测              | 人行横道检测使用YOLOV5网络，该应用对图片或视频中的人行横道进行检测，可用于辅助驾驶等场景。                        |[crosswalk_detect](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/crosswalk_detect)|
| demo_mix  | 示例集锦                 | 示例集锦综合了k230中的人手关键点检测、手势识别、动态手势识别、人脸姿态估计、目标跟踪等示例，实现手势控制应用切换。当出示“1”手势的时候进入动态手势识别，出示“2”手势时进图人人脸姿态估计，出示“3”手势的时候进入人脸自动跟踪。出示“love”手势时退出当前任务，进入切换状态。 | [demo_mix](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/demo_mix)|
| dynamic_gesture       | 视觉动态手势识别            | 视觉动态手势识别可以对上下左右摆手和五指捏合五个动作进行识别，用于隔空操作控制场景。 手掌检测采用了yolov5网络结构，backbone选取了1.0-mobilenetV2，手掌关键点检测采用了resnet50网络结构,动态手势识别采用了tsm结构，backbone选取了mobilenetV2。                            | [dynamic_gesture](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/dynamic_gesture)|
| eye_gaze              | 注视估计                 |   注视估计示例根据人脸预测人正在看哪里，对视频帧或图片，先进行人脸检测，然后对每个人脸进行注视估计，预测出注视向量，并以箭头的方式显示到屏幕上。该应用采用retina-face网络实现人脸检测，使用L2CS-Net实现注视估计。注视估计可以应用到汽车安全领域。                          | [eye_gaze](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/eye_gaze)|
| face_alignment        | 人脸对齐                 | 人脸对齐示例可得到图像或视频中的每个人脸的深度图（depth）或归一化投影坐标编码图。人脸检测采用了retina-face网络结构，backbone选取0.25-mobilenet，人脸对齐网络基于3DDFA(3D Dense Face Alignment)实现。            | [face_alignment](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/face_alignment)|
| face_detection        | 人脸检测                 |  人脸检测实例可得到图像或视频中的每个人脸检测框以及每个人脸的左眼球/右眼球/鼻尖/左嘴角/右嘴角五个关键点位置。人脸检测采用了retina-face网络结构，backbone选取0.25-mobilenet。                           | [face_detection](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/face_detection)|
| face_emotion          | 面部表情识别              | 面部表情识别使用两个模型实现图像/视频中每个人的表情识别的功能，可识别的表情类别包括Neutral、Happiness、Sadness、Anger、Disgust、Fear、Surprise。人脸检测使用retina-face网络结构；表情分类选用mobilenet为backbone进行分类，得到人物表情。                            | [face_emotion](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/face_emotion)|
| face_gender           | 性别分类                 | 人脸性别分类示例使用两个模型实现判断图像/视频中每个人的性别的功能，每个人物性别用M或F表示，其中M表示男性（Male），F表示女性（Female）。 人脸检测使用retina-face网络结构；性别分类选用EfficientNetB3为backbone进行分类，得到人物性别。                           | [face_gender](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/face_gender)|
| face_glasses          | 是否佩戴眼镜分类         | 是否佩戴眼镜分类示例使用两个模型实现判断图像/视频每个人是否佩戴眼镜。 人脸检测检测模型使用retina-face网络结构；人脸眼镜分类模型选用SqueezeNet-1.1为backbone，用于对每个人脸框判断眼镜佩戴情况。                           | [face_glasses](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/face_glasses)|
| face_landmark         | 人脸密集关键点            | 人脸密集关键点检测应用使用两个模型实现检测图像/视频中每张人脸的106关键点，并根据106关键点绘制人脸、五官等轮廓，不同轮廓使用不用的颜色表示。人脸检测使用retina-face网络结构；密集关键点检测选用0.5-mobilenet为backbone，用于对每张人脸检测106个关键点，106关键点包括人脸的脸颊、嘴巴、眼睛、鼻子和眉毛区域。                            | [face_landmark](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/face_landmark)|
| face_mask             | 是否佩戴口罩分类          | 是否佩戴口罩分类应用使用两个模型实现判断图像/视频每个人是否佩戴口罩。在需要佩戴口罩的应用场景中，若发现有人没有佩戴口罩，可进行相关提醒。人脸检测检测模型使用retina-face网络结构；人脸口罩分类模型使用mobilenet-v2为backbone，用于对每个人脸框判断口罩佩戴情况。                            | [face_mask](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/face_mask)|
| face_mesh             | 3D人脸网格              |  3D人脸网格可得到图像或视频中的每个人脸的三维网格结构。人脸检测采用了retina-face网络结构，backbone选取0.25-mobilenet，人脸对齐网络基于3DDFA(3D Dense Face Alignment)实现。| [face_mesh](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/face_mesh)|
| face_parse            | 人脸分割                  | 人脸分割示例使用两个模型实现对图像/视频中每个人脸的分割功能，人脸分割包含对人脸眼睛、鼻子、嘴巴等部位按照像素进行区分，不同的区域用不同的颜色表示。 人脸检测采用了retina-face网络结构，人脸部位分割使用DeepNetV3网络结构，backbone使用mobilenet-1.0。                           | [face_parse](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/face_parse)|
| face_pose             | 人脸姿态估计             | 人脸姿态估计使用两个模型实现对图像/视频中每个人的脸部朝向的角度进行估计的功能。人脸朝向用一般用欧拉角（roll/yaw/pitch）表示，其中roll代表了人脸左右摇头的程度；yaw代表了人脸左右旋转的程度；pitch代表了人脸低头抬头的程度。人脸检测采用了retina-face模型，人脸朝向估计98个2D关键点拟合。                            | [face_pose](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/face_pose)|
| face_verification     | 人脸身份验证             | 人脸身份验证是一种基于人脸生物特征的身份验证技术，旨在确认个体是否是其所声称的身份。该技术通过分析和比对用户的脸部特征来验证其身份，通常是在人脸验证系统通过对比两张图片，确定两张图像中的人脸是否属于同一个人。 人脸检测采用了retina-face模型，人脸朝特征化使用ResNet50,输出512维特征。                           | [face_verification](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/face_verification)|
| falldown_detect       | 跌倒检测                 |  跌倒检测可以对图片或视频中的人的跌倒状态进行检测。该示例使用yolov5n模型实现。                           | [falldown_detect](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/falldown_detect)|
| finger_guessing       | 猜拳游戏                 |  猜拳游戏示例通过手部手势识别区分石头鸡剪刀布，包括手掌检测和手部21关键点识别两个模型，通过21个关键点的位置约束确定手势类别。手掌检测部分采用了yolov5网络结构，backbone选取了1.0-mobilenetV2，手掌关键点检测部分采用了resnet50网络结构。                          | [finger_guessing](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/finger_guessing)|
| fitness               | 蹲起动作计数             |  蹲起动作计数示例实现视频中人的蹲起动作计数功能，适用于健身状态检测等场景。使用yolov8n-pose模型实现。                           | [fitness](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/fitness)|
| head_detection        | 人头检测计数             |  人头检测计数示例实现了获取图片或视频中出现的人头的坐标和数量的功能。使用yolov8模型实现。                           | [head_detection](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/head_detection)|
| helmet_detect         | 安全帽检测               | 安全帽检测实例实现了对图片或视频中出现的人是否佩戴安全帽进行检测，适用于建筑制造业的安全预防场景。使用yolov5模型实现。                            | [helmet_detect](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/helmet_detect)|
| kws                   | 关键词唤醒               |关键词唤醒通过音频识别模型检测音频流中是否包含训练时设定的关键词，如果检测到对应的关键词，给出语音响应。本示例提供的模型为WeNet训练得到，正负样本分别采用在k230开发板上采集的“xiaonan”音频和开源数据集speech_commands。                             | [kws](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/kws)|
| licence_det           | 车牌检测                 | 车牌检测可以检测图像或视频中的出现的车牌。 车牌检测采用了retinanet网络结构。                          | [licence_det](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/licence_det)|
| licence_det_rec       | 车牌识别                 | 车牌识别可以识别图图像或视频中出现的车牌的位置以及牌照信息。车牌检测采用了retinanet网络结构，车牌识别采用了以MobileNetV3为backbone的RLNet网络结构。                            | [licence_det_rec](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/licence_det_rec)|
| object_detect_yolov8n | YOLOV8多目标检测         | YOLOv8多目标检测检测示例实现COCO数据集80类别检测。使用yolov8n模型。                            | [object_detect_yolov8n](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/object_detect_yolov8n)|
| ocr                   | ocr检测+识别             | OCR识别示例可检测到图像或视频中的文本位置以及相应的文字内容。OCR识别任务采用了CRNN网络结构，OCR检测任务采用了DBnet的网络结构。                           | [ocr](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/ocr)|
| person_attr           | 人体属性                 | 人体属性检测可以识别图片或视频中的人体位置坐标，性别、年龄、是否佩戴眼镜、是否持物。人体检测使用YOLOv5模型实现，人体属性使用PULC人模型实现。                            | [person_attr](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/person_attr)|
| person_detect         | 人体检测                 |  人体检测可以检测图片或视频中的人体位置坐标信息，并用检测框标记出来。本示例使用yolov5模型实现。                           | [person_detect](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/person_detect)|
| person_distance       | 行人测距                 |  行人测距是先通过行人检测检测行人，再通过检测框在图像中的大小去估算目标距离。其中行人检测采用了yolov5n的网络结构。使用该应用，可得到图像或视频中的每个行人的检测框以及估算的距离。该技术可应用在车辆辅助驾驶系统、智能交通等领域。该应用需要根据摄像头调整计算数据，现有示例可能识别不准。                   | [person_distance](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/person_distance)|
| pose_detect           | 人体关键点检测           |  人体关键点检测模型的输出是一组代表图像或视频中人体对象上的关键点（17个），以及每个点的置信度得分，并使用不同颜色的线将关键点连接成人体的形状。本示例使用yolov8n-pose模型实现。                           | [pose_detect](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/pose_detect)|
| pphumanseg            | 人像分割                 | 人像分割指对图片或视频中的人体轮廓范围进行识别，将其与背景进行分离，返回分割后的二值图、灰度图、前景人像图等，实现背景图像的替换与合成。 可应用于人像抠图、照片合成、人像特效、背景特效等场景，大大提升图片和视频工具效率。本示例使用pphumanseg模型实现。                            | [pphumanseg](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/pphumanseg)|
| puzzle_game           | 拼图游戏                 | 拼图游戏可得到图像或视频中的每个手掌的21个骨骼关键点位置。并且可以实现拼图游戏的功能，张开拇指和中指，将其中点放到空格旁边的非空格，拟合两指，当前非空格会移动到空格内。 示例中手掌检测采用了yolov5网络结构，backbone选取了1.0-mobilenetV2，手掌关键点检测采用了resnet50网络结构。                           | [puzzle_game](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/puzzle_game)|
| segment_yolov8n       | YOLOV8多目标分割         | YOLOv8多目标分割检测示例实现COCO数据集80类别分割掩码。使用yolov8n-seg模型。                            | [segment_yolov8n](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/segment_yolov8n)|
| smoke_detect          | 吸烟检测                 |  吸烟检测对图片或视频中存在的吸烟行为进行实时监测识别。该示例使用yolov5模型实现。                           | [smoke_detect](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/smoke_detect)|
| space_resize          | 手势隔空缩放             | 手势隔空缩放可得到图像或视频中的每个手掌的21个骨骼关键点位置，并且我们通过拇指中指来实现隔空缩放图像。手掌检测采用了yolov5网络结构，backbone选取了1.0-mobilenetV2，手掌关键点检测采用了resnet50网络结构。                            | [space_resize](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/space_resize)|
| sq_hand_det           | 手掌检测                 |  手掌检测可获取图像或视频中的每个手掌的检测框。手掌检测采用了yolov5网络结构，backbone选取了1.0-mobilenetV2。                           | [sq_hand_det](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/sq_hand_det)|
| sq_handkp_class       | 手掌关键点手势分类       |   手掌关键点手势分类可得到图像或视频中的每个手掌的21个骨骼关键点位置,并根据关键点的位置二维约束获得静态手势。共支持握拳，五指张开，一手势，yeah手势，三手势，八手势，六手势，点赞，拇指食指小拇指张开共9种手势。本示例中手掌检测采用了yolov5网络结构，backbone选取了1.0-mobilenetV2，手掌关键点检测采用了resnet50网络结构。                          | [sq_handkp_class](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/sq_handkp_class)|
| sq_handkp_det         | 手掌关键点检测           | 手掌关键点检测示例可得到图像或视频中的每个手掌的21个骨骼关键点位置。手掌检测采用了yolov5网络结构，backbone选取了1.0-mobilenetV2，手掌关键点检测采用了resnet50网络结构。                           | [sq_handkp_det](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/sq_handkp_det)|
| sq_handkp_flower      | 指尖区域花卉分类         | 指尖区域花卉识别可得到图像或视频中的两个手掌的食指指尖包围区域内的花卉类别。可支持102种花卉的种类识别。本示例手掌检测采用了yolov5网络结构，backbone选取了1.0-mobilenetV2，手掌关键点检测采用了resnet50网络结构。花朵分类backbone选取了1.0-mobilenetV2。                            | [sq_handkp_flower](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/sq_handkp_flower)|
| sq_handkp_ocr         | 手指区域OCR识别          | 手指区域OCR识别可得到图像或视频中的每个手掌的食指左上区域范围内识别到的文字。手掌检测采用了yolov5网络结构，backbone选取了1.0-mobilenetV2，手掌关键点检测采用了resnet50网络结构。文字检测采用了retinanet网络结构，文字识别采用了以MobileNetV3为backbone的RLnet网络结构。                            | [sq_handkp_ocr](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/sq_handkp_ocr)|
| sq_handreco           | 手势识别                 | 手势识别可得到图像或视频中的每个手势的类别。仅支持五指张开、八手势、  yeah手势三种。 本示例中手掌检测采用了yolov5网络结构，backbone选取了1.0-mobilenetV2，手势识别backbone选取了1.0-mobilenetV2。                        | [sq_handreco](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/sq_handreco)|
| traffic_light_detect  | 交通信号灯检测           | 可检测到图像或视频中的交红绿黄信号灯。本示例使用yolov5模型实现。                            | [traffic_light_detect](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/traffic_light_detect)|
| tts_zh                | 中文转语音               | 中文文字转语音（text to chinese speech, tts_zh）使用三个模型实现。用户默认输入三次文字，生成文字对应的wav文件。 本示例将FastSpeech2模型拆分成两个模型，Encoder+Variance Adaptor为fastspeech1，Decoder为fastspeech2，声码器选择hifigan。持续时间特征在fastspeech1之后添加。                       | [tts_zh](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/tts_zh)|
| vehicle_attr          | 车辆属性识别             | 车辆属性识别可以识别图像或视频中每个车辆，并返回该车辆的位置坐标、车型、车身颜色。本示例采用了yolov5网络结构实现了车辆检测，车辆属性检测使用PULC模型。                         | [vehicle_attr](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/vehicle_attr)|
| virtual_keyboard      | 隔空虚拟键盘             | 隔空虚拟键盘可以使用屏幕上的虚拟键盘输出字符。拇指和食指捏合是输入动作。本示例中手掌检测采用了yolov5网络结构，backbone选取了1.0-mobilenetV2，手掌关键点检测采用了resnet50网络结构。                          | [virtual_keyboard](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/virtual_keyboard)|
| yolop_lane_seg        | 路面车道线分割           | 路面车道线分割可在图像或视频中实现路面分割，即检测到车道线和可行驶区域，并加以颜色区分。本示例使用yolop模型实现。         | [yolop_lane_seg](https://github.com/kendryte/k230_linux_sdk/tree/dev/buildroot-overlay/package/ai_demo/yolop_lane_seg)|

## 编译及运行程序

### 编译环境搭建

如果已经编译好固件，或者选择不使用自行编译的固件，可以跳过此步骤。

- **下载sdk源码**

参考如下命令下载sdk代码

```bash
git clone git@github.com:kendryte/k230_linux_sdk.git
# git clone git@gitee.com:kendryte/k230_linux_sdk.git
cd k230_linux_sdk
```

>github上仓库地址是 <https://github.com/kendryte/k230_linux_sdk.git>
>
>gitee上仓库地址是 <https://gitee.com/kendryte/k230_linux_sdk.git>

- **安装交叉工具链**

下载Xuantie-900-gcc-linux-6.6.0-glibc-x86_64-V3.0.2.tar.gz 文件（下载地址1：<https://www.xrvm.cn/community/download?id=4433353576298909696> ，下载地址2：<https://kendryte-download.canaan-creative.com/k230/downloads/dl/gcc/Xuantie-900-gcc-linux-6.6.0-glibc-x86_64-V3.0.2-20250410.tar.gz>），并解压缩到/opt/toolchain目录 ，参考命令如下:

```bash
mkdir -p /opt/toolchain;
tar -zxvf Xuantie-900-gcc-linux-6.6.0-glibc-x86_64-V3.0.2.tar.gz -C /opt/toolchain;
```

> 安装新32位交叉工具链（下载地址：<https://github.com/ruyisdk/riscv-gnu-toolchain-rv64ilp32/releases/download/2024.06.25/riscv64ilp32-elf-ubuntu-22.04-gcc-nightly-2024.06.25-nightly.tar.gz>）(可选, 只有k230d_canmv_ilp32_defconfig配置需要)，参考命令如下：
>
> wget -c <https://github.com/ruyisdk/riscv-gnu-toolchain-rv64ilp32/releases/download/2024.06.25/riscv64ilp32-elf-ubuntu-22.04-gcc-nightly-2024.06.25-nightly.tar.gz> ;
>
> mkdir -p  /opt/toolchain/riscv64ilp32-elf-ubuntu-22.04-gcc-nightly-2024.06.25/ ;
>
> tar -xvf riscv64ilp32-elf-ubuntu-22.04-gcc-nightly-2024.06.25-nightly.tar.gz -C  /opt/toolchain/riscv64ilp32-elf-ubuntu-22.04-gcc-nightly-2024.06.25/

- **安装依赖**

需要安装如下软件的 ubuntu22.04 或者ubuntu 24.04系统(参考安装命令)

```bash
sudo apt-get install -y wget git sed make binutils build-essential diffutils gcc  g++ bash patch gzip bzip2 perl tar cpio unzip rsync file bc findutils wget libncurses-dev python3 libssl-dev  gawk cmake bison flex bash-completion  parted curl xz-utils
```

>依赖软件包见tools/docker/Dockerfile 文件，构建和进入docker环境参考如下命令：
>
>docker  build   -f tools/docker/Dockerfile  -t wjx/d tools/docker  #构建
>
>docker run -it  -h k230  -e uid=\$(id -u) -e gid=\$(id -g) -e user=\${USER} -v \${HOME}:\${HOME}  -w \$(pwd) wjx/d:latest   #使用

- **编译固件**

参考下面命令进行编译

```bash
make CONF=k230_canmv_01studio_defconfig 
```

>k230_canmv_01studio_defconfig是个例子，需要替换为正确的配置文件，比如替换为k230_canmv_defconfig
>
>sdk支持的所有配置文件见buildroot-overlay/configs目录
>
>make CONF=k230d_canmv_defconfig  含义是使用k230d_canmv_defconfig配置文件

- **编译输出文件**

output/k230_canmv_01studio_defconfig/images/sysimage-sdcard.img.gz

>从嘉楠官网下载的就是这个文件，烧录前需要解压缩，烧录方法见后面
>
>k230_canmv_01studio_defconfig 是个例子，请根据编译配置文件替换为正确名字

### 编译带 AI Demo 的固件

在K230 Linux SDK 根目录下使用 `make menuconfig` 配置 `Target packages -> canaan package -> AI > AI demo` 配置对应的aidemo使能。退出时保存配置，回到根目录下重新执行 `make` 命令。生成固件后烧录，连接串口在 `/root/app`目录下可以看到编译进固件的应用。

### 单独编译AI Demo

- **编译单个ai demo**

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

- **编译所有AI Demo**

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
