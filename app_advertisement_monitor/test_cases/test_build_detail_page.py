import pytest
import allure
from pages.build_detail_page import NewBuildDetailPage
from pages.build_home_page import NewBuildHomePage
from pages.build_search_page import BuildSearchPage
from commons.init import *


@allure.epic('APP广告监控')
@allure.feature('新建案详情页')
class TestBuiDetailPage:
    pytestmark = pytest.mark.usefixtures("init_setup2")

    def setup_class(self):
        init_device()
        self.build_detailpage = NewBuildDetailPage(poco)
        self.build_homepage = NewBuildHomePage(poco)
        self.build_searchpage = BuildSearchPage(poco)
        self.region_id = region_id
        # 进入首页
        self.build_detailpage.click_home()
        # 切换城市
        self.build_detailpage.region_switch(self.build_detailpage.region_dict[self.region_id])
        # 进入新建案首页
        self.build_detailpage.swipe_homepage_to_the_top()
        self.build_homepage.click_new_build()
        sleep(3)
        # 获取首页列表图片
        self.build_hid = self.build_detailpage.get_build_list_hid(self.region_id)
        # 获取推荐建案图片
        self.recommend_build_img = self.build_detailpage.get_recommend_build_img(self.build_hid[0])

    def setup_method(self):
        self.build_detailpage.init_build_home_page()

    @allure.title('新建案详情页推荐广告')
    def test_recommend_build_detail_page(self):
        """
        测试新建案详情页推荐楼盘是否可以点击
        """
        # 进入新建案搜索页
        self.build_searchpage.into_search_page()
        # 输入建案名称,并点击搜索
        self.build_searchpage.input_content_search(self.build_hid[1])
        # 进入详情页
        self.build_homepage.image_exist_and_click(self.build_hid[2], self.build_detailpage.file_path)
        # 判断推荐建案是否存在
        sleep(2)
        self.build_detailpage.swipe_up()
        self.build_detailpage.clear_login_pop_up()
        self.build_detailpage.img_wait_click(self.build_detailpage.surrounding_img)
        self.build_detailpage.swipe_up()
        assert_true(self.build_detailpage.image_wait_and_click(self.recommend_build_img, self.build_detailpage.file_path))
        assert_true(self.build_detailpage.is_detail_page_exist())

    def teardown_method(self):
        # 返回新建案首页
        self.build_detailpage.go_back()
        self.build_detailpage.go_back()

