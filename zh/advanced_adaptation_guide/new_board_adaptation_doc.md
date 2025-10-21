# K230 linux sdk 适配指南

## 文档目的

本文旨在介绍当开发人员使用非k230_linux_sdk支持的标准开发板时，如何修改k230_linux_sdk，使其适配新的板子。

参考k230d_canmv开发板的源码文件。

## uboot适配

### step 1

在buildroot-overlay/boot/uboot/u-boot-2022.10-overlay/board/canaan/目录增加你自己板子的目录

```bash
cp k230d_canmv k230_${board_name} -r
```

### step 2

修改buildroot-overlay/boot/uboot/u-boot-2022.10-overlay/board/canaan/k230_${board_name}/Kconfig

```makefile
if TARGET_${BOARD_NAME}

config SYS_CPU
        default "k230"
    
config SYS_VENDOR
    default "canaan"

config SYS_BOARD
    default "k230_${board_name}"

config SYS_CONFIG_NAME
    default "k230_evb"


config BOARD_SPECIFIC_OPTIONS # dummy
        def_bool y
        select RISCV_THEAD
    
config SIPLP4_2667
        def_bool y

endif
```

### step 3

在buildroot-overlay/boot/uboot/u-boot-2022.10-overlay/arch/riscv/dts/增加你自己板子的设备树

```bash
cp k230d_canmv.dts k230_${board_name}.dts
```

出于篇幅考虑，仅列出可能涉及修改的部分代码

```c
...
// BANK电压设置，需要与板子的BANK电压保持一致，不一致有导致芯片损坏的风险。
#define BANK_VOLTAGE_IO0_IO1           K230_MSC_1V8  // FIXED
#define BANK_VOLTAGE_IO2_IO13          K230_MSC_3V3
#define BANK_VOLTAGE_IO14_IO25         K230_MSC_3V3
#define BANK_VOLTAGE_IO26_IO37         K230_MSC_3V3
#define BANK_VOLTAGE_IO38_IO49         K230_MSC_3V3
#define BANK_VOLTAGE_IO50_IO61         K230_MSC_3V3
#define BANK_VOLTAGE_IO62_IO63         K230_MSC_3V3
#include "k230.dtsi"

/ {
        model = "kendryte k230 ${board name}";
        compatible = "kendryte,k230_${board_name}";

        memory@0 {
                device_type = "memory";
                // 根据实际内存大小做调整，0x20000000为512MB
                reg = <
                                0x0 0 0x0 0x20000000
                          >;
        };
};

&mmc0 {
        // 1-8-v 配置mmc0为1V8 IO。否则mmc0为3V3 IO
        1-8-v;
        status = "okay";
};

&mmc1 {
        status = "okay";
};

...

// 这里需要把芯片的64个IO的使用清楚的表达描述，参考 附录A 关于IO如何配置的详细描述。
&iomux {
        pinctrl-names = "default";
        pinctrl-0 = <&pins>;

//        Please pay attention to the bank voltage! will damage the chip.
        pins: iomux_pins {
                u-boot,dm-pre-reloc;
                pinctrl-single,pins = <

                (IO2 ) ( 1<<SEL | 0<<SL | BANK_VOLTAGE_IO2_IO13 <<MSC | 1<<IE | 0<<OE | 0<<PU | 1<<PD | 4<<DS | 1<<ST )

...

                (IO63) ( 0<<SEL | 0<<SL | BANK_VOLTAGE_IO62_IO63<<MSC | 1<<IE | 1<<OE | 0<<PU | 0<<PD | 7<<DS | 1<<ST )
                >;
        };
};

```

### step 4

修改buildroot-overlay/boot/uboot/u-boot-2022.10-overlay/arch/riscv/Kconfig
出于篇幅考虑，省略大部分无关代码，保留部分用于指示添加代码的位置。

```makefile
...
config TARGET_K230D_CANMV
        bool "Support k230D_CANMV(K230PI zero)"
        select SYS_CACHE_SHIFT_6

config TARGET_${BOARD_NAME}
        bool "Support k230_${board_name}
    select SYS_CACHE_SHIFT_6
...
source "board/canaan/k230d_canmv/Kconfig"
source "board/canaan/k230_${board_name}/Kconfig"
...
```

### step 5

在buildroot-overlay/boot/uboot/u-boot-2022.10-overlay/configs/目录增加你自己板子的编译配置文件。

```bash
cp k230d_canmv_defconfig k230_${board_name}_defconfig
```

出于篇幅考虑，省略大部分无关代码，保留部分用于指示添加代码的位置

