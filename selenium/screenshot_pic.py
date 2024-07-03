# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

driver = webdriver.Chrome("../driver/chromedriver")
driver.get("https://www.baidu.com")

driver.implicitly_wait(5)
# 图片最大化
driver.maximize_window()
more = driver.find_element(By.LINK_TEXT, "更多")
# 链式操作
ActionChains(driver).move_to_element(more).perform()

# 截图
driver.get_screenshot_as_file("../pic/demo.png")


time.sleep(5)
driver.quit()