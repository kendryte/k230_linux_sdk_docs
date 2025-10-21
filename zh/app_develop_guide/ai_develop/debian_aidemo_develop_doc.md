# K230 debian发行版AI Demo开发

## 环境准备

### SDK编译

搭建buildroot编译环境，如果已经搭建完成，可以跳过此步骤。

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

- **编译buildroot固件**

参考下面命令进行编译

```bash
make CONF=k230_canmv_01studio_defconfig 
```

>`k230_canmv_01studio_defconfig`是个例子，需要替换为正确的配置文件，比如替换为`k230_canmv_defconfig`
>
>sdk支持的所有配置文件见`buildroot-overlay/configs`目录
>
>`make CONF=k230_canmv_01studio_defconfig``  含义是使用`k230_canmv_01studio_defconfig`配置文件编译01studio开发板固件。

生成的固件在`output/k230_canmv_01studio_defconfig/images/sysimage-sdcard.img.gz`。

- **生成debian固件**

命令行切换用户权限到root，执行下述命令：

```shell
make debian
```

生成的固件在`output/k230_canmv_01studio_defconfig/images/CanMV-K230_01studio_debian_vx.x.x_nncase_v2.x.0.img.gz`，版本号会随代码更新有所区别。

### 搭建debian系统板上环境

- **烧录和屏幕切换**

编译得到debian固件后烧录到k230开发板，上电启动，并配置屏幕。进入`/boot`，如果使用`hdmi`，可以不做任何操作，如果使用`lcd`，需要修改`k.dtb`，将`***-lcd.dtb`创建符号链接到`k.dtb`，命令如下：

```shell
# 根据实际带lcd的dtb文件创建符号链接，注意替换名称
ln -s ***-lcd.dtb k.dtb

reboot
```

- **安装wget**

```shell
apt-get install wget
```

- **下载whl文件**

下载nncase runtime依赖包和k230 display依赖包，实现使用python代码完成模型推理和结果显示。

```shell
wget https://kendryte-download.canaan-creative.com/developer/common/debian_wheel/nncaseruntime_k230-2.10.0-py3-none-linux_riscv64.whl
wget https://kendryte-download.canaan-creative.com/developer/common/debian_wheel/k230_display-0.1.0-py3-none-any.whl
```

- **安装whl文件**

安装下载的whl依赖包，注意添加安装选项`--break-system-packages`

```shell
pip install nncaseruntime_k230-2.10.0-py3-none-linux_riscv64.whl --break-system-packages
pip install k230_display-0.1.0-py3-none-any.whl --break-system-packages
```

## 运行示例代码

编写python代码，并在debian系统中使用python运行示例。你可以使用常用的python库进行后处理，比如numpy和opencv，实现纯python aidemo开发。下面以yolov8的coco目标检测为例给出代码，您可以参考开发自己的应用。

示例代码如下：

```python
import numpy as np
import random
import cv2
import nncaseruntime as nn
import time
import sys
import select
import k230_display

