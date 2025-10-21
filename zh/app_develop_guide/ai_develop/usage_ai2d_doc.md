# AI2D 应用指南

## 概述

`AI2D` 提供了使用硬件处理的5种预处理方法，包括 `Crop/Shift/Resize/Pad/Affine` 。 比如其中的 `Pad` 和 `Resize` 可以实现目标检测任务中常用的 `letterbox` 操作。AI2D 运行时主要在编写开发板部署代码时使用，提供C++版本的API。下文给出的示例源码位于 `k230_linux_sdk/buildroot-overlay/package/usage_ai2d` 目录下，执行 `build_app.sh` 即可进行编译，编译生成物在 `k230_bin` 目录下，将生成物拷贝到开发板上即可运行。请注意 `AI2D` 的使用注意事项。

> 注意：
>
> 1、Affine和Resize功能是互斥的，不能同时开启；
> 2、Shift功能的输入格式只能是Raw16；
> 3、Pad value是按通道配置的，对应的list元素个数要与channel数相等；
> 4、当前版本中，当只需要AI2D的一个功能时，其他参数也需要配置，flag置为false即可，其他字段不用配置；
> 5、当配置了多个功能时，执行顺序是Crop->Shift->Resize/Affine->Pad, 配置参数时注意要匹配。
> 6、在linux下使用ai2d的时候需要加载一个kmodel完成部分初始化操作。

## 预处理方法

### Resize 方法

`Resize` 方法是一种在图片预处理中广泛使用的操作，它主要用于改变图像的尺寸大小。无论是放大还是缩小图像，都可以通过这个方法来实现。源码位于 `k230_linux_sdk/buildroot-overlay/package/usage_ai2d/test_resize` 目录下。实现`Resize` 的流程如下：

<div class="mermaid">
graph TD;
    ReadData("读取数据<br>(from pictures/camera)") -->SetInput("初始化AI2D输入tensor")-->SetOutput("根据预处理后的shape<br>初始化AI2D输出tensor")-->SetParam("配置Resize参数<br>ai2d_resize_param_t")-->InitBuilder("构造ai2d_builder实例<br>执行build_schedule")-->Run("调用invoke接口运行配置的预处理方法")-->GetOutput("从配置的AI2D输出tensor处获取输出数据");
</div>

这里给出使用 `AI2D` 实现 `Resize` 过程的示例代码，实现将读入的图片`resize`成`640*320`分辨率的图像。

