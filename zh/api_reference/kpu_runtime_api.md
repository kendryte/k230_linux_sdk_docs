# `KPU` 运行时API手册

## 概述

KPU 运行时 APIs 用于在 AI 设备加载 kmodel，设置输入数据，执行 KPU/CPU 计算，获取输出数据等。本文档提供了 C++ APIs。本文档提供的 API 用于在本地 PC 用 `C++` 编写在 `k230` 上运行的代码，编译成可执行文件后拷贝到 `k230` 上运行。

## API 介绍

### hrt::create

【描述】

创建runtime_tensor。

【定义】

```cpp
(1) NNCASE_API result<runtime_tensor> create(typecode_t datatype, dims_t shape, memory_pool_t pool = pool_shared_first) noexcept;
(2) NNCASE_API result<runtime_tensor> create(typecode_t datatype, dims_t shape, gsl::span<gsl::byte> data, bool copy,
       memory_pool_t pool = pool_shared_first) noexcept;
(3)NNCASE_API result<runtime_tensor>create(typecode_t datatype, dims_t shape, strides_t strides, gsl::span<gsl::byte> data, bool copy, memory_pool_t pool = pool_shared_first, uintptr_t physical_address = 0) noexcept;
```

【参数】

| 名称             | 类型                   | 描述                                  |
| ---------------- | ---------------------- | ------------------------------------- |
| datatype         | typecode_t             | 数据类型, 如dt_float32, dt_uint8等    |
| shape            | dims_t                 | tensor的形状                          |
| data             | gsl::span\<gsl::byte\> | 用户态数据buffer                      |
| copy             | bool                   | 是否拷贝                              |
| pool             | memory_pool_t          | 内存池类型, 默认值为pool_shared_first |
| physical_address | uintptr_t              | 用户指定buffer的物理地址              |

【返回值】

`result<runtime_tensor>`

【示例】

```cpp
// create input tensor
auto input_desc = interp.input_desc(0);
auto input_shape = interp.input_shape(0);
auto input_tensor = host_runtime_tensor::create(input_desc.datatype, input_shape, hrt::pool_shared).expect("cannot create input tensor");
```

### hrt::sync

【描述】

同步tensor的cache。

- 对用户的输入数据， 需要调用 此接口的sync_write_back确保数据已刷入ddr。
- 对gnne/ai2d计算后输出数据，默认gnne/ai2d runtime已做了sync_invalidate处理。

【定义】

`NNCASE_API result<void> sync(runtime_tensor &tensor, sync_op_t op, bool force = false) noexcept;`

【参数】

| 名称   | 类型           | 描述                                                                                 |
| ------ | -------------- | ------------------------------------------------------------------------------------ |
| tensor | runtime_tensor | 要操作的tensor                                                                       |
| op     | sync_op_t      | sync_invalidate(将tensor的cache invalidate)或sync_write_back(将tensor的cache写入ddr) |
| force  | bool           | 是否强制执行                                                                         |

【返回值】

`result<void>`

【示例】

```cpp
hrt::sync(input_tensor, sync_op_t::sync_write_back, true).expect("sync write_back failed");
```

### interpreter::load_model

【描述】

加载kmodel模型。

【定义】

`NNCASE_NODISCARD result<void> load_model(gsl::span<const gsl::byte> buffer) noexcept;`

【参数】

| 名称   | 类型                          | 描述          |
| ------ | ----------------------------- | ------------- |
| buffer | gsl::span \<const gsl::byte\> | kmodel buffer |

【返回值】

`result<void>`

【示例】

```cpp
interpreter interp;
auto model = read_binary_file<unsigned char>(kmodel);
interp.load_model({(const gsl::byte *)model.data(), model.size()}).expect("cannot load model.");
```

### interpreter::inputs_size

【描述】

获取模型输入的个数。

【定义】

`size_t inputs_size() const noexcept;`

【参数】

无。

【返回值】

`size_t`

【示例】

`auto inputs_size = interp.inputs_size();`

### interpreter::outputs_size

【描述】

获取模型输出的个数。

【定义】

`size_t outputs_size() const noexcept;`

【参数】

无。

【返回值】

`size_t`

【示例】

`auto outputs_size = interp.outputs_size();`

### interpreter:: input_shape

【描述】

获取模型指定输入的形状。

