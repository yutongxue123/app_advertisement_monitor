import pytest
from pages.build_home_page import NewBuildHomePage
from pages.home_page import HomePage
from commons.init import *
from commons.common import get_advertisement_img
import allure


@allure.epic('APP广告监控')
@allure.feature('新建案首页')
class TestBuildHomePage:
    pytestmark = pytest.mark.usefixtures("init_setup2")

    def setup_class(self):
        init_device()
        # 创建新建案首页对象
        self.build_homepage = NewBuildHomePage(poco)
        self.region_id = region_id
        # 进入首页
        self.build_homepage.click_home()
        # 切换城市
        self.build_homepage.region_switch(self.build_homepage.region_dict[ self.region_id])
        self.build_homepage.swipe_homepage_to_the_top()
        # 进入新建案首页
        self.build_homepage.click_new_build()
        sleep(1)
        # 获取新建案首页列表广告
        self.list_img = self.build_homepage.get_build_home_list_img(self.region_id)
        # 获取新建案首页列表感兴趣广告
        self.list_interest_img = self.build_homepage.get_build_home_interesting_img(self.region_id)
        # # 获取新建案首页右侧下方广告
        # self.right_focus_img_dict = self.build_homepage.get_build_focus_right_img(self.region_id)
        # # 右侧上方广告
        # self.right_img_1 = self.right_focus_img_dict['waist']
        # # 右侧下方广告
        # self.right_img_2 = self.right_focus_img_dict['topic']

    def setup_method(self):
        self.build_homepage.init_build_home_page()

    @allure.title('新建案首页封面广告')
    def test_cover_advertisement(self):
        """
        判断新建案首页封面广告是否可以点击
        """
        # 获取新建案首页封面广告
        cover_img_list = self.build_homepage.get_build_cover_img(self.region_id)
        # 判断封面广告是否存在
        assert_true(self.build_homepage.images_exist_and_click(cover_img_list, self.build_homepage.file_path))
        # # 判断广告详情页是否存在
        assert_true(self.build_homepage.is_detail_page_exist())

    @allure.title('新建案首页左侧焦点广告')
    @pytest.mark.parametrize('img_url', get_advertisement_img(region_id, 91))
    def test_focus_advertisement(self, img_url):
        """
        判断新建案首页焦点左侧轮播图是否可以点击
        """
        # 判断轮播图是否存在,且可以点击,并进入广告详情页
        assert_true(self.build_homepage.image_wait_and_click(img_url, self.build_homepage.file_path, threshold=0.5, img_url=False))
        # 判断广告详情页是否存在
        assert_true(self.build_homepage.is_detail_page_exist())

    @allure.title('新建案首页右侧焦点广告a')
    def test_focus_right_advertisement_a(self):
        """
        判断新建案首页焦点右侧上方广告位是否可以点击
        """
        self.build_homepage.is_focus_right_advertisement(self.region_id, 0, 94)

    @allure.title('新建案首页右侧焦点广告b')
    def test_focus_right_advertisement_b(self):
        """
        判断新建案首页焦点右侧下方广告位是否可以点击
        """
        self.build_homepage.is_focus_right_advertisement(self.region_id, 1, 95)

    @allure.title('新建案首页列表广告')
    @pytest.mark.usefixtures('swipe_up')
    def test_list_advertisement(self, swipe_up):
        """
        判断新建案首页列表广告是否可以点击
        备注：执行fixture操作, 没有返回值
        """
        # 判断右侧广告位是否存在,且可以点击,并进入广告详情页
        assert_true(self.build_homepage.images_exist_and_click(self.list_img, self.build_homepage.file_path))
        # 判断广告详情页是否存在
        assert_true(self.build_homepage.is_detail_page_exist())

    @allure.title('新建案首页感兴趣广告')
    def test_list_interested_advertisement(self):
        """
        判断新建案首页列表感兴趣广告是否可以点击
        """
        if self.list_interest_img:
            self.build_homepage.swipe_to_the_top()
            self.build_homepage.swipe_up()
            # 判断右侧广告位是否存在,且可以点击,并进入广告详情页
            assert_true(self.build_homepage.images_exist_and_click(self.list_interest_img, self.build_homepage.file_path))
            # 判断广告详情页是否存在
            assert_true(self.build_homepage.is_detail_page_exist())
        else:
            print('感兴趣广告不存在')

    def teardown_method(self):
        self.build_homepage.go_back()


if __name__ == '__main__':
    pytest.main(['-svq', 'test_cases/test_build_home_page.py', '--reruns 2 --reruns-delay 2'])
