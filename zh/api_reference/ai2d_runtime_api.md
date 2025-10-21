# `AI2D` 运行时 API 手册

## 概述

`AI2D` 运行时 APIs 用于在 AI 设备配置 `AI2D` 的参数，生成相关寄存器配置，执行 `AI2D` 预处理计算。本文档提供的 API 用于在本地 PC 用 `C++` 编写在 `k230` 上运行的代码，编译成可执行文件后拷贝到 `k230` 上运行。

> 注意：
>
> 1、 Affine和Resize功能是互斥的，不能同时开启；
> 2、 Shift功能的输入格式只能是Raw16；
> 3、 Pad value是按通道配置的，对应的list元素个数要与channel数相等；
> 4、 当前版本中，当只需要AI2D的一个功能时，其他参数也需要配置，flag置为false即可，其他字段不用配置；
> 5、 当配置了多个功能时，执行顺序是Crop->Shift->Resize/Affine->Pad, 配置参数时注意要匹配。

### 支持的格式转换

| 输入格式         | 输出格式               | 备注                  |
| ---------------- | ---------------------- | --------------------- |
| YUV420_NV12      | RGB_planar/YUV420_NV12 |                       |
| YUV420_NV21      | RGB_planar/YUV420_NV21 |                       |
| YUV420_I420      | RGB_planar/YUV420_I420 |                       |
| YUV400           | YUV400                 |                       |
| NCHW(RGB_planar) | NCHW(RGB_planar)       |                       |
| RGB_packed       | RGB_planar/RGB_packed  |                       |
| RAW16            | RAW16/8                | 深度图，执行shift操作 |

### 功能描述

| 功能                | 描述                                                                                                            | 备注              |
| ------------------- | --------------------------------------------------------------------------------------------------------------- | ----------------- |
| Affine              | 支持输入格式YUV420、YUV400、RGB（planar/packed）  支持深度图RAW16格式  支持输出格式YUV400、RGB、深度图          |                   |
| Crop/Resize/Padding | 支持输入YUV420、YUV400、RGB  支持深度图RAW16格式  Resize支持中间NCHW的排列格式  支持输出格式YUV420、YUV400、RGB | 只支持padding常数 |
| Shift               | 支持输入格式Raw16  支持输出格式Raw8                                                                             |                   |
| 符号位              | 支持有符号和无符号输入                                                                                          |                   |

## 参数类型介绍

### ai2d_format

【描述】

ai2d_format用于配置输入输出的可选数据格式。

【定义】

```cpp
enum class ai2d_format
{
    YUV420_NV12 = 0,
    YUV420_NV21 = 1,
    YUV420_I420 = 2,
    NCHW_FMT = 3,
    RGB_packed = 4,
    RAW16 = 5,
}
```

### ai2d_interp_method

【描述】

ai2d_interp_method用于配置可选的插值方式。

【定义】

```cpp
 enum class ai2d_interp_method
{
    tf_nearest = 0,
    tf_bilinear = 1,
    cv2_nearest = 2,
    cv2_bilinear = 3,
}
```

### ai2d_interp_mode

【描述】

ai2d_interp_mode 用于配置可选的插值模式。

【定义】

```cpp
enum class ai2d_interp_mode
{
    none = 0,
    align_corner = 1,
    half_pixel = 2,
}
```

### ai2d_pad_mode

【描述】

ai2d_pad_mode用于配置可选的padding模式，目前只支持常数padding。

【定义】

```cpp
enum class ai2d_pad_mode
{
    constant = 0,
    copy = 1,
    mirror = 2,
}
```

### ai2d_datatype_t

【描述】

ai2d_datatype_t 用于设置AI2D计算过程中的数据类型。

【定义】

```cpp
struct ai2d_datatype_t
{
    ai2d_format src_format;
    ai2d_format dst_format;
    datatype_t src_type;
    datatype_t dst_type;
    ai2d_data_loc src_loc = ai2d_data_loc::ddr;
    ai2d_data_loc dst_loc = ai2d_data_loc::ddr;
}
```

