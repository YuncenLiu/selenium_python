import time

from selenium.webdriver.common.by import By

from xisai_book import xs_driver
from xisai import xs_login

if __name__ == '__main__':
    driver = xs_driver.getDriver()
    xs_login.login(driver)

    file_path = "doc/book1.txt"

    chapterList = driver.find_elements(By.CSS_SELECTOR,'#accordion > div')
    with open(file_path, 'a+') as file:
        for chapter in chapterList:
            chEl = chapter.find_element(By.TAG_NAME, 'h4').find_element(By.TAG_NAME, 'a')

            for line in chEl.text.split():
                file.write(line)

            print(chEl.text.split())
            chEl.click()
            descChList = chapter.find_element(By.CSS_SELECTOR, '.ul-listStyle-none').find_elements(By.TAG_NAME, 'li')
            for dc in descChList:
                dcEl = dc.find_element(By.CSS_SELECTOR, 'a')

                for line in dcEl.text.strip():
                    file.write(line)

                print(dcEl.text.strip())
                dcEl.click()
                contextList = driver.find_elements(By.CSS_SELECTOR, '.detail > p')
                for con in contextList:

                    for line in con.text.strip():
                        file.write(line)

                    print(con.text.strip())
                    imgs = con.find_elements(By.TAG_NAME, 'img')
                    for imgEl in imgs:

                        for line in imgEl.get_attribute('src'):
                            file.write(line)

                        print(imgEl.get_attribute('src'))
                # 点击返回
                driver.find_element(By.CSS_SELECTOR, '#qqonline').click()

    time.sleep(5)
    # 关闭
    xs_driver.closeBrew(driver)
