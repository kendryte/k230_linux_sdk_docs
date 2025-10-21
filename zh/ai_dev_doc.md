# AI开发文档

## KPU硬件基本原理介绍

在边缘计算场景中（如物联网设备、智能摄像头、工业检测终端、可穿戴设备等），设备通常部署在远离云端数据中心的现场，面临着**实时性要求高、网络带宽受限、数据隐私敏感以及功耗约束严格**的挑战。在这些场景下运行复杂的AI模型（如图像识别、目标检测、语音唤醒），如果仅依赖传统的通用CPU进行计算，往往会遇到**计算量过大、处理速度慢、功耗过高**的问题，难以满足实时响应和能效比的要求。

**KPU（Knowledge Processing Unit）** 是嘉楠科技专为应对边缘AI计算挑战而设计的硬件加速引擎。它本质上是一个高度优化的**深度学习协处理器/加速器**，其核心功能是**高效执行神经网络模型中的密集计算任务**（特别是卷积、矩阵乘法、激活函数等操作）。

**KPU的核心优势**：专精与高效, 与通用CPU相比，KPU的优势在于其**专用化架构**：

- **并行计算能力：** KPU内部包含大量专为神经网络计算设计的处理单元（PE），能够同时处理海量数据（如特征图、权重），显著加速模型推理过程。
- **优化的数据流与内存访问：** 针对神经网络计算模式（如数据复用）进行深度优化，减少不必要的数据搬运，最大化利用内存带宽，降低延迟。
- **高能效比：** 专用电路设计避免了CPU执行通用指令的开销，在执行相同的AI计算任务时，KPU通常能提供**数十倍甚至上百倍于CPU的计算效率（TOPS/W）**，在有限的边缘设备功耗预算内实现高性能AI处理。
- **降低CPU负载：** 将繁重的AI计算任务卸载（Offload）到KPU执行，释放宝贵的CPU资源去处理设备控制、通信、用户交互等其他关键任务，提升系统整体响应能力和稳定性。

KPU支持各种主流的神经网络模型结构，适用于广泛的边缘视觉AI应用场景，包括但不限于：

- **图像分类：** 识别图像中的物体类别（如识别水果种类、工业零件）。
- **目标检测：** 定位并识别图像中的多个目标及其位置（如检测行人、车辆、缺陷）。
- **语义分割：** 对图像中的每个像素进行分类（如区分道路、天空、建筑物；医疗图像分析）。
- **人脸检测与识别：** 设备端的人脸验证、门禁考勤。
- **姿态估计：** 分析人体关节位置（如健身动作指导）。

**KPU在系统中的定位：**

它通常作为SoC（System on Chip）中的一个独立IP核存在，与CPU、内存、外设等协同工作。CPU负责系统管理、任务调度和应用逻辑，而将计算密集型的AI模型推理任务高效地交给KPU执行。下图展示了KPU在典型边缘AI SoC中的位置。