```makefile
...
CONFIG_SPL_DM_SPI=y
CONFIG_DEFAULT_DEVICE_TREE="k230_${board_name}"
...
CONFIG_BUILD_TARGET="u-boot.bin"
# CONFIG_TARGET_K230D_CANMV=y
CONFIG_TARGET_K230_${BOARD_NAME}=y
CONFIG_ARCH_RV64I=y
...
```

## linux适配

### step 1

在arch/riscv/boot/dts/canaan/目录增加你自己板子的设备树。

```bash
cp k230d-canmv.dts k230-${board_name}.dts
```

出于篇幅考虑，仅列出可能涉及修改的部分代码

```c
...
// io_fixed_1v8 配置mmc0为1V8 IO。否则mmc0为3V3 IO
&mmc_sd0{
    status = "okay";
    io_fixed_1v8;
    rx_delay_line = <0x0d>;
    tx_delay_line = <0x40>;
};
...
```

### step 2

linux的编译配置可以使用默认的k230_defconfig，如果有特殊需求修改，在arch/riscv/configs/目录增加你自己板子的编译配置。

```bash
cp k230_defconfig k230_${board_name}_defconfig
```

## k230_linux_sdk适配

### step 1

在buildroot-overlay/configs/目录增加你自己板子的顶层配置文件。

```bash
cp k230d_canmv_defconfig k230_${board_name}_defconfig
```

出于篇幅考虑，仅列出可能涉及修改的部分代码

```makefile
...
BR2_ROOTFS_POST_SCRIPT_ARGS="k230-${board_name} $(LINUX_DIR)"
...
BR2_LINUX_KERNEL_DEFCONFIG="k230_${board_name}"
...
BR2_LINUX_KERNEL_INTREE_DTS_NAME="canaan/k230-${board_name}"
...
BR2_TARGET_UBOOT_BOARDNAME="k230_${board_name}"
...
```

## 开发板ROM电压适配

### step 1

根据板子设计使用 K230 OTP配置工具 生成otp.bin。参考k230d canmv原理图，ROM串口使用IO38/IO39，bank电压为3V3，OSPI IO电压BANK3为3V3，SDIO0为3V3，SDIO1 IO电压BANK2为3V3

![bank_vol](https://www.kendryte.com/api/post/attachment?id=447)

![otp_config](https://www.kendryte.com/api/post/attachment?id=446)

### step 2

使用k230烧录工具烧录otp。开发板通过USB线连接电脑，开发板上电启动失败会进入usb烧录模式。

```shell
k230_flash_cli> .\k230_flash_cli.exe -m OTP 0  .\img\K230D-otp-1731400641587.bin
```

## 附录A

IOMUX节点的配置，需要参考板子原理图 和 iomux表。没有用的IO建议配置为GPIO功能，避免同一个功能连接到了多个IO。无论大核使用IO还是小核使用IO，IO的功能配置统一放在uboot。
每个IO用作什么功能在设计硬件的时候已经确定，适配SDK时参考原理图配置。以下图的IO7为例：

![gpio7](https://www.kendryte.com/api/post/attachment?id=445)

BANK0_GPIO7 复用为了I2C4_SCL功能，连接摄像头。

查阅 [iomux表](https://kendryte-download.canaan-creative.com/developer/k230/HDK/K230%E7%A1%AC%E4%BB%B6%E6%96%87%E6%A1%A3/K230_PINOUT_V1.2_20240822.xlsx)

设备树的IO7进行如下配置：

```c
(IO7) ( 2<<SEL | 0<<SL | BANK_VOLTAGE_IO2_IO13<<MSC | 1<<IE | 1<<OE | 1<<PU | 0<<PD | 7<<DS | 1<<ST )
```

- SEL为功能号选择，从0开始，iomux表 里面 Function Number - 1。IIC4_SCL对应2<<SEL
- SL输出翻转率控制，只有IO0/IO1单电压PAD可配置。
- MSC工作电压配置，需要与板子上的bank供压保持一致
- IE输入使能，为0表示方向无效，输入为低电平。
- OE输出使能，为0表示输出方向无效，PAD的电压取决于PU/PD，不确定IO的方向，IE/OE都配置为1也没问题。
- PU上拉配置，与IO的功能有关。IIC总线，空闲是高电平，所以建议配置上拉。一般硬件设计外部会有上拉，所以IOMUX配置不上拉也没有问题。
- PD下拉配置，与IO的功能有关。

![pull_resistor](https://www.kendryte.com/api/post/attachment?id=443)

- DS驱动强度配置，单电压PAD为8驱PAD，3bit有效，取值为4’b000~4’b111。双电压PAD为16驱PAD，4bit有效，取值为4’b0000~4’b1111，IO2~IO63都是双电压PAD。

![iol](https://www.kendryte.com/api/post/attachment?id=442)

![ioh](https://www.kendryte.com/api/post/attachment?id=441)

- ST输入施密特触发器配置，一般配置为1