```c++
int main(int argc, char *argv[])
{
    std::cout << "case " << argv[0] << " build " << __DATE__ << " " << __TIME__ << std::endl;
    if (argc < 3)
    {
        std::cerr << "Usage: " << argv[0] << "<image> <debug_mode>" << std::endl;
        return -1;
    }

    int debug_mode=atoi(argv[2]);

    // 读入图片，并将数据处理成CHW和RGB格式
    cv::Mat ori_img = cv::imread(argv[1]);
    int ori_w = ori_img.cols;
    int ori_h = ori_img.rows;
    std::vector<uint8_t> chw_vec;
    std::vector<cv::Mat> bgrChannels(3);
    cv::split(ori_img, bgrChannels);
    for (auto i = 2; i > -1; i--)
    {
        std::vector<uint8_t> data = std::vector<uint8_t>(bgrChannels[i].reshape(1, 1));
        chw_vec.insert(chw_vec.end(), data.begin(), data.end());
    }

    // 创建AI2D输入tensor，并将CHW_RGB数据拷贝到tensor中，并回写到DDR
    dims_t ai2d_in_shape{1, 3, ori_h, ori_w};
    runtime_tensor ai2d_in_tensor = host_runtime_tensor::create(typecode_t::dt_uint8, ai2d_in_shape, hrt::pool_shared).expect("cannot create input tensor");
    auto input_buf = ai2d_in_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_write).unwrap().buffer();
    memcpy(reinterpret_cast<char *>(input_buf.data()), chw_vec.data(), chw_vec.size());
    hrt::sync(ai2d_in_tensor, sync_op_t::sync_write_back, true).expect("write back input failed");

    // resize参数
    int out_w=640;
    int out_h=320;
    int size=out_w*out_h;

    // 创建AI2D输出tensor
    dims_t ai2d_out_shape{1, 3, out_h, out_w};
    runtime_tensor ai2d_out_tensor = host_runtime_tensor::create(typecode_t::dt_uint8, ai2d_out_shape, hrt::pool_shared).expect("cannot create input tensor");

    // 设置AI2D参数，AI2D支持5种预处理方法，crop/shift/pad/resize/affine。这里开启resize
    ai2d_datatype_t ai2d_dtype{ai2d_format::NCHW_FMT, ai2d_format::NCHW_FMT, ai2d_in_tensor.datatype(), ai2d_out_tensor.datatype()};
    ai2d_crop_param_t crop_param{false, 0, 0, 0, 0};
    ai2d_shift_param_t shift_param{false, 0};
    ai2d_pad_param_t pad_param{false, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}, ai2d_pad_mode::constant, {0,0,0}};
    ai2d_resize_param_t resize_param{true, ai2d_interp_method::tf_bilinear, ai2d_interp_mode::half_pixel};
    ai2d_affine_param_t affine_param{false, ai2d_interp_method::cv2_bilinear, 0, 0, 127, 1, {0.5, 0.1, 0.0, 0.1, 0.5, 0.0}};

    // 构造ai2d_builder
    ai2d_builder builder(ai2d_in_shape, ai2d_out_shape, ai2d_dtype, crop_param, shift_param, pad_param, resize_param, affine_param);
    builder.build_schedule();
    // 执行ai2d，实现从ai2d_in_tensor->ai2d_out_tensor的预处理过程
    builder.invoke(ai2d_in_tensor,ai2d_out_tensor).expect("error occurred in ai2d running");

    //获取处理结果，并将结果存成图片
    auto output_buf = ai2d_out_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_write).unwrap().buffer();
    cv::Mat image_r = cv::Mat(out_h, out_w, CV_8UC1, output_buf.data());
    cv::Mat image_g = cv::Mat(out_h, out_w, CV_8UC1, output_buf.data()+size);
    cv::Mat image_b = cv::Mat(out_h, out_w, CV_8UC1, output_buf.data()+2*size);
    
    std::vector<cv::Mat> color_vec(3);
    color_vec.clear();
    color_vec.push_back(image_b);
    color_vec.push_back(image_g);
    color_vec.push_back(image_r);
    cv::Mat color_img;
    cv::merge(color_vec, color_img);
    cv::imwrite("test_resize.jpg", color_img);

    return 0;
}
```

编译后在开发板上运行：

```shell
./test_resize.elf test.jpg 2
```

执行后原图和预处理后图像的对比图如下：

