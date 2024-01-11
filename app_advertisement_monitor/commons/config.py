import os
# ENV = "TEST"
ENV = "PROD"
projectName = 'app_advertisement_monitor'
PROJECT_PATH = os.path.abspath(__file__).split(projectName)[0] + projectName
API_DEVICE_INFO = {
        "device": "android",
        "version": "6.6.1.319",
        "mobile_id": "8ac9ec99-7f88-4e40-8988-ee6425f9eefd",
        "device_id": "8ac9ec99-7f88-4e40-8988-ee6425f9eefd",
        "deviceid": "8ac9ec99-7f88-4e40-8988-ee6425f9eefd",
    }

# print(PROJECT_PATH)
# print(os.getcwd())
# print(os.path.abspath(__file__))
# print(os.path.realpath(__file__))
# print(__file__)
