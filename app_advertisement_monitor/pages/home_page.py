# -*- coding:utf-8 -*-
from pages.base_page import BaseBase
from commons.init import *
from commons.config import PROJECT_PATH, API_DEVICE_INFO


class HomePage(BaseBase):
    """
        591首页
    """

    def __init__(self, poco):
        super().__init__(poco)
        self.file_path = PROJECT_PATH + '/page_img/homepage_img/'
        self.img_path = PROJECT_PATH + '/page_img/common_img/'

    def get_homepage_advertisement(self, regionid, advertisement_position_id):
        """
        获取首页广告数据
        :return: 广告列表，包含广告的图片地址、物件的url
        """
        img_list = []
        for advertisement in self.advertisement_dict:
            if advertisement['id'] == advertisement_position_id:
                for info in advertisement['info']:
                    if info['regionid'] == regionid:
                        for img in info['img']:
                            if img['img'] != '':
                                img_list.append(img['img'])
        return img_list

    def get_recommend_advertisement(self):
        """
        获取首页推荐广告
        :return: 推荐广告列表：包含regionid、img，仅取一个县市的推荐广告
        """
        img_dict = {}
        for advertisement in self.advertisement_dict:
            if advertisement['id'] == 44:
                for info in advertisement['info']:  # info是一个列表,包含所有县市的广告
                    for i in range(len(info['img'])):  # 遍历每个县市的广告
                        if info['img'][i]['img'] != '':
                            if not img_dict:
                                img_dict['regionid'] = info['regionid']
                                img_dict['img'] = [info['img'][i]['url']]
                            img_dict['img'].append(info['img'][i]['url'])
                        if i+1 == len(info['img']) and img_dict != {}:
                            return img_dict

    def click_cover_advertisement(self):
        """
        点击首页横幅广告
        """
        touch([0.51 * w, 0.18 * h])

    def is_guess_you_like_list_advertisement(self, region_id):
        """
        判断猜你喜欢列表广告是否可以点击
        """
        guess_you_like_img_list = self.get_guess_you_like_list_img(region_id)
        print(guess_you_like_img_list)
        # guess_you_like_img_list = ['https://hp3.591.com.tw/banner/170123483365850304.jpg']
        for i in range(4):
            # 向上滑动页面
            self.swipe_up()
            # 判断猜你喜欢广告是否存在
            if self.images_exist_and_click(guess_you_like_img_list, self.file_path, threshold=0.8):
                return True
        return False

    def is_guess_you_like_list_advertisement2(self):
        """
        判断猜你喜欢列表广告是否可以点击
        """
        for i in range(4):
            # 向上滑动页面
            sleep(1)
            self.swipe_up()
            self.swipe_up()
            # 判断猜你喜欢广告是否存在
            name = 'com.addcn.android.house591:id/iv_cover'
            if self.poco_exist(name):
                self.poco(name).click()
                return True
        return False
        # return False
        # while not self.poco_exist(text="猜你喜歡"):
        #     self.swipe_up()
        #     if self.poco_exist(text='猜你喜歡'):
        #         if self.poco_exist('com.addcn.android.house591:id/iv_cover'):
        #             self.poco('com.addcn.android.house591:id/iv_cover').click()
        #             return True
        # return False

    def get_guess_you_like_list_img(self, regionid):
        """
        获取首页猜你喜欢广告, 请求参数动态的，根据APP本地存储用户的行为，来传递不同的参数
        :return: 广告列表，包含广告的图片地址、物件的url
        """
        img_list = []
        url = f'https://api.591.com.tw/api/recom/guessLike'
        payload = {
            "search_type": "1",
            "regionid": f"{regionid}",
            # "tag": "12",
            # "build_id": "132397,125302,128751",
            # "keywords": "大直街",
        }
        payload.update(API_DEVICE_INFO)
        print(payload)
        result = self.request('GET', url, params=payload)
        for j in range(len(result['data']['items'])):
            if j > 2:
                break
            img_list.append(result['data']['items'][j]['cover'])
        return img_list

    def get_recommend_list_img(self, regionid):
        """
        获取首页猜推荐广告
        :return: 广告列表，包含广告的图片地址、物件的url
        """
        img_list = []
        url = 'https://union.591.com.tw/advert'
        payload = {
            "pid": "44",
            "regionid": f"{regionid}",
        }
        payload.update(API_DEVICE_INFO)
        result = self.request('GET', url, params=payload)
        for advertisement in result['data']['84']:
            img_list.append(advertisement['img'])


if __name__ == '__main__':
    homepage = HomePage(poco)
    print(homepage.get_guess_you_like_list_img(1))







