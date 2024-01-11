import pytest
import allure
from pages.home_search_page import HomeSearchPage
from pages.build_home_page import NewBuildHomePage
from commons.init import *
from commons.common import get_test_data


@allure.epic('APP广告监控')
@allure.story('APP首页搜索')
class TestBuildSearchPage:
    def setup_class(self):
        init_device()
        self.testdata = get_test_data(__file__)
        self.region_id = self.testdata['region_id']
        self.home_searchpage = HomeSearchPage(poco)
        # 进入首页
        self.home_searchpage.click_home()
        # 切换城市
        self.home_searchpage.region_switch(self.home_searchpage.region_dict[self.region_id])
        # 进入搜索页
        self.home_searchpage.into_search_page()
        sleep(3)
        # 切换搜索类型为新建案
        self.home_searchpage.switch_new_build()
        # 获取区域关键词广告
        self.region_list_img = self.home_searchpage.get_home_build_list_img(self.region_id, self.testdata['keywords'])

    def setup_method(self):
        self.home_searchpage.init_search_page()

    @allure.title('文字链接搜索')
    def test_search_box_text_link(self):
        """
        测试搜索框文字链接
        """
        # 点击搜索框文字链接
        self.home_searchpage.confirm()
        if self.home_searchpage.img_wait_exist(self.home_searchpage.build_list_img):
            print('搜索框文字链接广告存在')
        else:
            # 判断广告详情页是否存在
            assert_true(self.home_searchpage.is_detail_page_exist())

    @allure.title('热门关键词搜索')
    def test_hot_keyword_search(self):
        """
        测试热门关键词搜索
        """
        # 获取热门关键词
        hot_keyword_list = self.home_searchpage.get_hot_search_text()
        # 清空搜索历史
        self.home_searchpage.clear_history()
        sleep(3)
        assert_true(self.home_searchpage.pocos_exist_and_click(hot_keyword_list))
        # 判断广告详情页是否存在
        assert_true(self.home_searchpage.is_detail_page_exist())

    @allure.title('区域关键词搜索')
    def test_region_search(self):
        """
        测试区域关键字搜索
        """
        # 区域关键词搜索
        self.home_searchpage.input_content_search(self.testdata['keywords'])
        assert_true(self.home_searchpage.images_exist_and_click(self.region_list_img, self.home_searchpage.file_path))
        # 判断广告详情页是否存在
        assert_true(self.home_searchpage.is_detail_page_exist())
        self.home_searchpage.go_back()

    def teardown_method(self):
        self.home_searchpage.go_back()

    def teardown_class(self):
        self.home_searchpage.go_back()