【参数】

| 名称       | 类型          | 描述                  |
| ---------- | ------------- | --------------------- |
| src_format | ai2d_format   | 输入数据格式          |
| dst_format | ai2d_format   | 输出数据格式          |
| src_type   | datatype_t    | 输入数据类型          |
| dst_type   | datatype_t    | 输出数据类型          |
| src_loc    | ai2d_data_loc | 输入数据位置，默认ddr |
| dst_loc    | ai2d_data_loc | 输出数据位置，默认ddr |

【示例】

```cpp
ai2d_datatype_t ai2d_dtype { ai2d_format::RAW16, ai2d_format::NCHW_FMT, datatype_t::dt_uint16, datatype_t::dt_uint8 };
```

### ai2d_crop_param_t

【描述】

ai2d_crop_param_t用于配置crop相关的参数。

【定义】

```cpp
struct ai2d_crop_param_t
{
    bool crop_flag = false;
    int32_t start_x = 0;
    int32_t start_y = 0;
    int32_t width = 0;
    int32_t height = 0;
}
```

【参数】

| 名称      | 类型 | 描述               |
| --------- | ---- | ------------------ |
| crop_flag | bool | 是否开启crop功能   |
| start_x   | int  | 宽度方向的起始像素 |
| start_y   | int  | 高度方向的起始像素 |
| width     | int  | 宽度方向的crop长度 |
| height    | int  | 高度方向的crop长度 |

【示例】

```cpp
ai2d_crop_param_t crop_param { true, 40, 30, 400, 600 };
```

### ai2d_shift_param_t

【描述】

ai2d_shift_param_t用于配置shift相关的参数。

【定义】

```cpp
struct ai2d_shift_param_t
{
    bool shift_flag = false;
    int32_t shift_val = 0;
}
```

【参数】

| 名称       | 类型 | 描述              |
| ---------- | ---- | ----------------- |
| shift_flag | bool | 是否开启shift功能 |
| shift_val  | int  | 右移的比特数      |

【示例】

`ai2d_shift_param_t shift_param { true, 2 };`

### ai2d_pad_param_t

【描述】

ai2d_pad_param_t 用于配置pad相关的参数。

【定义】

```cpp
struct ai2d_pad_param_t
{
    bool pad_flag = false;
    runtime_paddings_t paddings;
    ai2d_pad_mode pad_mode = ai2d_pad_mode::constant;
    std::vector<int32_t> pad_val; // by channel
}
```

【参数】

| 名称     | 类型                   | 描述                                                                                                  |
| -------- | ---------------------- | ----------------------------------------------------------------------------------------------------- |
| pad_flag | bool                   | 是否开启pad功能                                                                                       |
| paddings | runtime_paddings_t     | 各个维度的padding, shape=`[4, 2]`，分别表示dim0到dim4的前后padding的个数，其中dim0/dim1固定配置{0, 0} |
| pad_mode | ai2d_pad_mode          | padding模式，只支持constant padding                                                                   |
| pad_val  | std::vector\<int32_t\> | 每个channel的padding value                                                                            |

【示例】

```cpp
ai2d_pad_param_t pad_param { false, { { 0, 0 }, { 0, 0 }, { 0, 0 }, { 60, 60 } }, ai2d_pad_mode::constant, { 255 } };
```

### ai2d_resize_param_t

【描述】

ai2d_resize_param_t 用于配置resize相关的参数。

【定义】

```cpp
struct ai2d_resize_param_t
{
    bool resize_flag = false;
    ai2d_interp_method interp_method = ai2d_interp_method::tf_bilinear;
    ai2d_interp_mode interp_mode = ai2d_interp_mode::none;
}
```

【参数】

| 名称          | 类型               | 描述               |
| ------------- | ------------------ | ------------------ |
| resize_flag   | bool               | 是否开启resize功能 |
| interp_method | ai2d_interp_method | resize插值方法     |
| interp_mode   | ai2d_interp_mode   | resize模式         |

【示例】

