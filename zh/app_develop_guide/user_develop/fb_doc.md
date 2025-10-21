# framebuffer 使用指南

## 概述

本指南旨在帮助用户了解和使用K230 Linux 下 显示中 fb 设备的配置，默认是不打开fb 显示设备、如果需要可以根据本文档自己去配置打开

## 配置如下

代码中增加如下：

```shell
linux/drivers/gpu/drm/canaan/canaan_dsi.c ：

static const struct drm_encoder_helper_funcs canaan_dsi_enc_helper_funcs = {
    .mode_fixup = canaan_dsi_encoder_mode_fixup,
    .disable = canaan_dsi_encoder_disable,
    .enable = canaan_dsi_encoder_enable,
    .atomic_check = canaan_dsi_encoder_atomic_check,
    .mode_valid    = canaan_dsi_mode_valid,
};


static int canaan_dsi_encoder_atomic_check(struct drm_encoder *encoder,
                struct drm_crtc_state *crtc_state,
                struct drm_connector_state *conn_state)
{
    struct canaan_dsi *dsi = encoder_to_canaan_dsi(encoder);
    int vrefresh = 0;

    vrefresh = drm_mode_vrefresh(&crtc_state->mode);
    if(vrefresh > 60) {
        return -1;
    }

    return 0;
}


static enum drm_mode_status canaan_dsi_mode_valid(struct drm_encoder *crtc,const struct drm_display_mode *mode)
{
    struct canaan_dsi *dsi = encoder_to_canaan_dsi(crtc);
    int vrefresh = 0;
    vrefresh = drm_mode_vrefresh(mode);
    if(vrefresh > 60) {
        return MODE_HSYNC_WIDE;
    }
    return MODE_OK;
}
```

在dsi 中drm_encoder_helper_funcs 结构体中增加atomic_check 和 mode_valid。

```shell
linux/drivers/gpu/drm/canaan/canaan_drv.c

static int canaan_drm_bind(struct device *dev)
{
    int ret = 0;
    struct drm_device *drm_dev;

    drm_dev = drm_dev_alloc(&canaan_drm_driver, dev);
    if (IS_ERR(drm_dev))
        return PTR_ERR(drm_dev);
    dev_set_drvdata(dev, drm_dev);

    drm_mode_config_init(drm_dev);
    drm_dev->mode_config.min_width = 16;
    drm_dev->mode_config.min_height = 16;
    drm_dev->mode_config.max_width = 1920; //4096
    drm_dev->mode_config.max_height = 1080;//4096
    drm_dev->mode_config.normalize_zpos = true;
    drm_dev->mode_config.funcs = &canaan_drm_mode_config_funcs;
    drm_dev->mode_config.helper_private = &canaan_drm_mode_config_helpers;

    ret = component_bind_all(dev, drm_dev);
    if (ret) {
        DRM_DEV_ERROR(dev, "Failed to bind all components\n");
        goto cleanup_mode_config;
    }

    ret = drm_vblank_init(drm_dev, drm_dev->mode_config.num_crtc);
    if (ret) {
        DRM_DEV_ERROR(dev, "Failed to init vblank\n");
        goto unbind_all;
    }

    drm_mode_config_reset(drm_dev);
    drm_kms_helper_poll_init(drm_dev);

    ret = drm_dev_register(drm_dev, 0);
    if (ret) {
        DRM_DEV_ERROR(dev, "Failed to register drm device\n");
        goto finish_poll;
    }

    pm_runtime_get_sync(disp_dev);
    drm_fbdev_generic_setup(drm_dev, 24);
    DRM_DEV_INFO(dev, "Canaan K230 DRM driver register successfully\n");

    return 0;

finish_poll:
    drm_kms_helper_poll_fini(drm_dev);
unbind_all:
    component_unbind_all(dev, drm_dev);
cleanup_mode_config:
    drm_mode_config_cleanup(drm_dev);

    dev_set_drvdata(dev, NULL);
    drm_dev_put(drm_dev);
    return ret;
}
```

将 drm_dev->mode_config.max_width 配置成1920 ，drm_dev->mode_config.max_height配置成1080，drm_fbdev_generic_setup(drm_dev, 24); 中的32 修改成24.pm_runtime_get_sync 这个函数打开电源域。默认电源域是关的。

```shell
Device Drivers  ---> 
    Graphics support  --->
        Frame buffer Devices  --->
            [*] Enable Video Mode Handling Helpers
```

make linux-menuconfig 中配置 FB_MODE_HELPERS。

到这从新编译代码即可。烧录镜像后查看dev。

```shell
zhaoshuai@develop:~$ ls /dev/fb0 
/dev/fb0
```

测试命令，可以安装fbtest ,或者通过下边命令往屏幕的左上角画一个白色的像素点

```shell
echo -en '\xFF\xFF\xFF\x00' > /dev/fb0
```
