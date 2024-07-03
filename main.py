# -*- coding: utf-8 -*-
# coding:utf8
# 访问百度 然后输入框输入 昆仑健康 再搜索
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':

    driver = webdriver.Chrome("driver/chromedriver.exe")
    driver.get("https://www.baidu.com")

    driver.find_element(By.CSS_SELECTOR,"#kw").send_keys("昆仑健康")
    driver.find_element(By.CSS_SELECTOR,"#su").click()


    time.sleep(2)
    driver.quit()