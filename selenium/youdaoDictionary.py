# -*- coding: utf-8 -*-

# https://fanyi.youdao.com/#/
# 打开浏览器 输入 "你好，世界" 拿出翻译内容
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("../driver/chromedriver")
driver.get("https://fanyi.youdao.com/#/")

time.sleep(1)

# 关闭提示按钮
close_btn = driver.find_element(By.CSS_SELECTOR,".inner-content .close")
close_btn.click()

time.sleep(1)

# 输入要翻译的内容
input = driver.find_element(By.ID, "js_fanyi_input")
input.send_keys("你好，世界，不得不说，爬虫是真的牛哈，可以做任何事情。")

time.sleep(1)

# 好像有延迟
outPut = driver.find_element(By.CSS_SELECTOR, "#js_fanyi_output")
print(outPut.text)

time.sleep(2)
driver.quit()