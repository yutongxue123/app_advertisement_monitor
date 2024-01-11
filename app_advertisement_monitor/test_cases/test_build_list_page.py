import pytest
import allure
from pages.build_list_page import BuildListPage
from pages.build_home_page import NewBuildHomePage
from commons.init import *


@allure.epic('APP广告监控')
@allure.feature('新建案列表页')
class TestBuildListPage:
    pytestmark = pytest.mark.usefixtures("init_setup2")

    def setup_class(self):
        init_device()
        # 创建新建案列表页对象
        self.build_listpage = BuildListPage(poco)
        self.build_homepage = NewBuildHomePage(poco)
        self.region_id = region_id
        # 进入首页
        self.build_listpage.click_home()
        # 切换城市
        self.build_listpage.region_switch(self.build_listpage.region_dict[self.region_id])
        # 进入新建案首页
        self.build_listpage.swipe_homepage_to_the_top()
        self.build_homepage.click_new_build()
        sleep(1)

    def setup_method(self):
        self.build_listpage.init_build_home_page()

    @allure.title('所有建案列表广告')
    def test_all_build_list_page(self):
        """
        测试所有建案列表广告
        """
        # 进入全部建案列表页
        self.build_listpage.into_all_build_list()
        # 获取全部新建案列表广告
        all_list_img = self.build_homepage.get_build_home_list_img(self.region_id)
        # 判断全部新建案列表广告是否存在,且可以点击,并进入广告详情页
        assert_true(self.build_listpage.images_exist_and_click(all_list_img, self.build_listpage.file_path))
        # 判断广告详情页是否存在
        assert_true(self.build_listpage.is_detail_page_exist())

    @allure.title('最新建案列表广告')
    def test_latest_build_list_page(self):
        """
        测试最新建案列表广告
        """
        # 进入建案列表页
        self.build_listpage.into_latest_build_list()
        # 获取新建案列表广告
        latest_list_img = self.build_listpage.get_latest_build_list_img(self.region_id)
        # 判断新建案列表广告是否存在,且可以点击,并进入广告详情页
        assert_true(self.build_listpage.images_exist_and_click(latest_list_img, self.build_listpage.file_path))
        # 判断广告详情页是否存在
        assert_true(self.build_listpage.is_detail_page_exist())

    @allure.title('即将发布列表广告')
    def test_upcoming_release_list_page(self):
        """
        测试即将发布列表广告
        """
        # 进入即将发布列表页
        self.build_listpage.into_upcoming_release_list()
        # 获取即将发布列表广告
        list_img = self.build_listpage.get_upcoming_release_list_img(self.region_id)
        # for i in range(3):
        #     if self.build_listpage.imgs_exist(list_img, self.build_listpage.file_path):
        #         # 判断即将发布列表广告是否存在,且可以点击,并进入广告详情页
        #         assert_true(self.build_listpage.images_exist_and_click(list_img, self.build_listpage.file_path))
        #         break
        #     else:
        #         self.build_listpage.swipe_down()
        # 判断即将发布列表广告是否存在,且可以点击,并进入广告详情页
        assert_true(self.build_listpage.images_exist_and_click(list_img, self.build_listpage.file_path))
        # 判断广告详情页是否存在
        assert_true(self.build_listpage.is_detail_page_exist())

    @allure.title('精選建案列表广告')
    def test_choice_build_list_page(self):
        """
        测试精選建案列表广告
        """
        # 进入精选建案列表页
        self.build_listpage.into_choice_build_list()
        # 获取精选建案列表广告
        choice_list_img = self.build_listpage.get_choice_build_list_img(self.region_id)
        # 判断精选建案列表广告是否存在,且可以点击,并进入广告详情页
        assert_true(self.build_listpage.images_exist_and_click(choice_list_img, self.build_listpage.file_path))
        # 判断广告详情页是否存在
        assert_true(self.build_listpage.is_detail_page_exist())

    @allure.title('专属服务列表广告')
    @pytest.mark.skip(reason="暂时不执行")
    def test_dedicated_service_list_page(self):
        """
        测试专属服务列表广告
        """
        # 进入专属服务列表页
        self.build_listpage.into_dedicated_service_list()
        # 获取专属服务列表广告
        dedicated_list_img = self.build_listpage.get_dedicated_service_list_img(self.region_id)
        # 判断专属服务列表广告是否存在,且可以点击,并进入广告详情页
        assert_true(self.build_listpage.images_exist_and_click(dedicated_list_img, self.build_listpage.file_path))
        # 判断广告详情页是否存在
        assert_true(self.build_listpage.is_detail_page_exist())

    @allure.title('特色标签列表广告')
    def test_tag_list_page(self):
        """
        测试特色标签列表广告
        """
        # 进入标签列表页
        self.build_listpage.into_tag_list()
        # 获取标签列表广告
        dedicated_list_img = self.build_listpage.get_tag_list_img(self.region_id)
        # 判断标签列表广告是否存在,且可以点击,并进入广告详情页
        assert_true(self.build_listpage.images_exist_and_click(dedicated_list_img, self.build_listpage.file_path))
        # 判断广告详情页是否存在
        assert_true(self.build_listpage.is_detail_page_exist())

    def teardown_method(self):
        # 返回新建案首页
        self.build_listpage.go_back()
        self.build_listpage.go_back()

