# K230 linux LCD 移植指南

本文档主要介绍视频输出系统控制模块的功能和用法，其它模块的功能和用法将各有专门的文档加以论述。

## 概述

VO（Video Output，视频输出）模块主动从内存相应位置读取视频和图形数据，并通过相应的显示设备输出视频和图形。芯片支持的显示/回写设备、视频层和图形层情况。

LAYER层支持：

|            | LAYER1             | LAYER3             | LAYER4                    |
|------------|--------------------|--------------------|---------------------------|
| 输入格式   | YUV420 NV12        | YUV420 NV12        | YUV420 NV12       |
| 最大分辨率 | 1920x1080          | 1920x1080          | 1920x1080                 |
| 叠加显示   | 支持可配置叠加顺序 | 支持可配置叠加顺序 | 支持可配置叠加顺序        |
| Rotation   | √                  | -                  | -                         |
| Scaler     | √                  | -                  | -                         |
| Mirror     | √                  | -                  | -                         |
| Gray       | √                  | -                  | -                         |
| 独立开关   | √                  | √                  | √                         |

OSD 层支持

|                    | OSD0                                                      | OSD1                                                      | OSD2                                                      | OSD3                                                      |
|--------------------|-----------------------------------------------------------|-----------------------------------------------------------|-----------------------------------------------------------|-----------------------------------------------------------|
| 输入格式           | RGB888  RGB565 ARGB8888 Monochrome-8-bit RGB4444 RGB1555  | RGB888  RGB565 ARGB8888 Monochrome-8-bit RGB4444 RGB1555  | RGB888  RGB565 ARGB8888 Monochrome-8-bit RGB4444 RGB1555  | RGB888  RGB565 ARGB8888 Monochrome-8-bit RGB4444 RGB1555  |
| 最大分辨率         | 1920x1080                                                 | 1920x1080                                                 | 1920x1080                                                 | 1920x1080                                                 |
| 叠加显示           | 支持可配置叠加顺序                                        | 支持可配置叠加顺序                                        | 支持可配置叠加顺序                                        | 支持可配置叠加顺序                                        |
| ARGB 265 等级ALPHA | √                                                         | √                                                         | √                                                         | √                                                         |
| 独立开关           | √                                                         | √                                                         | √                                                         | √                                                         |

## 软件描述

视频输出软件配置分为3部分配置：phy 配置、dsi配置、VO配置，

### 计算phy的pll

数据速率由 PLL 输出时钟相位频率的两倍给出：数据速率 (Gbps) = PLL Fout(GHz) \* 2，输出频率是输入参考频率和倍频/分频比的函数。 计算phy 的pll共分为4种范围做的计算，不同的频率对应着不同的频率，它可以通过以下方式确定：

| M      | m+2 |
|--------|-----|
| N      | n+1 |
| Fclkin | 24M |

For：

