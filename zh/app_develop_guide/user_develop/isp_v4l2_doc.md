# K230_Linux ISP V4l2 使用指南

## 概述

本指南旨在帮助用户了解和使用K230 Linux多媒体功能。主要内容包括如何使用V4L2 Isp（视频处理单元）接口。
通过本指南，用户将能够：

- 掌握V4L2 ISP的使用方法，包括图片捕获、显示，并提供v4l2 Isp demo演示

## V4L2 ISP使用指南

### V4l2 ISP 设置crop

本isp 的crop 是一个硬件的crop、使用的方式是sensor 的输入 ---> crop --->scaler--->output, isp 的pipe是这样的一个流程，

v4l2 设置crop 有两种方式、一种是通过VIDIOC_S_CROP 方式，代码实现如下：

```shell
struct v4l2_crop crop;
struct v4l2_cropcap cropcap;

memset (&cropcap, 0, sizeof (cropcap));
cropcap.type = V4L2_BUF_TYPE_VIDEO_OUTPUT;

if (-1 == ioctl (context[i].video_fd, VIDIOC_CROPCAP, &cropcap)) {
    perror ("VIDIOC_CROPCAP");   
}

memset (&crop, 0, sizeof (crop));
crop.type = V4L2_BUF_TYPE_VIDEO_OUTPUT;
crop.c = cropcap.defrect;

crop.c.width = context[i].crop_size.width;
crop.c.height = context[i].crop_size.height;
crop.c.left = context[i].crop_size.offset_x;
crop.c.top = context[i].crop_size.offset_y;

/* Ignore if cropping is not supported (EINVAL). */

if (-1 == ioctl (context[i].video_fd, VIDIOC_S_CROP, &crop)
    && errno != EINVAL) {
    perror ("VIDIOC_S_CROP");
}
printf("set crop crop.c.height is %d \n", crop.c.height);

```

另外一种是 VIDIOC_S_SELECTION 方式实现，代码如下：

```shell
struct v4l2_selection sel = {
    .type = V4L2_BUF_TYPE_VIDEO_OUTPUT,
    .target = V4L2_SEL_TGT_COMPOSE_BOUNDS,
};
struct v4l2_rect r;
int ret = 0;

ret = ioctl(context[i].video_fd, VIDIOC_G_SELECTION, &sel);
if(ret < 0)
    printf("get VIDIOC_G_SELECTION err \n");

/* setting smaller compose rectangle */
r.width = context[i].crop_size.width;
r.height = context[i].crop_size.height;
r.left = context[i].crop_size.offset_x;
r.top = context[i].crop_size.offset_y;

sel.r = r;
sel.target = V4L2_SEL_TGT_COMPOSE;
sel.flags = V4L2_SEL_FLAG_LE;

ret = ioctl(context[i].video_fd, VIDIOC_S_SELECTION, &sel);
if(ret < 0)
    printf("get VIDIOC_S_SELECTION err \n");

```

目前v4l2 中这两种方式都是支持，需要注意的事项如下：

- 设置crop 需要在设置VIDIOC_S_FMT 之前
- VIDIOC_S_SELECTION 这种方式目前target 值目前只支持V4L2_SEL_TGT_COMPOSE，设置别的会返回错误
- 设置crop的size要大于设置isp 的输出size（VIDIOC_S_FMT设置的尺寸），要小于sensor 的输出尺寸

测试命令如下：

```shell
./v4l2-drm -d 1 -w 640 -h 480 -x 0 -y 0 --crop-width 1280 --crop-height 960
```
