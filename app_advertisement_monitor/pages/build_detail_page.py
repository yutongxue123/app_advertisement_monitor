# -*- coding:utf-8 -*-
from pages.base_page import BaseBase
from commons.init import *
from commons.config import PROJECT_PATH, API_DEVICE_INFO
import json


class NewBuildDetailPage(BaseBase):
    """
        新建案详情页
    """
    def __init__(self, poco):
        super().__init__(poco)
        self.file_path = PROJECT_PATH + '/page_img/newbuild_detailpage_img/'
        self.surrounding_img = self.common_img_path + 'tpl1702547654267.png'

    def swipe_up(self, duration=0.3):
        """
        向上滑动
        """
        poco.swipe([0.9, 0.7], [0.9, 0], duration=duration)

    def clear_login_pop_up(self):
        name = '下次一定'
        if self.poco_exist(name):
            self.poco.click(name)

    def get_build_list_hid(self, regionid):
        """
        获取新建案列表页广告第一个广告id
        """
        url = 'https://api.591.com.tw/api/housing/houseList'
        payload = {
            "keywords": "",
            "searchtype": "1",
            "regionid": f"{regionid}",
            "p": 1,
        }
        result = self.request('POST', url, json=payload)
        # formatted_result = json.dumps(result, indent=4, ensure_ascii=False)
        # print(formatted_result)
        return result['data'][0]['hid'], result['data'][0]['build_name'], result['data'][0]['photo_src']

    def get_recommend_build_img(self, hid):
        """
        获取新建案详情页推荐楼盘图片
        """
        url = 'https://union.591.com.tw/home/housing/getDetailRecom'
        payload = {
            'hid': f'{hid}',
            'limit': '7',
            'isindex': '1'
        }
        payload.update(API_DEVICE_INFO)
        result = self.request("GET", url, params=payload)
        return result['data'][0]['cover']


if __name__ == '__main__':
    # print(NewBuildDetailPage(poco).get_recommend_build_img(134523))
    print(NewBuildDetailPage(poco).get_build_list_hid(1))