【定义】

`const runtime_shape_t &input_shape(size_t index) const noexcept;`

【参数】

| 名称  | 类型   | 描述       |
| ----- | ------ | ---------- |
| index | size_t | 输入的索引 |

【返回值】

`runtime_shape_t`

【示例】

`auto shape = interp.input_shape(0);`

### interpreter:: output_shape

【描述】

获取模型指定输出的形状。

【定义】

`const runtime_shape_t &output_shape(size_t index) const noexcept;`

【参数】

| 名称  | 类型   | 描述       |
| ----- | ------ | ---------- |
| index | size_t | 输出的索引 |

【返回值】

`runtime_shape_t`

【示例】

`auto shape = interp.output_shape(0);`

### interpreter:: input_tensor

【描述】

获取/设置指定索引的输入tensor。

【定义】

```cpp
(1) result<runtime_tensor> input_tensor(size_t index) noexcept;
(2) result<void> input_tensor(size_t index, runtime_tensor tensor) noexcept;
```

【参数】

| 名称   | 类型           | 描述                     |
| ------ | -------------- | ------------------------ |
| index  | size_t         | 输入的索引               |
| tensor | runtime_tensor | 输入对应的runtime tensor |

【返回值】

```cpp
(1) result<runtime_tensor>
(2) result<void>
```

【示例】

```cpp
// set input
interp.input_tensor(0, input_tensor).expect("cannot set input tensor");
```

### interpreter:: output_tensor

【描述】

获取/设置指定索引的输出tensor。

【定义】

```cpp
(1) result<runtime_tensor> output_tensor(size_t index) noexcept;
(2) result<void> output_tensor(size_t index, runtime_tensor tensor) noexcept;
```

【参数】

| 名称   | 类型           | 描述                     |
| ------ | -------------- | ------------------------ |
| index  | size_t         | 输出的索引               |
| tensor | runtime_tensor | 输出对应的runtime tensor |

【返回值】

```cpp
(1) result<runtime_tensor>
(2) result<void>
```

【示例】

```cpp
// get output
auto output_tensor = interp.output_tensor(0).expect("cannot get output tensor");
```

### interpreter:: run

【描述】

执行KPU计算。

【定义】

`result<void> run() noexcept;`

【参数】

无。

【返回值】

返回result \<void\>。

【示例】

```cpp
// run
interp.run().expect("error occurred in running model");
```

## 示例

