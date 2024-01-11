from pages.base_page import BaseBase
from commons.config import PROJECT_PATH, API_DEVICE_INFO
from commons.init import *


class LoginPage(BaseBase):
    """
    登录页
    """
    def __init__(self, poco):
        super().__init__(poco)

    def login(self, username, password, env):
        # 第一次启动APP，需要点击的弹窗(包括系统访问权限和591APP的弹窗)
        try:
            # 开启591 ，下一步
            poco(text='下一步').click()
            # 获取拨打电话权限
            poco(text='允许').click()
            # 获取位置信息权限，选择【仅在使用该应用时允许】
            poco(text='仅在使用该应用时允许').click()
            # 获取照片和媒体权限
            poco(text='允许').click()
            # 选择城市
            poco(text='選擇縣市').click()
            # 在城市列表选择县市，我这里选择：台北市
            poco('android.view.View').child('android.view.View')[1].click()
            # 同意隐私条款
            poco(text='同意').click()
        except:
            pass
        # 点击广告：跳过
        #     try:
        #         poco(text="跳過").click()
        #     except:
        #         pass
        # 如果有广告，则点击
        if poco('com.addcn.android.house591:id/sml_refresh ').exists():
            poco('com.addcn.android.house591:id/sml_refresh ').click()
        else:
            pass

        # 進入我的模塊
        poco(text='我的').wait(10).click()
        # 点击设置
        poco('com.addcn.android.house591:id/iv_more').click()

        # # 判断是否已有账号登录，如果有，则不进行登录
        # if poco('退出登入').wait(2):
        #     print('已有账号登录')
        #     # 退出账号设置页面
        #     poco('android.widget.ImageView')[1].wait(2).click()

        # 判断是否是debug包
        try:
            # 点击测试工具选项
            poco('測試工具').wait(10).click()
            # 定位环境切换按钮的文本
            elem = poco('com.addcn.android.house591:id/bt_change_debug')
            # 切换APP环境
            if elem.attr('text') != env:
                elem.click()
            # 退出测试工具页面
            poco('com.addcn.android.house591:id/ib_back').click()
        except:
            pass

        # 判断是否已有账号登录，如果有，则退出登录在进行登录
        if poco('退出登入').wait(2):
            poco('退出登入').click()
            poco('確定').click()

        # 退出账号设置页面
        poco('android.widget.ImageView')[1].wait(2).click()
        # 执行登录操作
        # 1. 输入账号
        poco('com.addcn.android.house591:id/et_mine_id').set_text(username)
        # 2. 输入密码
        poco('com.addcn.android.house591:id/et_mine_password').set_text(password)
        # 3. 点击登录按钮
        poco('com.addcn.android.house591:id/btn_mine_login').click()
        # 4. 若是存在弹窗，则清除弹窗
        for i in range(2):
            if self.poco_exist('com.addcn.android.house591:id/iv_mine_avatar'):
                print('登录成功')
                break
            self.img_exist_and_click(self.common_img_path + 'tpl1702374419487.png')


if __name__ == '__main__':
    login_page = LoginPage(poco)
    init_device()
    # login_page.login('0921223333','tw591TW;', '線上')
    login_page.login('0978654732','wentao123', 'DEBUG')






