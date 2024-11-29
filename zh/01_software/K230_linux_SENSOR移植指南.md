# K230 linux SENSOR 移植教程

本文档主要描述K230平台Camera Sensor基本框架以及如何新增支持一款新的Camera Sensor。

K230平台只支持mipi接口类型的sensor，我们以当前最常用的MIPI CSI接口Sensor为例进行说明。Sensor与主控平台的硬件连接示意图如下：

![文本, 信件 描述已自动生成](https://developer.canaan-creative.com/api/post/attachment?id=464)

主控通过I2C接口下发配置寄存器控制sensor的工作方式，sensor通过MIPI CSI接口将图像数据发送至主控SOC。

## 1. Sensor适配准备工作

用户在适配新的sensor之前需要做以下一些准备工作：

1. 从正规渠道获取 Sensor datasheet、初始化序列。
1. 查看 Sensor datasheet 和相关应用手册，特别关注 Sensor 曝光、增益控制方法，不同模式下曝光和增益的限制，长曝光实现方法，黑电平值，bayer 数据输出顺序等。
1. 跟 Sensor 厂家索要所需模式初始化序列，了解各序列的数据数率，Sensor 输出总的宽高，精确的帧率是多少等。
1. 确认 Sensor 控制接口是 I2C、SPI 还是其他接口，Sensor 的设备地址可以通过硬件设置。对于多个摄像头的场景，sensor 尽量不要复用 I2C 总线。不同场景的Sensor IO 电平可能是 1.8V 或者 3.3V，设计时需要保证 sensor 的 IO 电平与SOC 对应的 GPIO 供电电压一致。如 sensor 电平是 1.8V，则用于 sensor 控制的GPIO，如 Reset，I2C，PRDN，需要使用 1.8V 供电。
1. 确认 Sensor 输出数据接口和协议类型。当前仅支持MIPI CSI接口。
1. 确认 wdr mode 是 VC、DT 或者 DOL 等。
1. 确认不同时序是否需要图像裁剪。

## 2. Sensor适配示例

本节将按照如何增加支持一个新的camera sensor的步骤来进行详细描述。

这里以ov5647驱动作为示例进行说明，对应的驱动文件源码路径如下：

```shell
k230_linux_sdk/buildroot-overlay/package/vvcam/src/
```

### 2.1 定义支持的sensor类型

查看当前linux sensor 的默认配置

```shell
[root@canaan /sharefs/isp_linux ]#cat /proc/vsi/isp_subdev0
/******sensor configuration******/
isp0 port0:
sensor   : ov5647
mode     : 0
xml      : /etc/vvcam/ov5647.xml
manu_json: /etc/vvcam/ov5647.manual.json
auto_json: /etc/vvcam/ov5647.auto.json
*********************************
```

可以看出当前的默认sensor 是 ov5647、对应的配置文件在/etc/vvcam/ 目录下的ov5647.manual.json，ov5647.xml，ov5647.auto.json。

### 2.2 sensor驱动适配

sensor驱动适配在整个环节中最重要的环节，用户可以通过拷贝现有的sensor驱动文件来修改，其中关于sensor的AE相关寄存器配置和计算方式需要查看对应的手册或者寻求专业人事协助。

#### 2.2.1 定义sensor寄存器配置列表

sensor寄存器配置由数据类型 k_sensor_reg_list 定义：

```c
struct reg_list {
    uint16_t addr;
    uint8_t value;
};
```

以下是ov5647的寄存器配置列表

```c
static const reg_list ov5647_1920x1080_30fps[] = {
    //pixel_rate = 81666700
    {0x0103, 0x01},
    {0x0100, 0x00},
    {0x3034, 0x1a},
    {0x3035, 0x21},
    ...
    {0x3501, 0x02},
    {0x3502, 0xa0},
    {0x3503, 0x07},
    {0x350b, 0x10},
    {0, 0x00},
};
```

#### 2.2.2 定义sensor支持的模式

sensor的模式参数由数据类型ov5647_mode 定义

```c
struct ov5647_mode {
    struct vvcam_sensor_mode mode;
    struct reg_list* regs;
};
```

以下是ov5647的支持的模式

```c
static struct ov5647_mode modes[] = {
    {
        .mode = {
            .clk = 25000000,
            .width = 1920,
            .height = 1080,
            .lanes = VVCAM_SENSOR_2LANE,
            .freq = VVCAM_SENSOR_800M,
            .bayer = VVCAM_BAYER_PAT_GBRG,
            .bit_width = 10,
            .ae_info = {
                .frame_length = 1199,
                .cur_frame_length = 1199,
                .one_line_exp_time = 0.000027808,
                .gain_accuracy = 1024,
                .min_gain = 1.0,
                .max_gain = 8.0,
                .int_time_delay_frame = 2,
                .gain_delay_frame = 2,
                .color_type = 0,
                .integration_time_increment = 0.000027808,
                .gain_increment = (1.0f/16.0f),
                .max_long_integraion_line = 1199 - 12,
                .min_long_integraion_line = 2,
                .max_integraion_line = 1199 - 12,
                .min_integraion_line = 2,
                .max_long_integraion_time = 0.000027808 * (1199 - 12),
                .min_long_integraion_time = 0.000027808 * 2,
                .max_integraion_time = 0.000027808 * (1199 - 12),
                .min_integraion_time = 0.000027808 * 2,
                .cur_long_integration_time = 0.0,
                .cur_integration_time = 0.0,
                .cur_long_again = 0.0,
                .cur_long_dgain = 0.0,
                .cur_again = 0.0,
                .cur_dgain = 0.0,
                .a_long_gain.min = 1.0,
                .a_long_gain.max = 8.0,
                .a_long_gain.step = (1.0f/16.0f),
                .a_gain.min = 1.0,
                .a_gain.max = 8.0,
                .a_gain.step = (1.0f/16.0f),
                .d_long_gain.max = 1.0,
                .d_long_gain.min = 1.0,
                .d_long_gain.step = (1.0f/1024.0f),
                .d_gain.max = 1.0,
                .d_gain.min = 1.0,
                .d_gain.step = (1.0f/1024.0f),
                .cur_fps = 30,
            }
        },
        .regs = ov5647_1920x1080_30fps
    }
};
```

#### 2.2.3 实现sensor操作接口

sensor的操作接口由数据类型k_sensor_function定义，用户根据实际情况实现相关的操作接口，不是所有接口都必须实现。

```c
struct vvcam_sensor_ctrl {
    int (*init)(void** ctx);
    void (*deinit)(void* ctx);
    int (*enum_mode)(void* ctx, uint32_t index, struct vvcam_sensor_mode* mode);
    int (*get_mode)(void* ctx, struct vvcam_sensor_mode* mode);
    int (*set_mode)(void* ctx, uint32_t index);
    int (*set_stream)(void* ctx, bool on);
    int (*set_analog_gain)(void* ctx, float gain);
    int (*set_digital_gain)(void* ctx, float gain);
    int (*set_int_time)(void* ctx, float time);
};
```

以下是ov5647的支持的模式

```c
struct vvcam_sensor vvcam_ov5647 = {
    .name = "ov5647",
    .ctrl = {
        .init = init,
        .deinit = deinit,
        .enum_mode = enum_mode,
        .get_mode = get_mode,
        .set_mode = set_mode,
        .set_stream = set_stream,
        .set_analog_gain = set_analog_gain,
        .set_digital_gain = set_digital_gain,
        .set_int_time = set_int_time
    }
};
```

#### 2.2.4 更新sensor驱动列表

将上一节定义的sensor驱动结构体添加到lib.c中的vvcam_sensor_init 的函数中。
当前系统支持的sensor列表如下：

```c
void vvcam_sensor_init(void) {
    // get /dev/media0
    printf("k230 builtin sensor driver, built %s %s, API version %lu\n", __DATE__, __TIME__, VVCAM_API_VERSION);
    vvcam_sensor_add(&vvcam_ov5647);
    vvcam_sensor_add(&vvcam_imx335);
    vvcam_sensor_add(&vvcam_gc2093);
}
```

## 3. 编译sensor

按照上边从新配置好新的sensor 之后，需要从新编译sensor，编译命令如下

```shell
make vvcam-reconfigure
```

编译完成之后会生成一个新的libvvcam.so ，路径在：

```shell
k230_linux_sdk/output/k230_canmv_defconfig/target/usr/lib/libvvcam.so
```

## 4. 运行sensor

替换新的libvvcam.so 到 开发板 /usr/lib 下，然后修改对应的配置文件和sensor，配置命令如下。

首先kill isp_media_server, 命令如下：

```shell
killall isp_media_server
```

看默认的配置，默认的配置如下

```shell
[root@canaan /sharefs/isp_linux ]#cat /proc/vsi/isp_subdev0
/******sensor configuration******/
isp0 port0:
sensor   : ov5647
mode     : 0
xml      : /etc/vvcam/ov5647.xml
manu_json: /etc/vvcam/ov5647.manual.json
auto_json: /etc/vvcam/ov5647.auto.json
*********************************
```

配置新的sensor 和 配置文件

```shell
echo 0 sensor=imx335 > /proc/vsi/isp_subdev0
echo 0 mode=0 > /proc/vsi/isp_subdev0
echo 0 xml=/etc/vvcam/imx335.xml > /proc/vsi/isp_subdev0
echo 0 manu_json=/etc/vvcam/imx335.xml > /proc/vsi/isp_subdev0
echo 0 auto_json=/etc/vvcam/imx335.xml > /proc/vsi/isp_subdev0
```

配置完成之后从新查看配置文件

```shell
[root@canaan /sharefs/isp_linux ]#cat /proc/vsi/isp_subdev0
/******sensor configuration******/
isp0 port0:
sensor   : imx335
mode     : 0
xml      : /etc/vvcam/imx335.xml
manu_json: /etc/vvcam/imx335.xml
auto_json: /etc/vvcam/imx335.xml
*********************************
```

发现sensor 类型和配置文件都已经换成我们想要的配置文件和参数了

从新执行isp_media_server，运行命令如下：

```shell
ISP_MEDIA_SENSOR_DRIVER=/usr/lib/libvvcam.so /usr/bin/isp_media_server > /dev/null 2> /tmp/isp.err.log &
```

查看video 设备，会发现有多个video设备：

```shell
[root@canaan /sharefs/isp_linux ]#ls /dev/video
video0  video1  video2  video3  video4
```

运行测试命令

```shell
v4l2-drm -d 1 -w 640 -h 480
```

测试效果如下：

![文本, 信件 描述已自动生成](https://developer.canaan-creative.com/api/post/attachment?id=465)