```cpp
#include <chrono>
#include <fstream>
#include <iostream>
#include <nncase/runtime/interpreter.h>
#include <nncase/runtime/runtime_op_utility.h>

#define USE_OPENCV 1
#define preprocess 1

#if USE_OPENCV
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#endif

using namespace nncase;
using namespace nncase::runtime;
using namespace nncase::runtime::detail;

// 模型输入分辨率
#define INTPUT_HEIGHT 224
#define INTPUT_WIDTH 224
#define INTPUT_CHANNELS 3

template <class T>
std::vector<T> read_binary_file(const std::string &file_name)
{
    std::ifstream ifs(file_name, std::ios::binary);
    ifs.seekg(0, ifs.end);
    size_t len = ifs.tellg();
    std::vector<T> vec(len / sizeof(T), 0);
    ifs.seekg(0, ifs.beg);
    ifs.read(reinterpret_cast<char *>(vec.data()), len);
    ifs.close();
    return vec;
}

void read_binary_file(const char *file_name, char *buffer)
{
    std::ifstream ifs(file_name, std::ios::binary);
    ifs.seekg(0, ifs.end);
    size_t len = ifs.tellg();
    ifs.seekg(0, ifs.beg);
    ifs.read(buffer, len);
    ifs.close();
}

static std::vector<std::string> read_txt_file(const char *file_name)
{
    std::vector<std::string> vec;
    vec.reserve(1024);
    std::ifstream fp(file_name);
    std::string label;
    while (getline(fp, label))
    {
        vec.push_back(label);
    }
    return vec;
}

template<typename T>
static int softmax(const T* src, T* dst, int length)
{
    const T alpha = *std::max_element(src, src + length);
    T denominator{ 0 };

    for (int i = 0; i < length; ++i) {
        dst[i] = std::exp(src[i] - alpha);
        denominator += dst[i];
    }

    for (int i = 0; i < length; ++i) {
        dst[i] /= denominator;
    }

    return 0;
}

#if USE_OPENCV
std::vector<uint8_t> hwc2chw(cv::Mat &img)
{
    std::vector<uint8_t> vec;
    std::vector<cv::Mat> rgbChannels(3);
    cv::split(img, rgbChannels);
    for (auto i = 0; i < rgbChannels.size(); i++)
    {
        std::vector<uint8_t> data = std::vector<uint8_t>(rgbChannels[i].reshape(1, 1));
        vec.insert(vec.end(), data.begin(), data.end());
    }

    return vec;
}
#endif

static int inference(const char *kmodel_file, const char *image_file, const char *label_file)
{
    // load kmodel
    interpreter interp;
    
    // 从内存加载kmodel
    auto kmodel = read_binary_file<unsigned char>(kmodel_file);
    interp.load_model({ (const gsl::byte *)kmodel.data(), kmodel.size() }).expect("cannot load kmodel.");
    // 从文件流加载kmodel
    std::ifstream ifs(kmodel_file, std::ios::binary);
    interp.load_model(ifs).expect("cannot load kmodel");
    

    // create input tensor
    auto input_desc = interp.input_desc(0);
    auto input_shape = interp.input_shape(0);
    auto input_tensor = host_runtime_tensor::create(input_desc.datatype, input_shape, hrt::pool_shared).expect("cannot create input tensor");
    interp.input_tensor(0, input_tensor).expect("cannot set input tensor");

    // create output tensor
    // auto output_desc = interp.output_desc(0);
    // auto output_shape = interp.output_shape(0);
    // auto output_tensor = host_runtime_tensor::create(output_desc.datatype, output_shape, hrt::pool_shared).expect("cannot create output tensor");
    // interp.output_tensor(0, output_tensor).expect("cannot set output tensor");

    // set input data
    auto dst = input_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_write).unwrap().buffer();
#if USE_OPENCV
    cv::Mat img = cv::imread(image_file);
    cv::resize(img, img, cv::Size(INTPUT_WIDTH, INTPUT_HEIGHT), cv::INTER_NEAREST);
    auto input_vec = hwc2chw(img);
    memcpy(reinterpret_cast<char *>(dst.data()), input_vec.data(), input_vec.size());
#else
    read_binary_file(image_file, reinterpret_cast<char *>(dst.data()));
#endif
    hrt::sync(input_tensor, sync_op_t::sync_write_back, true).expect("sync write_back failed");

    // run
    size_t counter = 1;
    auto start = std::chrono::steady_clock::now();
    for (size_t c = 0; c < counter; c++)
    {
        interp.run().expect("error occurred in running model");
    }
    auto stop = std::chrono::steady_clock::now();
    double duration = std::chrono::duration<double, std::milli>(stop - start).count();
    std::cout << "interp.run() took: " << duration / counter << " ms" << std::endl;

    // get output data
    auto output_tensor = interp.output_tensor(0).expect("cannot set output tensor");
    dst = output_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_read).unwrap().buffer();
    float *output_data = reinterpret_cast<float *>(dst.data());
    auto out_shape = interp.output_shape(0);
    auto size = compute_size(out_shape);

    // postprogress softmax by cpu
    std::vector<float> softmax_vec(size, 0);
    auto buf = softmax_vec.data();
    softmax(output_data, buf, size);
    auto it = std::max_element(buf, buf + size);
    size_t idx = it - buf;

    // load label
    auto labels = read_txt_file(label_file);
    std::cout << "image classify result: " << labels[idx] << "(" << *it << ")" << std::endl;

    return 0;
}

int main(int argc, char *argv[])
{
    std::cout << "case " << argv[0] << " built at " << __DATE__ << " " << __TIME__ << std::endl;
    if (argc != 4)
    {
        std::cerr << "Usage: " << argv[0] << " <kmodel> <image> <label>" << std::endl;
        return -1;
    }

    int ret = inference(argv[1], argv[2], argv[3]);
    if (ret)
    {
        std::cerr << "inference failed: ret = " << ret << std::endl;
        return -2;
    }
    return 0;
}
```

上述代码需要在 `k230 linux sdk` 环境下使用编译工具编译成 `elf` 可执行文件，然后拷贝到开发板运行。