![resize_res](https://www.kendryte.com/api/post/attachment?id=507)

### Crop 方法

`Crop` 方法是一种用于从原始图像中提取（裁剪）出感兴趣区域（ROI，Region of Interest）的操作。它可以根据指定的坐标和尺寸，从图像中选取一部分作为新的图像。源码位于 `k230_linux_sdk/buildroot-overlay/package/usage_ai2d/test_crop` 。实现 `Crop` 的流程如下：

<div class="mermaid">
graph TD;
    ReadData("读取数据<br>(from pictures/camera)") -->SetInput("初始化AI2D输入tensor")-->SetOutput("根据预处理后的shape<br>初始化AI2D输出tensor")-->SetParam("配置Crop参数<br>ai2d_crop_param_t")-->InitBuilder("构造ai2d_builder实例<br>执行build_schedule")-->Run("调用invoke接口运行配置的预处理方法")-->GetOutput("从配置的AI2D输出tensor处获取输出数据");
</div>

这里给出使用 AI2D 实现 `Crop` 过程的示例代码，实现将读入的图片在`[10,10]`位置裁剪`[400,400]`分辨率的图像。

```c++
int main(int argc, char *argv[])
{
    std::cout << "case " << argv[0] << " build " << __DATE__ << " " << __TIME__ << std::endl;
    if (argc < 3)
    {
        std::cerr << "Usage: " << argv[0] << "<image> <debug_mode>" << std::endl;
        return -1;
    }

    int debug_mode=atoi(argv[2]);

    // 读入图片，并将数据处理成CHW和RGB格式
    cv::Mat ori_img = cv::imread(argv[1]);
    int ori_w = ori_img.cols;
    int ori_h = ori_img.rows;
    std::vector<uint8_t> chw_vec;
    std::vector<cv::Mat> bgrChannels(3);
    cv::split(ori_img, bgrChannels);
    for (auto i = 2; i > -1; i--)
    {
        std::vector<uint8_t> data = std::vector<uint8_t>(bgrChannels[i].reshape(1, 1));
        chw_vec.insert(chw_vec.end(), data.begin(), data.end());
    }

    // 创建AI2D输入tensor，并将CHW_RGB数据拷贝到tensor中，并回写到DDR
    dims_t ai2d_in_shape{1, 3, ori_h, ori_w};
    runtime_tensor ai2d_in_tensor = host_runtime_tensor::create(typecode_t::dt_uint8, ai2d_in_shape, hrt::pool_shared).expect("cannot create input tensor");
    auto input_buf = ai2d_in_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_write).unwrap().buffer();
    memcpy(reinterpret_cast<char *>(input_buf.data()), chw_vec.data(), chw_vec.size());
    hrt::sync(ai2d_in_tensor, sync_op_t::sync_write_back, true).expect("write back input failed");

    // crop参数
    int crop_x=10;
    int crop_y=10;
    int crop_w=400;
    int crop_h=400;

    // 创建AI2D输出tensor
    dims_t ai2d_out_shape{1, 3,crop_h, crop_w};
    runtime_tensor ai2d_out_tensor = host_runtime_tensor::create(typecode_t::dt_uint8, ai2d_out_shape, hrt::pool_shared).expect("cannot create input tensor");

    // 设置AI2D参数，AI2D支持5种预处理方法，crop/shift/pad/resize/affine。这里开启crop
    ai2d_datatype_t ai2d_dtype{ai2d_format::NCHW_FMT, ai2d_format::NCHW_FMT, ai2d_in_tensor.datatype(), ai2d_out_tensor.datatype()};
    ai2d_crop_param_t crop_param{true, crop_x, crop_y, crop_w, crop_h};
    ai2d_shift_param_t shift_param{false, 0};
    ai2d_pad_param_t pad_param{false, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}, ai2d_pad_mode::constant, {114, 114, 114}};
    ai2d_resize_param_t resize_param{false, ai2d_interp_method::tf_bilinear, ai2d_interp_mode::half_pixel};
    ai2d_affine_param_t affine_param{false, ai2d_interp_method::cv2_bilinear, 0, 0, 127, 1, {0.5, 0.1, 0.0, 0.1, 0.5, 0.0}};

    // 构造ai2d_builder
    ai2d_builder builder(ai2d_in_shape, ai2d_out_shape, ai2d_dtype, crop_param, shift_param, pad_param, resize_param, affine_param);
    builder.build_schedule();
    // 执行ai2d，实现从ai2d_in_tensor->ai2d_out_tensor的预处理过程
    builder.invoke(ai2d_in_tensor,ai2d_out_tensor).expect("error occurred in ai2d running");

    //获取处理结果，并将结果存成图片
    auto output_buf = ai2d_out_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_write).unwrap().buffer();
    cv::Mat image_r = cv::Mat(crop_h, crop_w, CV_8UC1, output_buf.data());
    cv::Mat image_g = cv::Mat(crop_h, crop_w, CV_8UC1, output_buf.data()+crop_h*crop_w);
    cv::Mat image_b = cv::Mat(crop_h, crop_w, CV_8UC1, output_buf.data()+2*crop_h*crop_w);
    
    std::vector<cv::Mat> color_vec(3);
    color_vec.clear();
    color_vec.push_back(image_b);
    color_vec.push_back(image_g);
    color_vec.push_back(image_r);
    cv::Mat color_img;
    cv::merge(color_vec, color_img);
    cv::imwrite("test_crop.jpg", color_img);

    return 0;
}
```

编译后在开发板上运行：

```shell
./test_crop.elf test.jpg 2
```

执行后原图和预处理后图像的对比图如下：

![crop_res](https://www.kendryte.com/api/post/attachment?id=505)

### Pad 方法

`Pad`（填充）方法是一种在图片预处理阶段，对图像边缘进行填充操作的技术。它通过在图像的四周（上下左右）添加像素值，来改变图像的尺寸大小。这些添加的像素值可以自定义。源码位于 `k230_linux_sdk/buildroot-overlay/package/usage_ai2d/test_pad` 。实现 `Pad` 的流程如下：

<div class="mermaid">
graph TD;
    ReadData("读取数据<br>(from pictures/camera)") -->SetInput("初始化AI2D输入tensor")-->SetOutput("根据预处理后的shape<br>初始化AI2D输出tensor")-->SetParam("配置Pad参数<br>ai2d_pad_param_t")-->InitBuilder("构造ai2d_builder实例<br>执行build_schedule")-->Run("调用invoke接口运行配置的预处理方法")-->GetOutput("从配置的AI2D输出tensor处获取输出数据");
</div>

这里给出使用 AI2D 实现 `Pad` 过程的示例代码,实现将读入的图片在上下左右分别填充100、100、200、200像素的图像。

```c++
int main(int argc, char *argv[])
{
    std::cout << "case " << argv[0] << " build " << __DATE__ << " " << __TIME__ << std::endl;
    if (argc < 3)
    {
        std::cerr << "Usage: " << argv[0] << "<image> <debug_mode>" << std::endl;
        return -1;
    }

    int debug_mode=atoi(argv[2]);

    // 读入图片，并将数据处理成CHW和RGB格式
    cv::Mat ori_img = cv::imread(argv[1]);
    int ori_w = ori_img.cols;
    int ori_h = ori_img.rows;
    std::vector<uint8_t> chw_vec;
    std::vector<cv::Mat> bgrChannels(3);
    cv::split(ori_img, bgrChannels);
    for (auto i = 2; i > -1; i--)
    {
        std::vector<uint8_t> data = std::vector<uint8_t>(bgrChannels[i].reshape(1, 1));
        chw_vec.insert(chw_vec.end(), data.begin(), data.end());
    }

    // 创建AI2D输入tensor，并将CHW_RGB数据拷贝到tensor中，并回写到DDR
    dims_t ai2d_in_shape{1, 3, ori_h, ori_w};
    runtime_tensor ai2d_in_tensor = host_runtime_tensor::create(typecode_t::dt_uint8, ai2d_in_shape, hrt::pool_shared).expect("cannot create input tensor");
    auto input_buf = ai2d_in_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_write).unwrap().buffer();
    memcpy(reinterpret_cast<char *>(input_buf.data()), chw_vec.data(), chw_vec.size());
    hrt::sync(ai2d_in_tensor, sync_op_t::sync_write_back, true).expect("write back input failed");

    // padding参数
    int pad_top=100;
    int pad_bottom=100;
    int pad_left=200;
    int pad_right=200;
    std::vector<int> pad_val={114,114,114};
    int out_w=ori_w+pad_left+pad_right;
    int out_h=ori_h+pad_top+pad_bottom;
    int size=(ori_w+pad_left+pad_right)*(ori_h+pad_top+pad_bottom);

    // 创建AI2D输出tensor
    dims_t ai2d_out_shape{1, 3, out_h, out_w};
    runtime_tensor ai2d_out_tensor = host_runtime_tensor::create(typecode_t::dt_uint8, ai2d_out_shape, hrt::pool_shared).expect("cannot create input tensor");

    // 设置AI2D参数，AI2D支持5种预处理方法，crop/shift/pad/resize/affine。这里开启pad
    ai2d_datatype_t ai2d_dtype{ai2d_format::NCHW_FMT, ai2d_format::NCHW_FMT, ai2d_in_tensor.datatype(), ai2d_out_tensor.datatype()};
    ai2d_crop_param_t crop_param{false, 0, 0, 0, 0};
    ai2d_shift_param_t shift_param{false, 0};
    ai2d_pad_param_t pad_param{true, {{0, 0}, {0, 0}, {pad_top, pad_bottom}, {pad_left, pad_right}}, ai2d_pad_mode::constant, pad_val};
    ai2d_resize_param_t resize_param{false, ai2d_interp_method::tf_bilinear, ai2d_interp_mode::half_pixel};
    ai2d_affine_param_t affine_param{false, ai2d_interp_method::cv2_bilinear, 0, 0, 127, 1, {0.5, 0.1, 0.0, 0.1, 0.5, 0.0}};

    // 构造ai2d_builder
    ai2d_builder builder(ai2d_in_shape, ai2d_out_shape, ai2d_dtype, crop_param, shift_param, pad_param, resize_param, affine_param);
    builder.build_schedule();
    // 执行ai2d，实现从ai2d_in_tensor->ai2d_out_tensor的预处理过程
    builder.invoke(ai2d_in_tensor,ai2d_out_tensor).expect("error occurred in ai2d running");

    //获取处理结果，并将结果存成图片
    auto output_buf = ai2d_out_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_write).unwrap().buffer();
    cv::Mat image_r = cv::Mat(out_h, out_w, CV_8UC1, output_buf.data());
    cv::Mat image_g = cv::Mat(out_h, out_w, CV_8UC1, output_buf.data()+size);
    cv::Mat image_b = cv::Mat(out_h, out_w, CV_8UC1, output_buf.data()+2*size);
    
    std::vector<cv::Mat> color_vec(3);
    color_vec.clear();
    color_vec.push_back(image_b);
    color_vec.push_back(image_g);
    color_vec.push_back(image_r);
    cv::Mat color_img;
    cv::merge(color_vec, color_img);
    cv::imwrite("test_pad.jpg", color_img);

    return 0;
}
```

编译后在开发板上运行：

```shell
./test_pad.elf test.jpg 2
```

执行后原图和预处理后图像的对比图如下：

![pad_res](https://www.kendryte.com/api/post/attachment?id=506)

### Affine 方法

`Affine`（仿射变换）方法是一种在图像预处理中用于对图像进行几何变换的技术。它可以实现图像的旋转、平移、缩放等多种几何变换操作，并且能够保持图像的 “平直性”（即直线在变换后仍然是直线）和 “平行性”（即平行的线在变换后仍然平行）。实现 `Affine` 的流程如下：

<div class="mermaid">
graph TD;
    ReadData("读取数据<br>(from pictures/camera)") -->SetInput("初始化AI2D输入tensor")-->SetOutput("根据预处理后的shape<br>初始化AI2D输出tensor")-->SetParam("配置Affine参数<br>ai2d_affine_param_t")-->InitBuilder("构造ai2d_builder实例<br>执行build_schedule")-->Run("调用invoke接口运行配置的预处理方法")-->GetOutput("从配置的AI2D输出tensor处获取输出数据");
</div>

这里给出使用 AI2D 实现 `Affine` 过程的示例代码，实现将读入的图片缩放0.5倍，并分别在x,y方向平移200像素的图像。

```c++
int main(int argc, char *argv[])
{
    std::cout << "case " << argv[0] << " build " << __DATE__ << " " << __TIME__ << std::endl;
    if (argc < 3)
    {
        std::cerr << "Usage: " << argv[0] << "<image> <debug_mode>" << std::endl;
        return -1;
    }

    int debug_mode=atoi(argv[2]);

    // 读入图片，并将数据处理成CHW和RGB格式
    cv::Mat ori_img = cv::imread(argv[1]);
    int ori_w = ori_img.cols;
    int ori_h = ori_img.rows;
    std::vector<uint8_t> chw_vec;
    std::vector<cv::Mat> bgrChannels(3);
    cv::split(ori_img, bgrChannels);
    for (auto i = 2; i > -1; i--)
    {
        std::vector<uint8_t> data = std::vector<uint8_t>(bgrChannels[i].reshape(1, 1));
        chw_vec.insert(chw_vec.end(), data.begin(), data.end());
    }

    // 创建AI2D输入tensor，并将CHW_RGB数据拷贝到tensor中，并回写到DDR
    dims_t ai2d_in_shape{1, 3, ori_h, ori_w};
    runtime_tensor ai2d_in_tensor = host_runtime_tensor::create(typecode_t::dt_uint8, ai2d_in_shape, hrt::pool_shared).expect("cannot create input tensor");
    auto input_buf = ai2d_in_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_write).unwrap().buffer();
    memcpy(reinterpret_cast<char *>(input_buf.data()), chw_vec.data(), chw_vec.size());
    hrt::sync(ai2d_in_tensor, sync_op_t::sync_write_back, true).expect("write back input failed");

    // affine参数,创建仿射变换矩阵，缩放0.5倍，X/Y方向各平移200px
    std::vector<float> affine_matrix = {0.5,0.0,200.0,
                                        0.0,0.5,200.0};
    int out_w=0.5*ori_w;
    int out_h=0.5*ori_h;
    int size=out_w*out_h;

    // 创建AI2D输出tensor
    dims_t ai2d_out_shape{1, 3, out_h, out_w};
    runtime_tensor ai2d_out_tensor = host_runtime_tensor::create(typecode_t::dt_uint8, ai2d_out_shape, hrt::pool_shared).expect("cannot create input tensor");

    // 设置AI2D参数，AI2D支持5种预处理方法，crop/shift/pad/resize/affine。这里开启affine
    ai2d_datatype_t ai2d_dtype{ai2d_format::NCHW_FMT, ai2d_format::NCHW_FMT, ai2d_in_tensor.datatype(), ai2d_out_tensor.datatype()};
    ai2d_crop_param_t crop_param{false, 0, 0, 0, 0};
    ai2d_shift_param_t shift_param{false, 0};
    ai2d_pad_param_t pad_param{false, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}, ai2d_pad_mode::constant, {0,0,0}};
    ai2d_resize_param_t resize_param{false, ai2d_interp_method::tf_bilinear, ai2d_interp_mode::half_pixel};
    ai2d_affine_param_t affine_param{true, ai2d_interp_method::cv2_bilinear, 0, 0, 127, 1, affine_matrix};

    // 构造ai2d_builder
    ai2d_builder builder(ai2d_in_shape, ai2d_out_shape, ai2d_dtype, crop_param, shift_param, pad_param, resize_param, affine_param);
    builder.build_schedule();
    // 执行ai2d，实现从ai2d_in_tensor->ai2d_out_tensor的预处理过程
    builder.invoke(ai2d_in_tensor,ai2d_out_tensor).expect("error occurred in ai2d running");

    //获取处理结果，并将结果存成图片
    auto output_buf = ai2d_out_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_write).unwrap().buffer();
    cv::Mat image_r = cv::Mat(out_h, out_w, CV_8UC1, output_buf.data());
    cv::Mat image_g = cv::Mat(out_h, out_w, CV_8UC1, output_buf.data()+size);
    cv::Mat image_b = cv::Mat(out_h, out_w, CV_8UC1, output_buf.data()+2*size);
    
    std::vector<cv::Mat> color_vec(3);
    color_vec.clear();
    color_vec.push_back(image_b);
    color_vec.push_back(image_g);
    color_vec.push_back(image_r);
    cv::Mat color_img;
    cv::merge(color_vec, color_img);
    cv::imwrite("test_affine.jpg", color_img);

    return 0;
}
```

编译后在开发板上运行：

```shell
./test_affine.elf test.jpg 2
```

执行后原图和预处理后图像的对比图如下：

![affine_res](https://www.kendryte.com/api/post/attachment?id=504)

### Shift 方法

`Shift` 方法是数据预处理中比特位右移的方法，每右移一位原数据变为原来的1/2。需要注意的是 `Shift` 的输入数据格式必须为 `RAW16` 。 实现 `Affine` 的流程如下：

<div class="mermaid">
graph TD;
    ReadData("读取数据<br>(from pictures/camera)") -->SetInput("初始化AI2D输入tensor")-->SetOutput("根据预处理后的shape<br>初始化AI2D输出tensor")-->SetParam("配置Shift参数<br>ai2d_shift_param_t")-->InitBuilder("构造ai2d_builder实例<br>执行build_schedule")-->Run("调用invoke接口运行配置的预处理方法")-->GetOutput("从配置的AI2D输出tensor处获取输出数据");
</div>

这里给出使用 AI2D 实现 `Shift` 过程的示例代码，这里创建了一个全为240的数据，通过 `Shift` 右移一位，将所有的数据变成120。

```c++
int main(int argc, char *argv[])
{
    std::cout << "case " << argv[0] << " build " << __DATE__ << " " << __TIME__ << std::endl;
    if (argc < 2)
    {
        std::cerr << "Usage: " << argv[0] << "<debug_mode:0,1,2>" << std::endl;
        return -1;
    }

    int debug_mode=atoi(argv[1]);

    // 创建一张位深为16的原始数据，初始化为240
    cv::Mat ori_img(320, 320, CV_16UC3, cv::Scalar(240, 240, 240));
    cv::imwrite("ori_img.jpg",ori_img);

    //hwc,bgr
    int ori_w = ori_img.cols;
    int ori_h = ori_img.rows;
    
    // 创建AI2D输入tensor
    dims_t ai2d_in_shape{1,ori_h, ori_w,3};
    runtime_tensor ai2d_in_tensor = host_runtime_tensor::create(typecode_t::dt_uint16, ai2d_in_shape, hrt::pool_shared).expect("cannot create input tensor");
    auto input_buf = ai2d_in_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_write).unwrap().buffer();
    memcpy(reinterpret_cast<uint16_t *>(input_buf.data()), ori_img.data , ori_h*ori_w*3*sizeof(uint16_t));
    hrt::sync(ai2d_in_tensor, sync_op_t::sync_write_back, true).expect("write back input failed");

    int out_w=ori_w;
    int out_h=ori_h;
    // 创建AI2D输出tensor
    dims_t ai2d_out_shape{1,out_h, out_w,3};
    runtime_tensor ai2d_out_tensor = host_runtime_tensor::create(typecode_t::dt_uint16, ai2d_out_shape, hrt::pool_shared).expect("cannot create input tensor");

    // 设置AI2D参数，AI2D支持5种预处理方法，crop/shift/pad/resize/affine。这里开启shift,右移1位，数据变为原来的1/2
    ai2d_datatype_t ai2d_dtype{ai2d_format::RAW16, ai2d_format::RAW16, ai2d_in_tensor.datatype(), ai2d_out_tensor.datatype()};
    ai2d_crop_param_t crop_param{false, 0, 0, 0, 0};
    ai2d_shift_param_t shift_param{true, 1};
    ai2d_pad_param_t pad_param{false, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}, ai2d_pad_mode::constant, {0,0,0}};
    ai2d_resize_param_t resize_param{false, ai2d_interp_method::tf_bilinear, ai2d_interp_mode::half_pixel};
    ai2d_affine_param_t affine_param{false, ai2d_interp_method::cv2_bilinear, 0, 0, 127, 1, {0.5, 0.1, 0.0, 0.1, 0.5, 0.0}};

    // 构造ai2d_builder
    ai2d_builder builder(ai2d_in_shape, ai2d_out_shape, ai2d_dtype, crop_param, shift_param, pad_param, resize_param, affine_param);
    builder.build_schedule();
    // 执行ai2d，实现从ai2d_in_tensor->ai2d_out_tensor的预处理过程
    builder.invoke(ai2d_in_tensor,ai2d_out_tensor).expect("error occurred in ai2d running");

    //获取处理结果，并将结果存成图片
    auto output_buf = ai2d_out_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_write).unwrap().buffer();
    cv::Mat image_r = cv::Mat(out_h, out_w, CV_16UC3, output_buf.data());
    cv::imwrite("test_shift.jpg", image_r);

    return 0;
}
```

编译后在开发板上运行：

```shell
./test_shift.elf 2
```

执行后原图和预处理后图像的对比图如下：

![shift_res](https://www.kendryte.com/api/post/attachment?id=508)