```cpp
ai2d_resize_param_t resize_param { true, ai2d_interp_method::tf_bilinear, ai2d_interp_mode::half_pixel };
```

### ai2d_affine_param_t

【描述】

ai2d_affine_param_t 用于配置affine相关的参数。

【定义】

```cpp
struct ai2d_affine_param_t
{
    bool affine_flag = false;
    ai2d_interp_method interp_method = ai2d_interp_method::cv2_bilinear;
    uint32_t cord_round = 0;
    uint32_t bound_ind = 0;
    int32_t bound_val = 0;
    uint32_t bound_smooth = 0;
    std::vector<float> M;
}
```

【参数】

| 名称          | 类型                 | 描述                                                                                                                         |
| ------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| affine_flag   | bool                 | 是否开启affine功能                                                                                                           |
| interp_method | ai2d_interp_method   | Affine采用的插值方法                                                                                                         |
| cord_round    | uint32_t             | 整数边界0或者1                                                                                                               |
| bound_ind     | uint32_t             | 边界像素模式0或者1                                                                                                           |
| bound_val     | uint32_t             | 边界填充值                                                                                                                   |
| bound_smooth  | uint32_t             | 边界平滑0或者1                                                                                                               |
| M             | std::vector\<float\> | 仿射变换矩阵对应的vector，仿射变换为$Y=\[a_0, a_1; a_2, a_3\] \cdot X + \[b_0, b_1\] $, 则 $ M=\{a_0,a_1,b_0,a_2,a_3,b_1\} $ |

【示例】

```cpp
ai2d_affine_param_t affine_param { true, ai2d_interp_method::cv2_bilinear, 0, 0, 127, 1, { 0.5, 0.1, 0.0, 0.1, 0.5, 0.0 } };
```

## API 介绍

### ai2d_builder:: ai2d_builder

【描述】

ai2d_builder的构造函数。

【定义】

```cpp
ai2d_builder(dims_t &input_shape, dims_t &output_shape, ai2d_datatype_t ai2d_dtype, ai2d_crop_param_t crop_param, ai2d_shift_param_t shift_param, ai2d_pad_param_t pad_param, ai2d_resize_param_t resize_param, ai2d_affine_param_t affine_param);
```

【参数】

| 名称         | 类型                | 描述           |
| ------------ | ------------------- | -------------- |
| input_shape  | dims_t              | 输入形状       |
| output_shape | dims_t              | 输出形状       |
| ai2d_dtype   | ai2d_datatype_t     | ai2d数据类型   |
| crop_param   | ai2d_crop_param_t   | crop相关参数   |
| shift_param  | ai2d_shift_param_t  | shift相关参数  |
| pad_param    | ai2d_pad_param_t    | pad相关参数    |
| resize_param | ai2d_resize_param_t | resize相关参数 |
| affine_param | ai2d_affine_param_t | affine相关参数 |

【返回值 】

无

【示例】

```cpp
dims_t in_shape { 1, ai2d_input_c_, ai2d_input_h_, ai2d_input_w_ };          
auto out_span = ai2d_out_tensor_.shape();                                    
dims_t out_shape { out_span.begin(), out_span.end() };                       
ai2d_datatype_t ai2d_dtype { ai2d_format::NCHW_FMT, ai2d_format::NCHW_FMT, typecode_t::dt_uint8, typecode_t::dt_uint8 };
ai2d_crop_param_t crop_param { false, 0, 0, 0, 0 };                          
ai2d_shift_param_t shift_param { false, 0 };                                 
ai2d_pad_param_t pad_param { true, { { 0, 0 }, { 0, 0 }, { 0, 0 }, { 70, 70 } }, ai2d_pad_mode::constant, { 0, 0, 0 } };
ai2d_resize_param_t resize_param { true, ai2d_interp_method::tf_bilinear, ai2d_interp_mode::half_pixel };
ai2d_affine_param_t affine_param { false };                                  
ai2d_builder_.reset(new ai2d_builder(in_shape, out_shape, ai2d_dtype, crop_param, shift_param, pad_param, resize_param, affine_param));
```

### ai2d_builder:: build_schedule

