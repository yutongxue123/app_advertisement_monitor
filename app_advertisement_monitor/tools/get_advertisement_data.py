# -*- coding:utf-8 -*-
from tools.connect_mysql import ConnectDatabase
import yaml
from tools.dispose_data import get_yaml_data
from commons.file_operations import del_file
from commons.config import PROJECT_PATH


class GetAdvertisementData:
    """
    从数据库获取广告位数据
    """
    sql = """
    select po.id,po.name,img, url, regionid  from t591_new.`union_position` po inner join t591_new.union_advert ad on po.id = ad.position_id inner join t591_new.`union_advert_region` re on ad.id = re.advert_id inner join t591_new.union_advert_detail de on ad.id = de.advert_id where po.id in (32,42,44,91,94)  and unix_timestamp() between ad.start_time and ad.end_time and ad.category = 2 and ad.platform = 4 and ad.close = 0 order by po.id asc, regionid asc;
    """

    def __init__(self):
        # 1.连接tw591数据库
        user_info = get_yaml_data(PROJECT_PATH + '/test_data/database_data.yaml')
        # print(user_info)
        self.tw591 = ConnectDatabase(user_info['username'], user_info['password'], connect_database_name=user_info["connect_database_tw591"])
        # 删除已下载的广告图片
        del_file(PROJECT_PATH + '/page_img')

    def query_advertisement(self, sql):
        # 2.查询广告位信息
        self.tw591.select("""set names utf8;""")
        content = self.tw591.select(sql)
        advertising_list = []
        for x in content:
            advertising = {}
            advertising['id'] = x[0]
            advertising['name'] = x[1]
            advertising['img'] = x[2]
            advertising['url'] = x[3]
            advertising['regionid'] = x[4]
            advertising_list.append(advertising)
        return advertising_list

    def dispose_advertising(self):
        all_advertising = []
        for x in self.query_advertisement(self.sql):
            pos_obj = {}
            pos_obj['id'] = x['id']     # 广告位id
            pos_obj['name'] = x['name']     # 广告位名称
            # name = x['name'].replace('\\', '\\\\')
            # pos_obj['name'] = name  # 广告位名称
            pos_obj['name'] = x['name'].encode('unicode_escape').decode()  # 广告位名称
            # print(pos_obj['name'])
            pos_obj['info'] = []        # 广告信息
            if len(all_advertising) == 0:
                pos_obj['info'].append({'regionid': x['regionid'], 'img': [{'img': x['img'], 'url': x['url']}]})
                all_advertising.append(pos_obj)
            else:
                for y in range(len(all_advertising)):
                    if pos_obj['id'] == all_advertising[y]['id']:
                        for z in range(len(all_advertising[y]['info'])):
                            if x['regionid'] == all_advertising[y]['info'][z]['regionid']:
                                all_advertising[y]['info'][z]['img'].append({'img': x['img'], 'url': x['url']})
                                break
                            elif z == len(all_advertising[y]['info']) - 1:
                                all_advertising[y]['info'].append({'regionid': x['regionid'], 'img': [{'img': x['img'], 'url': x['url']}]})
                    else:
                        if y == len(all_advertising) - 1:
                            pos_obj['info'].append({'regionid': x['regionid'], 'img': [{'img': x['img'], 'url': x['url']}]})
                            all_advertising.append(pos_obj)
    # for i in all_advertising:
    #     sum = 0
    #     for j in i['info']:
    #         sum += len(j['img'])
    #         print('县市：', j['regionid'], j['img'], len(j['img']))
    #     print('广告位id：', i['id'], '广告总数：', sum)
    #     print(all_advertising)
        return all_advertising

    def write_yaml(self):
        # print(self.dispose_advertising(), type(self.dispose_advertising()))
        with open(PROJECT_PATH + '/test_data/advertisement_data.yaml', 'w', encoding='utf-8') as f:
            # 将yaml数据写入到yaml_data.yaml文件中
            yaml.dump(self.dispose_advertising(), f)

    def get_region(self):
        region_dict = {}
        self.tw591.select("""select id, name from t591.area_region;""")
        region = self.tw591.select("""select id, name from t591.area_region;""")
        # print(region)
        for x in region:
            region_dict[x[0]] = x[1]
        # print(region_dict)


if __name__ == '__main__':
    GetAdvertisementData().write_yaml()
    # GetAdvertisementData().get_region()




