# -*- coding:utf-8 -*-
import logging,os,subprocess
from airtest.core.api import *
from airtest.aircv import *
from airtest.core.settings import Settings
from airtest.report.report import simple_report
from airtest.core.android.android import Android
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
w, h = None, None

# 设置日志级别
# logger = logging.getLogger("airtest")
# logger.setLevel(logging.WARNING)

# 关闭APP
# stop_app('com.addcn.android.house591')


def init_device():
    # 连接设备
    connect_device("Android://127.0.0.1:5037")
    # auto_setup(r'reports/log1', devices=["Android://127.0.0.1:5037"], logdir=True)
    # wake()
    # 关闭APP
    stop_app('com.addcn.android.house591')
    # 启动APP，如果已启动，则直接进入到主活动页
    sleep(1)
    start_app('com.addcn.android.house591', activity='ui.MainActivity')
    # 判断退出按钮是否存在
    if poco('您確定要退出591嗎？').exists():
        poco('取消').click()
    elif poco(text='您確定要退出591嗎？').exists():
        poco(text='取消').click()
    # app_version = subprocess.getoutput("adb shell dumpsys package com.addcn.android.house591 | findstr versionName")
    # # # 输出版本号信息
    # print(app_version)
    # elem = poco('com.addcn.android.house591:id/cancel_btn')
    # if elem.exists():
    #     elem.click()


# 获取当前手机的分辨率，通过相对坐标计算出绝对坐标，再点击绝对坐标
# global w, h
w, h = device().get_current_resolution()
print('设备分辨率：', w, h)
# 获取设备型号
device_name = Android().get_default_device()
print('设备型号：', device_name)
# 获取设备系统版本
device_version = shell('getprop ro.build.version.release')
print('设备系统版本：', device_version)

# 县市区域id
region_id = 1


# 方法一：在auto_setup()接口添加设备
# auto_setup(__file__, devices=["Android://127.0.0.1:5037"])
# 方法二：用connect_device()方法连接设备
# dev = connect_device("Android://127.0.0.1:5037")
# 方法三：用init_device()方法连接设备
# init_device(platform="Android",uuid="SJE5T17B17")

# start_app('com.addcn.android.house591', activity='com.addcn.android.flutter.page.common.SplashByFlutterActivity')
# start_app('com.addcn.android.house591', activity='.flutter.page.common.SplashByFlutterActivity')
if __name__ == '__main__':
    init_device()




