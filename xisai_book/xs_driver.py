# 获取当前服务环境 Mac、Windows
import platform
import time
from datetime import datetime

# 获取 selenium 对象
from selenium import webdriver

system = platform.system()

studyBookUrl = "https://wangxiao.xisaiwang.com/ucenter2/ebook/130/zt210068.html"
studyBook2Url = "https://wangxiao.xisaiwang.com/ucenter2/ebook/130/zt210184.html"
studyBook3Url = "https://wangxiao.xisaiwang.com/ucenter2/ebook/130/zt250010084.html"
studyBook4Url = "https://wangxiao.xisaiwang.com/ucenter2/ebook/130/zt250010090.html"

MacDriverIndex = "Darwin"
MacDriverFile = "../driver/chromedriver"

WindowsDriverIndex = "Windows"
WindowsDriverFile = "../driver/chromedriver.exe"


# 判断当前环境是 Windows 环境 还是 Mac 环境 返回谷歌插件地址
def getEnv():
    driverPath = ""
    if system == MacDriverIndex:
        driverPath = MacDriverFile
    elif system == WindowsDriverIndex:
        driverPath = WindowsDriverFile
    return driverPath


# 获取 Selenium 的 driver 对象并返回
def getDriver():
    driverPath = getEnv()
    driver = webdriver.Chrome(driverPath)
    driver.get(studyBook4Url)
    return driver


# 关闭 driver 服务
def closeBrew(driver):
    time.sleep(5)
    print('时间：', getTime(), ' 当前任务结束')
    driver.quit()


def getTime():
    # 获取当前时间戳
    current_timestamp = datetime.now().timestamp()
    # 将时间戳转换为日期字符串
    return datetime.fromtimestamp(current_timestamp).strftime('%Y-%m-%d')