【描述】

生成AI2D计算需要的参数。

【定义】

```c++
result<void> build_schedule();
```

【参数】

无。

【返回值】

`result<void>`

【示例】

```c++
ai2d_builder_->build_schedule();
```

### ai2d_builder::invoke

【描述】

配置寄存器并启动AI2D的计算。

【定义】

```c++
result<void> invoke(runtime_tensor &input, runtime_tensor &output);
```

【参数】

| 名称   | 类型           | 描述       |
| ------ | -------------- | ---------- |
| input  | runtime_tensor | 输入tensor |
| output | runtime_tensor | 输出tensor |

【返回值 】

result\<void\>。

【示例】

```c++
// run ai2d                                                                  
ai2d_builder_->invoke(ai2d_in_tensor, ai2d_out_tensor_).expect("error occurred in ai2d running");
```

## 示例

```cpp
static void test_pad_mini_test(const char *gmodel_file, const char *expect_file)
{
    // input tensor
    dims_t in_shape { 1, 100, 150, 3 };
    auto in_tensor = host_runtime_tensor::create(dt_uint8, in_shape, hrt::pool_shared).expect("cannot create input tensor");
    auto mapped_in_buf = std::move(hrt::map(in_tensor, map_access_t::map_write).unwrap());
    read_binary_file(gmodel_file, reinterpret_cast<char *>(mapped_in_buf.buffer().data()));
    mapped_in_buf.unmap().expect("unmap input tensor failed");
    hrt::sync(in_tensor, sync_op_t::sync_write_back, true).expect("write back input failed");

    // output tensor
    dims_t out_shape { 1, 100, 160, 3 };
    auto out_tensor = host_runtime_tensor::create(dt_uint8, out_shape, hrt::pool_shared).expect("cannot create output tensor");

    // config ai2d，这里配置的是padding预处理
    ai2d_datatype_t ai2d_dtype { ai2d_format::RGB_packed, ai2d_format::RGB_packed, dt_uint8, dt_uint8 };
    ai2d_crop_param_t crop_param { false, 0, 0, 0, 0 };
    ai2d_shift_param_t shift_param { false, 0 };
    ai2d_pad_param_t pad_param { true, { { 0, 0 }, { 0, 0 }, { 0, 0 }, { 10, 0 } }, ai2d_pad_mode::constant, { 255, 10, 5 } };
    ai2d_resize_param_t resize_param { false, ai2d_interp_method::tf_bilinear, ai2d_interp_mode::half_pixel };
    ai2d_affine_param_t affine_param { false };

    // run
    ai2d_builder builder { in_shape, out_shape, ai2d_dtype, crop_param, shift_param, pad_param, resize_param, affine_param };
    auto start = std::chrono::steady_clock::now();
    builder.build_schedule().expect("error occurred in ai2d build_schedule");
    builder.invoke(in_tensor, out_tensor).expect("error occurred in ai2d invoke");
    auto stop = std::chrono::steady_clock::now();
    double duration = std::chrono::duration<double, std::milli>(stop - start).count();
    std::cout << "ai2d run: duration = " << duration << " ms, fps = " << 1000 / duration << std::endl;

    // compare
    auto mapped_out_buf = std::move(hrt::map(out_tensor, map_access_t::map_read).unwrap());
    auto actual = mapped_out_buf.buffer().data();
    auto expected = read_binary_file<unsigned char>(expect_file);
    int ret = memcmp(reinterpret_cast<void *>(actual), reinterpret_cast<void *>(expected.data()), expected.size());
    if (!ret)
    {
        std::cout << "compare output succeed!" << std::endl;
    }
    else
    {
        auto cos = cosine(reinterpret_cast<const uint8_t *>(actual), reinterpret_cast<const uint8_t *>(expected.data()), expected.size());
        std::cerr << "compare output failed: cosine similarity = " << cos << std::endl;
    }
}
```

上述代码需要在 `k230 linux sdk` 环境下使用编译工具编译成 `elf` 可执行文件，然后拷贝到开发板运行。
