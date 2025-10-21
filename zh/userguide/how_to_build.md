# K230 linux SDK镜像编译指南

## sdk源码及编译

### 获取sdk代码

参考如下命令下载sdk代码

```bash
git clone git@github.com:kendryte/k230_linux_sdk.git
# git clone git@gitee.com:kendryte/k230_linux_sdk.git
cd k230_linux_sdk
```

>github上仓库地址是 <https://github.com/kendryte/k230_linux_sdk.git>
>
>gitee上仓库地址是 <https://gitee.com/kendryte/k230_linux_sdk.git>

### 安装交叉工具链

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

### 安装依赖

需要安装如下软件的 ubuntu22.04 或者ubuntu 24.04系统(参考安装命令)

```bash
sudo apt-get install -y wget git sed make binutils build-essential diffutils gcc  g++ bash patch gzip bzip2 perl tar cpio unzip rsync file bc findutils wget libncurses-dev python3 libssl-dev  gawk cmake bison flex bash-completion  parted curl xz-utils
```

>依赖软件包见tools/docker/Dockerfile 文件，构建和进入docker环境参考如下命令：
>
>docker  build   -f tools/docker/Dockerfile  -t wjx/d tools/docker  #构建
>
>docker run -it  -h k230  -e uid=\$(id -u) -e gid=\$(id -g) -e user=\${USER} -v \${HOME}:\${HOME}  -w \$(pwd) wjx/d:latest   #使用

### 编译

参考下面命令进行编译

```bash
make CONF=k230d_canmv_defconfig #build k230d canmv image (kernel and rootfs both 64bit)
#make CONF=k230_canmv_01studio_defconfig # build 01studio canmv board
# make CONF=k230_canmv_defconfig # build k230 canmv image
# make CONF=k230d_canmv_ilp32_defconfig  #build k230d canmv 32bit rootfs;
```

>k230d_canmv_defconfig是个例子，需要替换为正确的配置文件，比如替换为k230_canmv_defconfig
>
>sdk支持的所有配置文件见buildroot-overlay/configs目录
>
>make CONF=k230d_canmv_defconfig  含义是使用k230d_canmv_defconfig配置文件

### 编译输出文件

output/k230d_canmv_defconfig/images/sysimage-sdcard.img.gz

>从嘉楠官网下载的就是这个文件，烧录前需要解压缩，烧录方法见后面
>
>k230d_canmv_defconfig 是个例子，请根据编译配置文件替换为正确名字
