# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import platform

# 获取系统平台信息
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

system = platform.system()
driverPath = ""
# 根据平台找到对应源
if system == 'Darwin':
    driverPath = "../driver/chromedriver"
elif system == 'Windows':
    driverPath = "../driver/chromedriver.exe"


def openBrew():
    driver = webdriver.Chrome(driverPath)
    driver.get("https://wangxiao.xisaiwang.com/ucenter2/login.html")
    return driver


def doPach(driver):
    # 隐式等待 如果取元素的时候，如果找不到找不到整个元素，我最多等5秒，超过5秒就一场（推荐）
    # 全局使用
    driver.implicitly_wait(5)

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

    time.sleep(8)

    driver.find_element(By.CSS_SELECTOR, ".xpc-menu-box").find_elements_by_tag_name("dl")[1].find_elements_by_tag_name(
        "dd")[2].click()
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, ".xpc_tiku_tab .clearfix").find_elements_by_tag_name("li")[3].click()
    time.sleep(0.5)

    # 遍历每个链接并打印其 href 属性
    # for link in retest_links:
    #     link_href = link.get_attribute('href')
    #     print("测试报告链接:", link_href)

    for i in range(3):
        # 找到所有的 ti_item 元素
        ti_items = driver.find_element(By.ID, "dataList").find_elements_by_css_selector(".ti_item > div")

        retest_links = driver.find_element(By.ID, "dataList").find_elements_by_xpath(
            './/a[contains(@class, "tiku-list-item-fr") and contains(text(), "测试报告")]')

        test_links = driver.find_element(By.ID, "dataList").find_elements_by_xpath(
            './/a[contains(@class, "tiku-list-item-fr") and contains(text(), "重新做题")]')
        count = 0
        for item1, item2, item3 in zip(ti_items, retest_links, test_links):
            count = count + 1
            title = item1.text.strip()
            if item2 is None:
                print(count, " - 标题：", title, "为空，跳过")
                continue

            testReport = item2.get_attribute('href')
            doAgain = item2.get_attribute('href')

            print(count, " - 标题：",
                  title, "测试报告：",
                  testReport, "重新做题：",
                  doAgain)
            item2.click()
            all_handles = driver.window_handles

            # 切换到新窗口
            new_window_handle = None
            for handle in all_handles:
                if handle != driver.current_window_handle:
                    new_window_handle = handle
                    driver.switch_to.window(new_window_handle)

                    # 等待新窗口中的元素加载完成（假设需要等待 h3 元素加载完毕）
                    getAna = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='rep_new_Buts']/a"))
                    )
                    time.sleep(0.5)
                    getAna.click()
                    time.sleep(0.7)
                    getAnswer(driver)
                    driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # 临时关闭
            break
        if i != 2:
            nextBtn = driver.find_element(By.LINK_TEXT, "下一页")
            nextBtn.click()
            time.sleep(0.5)
        # 临时关闭
        break


# 获取题库
def getAnswer(driver):
    selectors = driver.find_element(By.CSS_SELECTOR, ".cbnWrap").find_elements_by_css_selector('span[data-stid]')
    ansCount = 0
    # 循环的每一个是每一道题目，如果有45道题，会循环 45次
    for sec in selectors:
        ansCount = ansCount + 1
        if ansCount != 9:
            continue

        sec.click()
        time.sleep(0.5)

        ansTitleEl = driver.find_element_by_class_name('single-content')
        # 题号 第9题（单选题）：
        titleNo = ansTitleEl.find_element_by_class_name('lh2').text.strip()

        p_elements = ansTitleEl.find_elements_by_css_selector('.singleR')
        ansTitleSet = set()
        if p_elements:
            for p in p_elements:
                ansTitleSet.add(p.text.strip() + "\n")

        div_elements = ansTitleEl.find_elements_by_css_selector('.singleR')
        if div_elements:
            for div in div_elements:
                ansTitleSet.add(div.text.strip() + "\n")
        # 题主体部分
        ansTitleStr = str(ansTitleSet)[1:-1]

        imgEl = driver.find_elements(By.CSS_SELECTOR, ".singleR img")
        imgList = [img.get_attribute("src") for img in imgEl]
        # 题目里的图片，按逗号分隔
        imgStr = ", ".join(imgList)

        print(titleNo, ansTitleStr, imgStr)

        # 这里处理选项
        chooseEl = driver.find_element_by_class_name('answerWrap')
        chooseList = chooseEl.find_elements_by_class_name('answerList')
        ansChCount = 0
        for ch in chooseList:
            ansChCount = ansChCount+1
            singleChList = ch.find_element_by_class_name('answerContent').find_elements_by_class_name('answerContentList')
            chList = []
            for singlech in singleChList:
                chooseStr = singlech.find_element(By.TAG_NAME, "label").text.strip()
                chList.insert(ansChCount,chooseStr)

            print('第',ansChCount,'题','选项分别是：',chList)
        # 这里处理答案

        answerEndEl = driver.find_element_by_class_name('answerEnd')
        daanList = answerEndEl.find_elements_by_class_name('daan_sty')

        for daan in daanList:
            answer_elements = daan.find_elements(By.CLASS_NAME, "p1")
            for answer_element in answer_elements:
                answer_type = answer_element.find_element(By.TAG_NAME, "span").text
                answer_text = answer_element.find_element(By.TAG_NAME, "span:nth-child(2)").text
                print(f"{answer_type}: {answer_text}")

        # 这里获取解析与类型



def closeBrew(driver):
    time.sleep(5)
    driver.quit()


driver = openBrew()
doPach(driver)
closeBrew(driver)
