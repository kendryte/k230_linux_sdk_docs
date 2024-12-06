# K230 debian ubuntu等发行版说明

## 1.k230发行版概述

k230支持debian和ubuntu发行版，发行版镜像编译方法见本的文后面章节。

k230 debian镜像 支持pyqt,支持qt单界面显示(没有使用gpu)，ubuntu是命令行版本的镜像，如果需要其他软件，请使用apt-get进行安装。
镜像的用户名和密码均为root

## 2.debian发行版

### 2.1 debian镜像编译

参考如下命令可以生成debian镜像

```bash
git clone git@github.com:kendryte/k230_linux_sdk.git
# git clone git@gitee.com:kendryte/k230_linux_sdk.git
cd k230_linux_sdk
make CONF=k230_canmv_01studio_defconfig # 01studio
# make CONF=k230_canmv_defconfig #k230_canmv
sudo make debian   # genration debian image
```

生成的debian镜像名字类似如下：
output/k230_canmv_01studio_defconfig/images/CanMV-K230_01studio_debian_v0.5_nncase_v2.9.0.img.gz
把上述镜像解压缩并烧录到tf卡，把tf卡插入设备，重启设备，通过串口可以看到debian的启动输出，类似如下：

```bash
[  OK  ] Finished plymouth-quit.service - Terminate Plymouth Boot Screen.

Debian GNU/Linux trixie/sid k230 ttyS0

k230 login: root
```

### 2.2 debian rootfs更新

apt install可以安装软件包，类似如下：

```bash
root@k230:~# apt install vim
vim is already the newest version (2:9.1.0777-1+b1).
Summary:
  Upgrading: 0, Installing: 0, Removing: 0, Not Upgrading: 0
root@k230:~#
```

镜像已经执行过的命令可以通过make debian_rootfs查看,输入类似如下：

```bash
you need manually execute the follow commands

sudo rm -rf debian13
sudo apt-get update
sudo apt install qemu-user-static binfmt-support debootstrap debian-ports-archive-keyring systemd-container rsync wget
sudo debootstrap --arch=riscv64  unstable debian13 https://mirrors.aliyun.com/debian/
sudo chroot debian13/
echo "root:root" | chpasswd

cat >>/etc/network/interfaces <<EOF
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet dhcp
'EOF'
apt-get install -y  net-tools ntpdate
ntpdate ntp.ntsc.ac.cn
exit


chroot /path/to/rootfs
apt-get install python3-pyqt5 vim ntp
apt-get install openssh-server
apt-get install libdrm-dev
apt-get install qtbase5-dev qtbase5-examples
apt-get install lxqt
systemctl disable sddm


cat << EOF > /etc/profile.d/qt_env.sh
export QT_QPA_PLATFORM=linuxfb
export QT_QPA_FB_DRM=1
export QT_QPA_EGLFS_KMS_CONFIG="/root/kms_config.json"
EOF




cat << EOF > /root/kms_config.json
{
"device": "/dev/dri/card0",
"outputs": [
    { "name": "HDMI1", "format": "argb8888" }
]
}
EOF

cat << EOF > /root/helloworld_pyqt.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QFont

def main():
    app = QApplication(sys.argv)  # 创建一个 QApplication 实例
    window = QWidget()  # 创建一个 QWidget 实例作为主窗口
    window.setWindowTitle('Hello World')  # 设置窗口标题
    label = QLabel('Hello World', window)  # 创建一个 QLabel 实例显示文本
    label.move(50, 50)  # 移动标签到窗口中的位置

    label = QLabel('王建新，，测试', window)  # 创建一个 QLabel 实例显示文本
    label.move(300, 400)  # 移动标签到窗口中的位置

    label.setFont(QFont('Arial', 30, QFont.Bold))
    label.setStyleSheet("QLabel { color: red; }")  # 设置字体颜色为红色


    label = QLabel('k230 pyqt5 测试', window)  # 创建一个 QLabel 实例显示文本
    label.move(500, 500)  # 移动标签到窗口中的位置

    label.setFont(QFont('Arial', 50, QFont.Bold))
    label.setStyleSheet("QLabel { color: red; }")  # 设置字体颜色为红色



    window.show()  # 显示窗口
    sys.exit(app.exec_())  # 进入 Qt 事件循环

if __name__ == '__main__':
    main()
EOF

echo "a"> /first_boot_flag
cat << 'EOF' > /etc/profile.d/disk.sh
if [ -f /first_boot_flag ]; then
    echo "first boot flag"
    sd_size=$(parted /dev/mmcblk0 print | grep mmcblk0 | cut -d: -f2)
    parted /dev/mmcblk0 resizepart 2 ${sd_size}; resize2fs /dev/mmcblk0p2
    rm -rf /first_boot_flag
else
    echo "not exit flag"
fi
EOF
echo "PermitRootLogin yes" >> etc/ssh/sshd_config

tar  -czf debian13.tar.gz debian13
#debian13_size="$(( "$(sudo du -sm debian13 | cut -f1 )" + 300 ))"
#sudo  mkfs.ext4 -d debian13  -r 1 -N 0 -m 1 -L "rootfs" -O ^64bit debian13.ext4 ${debian13_size}m
#tar -czvf debian13.ext4.tar.gz debian13.ext4
#debian13.ext4.tar.gz 是debian的ext4格式根文件系统压缩包


You need to manually execute the above commands one by one on linux(not docker)
referenc doc is <<https://developer.canaan-creative.com/k230/zh/dev/03_other/K230_debian_ubuntu%E8%AF%B4%E6%98%8E.html>>
```