def detect():
    """主检测函数：初始化摄像头、加载模型、执行推理、显示结果"""
    print(time.time())

    # ===============================
    # 一、检测与模型相关参数配置
    # ===============================
    confidence_thres = 0.3      # 置信度阈值（过滤低置信度目标）
    iou_thres = 0.45            # NMS（非极大值抑制）的 IoU 阈值
    kmodel_path = "yolov8n.kmodel"  # 模型文件路径
    input_size = [224, 224]     # 模型输入分辨率（宽、高）

    # 为每个类别生成随机颜色（用于绘制框）
    random.seed(0)
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(80)]

    # COCO 数据集的 80 类标签
    class_names = [
        'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
        'train', 'truck', 'boat', 'traffic light', 'fire hydrant',
        'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog',
        'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
        'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat',
        'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
        'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
        'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot',
        'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
        'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
        'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
        'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
    ]

    # ===============================
    # 二、初始化摄像头与显示
    # ===============================

    # 打开摄像头设备（索引 1）
    cap = cv2.VideoCapture(1)

    # 初始化 K230 显示设备
    k230_display.init()
    display_width = k230_display.get_width()
    display_height = k230_display.get_height()
    print("INFO: display width:", display_width, "display height:", display_height)

    # 根据显示尺寸确定图像捕获尺寸
    img_size = [max(display_width, display_height), min(display_width, display_height)]

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        raise IOError(f"无法打开摄像头索引 1")

    # 设置摄像头分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, img_size[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size[1])
    print("摄像头1初始化成功")

    # ===============================
    # 三、初始化模型与 AI2D 预处理
    # ===============================

    # 初始化 nncase 推理器和预处理引擎
    kpu = nn.Interpreter()
    ai2d = nn.AI2D()

    # 加载 YOLOv8 模型
    kpu.load_model(kmodel_path)

    # 创建一个临时输入张量用于绑定输入
    tmp_tensor = nn.RuntimeTensor.from_numpy(
        np.ones((1, 3, input_size[1], input_size[0]), dtype=np.uint8)
    )
    kpu.set_input_tensor(0, tmp_tensor)
    kpu_input_tensor = kpu.get_input_tensor(0)

    # ===============================
    # 四、计算图像缩放和填充参数（letterbox）
    # ===============================
    # 计算输入图像缩放比例，保持纵横比
    ratio = min(input_size[0] / img_size[0], input_size[1] / img_size[1])
    new_w, new_h = int(img_size[0] * ratio), int(img_size[1] * ratio)
    dw, dh = (input_size[0] - new_w), (input_size[1] - new_h)
    pad_left, pad_right = 0, int(dw)
    pad_top, pad_bottom = 0, int(dh)

    # ===============================
    # 五、配置 AI2D 预处理流水线
    # ===============================
    ai2d.set_datatype(
        nn.AI2D_FORMAT.NCHW_FMT,  # 输入格式
        nn.AI2D_FORMAT.NCHW_FMT,  # 输出格式
        np.uint8, np.uint8        # 输入输出数据类型
    )
    # 设置 resize 参数（使用 tf_bilinear 双线性插值）
    ai2d.set_resize_param(True, nn.AI2D_INTERP_METHOD.tf_bilinear, nn.AI2D_INTERP_MODE.half_pixel)
    # 设置 padding 参数（补边）
    ai2d.set_pad_param(True, [0, 0, 0, 0, pad_top, pad_bottom, pad_left, pad_right],
                       0, [114, 114, 114])  # 用灰色填充
    # 构建 AI2D pipeline（输入、输出 shape）
    ai2d.build([1, 3, img_size[1], img_size[0]], [1, 3, input_size[1], input_size[0]])

    # ===============================
    # 六、主推理循环
    # ===============================
    last_time = time.time()
    frame_count = 0
    fps = 0

    while True:
        # 获取当前时间
        time1 = time.time()

        # 从摄像头捕获一帧图像
        ret, frame = cap.read()
        if not ret:
            print("视频流结束或发生错误")
            break

        # -------------------------------
        # FPS 计算逻辑（每秒更新一次）
        # -------------------------------
        frame_count += 1
        now_time = time.time()
        if now_time - last_time >= 1.0:
            fps = frame_count / (now_time - last_time)
            last_time = now_time
            frame_count = 0

        # -------------------------------
        # 图像预处理：BGR -> RGB
        # -------------------------------
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_nchw = np.array([img_rgb.transpose((2, 0, 1))])  # 转换为 NCHW

        # -------------------------------
        # 执行 AI2D 预处理（resize + pad）
        # -------------------------------
        ai2d_input_tensor = nn.RuntimeTensor.from_numpy(img_nchw)
        ai2d.run(ai2d_input_tensor, kpu_input_tensor)

        # -------------------------------
        # 模型推理
        # -------------------------------
        kpu.run()

        # 获取模型输出
        model_output = kpu.get_output_tensor(0).to_numpy()
        predictions = model_output[0].transpose()  # (8400, 84)

        # -------------------------------
        # 后处理：YOLOv8 输出解析
        # -------------------------------
        boxes = predictions[:, :4]          # [x_center, y_center, w, h]
        class_scores = predictions[:, 4:]   # 各类别置信度

        # 取每个候选框的最大类别得分
        scores = np.max(class_scores, axis=1)
        class_ids = class_scores.argmax(axis=1)

        # 过滤低置信度目标
        mask = scores > confidence_thres
        boxes = boxes[mask]
        scores = scores[mask]
        class_ids = class_ids[mask]

        # -------------------------------
        # 边界框格式转换 (xywh → xyxy)
        # -------------------------------
        boxes_xy = boxes[:, :2] - boxes[:, 2:4] / 2
        boxes_xy = boxes_xy / ratio
        boxes_wh = boxes[:, 2:4] / ratio
        boxes_xy2 = boxes_xy + boxes_wh
        boxes = np.concatenate([boxes_xy, boxes_xy2], axis=1).astype(np.float32)
        scores = scores.astype(np.float32)

        # -------------------------------
        # 执行 NMS（非极大值抑制）
        # -------------------------------
        indices = cv2.dnn.NMSBoxes(boxes.tolist(), scores.tolist(), confidence_thres, iou_thres)

        # -------------------------------
        # 绘制检测结果
        # -------------------------------
        if len(indices) > 0:
            indices = indices.flatten()
            detections = []
            for i in indices:
                box = boxes[i]
                score = scores[i]
                class_id = class_ids[i]
                detections.append({
                    "box": box,
                    "score": score,
                    "class_id": class_id
                })

            # 绘制每个检测到的目标
            for det in detections:
                box = det["box"]
                score = det["score"]
                class_id = det["class_id"]
                x1, y1, x2, y2 = map(int, box)
                label = f"{class_names[class_id]}: {score:.2f}"

                # 绘制矩形框
                cv2.rectangle(img_rgb, (x1, y1), (x2, y2), colors[class_id], 2)

                # 绘制类别与置信度文字
                cv2.putText(img_rgb, label, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[class_id], 1)

        # -------------------------------
        # 在图像上绘制 FPS 信息
        # -------------------------------
        cv2.putText(img_rgb, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # -------------------------------
        # 缩放并显示到屏幕
        # -------------------------------
        resized_img = cv2.resize(img_rgb, (img_size[0], img_size[1]), interpolation=cv2.INTER_LINEAR)
        k230_display.show(resized_img)

        # -------------------------------
        # 键盘输入检测（非阻塞）
        # -------------------------------
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline().strip()
            if line in ('q', 'Q', 'exit'):
                print("收到退出命令")
                break

    # ===============================
    # 七、资源释放与退出
    # ===============================
    cap.release()
    k230_display.deinit()
    print("程序已退出")

# ===============================
# 主程序入口
# ===============================
if __name__ == '__main__':
    detect()
```

运行代码可以看到摄像头捕获的视频流中检测到的物体被框出，并且在框中显示物体的类别和置信度。

使用yolov8n 224×224输入的模型，使用opencv实现nms，摄像头出图和屏幕分辨率一致，但都为横向图即（800×480或1920×1080）

480×800 lcd屏幕可以达到30fps:

![lcd](https://www.kendryte.com/api/post/attachment?id=659)

1920×1080 lcd屏幕可以达到16fps:

![hdmi](https://www.kendryte.com/api/post/attachment?id=660)

> 注意：该代码是单通道流程，从获取摄像头图像->ai2d预处理->推理->后处理->绘制结果->处理图像并显示的完整流程，受到模型推理的耗时影响，模型越大，输入分辨率越大，耗时越长。
