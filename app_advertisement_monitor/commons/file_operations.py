# -*- coding:utf-8 -*-
import requests,os,re
from commons.config import PROJECT_PATH
import shutil
from PIL import Image
from urllib.parse import urlparse


def download_img(file_path, url):
    # 如果文件目录不存在，则创建目录
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # 拼接文件名（包含路径）
    if 'https://hp3.591.com.tw/banner/' in url:
        file_path = file_path + ''.join(url.split('/')[-2:])
    else:
        file_path = file_path + ''.join(url.split('/')[-1:])
    # 判断文件是否存在，如果不存在则下载
    if not os.path.exists(file_path):
        # 打开文件，并下载文件
        with open(file_path, 'wb') as f:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
            # print('url:',url)
            img = requests.get(url, verify=False, headers=headers).content
            # print(img)
            f.write(img)
            f.close()
        # 返回文件路径
    if file_path.split('.')[-1] == 'gif':
        file_gif = file_path
        # 加载gif图片
        image = Image.open(file_path)
        # 将gif图片转换为jpg图片,在保存时，我们可以选择调整JPG图像的质量。质量值范围为1到95，较高的值表示更好的质量。
        first_image = image.convert('RGB')
        file_path = file_path.split('.')[0] + '.jpg'
        first_image.save(file_path.split('.')[0] + '.jpg', quality=90)
        image.close()
        os.remove(file_gif)
    # print(file_path)
    return file_path


def del_files(file_path):
    """
    删除指定目录下的所有文件和文件夹
    """
    dirList = os.listdir(file_path)
    for f in dirList:
        if f.split('.')[-1] == 'jpg':
            os.remove(f) if os.path.isfile(f) else shutil.rmtree(f)


def del_file(file_path):
    """
    获取指定目录下（包括子目录）的所有文件，并删除指定后缀的文件
    """
    file_list = []
    for root, dirs, files in os.walk(file_path):
        # print(root, dirs, files)
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    for f in file_list:
        if f.split('.')[-1] in ['jpg', 'gif']:
            os.remove(f)


# def get_img_url(file_path, url):
#     """
#     通过模拟前端请求接口获取新建案id的图片url。并下载建案id的封面图
#     """
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
#     resp = requests.get(url, verify=False, headers=headers)
#     if resp.status_code == 200:
#         # 使用正则表达式获取图片的url
#         print(resp.text)
#         pattern = r'<img data-src="(.*?)160x120.jpg" alt="封面圖"'
#         matches = re.findall(pattern, resp.text)[0]
#         # print('匹配的字符：', matches)
#         # 判断是否是完整的url
#         # parsed_url = urlparse(matches)
#         # if parsed_url.scheme and parsed_url.netloc:
#         #     url = parsed_url.geturl()
#         #     print('打印：', url)
#         # pattern2 = r'<img data-src="(.*?)'
#         # matches2 = re.findall(pattern2, matches)
#         # print('匹配的字符2：', matches2)
#         return download_img(file_path, matches)
#     else:
#         print('请求失败')
#         print('详情状态码：', resp.status_code)


def get_small_img(file_path, url):
    """
    通过接口获取新建案id的图片url。并下载建案id的封面图
    """
    # 获取建案id
    id = url.split('/')[-1]
    url = f'https://ms-housing.591.com.tw/v1/housing/picture?id={id}&device=android'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    resp = requests.get(url, verify=False, headers=headers)
    if resp.status_code == 200:
        result = resp.json()['data']['logo']
        # print(result)
        if result[0]['small_img'] != '':
            img_url = result[0]['small_img']
        else:
            img_url = result[0]['big_img']
        # img_url = result[0]['img_url']
        # # img_url = result[0]['src_img']
        return download_img(file_path, img_url)
    else:
        print('请求失败')
        print('详情状态码：', resp.status_code)


if __name__ == '__main__':
    # print(download_img(PROJECT_PATH + '/page_img/homepage_img/', 'https://img2.591.com.tw/house/2023/06/21/168731241187534507.jpg!660x495.water3.jpg'))
    # # del_file(PROJECT_PATH + '/page_img')
    get_small_img(PROJECT_PATH + '/page_img/homepage_img/', 'https://newhouse.591.com.tw/132984')
    # get_img_url('https://newhouse.591.com.tw/130506')