![kpu_in_system](https://www.kendryte.com/api/post/attachment?id=610)

## K230 AI 应用示例展示

为了帮助开发者快速上手并直观体验 K230 强大的边缘 AI 能力，K230 Linux 源码 镜像内置了丰富多样的 AI 示例程序 (AI Demo)。

这些开箱即用的 Demo 涵盖了单模型应用（如人脸检测）和多模型应用（如手掌关键点）两大类别，用户只需一条命令编译应用，体验主流 AI 功能，且支持`make menuconfig`编译配置，包括但不限于：

- 视觉应用： 物体识别、人脸检测、手势识别、人体识别、车牌识别、OCR 文字识别。
- 音频应用： 关键词识别 (KWS)、中文语音合成 (TTS) 等。

通过这些 Demo，开发者可以快速验证模型性能，熟悉 K230 的 AI 推理能力，为后续的定制化开发打下坚实基础。

**运行方式：**

所有 Demo 的源代码均开放、结构清晰，统一存放在 `k230_linux_sdk/buildroot-overlay/package/ai_demo` 目录下。用户可以自行搭建编译环境，并完成aidemo的编译、运行、调试和深入研究这些代码，理解 API 调用、数据处理流程和模型集成方式，极大地加速自身应用的开发进程。具体内容请参考文档：[K230_AI_Demo使用指南](./app_develop_guide/ai_develop/aidemo_doc.md)。

**注意事项：**

- 部分 Demo 因内存占用较高，在 K230D 芯片上可能无法正常运行。

- 关于K230和K230D的区别，请参考：**[产品中心](https://www.kendryte.com/zh/products)**

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

## AI模型推理的基本流程

把训练的AI模型部署在K230上的基本流程见下面的流程图：

![pipeline_model_deploy](https://www.kendryte.com/api/post/attachment?id=611)

🏷️ **数据采集**:

数据采集是指通过摄像头、麦克风等传感设备收集原始输入数据的过程。采集数据的质量与数量直接决定了模型训练与推理的效果。因此，选择合适的采集设备和策略至关重要。

为获得更好的部署效果，推荐使用 K230 本身采集图像数据，以确保数据分布更贴近实际部署环境。

🏷️ **数据标注**:

数据标注是为采集到的数据添加语义标签的过程，用于监督学习模型的训练。这一过程可以通过人工方式完成，也可以借助标注工具进行半自动化处理。

比如图像分类任务需要为每张图像分配正确的类别标签；目标检测任务要为图像中每个目标添加边界框及其类别标签。准确的标注对于训练出高性能、泛化能力强的模型至关重要。

🏷️ **模型训练**:

模型训练阶段是整个 AI 应用开发流程的重要步骤之一，其主要目标是利用已标注的数据集，通过深度学习方法训练出具有泛化能力的神经网络模型。在这一过程中，模型通过不断地调整内部参数，逐步拟合数据的分布特征，以便在面对未见过的输入数据时，仍能做出准确且稳定的预测结果。

模型训练通常需要依托大量高质量的样本数据，涵盖任务相关的多样性场景与类别。数据的充分性和标注的准确性直接影响模型的学习效果和应用表现。在训练过程中，神经网络模型会从输入数据中提取特征，计算预测输出，并通过与真实标签对比产生损失（Loss），再借助反向传播机制调整网络中的权重参数，不断优化模型的性能。

为了实现高效的训练，开发者需要选择一个适合当前任务的模型结构，如图像分类中的 MobileNet、ResNet，目标检测中的 YOLO 系列等。模型的选择不仅取决于精度要求，还需考虑推理速度、模型体积和部署平台的资源约束等因素，特别是在面向 K230 这样的边缘 AI 芯片时，轻量化模型更具实际价值。

此外，训练过程往往需要在具备一定算力支持的计算平台（如 GPU 服务器或本地高性能工作站）上进行，以保证模型在合理时间内完成优化。现代深度学习训练通常使用成熟的训练框架，如 **PyTorch** 和 **TensorFlow**，它们提供了丰富的神经网络构建模块、优化器、损失函数及数据处理工具，极大地简化了模型开发流程。您可以根据自身的技术背景和模型需求，选择合适的框架开展训练工作。

🏷️ **模型转换和验证**:

由于边缘设备计算资源有限，不能直接部署在高算力平台训练得到的模型。必须通过模型转换工具对模型进行优化与量化，生成适用于目标硬件的推理格式。

对于 K230 芯片：

- 使用 KPU（Knowledge Processing Unit） 作为神经网络加速单元；
- 支持的模型格式为 KModel；
- 使用 nncase 编译器 将训练好的 ONNX 或 TFLite 模型 转换为 KModel；
- 转换过程中会进行结构优化与量化，以减少模型体积和计算复杂度。

转换完成后，还需进行功能验证，确保模型在精度、延迟和资源使用方面满足应用需求。

🏷️ **模型部署**:

验证通过的 KModel 可以通过 K230 Linux SDK 提供的 API 加载到设备上运行。

部署流程通常包含以下几个步骤：

- 加载kmodel；
- 读取图像/音频等输入数据；
- 执行数据预处理（如缩放、归一化、通道排列等）；
- 运行模型推理；
- 执行结果后处理（如分类解码、边界框过滤等）；
- 绘制/输出推理结果。

不同模型的预处理和后处理流程可能不同，需根据具体模型手动适配相应代码逻辑。

🏷️ **模型调优**:

部署完成后，仍需对模型进行性能与效果上的调优，以适配边缘场景的实际需求。优化措施包括但不限于：

- 设置更合理的推理阈值或输出策略；
- 调整模型转换参数（如量化策略、输入分辨率）；
- 改进模型结构或训练超参数；
- 丰富并优化数据集；
- 优化推理流程（如线程调度、内存复用）。

模型调优是一个持续迭代的过程，有助于提升系统的稳定性、实时性与能效比。

以上六个步骤构成了在 K230 芯片 上完成 AI 模型部署与推理的完整流程。每一步均需精心设计与执行，以确保最终应用具备良好的性能、稳定性与用户体验。

## 训练模型

```{note}
🤖 **【场景定义】**：在 K230 开发板上实现“打印数字的识别与定位”。

📌 **任务背景**：
在很多 AI 应用中，我们经常会遇到“识别图片里的某些东西”的需求，比如识别图片中的人脸、物体，或者像本例中识别数字。为了更好地理解目标检测的基本流程，我们设计了一个简单的小任务————**识别打印纸上 “0”、“1”、“2”、“3” 这四种数字，并标出它们在图像中的位置**。

这个任务不复杂，但能完整地练习一遍从模型部署到图像处理、结果显示的整个过程。它作为一个入门教程，帮助大家快速掌握如何在 K230 平台上部署 AI 模型，进行目标检测，并将检测结果显示在屏幕上。

🎯 **项目目标**：
基于 Kendryte K230 AI SoC 平台，开发一个轻量级、高性能的视觉识别示例，实现以下功能：

* ✅ **识别类别**：仅识别“0”、“1”、“2”、“3”四类数字字符；
* ✅ **识别对象**：打印在纸张上的标准字体数字；
* ✅ **定位功能**：不仅识别数字类别，还能**准确获取每个数字在图像中的位置坐标**（框出检测框），为后续处理或操作提供基础；
* ✅ **运行平台**：应用部署在 K230 开发板，利用其**AI 硬件加速、摄像头输入、屏幕显示能力**，实现端侧推理、实时显示。

🖼 **预期效果图**：

![4_number_det](https://www.kendryte.com/api/post/attachment?id=645)
```

### 数据采集

```{note}
👉 采集训练数据其实很简单！你只需要先把 MicroPython 固件烧进开发板，然后找到那个脚本——/sdcard/examples/16-AI-Cube/DataCollectionCamera.py，把它改名为 main.py，放到 /sdcard 目录下。接着重新上电（也就是重启一下板子），运行起来后，按下板子上的key按键就可以开始采集啦！每按一下就拍一张照片，图像会自动保存到 /sdcard/examples/data/ 文件夹里，完全不用你管，超省心！
```

在训练模型之前，数据采集是整个流程中的第一步，也是至关重要的一步。高质量的数据不仅能提升模型的性能，还能增强模型在实际应用场景中的泛化能力。根据不同的应用需求，数据采集可以分为**通用场景**和**专用场景**两种情况，下面将分别进行详细说明。

📌 **通用场景下的数据采集**

在通用人工智能任务中，如图像分类、目标检测、语义分割等，通常可以借助已有的公开数据集来构建训练样本。这些数据集由学术机构、研究组织或大型企业整理发布，具有良好的标注质量和广泛的应用基础。

比如，常见图像类公开数据集包括：ImageNet、COCO、MNIST、Fashion-MNIST、CIFAR系列等，或者寻找网络上对应场景的开源数据集。

虽然公开数据集质量较高，但在实际使用前仍需进行适当的筛选与处理，以确保其符合项目需求：

- **质量保证处理**：去除模糊、错误标注或低质量样本。
- **类别平衡**：确保各类别样本数量均衡，避免模型偏向。
- **格式统一**：将数据转换为统一格式（如JPEG、PNG等）。
- **数据扩增**：通过旋转、裁剪、翻转、添加噪声等方式扩充数据量，提高模型鲁棒性。
- **构建定制化数据集**：有时单一数据集可能无法满足特定需求，可以通过组合多个数据集并进行重新标注和清洗，构建更符合业务场景的定制化数据集。

📌 **专用场景下的数据采集**

对于一些特殊行业或具体应用场景（如工业质检、农业监测、安防监控、医疗诊断等），往往需要采集专用于该场景的数据。这种情况下，公开数据集可能无法准确反映真实环境的数据分布，因此需要进行**定制化数据采集**。

在某些特定的AI部署场景中，有条件的情况下可以直接**使用K230设备**进行数据采集。这样**采集的数据更贴近实际部署环境，有助于提升模型在设备上的表现**。

⚠️ 这里给出一些数据采集流程建议：

- **明确采集目标**：定义采集对象（如物体类型、场景）、光照条件、角度、分辨率等。
- **明确数据任务**：不同的任务对数据集的要求不同，一方面要考虑实际部署场景，另一方面要考虑任务需求，比如分类任务可能需要物体占据较大的区域，大片的背景可能会影响分类效果；而目标检测可以有大小不同的多个物体。
- **使用合适工具**：使用K230开发板配合摄像头模块，可编写脚本自动采集。
- **同步标注信息**：在采集过程中尽量同步记录标签信息，便于后期标注。
- **初步质量检查**：剔除模糊、曝光过度、遮挡严重等无效样本。
  
### 数据标注

```{note}
👉 拿到采集好的图片之后，就可以开始给它们打标签啦！根据这个任务的要求，你可以用一些常见的标注工具，比如 LabelImg、Labelme 或 X-AnyLabeling，给图片里的数字加上对应的类别、画出目标框。你可以亲自采集图像、自己动手标注，整个过程也挺有趣的。当然啦，如果你不想从头做，我们也贴心准备了一份现成的“0/1/2/3四类打印数字识别”数据集，直接点这里就能下载：[0/1/2/3四类打印数字识别数据集](https://kendryte-download.canaan-creative.com/developer/k230/yolo_dataset/number_det.zip)。省时又省力，直接上手训练也没问题！
```

数据标注是训练模型的关键步骤之一，它涉及到对原始数据进行标注，以便模型能够学习到数据的特征和模式。在进行数据标注时，需要考虑以下几个方面：

- **标注格式**：选择适合模型的标注格式，如XML、JSON、TXT等。
- **标注工具**：选择适合的标注工具，如LabelImg、Labelme、X-AnyLabeling、VIA等。
- **标注质量**：确保标注的准确性和一致性，避免标注错误。
- **标注策略**：根据任务需求和数据特点，选择合适的标注策略，如边界框标注、关键点标注等。

关于常见的视觉任务，这里推荐使用X-AnyLabeling进行标注。下载链接: [X-AnyLabeling-release](https://github.com/CVHub520/X-AnyLabeling/releases)。
  
### 模型训练

```{note}
👉 模型训练的方法有很多，其中 YOLO 系列是现在特别常用的选择，比如 YOLOv5、YOLOv8 或 YOLO11。我们推荐你用 YOLO 来进行训练，因为它效果好、速度快、社区也很活跃。更棒的是，我们提供的数据集已经整理好了，可以直接用来训练 YOLO 模型！你只需要跳转到这个示例：[YOLO检测示例](#yolov8跌倒检测)，按照里面的流程来做，把示例中的数据集部分换成我们准备的“0/1/2/3 四类打印数字识别数据集”就行啦。本节的目标是先把模型训练好，并导出为 ONNX 格式，后面还有更多有趣的内容等着你继续解锁！
```

模型训练是整个AI流程中最重要的一步，它涉及到模型的构建、训练和优化。在进行模型训练时，需要考虑以下几个方面：

- **模型选择**：根据任务需求和数据特点，选择适合的模型。
- **模型构建**：构建模型的网络结构，包括输入层、隐藏层和输出层。
- **模型训练**：使用标注好的数据进行模型训练，包括选择合适的损失函数和优化器。
- **模型评估**：使用测试集对模型进行评估，评估模型的性能和泛化能力。
- **模型优化**：根据模型评估结果，对模型进行优化，提高模型的性能和泛化能力。

训练好的模型需要转换成onnx模型或者tflite模型，准备后续使用nncase进行模型转换，得到可以在K230上推理的kmodel。

## 模型转换

当我们训练结束后，会得到一个 ONNX 模型文件。但这个模型还不能直接在 K230 上用 KPU 来跑，因为 KPU 只支持 Kmodel 格式。

所以接下来，我们要用一个叫 nncase 的编译器，把 ONNX 模型“翻译”成 Kmodel，这样 KPU 才能理解并运行它。

下面我们就来简单认识一下这个关键工具 —— nncase！

### 什么是 nncase

#### nncase 简介

`nncase` 是一款专为 AI 加速器设计的**神经网络编译器**，目前已支持的后端（target）包括：**CPU、K210、K510、K230** 等平台。

**nncase 提供的核心功能**：

- 支持 **多输入多输出** 的网络结构，兼容常见的 **多分支模型拓扑**；
- 采用 **静态内存分配** 策略，无需依赖运行时堆内存，资源占用可控；
- 实现 **算子融合与图优化**，有效减少冗余计算，提升推理效率；
- 支持 **浮点（float）推理** 和 **定点量化推理（uint8/int8）**；
- 支持 **训练后量化（Post-Training Quantization, PTQ）**，可基于浮点模型和校准数据集生成高效的量化模型；
- 编译生成的模型为**平坦结构（Flat Model）**，具备 **零拷贝加载（Zero-Copy Loading）** 能力，适合资源受限的嵌入式场景。

**支持的模型格式**：

nncase 支持从主流深度学习框架导出的以下模型格式：

- **TFLite（TensorFlow Lite）**
- **ONNX（Open Neural Network Exchange）**

您可以使用 PyTorch、TensorFlow 等训练框架导出模型至上述格式，再通过 nncase 转换为 KModel，以部署至 K230 等设备。

**架构概览**：

![nncase架构](https://www.kendryte.com/api/post/attachment?id=509)

nncase 的软件栈主要包括以下两大组成部分：

- **Compiler（编译器）**：将高层框架导出的 TFLite 或 ONNX 模型，转换为适用于目标硬件平台的 KModel 格式，并执行结构优化、算子调度与量化处理；
- **Runtime（运行时）**：在目标设备（如 K230）上加载并运行 KModel，结合硬件加速单元（如 KPU）实现高性能模型推理。

🏷️ **Compiler**: 用于在PC上编译神经网络模型，最终生成kmodel文件。主要包括importer, IR, Evaluator, Quantize, Transform优化, Tiling, Partition, Schedule, Codegen等模块。

- Importer: 将其它神经网络框架的模型导入到nncase中；
- IR: 中间表示, 分为importer导入的Neutral IR(设备无关)和Neutral IR经lowering转换生成的Target IR(设备相关)；
- Evaluator: Evaluator提供IR的解释执行能力，常被用于Constant Folding/PTQ Calibration等场景；
- Transform: 用于IR转换和图的遍历优化等；
- Quantize: 训练后量化, 对要量化的tensor加入量化标记, 根据输入的校正集, 调用 Evaluator进行解释执行, 收集tensor的数据范围, 插入量化/反量化结点, 最后优化消除不必要的量化/反量化结点等；
- Tiling: 受限于NPU较低的存储器容量，需要将大块计算进行拆分。另外，计算存在大量数据复用时选择Tiling参数会对时延和带宽产生影响；
- Partition: 将图按ModuleType进行切分, 切分后的每个子图会对应RuntimeModule, 不同类型的RuntimeModule对应不同的Device(CPU/K230)；
- Schedule: 根据优化后图中的数据依赖关系生成计算顺序并分配Buffer；
- Codegen: 对每个子图分别调用ModuleType对应的codegen，生成RuntimeModule；

🏷️ **Runtime**: 集成于用户应用程序（App）中，提供模型加载、输入设置、推理执行和输出读取等功能。Runtime 接口屏蔽了底层硬件差异，使开发者能更专注于模型推理逻辑的集成与应用开发。

模型转换章节主要介绍nncase compiler和simulator的使用方法。

#### 安装 nncase 环境

- **Linux 环境搭建 nncase**

首先，请安装 `.NET SDK 7.0` 并配置 `DOTNET_ROOT` 环境变量。**请注意，不建议在 Anaconda 虚拟环境中安装 `dotnet`，否则可能导致兼容性问题。**

```bash
sudo apt-get update
sudo apt-get install dotnet-sdk-7.0
export DOTNET_ROOT=/usr/share/dotnet
```

接下来，通过 pip 安装 `nncase` 和 `nncase-kpu`：

```bash
pip install nncase nncase-kpu
```

- **Windows 环境搭建 nncase**

首先安装 [.NET SDK 7.0](https://learn.microsoft.com/zh-cn/dotnet/core/install/windows)，请根据 Microsoft 官方文档完成安装流程。
安装 `nncase` 库。可通过 pip 在线安装主程序 `nncase`，并从 [GitHub Releases 页面](https://github.com/kendryte/nncase/releases) 下载对应版本的 `nncase_kpu`，再使用 pip 离线安装。

```bash
pip install nncase
# 请将 `2.x.x` 替换为实际下载版本号。
pip install nncase_kpu-2.x.x-py2.py3-none-win_amd64.whl
```

- **使用 Docker 搭建环境**

如果您未配置 Ubuntu 本地环境，可直接使用官方提供的 `nncase` Docker 镜像。该镜像基于 Ubuntu 20.04，预装了 Python 3.8 和 dotnet-sdk-7.0，方便快速启动。

```bash
cd /path/to/nncase_sdk
docker pull ghcr.io/kendryte/k230_sdk
docker run -it --rm -v `pwd`:/mnt -w /mnt ghcr.io/kendryte/k230_sdk /bin/bash
```

- **查看 nncase 版本信息**

进入 Python 交互环境后可通过如下命令确认当前安装的 `nncase` 版本：

```python
>>> import _nncase
>>> print(_nncase.__version__)
2.9.0
```

> 示例输出为 `2.9.0`，请以实际安装版本为准。

### 使用 nncase 编译器转换kmodel

![compile_kmodel](https://www.kendryte.com/api/post/attachment?id=636)

编译kmodel的流程主要包含以下关键步骤，每个步骤都有其特定的目的和技术考量：

**设置编译选项**：这一步的核心目的是为模型部署适配目标硬件平台。由于边缘计算设备需要明确指定运行平台以确保生成的kmodel是否需要利用硬件（kpu）加速。同时，配置预处理参数（如输入标准化参数）到kmodel内部可减少推理时的计算开销，提升整体效率。

**初始化编译器**：nncase编译器的初始化是为后续转换工作构建标准化环境。编译器根据前述配置的编译选项完成初始化过程。

**导入原始模型**：当前主流训练框架（如TensorFlow/PyTorch）生成的ONNX/TFLite模型包含通用运算符，但KPU作为专用加速器需要特定算子格式。此步骤通过模型解析和算子转换，将原始模型转化为编译器可优化的中间表示，为后续硬件相关优化奠定基础。

**量化处理**：这是提升边缘侧推理性能的关键环节。我们训练得到的FP32模型虽精度高但存在计算延迟大、内存占用高等问题。通过量化到INT8/INT16：显著减少模型体积，提升计算速度（利用硬件定点加速指令），降低功耗（减少内存带宽需求）。需注意的是，量化会引入精度损失，因此需要通过校准数据集帮助模型确定在量化过程中每一层权重和激活值应该被映射到的范围，以便保留更多的信息，减少量化误差。量化过程需要配置量化参数和校准数据，量化参数见[编译参数说明](#编译参数说明)。

**编译生成kmodel**：在前述优化基础上，最终生成的kmodel是经过深度优化的可直接部署到K230设备执行高效推理。

#### 转换示例

我们就以**四类打印数字识别**场景为例，将上面得到的ONNX模型转换成Kmodel。这里给出编译示例脚本：

```python
# 导入所需库
import os
import argparse
import numpy as np
from PIL import Image  # 用于图像读取和处理
import onnxsim         # ONNX 模型简化工具
import onnx            # ONNX 模型处理工具
import nncase          # nncase 编译器 SDK
import shutil
import math

def parse_model_input_output(model_file, input_shape):
    # 加载ONNX模型
    onnx_model = onnx.load(model_file)
    
    # 获取模型中所有输入节点名称
    input_all = [node.name for node in onnx_model.graph.input]
    
    # 获取模型中已经被初始化的参数（如权重等），这些不属于输入数据
    input_initializer = [node.name for node in onnx_model.graph.initializer]
    
    # 真实输入 = 所有输入 - 初始化器
    input_names = list(set(input_all) - set(input_initializer))
    
    # 从图中提取真实输入张量
    input_tensors = [node for node in onnx_model.graph.input if node.name in input_names]

    # 提取输入张量的名称、数据类型、形状等信息
    inputs = []
    for _, e in enumerate(input_tensors):
        onnx_type = e.type.tensor_type
        input_dict = {}
        input_dict['name'] = e.name
        # 转换为NumPy数据类型
        input_dict['dtype'] = onnx.mapping.TENSOR_TYPE_TO_NP_TYPE[onnx_type.elem_type]
        # 如果某维为0，说明ONNX模型未固定shape，使用传入的input_shape代替
        input_dict['shape'] = [(i.dim_value if i.dim_value != 0 else d) for i, d in zip(onnx_type.shape.dim, input_shape)]
        inputs.append(input_dict)

    return onnx_model, inputs

def onnx_simplify(model_file, dump_dir, input_shape):
    # 获取模型和输入形状信息
    onnx_model, inputs = parse_model_input_output(model_file, input_shape)

    # 自动推断缺失的shape信息
    onnx_model = onnx.shape_inference.infer_shapes(onnx_model)

    # 构造用于onnxsim的输入shape映射
    input_shapes = {input['name']: input['shape'] for input in inputs}

    # 简化模型
    onnx_model, check = onnxsim.simplify(onnx_model, input_shapes=input_shapes)
    assert check, "模型简化校验失败"

    # 保存简化后的模型
    model_file = os.path.join(dump_dir, 'simplified.onnx')
    onnx.save_model(onnx_model, model_file)
    return model_file

def read_model_file(model_file):
    with open(model_file, 'rb') as f:
        model_content = f.read()
    return model_content

def generate_data(shape, batch, calib_dir):
    # 获取数据集中的所有图片路径
    img_paths = [os.path.join(calib_dir, p) for p in os.listdir(calib_dir)]
    data = []

    for i in range(batch):
        assert i < len(img_paths), "校准图片数量不足"

        # 加载图片，转换为RGB格式
        img_data = Image.open(img_paths[i]).convert('RGB')

        # 按模型输入尺寸进行缩放
        img_data = img_data.resize((shape[3], shape[2]), Image.BILINEAR)

        # 转换为NumPy数组
        img_data = np.asarray(img_data, dtype=np.uint8)

        # 转换为 NCHW 格式
        img_data = np.transpose(img_data, (2, 0, 1))

        # 增加batch维度
        data.append([img_data[np.newaxis, ...]])

    return np.array(data)

def main():
    # 命令行参数定义
    parser = argparse.ArgumentParser(prog="nncase")
    parser.add_argument("--target", default="k230", type=str, help='编译目标，例如k230或cpu')
    parser.add_argument("--model", type=str, help='输入ONNX模型路径')
    parser.add_argument("--dataset_path", type=str, help='PTQ校准数据集路径')
    parser.add_argument("--input_width", type=int, default=320, help='模型输入宽度')
    parser.add_argument("--input_height", type=int, default=320, help='模型输入高度')
    parser.add_argument("--ptq_option", type=int, default=0, help='PTQ选项：0-5')

    args = parser.parse_args()

    # 输入尺寸向上对齐到32的整数倍，符合硬件要求
    input_width = int(math.ceil(args.input_width / 32.0)) * 32
    input_height = int(math.ceil(args.input_height / 32.0)) * 32
    input_shape = [1, 3, input_height, input_width]  # NCHW格式

    # 创建临时目录保存中间模型
    dump_dir = 'tmp'
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)

    # 简化模型
    model_file = onnx_simplify(args.model, dump_dir, input_shape)

    # 编译选项设置
    compile_options = nncase.CompileOptions()
    compile_options.target = args.target                  # 指定目标平台
    compile_options.preprocess = True                     # 启用预处理
    compile_options.swapRB = False                        # 不交换RB通道
    compile_options.input_shape = input_shape             # 设置输入形状
    compile_options.input_type = 'uint8'                  # 输入图像数据类型
    compile_options.input_range = [0, 1]                  # 输入图像反量化范围
    compile_options.mean = [0, 0, 0]                      # 预处理均值
    compile_options.std = [1, 1, 1]                       # 标准差设为1，不进行归一化
    compile_options.input_layout = "NCHW"                 # 输入数据格式

    # 初始化编译器
    compiler = nncase.Compiler(compile_options)

    # 导入ONNX模型为IR
    model_content = read_model_file(model_file)
    import_options = nncase.ImportOptions()
    compiler.import_onnx(model_content, import_options)

    # PTQ选项设置（后训练量化）
    ptq_options = nncase.PTQTensorOptions()
    ptq_options.samples_count = 10  # 校准样本数量

    # 支持6种量化方案（根据精度与性能权衡选择）
    if args.ptq_option == 0:
        ptq_options.calibrate_method = 'NoClip'
        ptq_options.quant_type = 'uint8'
        ptq_options.w_quant_type = 'uint8'
    elif args.ptq_option == 1:
        ptq_options.calibrate_method = 'NoClip'
        ptq_options.quant_type = 'uint8'
        ptq_options.w_quant_type = 'int16'
    elif args.ptq_option == 2:
        ptq_options.calibrate_method = 'NoClip'
        ptq_options.quant_type = 'int16'
        ptq_options.w_quant_type = 'uint8'
    elif args.ptq_option == 3:
        ptq_options.calibrate_method = 'Kld'
        ptq_options.quant_type = 'uint8'
        ptq_options.w_quant_type = 'uint8'
    elif args.ptq_option == 4:
        ptq_options.calibrate_method = 'Kld'
        ptq_options.quant_type = 'uint8'
        ptq_options.w_quant_type = 'int16'
    elif args.ptq_option == 5:
        ptq_options.calibrate_method = 'Kld'
        ptq_options.quant_type = 'int16'
        ptq_options.w_quant_type = 'uint8'

    # 设置PTQ校准数据
    ptq_options.set_tensor_data(generate_data(input_shape, ptq_options.samples_count, args.dataset_path))

    # 应用PTQ
    compiler.use_ptq(ptq_options)

    # 编译模型
    compiler.compile()

    # 导出KModel文件
    base, ext = os.path.splitext(args.model)
    kmodel_name = base + ".kmodel"
    with open(kmodel_name, 'wb') as f:
        f.write(compiler.gencode_tobytes())

# Python程序主入口
if __name__ == '__main__':
    main()
```

将上述代码保存为`to_kmodel.py`脚本，使用如下转换命令完成编译：

```shell
# 你需要将onnx模型换成你训练好的模型
python to_kmodel.py --target k230 --model best.onnx --dataset_path test --input_width 320 --input_height 320 --ptq_option 0
```

通过上面的代码，我们已经成功拿到了用于识别四类数字的 Kmodel 模型。那么你可能会好奇：在把模型转换成 Kmodel 的过程中，里面用到的那些参数到底是啥意思？如果以后我想换个模型来转，是不是也要改参数呢？别着急，接下来的章节我们就会带你搞懂这些转换参数的具体含义，还会教你在转换其他模型时该怎么正确配置，一步步带你上手，不迷路！

#### 编译参数说明

使用 `nncase compiler` 将 `tflite/onnx` 模型转换成 `kmodel` ，模型转换代码的关键在于根据自身需求进行选项配置，主要是 `CompileOptions` 、 `PTQTensorOptions` 和 `ImportOptions`。

`nncase` 用户指南文档见：[github: user_guide](https://github.com/kendryte/nncase/tree/master/examples/user_guide) 或 [gitee: user_guide](https://gitee.com/kendryte/nncase/tree/master/examples/user_guide) 。

- **编译选项 CompileOptions**

`CompileOptions` 类, 用于配置 `nncase` 编译选项，各属性说明如下：

| 属性名称                    |         类型          | 是否必须 | 描述                                                                                                                   |
| :-------------------------- | :-------------------: | :------: | ---------------------------------------------------------------------------------------------------------------------- |
| target                      |        string         |    是    | 指定编译目标, 如'cpu', 'k230'                                                                                          |
| dump_ir                     |         bool          |    否    | 指定是否dump IR, 默认为False                                                                                           |
| dump_asm                    |         bool          |    否    | 指定是否dump asm汇编文件, 默认为False                                                                                  |
| dump_dir                    |        string         |    否    | 前面指定dump_ir等开关后, 这里指定dump的目录, 默认为""                                                                  |
| input_file                  |        string         |    否    | ONNX模型超过2GB时，用于指定参数文件路径，默认为""                                                                      |
| preprocess                  |         bool          |    否    | 是否开启前处理，默认为False。以下参数仅在 `preprocess=True`时生效                                                      |
| input_type                  |        string         |    否    | 开启前处理时指定输入数据类型，默认为"float"。当 `preprocess`为 `True`时，必须指定为"uint8"或者"float32"                |
| input_shape                 |       list[int]       |    否    | 开启前处理时指定输入数据的shape，默认为[]。当 `preprocess`为 `True`时，必须指定                                        |
| input_range                 |      list[float]      |    否    | 开启前处理时指定输入数据反量化后的浮点数范围，默认为[ ]。当 `preprocess`为 `True`且 `input_type`为 `uint8`时，必须指定 |
| input_layout                |        string         |    否    | 指定输入数据的layout，默认为""                                                                                         |
| swapRB                      |         bool          |    否    | 是否在 `channel`维度反转数据，默认为False                                                                              |
| mean                        |      list[float]      |    否    | 前处理标准化参数均值，默认为[0,0,0]                                                                                    |
| std                         |      list[float]      |    否    | 前处理标准化参数方差，默认为[1,1,1]                                                                                    |
| letterbox_value             |         float         |    否    | 指定前处理letterbox的填充值，默认为0                                                                                   |
| output_layout               |        string         |    否    | 指定输出数据的layout, 默认为""                                                                                         |
| shape_bucket_enable         |         bool          |    是    | 是否开启ShapeBucket功能，默认为False。在 `dump_ir=True`时生效                                                          |
| shape_bucket_range_info     | Dict[str, [int, int]] |    是    | 每个输入shape维度信息中的变量的范围，最小值必须大于等于1                                                               |
| shape_bucket_segments_count |          int          |    是    | 输入变量的范围划分为几段                                                                                               |
| shape_bucket_fix_var_map    |    Dict[str, int]     |    否    | 固定shape维度信息中的变量为特定的值|

关于前处理的配置说明，请参考 API 文档：[nncase 模型编译API手册前处理流程](./app_develop_guide/nncase/nncase_compile.md#前处理流程说明)。将部分前处理操作封装在模型内可以提高开发板推理时的前处理效率，支持的前处理包括：`swapRB`(RGB->BGR or BGR->RGB)、`Transpose`(NHWC->NCHW or NCHW->NHWC)、`Normalization`（减均值除方差）、`Dequantize`等。比如：onnx模型需要的输入是`RGB`的，我们使用`opencv`读取的图片是`BGR`，正常onnx模型推理的预处理我们需要先将`BGR`转成`RGB`给onnx模型使用。转kmodel的时候我们就可以设置 `swapRB` 为 `True` ，这样kmodel中自带交换`RB`通道的预处理步骤，在进行kmodel推理的预处理时，我们就可以忽略交换`RB`通道的步骤，将此步骤放到kmodel内部。

- **导入选项 ImportOptions**

ImportOptions类, 用于配置nncase导入选项，配置编译器的待转换模型。可以配置 `tflite/onnx`。使用示例如下：

```python
# 读取并导入tflite模型
model_content = read_model_file(model)
compiler.import_tflite(model_content, import_options)

# 读取并导入onnx模型
model_content = read_model_file(model)
compiler.import_onnx(model_content, import_options)
```

- **训练后量化选项 PTQTensorOptions**

`PTQTensorOptions` 类, 用于配置 `nncase PTQ` 选项：

| 名称                           | 类型   | 是否必须 | 描述 |
| ------------------------------ | ------ | -------- | ---- |
| samples_count                  | int    |    否    |  指定用于量化的校正集数量    |
| calibrate_method               | string |    否    |  指定量化方法，可选'NoClip'、'Kld'，默认为'Kld'   |
| finetune_weights_method        | string |    否    |  指定是否对权重进行微调，可选'NoFineTuneWeights'、'UseSquant'，默认为'NoFineTuneWeights'  |
| quant_type                     | string |    否    |  指定数据量化类型，可选'uint8'，'int8'，'int16'，`quant_type`和`w_quant_type`两种类型不可同时为'int16'  |
| w_quant_type                   | string |    否    |  指定权重量化类型，可选'uint8'，'int8'，'int16'，`quant_type`和`w_quant_type`两种类型不可同时为'int16' |
| quant_scheme                   | string |    否    |  导入量化参数配置文件的路径 |
| quant_scheme_strict_mode       | bool   |    否    |  是否严格按照quant_scheme执行量化  |
| export_quant_scheme            | bool   |    否    |  是否导出量化参数配置文件  |
| export_weight_range_by_channel | bool   |    否    |  是否导出 `bychannel`形式的weights量化参数，该参数建议设置为 `True`  |

混合量化具体使用流程见 [MixQuant说明](https://github.com/kendryte/nncase/blob/release/2.0/docs/MixQuant.md)。

关于量化的配置说明，请参考上表。如果转换的kmodel达不到效果，可以修改 `quant_type` 和 `w_quant_type` 参数，修改模型数据和权重的量化类型，但是这两个参数不能同时设置为 `int16`。

- **量化校正集设置**

| 名称 | 类型                  | 描述           |
| ---- | --------------------- | -------------- |
| data | List[List[np.ndarray]] | 读取的校准数据 |

量化过程中使用的校正数据通过 `set_tensor_data` 方法进行设置，接口参数类型为 `List[List[np.ndarray]]`，比如：模型有一个输入，校正数据量设置为10，传入的校正数据维度为 `[10,1,3,320,320]`；如果模型有两个输入，校正数据量设置为10，传入的校正数据维度为 `[[10,1,3,224,224],[10,1,3,320,320]]`。

### 使用 nncase 模拟器验证转换效果

前面我们说了怎么把模型转换成 Kmodel，现在我们要来“体检”一下这个模型，看它转得好不好！

因为 ONNX 和 Kmodel 在预处理的时候可能不太一样，所以我们得分别按它们各自的要求来准备输入数据。然后，用 ONNX 模型和 Kmodel 模型各跑一遍推理，把结果都保存下来，接着算一下它们之间的 **Cosine 相似度**——这就像是在对比它俩输出的“相似度”。

一句话总结就是：我们要看看转换后的 Kmodel 和原来的 ONNX 模型，输出差不多不？如果相差太大，说明转换过程中可能有问题，那就要回头检查参数设置～

模型转换成功后，可以使用`nncase.Simulator` 在本地PC上加载Kmodel进行推理，通过计算onnx模型和kmodel模型的余弦相似度判断kmodel输出是否正确。**这里需要注意的是，该过程是在本地计算机上运行的，而不是在k230开发板上运行的。**

首先需要在python环境下安装onnx相关的包：

```shell
pip install onnx
pip install onnxruntime
pip install onnxsim
```

执行模拟器推理脚本需要添加nncase插件环境变量：

- **linux**：

```shell
# 下述命令中的路径为安装 nncase 的 Python 环境的路径，请按照您的环境适配修改
export NNCASE_PLUGIN_PATH=$NNCASE_PLUGIN_PATH:/usr/local/lib/python3.9/site-packages/
export PATH=$PATH:/usr/local/lib/python3.9/site-packages/
source /etc/profile
```

- **windows**：

将安装 `nncase` 的 `Python` 环境下的 `Lib/site-packages` 路径添加到环境变量的系统变量 `Path` 中。

针对**4类打印数字识别**场景，验证输出相似度的示例代码：

```python
import os
import cv2
import numpy as np
import onnxruntime as ort
import nncase
import math

def get_onnx_input(img_path,mean,std,model_input_size):
    # 读取图片，图片数据一般是RGB三通道，颜色范围为[0, 255.0]
    image_fp32=cv2.imread(img_path)
    # 如果模型输入要求是RGB的，则转换为RGB格式，如果要求是BGR的，则不需要转换
    image_fp32=cv2.cvtColor(image_fp32, cv2.COLOR_BGR2RGB)
    # 缩放成模型输入大小
    image_fp32 = cv2.resize(image_fp32, (model_input_size[0], model_input_size[1]))
    # 数据类型为float32,
    image_fp32 = np.asarray(image_fp32, dtype=np.float32)
    # 数据标准化,先归一化到[0,1]范围内，然后减均值除方差
    image_fp32/=255.0
    for i in range(3):
        image_fp32[:, :, i] -= mean[i]
        image_fp32[:, :, i] /= std[i]
    # 按照模型输入要求处理成NCHW排布或者NHWC排布
    image_fp32 = np.transpose(image_fp32, (2, 0, 1))
    return image_fp32.copy()

def get_kmodel_input(img_path,mean,std,model_input_size):
    # 读取图片，图片数据一般是RGB三通道，颜色范围为[0, 255.0]
    image_uint8=cv2.imread(img_path)
    # 如果模型输入要求是RGB的，则转换为RGB格式，如果要求是BGR的，则不需要转换
    image_uint8=cv2.cvtColor(image_uint8, cv2.COLOR_BGR2RGB)
    # 缩放成模型输入大小
    image_uint8 = cv2.resize(image_uint8, (model_input_size[0], model_input_size[1]))
    # 数据类型为uint8,因为转换kmodel的时候开启了预处理，并且设定了标准化参数，因此这里的输入就不需要实现标准化了
    image_uint8 = np.asarray(image_uint8, dtype=np.uint8)
    # 按照模型输入要求处理成NCHW排布或者NHWC排布
    image_uint8 = np.transpose(image_uint8, (2, 0, 1))
    return image_uint8.copy()

def onnx_inference(onnx_path,onnx_input_data):
    # 创建 ONNX 推理会话（加载模型）
    ort_session = ort.InferenceSession(onnx_path)
    # 获取模型输出名称列表，用于后续调用推理
    output_names = []
    model_outputs = ort_session.get_outputs()
    for i in range(len(model_outputs)):
        output_names.append(model_outputs[i].name)

    # 获取模型的输入信息
    model_input = ort_session.get_inputs()[0]             # 第一个输入（通常只有一个）
    model_input_name = model_input.name                   # 输入的名称（键）
    model_input_type = np.float32                         # 输入数据类型，这里假设是 float32
    model_input_shape = model_input.shape                 # 输入张量的形状（维度）

    # 处理输入数据,需确保和模型输入形状一致
    model_input_data = onnx_input_data.astype(model_input_type).reshape(model_input_shape)

    # 执行推理，传入输入名称和数据，返回所有输出结果
    onnx_results = ort_session.run(output_names, { model_input_name : model_input_data })
    return onnx_results

def kmodel_inference(kmodel_path,kmodel_input_data,model_input_size):
    # 初始化nncase 模拟器
    sim = nncase.Simulator()
    # 读取kmodel
    with open(kmodel_path, 'rb') as f:
        kmodel = f.read()
    # 加载kmodel
    sim.load_model(kmodel)
    # 读取输入数据
    input_shape = [1, 3, model_input_size[1], model_input_size[0]]
    dtype = sim.get_input_desc(0).dtype
    # 处理输入数据,需确保和模型输入形状一致
    kmodel_input = kmodel_input_data.astype(dtype).reshape(input_shape)
    # 设置模拟器输入tensor,此处为单输入
    sim.set_input_tensor(0, nncase.RuntimeTensor.from_numpy(kmodel_input))
    # 模拟器推理kmodel模型
    sim.run()
    # 获取推理输出
    kmodel_results = []
    for i in range(sim.outputs_size):
        kmodel_result = sim.get_output_tensor(i).to_numpy()  # 转换为numpy数组
        kmodel_results.append(kmodel_result)  # 保存到列表中
    return kmodel_results

def cosine_similarity(onnx_results,kmodel_results):
    output_size=len(kmodel_results)
    # 将每个输出展成一维，然后计算余弦相似度
    for i in range(output_size):
        onnx_i=np.reshape(onnx_results[i], (-1))
        kmodel_i=np.reshape(kmodel_results[i], (-1))
        cos = (onnx_i @ kmodel_i) / (np.linalg.norm(onnx_i, 2) * np.linalg.norm(kmodel_i, 2))
        print('output {0} cosine similarity : {1}'.format(i, cos))
    return

if __name__ == '__main__':
    img_path="test.jpg"
    mean=[0,0,0]
    std=[1,1,1]
    model_input_size=[320,320]
    # ONNX 模型文件
    onnx_model = "best.onnx"
    # kmodel 模型文件
    kmodel_path="best.kmodel"
    # 生成onnx模型输入数据
    onnx_input_data = get_onnx_input(img_path,mean,std,model_input_size)
    # 生成kmodel模型输入数据
    kmodel_input_data = get_kmodel_input(img_path,mean,std,model_input_size)
    # onnx模型推理
    onnx_results = onnx_inference(onnx_model,onnx_input_data)
    # kmodel模型推理
    nncase_results = kmodel_inference(kmodel_path,kmodel_input_data,model_input_size)
    # 计算输出相似度
    cosine_similarity(onnx_results,nncase_results)
```

将上述代码保存成文件，并将代码内的模型换成您自己转换的模型后，运行脚本得到如下输出：

```shell
output 0 cosine similarity : 0.9995334148406982
```

一般我们认为当相似度大于0.99时，表示该模型转换成功，在实际部署场景下是可用的。

#### 生成输入数据

⚠️ **注意**：在使用 ONNX 模型和 KModel 进行推理时，**必须谨慎处理输入数据的预处理步骤**。若 KModel 中已封装了特定的预处理操作，则在推理前无需对其输入数据手动执行这些预处理；但在使用 ONNX 模型推理时，则需显式地在模型外部完成所有必要的预处理流程。

KModel 所支持并可封装的预处理操作包括：

- 通道顺序变换（如 RGB ↔ BGR），对应 `SwapRB` 参数；
- 布局转换（NCHW ↔ NHWC），对应 `input_shape` 与 `input_layout` 参数；
- 数据标准化处理，依赖 `mean` 和 `std` 参数；
- 输入反量化处理，依赖 `input_type` 和 `input_range` 参数；

关于 ONNX 与 KModel 推理流程的差异，可参考以下流程图：

![inference_diff_onnx_kmodel](https://www.kendryte.com/api/post/attachment?id=612)

在使用 ONNX 模型推理时，由于其本体不包含任何预处理逻辑，用户必须在输入前完成所需的全部预处理步骤。
而对于 KModel，如果在模型编译时启用了 `preprocess` 选项，则相关预处理操作将被自动封装进模型内部，推理时不再需要用户手动处理。
如果未启用 `preprocess`，其使用方式与 ONNX 模型相同，仍需在模型外部完成所有预处理过程。

根据上述流程，开发者可按照模型要求构造符合输入规范的推理数据，以便在推理过程中使用。
**请注意：数据生成过程必须严格符合模型要求，不同模型之间的输入处理流程可能存在显著差异，不能混用。**

以下为数据预处理的示例代码：

```python
def get_onnx_input(img_path,mean,std,model_input_size):
    # 读取图片，图片数据一般是RGB三通道，颜色范围为[0, 255.0]
    image_fp32=cv2.imread(img_path)
    # 如果模型输入要求是RGB的，则转换为RGB格式，如果要求是BGR的，则不需要转换
    image_fp32=cv2.cvtColor(image_fp32, cv2.COLOR_BGR2RGB)
    # 缩放成模型输入大小
    image_fp32 = cv2.resize(image_fp32, (model_input_size[0], model_input_size[1]))
    # 数据类型为float32,
    image_fp32 = np.asarray(image_fp32, dtype=np.float32)
    # 数据标准化,先归一化到[0,1]范围内，然后减均值除方差
    image_fp32/=255.0
    for i in range(3):
        image_fp32[:, :, i] -= mean[i]
        image_fp32[:, :, i] /= std[i]
    # 按照模型输入要求处理成NCHW排布或者NHWC排布
    image_fp32 = np.transpose(image_fp32, (2, 0, 1))
    return image_fp32.copy()

def get_kmodel_input(img_path,mean,std,model_input_size):
    # 读取图片，图片数据一般是RGB三通道，颜色范围为[0, 255.0]
    image_uint8=cv2.imread(img_path)
    # 如果模型输入要求是RGB的，则转换为RGB格式，如果要求是BGR的，则不需要转换
    image_uint8=cv2.cvtColor(image_uint8, cv2.COLOR_BGR2RGB)
    # 缩放成模型输入大小
    image_uint8 = cv2.resize(image_uint8, (model_input_size[0], model_input_size[1]))
    # 数据类型为uint8,因为转换kmodel的时候开启了预处理，并且设定了标准化参数，因此这里的输入就不需要实现标准化了
    image_uint8 = np.asarray(image_uint8, dtype=np.uint8)
    # 按照模型输入要求处理成NCHW排布或者NHWC排布
    image_uint8 = np.transpose(image_uint8, (2, 0, 1))
    return image_uint8.copy()
```

在使用 ONNX 模型和 KModel 进行推理时，输入数据的预处理存在若干关键差异，主要体现在以下几个方面：

- **标准化处理**：ONNX 模型本身不包含任何预处理逻辑，因此其输入数据必须在外部完成标准化（例如减均值除标准差）。而对于 KModel，如果在模型转换阶段已配置了归一化参数（如 `mean` 和 `std`），则这部分标准化操作会被封装进模型内部，**推理前无需重复处理**。

- **数据类型差异**：ONNX 模型的输入通常为 `float32` 类型，而 KModel 的输入类型则依赖模型转换时指定的 `input_type`（例如 `uint8`）及 `input_range`。KModel 会在推理内部进行反量化处理，将整数类型还原为近似的浮点表达。

- **通道顺序处理**：若在模型转换过程中未启用 `SwapRB`（即参数为 `False`），则需要在外部预处理阶段将输入图像的通道顺序从 BGR 转换为 RGB。若 `SwapRB=True`，该通道变换操作将自动由 KModel 内部处理，**无需在外部执行**。

综合来看，ONNX 模型所需的外部预处理操作等于 KModel 的外部预处理 **加上** 内部预处理，两者的关系可表示如下：

```shell
ONNX 模型外部预处理 = KModel 外部预处理 + KModel 内部预处理
```

#### 加载onnx模型并推理

首先需要使用onnx模型完成推理，获取onnx模型的推理结果。示例代码如下：

```python
def onnx_inference(onnx_path,onnx_input_data):
    # 创建 ONNX 推理会话（加载模型）
    ort_session = ort.InferenceSession(onnx_path)
    # 获取模型输出名称列表，用于后续调用推理
    output_names = []
    model_outputs = ort_session.get_outputs()
    for i in range(len(model_outputs)):
        output_names.append(model_outputs[i].name)

    # 获取模型的输入信息
    model_input = ort_session.get_inputs()[0]             # 第一个输入（通常只有一个）
    model_input_name = model_input.name                   # 输入的名称（键）
    model_input_type = np.float32                         # 输入数据类型，这里假设是 float32
    model_input_shape = model_input.shape                 # 输入张量的形状（维度）

    # 处理输入数据,需确保和模型输入形状一致
    model_input_data = onnx_input_data.astype(model_input_type).reshape(model_input_shape)

    # 执行推理，传入输入名称和数据，返回所有输出结果
    onnx_results = ort_session.run(output_names, { model_input_name : model_input_data })
    return onnx_results
```

#### 加载kmodel模型并推理

然后使用转换成功的kmodel进行推理，获得kmodel的推理结果。示例代码如下：

```python
def kmodel_inference(kmodel_path,kmodel_input_data,model_input_size):
    # 初始化nncase 模拟器
    sim = nncase.Simulator()
    # 读取kmodel
    with open(kmodel_path, 'rb') as f:
        kmodel = f.read()
    # 加载kmodel
    sim.load_model(kmodel)
    # 读取输入数据
    input_shape = [1, 3, model_input_size[1], model_input_size[0]]
    dtype = sim.get_input_desc(0).dtype
    # 处理输入数据,需确保和模型输入形状一致
    kmodel_input = kmodel_input_data.astype(dtype).reshape(input_shape)
    # 设置模拟器输入tensor,此处为单输入
    sim.set_input_tensor(0, nncase.RuntimeTensor.from_numpy(kmodel_input))
    # 模拟器推理kmodel模型
    sim.run()
    # 获取推理输出
    kmodel_results = []
    for i in range(sim.outputs_size):
        kmodel_result = sim.get_output_tensor(i).to_numpy()  # 转换为numpy数组
        kmodel_results.append(kmodel_result)  # 保存到列表中
    return kmodel_results
```

#### 计算输出的余弦相似度

得到onnx模型和kmodel模型的推理结果后，逐个计算每个输出的余弦相似度。一般相似度在0.99以上可以认为该模型转换成功，可部署使用。示例代码如下：

```python
def cosine_similarity(onnx_results,kmodel_results):
    output_size=len(kmodel_results)
    # 将每个输出展成一维，然后计算余弦相似度
    for i in range(output_size):
        onnx_i=np.reshape(onnx_results[i], (-1))
        kmodel_i=np.reshape(kmodel_results[i], (-1))
        cos = (onnx_i @ kmodel_i) / (np.linalg.norm(onnx_i, 2) * np.linalg.norm(kmodel_i, 2))
        print('output {0} cosine similarity : {1}'.format(i, cos))
    return
```

## 模型部署

```{note}
👉 前面我们把kmodel模型转好了、也验证过了，接下来当然就是———**上板子跑起来啦！** 这一章我们就来聊聊怎么在 K230 的 Linux 环境下，用提供的 nncase runtime API 把模型加载进来并实现推理。

那问题来了：模型是有了，那输入数据要怎么准备？我们要根据模型的“口味”对输入图像做一些处理，比如尺寸、格式、归一化等等，确保它能“吃得对”。然后把处理好的数据喂进去，让模型开始推理。推理完之后，模型会给我们一堆“输出结果”，这些结果是啥意思？我们还得做一番解析，比如拿出类别、坐标这些有用的信息。

最后嘛，当然不能藏着掖着！我们会把这些识别出来的内容显示在屏幕上，比如画框、标数字，让整个流程从图像采集、模型推理，到结果展示**一气呵成、全流程跑通**！

这一章就会带你把这个完整过程搞明白，让模型真的开始“动起来”～
```

对于一个实用的 AI 程序，不仅包括模型推理，还包括有图像输入、前后处理程序、结果显示等不同模块。下图展示了一个典型的AI应用程序的完整框图：

![deploy_pipeline](https://www.kendryte.com/api/post/attachment?id=650)

`k230_linux_sdk`中摄像头和显示部分使用`v4l2`和`drm`做了集成。V4L2（Video for Linux 2）是 Linux 的视频采集标准接口，用于管理摄像头、视频输入设备,主要用于提供AI推理模型的输入数据。DRM (Direct Rendering Manager) 是 Linux 内核中管理显示输出的 显示/显存控制子系统，主要职责包括管理显存（framebuffer）、控制显示管线（CRTC、plane、encoder、connector）、提供 KMS（Kernel Mode Setting） 接口进行图像显示控制、支持 2D/3D 硬件加速渲染（通过 GPU 驱动）。

🚀 部署流程讲解：部署其实可以理解为“让模型真正工作起来”的过程，下面我们按照流程，分步介绍。

**1️⃣ 获取图像数据（输入数据源）**
我们先得拿到一张图像，通常是从摄像头中实时采集，也可以从本地加载一张测试图片。拿到图像后，可以使用图像的数据指针创建一个`runtime_tensor`。在 K230 开发板上，通常你会通过 `v4l2_drm_dump` 接口来获取一帧数据，并从虚拟地址拿到数据创建`runtime_tensor`。

**2️⃣ 构造输入 Tensor（准备投喂模型的数据）**
有了图像之后，我们要把它“打包”成模型能处理的格式`runtime_tensor`。这一步，是为了喂给模型一个标准结构的数据。

**3️⃣ 预处理（ai2d 模块）**
模型对输入图像有特定要求，比如大小、格式、通道顺序等等。这一步我们就用 ai2d 模块把图像tensor处理成模型需要的“样子”。

**4️⃣ 模型推理（使用 KPU 推理模块）**
图像处理好后，喂进 KPU（K230 的神经网络加速模块）进行推理。KPU 会返回一个结果 tensor，这里面包含了模型的输出，比如检测框、分类概率等等。

**5️⃣ 后处理（提取有用信息）**
KPU 输出的是一堆数字，我们得把这些“干货”解析出来。比如识别到的数字是几？框在图像上的位置在哪？这些都需要用后处理算法来搞定。对 YOLO 模型来说，后处理包括置信度过滤、NMS 非极大值抑制等。

**6️⃣ 显示识别结果（可视化）**
最后一步，把识别到的内容“画”出来！我们可以在屏幕上画出检测框、数字标签等，让结果一目了然。一般会用两个图层来显示，一层是原始图像，另一层是识别结果（如框和数字），叠加显示可以保证效果更清晰也更灵活。

总结：部署的核心流程就是：拿图像 → 处理成输入 → 扔给模型 → 拿结果 → 解读结果 → 显示出来！这套流程跑通了，你的模型就等于真正“上线工作”了！🎉

💡 **固件介绍**：请参考下面文档中的步骤搭建编译环境，并编译固件，以保证**最新的特性**被支持！

### 获取输入并创建tensor

前面我们说了，模型跑起来之后，需要输入数据才能开始推理对吧？那这些图像数据从哪儿来呢？这节我们就来聊聊——**图像是怎么来的，又是怎么一步步变成模型能“吃”的格式的！**

图像来源其实有两种方式：可以用板子上提前放好的本地图片（比如你事先拷进去的测试图），也可以用板载的 MIPI 摄像头拍摄实时画面。不管你选哪种方式，最终我们都要拿到一个 **RGB888P格式的数据指针**——这个就像是“原材料”。如果得到的数据格式不符合，还需要使用一些模块进行转换。

```{note}
👉 **`RGB888` 和 `RGB888P`** 的区别主要在于 **像素数据在内存中的排列方式**。

**RGB888格式**：每个像素的 R、G、B 三个分量直接连续存放在一起，数据排布为`HWC`。
**内存布局**：

[R0][G0][B0]  [R1][G1][B1]  [R2][G2][B2]  ...
[Rw][Gw][Bw]  ...

每个像素占 **3 字节**（8 位 R + 8 位 G + 8 位 B = 24 位）。

**RGB888P格式**：将所有 R 分量放在一起、所有 G 分量放在一起、所有 B 分量放在一起，数据排布为`CHW`。
**内存布局**：
[R0][R1][R2]...[Rn]    ← 全部红色分量
[G0][G1][G2]...[Gn]    ← 全部绿色分量
[B0][B1][B2]...[Bn]    ← 全部蓝色分量

每个分量的内存块大小都是 `width × height` 字节。

因此如何创建输入`tensor`，需要根据转换模型时`nncase.CompileOptions`的`input_layout`确定，或者使用`netron`查看`onnx`模型的输入排布顺序。
```

拿到图像之后，我们还不能直接送给模型。我们用 `nncase::runtime` 模块提供的 API，把这个数组转成 **runtime_tensor（张量）**。这时候数据就“打包”好了，可以安心送进模型做推理了！

那什么是 tensor 呢？你可以把它想象成是模型能听懂的“语言”——它就像一个装数据的盒子，模型吃进去的是 tensor，推理之后吐出来的结果也是 tensor。在 `nncase::runtime` 模块里，这个东西被封装成了 `runtime_tensor`，你只要按照要求构造好，就能直接用了。

![create_tensor](https://www.kendryte.com/api/post/attachment?id=661)

上图说明了在获取输入图像并创建tensor的过程。模型推理输入为`runtime_tensor`类型，可以从某一个数据指针创建。

常用的输入数据源包括：

- 图片文件
- MIPI摄像头

本节就这两种输入数据来源进行详细介绍。
  
#### 图片文件输入

从开发板读入一张图片数据，创建`cv::Mat`实例，并从`cv::Mat实例的data指针`创建`runtime tensor`实例。示例代码如下，`opencv`读入一张图，`cv::Mat`默认实例是`BGR HWC格式`，首先将其转换成`RGB CHW`格式，然后创建一个空的tensor，并映射出Host端的可写内存区域，拷贝数据到张量内，然后同步到设备中：

```cpp
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <nncase/runtime/interpreter.h>
#include <nncase/runtime/runtime_op_utility.h>
#include "scoped_timing.h"

using namespace std;
using namespace nncase::runtime;

/**
 * @brief 单张/帧图片大小
 */
typedef struct FrameCHWSize
{
    int channel;
    int height; // 高
    int width;  // 宽
} FrameCHWSize;

std::string image_path = "/mnt/test.jpg";
// 读取图片
cv::Mat ori_img = cv::imread(image_path);
FrameCHWSize image_size={ori_img.channels(),ori_img.rows,ori_img.cols};
// 创建一个空的向量，用于存储chw图像数据,将读入的hwc数据转换成chw数据
std::vector<uint8_t> chw_vec;
std::vector<cv::Mat> bgrChannels(3);
cv::split(ori_img, bgrChannels);
for (auto i = 2; i > -1; i--)
{
    std::vector<uint8_t> data = std::vector<uint8_t>(bgrChannels[i].reshape(1, 1));
    chw_vec.insert(chw_vec.end(), data.begin(), data.end());
}
// 创建tensor
dims_t in_shape { 1, 3, ori_img.rows, ori_img.cols };
runtime_tensor input_tensor = host_runtime_tensor::create(typecode_t::dt_uint8, in_shape, hrt::pool_shared).expect("cannot create input tensor");
auto input_buf = input_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_write).unwrap().buffer();
memcpy(reinterpret_cast<char *>(input_buf.data()), chw_vec.data(), chw_vec.size());
hrt::sync(input_tensor, sync_op_t::sync_write_back, true).expect("write back input failed");
```
  
#### MIPI视频流输入

k230 vvcam模块负责图像采集和数据处理，支持MIPI接口摄像头。MIPI摄像头可以通过v4l2框架的接口采集图像数据，将采集到的图像数据转换为`runtime_tensor`类型，供kmodel模型推理使用。

每个MIPI摄像头最多可以出3路图像通道（各路通道可以具有不同分辨率或不同格式）。
这里我们采用一路通道输出作为示例，数据处理流程图下图所示：

![1_chn_process](https://www.kendryte.com/api/post/attachment?id=613)

模型推理过程中的输入数据也可以来自MIPI摄像头的视频流，为了保证输出数据为CHW排布的RGB格式数据，我们一般指定摄像头流出数据格式为`v4l2_fourcc('B', 'G', '3', 'P');`。配置vvcam设备出图的代码如下，下述代码为伪代码，不可实际运行：

```cpp
// 定义ISP出图分辨率和单通道的出图分辨率
#define SENSOR_WIDTH 640
#define SENSOR_HEIGHT 360
#define SENSOR_CHANNEL 3
#define BUFFER_NUM 3

struct v4l2_drm_context context;
struct v4l2_drm_video_buffer buffer;

v4l2_drm_default_context(&context);
context.device = video_device;
context.display = false;
context.width = SENSOR_WIDTH;
context.height = SENSOR_HEIGHT;
context.video_format = v4l2_fourcc('B', 'G', '3', 'P');
context.buffer_num = BUFFER_NUM;
if (v4l2_drm_setup(&context, 1, NULL)) {
    cerr << "v4l2_drm_setup error" << endl;
    return;
}
if (v4l2_drm_start(&context)) {
    cerr << "v4l2_drm_start error" << endl;
    return;
}
```

完成上述配置后，调用接口`v4l2_drm_dump(&context, 1000)`即可从`context.buffers[0].mmap`中获取一帧图像数据，该数据为`SENSOR_CHANNEL x SENSOR_HEIGHT x SENSOR_WIDTH`的CHW格式RGB数据。

🏷️ **双通道采图**

在边缘设备上执行 AI 模型推理时，由于模型计算量较大，**推理过程通常较耗时**，耗时范围从几毫秒到数百毫秒不等。若采用单通道处理流程：

```text
图像采集 → 格式转换 → 数据预处理 → 模型推理 → 结果后处理 → 原图绘制 → 图像显示
```

这种串行执行方式会导致图像显示延迟较高，尤其是当模型较大或系统资源有限时，画面更新明显变慢，影响用户体验。

为了解决这一问题，**推荐使用双通道处理架构**，即采用“**一通道用于实时显示，另一通道用于模型推理**”的异步处理策略。该架构通过并行处理图像采集与模型推理，有效减少了显示延迟，提升了画面流畅性。双通道处理机制如下：

- **显示通道**：直接采集图像并推送至屏幕，实现低延迟的实时画面显示，该路数据可以使用绑定的方式实现。
- **推理通道**：独立采集图像并执行完整的 AI 推理流程（包括格式转换、预处理、模型推理与后处理）。
- **OSD 图层合成**：将模型推理结果（如检测框、关键点等）绘制为 OSD 图层，并通过硬件叠加与原始图像合成后再输出显示。

虽然推理结果在视觉上会存在一定延迟（即上一帧的检测框显示在当前帧图像上），但整体画面连续性更好，用户体验更加流畅。

![2_chn_process](https://www.kendryte.com/api/post/attachment?id=665)

双通道彩图模式的伪代码如下，下述代码无法直接运行，仅用于说明：

```cpp
#define SENSOR_WIDTH 640
#define SENSOR_HEIGHT 360
#define SENSOR_CHANNEL 3

static std::mutex result_mutex;

std::atomic<bool> ai_stop(false);
// 显示线程退出标志
std::atomic<bool> display_stop(false);
static volatile unsigned kpu_frame_count = 0;
static struct timeval tv, tv2;
// 显示实例和OSD缓冲区
static struct display* display;
struct display_buffer* draw_buffer;
cv::Mat draw_frame;

/**
 * @brief AI 推理处理线程函数
 **/
static void ai_proc(char *argv[], int video_device) {
    struct v4l2_drm_context context;
    struct v4l2_drm_video_buffer buffer;
    #define BUFFER_NUM 3

    /**
    * 等待display_proc运行，确保display drm设备已初始化
    **/
    result_mutex.lock();
    result_mutex.unlock();

    v4l2_drm_default_context(&context);
    context.device = video_device;
    context.display = false;
    context.width = SENSOR_WIDTH;
    context.height = SENSOR_HEIGHT;
    context.video_format = v4l2_fourcc('B', 'G', '3', 'P');
    context.buffer_num = BUFFER_NUM;
    if (v4l2_drm_setup(&context, 1, NULL)) {
        cerr << "v4l2_drm_setup error" << endl;
        return;
    }
    if (v4l2_drm_start(&context)) {
        cerr << "v4l2_drm_start error" << endl;
        return;
    }


    /**
    * 这里添加模型初始化，加载模型，应用类实例化代码
    **/

    
    std::vector<std::tuple<int, void*>> tensors;
    for (unsigned i = 0; i < BUFFER_NUM; i++) {
        tensors.push_back({context.buffers[i].fd, context.buffers[i].mmap});
    }
    SensorBufManager sensor_buf = SensorBufManager({SENSOR_CHANNEL, SENSOR_HEIGHT, SENSOR_WIDTH},tensors);
    
    while (!ai_stop) {
        int ret = v4l2_drm_dump(&context, 1000);
        if (ret) {
            perror("v4l2_drm_dump error");
            continue;
        }

        // 从这里可以获取帧数据创建tensor
        void* frame_data=context.buffers[0].mmap;

        
        /**
        * 输入预处理、模型推理、输出后处理，绘制结果可以在frame_handler中处理，也可以在这里绘制然后将整个cv::Mat拷贝到申请的plane缓冲；
        **/

        v4l2_drm_dump_release(&context);
    }
    v4l2_drm_stop(&context);
}

/**
 * @brief V4L2-DRM 显示帧处理函数（每帧触发一次）
 *
 * 该函数由 v4l2_drm_run 驱动循环回调，在每一帧显示数据时被调用。主要功能用于显示AI推理的结果。
 * @param context V4L2-DRM 上下文结构体指针
 * @param displayed 表示该帧是否已经被实际显示
 * @return 返回 0 表示正常，返回 'q' 表示请求退出主循环（受控于 display_stop 标志）
 */
int frame_handler(struct v4l2_drm_context *context, bool displayed) 
{
    static bool first_frame = true;
    if (first_frame) {
        result_mutex.unlock();
        first_frame = false;
    }

    static unsigned response = 0, display_frame_count = 0;
    response += 1;
    if (displayed) 
    {
        if (context[0].buffer_hold[context[0].wp] >= 0) 
        {
            static struct display_buffer* last_drawed_buffer = nullptr;
            auto buffer = context[0].display_buffers[context[0].buffer_hold[context[0].wp]];
            if (buffer != last_drawed_buffer) {
                //---------------------- 绘制显示结果 ----------------------
                if (draw_buffer->width > draw_buffer->height)
                {
                    // 创建临时 BGRA 显示缓冲Mat（用于画图）
                    cv::Mat temp_img(draw_buffer->height, draw_buffer->width, CV_8UC4);
                    // 横屏
                    temp_img.setTo(cv::Scalar(0, 0, 0, 0));
                    result_mutex.lock();
                    draw_frame.copyTo(temp_img);
                    result_mutex.unlock();
                    //---------------------- 显示缓冲同步 ----------------------
                    // 将绘图图像复制到实际显示缓冲区
                    memcpy(draw_buffer->map, temp_img.data, draw_buffer->size);
                }
                else
                {
                    // 竖屏
                    // 创建临时 BGRA 显示缓冲Mat（用于画图）
                    cv::Mat temp_img(draw_buffer->width, draw_buffer->height, CV_8UC4);
                    // 竖屏st7701：横图绘制，然后转回竖图给display显示
                
                    temp_img.setTo(cv::Scalar(0, 0, 0, 0));
                    result_mutex.lock();
                    draw_frame.copyTo(temp_img);
                    result_mutex.unlock();
                    // 旋转回屏幕方向
                    cv::rotate(temp_img, temp_img, cv::ROTATE_90_CLOCKWISE);
                    //---------------------- 显示缓冲同步 ----------------------
                    // 将绘图图像复制到实际显示缓冲区
                    memcpy(draw_buffer->map, temp_img.data, draw_buffer->size);
                }
                last_drawed_buffer = buffer;
                // flush cache
                thead_csi_dcache_clean_invalid_range(draw_buffer->map, draw_buffer->size);
                display_update_buffer(draw_buffer, 0, 0);
            }
        }
        display_frame_count += 1;
    }

    // FPS counter
    gettimeofday(&tv2, NULL);
    uint64_t duration = 1000000 * (tv2.tv_sec - tv.tv_sec) + tv2.tv_usec - tv.tv_usec;
    if (duration >= 1000000) {
        fprintf(stderr, " poll: %.2f, ", response * 1000000. / duration);
        response = 0;
        if (display) {
            fprintf(stderr, "display: %.2f, ", display_frame_count * 1000000. / duration);
            display_frame_count = 0;
        }
        fprintf(stderr, "camera: %.2f, ", context[0].frame_count * 1000000. / duration);
        context[0].frame_count = 0;
        fprintf(stderr, "KPU: %.2f", kpu_frame_count * 1000000. / duration);
        kpu_frame_count = 0;
        fprintf(stderr, "          \r");
        fflush(stderr);
        gettimeofday(&tv, NULL);
    }

    // 若收到退出信号，返回 'q' 表示主循环退出
    if (display_stop) {
        return 'q';
    }
    return 0;
}

/**
 * @brief 显示线程函数，初始化 V4L2-DRM 并绑定绘制回调
 *
 * 根据屏幕方向（横屏 / 竖屏）配置对应的宽高、格式和旋转角度，
 * 然后调用 `v4l2_drm_run()` 启动帧处理主循环，由 `frame_handler()` 每帧触发绘制。
 *
 * @param video_device 视频设备编号（如 /dev/video0 中的 1）
 */
void display_proc(int video_device) 
{
    struct v4l2_drm_context context;
    v4l2_drm_default_context(&context);
    context.device = video_device;
    // 根据屏幕方向设置 width/height/rotation
    if (display->width > display->height)
    {
        // 横屏
        context.width = display->width;
        context.height = (display->width * SENSOR_HEIGHT / SENSOR_WIDTH) & 0xfff8;
        context.video_format = V4L2_PIX_FMT_NV12;
        context.display_format = 0;
        context.drm_rotation = rotation_0;
    }
    else 
    {
        // 竖屏
        context.width = display->height;
        context.height = display->width;
        context.video_format = V4L2_PIX_FMT_NV12;
        context.display_format = 0;
        context.drm_rotation = rotation_90;
    }
    if (v4l2_drm_setup(&context, 1, &display)) {
        std::cerr << "v4l2_drm_setup error" << std::endl;
        return;
    }
    // 分配OSD显示 plane 和 buffer
    struct display_plane* plane = display_get_plane(display, DRM_FORMAT_ARGB8888);
    draw_buffer = display_allocate_buffer(plane, display->width, display->height);
    display_commit_buffer(draw_buffer, 0, 0);

    /**
    * 初始化显示Mat，用于绘制推理结果
    **/
    if (draw_buffer->width > draw_buffer->height)
    {
        draw_frame = cv::Mat(draw_buffer->height, draw_buffer->width, CV_8UC4, cv::Scalar(0,0, 0, 0));
    }
    else{
        draw_frame = cv::Mat(draw_buffer->width, draw_buffer->height, CV_8UC4, cv::Scalar(0,0, 0, 0));
    }

    /**
    * 启动V4L2-DRM显示线程，绑定帧处理回调函数
    **/
    std::cout << "press 'q' to exit" << std::endl;
    gettimeofday(&tv, NULL);
    v4l2_drm_run(&context, 1, frame_handler);
    // 清理资源
    if (display) {
        display_free_plane(plane);
        display_exit(display);
    }
    return;
}

```
  
### 图像tensor预处理

我们之前已经成功得到了图像数据，并且可以创建一个 tensor，但问题来了——这个 tensor 可能跟模型“胃口不合”。比如大小不对、颜色通道不对。这时候，就需要我们出马，把 tensor 加工一下，让它变成模型可以接受的格式。这整个处理过程就叫“预处理”，而完成这个工作的，就是我们今天的主角 —— ai2d 模块！

**🛠️ 为什么要做预处理？**
模型是“挑食”的，它只接受特定尺寸、格式的数据，比如：输入要是 320x320 大小；要是 RGB 顺序，而不是 BGR；通道在前（CHW）还是通道在后（HWC）也得对上。如果不对，就会识别错误，甚至模型直接罢工报错。

**⚡ ai2d 模块：硬件加速，飞快处理！**
ai2d 是 K230 平台上专门用于图像tensor预处理的模块，运行在硬件上，非常快，适合嵌入式实时任务。它可以帮你完成：缩放、裁剪、填充、仿射变换等操作，使得图像数据被处理成符合模型输入要求的tensor数据。

下图展示了在 K230 平台上通过 ai2d 模块进行预处理的输入输出流程和格式：

![preprocess](https://www.kendryte.com/api/post/attachment?id=653)

#### 预处理过程介绍

在部署模型时，输入图像的 `runtime_tensor` 并不一定符合模型的输入规格。例如，摄像头采集的图像尺寸可能为 `1280×720`，而模型的输入要求是 `320×320`，此时就需要对图像进行**预处理**。

预处理操作包括但不限于以下常见方式：

- **缩放（Resize）**：将原始图像调整为模型输入所需尺寸；
- **裁剪（Crop）**：保留图像的关键区域，去除冗余部分；
- **归一化（Normalization）**：将像素值映射到指定区间（如 `[0, 1]` 或 `[-1, 1]`）；
- **填充（Padding）**：为保持图像纵横比进行边缘填充，避免拉伸变形。

具体应采用哪些预处理方式，需根据 **ONNX 模型的训练预处理流程**进行对标设置。同时，在将 ONNX 模型转换为 KModel 的过程中，部分预处理步骤（如标准化、颜色通道转换等）可通过编译器参数封装进模型内部，这些操作在部署时**无需再次实现**，由 KModel 自动完成。

> ⚠️ **注意**：
> 对预处理流程需有清晰理解，尤其在进行图像**等比例填充（Aspect Ratio Padding）**时，用户可选择不同策略：
>
> - **双边填充**：在图像的上下和左右两侧均进行填充，使图像居中；
> - **单边填充**：仅在图像一侧（如上/左或下/右）填充，保持一边对齐。
>
> 不同填充方式会影响模型推理输出坐标的复原逻辑，因此在后处理阶段需要**匹配相应的坐标变换规则**，确保结果正确映射回原始图像。

#### ai2d模块介绍

在 RT-Smart 方案中，常见的图像预处理操作通常通过 `nncase的ai2d_builder` 模块由硬件加速实现。该模块支持五种主要的预处理方法，包括：

- **缩放（Resize）**
- **裁剪（Crop）**
- **填充（Pad）**
- **仿射变换（Affine）**
- **比特位右移（Shift）**

使用 `ai2d` 模块可有效降低 CPU 运算负担，提高预处理效率，适用于模型推理前的图像适配操作。下面是AI2D使用过程中的一些注意事项：

```{attention}
(1) **Affine 与 Resize 互斥**：二者不可同时启用，仅能选择其中一种进行几何变换。  
(2) **Shift 仅支持 Raw16 输入格式**，用于特定格式的高位移位操作。  
(3) **Pad Value 按通道配置**：应提供与输入图像通道数一致的列表，例如 RGB 图像需配置三个通道的填充值。  
(4) **功能执行顺序为 Crop → Shift → Resize/Affine → Pad**：配置多个预处理步骤时必须遵循此顺序。如果预处理流程不符合此顺序，建议初始化多个 `ai2d` 实例，逐步完成所需处理。
```

通过合理配置 `ai2d` 模块，可实现高效、灵活的图像预处理，以满足不同模型对输入数据的要求。

这里以**打印数字识别**任务使用的等比例缩放填充预处理过程为例，介绍`ai2d`模块的使用方法。**核心代码**(此代码仅用于说明，无法直接运行)如下：

```cpp
int input_w=1280;
int input_h=720;
int output_w=320;
int output_h=320;
// -------这两个tensor自行创建------
runtime_tensor input_tensor;
runtime_tensor output_tensor;
// -------------------------------

// 计算填充参数，这里选择单侧填充，仅在右侧和下侧做填充，先按照短边计算缩放比例，然后计算两侧填充像素宽度
float ratiow = (float)output_w / input_w;
float ratioh = (float)output_h / input_h;
float ratio = ratiow < ratioh ? ratiow : ratioh;
int new_w = (int)(ratio * input_w);
int new_h = (int)(ratio * input_h);
int top = 0;
int bottom = output_h - new_h;
int left = 0;
int right = output_w - new_w;

// 设置ai2d的参数，包括输入格式输出格式，输入数据类型输出数据类型，裁剪参数，移位参数，填充参数，缩放参数，仿射参数，使用哪种方法就将其设置为true，且配置操作参数，这里使用了resize+pad方法
ai2d_datatype_t ai2d_dtype{ai2d_format::NCHW_FMT, ai2d_format::NCHW_FMT, typecode_t::dt_uint8, typecode_t::dt_uint8};
ai2d_crop_param_t crop_param{false, 0, 0, 0, 0};
ai2d_shift_param_t shift_param{false, 0};
ai2d_pad_param_t pad_param{true, {{0, 0}, {0, 0}, {top, bottom}, {left, right}}, ai2d_pad_mode::constant, {padding[0], padding[1], padding[2]}};
ai2d_resize_param_t resize_param{true, ai2d_interp_method::tf_bilinear, ai2d_interp_mode::half_pixel};
ai2d_affine_param_t affine_param{false, ai2d_interp_method::cv2_bilinear, 0, 0, 127, 1, {0.5, 0.1, 0.0, 0.1, 0.5, 0.0}};
// 设置输入输出维度
dims_t in_shape = {1,3,input_h,input_w};
dims_t out_shape = {1,3,output_h,output_w};
// 初始化ai2d_builder实例
std::unique_ptr<ai2d_builder> ai2d_builder_; // ai2d构建器
//设置参数
ai2d_builder_.reset(new ai2d_builder(in_shape, out_shape, ai2d_dtype, crop_param, shift_param, pad_param, resize_param, affine_param));
ai2d_builder_.build_schedule();
// 执行预处理
ai2d_builder_.invoke(input_tensor,output_tensor_).expect("error occurred in ai2d running");

//最后可以从output_tensor获取处理后的数据
```

关于`ai2d`的五种预处理方法，在源码`k230_linux_sdk/buildroot-overlay/package/usage_ai2d`中给出了示例，执行目录下的`build_app.sh`既可以编译得到可执行文件，编译产物在`k230_bin`目录下，可以拷贝到开发板上执行并查看结果。
  
### KPU推理

前面我们已经把图像预处理好了，输入 tensor 也准备就绪——现在终于轮到**主角登场**啦，那就是我们的“神经网络加速单元”——**KPU**！

KPU 是 K230 上专门用来跑神经网络模型的硬件加速器，它的作用就是：**模型交给我，推理我来搞！**
不过在开始之前，我们得先告诉它：嘿，我要用哪个模型！所以你需要提前把 `.kmodel` 文件放进 K230 的板子里，然后在代码里把这个模型加载进 KPU。

接着，就要设置输入啦——我们之前用 ai2d 模块处理好的 tensor 就派上用场了，作为模型输入传给 KPU。然后，就可以让 KPU 开始飞速地跑模型啦！

模型一跑完，KPU 会把结果返回给我们，这个结果是一个 **输出 tensor**，里面就是模型推理出来的原始数据。但是这个格式人看不懂也不好用，所以我们还得做一步“翻译”，首先将输出的`tensor`映射成数据指针，从中取出输出数据，然后做后处理操作，比如判断识别出的是哪个数字、它的位置在哪儿等等。

下图是使用 KPU 实现模型推理的过程，模型推理过程包括加载模型、设置模型输入、执行模型推理、获取模型输出：

![kpu_run](https://www.kendryte.com/api/post/attachment?id=654)

KPU是一个专门用于深度学习的加速引擎，实现对神经网络模型的计算过程进行加速。该模块的API文档见链接：[nncase KPU运行时API文档](./api_reference/ai2d_runtime_api.md)。**关于KPU的应用示例，见源代码`src/rtsmart/examples/kpu_run_yolov8`**。

这里给出使用`kpu`模块进行KPU推理的核心代码（此代码仅用于说明，无法直接运行）如下：

```cpp
//假设此模型有一个输入，一个输出
runtime_tensor input_tensor;
runtime_tensor output_tensor;
const char* kmodel_path="./test.kmodel";

// 加载模型
interpreter interp;     
std::ifstream ifs(kmodel_path, std::ios::binary);
interp.load_model(ifs).expect("Invalid kmodel");
//设置输入tensor,这里只设置了一个，如果有多个，可以按照索引设置
interp.input_tensor(0, input_tensor).expect("cannot set input tensor");
//interp.input_tensor(1, input_tensor_1).expect("cannot set input tensor");

//设置输出tensor,这里只设置了一个，如果有多个，可以按照索引设置
interp.output_tensor(0, output_tensor).expect("cannot set input tensor");
//interp.output_tensor(1, output_tensor_1).expect("cannot set input tensor");

// 执行kpu推理过程
interp.run().expect("error occurred in running model");

// 获取模型输出数据的指针,可以从该指针出取数据进行后处理
auto buf = output_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_read).unwrap().buffer();
float *p_out = reinterpret_cast<float *>(buf.data());
```

对于**四类打印数字识别任务**，kpu模型推理的输出只有一个，输出shape为[1,8,2100]。输出的数据shape如下图：

![output_shape](https://www.kendryte.com/api/post/attachment?id=634)

### 后处理

模型推理已经跑完啦，KPU 给了我们一大串“数字数组”当作结果，但别高兴太早——这些数字乍一看根本不知道是什么意思。所以，接下来的工作，就是要把这些数据**翻译成人类能看懂的内容**，比如：画面里出现了哪个数字？在什么位置？这个识别结果靠不靠谱？

举个例子，我们这个“四类打印数字识别”模型的输出形状是`[1, 8, 2100]`，意思是总共有 2100 个候选框，每个框用 8 个数字来描述。具体是什么呢？前 4 个是框的位置（中心点的 X、Y 坐标，加上宽度和高度），后 4 个是四种数字（0、1、2、3）的“得分”，也就是模型对每类的判断信心。

我们要做的第一步，就是从这 4 个得分里，挑出得分最高的那个，拿到它的类别编号和对应的分数，这就代表这个框最可能是什么数字，以及模型有多确定是这个数字。

然后，再处理一下位置。模型输出的是框的“中心点 + 宽高”，但我们通常更习惯用“左上角坐标 + 右下角坐标”的方式，这样才能方便后面做 NMS 操作。

那 NMS（非极大值抑制） 是啥呢？你可以理解为“去重”。有时候模型太“热情”，对同一个数字框出好几个，我们不需要那么多——只保留得分最高的那一个，其它重叠太多的全删掉，干干净净！这一步就叫做 NMS，几乎所有目标检测的模型后处理都会有这一步，非常关键！

最后，还有个细节就是：模型是对输入尺寸做推理的，比如我们输入的是 320×320 的图像，但原图可能是别的大小，所以我们还要把这些坐标按比例“复原”到原图上，才能正确画框。

这样一通操作下来，我们就从模型输出的一堆“谜之数字”，得到了清晰的识别结果：**画面中出现了哪个数字、它在哪儿、识别有多靠谱，框框也画好了！**这一步就是传说中的“后处理”阶段，整个流程才算真正跑通了！

下图说明了后处理过程的主要工作：

![postprocess](https://www.kendryte.com/api/post/attachment?id=655)

模型推理结束后，模型的输出`tensor`被映射成`float`类型的指针。用户可以根据应用场景的需求实现后处理。比如，对YOLOv8模型的输出实现后处理得到检测框的坐标和类别信息。首先要了解输出的含义，对于[1,8,2100]的输出，8表示4个数据是坐标信息和4个类的分数，后处理过程需要找到分数最大的类别索引和类别分数，并将坐标信息使用预处理时计算的比例复原回原图尺寸，从**中心点+宽高格式**转换成**左上右下坐标格式**，然后使用置信度阈值筛掉一部分框，再使用NMS（非极大值抑制）方法筛掉冗余重叠框，最后得到的才是基于原图的检测框信息。针对**四类打印数字识别**，我们给出该任务后处理的**核心代码**（此代码仅用于说明，无法直接运行）如下：

```cpp
//定义检测框类型
typedef struct Bbox{
    cv::Rect box;
    float confidence;
    int index;
}Bbox;

// 后处理IOU计算
float get_iou_value(cv::Rect rect1, cv::Rect rect2)
{
    int xx1, yy1, xx2, yy2;
 
    xx1 = std::max(rect1.x, rect2.x);
    yy1 = std::max(rect1.y, rect2.y);
    xx2 = std::min(rect1.x + rect1.width - 1, rect2.x + rect2.width - 1);
    yy2 = std::min(rect1.y + rect1.height - 1, rect2.y + rect2.height - 1);
 
    int insection_width, insection_height;
    insection_width = std::max(0, xx2 - xx1 + 1);
    insection_height = std::max(0, yy2 - yy1 + 1);
 
    float insection_area, union_area, iou;
    insection_area = float(insection_width) * insection_height;
    union_area = float(rect1.width*rect1.height + rect2.width*rect2.height - insection_area);
    iou = insection_area / union_area;

    return iou;
}

//NMS非极大值抑制，bboxes是待处理框Bbox实例的列表，indices是NMS后剩余的bboxes框索引
void nms(std::vector<Bbox> &bboxes,  float confThreshold, float nmsThreshold, std::vector<int> &indices)
{
    sort(bboxes.begin(), bboxes.end(), [](Bbox a, Bbox b) { return a.confidence > b.confidence; });
    int updated_size = bboxes.size();
    for (int i = 0; i < updated_size; i++)
    {
        if (bboxes[i].confidence < confThreshold)
            continue;
        indices.push_back(i);
        for (int j = i + 1; j < updated_size;)
        {
            float iou = get_iou_value(bboxes[i].box, bboxes[j].box);
            if (iou > nmsThreshold)
            {
                bboxes.erase(bboxes.begin() + j);
                updated_size = bboxes.size();
            }
            else
            {
                j++;    
            }
        }
    }
}

// 模型推理结束后，进行后处理
//上一步得到的输出指针
float *p_out;
// 标签名称
std::vector<std::string> classes{"0","1","2","3"};
// 置信度阈值
float conf_thresh=0.25;
// nms阈值
float nms_thresh=0.45;
//类别数
int class_num=classes.size();

// output0 [num_class+4,(w/8)*(h/8)+(w/16)*(h/16)+(w/32)*(h/32)]
float *output0 = p_out;
// 每个框的特征长度，ckass_num个分数+4个坐标
int f_len=class_num+4;
// 根据模型的输入分辨率计算总输出框数
int num_box=((input_shapes[0][2]/8)*(input_shapes[0][3]/8)+(input_shapes[0][2]/16)*(input_shapes[0][3]/16)+(input_shapes[0][2]/32)*(input_shapes[0][3]/32));
// 申请框数据内存
float *output_det = new float[num_box * f_len];
// 将输出数据排布从[num_class+4,(w/8)*(h/8)+(w/16)*(h/16)+(w/32)*(h/32)]调整为[(w/8)*(h/8)+(w/16)*(h/16)+(w/32)*(h/32),num_class+4],方便后续处理
for(int r = 0; r < num_box; r++)
{
    for(int c = 0; c < f_len; c++)
    {
        output_det[r*f_len + c] = output0[c*num_box + r];
    }
}

// 解析每个框的信息，class_num+4为一个框，前四个数据为坐标值，后面的class_num个分数，选择分数最大的作为识别的类别，因为开始的时候做了padding+resize，所以模型推理的坐标是基于与处理后的图像的结果，要先把框的坐标使用ratio映射回原图
std::vector<Bbox> bboxes;
for(int i=0;i<num_box;i++){
    float* vec=output_det+i*f_len;
    float box[4]={vec[0],vec[1],vec[2],vec[3]};
    float* class_scores=vec+4;
    float* max_class_score_ptr=std::max_element(class_scores,class_scores+class_num);
    float score=*max_class_score_ptr;
    int max_class_index = max_class_score_ptr - class_scores; // 计算索引
    if(score>conf_thresh){
        Bbox bbox;
        // 恢复到原图比例
        float x_=box[0]/ratio*1.0;
        float y_=box[1]/ratio*1.0;
        float w_=box[2]/ratio*1.0;
        float h_=box[3]/ratio*1.0;
        int x=int(MAX(x_-0.5*w_,0));
        int y=int(MAX(y_-0.5*h_,0));
        int w=int(w_);
        int h=int(h_);
        if (w <= 0 || h <= 0) { continue; }
        bbox.box=cv::Rect(x,y,w,h);
        bbox.confidence=score;
        bbox.index=max_class_index;
        bboxes.push_back(bbox);
    }

}

//执行非最大抑制以消除具有较低置信度的冗余重叠框（NMS）
std::vector<int> nms_result;
nms(bboxes, conf_thresh, nms_thresh, nms_result);
```

上述代码给出了YOLOv8 四类打印数字识别模型的后处理步骤。
  
### 结果绘制

现在我们已经得到了识别结果啦！每个数字的“身份”和“位置”我们都知道了，接下来就是让这些结果**变得“看得见”**——也就是在图像上画出检测框、标上数字，告诉大家：“看！这里有个 1！”、“那边是个 3！”

不过，事情没那么简单——你的模型是对 320×320 的图像做的识别，但屏幕可能是 800×480、1920×1080，甚至别的尺寸。如果直接把模型的框画在屏幕上，那位置可能就全歪了！所以我们要做一件非常重要的事：**把图像坐标“映射”成屏幕坐标**，也就是说把框的位置按比例转换一下，让它在屏幕上刚刚好。

画这些识别信息的时候，我们一般不会直接动原图，而是创建一个叫做 **OSD（On-Screen Display）和屏幕一样大**的“透明图层”，就像在照片上贴了一张玻璃膜，我们就在这上面画框、标类别，不会影响底下的画面。

最后一步，就是把这个 OSD 图层和原始图像叠加在一起，一起显示到屏幕上！这样你就能清楚地看到：每个数字被识别出来了，框也画得妥妥的！

下图给出了绘制结果的流程：

![draw_result](https://www.kendryte.com/api/post/attachment?id=666)

以**四类打印数字识别**的检测框为例，我们计算得到的检测框坐标是基于输入原图分辨率的，如果要在屏幕上实现显示，我们需要将坐标等比例转换成屏幕坐标分辨率下的坐标，然后将效果绘制在初始化透明的`cv::Mat`上，然后调用`V4L2-DRM`的回调方法实现叠加显示。这里给出核心代码（此代码仅用于说明，无法直接运行）如下：

```cpp
/**
 * @brief V4L2-DRM 显示帧处理函数（每帧触发一次）
 *
 * 该函数由 v4l2_drm_run 驱动循环回调，在每一帧显示数据时被调用。主要功能用于显示AI推理的结果。
 * @param context V4L2-DRM 上下文结构体指针
 * @param displayed 表示该帧是否已经被实际显示
 * @return 返回 0 表示正常，返回 'q' 表示请求退出主循环（受控于 display_stop 标志）
 */
int frame_handler(struct v4l2_drm_context *context, bool displayed) 
{
    static bool first_frame = true;
    if (first_frame) {
        result_mutex.unlock();
        first_frame = false;
    }

    static unsigned response = 0, display_frame_count = 0;
    response += 1;
    if (displayed) 
    {
        if (context[0].buffer_hold[context[0].wp] >= 0) 
        {
            static struct display_buffer* last_drawed_buffer = nullptr;
            auto buffer = context[0].display_buffers[context[0].buffer_hold[context[0].wp]];
            if (buffer != last_drawed_buffer) {
                //---------------------- 绘制显示结果 ----------------------
                if (draw_buffer->width > draw_buffer->height)
                {
                    // 创建临时 BGRA 显示缓冲Mat（用于画图）
                    cv::Mat temp_img(draw_buffer->height, draw_buffer->width, CV_8UC4);
                    // 横屏
                    temp_img.setTo(cv::Scalar(0, 0, 0, 0));
                    result_mutex.lock();
                    draw_frame.copyTo(temp_img);
                    result_mutex.unlock();
                    //---------------------- 显示缓冲同步 ----------------------
                    // 将绘图图像复制到实际显示缓冲区
                    memcpy(draw_buffer->map, temp_img.data, draw_buffer->size);
                }
                else
                {
                    // 竖屏
                    // 创建临时 BGRA 显示缓冲Mat（用于画图）
                    cv::Mat temp_img(draw_buffer->width, draw_buffer->height, CV_8UC4);
                    // 竖屏st7701：横图绘制，然后转回竖图给display显示
                
                    temp_img.setTo(cv::Scalar(0, 0, 0, 0));
                    result_mutex.lock();
                    draw_frame.copyTo(temp_img);
                    result_mutex.unlock();
                    // 旋转回屏幕方向
                    cv::rotate(temp_img, temp_img, cv::ROTATE_90_CLOCKWISE);
                    //---------------------- 显示缓冲同步 ----------------------
                    // 将绘图图像复制到实际显示缓冲区
                    memcpy(draw_buffer->map, temp_img.data, draw_buffer->size);
                }
                last_drawed_buffer = buffer;
                // flush cache
                thead_csi_dcache_clean_invalid_range(draw_buffer->map, draw_buffer->size);
                display_update_buffer(draw_buffer, 0, 0);
            }
        }
        display_frame_count += 1;
    }

    // FPS counter
    gettimeofday(&tv2, NULL);
    uint64_t duration = 1000000 * (tv2.tv_sec - tv.tv_sec) + tv2.tv_usec - tv.tv_usec;
    if (duration >= 1000000) {
        fprintf(stderr, " poll: %.2f, ", response * 1000000. / duration);
        response = 0;
        if (display) {
            fprintf(stderr, "display: %.2f, ", display_frame_count * 1000000. / duration);
            display_frame_count = 0;
        }
        fprintf(stderr, "camera: %.2f, ", context[0].frame_count * 1000000. / duration);
        context[0].frame_count = 0;
        fprintf(stderr, "KPU: %.2f", kpu_frame_count * 1000000. / duration);
        kpu_frame_count = 0;
        fprintf(stderr, "          \r");
        fflush(stderr);
        gettimeofday(&tv, NULL);
    }

    // 若收到退出信号，返回 'q' 表示主循环退出
    if (display_stop) {
        return 'q';
    }
    return 0;
}

/**
 * @brief 显示线程主函数，初始化 V4L2-DRM 并绑定绘制回调
 *
 * 根据屏幕方向（横屏 / 竖屏）配置对应的宽高、格式和旋转角度，
 * 然后调用 `v4l2_drm_run()` 启动帧处理主循环，由 `frame_handler()` 每帧触发绘制。
 *
 * @param video_device 视频设备编号（如 /dev/video0 中的 1）
 */
void display_proc(int video_device) 
{
    struct v4l2_drm_context context;
    v4l2_drm_default_context(&context);
    context.device = video_device;
    // 根据屏幕方向设置 width/height/rotation
    if (display->width > display->height)
    {
        // 横屏
        context.width = display->width;
        context.height = (display->width * SENSOR_HEIGHT / SENSOR_WIDTH) & 0xfff8;
        context.video_format = V4L2_PIX_FMT_NV12;
        context.display_format = 0;
        context.drm_rotation = rotation_0;
    }
    else 
    {
        // 竖屏
        context.width = display->height;
        context.height = display->width;
        context.video_format = V4L2_PIX_FMT_NV12;
        context.display_format = 0;
        context.drm_rotation = rotation_90;
    }
    if (v4l2_drm_setup(&context, 1, &display)) {
        std::cerr << "v4l2_drm_setup error" << std::endl;
        return;
    }
    // 分配OSD显示 plane 和 buffer
    struct display_plane* plane = display_get_plane(display, DRM_FORMAT_ARGB8888);
    draw_buffer = display_allocate_buffer(plane, display->width, display->height);
    display_commit_buffer(draw_buffer, 0, 0);

    if (draw_buffer->width > draw_buffer->height)
    {
        draw_frame = cv::Mat(draw_buffer->height, draw_buffer->width, CV_8UC4, cv::Scalar(0,0, 0, 0));
    }
    else{
        draw_frame = cv::Mat(draw_buffer->width, draw_buffer->height, CV_8UC4, cv::Scalar(0,0, 0, 0));
    }

    std::cout << "press 'q' to exit" << std::endl;
    gettimeofday(&tv, NULL);
    v4l2_drm_run(&context, 1, frame_handler);
    // 清理资源
    if (display) {
        display_free_plane(plane);
        display_exit(display);
    }
    return;
}
```

通过上述步骤，我们基本上就完成了使用k230 Linux SDK的开发一个应用的完整步骤。用户从转模型开始，需要对模型推理的整个过程有比较好的了解。
  
### 显示设备介绍

对于显示输出，k230提供了两种显示设备，你可以选择使用`HDMI/LCD屏幕`两种方式中的一种。

🏷️ **HDMI**：设备类型为`LT9611`，可以参照API文档查看初始化时支持的分辨率、帧率、osd数目。在双通道AI推理下，一般还会创建另一个图层，将一帧和屏幕显示分辨率同样大的OSD透明图像贴在上边显示推理结果。

🏷️ **LCD**：设备类型为`ST7701`，可以参照API文档查看初始化时支持的分辨率、帧率、osd数目。在双通道AI推理下，一般还会创建另一个图层，将一帧和屏幕显示分辨率同样大的OSD透明图像贴在上边显示推理结果。

如何进行屏幕的切换呢？开发板烧录镜像上电，进入`/boot`，如果使用`hdmi`，可以不做任何操作，如果使用`lcd`，需要修改`k.dtb`，将`***-lcd.dtb`创建符号链接到`k.dtb`，命令如下：

```shell
# 带lcd的dtb文件文件为屏幕，不带的为hdmi，创建符号链接，注意替换名称
ln -s k230-***-**.dtb k.dtb

reboot
```

重新启动后，默认显示设备切换为`hdmi`或者`lcd`，根据你修改的`k.dtb`文件而定。

### 类打印数字识别部署代码

如果使用YOLO实现四类打印数字检测识别，SDK中已经为你准备好了完整代码，**不仅支持单张图片的推理**，还支持**实时视频流的连续识别**！无论你是想在静态图片上测试模型效果，还是在接入摄像头后实时检测，都可以快速上手。你只需要用前面步骤中导出的 `kmodel` 模型，配合我们提供的示例脚本，就可以轻松在 K230 开发板上部署运行啦！

如果你想验证模型在图片上的识别精度和定位效果，可以直接跑我们的 **图片识别代码**；如果你想实时体验识别过程中的“视频效果”，那就试试 **双通道视频识别代码**，看看数字出现在屏幕上的那一刻，框框是不是能精准追踪到位！

接下来你就可以大胆动手试试部署流程，感受 K230 端侧 AI 的运行效果，AI 就能读懂你拍下的数字世界！

💡 **固件介绍**：请参考下面文档中的步骤搭建编译环境，并编译固件，以保证**最新的特性**被支持！文档教程见：[固件编译](./userguide/how_to_build.md)。

#### yolo编译

进入到`src/rtsmart/examples/YOLO`目录下，执行`build_app.sh`，编译生成的固件在`k230_bin`目录下。

#### 模型文件拷贝

开发板烧录固件上电后，可以在磁盘处发现虚拟U盘`CanMV`,磁盘被分为`/sdcard`和`/data`两个分区，将转换好的`kmodel`和编译的可执行`elf文件`以及测试图片、标签文件（txt格式，每行表示一类）拷贝到开发板上某一个目录中。

#### 图片识别命令

这里给出完整的**4类打印数字识别**图片推理命令，您可以使用上面步骤得到的kmodel进行测试：

```shell
./yolo.elf -model_type yolov5 -task_type detect -task_mode image -image_path test.jpg -kmodel_path best.kmodel -labels_txt_filepath number_labels.txt -conf_thres 0.35 -nms_thres 0.65 -mask_thres 0.5 -debug_mode 0
```

#### 双通道视频识别命令

这里给出完整的**4类打印数字识别**视频推理命令，您可以使用上面步骤得到的kmodel进行测试：

```shell
./yolo.elf -model_type yolov5 -task_type detect -task_mode video -kmodel_path best.kmodel -labels_txt_filepath number_labels.txt -conf_thres 0.35 -nms_thres 0.65 -mask_thres 0.5 -debug_mode 0
```

## YOLO部署

YOLO 是视觉任务中常用的模型，支持分类、检测、分割、旋转目标检测等任务。我们选择YOLO系列模型中经典的YOLOv5、YOLOv8和YOLO11为基础，封装了YOLOv5、YOLOv8和YOLO11的部署代码，方便用户快速部署YOLO模型。具体内容见链接：[YOLO应用指南](./app_develop_guide/ai_develop/yolo_deploy_doc.md)。

### YOLOv5猫狗分类

基于YOLOv5模型实现猫狗分类模型在K230上的部署。

#### YOLOv5源码及训练环境搭建

`YOLOv5` 训练环境搭建请参考[ultralytics/yolov5: YOLOv5 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/yolov5)

```shell
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

如果您已搭建好环境，请忽略此步骤。

#### 训练数据准备

请下载提供的示例数据集，示例数据集以猫狗分类为场景，使用YOLOv5完成训练。

```shell
cd yolov5
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_dataset/cat_dog.zip
unzip cat_dog.zip
```

⚠️ **windows系统请直接复制链接到浏览器下载，并解压到对应目录**。

如果您已下载好数据，请忽略此步骤。

#### 使用YOLOv5训练猫狗分类模型

在 `yolov5` 目录下执行命令，使用 `yolov5` 训练猫狗分类模型：

```shell
python classify/train.py --model yolov5n-cls.pt --data cat_dog --epochs 100 --batch-size 8 --imgsz 224 --device '0'
```

#### 转换猫狗分类kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolov5.zip` 解压到 `yolov5` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov5.zip
unzip test_yolov5.zip
```

按照如下命令，对 `runs/train-cls/exp/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
python export.py --weight runs/train-cls/exp/weights/best.pt --imgsz 224 --batch 1 --include onnx
cd test_yolov5/classify
# 将test目录下的图片换成你自己的训练数据的一部分，转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/train-cls/exp/weights/best.onnx --dataset ../test --input_width 224 --input_height 224 --ptq_option 0
cd ../../
```

💡 **模型转换脚本(to_kmodel.py)参数说明**：

| 参数名称     | 描述     | 说明                                                         | 类型  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | 目标平台 | 可选项为k230/cpu，对应k230 kpu和cpu；                         | str   |
| model        | 模型路径 | 待转换的ONNX模型路径；                                        | str   |
| dataset      | 校准图片集  | 模型转换时使用的图片数据，在量化阶段使用，可以从训练数据中取一部分                    | str   |
| input_width  | 输入宽度 | 模型输入的宽度                                             | int   |
| input_height | 输入高度 | 模型输入的高度                                             | int   |
| ptq_option   | 量化方式 | data和weights的量化方式，0为[uint8,uint8], 1为[uint8,int16], 2为[int16,uint8] | 0/1/2 |

#### 在k230上使用RT-Smart部署模型

##### 搭建编译环境

💡 **固件介绍**：请参考k230_linux文档中的步骤搭建编译环境，并编译固件，以保证**最新的特性**被支持！

##### yolo编译

在 `k230_linux_sdk` 下执行 `make menuconfig`，选择 `Target packages > canaan package > AI > yolo demo`，选择下方的`Save`->`OK`，保存后退出。这样在编译固件时就可以将yolo示例编译到固件中，烧录固件后在 `/app/yolo` 下可以找到编译好的 `yolo.elf` 可执行文件和测试文件。

如果不在编译固件时编译，您也可以选择单独编译yolos示例。进入 `k230_linux_sdk/buildroot-overlay/package/yolo` 目录下，执行 `./build_app.sh` 脚本，编译生成的 `yolo.elf` 可执行文件在 `k230_bin` 目录下，您可以将 `k230_bin` 目录拷贝到已经烧录固件的开发板中。

##### 模型文件拷贝

开发板烧录固件上电后，将转换好的`kmodel`和编译的可执行`elf文件`以及测试图片、标签文件（txt格式，每行表示一类）拷贝到开发板上某一个目录中。

##### YOLO 模块

`YOLO` 模块是基于`YOLO系列模型`开发的部署代码，实现了此类模型的部署过程，其支持的情况如下：

- 集成了 `YOLOv5、YOLOv8、YOLO11` 的三种模型；
- 支持四类任务，其中`YOLOv5`支持分类(classify)、检测(detect)、分割(segment)三种，`YOLOv8和YOLO11`支持分类(classify)、检测(detect)、分割(segment)、旋转目标检测(obb)四种任务；
- 支持两种推理模式，包括图片(image)和视频流(video)；
- 支持两种显示模式，包括`LT9611 (hdmi,1920×1080)`,`ST7701 (lcd屏幕,800×480)`；

- **参数说明**

| 参数名称               | 默认值          | 说明                                                                 |
|------------------------|----------------|----------------------------------------------------------------------|
| `-model_type`          | yolov8         | 设置模型类型，默认值为 yolov8，可选值：yolov5/yolov8/yolo11。          |
| `-task_type`           | detect         | 设置任务类型，默认值为 detect，可选值：classify/detect/segment/obb。       |
| `-task_mode`           | video          | 设置任务模式，默认值为 video，可选值：image/video |
| `-image_path`          | test.jpg       | 设置图像路径，默认值为 test.jpg。                                      |
| `-kmodel_path`         | yolov8n.kmodel | 设置 kmodel 路径，默认值为 yolov8n.kmodel。                            |
| `-labels_txt_filepath` | coco_labels.txt| 设置标签文本文件路径，默认值为 coco_labels.txt，每个标签独占一行。                        |
| `-conf_thres`          | 0.35           | 设置置信度阈值，默认值为 0.35。                                        |
| `-nms_thres`           | 0.65           | 设置非极大值抑制阈值，默认值为 0.65。                                  |
| `-mask_thres`          | 0.5            | 设置掩码阈值，默认值为 0.5。                                           |
| `-debug_mode`          | 0              | 设置调试模式，默认值为 0，可选值：0/1，0为不调试，1为调试打印。                                |

##### 部署模型实现图片推理

图片推理，请参考下述命令，**根据实际情况修改参数**；

```shell
./yolo.elf -model_type yolov5 -task_type classify -task_mode image -image_path test.jpg -kmodel_path yolov5n_cat_dog_cls.kmodel -labels_txt_filepath cat_dog_labels.txt -conf_thres 0.5 -debug_mode 0
```

##### 部署模型实现视频推理

视频推理，请参考下述命令，**根据实际情况修改参数**；

```shell
./yolo.elf -model_type yolov5 -task_type classify -task_mode video -kmodel_path yolov5n_cat_dog_cls.kmodel -labels_txt_filepath cat_dog_labels.txt -conf_thres 0.5 -debug_mode 0
```

##### 部署效果

选择两张猫狗图片使用kmodel进行分类。效果如下图：

![cat_dog_cls_res](https://www.kendryte.com/api/post/attachment?id=667)

### YOLOv8跌倒检测

基于YOLOv8模型实现跌倒检测模型在K230上的部署。

#### YOLOv8源码及训练环境搭建

`YOLOv8` 训练环境搭建请参考[ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

如果您已搭建好环境，请忽略此步骤。

#### 训练数据准备

下载提供的跌倒检测数据集，并解压。

```shell
cd yolov8
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_dataset/fall_det.zip
unzip fall_det.zip
```

⚠️ **windows系统请直接复制链接到浏览器下载，并解压到对应目录**。

如果您已下载好数据，请忽略此步骤。

#### 使用YOLOv8训练跌倒检测模型

在 `yolov8` 目录下执行命令，使用 `yolov8` 训练跌倒检测模型：

```shell
yolo detect train data=fall_det.yaml model=yolov8n.pt epochs=300 imgsz=320
```

#### 转换跌倒检测kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolov8.zip` 解压到 `yolov8` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolov8.zip
unzip test_yolov8.zip
```

按照如下命令，对 `runs/detect/train/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
yolo export model=runs/detect/train/weights/best.pt format=onnx imgsz=320
cd test_yolov8/detect
# 将test目录下的图片换成你自己的训练数据的一部分，转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/detect/train/weights/best.onnx --dataset ../test --input_width 320 --input_height 320 --ptq_option 1
cd ../../
```

💡 **模型转换脚本(to_kmodel.py)参数说明**：

| 参数名称     | 描述     | 说明                                                         | 类型  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | 目标平台 | 可选项为k230/cpu，对应k230 kpu和cpu；                              | str   |
| model        | 模型路径 | 待转换的ONNX模型路径；                                        | str   |
| dataset      | 校准图片集  | 模型转换时使用的图片数据，在量化阶段使用，可以从训练集中取一部分图片替换                   | str   |
| input_width  | 输入宽度 | 模型输入的宽度                                             | int   |
| input_height | 输入高度 | 模型输入的高度                                             | int   |
| ptq_option   | 量化方式 | data和weights的量化方式，0为[uint8,uint8], 1为[uint8,int16], 2为[int16,uint8] | 0/1/2 |

#### 在k230上使用RT-Smart部署模型

##### 搭建编译环境

💡 **固件介绍**：请参考k230_linux文档中的步骤搭建编译环境，并编译固件，以保证**最新的特性**被支持！

##### yolo编译

在 `k230_linux_sdk` 下执行 `make menuconfig`，选择 `Target packages > canaan package > AI > yolo demo`，选择下方的`Save`->`OK`，保存后退出。这样在编译固件时就可以将yolo示例编译到固件中，烧录固件后在 `/app/yolo` 下可以找到编译好的 `yolo.elf` 可执行文件和测试文件。

如果不在编译固件时编译，您也可以选择单独编译yolos示例。进入 `k230_linux_sdk/buildroot-overlay/package/yolo` 目录下，执行 `./build_app.sh` 脚本，编译生成的 `yolo.elf` 可执行文件在 `k230_bin` 目录下，您可以将 `k230_bin` 目录拷贝到已经烧录固件的开发板中。

##### 模型文件拷贝

开发板烧录固件上电后，将转换好的`kmodel`和编译的可执行`elf文件`以及测试图片、标签文件（txt格式，每行表示一类）拷贝到开发板上某一个目录中。

##### YOLO 模块

`YOLO` 模块是基于`YOLO系列模型`开发的部署代码，实现了此类模型的部署过程，其支持的情况如下：

- 集成了 `YOLOv5、YOLOv8、YOLO11` 的三种模型；
- 支持四类任务，其中`YOLOv5`支持分类(classify)、检测(detect)、分割(segment)三种，`YOLOv8和YOLO11`支持分类(classify)、检测(detect)、分割(segment)、旋转目标检测(obb)四种任务；
- 支持两种推理模式，包括图片(image)和视频流(video)；
- 支持两种显示模式，包括`LT9611 (hdmi,1920×1080)`,`ST7701 (lcd屏幕,800×480)`；

- **参数说明**

| 参数名称               | 默认值          | 说明                                                                 |
|------------------------|----------------|----------------------------------------------------------------------|
| `-model_type`          | yolov8         | 设置模型类型，默认值为 yolov8，可选值：yolov5/yolov8/yolo11。          |
| `-task_type`           | detect         | 设置任务类型，默认值为 detect，可选值：classify/detect/segment/obb。       |
| `-task_mode`           | video          | 设置任务模式，默认值为 video，可选值：image/video |
| `-image_path`          | test.jpg       | 设置图像路径，默认值为 test.jpg。                                      |
| `-kmodel_path`         | yolov8n.kmodel | 设置 kmodel 路径，默认值为 yolov8n.kmodel。                            |
| `-labels_txt_filepath` | coco_labels.txt| 设置标签文本文件路径，默认值为 coco_labels.txt，每个标签独占一行。                        |
| `-conf_thres`          | 0.35           | 设置置信度阈值，默认值为 0.35。                                        |
| `-nms_thres`           | 0.65           | 设置非极大值抑制阈值，默认值为 0.65。                                  |
| `-mask_thres`          | 0.5            | 设置掩码阈值，默认值为 0.5。                                           |
| `-debug_mode`          | 0              | 设置调试模式，默认值为 0，可选值：0/1，0为不调试，1为调试打印。                                |

##### 部署模型实现图片推理

图片推理，请参考下述命令，**根据实际情况修改参数**；

```shell
./yolo.elf -model_type yolov8 -task_type detect -task_mode image -image_path test.jpg -kmodel_path yolov8n_fall_det.kmodel -labels_txt_filepath fall_labels.txt -conf_thres 0.5 -nms_thres 0.45 -debug_mode 0
```

##### 部署模型实现视频推理

视频推理，请参考下述命令，**根据实际情况修改参数**；

```shell
./yolo.elf -model_type yolov8 -task_type detect -task_mode video -kmodel_path yolov8n_fall_det.kmodel -labels_txt_filepath fall_labels.txt -conf_thres 0.5 -nms_thres 0.45 -debug_mode 0
```

##### 部署效果

选择一张跌倒图片使用kmodel进行跌倒检测。原图和推理结果的对比如下图：

![fall_det_res](https://www.kendryte.com/api/post/attachment?id=668)

### YOLO11水果分割

#### YOLO11源码及训练环境搭建

`YOLO11` 训练环境搭建请参考[ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

如果您已搭建好环境，请忽略此步骤。

#### 训练数据准备

下载提供的水果分割数据集，并解压。

```shell
cd yolo11
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_dataset/fruit_seg.zip
unzip fruit_seg.zip
```

⚠️ **windows系统请直接复制链接到浏览器下载，并解压到对应目录**。

如果您已下载好数据，请忽略此步骤。

#### 使用YOLO11训练水果分割模型

在 `yolo11` 目录下执行命令，使用 `yolo11` 训练三类水果分割模型：

```shell
yolo segment train data=fruits_seg.yaml model=yolo11n-seg.pt epochs=100 imgsz=320
```

#### 转换水果分割kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolo11.zip` 解压到 `yolo11` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

按照如下命令，对 `runs/segment/train/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
yolo export model=runs/segment/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/segment
# test中的图片可以从训练集中选取一部分替换，转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/segment/train/weights/best.onnx --dataset ../test --input_width 320 --input_height 320 --ptq_option 1
cd ../../
```

💡 **模型转换脚本(to_kmodel.py)参数说明**：

| 参数名称     | 描述     | 说明                                                         | 类型  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | 目标平台 | 可选项为k230/cpu，对应k230 kpu和cpu；                              | str   |
| model        | 模型路径 | 待转换的ONNX模型路径；                                        | str   |
| dataset      | 校准图片集  | 模型转换时使用的图片数据，在量化阶段使用，可以从训练集中取一部分替换                    | str   |
| input_width  | 输入宽度 | 模型输入的宽度                                             | int   |
| input_height | 输入高度 | 模型输入的高度                                             | int   |
| ptq_option   | 量化方式 | data和weights的量化方式，0为[uint8,uint8], 1为[uint8,int16], 2为[int16,uint8] | 0/1/2 |

#### 在k230上使用RT-Smart部署模型

##### 搭建编译环境

💡 **固件介绍**：请参考k230_linux文档中的步骤搭建编译环境，并编译固件，以保证**最新的特性**被支持！

##### yolo编译

在 `k230_linux_sdk` 下执行 `make menuconfig`，选择 `Target packages > canaan package > AI > yolo demo`，选择下方的`Save`->`OK`，保存后退出。这样在编译固件时就可以将yolo示例编译到固件中，烧录固件后在 `/app/yolo` 下可以找到编译好的 `yolo.elf` 可执行文件和测试文件。

如果不在编译固件时编译，您也可以选择单独编译yolos示例。进入 `k230_linux_sdk/buildroot-overlay/package/yolo` 目录下，执行 `./build_app.sh` 脚本，编译生成的 `yolo.elf` 可执行文件在 `k230_bin` 目录下，您可以将 `k230_bin` 目录拷贝到已经烧录固件的开发板中。

##### 模型文件拷贝

开发板烧录固件上电后，将转换好的`kmodel`和编译的可执行`elf文件`以及测试图片、标签文件（txt格式，每行表示一类）拷贝到开发板上某一个目录中。

##### YOLO 模块

`YOLO` 模块是基于`YOLO系列模型`开发的部署代码，实现了此类模型的部署过程，其支持的情况如下：

- 集成了 `YOLOv5、YOLOv8、YOLO11` 的三种模型；
- 支持四类任务，其中`YOLOv5`支持分类(classify)、检测(detect)、分割(segment)三种，`YOLOv8和YOLO11`支持分类(classify)、检测(detect)、分割(segment)、旋转目标检测(obb)四种任务；
- 支持两种推理模式，包括图片(image)和视频流(video)；
- 支持两种显示模式，包括`LT9611 (hdmi,1920×1080)`,`ST7701 (lcd屏幕,800×480)`；

- **参数说明**

| 参数名称               | 默认值          | 说明                                                                 |
|------------------------|----------------|----------------------------------------------------------------------|
| `-model_type`          | yolov8         | 设置模型类型，默认值为 yolov8，可选值：yolov5/yolov8/yolo11。          |
| `-task_type`           | detect         | 设置任务类型，默认值为 detect，可选值：classify/detect/segment/obb。       |
| `-task_mode`           | video          | 设置任务模式，默认值为 video，可选值：image/video |
| `-image_path`          | test.jpg       | 设置图像路径，默认值为 test.jpg。                                      |
| `-kmodel_path`         | yolov8n.kmodel | 设置 kmodel 路径，默认值为 yolov8n.kmodel。                            |
| `-labels_txt_filepath` | coco_labels.txt| 设置标签文本文件路径，默认值为 coco_labels.txt，每个标签独占一行。                        |
| `-conf_thres`          | 0.35           | 设置置信度阈值，默认值为 0.35。                                        |
| `-nms_thres`           | 0.65           | 设置非极大值抑制阈值，默认值为 0.65。                                  |
| `-mask_thres`          | 0.5            | 设置掩码阈值，默认值为 0.5。                                           |
| `-debug_mode`          | 0              | 设置调试模式，默认值为 0，可选值：0/1，0为不调试，1为调试打印。                                |

##### 部署模型实现图片推理

图片推理，请参考下述命令，**根据实际情况修改参数**；

```shell
./yolo.elf -model_type yolo11 -task_type segment -task_mode image -image_path test.jpg -kmodel_path yolo11n_fruit_seg.kmodel -labels_txt_filepath fruit_labels.txt -conf_thres 0.5 -nms_thres 0.45 -mask_thres 0.5 -debug_mode 0
```

##### 部署模型实现视频推理

视频推理，请参考下述命令，**根据实际情况修改参数**；

```shell
./yolo.elf -model_type yolo11 -task_type segment -task_mode video -kmodel_path yolo11n_fruit_seg.kmodel -labels_txt_filepath fruit_labels.txt -conf_thres 0.5 -nms_thres 0.45 -mask_thres 0.5 -debug_mode 0
```

##### 部署效果

选择一张水果图片使用kmodel进行水果分割。原图和推理结果的对比如下图：

![fruit_seg_res](https://www.kendryte.com/api/post/attachment?id=669)

### YOLO11旋转目标检测

#### YOLO11源码及训练环境搭建

`YOLO11` 训练环境搭建请参考[ultralytics/ultralytics: Ultralytics YOLO 🚀 (github.com)](https://github.com/ultralytics/ultralytics)

```shell
# Pip install the ultralytics package including all requirements in a Python>=3.8 environment with PyTorch>=1.8.
pip install ultralytics
```

如果您已搭建好环境，请忽略此步骤。

#### 训练数据准备

下载桌面签字笔旋转目标检测数据集，并解压。

```shell
cd yolo11
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_dataset/pen_obb.zip
unzip pen_obb.zip
```

⚠️ **windows系统请直接复制链接到浏览器下载，并解压到对应目录**。

如果您已下载好数据，请忽略此步骤。

#### 使用YOLO11旋转目标检测模型

在 `yolo11` 目录下执行命令，使用 `yolo11` 训练单类旋转目标检测模型：

```shell
yolo obb train data=pen_obb.yaml model=yolo11n-obb.pt epochs=100 imgsz=320
```

#### 转换旋转目标检测kmodel

模型转换需要在训练环境安装如下库：

```Shell
# linux平台：nncase和nncase-kpu可以在线安装，nncase-2.x 需要安装 dotnet-7
sudo apt-get install -y dotnet-sdk-7.0
pip install --upgrade pip
pip install nncase==2.9.0
pip install nncase-kpu==2.9.0

# windows平台：请自行安装dotnet-7并添加环境变量,支持使用pip在线安装nncase，但是nncase-kpu库需要离线安装，在https://github.com/kendryte/nncase/releases下载nncase_kpu-2.*-py2.py3-none-win_amd64.whl
# 进入对应的python环境，在nncase_kpu-2.*-py2.py3-none-win_amd64.whl下载目录下使用pip安装
pip install nncase_kpu-2.*-py2.py3-none-win_amd64.whl

# 除nncase和nncase-kpu外，脚本还用到的其他库包括：
pip install onnx
pip install onnxruntime
pip install onnxsim
```

下载脚本工具，将模型转换脚本工具 `test_yolo11.zip` 解压到 `yolo11` 目录下；

```shell
wget https://kendryte-download.canaan-creative.com/developer/k230/yolo_files/test_yolo11.zip
unzip test_yolo11.zip
```

按照如下命令，对 `runs/obb/train/weights` 下的 `pt` 模型先导出为 `onnx` 模型，再转换成 `kmodel` 模型：

```shell
# 导出onnx，pt模型路径请自行选择
yolo export model=runs/obb/train/weights/best.pt format=onnx imgsz=320
cd test_yolo11/obb
# test下图片可以从训练集中选择一部分替换，转换kmodel,onnx模型路径请自行选择，生成的kmodel在onnx模型同级目录下
python to_kmodel.py --target k230 --model ../../runs/obb/train/weights/best.onnx --dataset ../test_obb --input_width 320 --input_height 320 --ptq_option 0
cd ../../
```

💡 **模型转换脚本(to_kmodel.py)参数说明**：

| 参数名称     | 描述     | 说明                                                         | 类型  |
| ------------ | -------- | ------------------------------------------------------------| ----- |
| target       | 目标平台 | 可选项为k230/cpu，对应k230 kpu和cpu；                              | str   |
| model        | 模型路径 | 待转换的ONNX模型路径；                                        | str   |
| dataset      | 校准图片集  | 模型转换时使用的图片数据，在量化阶段使用，可以从训练集中取一部分替换                    | str   |
| input_width  | 输入宽度 | 模型输入的宽度                                             | int   |
| input_height | 输入高度 | 模型输入的高度                                             | int   |
| ptq_option   | 量化方式 | data和weights的量化方式，0为[uint8,uint8], 1为[uint8,int16], 2为[int16,uint8] | 0/1/2 |

#### 在k230上使用RT-Smart部署模型

##### 搭建编译环境

💡 **固件介绍**：请参考k230_linux文档中的步骤搭建编译环境，并编译固件，以保证**最新的特性**被支持！

##### yolo编译

在 `k230_linux_sdk` 下执行 `make menuconfig`，选择 `Target packages > canaan package > AI > yolo demo`，选择下方的`Save`->`OK`，保存后退出。这样在编译固件时就可以将yolo示例编译到固件中，烧录固件后在 `/app/yolo` 下可以找到编译好的 `yolo.elf` 可执行文件和测试文件。

如果不在编译固件时编译，您也可以选择单独编译yolos示例。进入 `k230_linux_sdk/buildroot-overlay/package/yolo` 目录下，执行 `./build_app.sh` 脚本，编译生成的 `yolo.elf` 可执行文件在 `k230_bin` 目录下，您可以将 `k230_bin` 目录拷贝到已经烧录固件的开发板中。

##### 模型文件拷贝

开发板烧录固件上电后，将转换好的`kmodel`和编译的可执行`elf文件`以及测试图片、标签文件（txt格式，每行表示一类）拷贝到开发板上某一个目录中。

##### YOLO 模块

`YOLO` 模块是基于`YOLO系列模型`开发的部署代码，实现了此类模型的部署过程，其支持的情况如下：

- 集成了 `YOLOv5、YOLOv8、YOLO11` 的三种模型；
- 支持四类任务，其中`YOLOv5`支持分类(classify)、检测(detect)、分割(segment)三种，`YOLOv8和YOLO11`支持分类(classify)、检测(detect)、分割(segment)、旋转目标检测(obb)四种任务；
- 支持两种推理模式，包括图片(image)和视频流(video)；
- 支持两种显示模式，包括`LT9611 (hdmi,1920×1080)`,`ST7701 (lcd屏幕,800×480)`；

- **参数说明**

| 参数名称               | 默认值          | 说明                                                                 |
|------------------------|----------------|----------------------------------------------------------------------|
| `-model_type`          | yolov8         | 设置模型类型，默认值为 yolov8，可选值：yolov5/yolov8/yolo11。          |
| `-task_type`           | detect         | 设置任务类型，默认值为 detect，可选值：classify/detect/segment/obb。       |
| `-task_mode`           | video          | 设置任务模式，默认值为 video，可选值：image/video |
| `-image_path`          | test.jpg       | 设置图像路径，默认值为 test.jpg。                                      |
| `-kmodel_path`         | yolov8n.kmodel | 设置 kmodel 路径，默认值为 yolov8n.kmodel。                            |
| `-labels_txt_filepath` | coco_labels.txt| 设置标签文本文件路径，默认值为 coco_labels.txt，每个标签独占一行。                        |
| `-conf_thres`          | 0.35           | 设置置信度阈值，默认值为 0.35。                                        |
| `-nms_thres`           | 0.65           | 设置非极大值抑制阈值，默认值为 0.65。                                  |
| `-mask_thres`          | 0.5            | 设置掩码阈值，默认值为 0.5。                                           |
| `-debug_mode`          | 0              | 设置调试模式，默认值为 0，可选值：0/1，0为不调试，1为调试打印。                                |

##### 部署模型实现图片推理

图片推理，请参考下述命令，**根据实际情况修改参数**；

```shell
./yolo.elf -model_type yolo11 -task_type obb -task_mode image -image_path test.jpg -kmodel_path yolo11n_pen_obb.kmodel -labels_txt_filepath pen_labels.txt -conf_thres 0.5 -nms_thres 0.45 -debug_mode 0
```

##### 部署模型实现视频推理

视频推理，请参考下述命令，**根据实际情况修改参数**；

```shell
./yolo.elf -model_type yolo11 -task_type obb -task_mode video -kmodel_path yolo11n_pen_obb.kmodel -labels_txt_filepath pen_labels.txt -conf_thres 0.5 -nms_thres 0.45 -debug_mode 0
```

##### 部署效果

选择一张桌面签字笔图片使用kmodel进行旋转目标检测。原图和推理结果的对比如下图：

![pen_obb_res](https://www.kendryte.com/api/post/attachment?id=670)

## 辅助工具

### 在线训练平台

#### 云训练平台简介

Canaan开发者社区模型训练功能是为简化开发流程，提高开发效率开放的训练平台。该平台使用户关注视觉场景的落地实现，更加快捷的完成从数据标注到获得部署包中的KModel模型的过程，并在搭载嘉楠科技Kendryte®系列AIoT芯片中K230、K230D芯片开发板上进行部署。用户仅需上传数据集，简单的配置参数就可以开始训练了。

![plat](https://www.kendryte.com/api/post/attachment?id=600)

📌平台地址：**[嘉楠云训练平台](https://www.kendryte.com/zh/training/start)**

📌平台使用文档参考：**[嘉楠云训练平台文档教程](https://www.kendryte.com/web/CloudPlatDoc.html)**，请注意数据集的格式！

#### 支持任务介绍

云训练平台中对于K230系列芯片支持的视觉任务有7种，任务介绍如下表：

💡 **任务介绍**：

| 任务名称  | 任务说明                                                                                                           |
| ----- | --------------------------------------------------------------------------------------------------------------------- |
| 图像分类  | 对图片进行分类，得到图片的类别结果和分数。                                                                            |
| 图像检测  | 在图片中检测出目标物体，并给出物体的位置信息、类别信息和分数。                                                          |
| 语义分割  | 对图片中的目标区域进行分割，将图片中的不同标签区域切割出来，属于像素级任务。                                              |
| OCR检测 | 在图片中检测出文本区域，并给出文本区域的位置信息。                                                                        |
| OCR识别 | 在图片中识别出文本内容。                                                                                                |
| 度量学习  | 训练可以将图片特征化的模型，使用该模型创建特征库，通过特征对比，在不重新训练模型的前提下对新的类别进行分类，也可称为自学习。   |
| 多标签分类 | 对图片进行多类别分类，一些图片可能不只是属于某个单一的类别，天空和大海可以同时存在，得到图片的多标签分类结果。               |

#### 部署步骤

##### 部署包说明

训练结束后可以下载对应训练任务的部署包，下载的部署zip包解压后，目录如下：

```shell
📦 task_name
├── 📁 **_result
│   ├── test_0.jpg
│   ├── test_1.jpg
│   └──...
├── mp_deployment_source
├── **_image_1_2_2.py
├── **_image_1_3.py
├── **_video_1_2_2.py
├── **_video_1_3.py
└── README.pdf
```

内容如图所示：

![部署包](https://www.kendryte.com/api/post/attachment?id=657)

其中`mp_deployment_source`即是在K230镜像上部署的代码包，内部包含部署的配置文件和部署的KModel模型。注意：平台生成的配置文件`deploy_config.json`和`***.kmodel`是在k230上部署的关键,它们在各种SDK中均可用。

##### 文件拷贝

✅ **固件选择**：请参考k230 Linux sdk文档中的步骤搭建编译环境，并编译固件，以保证**最新的特性**被支持！

✅ **固件烧录**： 按照开发板类型烧录固件。

✅ **部署代码**：部署代码位于编译环境下`k230_linux_sdk/buildroot-overlay/package/cloudplat_deploy_code_linux`,需要进入该目录执行`./build.sh`完成编译，编译产物位于`k230_bin`目录下，使用方法参考该目录下的`README.md`。

##### 脚本运行

**参数配置**：

您可以在`common_files`中的`sensor_set.h`配置参数，关于参数配置的解析如下，主要用于配置屏幕显示：

|宏定义参数|说明|
|:-:|:-:|
|`SENSOR_WIDTH`|AI推理帧宽度|
|`SENSOR_HEIGHT`|AI推理帧高度|
|`SENSOR_CHANNEL`|AI推理帧通道数|

**源码编译**：

进入`k230_linux_sdk/buildroot-overlay/package/cloudplat_deploy_code_linux`目录

```shell
# 进入目录
cd cloudplat_deploy_code_linux

# 编译文件,会在k230_bin目录下得到所有的任务编译elf文件
./build.sh

# 如果只想编译某一个任务的部署文件，可以使用./build.sh <任务名>
./build.sh classification
./build.sh detection
...
```

编译产物在 `k230_bin` 目录下。

**上板部署**：

将得到的`elf文件`、字体文件和勘智训练平台得到的`kmodel`、`deploy_config.json`以及测试图片拷贝到开发板上的某一目录中，运行命令：

```shell
# 分类-视频推理，输入`q`回车退出视频推理
./classification.elf deploy_config.json None 0

# 分类-图片推理
./classification.elf deploy_config.json test.jpg 0

# 检测-视频推理，输入`q`回车退出视频推理
./detection.elf deploy_config.json None 0

# 检测-图片推理
./detection.elf deploy_config.json test.jpg 0

# 语义分割-视频推理，输入`q`回车退出视频推理
./segmentation.elf deploy_config.json None 0

# 语义分割-图片推理
./segmentation.elf deploy_config.json test.jpg 0

# OCR检测-视频推理，输入`q`回车退出视频推理
./ocr_detection.elf deploy_config.json None 0

# OCR检测-图片推理
./ocr_detection.elf deploy_config.json test.jpg 0

# OCR识别-图片推理，该任务只支持图片推理
./ocr_recognition.elf deploy_config.json test.jpg 0

# OCR-视频推理，输入`q`回车退出视频推理
./ocr.elf ocrdet_deploy_config.json ocrrec_deploy_config.json None 0

# OCR-图片推理
./ocr.elf ocrdet_deploy_config.json ocrrec_deploy_config.json test.jpg 0

# 度量学习-视频推理，输入`q`回车退出视频推理
./metric_learning.elf deploy_config.json None 0

# 度量学习-图片推理
./metric_learning.elf deploy_config.json test.jpg 0

# 多标签分类-视频推理，输入`q`回车退出视频推理
./multilabel_classification.elf deploy_config.json None 0

# 多标签分类-图片推理
./multilabel_classification.elf deploy_config.json test.jpg 0
```

##### 部署说明

- 📢 在部署模型时如果效果不理想，首先调整对应任务的阈值和推理图像的分辨率，测试结果是否可以有好转！

- 📢 学会定位问题，比如查看部署包中的`**_results`目录下的测试图片，如果该图片正常，则可能是部署代码、模型转换或者阈值的问题！

- 📢 调整模型训练的参数，比如`epoch`、`learning_rate`等，防止出现训练不充分的情况！

### AICube

#### AICube简介

AICube是嘉楠为开发者提供的离线训练工具，该平台保证了数据安全性，实现可视化的本地训练。该平台支持图像分类、目标检测、语义分割、OCR检测、OCR识别、度量学习、多标签分类、异常检测共8个任务。其相对于在线训练平台，可以保证用户使用本地的GPU实现模型训练，并将模型转换成kmodel部署在K230上。

#### 环境准备和软件安装

在安装AICube前，请关注一下前提条件是否具备：

- 带有NVIDIA GPU的设备，推荐显存8G以上；

- 计算机已安装CUDA 11.7以及以上版本，已安装CUDNN；

- 计算机已安装dotnet 7.0，并将安装路径添加到环境变量；

- 推荐计算机内存在8GB以上，硬盘剩余空间至少20GB以上；

如果您的计算机满足上述条件，可以下载AICube并解压使用。AICube提供了ubuntu版本和windows版本的安装包，因为安装包内包含了配套的**torch训练环境、多个预训练模型和示例数据集**，因此安装包较大，**请在合适的网络环境下载**，下载地址见: [AICube下载](https://www.kendryte.com/zh/resource?selected=4-2)。使用步骤请参考对应版本的用户指南。

📢 **下载时请选择最新版本下载**。

#### 支持任务介绍

AICube中对于K230系列芯片支持的视觉任务有8种，任务介绍如下表：

💡 **任务介绍**：

| 任务名称  | 任务说明                                                                                                           |
| ----- | --------------------------------------------------------------------------------------------------------------------- |
| 图像分类  | 对图片进行分类，得到图片的类别结果和分数。                                                                            |
| 图像检测  | 在图片中检测出目标物体，并给出物体的位置信息、类别信息和分数。                                                          |
| 语义分割  | 对图片中的目标区域进行分割，将图片中的不同标签区域切割出来，属于像素级任务。                                              |
| OCR检测 | 在图片中检测出文本区域，并给出文本区域的位置信息。                                                                        |
| OCR识别 | 在图片中识别出文本内容。                                                                                                |
| 度量学习  | 训练可以将图片特征化的模型，使用该模型创建特征库，通过特征对比，在不重新训练模型的前提下对新的类别进行分类，也可称为自学习。   |
| 多标签分类 | 对图片进行多类别分类，一些图片可能不只是属于某个单一的类别，天空和大海可以同时存在，得到图片的多标签分类结果。               |
|异常检测| 用于检测某类产品中的异常类别，常用于工业质检等领域。|

#### 使用说明

##### 功能页介绍

AI Cube包含5个功能页，“项目”页面主要实现项目管理功能，展示当前项目和最近项目；“图像”页面展示当前项目的数据集信息，便于用户查看数据集的图片；“拆分”页面展示拆分信息，统计拆分类别和不同拆分集的图片；“训练”页面实现训练参数配置，训练信息和训练曲线的显示；“评估”页面实现模型评估和评估信息的展示，并且可以配置部署必要参数生成部署包。

🗂️ **项目页面**图示：

![项目页面](https://www.kendryte.com/api/post/attachment?id=616)

🗂️ **图像页面**图示：

![图像页面](https://www.kendryte.com/api/post/attachment?id=617)

🗂️ **拆分页面**图示：

![拆分页面](https://www.kendryte.com/api/post/attachment?id=618)

🗂️ **训练页面**图示：

![训练页面](https://www.kendryte.com/api/post/attachment?id=619)

🗂️ **评估页面**图示：

![评估页面](https://www.kendryte.com/api/post/attachment?id=620)

##### 创建数据集

按照不同任务的数据集格式组织数据集。对应数据集格式在`项目页面`点击新建项目查看，同时我们提供了不同任务的示例数据集，在`example_dataset`目录下；并使用这些示例数据集创建了示例项目，位于`example_projects`目录下。

关于不同任务的示例数据集和示例任务，对应关系如下：

| 数据集名称     | 示例任务   | 说明                   |
| -------------- | ---------- | ---------------------- |
| vegetable_cls  | 图像分类   | 蔬菜分类场景           |
| insect         | 目标检测   | 昆虫检测场景           |
| Ocular_lesions | 语义分割   | 眼球病变区域分割场景   |
| dataset_td100  | OCR检测    | OCR文字检测场景        |
| ProductionDate | OCR识别    | 生产日期识别场景       |
| drink          | 度量学习   | 饮料瓶分类场景         |
| multilabel2000 | 多标签分类 | 自然风光多标签分类场景 |
| bottle         | 异常检测   | 瓶口异常检测场景       |

您可以使用我们提供的示例数据集，也可以自己按照`新建项目界面`对应任务格式组织您的数据集。AICube遇到的大多数问题都是数据的问题，我们只对数据集的目录结构实现了检查，并没有对数据内部的标注信息做检查，请谨慎的处理数据。

##### 创建项目

进入`项目页面`--->点击`新建项目`按钮--->选择任务类型--->导入数据集--->选择项目的存储路径--->添加项目的名称--->创建项目。

新建项目界面如下图所示：

![新建项目](https://www.kendryte.com/api/post/attachment?id=621)

项目新建完成后，会自动跳转到`图像页面`，您可以查看您的数据集详情。进入`拆分页面`，您可以按照自定义比例对数据集进行拆分，并查看拆分集的统计信息。

##### 启动训练

进入`训练页面`，在左侧配置**模型、数据增强和训练参数**。

常见参数解析：

| 平台参数名称     | 常用参数定义            | 参数含义解析                                                 |
| ---------------- | ----------------------- | ------------------------------------------------------------ |
| 模型             | model                   | 不同结构的网络模型，用于实现不同的任务；                     |
| Backbone         | model backbone          | 模型中的特征提取部分网络结构，比如检测和分割任务的模型；     |
| 是否预训练       | pretrain                | 是否加载AICube提供的预训练模型;                             |
| 预训练模型语言   | pretrain language       | **OCR识别**的特定任务参数，选择训练预训练模型的样本语言；其他任务忽略；        |
| 模型大小         | model size              | n、s、m、l、x，同一模型的变体，区别是模型尺寸，用于平衡准确率和速率； |
| 模型宽度         | model width             | 宽度越大，参数量越大;                                        |
| 图像尺寸         | model input size        | 模型输入分辨率，单值表示输入为[x,x]，双值表示输入为[x,y];    |
| ASPP空洞率       | ASPP dilation rate      | **语义分割**的特定任务参数，不同空洞卷积和池化操作的尺度，不同的空洞率进行空洞卷积可以扩大感受野，获得更广阔的的上下文信息； |
| 编码长度         | embedding length        | **度量学习**的特定任务参数，样本被向量化的向量长度；             |
| 自动数据增强     | TrivialAugment          | 无参数单图随机自动数据增强;                                  |
| 其他数据增强方法 | —                       | 亮度、对比度、饱和度、色度、锐度增强，翻转，旋转，随机缩放，随机裁剪，透视变换，高斯模糊，直方图均衡化，灰度世界算法，CutOut，Random Erasing，Mask; |
| 学习率           | learning rate           | 优化算法的参数，每次迭代的调整步长；                         |
| 迭代轮数         | epoch                   | 一个epoch是神经网络使用全部训练样本训练一次的过程；          |
| 训练批大小       | batchsize               | 每次前向和反向传播使用的样本数量；                           |
| 优化器           | optimizer               | 优化网络的时候使用的优化函数，比如SGD、Adam等；              |
| AutoAnchor       | autoanchor              | 目标检测任务中的锚框自适应；                                 |
| NMS选项          | nms option              | 目标检测任务中区别类内和类间的非极大值抑制选项；             |
| 置信度阈值       | confidience threshold   | 用于预测框类别的过滤，低于此阈值的预测框都将被删除；         |
| 交并比阈值       | IOU threshold           | 对多个重叠框进行极大值筛选，计算所有检测框的得分，依次与得分最高的检测框对比，大于此阈值的检测框被删除；OCR检测中的Box阈值类似； |
| 自动混合精度     | AMP                     | 针对不同层采用不同的数据精度，以节省显存并提高计算速度；     |
| 指数移动平均     | EMA                     | 平滑方法，防止异常值的影响，权重随时间指数递减；             |
| 早停             | Early Stopping          | 增加模型泛化性和防止过拟合的方法；                           |
| 预热策略         | WarmUp                  | 操作训练初始阶段的learning rate，使模型更快的收敛；          |
| 多尺度训练       | MST                     | 实现对不同尺度的输入图像进行训练，提高检测模型对不同大小物体的检测泛化性； |
| 损失函数         | loss function           | 用于评估模型预测值和真实值的差距程度，损失越小，模型性能越好； |
| 学习率调度       | learning rate scheduler | 学习率调整策略，训练过程中动态的调整学习率以适应梯度下降过程，包括StepLR、CosineAnnealingLR、LinearLR、MultiStepLR等； |
| 损失刷新步长     | loss refresh step       | 界面Loss曲线绘制频率，以batch为单位；                        |
| GPU索引          | gpu index               | 显卡索引；                                                 |

按照不同的任务配置好对应参数后，可以点击`增强样本按钮`查看经过数据增强的部分示例样本；点击`学习率曲线`可以查看不同的学习率策略导致的学习率变化；点击`开始训练按钮`，训练的信息会在右上方面板显示，损失曲线和指标曲线会在中间位置绘制；示例样本的预测结果会在右下面板迭代显示每个epoch的变化。训练时界面如下图：

![训练过程](https://www.kendryte.com/api/post/attachment?id=619)

##### 模型测试

进入`评估页面`，选择训练好的模型，然后选择测试方式。测试方式如下：

| 测试方式     | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| 测试集测试   | 对拆分得到的测试集进行测试评估，输出测试指标数据；           |
| 额外数据测试 | 使用和训练数据集相同格式的带标注数据进行测试，输出测试指标数据； |
| 图像目录测试 | 只选择使用训练的模型和参数对图片目录下的所有无标注样本进行推理，无测试指标； |

点击“开始测试”按钮，进行测试，测试结束后，根据评估指标查看您的模型性能；双击测试数据列表的条目可以查看推理结果大图。

##### 模型部署

如果模型的性能符合您的需求，您可以在芯片适配面板配置部署参数，主要是模型的输入分辨率和一些基础参数，点击`部署按钮`生成部署包。

![部署包生成](https://www.kendryte.com/api/post/attachment?id=622)

部署产物生成后您可以在当前项目的根目录下找到如下文件，我们主要使用`kmodel`和配置文件`deploy_config.json`：

```shell
📦 task_name
├── 📁 cpp_deployment_source
├── 📁 mp_deployment_source
└── README.md
```

![项目文件](https://www.kendryte.com/api/post/attachment?id=623)

其中`mp_deployment_source`目录是在K230方案上部署的资源，包含Kmodel文件和部署配置文件！**我们其实需要的只是其中的配置文件`deploy_config.json`和模型文件`***.kmodel`**，将该目录拷贝到开发板上。

#### 部署步骤

##### 部署包说明

训练结束后可以得到对应训练任务的部署产物。

##### 文件拷贝

✅ **固件选择**：请参考k230 linux sdk文档中的步骤搭建编译环境，并编译固件，以保证**最新的特性**被支持！

✅ **固件烧录**： 按照开发板类型烧录固件。

✅ **部署代码**：部署代码位于编译环境下`k230_linux_sdk/buildroot-overlay/package/cloudplat_deploy_code_linux`,需要进入该目录执行`./build.sh`完成编译，编译产物位于`k230_bin`目录下，使用方法参考该目录下的`README.md`。

##### 脚本运行

**参数配置**：

**源码编译**：

您可以在`common_files`中的`sensor_set.h`配置参数，关于参数配置的解析如下，主要用于配置屏幕显示：

|宏定义参数|说明|
|:-:|:-:|
|`SENSOR_WIDTH`|AI推理帧宽度|
|`SENSOR_HEIGHT`|AI推理帧高度|
|`SENSOR_CHANNEL`|AI推理帧通道数|

**源码编译**：

进入`k230_linux_sdk/buildroot-overlay/package/cloudplat_deploy_code_linux`目录

```shell
# 进入目录
cd cloudplat_deploy_code_linux

# 编译文件,会在k230_bin目录下得到所有的任务编译elf文件
./build.sh

# 如果只想编译某一个任务的部署文件，可以使用./build.sh <任务名>
./build.sh classification
./build.sh detection
...
```

编译产物在 `k230_bin` 目录下。

**上板部署**：

将得到的`elf文件`、字体文件和勘智训练平台得到的`kmodel`、`deploy_config.json`以及测试图片拷贝到开发板上的某一目录中，运行命令：

```shell
# 分类-视频推理，输入`q`回车退出视频推理
./classification.elf deploy_config.json None 0

# 分类-图片推理
./classification.elf deploy_config.json test.jpg 0

# 检测-视频推理，输入`q`回车退出视频推理
./detection.elf deploy_config.json None 0

# 检测-图片推理
./detection.elf deploy_config.json test.jpg 0

# 语义分割-视频推理，输入`q`回车退出视频推理
./segmentation.elf deploy_config.json None 0

# 语义分割-图片推理
./segmentation.elf deploy_config.json test.jpg 0

# OCR检测-视频推理，输入`q`回车退出视频推理
./ocr_detection.elf deploy_config.json None 0

# OCR检测-图片推理
./ocr_detection.elf deploy_config.json test.jpg 0

# OCR识别-图片推理，该任务只支持图片推理
./ocr_recognition.elf deploy_config.json test.jpg 0

# OCR-视频推理，输入`q`回车退出视频推理
./ocr.elf ocrdet_deploy_config.json ocrrec_deploy_config.json None 0

# OCR-图片推理
./ocr.elf ocrdet_deploy_config.json ocrrec_deploy_config.json test.jpg 0

# 度量学习-视频推理，输入`q`回车退出视频推理
./metric_learning.elf deploy_config.json None 0

# 度量学习-图片推理
./metric_learning.elf deploy_config.json test.jpg 0

# 多标签分类-视频推理，输入`q`回车退出视频推理
./multilabel_classification.elf deploy_config.json None 0

# 多标签分类-图片推理
./multilabel_classification.elf deploy_config.json test.jpg 0
```

##### 部署说明

- 📢 在部署模型时如果效果不理想，首先调整对应任务的阈值和推理图像的分辨率，测试结果是否可以有好转！

- 📢 学会定位问题，比如查看AICube模型评估的结果，如果该图片正常，则可能是部署代码、模型转换或者阈值的问题，您可以选择调整量化方式或者调整部署参数进行优化！

- 📢 AICube存在大量的训练参数，对深度学习了解的用户可以根据可能的优化方向调整训练参数，调整模型训练的参数实现重新训练转换！

## FAQ
  
### 开发过程中如何查找问题所在？

📝 首先根据不同的阶段和错误采取不同的方法：

- 如果模型转换阶段出现错误，可能是转换代码存在问题，需要阅读nncase的使用方法，调整转换代码；
- 如果模型转换成功，但是效果不及预期，可以考虑调整阈值、更改模型转换的量化方式、训练时调整训练参数；
- 如果模型转换成功，但是帧率较低，可以考虑更换更轻量的模型或者降低模型输入分辨率；
- 如果部署报错，请查看部署代码报错行数，根据API文档查找报错原因，调整代码；

### nncase支持哪些算子？

📝 nncase支持的onnx算子和tflite算子见链接：[onnx算子支持](https://github.com/kendryte/nncase/blob/master/docs/onnx_ops.md) 和 [tflite算子支持](https://github.com/kendryte/nncase/blob/master/docs/tflite_ops.md)

### 在转换模型时报错“ImportError: DLL load failed while importing _nncase”

📝 请参考如下链接的解决方法：[ImportError: DLL load failed while importing _nncase](https://github.com/kendryte/nncase/issues/451)

### 转换模型时报错“RuntimeError: Failed to initialize hostfxr”

📝 请安装dotnet-sdk-7.0， 请不要再Anaconda虚拟环境中安装dotnet-sdk。

Linux:

```shell
sudo apt-get update
sudo apt-get install dotnet-sdk-7.0
If you still have problems after installation, maybe you install dotnet in a virtual enviroment, set the environment variables. dotnet error
export DOTNET_ROOT=/usr/share/dotnet
```

Windows: 请参考微软官方网站。

### 在线训练平台和AICube的区别？

📝 在线训练平台的使用云端算力，资源紧张时需要排队，同时参数配置比较简单，一键训练，灵活性较低；AICube使用本地私人算力，环境和参数配置比较复杂，灵活性高。他们的目的都是获得kmodel和配置文件，使用固件中的`k230_linux_sdk/buildroot-overlay/package/cloudplat_deploy_code_linux`的代码编译即可实现部署。

### YOLO库中支持哪些任务？

📝 YOLOv5支持分类、检测、分割三类任务，YOLOv8和YOLO11支持分类、检测、分割和旋转目标检测四类任务。

### 如何获取支持？

📝 在开发过程中遇到问题，您可以前往嘉楠开发者社区问答论坛发帖提问。论坛地址：[Canaan问答论坛](https://www.kendryte.com/answer/)。

## 附录

### API

K230 Linux SDK文档见链接：[K230 Linux SDK文档](https://www.kendryte.com/zh/sdkResource/230linux)

### KTS

`K230_training_scripts（KTS）`是实现的端到端的训练处理过程，但是该项目的代码是基于双系统C++开发的，您可以使用该工具获取kmodel。项目地址：[K230_training_scripts](https://github.com/kendryte/K230_training_scripts)。
