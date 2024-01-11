# -*- coding:utf-8 -*-
from tools.dispose_data import read_yaml_data
from commons.config import PROJECT_PATH, ENV
from yaml import load, Loader


def get_advertisement_img(regionid, advertisement_position_id):
    """
    获取广告图片
    :return: 广告url列表
    """
    img_list = []
    advertisement_dict = read_yaml_data(PROJECT_PATH + '/test_data/advertisement_data.yaml')
    for advertisement in advertisement_dict:
        if advertisement['id'] == advertisement_position_id:
            for info in advertisement['info']:
                if info['regionid'] == regionid:
                    for img in info['img']:
                        if img['img'] is not None:
                            img_list.append(img['img'])
                        else:
                            img_list.append(img['url'])
    return img_list


def get_test_data(casename):
    casename = casename.split('.py')[0].replace('\\', '/').split('/')[-1]
    testdata = load(open(PROJECT_PATH + '/test_data/' + casename + '.yaml', encoding='utf-8').read(), Loader=Loader)
    testdata = testdata.get(ENV)
    return testdata.get(casename)


if __name__ == '__main__':
    print(get_advertisement_img(1, 91))