### 2.2 pyqt测试

执行如下命令可以在hdmi显示器上看到pyqt输出的文字：

```bash
root@k230:~# python3 /root/helloworld_pyqt.py
[ 1736.450790] lt9611_connect_detect 1
[ 1736.454337] lt9611_connector_get_modes
root@k230:~# python3 /root/helloworld_pyqt.py
```

helloworld_pyqt.py测试脚本内容如下：

```bash
root@k230:~# cat /root/helloworld_pyqt.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QFont

def main():
    app = QApplication(sys.argv)  # 创建一个 QApplication 实例
    window = QWidget()  # 创建一个 QWidget 实例作为主窗口
    window.setWindowTitle('Hello World')  # 设置窗口标题
    label = QLabel('Hello World', window)  # 创建一个 QLabel 实例显示文本
    label.move(50, 50)  # 移动标签到窗口中的位置

    label = QLabel('王建新，，测试', window)  # 创建一个 QLabel 实例显示文本
    label.move(300, 400)  # 移动标签到窗口中的位置

    label.setFont(QFont('Arial', 30, QFont.Bold))
    label.setStyleSheet("QLabel { color: red; }")  # 设置字体颜色为红色


    label = QLabel('k230 pyqt5 测试', window)  # 创建一个 QLabel 实例显示文本
    label.move(500, 500)  # 移动标签到窗口中的位置

    label.setFont(QFont('Arial', 50, QFont.Bold))
    label.setStyleSheet("QLabel { color: red; }")  # 设置字体颜色为红色



    window.show()  # 显示窗口
    sys.exit(app.exec_())  # 进入 Qt 事件循环

if __name__ == '__main__':
    main()
root@k230:~#
```

## 3.ubuntu发行版

### 3.1 debian镜像编译

参考如下命令可以生成k230 ubuntu镜像

```bash
git clone git@github.com:kendryte/k230_linux_sdk.git
# git clone git@gitee.com:kendryte/k230_linux_sdk.git
cd k230_linux_sdk
make CONF=k230_canmv_01studio_defconfig   # 01studio
# make CONF=k230_canmv_defconfig  #k230_canmv
sudo make ubuntu # ubuntu
```

生成的debian镜像名字类似如下：
output/k230_canmv_01studio_defconfig/images/CanMV-K230_01studio_ubuntu_v0.5_nncase_v2.9.0.img.gz
把上述镜像解压缩并烧录到tf卡，把tf卡插入设备，重启设备，通过串口可以看到ubuntu的启动输出。

### 2.2 debian rootfs更新

apt install可以安装软件包，类似如下：

```bash
root@k230:~# apt install vim
vim is already the newest version (2:9.1.0777-1+b1).
Summary:
  Upgrading: 0, Installing: 0, Removing: 0, Not Upgrading: 0
root@k230:~#
```

镜像已经执行过的命令可以通过make ubuntu_rootfs查看,输入类似如下：

```bash
you need manually execute the follow commands

#docker run  --privileged  -u root -it  -v $(pwd):$(pwd)    -w $(pwd) ubuntu24:v1  /bin/bash

rm -rf ubuntu24
sudo debootstrap --arch=riscv64   noble ubuntu24 https://mirrors.aliyun.com/ubuntu-ports/
chroot ubuntu24 /bin/bash

cat >/etc/apt/sources.list <<EOF
deb https://mirrors.aliyun.com/ubuntu-ports noble main restricted

deb https://mirrors.aliyun.com/ubuntu-ports noble-updates main restricted

deb https://mirrors.aliyun.com/ubuntu-ports noble universe
deb https://mirrors.aliyun.com/ubuntu-ports noble-updates universe

deb https://mirrors.aliyun.com/ubuntu-ports noble multiverse
deb https://mirrors.aliyun.com/ubuntu-ports noble-updates multiverse

deb https://mirrors.aliyun.com/ubuntu-ports noble-backports main restricted universe multiverse

deb https://mirrors.aliyun.com/ubuntu-ports noble-security main restricted
deb https://mirrors.aliyun.com/ubuntu-ports noble-security universe
deb https://mirrors.aliyun.com/ubuntu-ports noble-security multiverse
EOF
echo "root:root" | chpasswd
echo k230>/etc/hostname
apt-get install ssh  parted
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
echo "a" >/first_boot_flag
cat << 'EOF' > /etc/profile.d/disk.sh
if [ -f /first_boot_flag ]; then
    echo "first boot flag"
    sd_size=$(parted /dev/mmcblk0 print | grep mmcblk0 | cut -d: -f2)
    parted /dev/mmcblk0 resizepart 2 ${sd_size}; resize2fs /dev/mmcblk0p2
    rm -rf /first_boot_flag
else
    echo "not exit flag"
fi
EOF

exit
sudo tar -czf ubuntu24.tar.gz ubuntu24
# debian13_size="$(( "$(sudo du -sm ubuntu24 | cut -f1 )" + 300 ))"
# mkfs.ext4  -d ubuntu24  -r 1 -N 0 -m 1 -L "rootfs" -O ^64bit ubuntu24.ext4 ${debian13_size}m
# tar -czvf ubuntu24.ext4.tar.gz ubuntu24.ext4


You need to manually execute the above commands one by one on linux(not docker)
referenc doc is <<https://developer.canaan-creative.com/k230/zh/dev/03_other/K230_debian_ubuntu%E8%AF%B4%E6%98%8E.html>>
```

## 4.参考文档

<<https://developer.canaan-creative.com/k230/zh/dev/03_other/K230_debian_ubuntu%E8%AF%B4%E6%98%8E.html>>
