import pytest
from pages.home_page import HomePage
from commons.init import *
from commons.common import get_advertisement_img
import allure


@allure.epic('APP广告监控')
@allure.feature('APP首页')
class TestHomePage:
    def setup_class(self):
        init_device()
        self.homepage = HomePage(poco)
        self.region_id = region_id
        # 进入首页
        self.homepage.click_home()
        # 切换城市
        self.homepage.region_switch(self.homepage.region_dict[self.region_id])

    def setup_method(self):
        self.homepage.swipe_homepage_to_the_top()

    @pytest.mark.skip(reason='跳过')
    def test_pop_up_advertisement(self):
        """
        判断首页弹窗广告是否可以点击
        备注：由于每个县市的首页弹窗广告不一样，并且弹窗3s左右就会消失，所以不针对广告信息做判断，仅测试弹窗是否可正常点击
        """
        # 下拉刷新
        self.homepage.swipe_down()
        self.homepage.poco(text='立即查看').click()
        sleep(3)
        # 判断广告详情页是否存在
        assert_true(self.homepage.is_detail_page_exist())

    @allure.title('首页封面广告')
    @pytest.mark.parametrize('img_url', get_advertisement_img(region_id, 32))
    def test_cover_advertisement(self, img_url):
        """
        判断轮播图是否存在，且可以点击
        """
        # 获取首页-轮播图广告列表
        self.img_list = self.homepage.get_homepage_advertisement(self.region_id, 32)
        # 判断轮播图是否存在
        # self.homepage.is_img_exist(self.img_list, self.homepage.file_path)
        # self.homepage.click_cover_advertisement()
        self.homepage.refresh_page()
        self.homepage.image_wait_and_click(img_url, self.homepage.file_path)
        # 判断广告详情页是否存在
        assert_true(self.homepage.is_detail_page_exist())

    @allure.title('首页登荣广告')
    def test_deng_rong_advertisement(self):
        """
        判断登荣广告是否可以点击
        """
        # 获取首页-登荣广告列表
        self.img2_list = self.homepage.get_homepage_advertisement(self.region_id, 42)
        # 判断登荣广告是否存在
        assert_true(self.homepage.images_exist_and_click(self.img2_list, self.homepage.file_path))
        # 判断广告详情页是否存在
        assert_true(self.homepage.is_detail_page_exist())

    @allure.title('首页推荐广告')
    def test_recommend_list_advertisement(self):
        """
        判断推荐列表广告是否可以点击
        """
        # 获取首页-推荐广告列表
        self.recommend_dict = self.homepage.get_recommend_advertisement()
        # 切换县市
        self.homepage.region_switch(self.homepage.region_dict[self.recommend_dict['regionid']])
        sleep(2)
        self.homepage.swipe_homepage_to_the_top()
        # 判断推荐列表广告是否存在
        assert_true(self.homepage.images_wait_and_click(self.recommend_dict['img'], self.homepage.file_path, img_url=False))
        # 判断广告详情页是否存在
        assert_true(self.homepage.is_detail_page_exist())

    @allure.title('猜你喜欢广告')
    @pytest.mark.skip(reason='跳过')
    def test_guess_you_like_list_advertisement(self):
        """
        判断猜你喜欢列表广告是否可以点击,由于猜你喜欢每次请求的广告不一样，
        故不通过图像识别方式判断广告是否存在，改用该区域的广告是否存在，是否可点击
        """
        assert_true(self.homepage.is_guess_you_like_list_advertisement2())
        # 判断广告详情页是否存在
        assert_true(self.homepage.is_detail_page_exist())

    def teardown_method(self):
        self.homepage.go_back()
        self.homepage.region_switch(self.homepage.region_dict[self.region_id])


if __name__ == '__main__':
    pytest.main(['-sv', 'test_cases/test_home_page.py'])
