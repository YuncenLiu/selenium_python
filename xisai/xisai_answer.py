# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome("../driver/chromedriver")
driver.get("https://wangxiao.xisaiwang.com/ucenter2/login.html")

# 隐式等待 如果取元素的时候，如果找不到找不到整个元素，我最多等5秒，超过5秒就一场（推荐）
# 全局使用
driver.implicitly_wait(15)

# 找到包含 class="clearfix" 的 <ul> 元素
ul_element = driver.find_element(By.CSS_SELECTOR, ".ecv2_loginTabs .hd .clearfix")

# 找到该 <ul> 元素下的所有 <li> 元素
li_elements = ul_element.find_elements_by_tag_name("li")[2]
li_elements.click()

# 15279151605
# Abc123
account = "15279151605"
password = "Abc123"

driver.find_element(By.ID, "account").send_keys(account)

time.sleep(10)

driver.find_element(By.CSS_SELECTOR, ".xpc-menu-box").find_elements_by_tag_name("dl")[1].find_elements_by_tag_name(
    "dd")[2].click()
time.sleep(0.5)
driver.find_element(By.CSS_SELECTOR, ".xpc_tiku_tab .clearfix").find_elements_by_tag_name("li")[3].click()
time.sleep(0.5)
# 找到所有的 ti_item 元素
ti_items = driver.find_element(By.ID, "dataList").find_elements_by_css_selector(".ti_item > div")

# 遍历每个 ti_item 元素并打印文本内容
# for ti_item in ti_items:
#     item_text = ti_item.text.strip()
#     print("ti_item 文本内容:", item_text)

retest_links = driver.find_element(By.ID, "dataList").find_elements_by_xpath(
    './/a[contains(@class, "tiku-list-item-fr") and contains(text(), "测试报告")]')

test_links = driver.find_element(By.ID, "dataList").find_elements_by_xpath(
    './/a[contains(@class, "tiku-list-item-fr") and contains(text(), "重新做题")]')

# 遍历每个链接并打印其 href 属性
# for link in retest_links:
#     link_href = link.get_attribute('href')
#     print("测试报告链接:", link_href)

for item1, item2, item3 in zip(ti_items, retest_links, test_links):
    # print("标题：", item1.text.strip(), "测试报告：", item2.get_attribute('href'), "重新做题：", item3.get_attribute('href'))
    item3.click()

time.sleep(5)
driver.quit()
