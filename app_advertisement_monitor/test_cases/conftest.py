# -*- coding:utf-8 -*-
import pytest
import allure
from tools.dispose_data import read_yaml_data
from commons.config import PROJECT_PATH
from pages.base_page import BaseBase
from commons.init import *


@pytest.fixture()
def swipe_up():
    """
    初始化：向上滑动
    清除：向下滑动
    """
    # print('初始化操作')
    sleep(1)
    poco.swipe([0.5, 0.8], [0.5, 0.3], duration=0.3)
    # swipe([0.5*w, 0.5*h], [0.5*w, 0], duration=0.3)
    # yield
    # # # # print('清除操作')
    # sleep(1)
    # poco.swipe([0.5, 0.5], [0.5, 1], duration=0.3)


@pytest.fixture(autouse=True)
def init_setup():
    """
    初始化：判断退出按钮是否存在
    """
    # 判断退出按钮是否存在
    if poco('您確定要退出591嗎？').exists():
        poco('取消').click()
    elif poco(text='您確定要退出591嗎？').exists():
        poco(text='取消').click()


@pytest.fixture()
def init_setup2():
    """
    # 判断页面是否在首页
    """
    elem = poco("新建案")
    if elem.exists():
        elem.click()


@pytest.fixture()
def switch_region():
    """
    切换县市
    """
    yield
    basepage = BaseBase(poco)
    # 切换城市
    basepage.region_switch(region_id)




