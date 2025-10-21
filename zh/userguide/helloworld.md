# k230_linux_sdk开发helloworld

## 编译第一个程序hello world

创建内容如下的hello.c文件

```c
//hello.c 文件内容
#include <stdio.h>
int main()
{
    printf("Hello, World!\n");
    return 0;
}
```

编译程序

```shell
/opt/toolchain/Xuantie-900-gcc-linux-6.6.0-glibc-x86_64-V2.10.1/bin/riscv64-unknown-linux-gnu-gcc hello.c  -o hello
```

把hello文件复制到开发板上，并执行,可以看到打印正确

```bash
[root@canaan ~ ]#./hello
Hello, World!
[root@canaan ~ ]#
```

>可以通过scp或者rz命令复制到开发板上
