# -*- coding: utf-8 -*-
import time

from selenium.webdriver.common.by import By

from xisai_book import xs_driver
from xisai import xs_login

if __name__ == '__main__':
    driver = xs_driver.getDriver()
    xs_login.login(driver)


    chapterList = driver.find_elements(By.CSS_SELECTOR,'#accordion > div')
    for chapter in chapterList:
        chEl = chapter.find_element(By.TAG_NAME, 'h4').find_element(By.TAG_NAME, 'a')
        print(chEl.text.split())
        chEl.click()
        time.sleep(0.5)
        descChList = chapter.find_element(By.CSS_SELECTOR, '.ul-listStyle-none').find_elements(By.TAG_NAME, 'li')
        for dc in descChList:
            dcEl = dc.find_element(By.CSS_SELECTOR, 'a')

            print(dcEl.text.strip())
            dcEl.click()
            time.sleep(0.5)
            context = driver.find_element(By.CSS_SELECTOR, '.detail')
            print(context.text.strip())

            imgs = context.find_elements(By.TAG_NAME, 'img')
            for imgEl in imgs:
                print(imgEl.get_attribute('src'))

            # 点击返回
            driver.find_element(By.CSS_SELECTOR, '#qqonline').click()
            time.sleep(0.5)

    time.sleep(5)
    # 关闭
    xs_driver.closeBrew(driver)
