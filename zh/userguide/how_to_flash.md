# 镜像烧录指南

## 镜像获取

镜像可以按照文档使用编译生成的文件，也可以从嘉楠官网 <https://www.kendryte.com/resource>下载，

如果从官网下载，需要下载"linux_"开头的gz压缩包(比如linux_k230_canmv_v0.2_nncase_v0.0.0.img.gz)，解压缩得到sysimage-sdcard.img文件。

>需要解压缩

### linux下烧录

在TF卡插到宿主机之前，输入：

```bash
ls -l /dev/sd\*
```

查看当前的存储设备。

将TF卡插入宿主机后，再次输入：

```bash
ls -l /dev/sd\*
```

查看此时的存储设备，新增加的就是TF卡设备节点。

假设/dev/sdc就是TF卡设备节点，执行如下命令烧录TF卡：

```bash
sudo dd if=sysimage-sdcard.img of=/dev/sdc bs=1M oflag=sync
```

### windows下烧录

Windows下可通过rufus工具对TF卡进行烧录（rufus工具下载地址 `http://rufus.ie/downloads/`）。

1）将TF卡插入PC，然后启动rufus工具，点击工具界面的”选择”按钮，选择待烧写的固件。

![rufus-flash-from-file](https://www.kendryte.com/k230_canmv/main/_images/rufus_select.png)

4)启动：

把tf卡插入开发板，给开发板上电(usb接入电脑)，按下reset按键(可选)，

电脑上的串口软件可以看到打印

>板子连接及串口查看方法见后面章节

## 开发板连接

>开发板有差异，请参考对应章节连接各个开发板

### 说明

本sdk主要支持的开发板及配置文件说明

| 开发板         | 配置文件                      | 说明                            |
| -------------- | ----------------------------- | ------------------------------- |
| canmv          | k230_canmv_defconfig          | k230 canmv board                |
| canmv_01studio | k230_canmv_01studio_defconfig | 01studio  canmv board           |
| k230d_canmv    | k230d_canmv_defconfig         | k230d canmv board               |
| k230d_canmv    | k230d_canmv_ilp32_defconfig   | k230d canmv board 32bit systerm |
| BPI-CanMV-K230D-Zero    | BPI-CanMV-K230D-Zero_defconfig         | BPI CanMV-K230D-Zero board              |
| BPI-CanMV-K230D-Zero    | BPI-CanMV-K230D-Zero_ilp32_defconfig   | BPI CanMV-K230D-Zero board 32bit systerm |

### CanMV-K230-V1.0/1.1开发板连接

1)参考下图使用Type-C连接k230-canmv开发板

使用Type-C线连接CanMV-K230（下图5V供电+调试串口的位置），线另一端连接至电脑

![debug](https://www.kendryte.com/k230_canmv/main/_images/CanMV-K230_front.png)

![board-behind](https://www.kendryte.com/k230_canmv/main/_images/CanMV-K230_behind.png)

2)电脑上确认串口号：

设备上电后电脑上会多出两个串口，

windows串口显示如下：

![CanMV-K230-micropython-serial](https://www.kendryte.com/k230_canmv/main/_images/CanMV-K230-micropython-serial.png)

USB-Enhanced-SERIAL-A CH342（COM80）为小核linux调试串口

USB-Enhanced-SERIAL-B CH342（COM81）为串口3--暂未使用

>windows下如果串口识别错误，请重新安装ch342驱动(下载地址：<https://www.wch.cn/downloads/CH343SER_EXE.html>)

linux系统下串口显示如下：

/dev/ttyACM0为小核linux调试串口

/dev/ttyACM1为 为串口3--暂未使用

>不插tf卡，也可以看到串口。

3)查看串口输出

使用串口软件查看开发板串口输出

>开发板默认串口参数:波特率115200，数据位 8，停止位1，奇偶检验 无，流控 无
>不插tf卡，按下reset按键，默认串口也会输出一行打印，看到打印说明cpu工作正常。
>推荐串口软件是putty，其他串口软件(比如moblxterm xshell securecrt等)也可以。

### k230d-canmv开发板连接

1)参考下图连接k230d-canmv开发板

使用Type-C线连接开发板（下图Power+UART的位置），线另一端连接至电脑

![debug](https://www.kendryte.com/api/post/attachment?id=482)

>补充：需要硬件说明：
>typec usb线
>tf卡；

2)电脑上确认串口号：

设备上电后电脑上会多出两个串口，

windows串口显示如下：

![CanMV-K230-micropython-serial](https://www.kendryte.com/k230_canmv/main/_images/CanMV-K230-micropython-serial.png)

USB-Enhanced-SERIAL-A CH342（COM80）为小核linux调试串口

USB-Enhanced-SERIAL-B CH342（COM81）为串口3--暂未使用

> windows下如果串口识别错误，请重新安装ch342驱动(下载地址：<https://www.wch.cn/downloads/CH343SER_EXE.html>)

linux系统下串口显示如下：

/dev/ttyACM0为小核linux调试串口

/dev/ttyACM1为 为串口3--暂未使用

>不插tf卡，也可以看到串口。

3)查看串口输出

使用串口软件查看开发板串口输出

>开发板默认串口参数:波特率115200，数据位 8，停止位1，奇偶检验 无，流控 无
>不插tf卡，按下reset按键，默认串口也会输出一行打印，看到打印说明cpu工作正常。
>推荐串口软件是putty，其他串口软件(比如moblxterm xshell securecrt等)也可以。
