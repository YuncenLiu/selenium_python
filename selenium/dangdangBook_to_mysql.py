# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql

conn = pymysql.connect(host='39.105.177.10',
                       port=3388,
                       user='cloud',
                       passwd='cloud',
                       database='cloud',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
print("mysql 连接成功！")

driver = webdriver.Chrome("../driver/chromedriver")
driver.get("https://bang.dangdang.com")
# 隐式等待 如果取元素的时候，如果找不到找不到整个元素，我最多等5秒，超过5秒就一场（推荐）
# 全局使用
driver.implicitly_wait(5)

key = driver.find_element(By.CSS_SELECTOR, "#form_search_new .gray")
key.send_keys("科幻")

search_btn = driver.find_element(By.CSS_SELECTOR, "#form_search_new .button")
search_btn.click()

try:
    time.sleep(0.5)
    for i in range(5):
        shopList = driver.find_elements(By.CSS_SELECTOR, "#search_nature_rg li")
        for li in shopList:
            bookTitle = li.find_element(By.CSS_SELECTOR, "a").get_attribute("title")
            bookPrice = li.find_element(By.CSS_SELECTOR, ".search_now_price").text
            print('书名：', bookTitle, ' 价格：', bookPrice)
            sql = "INSERT INTO cloud.selenium_dangdang_book (title, price) VALUES (%s, %s)"
            cursor.execute(sql, (bookTitle, bookPrice))

        next = driver.find_element(By.LINK_TEXT, "下一页")
        next.click()
        time.sleep(0.5)


    conn.commit()
finally:
    conn.close()

time.sleep(2)
driver.close()
