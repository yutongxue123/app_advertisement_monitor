import allure
import pytest
from pages.build_search_page import BuildSearchPage
from pages.build_home_page import NewBuildHomePage
from commons.init import *


@allure.epic('APP广告监控')
@allure.feature('新建案首页搜索')
class TestBuildSearchPage:
    def setup_class(self):
        init_device()
        self.build_searchpage = BuildSearchPage(poco)
        self.build_homepage = NewBuildHomePage(poco)
        self.region_id = region_id
        # 进入首页
        self.build_searchpage.click_home()
        # 切换城市
        self.build_searchpage.region_switch(self.build_searchpage.region_dict[self.region_id])
        # 进入新建案首页
        self.build_searchpage.swipe_homepage_to_the_top()
        self.build_homepage.click_new_build()
        sleep(3)
        # 进入新建案搜索页
        self.build_searchpage.into_search_page()

    def setup_method(self):
        self.build_searchpage.init_build_search_page()

    @allure.title('新建案热词搜索')
    def test_hot_keyword_search(self):
        """
        测试热门关键词搜索
        """
        # 获取热门关键词
        hot_keyword_list = self.build_searchpage.get_hot_search_text()
        print(hot_keyword_list)
        sleep(1)
        # 清空搜索历史
        self.build_searchpage.clear_history()
        sleep(1)
        assert_true(self.build_searchpage.pocos_exist_and_click(hot_keyword_list))
        # 判断广告详情页是否存在
        assert_true(self.build_searchpage.is_detail_page_exist())

    def teardown_method(self):
        self.build_searchpage.go_back()

    def teardown_class(self):
        self.build_searchpage.go_back()