![文本, 信件 描述已自动生成](https://www.kendryte.com/api/post/attachment?id=449)

然而在这个需要遵循下边的限制：

![图片包含 文本 描述已自动生成](https://www.kendryte.com/api/post/attachment?id=450)

For：

![文本, 信件 描述已自动生成](https://www.kendryte.com/api/post/attachment?id=451)

For：

![文本, 信件 描述已自动生成](https://www.kendryte.com/api/post/attachment?id=473)

![文本 描述已自动生成](https://www.kendryte.com/api/post/attachment?id=453)

For：

![文本 中度可信度描述已自动生成](https://www.kendryte.com/api/post/attachment?id=454)

上边的每一个for 对应着一个pll的等级、不同的等级对应着不同的计算公式和限制，计算示例如下：

Example：

mipi 的速率为 445.5M：所以pll的速率就是222.75M，应该选择第二个公式，计算如下

222750000 = 1M / 2N = (m+2) / 2(n+1) \* 24000000 , 整理完成公式如下：

222.75n + 198.75 = 12m ，通过excel 计算如下：

![表格 描述已自动生成](https://www.kendryte.com/api/post/attachment?id=455)

得出来的m = 295 ，n = 15。

配置pll中的m 和n都是整数值、如果所有的值都不是整数，就需要在m 和 n的值做加1和减1处理、反推回去看哪个频率理你需要的最近，再去验证是否可用，不可以就重复上边的操作。

### 配置phy的voc

配置phy 的voc 可以根据表格查询即可：

![表格 描述已自动生成](https://www.kendryte.com/api/post/attachment?id=456)

![表格 描述已自动生成](https://www.kendryte.com/api/post/attachment?id=457)

Example：

mipi 的速率为 445.5M：所以pll的速率就是222.75M，voc = 010111 = 0x17

### 配置freq

配置phy 的freq 可以根据表格查询即可：

![表格 描述已自动生成](https://www.kendryte.com/api/post/attachment?id=458)

![表格 描述已自动生成](https://www.kendryte.com/api/post/attachment?id=459)

![表格 描述已自动生成](https://www.kendryte.com/api/post/attachment?id=460)

Example：

mipi 的速率为 445.5M：pll的速率就是222.75M，freq 选择0100101, 配置这个的时候需要将最高位bit\[7\] = 1，所有freq = 10100101= 0xa5

### 配置中断

drm 需要中断来触发每次的切换显示，下边是中断的计算和配置

```shell
vttr =  2^n ; 需要满足 vttr > Vtotal / 2
中断的行数 必须大于总行数的一办。
```

本次屏幕介绍以k230d Bpi 板子为例，配置路径如下

```shell
k230d Bpi dts 的路径：
linux/arch/riscv/boot/dts/canaan/bananapi-canmv-k230d-zero.dts：
k230d Bpi lcd dts 的路径：
linux/arch/riscv/boot/dts/canaan/display-st7701-480x800.dtsi ：

&vo {
    vth_line = <10>;
};
```

配置值为10， 2^10 = 1024 行 。

### 配置lcd驱动和时序

配置屏幕采用的是dsi 发送LP 的命令方式配置，具体的配置如下：

```shell
&dsi {
    ports {
        port@1 {
            reg = <1>;
            dsi_out_st7701: endpoint {
                remote-endpoint = <&st7701_in>;
            };
        };
    };

    lcd: panel@0 {
        compatible = "canaan,universal";
        reg = <0>;

        panel-width-mm = <480>;
        panel-height-mm = <800>;
        panel-dsi-lane = <2>;

        panel-init-sequence = [
            39 00 06 ff 77 01 00 00 13
            39 00 02 ef 08
            39 00 06 ff 77 01 00 00 10
            39 00 03 c0 63 00
            39 00 03 c1 10 02
            39 00 03 c2 31 02
            39 00 02 cc 10
            39 00 11 b0 c0 0c 92 0c 10 05 02 0d 07 21 04 53 11 6a 32 1f
            39 00 11 b1 c0 87 cf 0c 10 06 00 03 08 1d 06 54 12 e6 ec 0f
            39 00 06 ff 77 01 00 00 11
            39 00 02 b0 5d
            39 00 02 b1 62
            39 00 02 b2 82
            39 00 02 b3 80
            39 00 02 b5 42
            39 00 02 b7 85
            39 00 02 b8 20
            39 00 02 c0 09
            39 00 02 c1 78
            39 00 02 c2 78
            39 00 02 d0 88
            39 ff 02 ee 42
            39 00 04 e0 00 00 02
            39 00 0c e1 04 a0 06 a0 05 a0 07 a0 00 44 44
            39 00 0d e2 00 00 33 33 01 a0 00 00 01 a0 00 00
            39 00 05 e3 00 00 33 33
            39 00 03 e4 44 44
            39 00 11 e5 0c 30 a0 a0 0e 32 a0 a0 08 2c a0 a0 0a 2e a0 a0
            39 00 05 e6 00 00 33 33
            39 00 03 e7 44 44
            39 00 11 e8 0d 31 a0 a0 0f 33 a0 a0 09 2d a0 a0 0b 2f a0 a0
            39 00 08 eb 00 01 e4 e4 44 88 00
            39 00 11 ed ff f5 47 6f 0b a1 a2 bf fb 2a 1a b0 f6 74 5f ff
            39 00 07 ef 08 08 08 40 3f 64
            39 00 06 ff 77 01 00 00 13
            39 00 03 e8 00 0e
            39 00 06 ff 77 01 00 00 00
            39 ff 01 11
            39 00 06 ff 77 01 00 00 13
            39 ff 03 e8 00 0c
            39 00 03 e8 00 00
            39 00 06 ff 77 01 00 00 00
            39 00 02 3a 50
            39 ff 01 29
        ];

        display-timings {
            timing-0 {
                clock-frequency = <39600000>;
                hactive = <480>;
                vactive = <800>;
                hfront-porch = <80>;
                hback-porch = <20>;
                hsync-len = <20>;
                vfront-porch = <220>;
                vback-porch = <70>;
                vsync-len = <10>;
            };
        };

        ports {
            #address-cells = <1>;
            #size-cells = <0>;

            port@0 {
                reg = <0>;
                st7701_in: endpoint {
                    remote-endpoint = <&dsi_out_st7701>;
                };
            };
        };
    };
};
```

本次demo 以 Bpi 的st7701 为例，这个屏幕是一个480x800 的屏幕，参数解析如下：

- panel-width-mm ： 屏幕的宽度，Bpi 配置为480。
- panel-height-mm ：屏幕的高度，Bpi 配置为800。
- panel-dsi-lane ： 屏幕的lan数，Bpi 配置为2lan。
- panel-init-sequence ： 屏幕的参数，解析如下

```shell
15 00 02 80 77
|  |  |  |   |
|  |  |  |   data
|  |  |  | Register Address
|  |  Payload Length
|  Delay
Command type（0x05: Single byte data  0x15:Two byte data  0x39:Multi byte data）

Analysis：
Data Type: 0x15 (0x15 data type - DCS Short Write, 1 parameter)

Delay: 0x00 (Delay in ms after completing sending current packet before starting next command)

Payload Length: 0x02 (Payload length is 2 bytes)

Payload: 0x80 0x77 (Payload data)
```

上边介绍了屏幕的参数配置，这个是配置dsi 和 vo 按照这个时序去运行，下边介绍时序的配置，参数如下

```shell
display-timings {
    timing-0 {
        clock-frequency = <39600000>;
        hactive = <480>;
        vactive = <800>;
        hfront-porch = <80>;
        hback-porch = <20>;
        hsync-len = <20>;
        vfront-porch = <220>;
        vback-porch = <70>;
        vsync-len = <10>;
    };
};
```

解析参数如下：

- clock-frequency ： dsi pix clk 的频率，Bpi 配置为 39600000 k。
- hactive ： 有效宽度，Bpi 配置为480。
- vactive ： 有效高度，Bpi 配置为800。
- hfront-porch ：bfp，Bpi 配置为80。
- hback-porch ： hbp，Bpi 配置为20。
- hsync-len ： hsa，Bpi 配置为20。
- vfront-porch ： vfp ，Bpi 配置为220。
- vback-porch ： vbp ，Bpi 配置为70。
- vsync-len ： vbp ，Bpi 配置为10。

hsa、hbp、bfp hact 的单位都是pix， vsa、vbp、vfp vact 的单位都是行。

### phy 的配置

因为phy 的频率都是手动计算出来的不能自动计算出来、所以需要配置一下phy 的参数、配置方法如下

```shell
linux/drivers/gpu/drm/canaan/canaan_dsi.c：

static void canaan_dsi_encoder_enable(struct drm_encoder *encoder)
{
    struct canaan_dsi *dsi = encoder_to_canaan_dsi(encoder);
    struct drm_display_mode *adjusted_mode =
        &encoder->crtc->state->adjusted_mode;
    struct mipi_dsi_device *device = dsi->device;
    int dsi_test_en = 0;

    DRM_DEBUG_DRIVER("Enabling DSI output\n");

    dev_vdbg(dsi->dev, "DSI encoder enable %u\n", adjusted_mode->clock);
    switch (adjusted_mode->clock) {
    case 74250:
        // 74.25M
        k230_dsi_config_4lan_phy(dsi, TXPHY_445_5_M, TXPHY_445_5_N,
                     TXPHY_445_5_VOC, TXPHY_445_5_HS_FREQ);
        // set clk todo
        dsi->phy_freq = 445500;
        dsi->clk_freq = 74250;
        break;
    case 148500: {
        // 144.5M
        void *dis_clk = ioremap(0x91100000, 0x1000);
        u32 reg = 0;
        u32 div = 3;

        reg = readl(dis_clk + 0x78);
        reg = (reg & ~(GENMASK(10, 3))) | (div << 3); //  8M =    pll1(2376) / 4 / 66
        reg = reg | (1 << 31);
        writel(reg, dis_clk + 0x78);

        k230_dsi_config_4lan_phy(dsi, TXPHY_891_M, TXPHY_891_N,
                     TXPHY_891_VOC, TXPHY_891_HS_FREQ);
        // set clk todo
        dsi->phy_freq = 890666;
        dsi->clk_freq = 14850;
        break;
    }
    case 39600: {
        void *dis_clk = ioremap(0x91100000, 0x1000);
        u32 reg = 0;
        u32 div = 14;

        reg = readl(dis_clk + 0x78);
        reg = (reg & ~(GENMASK(10, 3))) |
              (div << 3); //  8M =    pll1(2376) / 4 / 66
        reg = reg | (1 << 31);
        writel(reg, dis_clk + 0x78);
        // 475.5M
        k230_dsi_config_4lan_phy(dsi, TXPHY_475_M, TXPHY_475_N,
                     TXPHY_475_VOC, TXPHY_475_HS_FREQ);
        // set clk todo
        dsi->phy_freq = 475200;
        dsi->clk_freq = 39600;
        break;
    }
    default:
        dev_err(dsi->dev, "MIPI clock not support\n");
        break;
    }
}
```

这快需要配置两部分，一部分是配置phy 的 参数、另一部分是配置pix 的clk，本次以39600为例，配置如下

首先配置pix clk，pix 计算如下：

![表格 描述已自动生成](https://www.kendryte.com/api/post/attachment?id=461)

只需要需改div 即可，Bpi 的板子配置pix clk 为 39.6M，根据上边 div = 15 ，但是配置从0 开始的，所以需要减1，div = （查表值） - 1

配置phy 的频率，这个根据上边的计算公式可以计算出M，N，VOC、FREQ 这四个参数（可以查看2.1章节），然后配置到下边函数即可

```shell
linux/drivers/gpu/drm/canaan/canaan_dsi.c：

k230_dsi_config_4lan_phy(dsi, TXPHY_475_M, TXPHY_475_N, TXPHY_475_VOC, TXPHY_475_HS_FREQ);
```

## HDMI 支持

目前在k230 canmv 和k230 01 studio 上都支持了 hdmi 显示，配置如下

```shell
linux/arch/riscv/boot/dts/canaan/k230-canmv.dts

/ {
    hdmi: connector {
        compatible = "hdmi-connector";
        label = "hdmi";
        type = "a";

        port {
            hdmi_connector_in: endpoint {
                remote-endpoint = <&lt9611_out>;
            };
        };
    };
};

&i2c4 {
    status = "okay";

    lt9611: hdmi-bridge@3b {
        compatible = "lontium,lt9611";
        reg = <0x3b>;
        reset-gpios = <&gpio1_ports 10 GPIO_ACTIVE_HIGH>;
        interrupt-parent = <&gpio1_ports>;
        interrupts = <11 IRQ_TYPE_EDGE_FALLING>;
        ports {
            #address-cells  = <1>;
            #size-cells     = <0>;
            port@1 {
                reg = <1>;
                lt9611_in: endpoint {
                    remote-endpoint = <&dsi_out_lt9611>;
                };
            };

            port@2 {
                reg = <2>;
                lt9611_out: endpoint {
                    remote-endpoint = <&hdmi_connector_in>;
                };
            };
        };
    };
};

&dsi {
    ports {
        port@1 {
            reg = <1>;
            dsi_out_lt9611: endpoint {
                remote-endpoint = <&lt9611_in>;
            };
        };
    };
};

```

主要是增加了lt9611 brange 芯片，需要移植可以参考这个dts

## 测试

本次测试采用的是modetest 的测试命令，具体测试如下

modetest -M canaan-drm  查看所有的参数

```shell
[root@canaan ~ ]#modetest -M canaan-drm
Encoders:
id crtc type possible crtcs possible clones
47 46 DSI 0x00000001 0x00000001

Connectors:
id encoder status  name size (mm) modes encoders
48 47 connected HDMI-A-1   600x340       4   47
  modes:
    index name refresh (Hz) hdisp hss hse htot vdisp vss vse vtot
  #0 1920x1080 60.00 1920 2008 2052 2200 1080 1084 1089 1125 148500 flags: phsync, pvsync; type: driver
  #1 1920x1080 59.94 1920 2008 2052 2200 1080 1084 1089 1125 148352 flags: phsync, pvsync; type: driver
  #2 1280x720 60.00 1280 1390 1430 1650 720 725 730 750 74250 flags: phsync, pvsync; type: driver
  #3 1280x720 59.94 1280 1390 1430 1650 720 725 730 750 74176 flags: phsync, pvsync; type: driver
  props:
    1 EDID:
        flags: immutable blob
        blobs:

        value:
            00ffffffffffff0010ac52d149365330
            0e200103803c2278eafa95a9534a9c24
            0e5054a54b00714f8180a9c0d1c00101
            010101010101565e00a0a0a029503020
            350056502100001a000000ff00474638
            364b4d330a2020202020000000fc0044
            454c4c205345323732334453000000fd
            00304b1d8c20000a2020202020200191
            020326f14a900504030201141f121323
            0907078301000065030c001000681a00
            000101304be6d2730080a0a01f502020
            350056502100001a2a4480a070382740
            3020350056502100001c023a80187138
            2d40582c450056502100001e00000000
            00000000000000000000000000000000
            00000000000000000000000000000015
    2 DPMS:
        flags: enum
        enums: On=0 Standby=1 Suspend=2 Off=3
        value: 0
    5 link-status:
        flags: enum
        enums: Good=0 Bad=1
        value: 0
    6 non-desktop:
        flags: immutable range
        values: 0 1
        value: 0
    4 TILE:
        flags: immutable blob
        blobs:

        value:

CRTCs:
id fb pos size
46 0 (0,0) (1920x1080)
  #0 1920x1080 60.00 1920 2008 2052 2200 1080 1084 1089 1125 148500 flags: phsync, pvsync; type: driver
  props:
    24 VRR_ENABLED:
        flags: range
        values: 0 1
        value: 0
    28 GAMMA_LUT:
        flags: blob
        blobs:

        value:
    29 GAMMA_LUT_SIZE:
        flags: immutable range
        values: 0 4294967295
        value: 256

Planes:
id crtc fb CRTC x,y x,y gamma size possible crtcs
31 0 0 0,0 0,0 0 0x00000001
  formats: NV12 NV21 NV16 NV61
  props:
    8 type:
        flags: immutable enum
        enums: Overlay=0 Primary=1 Cursor=2
        value: 0
    30 IN_FORMATS:
        flags: immutable blob
        blobs:

        value:
            01000000000000000400000018000000
            01000000280000004e5631324e563231
            4e5631364e5636310f00000000000000
            00000000000000000000000000000000
        in_formats blob decoded:
             NV12:  LINEAR(0x0)
             NV21:  LINEAR(0x0)
             NV16:  LINEAR(0x0)
             NV61:  LINEAR(0x0)
33 0 0 0,0 0,0 0 0x00000001
  formats: AR24 AR12 AR15 RG24 RG16 BG24
  props:
    8 type:
        flags: immutable enum
        enums: Overlay=0 Primary=1 Cursor=2
        value: 1
    30 IN_FORMATS:
        flags: immutable blob
        blobs:

        value:
            01000000000000000600000018000000
            01000000300000004152323441523132
            41523135524732345247313642473234
            3f000000000000000000000000000000
            0000000000000000
        in_formats blob decoded:
             AR24:  LINEAR(0x0)
             AR12:  LINEAR(0x0)
             AR15:  LINEAR(0x0)
             RG24:  LINEAR(0x0)
             RG16:  LINEAR(0x0)
             BG24:  LINEAR(0x0)
35 0 0 0,0 0,0 0 0x00000001
  formats: AR24 AR12 AR15 RG24 RG16 BG24
  props:
    8 type:
        flags: immutable enum
        enums: Overlay=0 Primary=1 Cursor=2
        value: 2
    30 IN_FORMATS:
        flags: immutable blob
        blobs:

        value:
            01000000000000000600000018000000
            01000000300000004152323441523132
            41523135524732345247313642473234
            3f000000000000000000000000000000
            0000000000000000
        in_formats blob decoded:
             AR24:  LINEAR(0x0)
             AR12:  LINEAR(0x0)
             AR15:  LINEAR(0x0)
             RG24:  LINEAR(0x0)
             RG16:  LINEAR(0x0)
             BG24:  LINEAR(0x0)
37 0 0 0,0 0,0 0 0x00000001
  formats: AR24 AR12 AR15 RG24 RG16 BG24
  props:
    8 type:
        flags: immutable enum
        enums: Overlay=0 Primary=1 Cursor=2
        value: 0
    30 IN_FORMATS:
        flags: immutable blob
        blobs:

        value:
            01000000000000000600000018000000
            01000000300000004152323441523132
            41523135524732345247313642473234
            3f000000000000000000000000000000
            0000000000000000
        in_formats blob decoded:
             AR24:  LINEAR(0x0)
             AR12:  LINEAR(0x0)
             AR15:  LINEAR(0x0)
             RG24:  LINEAR(0x0)
             RG16:  LINEAR(0x0)
             BG24:  LINEAR(0x0)
39 0 0 0,0 0,0 0 0x00000001
  formats: AR24 AR12 AR15 RG24 RG16 BG24
  props:
    8 type:
        flags: immutable enum
        enums: Overlay=0 Primary=1 Cursor=2
        value: 0
    30 IN_FORMATS:
        flags: immutable blob
        blobs:

        value:
            01000000000000000600000018000000
            01000000300000004152323441523132
            41523135524732345247313642473234
            3f000000000000000000000000000000
            0000000000000000
        in_formats blob decoded:
             AR24:  LINEAR(0x0)
             AR12:  LINEAR(0x0)
             AR15:  LINEAR(0x0)
             RG24:  LINEAR(0x0)
             RG16:  LINEAR(0x0)
             BG24:  LINEAR(0x0)
41 0 0 0,0 0,0 0 0x00000001
  formats: NV12 NV21 NV16 NV61
  props:
    8 type:
        flags: immutable enum
        enums: Overlay=0 Primary=1 Cursor=2
        value: 0
    30 IN_FORMATS:
        flags: immutable blob
        blobs:

        value:
            01000000000000000400000018000000
            01000000280000004e5631324e563231
            4e5631364e5636310f00000000000000
            00000000000000000000000000000000
        in_formats blob decoded:
             NV12:  LINEAR(0x0)
             NV21:  LINEAR(0x0)
             NV16:  LINEAR(0x0)
             NV61:  LINEAR(0x0)
43 0 0 0,0 0,0 0       0x00000001
  formats: NV12 NV21 NV16 NV61
  props:
    8 type:
        flags: immutable enum
        enums: Overlay=0 Primary=1 Cursor=2
        value: 0
    30 IN_FORMATS:
        flags: immutable blob
        blobs:

        value:
            01000000000000000400000018000000
            01000000280000004e5631324e563231
            4e5631364e5636310f00000000000000
            00000000000000000000000000000000
        in_formats blob decoded:
             NV12:  LINEAR(0x0)
             NV21:  LINEAR(0x0)
             NV16:  LINEAR(0x0)
             NV61:  LINEAR(0x0)
    45 rotation:
        flags: bitmask
        values: rotate-0=0x1 rotate-90=0x2 rotate-270=0x8 reflect-x=0x10 reflect-y=0x20
        value: 1

Frame buffers:
id size pitch

```

这个是disply 支持的所有参数, 可以看出43 是支持rotaion 和 mirror 的。

测试osd层

```shell
modetest -M canaan-drm  -D 0 -a -s 48@46:1920x1080 -P 39@46:640x480@RG16 -v -F tiles
```

测试效果如下：

![表格 描述已自动生成](https://www.kendryte.com/api/post/attachment?id=462)

测试layer层

```shell
modetest -M canaan-drm  -D 0 -a -s 48@46:1920x1080 -P 43@46:640x480@NV12 -v -F tiles
```

测试效果如下：

![表格 描述已自动生成](https://www.kendryte.com/api/post/attachment?id=462)
