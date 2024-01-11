from pages.base_page import BaseBase
from commons.config import PROJECT_PATH, API_DEVICE_INFO
from commons.init import *


class BuildSearchPage(BaseBase):
    """
    建案搜索页
    """
    def __init__(self, poco):
        super().__init__(poco)
        self.file_path = PROJECT_PATH + '/page_img/build_search_page_img/'

    def input_content_search(self, content):
        self.input_text(content, 'android.widget.EditText')
        keyevent("ENTER")
        if self.poco('android.widget.EditText').exists():
            keyevent("ENTER")

    def into_search_page(self):
        """
        进入建案搜索页
        """
        # self.poco_wait_click("建案名、位置或區域")
        self.click_img(PROJECT_PATH + '/page_img/common_img/tpl1704359076591.png')

    def clear_history(self):
        """
        清除搜索历史
        """
        self.poco_exist_and_click("清空")

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

    def init_build_search_page(self):
        # 如果当前页面不是新建案搜索页,则返回新建案搜索页
        if self.poco(nameMatches="首頁\n.*").exists():
            self.swipe_homepage_to_the_top()
            # 进入新建案首页
            self.poco("新建案").wait().click()
            # 进入新建案搜索页
            self.into_search_page()


if __name__ == '__main__':
    searchpage = BuildSearchPage(poco)
    txt_list = searchpage.get_search_advert_text(1)
    print(txt_list)
    searchpage.into_search_page()
    searchpage.poco_wait_click(txt_list[0])




