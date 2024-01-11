import allure

from pages.base_page import BaseBase
from commons.config import PROJECT_PATH, API_DEVICE_INFO
from commons.init import *


class HomeSearchPage(BaseBase):
    """
    首页搜索
    """
    def __init__(self, poco):
        super().__init__(poco)
        self.file_path = PROJECT_PATH + '/page_img/home_search_page_img/'
        self.build_list_img = PROJECT_PATH + '/page_img/common_img/tpl1702974607952.png'

    def into_search_page(self):
        """
        进入搜索页
        """
        # # self.poco_wait_click("com.addcn.android.house591:id/et_edittext")
        # if self.poco_exist(text="社區/街道/商圈/編號"):
        #     self.poco(text="社區/街道/商圈/編號").click()
        #     if self.poco_exist(nameMatches="首頁\n.*"):
        #         self.poco('android.view.View').child(type='android.widget.ImageView')[2].click()
        # elif self.poco_exist('社區/街道/商圈/編號'):
        #     self.poco('社區/街道/商圈/編號').click()
        self.click_img(PROJECT_PATH + '/page_img/common_img/tpl1704358680379.png')
        if self.poco_exist(text='首頁'):
            self.poco(text='社區/街道/商圈/編號').click()
        elif self.poco_exist(nameMatches="首頁\n.*"):
            self.poco('社區/街道/商圈/編號').click()

    def switch_new_build(self):
        """
        选择新建案
        """
        if not self.poco("新建案").exists():
            self.poco("出租").wait().click()
            self.poco_wait_click('新建案')

    def clear_history(self):
        """
        清除搜索历史
        """
        self.poco_exist_and_click("清空")

    def input_content_search(self, content):
        self.input_text(content, 'android.widget.EditText')
        keyevent("ENTER")
        if self.poco('android.widget.EditText').exists():
            keyevent("ENTER")

    def get_search_advert_text(self, regionid):
        """
        新建案搜索页热词广告热词
        """
        url = f'https://union.591.com.tw/advert?device=android&pid=65&regionid={regionid}'
        result = self.request('GET', url)
        text_list = []
        for advertisement in result['data']['105']:
            text_list.append(advertisement['txt'])
        return text_list

    def get_hot_search_text(self):
        """
        新建案搜索页热词广告热词
        """
        url = 'https://api.591.com.tw/api/housing/hotSearch'
        result = self.request('POST', url, json=API_DEVICE_INFO)
        text_list = []
        for advertisement in result['data']:
            text_list.append(advertisement['build_name'])
        return text_list

    def get_home_build_list_img(self, regionid, keywords):
        """
        新建案列表广告
        """
        payload = {
            "keywords": keywords,
            "searchtype": "1",
            "regionid": f"{regionid}",
            "p": 1,
        }
        payload.update(API_DEVICE_INFO)
        return self.get_build_list_img(payload)

    def get_text_link_img(self, region_id):
        """
        获取搜索框文字链接广告
        """
        url = 'https://union.591.com.tw/advert'
        payload = {
            "pid": "64",
            "regionid": f"{region_id}",
        }
        payload.update(API_DEVICE_INFO)
        result = self.request('GET', url, params=payload)
        return result['data']['104'][0]["url"]

    def init_search_page(self):
        # 如果当前页面是在首页,则进入搜索页
        if self.poco(nameMatches="首頁\n.*").exists():
            # 进入搜索页
            self.into_search_page()


if __name__ == '__main__':
    searchpage = HomeSearchPage(poco)
    txt_list = searchpage.get_text_link_img(3)
    print(txt_list)




