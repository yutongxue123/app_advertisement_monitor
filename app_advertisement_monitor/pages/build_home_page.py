# -*- coding:utf-8 -*-
from pages.base_page import BaseBase
from commons.init import *
from commons.config import PROJECT_PATH, API_DEVICE_INFO


class NewBuildHomePage(BaseBase):
    """
        新建案首页
    """
    def __init__(self, poco):
        super().__init__(poco)
        self.file_path = PROJECT_PATH + '/page_img/newbuild_homepage_img/'
        self.case_img = self.common_img_path + 'tpl1701230363293.png'

    def click_new_build(self):
        """
        进入新建案首页,默认等待3s
        """
        if self.poco(text="新建案").exists():
            self.poco(text="新建案").wait().click()
            if self.poco_exist('新建案'):
                self.poco("新建案").click()
        else:
            self.poco("新建案").wait().click()

    def init_build_home_page(self):
        # 如果当前页面不是新建案首页,则返回新建案首页
        if self.poco(text="首頁").exists():
            self.swipe_homepage_to_the_top()
            # 进入新建案首页
            self.poco(text="新建案").wait().click()

    def swipe_to_the_top(self):
        """
        若当前首页不在顶部，则向上滑动至顶部
        """
        # while not self.img_exist(self.img_path + 'tpl1702621485230.png'):
        while not self.poco_exist('全部建案'):
            self.swipe_down()

    def swipe_down(self, duration=0.3):
        """
        向下滑动
        """
        swipe((0.9*w, 0.1*h), (0.9*w, h), duration=duration)

    def is_focus_right_advertisement(self, region_id, i, position_id):
        """
        判断新建案首页焦点右侧广告是否存在：
            1.右侧上方广告位
            2.右侧下方广告位
        """
        # 获取新建案首页右侧广告
        build_img_list = self.get_advertisement_img(region_id, position_id)
        # 判断右侧广告位在数据库中是否存在
        if build_img_list:
            # 判断右侧广告位是否存在,且可以点击,并进入广告详情页
            assert_true(self.images_exist_and_click(build_img_list, self.file_path, threshold=0.6, img_url=False))
            # 判断广告详情页是否存在
            assert_true(self.is_detail_page_exist())
        else:
            focus_img_list = self.get_build_focus_right_img(region_id)['topic']
            # -----------判断右侧广告位是否存在,且可以点击,并进入二级列表页-----------
            # 判断右侧广告位是否存在,且可以点击,并进入二级列表
            sleep(1)
            assert_true(self.image_exist_and_click(focus_img_list[i]['img'], self.file_path, threshold=0.6))
            sleep(1)
            # 判断二級列表是否存在
            assert_true(self.is_second_list_advertisement())

            # -------------判断二级列表的广告是否存在------------------
            case_list_img = self.get_case_list_img(region_id, focus_img_list[i]['type'])
            # 判断右侧广告位是否存在,且可以点击,并进入广告详情页
            assert_true(self.images_exist_and_click(case_list_img, self.file_path))
            # 判断广告详情页是否存在
            assert_true(self.is_detail_page_exist())
            sleep(1)
            # 退出广告详情页
            self.go_back()

    def is_second_list_advertisement(self):
        """
        判断二级列表页是否存在，并检查"咨询案场"按钮是否可点击
        """
        pos = self.exist(self.case_img)
        if pos:
            # 判断二级列表交互按钮是否正常
            touch(pos)
            assert_equal(self.poco_exist('請案場聯絡我'), True)
            # 點擊取消
            self.poco("取消").click()
            return True
        else:
            print('二級列表广告不存在')
            return False

    def get_build_cover_img(self, regionid):
        """
        新建案首页横幅广告
        """
        url = f'https://union.591.com.tw/advert?device=android&pid=41&regionid={regionid}'
        result = self.request('GET', url)
        img_list = []
        for advertisement in result['data']['76']:
            img_list.append(advertisement['img'])
        return img_list

    def get_build_focus_right_img(self, regionid):
        """
        新建案首页焦点右侧广告
        """
        url = f'https://bff.591.com.tw/v2/housing/ad/list?device=android&pid=41&regionid={regionid}'
        # txt = ['waist', 'topic', 'operation']
        txt = ['topic']
        result = self.request('GET', url)
        img_dict = {}
        for t in txt:
            if t in result['data']:
                for ad in result['data'][t]:
                    if 'img' in ad:
                        if 'type' in ad:
                            ad_list = [{'type': ad['type'], 'img': ad['img']}]
                        else:
                            ad_list = {'img': [ad['img']]}
                        if t not in img_dict:
                            img_dict[t] = ad_list
                        else:
                            if 'type' in ad:
                                img_dict[t].append({'type': ad['type'], 'img': ad['img']})
                            else:
                                img_dict[t]['img'].append(ad['img'])
                    elif 'sm_img' in ad:
                        if 'type' in ad:
                            ad_list = [{'type': ad['type'], 'img': ad['sm_img']}]
                        else:
                            ad_list = {'img': [ad['sm_img']]}
                        if t not in img_dict:
                            img_dict[t] = ad_list
                        else:
                            if 'type' in ad:
                                img_dict[t].append({'type': ad['type'], 'img': ad['sm_img']})
                            else:
                                img_dict[t]['img'].append(ad['img'])
        # formatted_result = json.dumps(img_dict, indent=4, ensure_ascii=False)
        # print(formatted_result)
        return img_dict

    def get_build_home_list_img(self, regionid):
        """
        新建案首页列表广告
        """
        payload = {
            "keywords": "",
            "searchtype": "1",
            "regionid": f"{regionid}",
            "p": 1,
        }
        payload.update(API_DEVICE_INFO)
        return self.get_build_list_img(payload)

    def get_build_home_interesting_img(self, regionid):
        """
        新建案首页列表感兴趣广告
        """
        payload = {
            "keywords": "",
            "searchtype": "1",
            "regionid": f"{regionid}",
            "p": 1,
        }
        payload.update(API_DEVICE_INFO)
        url = 'https://api.591.com.tw/api/housing/houseList'
        result = self.request('POST', url, json=payload)
        img_list = []
        for data in result['data']:
            if 'lovely' in data.keys():
                for img in data['lovely']['items']:
                    img_list.append(img['cover'])
        return img_list

    def get_case_list_img(self, regionid, id):
        """
        新建案二级列表广告,由于不确定APP请求的id参数，所以分别获取不同id的广告列表的前3笔图片
        """
        img_list = []
        url = f'https://bff.591.com.tw/v1/housing/ad/detail'
        payload = {
            "page": "1",
            "regionid": f"{regionid}",
            "type": "2",
            "id": id
        }
        payload.update(API_DEVICE_INFO)
        result = self.request('GET', url, params=payload)
        # formatted_result = json.dumps(result, indent=4, ensure_ascii=False)
        # print(formatted_result)
        for j in range(len(result['data']['items'])):
            if j > 2:
                break
            img_list.append(result['data']['items'][j]['cover'])
        return img_list


if __name__ == '__main__':
    build_homepage = NewBuildHomePage(poco)
    print(build_homepage.get_build_home_interesting_img(1))





