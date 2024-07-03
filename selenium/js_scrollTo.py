# -*- coding: utf-8 -*-
import time

from selenium import webdriver

driver = webdriver.Chrome("../driver/chromedriver")
driver.get("https://2heng.xin")

driver.implicitly_wait(5)

js = "window.scrollTo(0,10000)"
driver.execute_script(js)


time.sleep(5)
driver.quit()