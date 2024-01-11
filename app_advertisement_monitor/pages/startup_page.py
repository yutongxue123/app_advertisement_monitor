from pages.base_page import BaseBase
from commons.config import PROJECT_PATH, API_DEVICE_INFO
from commons.init import *


class BuildSearchPage(BaseBase):
    """
    首页搜索
    """
    def __init__(self, poco):
        super().__init__(poco)
        self.file_path = PROJECT_PATH + '/page_img/build_search_page_img/'


if __name__ == '__main__':
    pass





