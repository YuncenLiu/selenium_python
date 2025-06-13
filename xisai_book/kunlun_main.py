# -*- coding: utf-8 -*-
import time

from selenium.webdriver.common.by import By

from xisai_book import xs_driver
from xisai import xs_login

if __name__ == '__main__':
    driver = xs_driver.getDriver()

    time.sleep(5)
    driver.get_screenshot_as_file("../pic/kunlun.png")
    time.sleep(5)

    # 关闭
    xs_driver.closeBrew(driver)
