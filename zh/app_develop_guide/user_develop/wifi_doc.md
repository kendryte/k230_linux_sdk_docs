# K230 linux WiFi使用指南

## 概述

本文档将讲解如何在k230开发板上使用WiFi。

## 使用流程

以k230-canmv为例，板卡上默认搭载了AP6212 WiFi模组。

WiFi模块在系统启动后，使用`if wlan down/up`对WiFi模块进行上电下电操作。

```sh
ifconfig -a
ifconfig  wlan0 up
wpa_supplicant -D nl80211 -i wlan0 -c /etc/wpa_supplicant.conf -B
# 扫描热点
# wpa_cli -i wlan0 scan
# 打印扫描结果
# wpa_cli -i wlan0 scan_result
wpa_cli -i wlan0 add_network
# 设置网络名称
wpa_cli -i wlan0 set_network 1 ssid '"wifi_test"'
# 设置网络密码
wpa_cli -i wlan0 set_network 1 psk '"12345678"'
# 连接网络
wpa_cli -i wlan0 select_network 1
# 获取ip
udhcpc -i wlan0 -q
```
