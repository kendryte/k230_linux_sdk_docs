# 如何开发开发一个 AI Demo

## 概述

`ai_demo` 提供了各式各样的 AI 应用，那么我们如何开发一个自己的 AI 应用并在 k230 linux系统上运行呢？ 本文档将以人脸检测为例介绍如何通过已有结构开发一个应用。参考代码：`k230_linux_sdk/buildroot-overlay/package/face_detect`

## 开发步骤

### 转换kmodel

首先是要有一个`kmodel`，对于人脸检测我们就使用 `k230_linux_sdk/buildroot-overlay/package/face_detect` 中 `utils` 目录下的 `kmodel` 模型。如果你想自己训练模型，可以参考开源资料，训练得到`pt/pth`模型，然后将模型转换成`onnx/tflite`模型，然后再将模型转换成`kmodel`。 `kmodel`转换部分请参考nncase官方链接：[nncase github](https://github.com/kendryte/nncase) 或 [nncase gitee](https://gitee.com/kendryte/nncase) 。

### 编写部署代码

然后您需要使用 `kpu runtime API` 和 `ai2d runtime API` 编写部署在 K230 开发板上运行的代码。这里介绍这部分的开发步骤。

#### 已有代码结构

下面是已有的代码结构：

```shell
face_detect
├── src
│    ├── ai_base.cc                # AIBase 类实现：封装模型加载、设置输入输出，模型推理等步骤
│    ├── ai_base.h                 # AIBase 类定义，提供通用 AI 模型推理基类
│    ├── anchors_320.cc            # 320x320 输入模型对应的 anchor(先验框) 参数表
│    ├── anchors_640.cc            # 640x640 输入模型对应的 anchor(先验框) 参数表
│    ├── face_detection.cc         # FaceDetection 类实现：输入预处理、模型推理、解码输出、置信度计算、NMS与坐标变换绘制结果
│    ├── face_detection.h          # FaceDetection 类定义，继承自 AIBase 的人脸检测实现
│    ├── main.cc                   # 主程序入口
│    ├── scoped_timing.h           # ScopedTiming 定时器类：用于性能分析的计时工具
│    ├── sensor_buf_manager.cc     # 摄像头缓冲区管理实现模型输入tensor的获取和释放
│    ├── sensor_buf_manager.h      # 摄像头缓冲区管理接口定义
│    ├── sensor_set.h              # AI推理帧分辨率设置
│    ├── utils.cc                  # 通用工具函数实现：预处理方法、获取颜色等
│    └── utils.h                   # 工具函数与结构体声明
├── utils
│    ├── face_detect_image.sh      # 使用人脸检测模型对单张图片进行检测的脚本
│    ├── face_detect_video.sh      # 使用人脸检测模型对视频流/摄像头进行检测的脚本
│    ├── face_detection_320.kmodel # 人脸检测模型（320x320 输入尺寸的 KModel 格式）
│    └── test.jpg                  # 测试图片样例
├── build_app.sh                   # 一键构建脚本：编译、打包并生成可执行程序
├── CMakeLists.txt                 # CMake 构建配置文件，定义项目依赖与编译规则
├── Config.in                      # Buildroot 组件配置文件，用于在菜单中选择启用此应用
└── face_detect.mk                 # Buildroot 编译规则文件，定义源码、依赖和安装路径
```

#### 已有代码功能

下面介绍已有的代码中不同文件的作用：

| 文件名称                    |         作用     |
|--------------------------- | -----------------|
|ai_base.h|提供模型推理过程中使用的接口|
|ai_bash.cc|提供ai_bash.h中定义的模型推理方法的接口实现|
|utils.h|提供共用的工具函数接口|
|utils.cc|提供utils.h中定义的工具函数实现|
|scoped_timing.h|提供计时工具，帮助开发调试|
|sensor_set.h|设置AI推理图像分辨率的配置|
|sensor_buf_manager.h|摄像头缓冲区管理实现模型输入tensor的获取和释放|
|sensor_buf_manager.cc|提供sensor_buf_manager.h中定义的缓冲区管理接口实现|
|face_detection.h|提供具体任务场景（这里是人脸检测）的预处理、推理、后处理、结果绘制等接口|
|face_detection.cc|提供了face_detection.h定义的任务场景接口实现|
|anchors_320.cc|人脸检测任务使用到的anchors数据|
|anchors_640.cc|人脸检测任务使用到的anchors数据|
|main.cc|主函数实现，基于face_detection.h提供的接口实现具体的AI应用场景|

在开发一个AI应用时，上述文件的应该如何使用和编写呢？

- `ai_base.h`和 `ai_base.cc` 实现了模型推理过程中的 `kmodel` 初始化、模型输入输出初始化、运行和获取输出的接口，代码见文件注释；`scoped_timing.h` 提供了计时工具；**这几个文件一般是不需要更改的**。
- `utils.h` 和 `utils.cc` 提供了通用的工具函数，主要是数据存取和共用的预处理方法，**如果提供的方法无法满足您的需求，您可以修改这两个文件新增方法，如已满足则无需修改**。
- `sensor_set.h`、`sensor_buf_manager.h`和`sensor_buf_manager.cc` 实现了AI推理帧分辨率的配置和摄像头数据转换推理tensor的功能；**如果您需要修改摄像头出图给AI模型推理的分辨率，可以调整`sensor_set.h`文件，否则可以保持不变。这几个文件保证能够得到可以给kmodel使用的tensor**。
- `face_detection.h`、 `face_detection.cc` 和 `main.cc` 是用户在开发新的AI应用时**需要自行编写**的文件，编写参考 `k230_linux_sdk/buildroot-overlay/package/face_detect/src` 下的对应文件即可。其中任务场景的头文件和实现文件主要**实现该任务模型的输入前处理、推理（一般直接调用`ai_base.h`中的`run`方法），模型后处理部分的代码**；`main.cc` 文件需要修改参数解析、模型推理部分的逻辑和结果绘制部分，包括**具体任务场景类的实例初始化，前处理、模型推理、后处理和显示线程中结果绘制接口的调用**。

#### 代码开发和修改

##### 开发逻辑

`ai_demo` 的基本开发结构采用了**单摄像头双通道处理**的方式。其核心思路是将摄像头采集到的图像分为两路处理：

- **一路图像**直接绑定到屏幕进行显示，以保证画面能够**实时、低延迟地呈现**；
- **另一路图像**则用于**AI 模型推理**，即将图像转换为 tensor，送入模型进行处理，得到检测或识别的结果。

推理完成后，程序会将这些结果绘制到一个**透明图层（OSD）**上，并与实时显示的那一路图像**叠加显示**。最终，用户在屏幕上看到的就是**融合了原始图像与 AI 识别结果的效果图**。

我们之所以采用这种“双通道处理 + 图层叠加”的方式，是为了解决性能瓶颈问题。
如果采用传统的流程：

```shell
获取一帧图像 → 预处理 → 创建 tensor → 模型推理 → 后处理 → 在图像上绘制结果 → 显示
```

如果**模型推理本身耗时较长**，整个流程会导致图像卡顿，尤其在使用复杂模型或处理复杂任务时尤为明显，体验会大打折扣。

因此，我们将显示与 AI 推理分离：**实时显示优先，推理结果异步绘制并叠加**，从而在保证画面流畅的同时，又能实时呈现 AI 分析的结果。

如下图所示，为该双通道处理逻辑的流程图：

![2_chn_process](https://www.kendryte.com/api/post/attachment?id=614)

##### 配置说明

`sensor_set.h`中配置的宏定义参数主要用于设置摄像头出图给AI推理图像的分辨率。

|宏定义参数|说明|
|:-:|:-:|
|`SENSOR_WIDTH`|AI推理帧宽度|
|`SENSOR_HEIGHT`|AI推理帧高度|
|`SENSOR_CHANNEL`|AI推理帧通道数|

> **注意：**
>
> 这里需要区分AI通道的分辨率和模型输入的分辨率，模型输入的分辨率是**模型预处理之后**直接传送给模型的数据宽高，AI通道的分辨率指的是**来自摄像头，在AI模型预处理前**的图像数据分辨率。预处理之后AI通道的数据才能准换成模型输入的数据。比如，摄像头AI通道的输出的分辨率是640×360，模型要求输入为320×320，因此必须经过预处理过程才能符合要求。

##### `ai_base.h` 部分说明

`ai_base.h` 中的`AIBase` 是实现模型推理的封装类，包括模型初始化，输入输出shape、tensor初始化、模型推理、获取输出等功能。

```cpp
/**
 * @file ai_base.h
 * @brief 定义 AIBase 基类，封装基于 nncase 的 Kmodel 推理逻辑
 * @author 
 * @date 2025
 */

#ifndef AI_BASE_H
#define AI_BASE_H

#include <vector>
#include <string>
#include <fstream>

#include <nncase/runtime/interpreter.h>
#include <nncase/runtime/runtime_op_utility.h>
#include <nncase/runtime/util.h>
#include "scoped_timing.h"

using std::string;
using std::vector;
using namespace nncase::runtime;

/**
 * @class AIBase
 * @brief AI 模型推理基类，封装了 Kmodel 模型的加载、输入输出管理和推理流程。
 *
 * 该类为 nncase 推理框架的封装，提供模型初始化、输入输出张量管理、推理执行等通用接口。
 * 子类可以继承该类并扩展具体模型的前处理与后处理逻辑。
 */
class AIBase
{
public:
    /**
     * @brief 构造函数，加载 Kmodel 模型并初始化输入输出信息。
     * @param kmodel_file Kmodel 模型文件路径
     * @param model_name 模型名称（用于日志标识）
     * @param debug_mode 调试模式（0：无日志，1：打印耗时，2：打印详细信息）
     */
    AIBase(const char *kmodel_file, const string model_name, const int debug_mode = 1);

    /**
     * @brief 析构函数，释放资源。
     */
    ~AIBase();

    /**
     * @brief 获取指定索引的输入张量。
     * @param idx 输入张量的索引（从 0 开始）
     * @return 对应的 runtime_tensor 输入张量对象
     */
    runtime_tensor get_input_tensor(size_t idx);

    /**
     * @brief 设置指定索引的输入张量。
     * @param idx 输入张量索引
     * @param input_tensor 输入张量的引用对象
     */
    void set_input_tensor(size_t idx, runtime_tensor &input_tensor);

    /**
     * @brief 执行一次前向推理。
     */
    void run();

    /**
     * @brief 获取模型推理结果并缓存到 p_outputs_ 中（float*）。
     */
    void get_output();

    /**
     * @brief 获取指定索引的输出张量。
     * @param idx 输出张量索引
     * @return 对应的 runtime_tensor 输出张量对象
     */
    runtime_tensor get_output_tensor(int idx);

protected:
    string model_name_;                        ///< 模型名称（日志用途）
    int debug_mode_;                           ///< 调试等级（0：无日志，1：打印耗时，2：详细信息）
    vector<float *> p_outputs_;                ///< 输出结果的缓存指针列表（每个 float* 指向一个输出张量）
    vector<vector<int>> input_shapes_;         ///< 每个输入张量的形状（维度）
    vector<vector<int>> output_shapes_;        ///< 每个输出张量的形状（维度）

private:
    /**
     * @brief 初始化模型输入信息（推理前调用一次）。
     */
    void set_input_init();

    /**
     * @brief 初始化模型输出信息（推理前调用一次）。
     */
    void set_output_init();

    interpreter kmodel_interp_;               ///< nncase 模型解释器对象
    vector<unsigned char> kmodel_vec_;        ///< Kmodel 模型二进制数据缓存
};

#endif // AI_BASE_H

```

在上述封装结构中，我们在应用开发时可能用到的主要是输入输出`tensor`的`shape`，这一部分可以在`input_shapes_`和`output_shapes_`中获取，输出`tensor`的数据指针可以从`p_outputs_`中获取，比如想要得到模型第一个输出的指针：

```cpp
float *output0 = p_outputs_[0];
```

##### 任务场景头文件和实现文件

`face_detection.h` 和 `face_detection.cc` 是开发过程中需要用户自己编写代码的部分，您可以使用您应用场景的文件名`***.h`和`***.cc`，在这两个文件中构造任务场景类，该类继承AIBase实现模型推理部分，用户需要自行编写前后处理和结果绘制部分。如果`utils.h`已经包含您需要的前处理方法，则您只需要编写后处理和结果绘制部分。**前处理指的是通过一些操作使得输入数据符合模型需要的输入，后处理指的是将模型计算输出的纯数据处理成任务场景需要的内容(比如检测框、类别索引、关键点坐标等)**。

这里假设应用场景类的头文件和实现为`myapp.h`和`myapp.cc`，其中`myapp.h`的结构可以仿照`face_detection.h`编写：

```cpp
#ifndef _MYAPP_H
#define _MYAPP_H

#include <iostream>
#include <vector>
#include "ai_utils.h"
#include "ai_base.h"

using std::vector;


/**
 * @brief 后处理过程中使用的自定义数据结构，比如检测框就需要包含坐标xywh、分类索引以及置信度，这里按需定义
 */
typedef struct ExampleResults
{
    //这里需要按需定义使用的数据结构
} ExampleResults;

/**
 * @brief 待开发应用类,继承AIBase
 * 主要封装基于具体应用场景的对于每一帧图片，从预处理、运行到后处理给出结果的过程
 */
class MyApp : public AIBase
{
public:
    /**
     * @brief 视频流推理，MyApp构造函数，加载kmodel,并初始化kmodel输入、输出和应用使用的其他参数比如阈值等，并配置对应的预处理方法
     * @param kmodel_file kmodel文件路径
     * @param other_params 其他参数，比如各种阈值
     * @param image_size   摄像头AI通道图像一帧输入shape
     * @param debug_mode  0（不调试）、 1（只显示时间）、2（显示所有打印信息）
     * @return None
     */
    MyApp(char *kmodel_file, other_params, FrameCHWSize image_size, int debug_mode);

    /**
     * @brief MyApp析构函数
     * @return None
     */
    ~MyApp();

    /**
     * @brief 预处理
     * @param input_tensor 输入张量
     * @return None
     */
    void pre_process(runtime_tensor &input_tensor);

    /**
     * @brief kmodel推理
     * @return None
     */
    void inference();

    /**
     * @brief kmodel推理结果后处理，使用传入的image_size，将坐标等信息复原到原图分辨率，并将结果存入results
     * @param image_size  输入图片的shape
     * @param results 后处理结果存储容器
     * @return None
     */
    void post_process(FrameCHWSize image_size,vector<ExampleReults> &results);

     /**
     * @brief 绘制结果
     * @param draw_frame  待绘制结果的透明图像（视频OSD）或者原图（单图推理），类型为cv::Mat
     * @param results     后处理结果
     * @return None
     */
    void draw_result(cv::Mat& draw_frame,vector<ExampleReults>& results);


    std::unique_ptr<ai2d_builder> ai2d_builder_; // ai2d构建器
    runtime_tensor ai2d_out_tensor_;             // ai2d输出tensor
    FrameCHWSize image_size_;                    // 输入图片的shape
    FrameCHWSize input_size_;                    // 模型输入的shape

    //这里可以定义其他当前任务场景使用的成员变量,比如分类阈值
    // ***
};

#endif
```

上述定义的接口需要在`myapp.cc`中做具体实现，此处不再赘述。您可以参考`k230_linux_sdk/buildroot-overlay/package/face_detect/src/face_detection.cc`中的代码仿写。

##### `main.cc`文件的修改

- **流程概述**

`main.cc`中是整个任务的逻辑，包括从摄像头获取一帧数据/读入一张图片、创建tensor、调用应用类的前处理、推理、后处理，并在现实线程绘制结果等步骤实现推理效果可视化。该过程的流程图如下所示：

![model_inference_rtos](https://www.kendryte.com/api/post/attachment?id=642)

- **视频推理代码**

`main.cc`中视频推理的代码如下所示，您需要根据自身的场景仿写这部分的代码。该部分代码分为两个线程，一个线程完成AI推理，另一个线程完成效果显示。

首先要定义一些全局变量，用于定义显示缓冲区和存储推理结果，定义线程退出标志。

```cpp
// 用于保护检测结果的互斥锁，防止多线程同时读写 face_results
static std::mutex result_mutex;

// 存放人脸检测的结果（如人脸框位置、置信度等）
static std::vector<FaceDetectionInfo> face_results;

// AI 推理停止标志（true 表示停止推理循环）
// 由主控线程或外部信号控制，用于安全退出推理线程
std::atomic<bool> ai_stop(false);

// 显示线程退出标志（true 表示退出显示循环）
// 一般由主控线程设置，用于安全结束显示线程
std::atomic<bool> display_stop(false);

// KPU（AI加速单元）帧计数器，用于统计推理帧率或调试性能
// volatile 关键字防止编译器优化，保证多线程访问的可见性
static volatile unsigned kpu_frame_count = 0;

// 时间变量，用于帧率统计或性能计时
static struct timeval tv, tv2;

// 显示设备实例指针（封装 DRM/LVGL 等底层显示接口）
static struct display* display;

// OSD（On-Screen Display）绘制缓冲区，用于渲染检测结果或叠加图层
struct display_buffer* draw_buffer;

// OpenCV 图像矩阵，用于临时保存绘制后的帧（如检测框、人脸标记等）
// 可用于显示或保存图像结果
cv::Mat draw_frame;

```

对于模型推理线程，从 V4L2 设备中采集视频帧，通过人脸检测模型 (FaceDetection)进行推理与后处理，生成检测结果并保存到全局变量 face_results，同时生成绘制帧 draw_frame，用于显示线程显示。示例代码如下：

```cpp
/**
 * @brief AI 推理处理线程
 * 
 * 从 V4L2 设备中采集视频帧，通过人脸检测模型 (FaceDetection)
 * 进行推理与后处理，生成检测结果并保存到全局变量 face_results，
 * 同时生成绘制帧 draw_frame，用于显示线程显示。
 * 
 * @param argv         命令行参数数组（包含模型路径、阈值等）
 * @param video_device 视频设备编号（/dev/videoX）
 */
void ai_proc(char *argv[], int video_device) {
    struct v4l2_drm_context context;          // V4L2 + DRM 视频上下文结构体
    struct v4l2_drm_video_buffer buffer;      // 用于存放单帧视频数据的缓冲区
    #define BUFFER_NUM 3                      // V4L2 缓冲区数量（循环使用）

    // 等待显示线程（display_proc）先行启动并完成初始化
    // 通过互斥锁实现同步（防止AI线程在显示资源未就绪前启动）
    result_mutex.lock();
    result_mutex.unlock();

    // 初始化 V4L2 + DRM 采集上下文的默认参数
    v4l2_drm_default_context(&context);
    context.device = video_device;            // 设置视频设备号
    context.display = false;                  // 不直接显示，由显示线程负责显示
    context.width = SENSOR_WIDTH;             // 传感器采集宽度
    context.height = SENSOR_HEIGHT;           // 传感器采集高度
    context.video_format = v4l2_fourcc('B', 'G', '3', 'P'); // BG3P 格式 (RGB planar)
    context.buffer_num = BUFFER_NUM;          // 缓冲区数量

    // 初始化视频采集上下文
    if (v4l2_drm_setup(&context, 1, NULL)) {
        std::cerr << "v4l2_drm_setup error" << std::endl;
        return;
    }

    // 启动视频采集（stream on）
    if (v4l2_drm_start(&context)) {
        std::cerr << "v4l2_drm_start error" << std::endl;
        return;
    }

    // 解析命令行参数：模型路径、置信度阈值、NMS 阈值、调试模式
    char* kmodel_det = argv[1];               // 人脸检测模型文件路径
    float obj_thresh = atof(argv[2]);         // 检测置信度阈值
    float nms_thresh = atof(argv[3]);         // 非极大值抑制（NMS）阈值
    int debug_mode = atoi(argv[5]);           // 调试模式开关（打印日志等）

    // 初始化人脸检测类实例（模型加载、输入输出配置）
    FaceDetection fd(
        kmodel_det,
        obj_thresh,
        nms_thresh,
        {SENSOR_CHANNEL, SENSOR_HEIGHT, SENSOR_WIDTH},
        debug_mode
    );

    // 创建传感器缓冲区映射表，将 V4L2 缓冲区与 AI 输入张量绑定
    std::vector<std::tuple<int, void*>> tensors;
    for (unsigned i = 0; i < BUFFER_NUM; i++) {
        tensors.push_back({context.buffers[i].fd, context.buffers[i].mmap});
    }
    // 管理传感器帧缓冲区的类，提供 AI 输入数据的读取接口
    SensorBufManager sensor_buf({SENSOR_CHANNEL, SENSOR_HEIGHT, SENSOR_WIDTH}, tensors);
    
    // ====================== 主推理循环 ======================
    while (!ai_stop) {
        // 从 V4L2 获取一帧视频数据（带超时 1000ms）
        int ret = v4l2_drm_dump(&context, 1000);
        if (ret) {
            perror("v4l2_drm_dump error");
            continue;
        }

        // -------------------- AI 推理流程 --------------------
        // 1. 预处理：将当前帧数据送入模型输入张量（resize、normalize 等）
        fd.pre_process(sensor_buf.get_buf_for_index(context.vbuffer.index));

        // 2. 模型推理：执行 KPU/nncase 推理
        fd.inference();

        // 3. 后处理：解码模型输出、执行 NMS、生成检测框
        result_mutex.lock();                  // 加锁保护全局结果
        face_results.clear();                 // 清空旧结果
        fd.post_process({SENSOR_WIDTH, SENSOR_HEIGHT}, face_results);

        // 4. 绘制检测结果（绘制框、人脸标签等）到全局帧缓冲
        draw_frame.setTo(cv::Scalar(0, 0, 0, 0)); // 清空上一帧内容
        FaceDetection::draw_result_video(draw_frame, face_results);
        result_mutex.unlock();                // 解锁

        // 统计帧数（用于性能计算）
        kpu_frame_count += 1;

        // 释放当前帧缓冲，返回给 V4L2 队列
        v4l2_drm_dump_release(&context);
    }

    // ====================== 停止采集与清理 ======================
    v4l2_drm_stop(&context);                  // 关闭视频流（stream off）
}
```

对于显示部分，由一个显示线程和一个显示回调方法组成。显示线程负责初始化显示资源，回调方法用于显示每一帧的绘制结果。

定义的 `v4l2_drm_run` 驱动循环回调方法如下，在每一帧显示数据时被调用。可以在AI线程中在全局变量`draw_frame`上绘制，然后拷贝到`temp_img`，也可以直接在`temp_img`上绘制。拷贝方式的代码如下：

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
```

显示资源初始化部分代码如下，`display_proc` 函数代码的主要功能是 启动一个视频显示线程，负责 初始化 V4L2 + DRM 显示环境、配置屏幕参数、绑定帧处理回调，并在主循环中不断刷新显示帧。

```cpp
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

- **图片推理代码**

`main.cc` 中存在图片推理的代码。首先加载一张输入图片并执行人脸检测推理流程，最终将绘制了检测结果的图像保存为 `face_detection_result.jpg`。它完整地展示了一个人脸检测模型从 `加载` → `推理` → `可视化输出` 的典型处理流程。示例代码如下：

```cpp
cv::Mat ori_img = cv::imread(argv[4]);
int ori_w = ori_img.cols;
int ori_h = ori_img.rows;
FaceDetection fd(argv[1], atof(argv[2]),atof(argv[3]), atoi(argv[5]));
fd.pre_process(ori_img);
fd.inference();
vector<FaceDetectionInfo> results;
fd.post_process({ori_w, ori_h}, results);
fd.draw_result(ori_img,results);

cv::imwrite("face_detection_result.jpg", ori_img);
```

修改推理逻辑时，注意也要修改传入参数说明和传入参数个数校验部分：

```cpp
void print_usage(const char *name)
{
    cout << "Usage: " << name << "<kmodel_det> <obj_thres> <nms_thres> <input_mode> <debug_mode>" << endl
         << "Options:" << endl
         << "  kmodel_det      人脸检测kmodel路径\n"
         << "  obj_thres       人脸检测kmodel阈值\n"
         << "  nms_thres       人脸检测kmodel nms阈值\n"
         << "  input_mode      本地图片(图片路径)/ 摄像头(None) \n"
         << "  debug_mode      是否需要调试，0、1、2分别表示不调试、简单调试、详细调试\n"
         << "\n"
         << endl;
}
```

```cpp
std::cout << "case " << argv[0] << " built at " << __DATE__ << " " << __TIME__ << std::endl;
if (argc != 6)
{
    print_usage(argv[0]);
    return -1;
}
```

##### 构建文件`CMakeLists.txt`和编译脚本`build_app.sh`

对于人脸检测任务目录中的`face_detect/CMakeLists.txt`，需要修改编译生成文件名称，即`set(bin face_detect.elf)`,其他配置的自动源文件收集、交叉编译器配置、头文件路径设置、库依赖链接、安装规则 等完整的构建流程可以不变。

```cmake
cmake_minimum_required(VERSION 3.5)
set(CMAKE_CXX_STANDARD 17)
project(face_detect)

message("CMAKE_TOOLCHAIN_FILE:" ${CMAKE_TOOLCHAIN_FILE})

# ========== 源文件自动收集 ==========
file(GLOB src CONFIGURE_DEPENDS src/*.cc)
set(bin face_detect.elf)

# ========== 创建可执行文件 ==========
add_executable(${bin} ${src})

# ========== 设置交叉编译工具链路径 ==========
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS}   -mcpu=c908v -mabi=lp64d  -mtune=c908 -mrvv-v0p10-compatible  -mrvv-auto-vectorize")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}   -mcpu=c908v -mabi=lp64d  -mtune=c908 -mrvv-v0p10-compatible  -mrvv-auto-vectorize")

if(CMAKE_TOOLCHAIN_FILE MATCHES "buildroot/toolchainfile.cmake")
    # buildroot环境编译，默认编译器为buildroot的编译器
else()
    # shell脚本编译，设置编译器路径
    set(CMAKE_C_COMPILER $ENV{GCC_PATH}/riscv64-unknown-linux-gnu-gcc)
    set(CMAKE_CXX_COMPILER $ENV{GCC_PATH}/riscv64-unknown-linux-gnu-g++)
    set(CMAKE_SYSROOT $ENV{sysroot})
endif()

message("CMAKE_C_COMPILER:" ${CMAKE_C_COMPILER})
message("CMAKE_CXX_COMPILER:" ${CMAKE_CXX_COMPILER})
message("CMAKE_SYSROOT:" ${CMAKE_SYSROOT})

# ========== 设置 SDK 路径和 sysroot ==========
set(usr_root ${CMAKE_SYSROOT}/usr)

# ========== 添加头文件搜索路径 ==========
include_directories(
    ${usr_root}/buildroot-overlay/package/libmmz/
    ${usr_root}/include/nncase/include/
    ${usr_root}/include
    ${usr_root}/include/libdrm
    ${usr_root}/include/opencv4
)

# ========== 添加链接库目录 ==========
target_link_directories(${bin} PRIVATE
    ${usr_root}/lib
    ${CMAKE_SYSROOT}
    ${CMAKE_SYSROOT}/usr/lib64/lp64d
)

# ========== 链接所需的库 ==========
# 使用 --start-group 和 --end-group 包裹，解决静态库相互依赖的链接问题
target_link_libraries(${bin}
    -Wl,--start-group
    Nncase.Runtime.Native
    nncase.rt_modules.k230
    functional_k230
    opencv_imgcodecs
    opencv_imgproc
    opencv_core
    sharpyuv
    libjpeg.so.9
    webp
    png
    z
    v4l2-drm
    drm
    display
    mmz
    pthread
    -Wl,--end-group
)

# ========== 安装规则 ==========

if(CMAKE_TOOLCHAIN_FILE MATCHES "buildroot/toolchainfile.cmake")
    # Buildroot 环境
    message(STATUS "使用 Buildroot 编译，安装到 /root/app/face_detect/")
    install(TARGETS ${bin} DESTINATION /root/app/face_detect)
    install(DIRECTORY utils/ DESTINATION /root/app/face_detect)
else()
    # 非 Buildroot，自己本地 build_app.sh 编译
    message(STATUS "本地编译，安装到 ./k230_bin/")
    install(TARGETS ${bin} DESTINATION bin)
endif()
```

编译脚本文件`face_detect/build_app.h`自动检测 SDK 环境、设置交叉编译路径、执行 CMake 构建、复制生成产物到部署目录，并清理临时文件。用户需要修改elf文件拷贝路径和名称：

```shell
if [ -f out/bin/face_detect.elf ]; then
      cp out/bin/face_detect.elf ${k230_bin}
fi
```

> `face_detect.mk`定义了 face_detect 应用在 Buildroot 环境下的构建与Debian 打包流程，支持本地源编译、依赖自动管理、安装钩子触发 .deb 生成，最终输出可直接安装的 K230 人脸检测应用包。
`face_detect.mk`是Buildroot 的配置文件片段（Config.in），用于在 Buildroot 菜单配置中添加一个可选的 “face detect demo” 软件包选项。
如果对这两个文件不熟悉的可以**忽略**，直接使用编译脚本`build_app.sh`编译。

### 编译代码

在`face_detect`目录下执行`build_app.sh`即可得到编译后的产物。编译产物将生成在`k230_bin` 目录下。将编译产物拷贝到开发板上即可运行部署脚本，查看部署效果。

### 开发板部署

使用`rufus`将生成的镜像烧录到TF卡，然后上电，连接网络，连接串口，使用`scp`拷贝文件到开发板，执行命令运行：

- **视频推理**

```shell
./face_detect.elf face_detection_320.kmodel 0.6 0.2 None 0
```

- **图片推理**

```shell
./face_detect.elf face_detection_320.kmodel 0.6 0.2 None 0
```

### 调试指南

#### 打印模型输入输出shape是否合理

通过打印输出`ai_base.h`中的`AIBase`类的成员变量`input_shapes_`和`output_shapes_`查看输入输出的维度是否正确。

#### 通过dump原始数据查看数据

获取一帧摄像头的数据可以使用如下代码进行保存,将如下代码添加到AI推理线程的`while`循环开始的地方，每次都将当前帧的图像保存：

```cpp
std::vector<cv::Mat> sensor_bgr(3);
cv::Mat ori_img;
sensor_bgr.clear();
void* data=context.buffers[0].mmap;
cv::Mat ori_img_R = cv::Mat(SENSOR_HEIGHT, SENSOR_WIDTH, CV_8UC1, data);
cv::Mat ori_img_G = cv::Mat(SENSOR_HEIGHT, SENSOR_WIDTH, CV_8UC1, data + 1 * SENSOR_WIDTH * SENSOR_HEIGHT);
cv::Mat ori_img_B = cv::Mat(SENSOR_HEIGHT, SENSOR_WIDTH, CV_8UC1, data + 2 * SENSOR_WIDTH * SENSOR_HEIGHT);

if (ori_img_B.empty() || ori_img_G.empty() || ori_img_R.empty()) {
    std::cout << "One or more of the channel images is empty." << std::endl;
    continue;
}
sensor_bgr.push_back(ori_img_B);
sensor_bgr.push_back(ori_img_G);
sensor_bgr.push_back(ori_img_R);
cv::merge(sensor_bgr, ori_img);
cv::imwrite("ori_img.jpg",ori_img); 
```

#### 通过打印定位运行bug的具体位置

在代码中添加`std::cout`语句或日志机制，重复编译上板运行，查看报错位置。

#### 添加时间统计工具查看异常

对于整体运行时间明显异常的demo，可以添加打印时间的语句，查看模块运行耗时异常。源码中提供了`scoped_timing.h` 工具用于时间统计。示例代码如下：

```cpp
{
    ScopedTiming st("test", 1);
    /*
    * 这里写测试代码
    */
}
```

#### 对于内存问题可以使用free命令查看占用情况

使用`free -h`命令查看每次执行后的内存占用是否正确释放，如果多次启停程序，内存占用不断上升，则内存中存在内存泄漏，需要定位问题所在。

#### 模型的效果不满足要求

如果模型效果不满足您的要求，可以从以下四个方面进行调优：

- 调整模型的参数，比如置信度阈值、NMS阈值等；
- 调整模型的输入分辨率，确认前处理的合理性，比如将分辨率从`320*320`调整到`640*640`;
- 调整模型转换的量化方式，修改模型转换脚本量化参数中的`calibrate_method` 、`quant_type`和`w_quant_type`。比如，将`w_quant_type`改为`int6`;
- 更换更加合理的模型，如果当前模型不满足需求，可以更换当前任务的其他模型尝试;
