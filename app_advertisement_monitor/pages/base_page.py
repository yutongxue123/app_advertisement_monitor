from commons.init import *
from tools.dispose_data import *
from commons.config import PROJECT_PATH
from commons.file_operations import download_img, get_small_img
import requests, json


class BaseBase:
    """
    包含
    通用的页面操作：切换城市，点击首页、循环查找图片是否存在、点击图片、点击广告详情、返回上一页
    以及系统页面的操作
    """
    region_dict = {1: '台北市', 2: '基隆市', 3: '新北市', 4: '新竹市', 5: '新竹縣', 6: '桃園市', 7: '苗栗縣', 8: '台中市', 10: '彰化縣', 11: '南投縣', 12: '嘉義市', 13: '嘉義縣', 14: '雲林縣', 15: '台南市', 17: '高雄市', 19: '屏東縣', 21: '宜蘭縣', 22: '台東縣', 23: '花蓮縣', 24: '澎湖縣', 25: '金門縣', 26: '連江縣', 99: '海外'}

    def __init__(self, poco):
        self.poco = poco
        self.advertisement_dict = read_yaml_data(PROJECT_PATH + '/test_data/advertisement_data.yaml')
        self.common_img_path = PROJECT_PATH + '/page_img/common_img/'

    def go_back(self):
        """
        返回上一页
        """
        keyevent('BACK')

    def confirm(self):
        """
        确定
        """
        keyevent('ENTER')

    def read_advertisement_data(self):
        """
        读取广告数据
        :return: 广告数据
        """
        return read_yaml_data(PROJECT_PATH + '/test_data/advertisement_data.yaml')

    def click_home(self):
        """
        点击首页tab
        """
        if self.poco_wait_click(text="首頁", timeout=20):
            return True
        else:
            self.poco(nameMatches="首頁\n.*").wait(20).click()

    def swipe_homepage_to_the_top(self):
        """
        若当前首页不在顶部，则向上滑动至顶部
        """
        while not (self.poco_exist('商用地產') or self.poco_exist(text='商用地產')):
        # while not self.img_exist(PROJECT_PATH + '/page_img/common_img/tpl1702621485230.png'):
            self.swipe_down()

    def region_switch(self, region_name):
        """
        切换城市
        """
        if self.poco_exist('com.addcn.android.house591:id/tv_chooseCity'):
            pos = self.poco('com.addcn.android.house591:id/tv_chooseCity')
            if pos.get_text() != region_name:
                pos.click()
                if self.poco('您確定要退出591嗎？').exists():
                    self.poco('取消').click()
                if self.poco_exist(nameMatches="首頁\n.*"):
                    if self.poco_exist(nameMatches=".*市"):
                        self.poco(nameMatches=".*市").click()
                    elif self.poco_exist('全台湾'):
                        self.poco('全台湾').click()
                    else:
                        self.poco(nameMatches=".*縣").click()
                self.poco(region_name).click()
        else:
            if not self.poco_exist(region_name):
                if self.poco_exist(nameMatches=".*市"):
                    self.poco(nameMatches=".*市").click()
                elif self.poco_exist('全台湾'):
                    self.poco('全台湾').click()
                else:
                    self.poco(nameMatches=".*縣").click()
                self.poco(region_name).click()
        self.img_exist_and_click(self.common_img_path + 'tpl1702374419487.png')
        if self.poco('您確定要退出591嗎？').exists():
            self.poco('取消').click()

    def get_advertisement_img(self, regionid, advertisement_position_id):
        """
        获取广告图片,如果图片url为空，则获取图片所属物件的url
        :return: 广告url列表
        """
        img_list = []
        for advertisement in self.advertisement_dict:
            if advertisement['id'] == advertisement_position_id:
                for info in advertisement['info']:
                    if info['regionid'] == regionid:
                        for img in info['img']:
                            if img['img'] is not None:
                                img_list.append(img['img'])
                            else:
                                img_list.append(img['url'])
        return img_list

    def imgs_exist(self, img_list, file_path, img_url=True):
        """
        多图查找，仅判断图片是否存在
        :param img_list: 图片url列表
        :param img_url:  若是有图片url，则直接下载图片，否则获取图片的url,再下载图片
        :param file_path: 保存图片路径
        :return: 存在返回True，不存在返回False
        """
        for img in img_list:
            if img_url:
                img = download_img(file_path, img)
            else:
                img = get_small_img(file_path, img)
            return self.img_wait_exist(img)

    def img_exist_and_click(self, img):
        """
        单图片查找，存在则点击
        :param img: 图片文件路径
        """
        pos = self.exist(img)
        if pos:
            touch(pos)
            return True

    def images_exist_and_click(self, img_list: list, file_path: str, threshold=0.7, img_url=True):
        """
        多图查找(循环查找)，存在则点击（不增加等待时间）
        :param img_list:  获取图片url列表
        :param img_url:  若是有图片url，则直接下载图片，否则获取图片的url,再下载图片
        :param threshold:  图片相似度的阈值
        :param file_path: 保存图片路径
        :return: true or false
        """
        for img in img_list:
            if img_url:
                img = download_img(file_path, img)
            else:
                img = get_small_img(file_path, img)
            pos = self.exist(img, threshold=threshold)
            if pos:
                touch(pos)
                return True
        return False

    def images_wait_and_click(self, img_list: list, file_path: str, threshold=0.7, img_url=True):
        """
        多图查找(循环查找)，存在则点击(增加等待时间)
        :param img_list:  获取图片url列表
        :param img_url:  若是有图片url，则直接下载图片，否则获取图片的url,再下载图片
        :param threshold:  图片相似度的阈值
        :param file_path: 保存图片路径
        :return: true or false
        """
        for img in img_list:
            if img_url:
                img = download_img(file_path, img)
            else:
                img = get_small_img(file_path, img)
            if self.img_wait_click(img, threshold=threshold):
                return True
        return False

    def image_exist_and_click(self, img, file_path: str, threshold=0.7, img_url=True):
        """
        单图查找，存在则点击，不增加等待时间
        :param threshold:  图片相似度的阈值
        :param file_path: 保存图片路径
        :return: true or false
        """
        if img_url:
            img = download_img(file_path, img)
        else:
            img = get_small_img(file_path, img)
        pos = self.exist(img, threshold=threshold)
        if pos:
            touch(pos)
            return True
        return False

    def image_wait_and_click(self, img: str, file_path: str, threshold=0.6, img_url=True):
        """
        单图片查找，存在则点击,增加等待时间
        :param img:  获取图片
        :param img_url:  若是有图片url，则直接下载图片，否则获取图片的url,再下载图片
        :param file_path: 保存图片路径
        :return: true or false
        """
        if img_url:
            img = download_img(file_path, img)
        else:
            img = get_small_img(file_path, img)
        # 进入广告详情页
        if self.img_wait_click(img, threshold=threshold):
            return True
        return False

    def img_wait_click(self, img, threshold=0.6, timeout=20):
        """
        通过wait方法测试图片是否存在，存在则返回图片坐标，并点击坐标,不存在则会抛出异常
        :param img: 图片
        """
        try:
            loc = wait(Template(r'%s' % img, resolution=(w, h), threshold=threshold), timeout=timeout)
            touch(loc)
            return True
        except TargetNotFoundError:
            print("图片不存在")

    def swipe_down(self, duration=0.3):
        """
        向下滑动
        """
        poco.swipe([0.5, 0.2], [0.5, 1], duration=duration)
        # swipe((0.5*w, 0.1*h), (0.5*w, h), duration=duration)

    def swipe_up(self, duration=0.3):
        """
        向上滑动
        """
        poco.swipe([0.5, 0.8], [0.5, 0], duration=duration)
        # swipe((0.5 * w, 0.8 * h), (0.5 * w, 0), duration=duration)

    def poco_not_exist_swipe_up(self, poco=None, text=None, name=None):
        """
        当控件不存在时，向上滑动
        """
        if poco is not None:
            if not self.poco_exist(poco):
                self.swipe_up()
        elif text is not None:
            if not self.poco_exist(text=text):
                self.swipe_up()
        elif name is not None:
            if not self.poco_exist(name=name):
                self.swipe_up()

    def refresh_page(self):
        """
        刷新页面
        """
        poco.swipe([0.5, 0.2], [0.5, 0.5], duration=0.3)
        self.img_exist_and_click(self.common_img_path + 'tpl1702374419487.png')

    def click_img(self, img):
        """
        根据图片模板匹配图片，并点击图片中心点坐标
        """
        touch(Template(rf"{img}", resolution=(w, h)))

    def exist(self, img, threshold=0.7):
        """
        判断图片是否存在,并返回图片中心点坐标，不存在则返回False
        """
        return exists(Template(r"{}".format(img), resolution=(w, h), threshold=threshold))

    def is_detail_page_exist(self):
        """
        判断详情页广告是否存在
        """
        sleep(1)
        if exists(Template(r"{}tpl1697625583157.png".format(self.common_img_path), resolution=(w, h))) or exists(Template(r"{}tpl1700452300405.png".format(self.common_img_path), resolution=(w, h))) or exists(Template(r"{}tpl1701669156676.png".format(self.common_img_path), resolution=(w, h))) or exists(Template(r"{}tpl1702624089962.png".format(self.common_img_path), resolution=(w, h))) or exists(Template(r"{}tpl1702968114352.png".format(self.common_img_path), resolution=(w, h))):
            return True
        else:
            return False

    def img_wait_exist(self, img):
        """
        判断图片是否存在
        :param img: 图片
        """
        try:
            wait(Template(r'%s' % img, resolution=(w, h), threshold=0.6))
            return True
        except TargetNotFoundError as e:
            print(e)
            return False

    def img_exist(self, img):
        """
        判断图片是否存在
        :param img: 图片
        """
        return exists(Template(r'%s' % img, resolution=(w, h)))

    def poco_exist(self, poco=None, text=None, name=None, nameMatches=None, textMatches=None):
        """
        判断元素是否存在
        :param poco: 控件元素名
        :param text: 控件text属性
        :param name: 控件name属性
        :return: 存在返回True，不存在返回False
        """
        if poco is not None:
            return self.poco(poco).exists()
        elif text is not None:
            return self.poco(text=text).exists()
        elif name is not None:
            return self.poco(name=name).exists()
        elif nameMatches is not None:
            return self.poco(nameMatches=nameMatches).exists()
        elif textMatches is not None:
            return self.poco(textMatches=textMatches).exists()

    def poco_exist_and_click(self, poco=None, text=None, name=None):
        """
        判断元素是否存在，存在则点击
        :param poco: 控件元素名
        :param text: 控件text属性
        :param name: 控件name属性
        """
        if poco is not None:
            if self.poco_exist(poco):
                self.poco(poco).click()
        elif text is not None:
            if self.poco_exist(text=text):
                self.poco(text=text).click()
        elif name is not None:
            if self.poco_exist(name=name):
                self.poco(name=name).click()

    def input_text(self, content, poco=None, text=None, name=None):
        """
        输入文本
        :param content: 输入的文本内容
        :param poco: 控件元素名
        :param text: 控件text属性
        :param name: 控件name属性
        """
        if poco is not None:
            self.poco(poco).set_text(content)
        elif text is not None:
            self.poco(text=text).set_text(content)
        elif name is not None:
            self.poco(name=name).set_text(content)

    def pocos_exist_and_click(self, poco_list):
        """
        循环遍历列表元素，判断元素是否存在,存在则点击
        :param poco: 控件元素
        :return: 存在返回True，不存在返回False
        """
        for txt in poco_list:
            if self.poco_wait_click(txt, timeout=3):
                return True
        return False

    def poco_wait_click(self, poco=None, text=None, timeout=10):
        """
        等待元素出现，存在则点击，否则抛出异常
        :param poco: 控件元素名
        :param timeout: 超时时间
        """
        try:
            if poco is not None:
                self.poco(poco).wait_for_appearance(timeout=timeout)
                self.poco(poco).click()
            elif text is not None:
                self.poco(text=text).wait_for_appearance(timeout=timeout)
                self.poco(text=text).click()
            return True
        except poco.PocoTargetTimeout as e:
            raise e

    def request(self, method, url, data=None, json=None, params=None,headers=None, **kwargs):
        """
        封装接口请求方法
        """
        headers = {
            'User-Agent': 'com.addcn.android/6.6.0.318/1080x2186/Android/12/SM-A525M/8ac9ec99-7f88-4e40-8988-ee6425f9eefd'}
        if method == 'GET':
            resp = requests.request(method, url, verify=False, params=params, headers=headers)
        elif method == 'POST':
            headers.update({'Content-Type': 'application/json'})

            resp = requests.request(method, url, data=data, json=json, verify=False, headers=headers)
        else:
            print('请求方法错误')
        if resp.status_code == 200:
            return resp.json()
        else:
            print('请求失败')
            print('详情状态码：', resp.status_code)

    def get_build_list_img(self, payload):
        """
        新建案列表广告
        """
        url = 'https://api.591.com.tw/api/housing/houseList'
        result = self.request('POST', url, json=payload)
        img_list = []
        for data in result['data']:
            if 'photo_src' in data.keys():
                img_list.append(data['photo_src'])
        return img_list

    def init_build_home_page(self):
        # 如果当前页面不是新建案首页,则返回新建案首页
        if self.poco(nameMatches="首頁\n.*").exists():
            self.swipe_homepage_to_the_top()
            # 进入新建案首页
            self.poco("新建案").wait().click()


if __name__ == '__main__':
    basepage = BaseBase(poco)



