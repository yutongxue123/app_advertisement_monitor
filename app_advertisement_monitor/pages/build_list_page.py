# -*- coding:utf-8 -*-
from pages.base_page import BaseBase
from commons.config import PROJECT_PATH, API_DEVICE_INFO
from commons.init import *


class BuildListPage(BaseBase):
    """
    建案列表页
    """
    def __init__(self, poco):
        super().__init__(poco)
        self.file_path = PROJECT_PATH + '/page_img/build_list_page_img/'

    def into_all_build_list(self):
        """
        进入全部新建案列表，默认等待3s
        """
        self.poco("全部建案").wait().click()

    def into_latest_build_list(self):
        """
        进入最新开案列表
        """
        self.poco('最新開案').wait().click()

    def into_upcoming_release_list(self):
        """
        进入即将发布列表
        """
        self.poco('即將推出').wait().click()

    def into_choice_build_list(self):
        """
        进入精选建案列表
        """
        self.poco('精選建案').wait().click()

    def into_dedicated_service_list(self):
        """
        进入专属服务列表
        """
        self.poco('專屬服務').wait().click()

    def into_tag_list(self):
        """
        进入特色标签列表
        """
        self.poco('低首付款').wait().click()

    def get_latest_build_list_img(self, regionid):
        """
        最新建案列表广告图片
        """
        payload = {
            "keywords": "",
            "searchtype": "1",
            "regionid": f"{regionid}",
            "p": 1,
            "o": "3",
            "open_sell_time": "5"
        }
        payload.update(API_DEVICE_INFO)
        return self.get_build_list_img(payload)

    def get_upcoming_release_list_img(self, regionid):
        """
        即将发布列表广告图片
        """
        payload = {
            "keywords": "",
            "searchtype": "1",
            "regionid": f"{regionid}",
            "p": 1,
            "o": "4",
            "open_sell_time": "3",
        }
        payload.update(API_DEVICE_INFO)
        return self.get_build_list_img(payload)

    def get_build_list_api(self, payload):
        """
        建案列表接口
        """
        url = 'https://m.591.com.tw/api/housing/houseListNew'
        result = self.request('POST', url, json=payload)
        img_list = []
        for data in result['data']:
            if 'photo_src' in data.keys():
                img_list.append(data['photo_src'])
        return img_list

    def get_choice_build_list_img(self, regionid):
        """
        精選建案列表广告
        """
        payload = {
                "p": 1,
                "is_package": 1,
                "regionid": [f"{regionid}", f"{regionid}"],
                "region_id": f"{regionid}",
            }
        payload.update(API_DEVICE_INFO)
        return self.get_build_list_api(payload)

    def get_dedicated_service_list_img(self, regionid):
        """
        专属服务列表广告
        """
        payload = {
            "p": 1,
            "search_type": "roster",
            "sort": 13,
            "regionid": f"{regionid}",
            "region_id": f"{regionid}"
        }
        payload.update(API_DEVICE_INFO)
        return self.get_build_list_api(payload)

    def get_tag_list_img(self, regionid):
        """
       特色标签列表广告
        """
        payload = {
            "access_token": "",
            "searchtype": "1",
            "regionid": f"{regionid}",
            "tag": "12",
            "o": "",
            "p": 1,
        }
        payload.update(API_DEVICE_INFO)
        return self.get_build_list_img(payload)


if __name__ == '__main__':
    listpage = BuildListPage(poco)
    print(listpage.get_upcoming_release_list_img(1))




