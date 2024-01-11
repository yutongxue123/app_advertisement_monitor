import shutil

import pytest, os, subprocess
from commons.config import PROJECT_PATH
from tools.get_advertisement_data import GetAdvertisementData
from airtest.report.report import simple_report


if __name__ == '__main__':
    GetAdvertisementData().write_yaml()
    # 筛选需要执行的用例
    pytest.main(['-sv',
                 'test_cases',
                 # 'test_cases/test_home_page.py',
                 # 'test_cases/test_home_search_page.py',
                 # 'test_cases/test_build_home_page.py',
                 # 'test_cases/test_build_search_page.py',
                 # 'test_cases/test_build_list_page.py',
                # 'test_cases/test_build_detail_page.py',
                 '--alluredir=./reports/allure-results',
                 '--clean-alluredir',
                 # '--reruns=1',
                 # '--reruns-delay=2'
                 ])
    # simple_report(__file__, logpath=True, output=r'reports/log1/report1.html')
    # 执行命令，生成测试报告
    shutil.copy('./reports/environment.properties', './reports/allure-results/environment.properties')
    # os.system('cp ./reports/environment.properties' './reports/allure-results/environment.properties')
    os.system('allure generate ./reports/allure-results -o ./reports/allure-report --clean')
    os.system('allure open reports/allure-report')
    # os.system('allure serve ./reports/allure-results')
    # addopts = -n
    # 1 - -dist = each - -tx
    # 2 * popen // interval = 5

