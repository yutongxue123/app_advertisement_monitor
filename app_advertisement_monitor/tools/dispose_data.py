# -*- coding:utf-8 -*-
import yaml,chardet
from commons.config import ENV, PROJECT_PATH


def get_yaml_data(yaml_file):
    with open(yaml_file, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        # print(data[ENV])
        return data[ENV]


def read_yaml_data(yaml_file):
    with open(yaml_file, 'r', encoding='unicode-escape') as f:
        # 检测文件编码
        # result = chardet.detect(f.read())
        # print(result['encoding'])
        # data = yaml.load(f, Loader=yaml.FullLoader)
        data = yaml.safe_load(f)
        return data


if __name__ == '__main__':
    # print('../test_data/advertisement_data.yaml')
    print(read_yaml_data('../test_data/advertisement_data.yaml'))
    # 打印读取的数据
    # print(loaded_data)
    # 解析unicode编码字符串
    # text = r'\u9996\u9801\u6A6B\u5E45'
    # text3 = '\\u9996\\u9801\\u6A6B\\u5E45'
    # decoded_text = bytes(text3, 'utf-8').decode('unicode_escape')
    # print(decoded_text)
    # text2 = '\\\\'
    # print(text2)

