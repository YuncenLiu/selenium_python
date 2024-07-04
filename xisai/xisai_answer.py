# -*- coding: utf-8 -*-
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
import platform
import pymysql

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

            p_type = ""
            if "案例" in title:
                p_type = "案例"
            elif "论文" in title:
                p_type = "论文"
            else:
                p_type = "综合"

            insert_s_paper_sql = "insert into s_paper(p_type,p_title,p_report_url,p_do_url) value (%s,%s, %s,%s)"
            insert_s_paper_data = (p_type, title, testReport, doAgain)
            s_paper_id = insertDb(insert_s_paper_sql, insert_s_paper_data)
            print("插入成功，s_paper 主键为:", s_paper_id)

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
                    getAnswer(s_paper_id, driver)
                    driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # 临时关闭
            # break
        if i != 2:
            nextBtn = driver.find_element(By.LINK_TEXT, "下一页")
            nextBtn.click()
            time.sleep(0.5)
        # 临时关闭
        # break


# 获取题库
def getAnswer(s_paper_id, driver):
    selectors = driver.find_element(By.CSS_SELECTOR, ".cbnWrap").find_elements_by_css_selector('span[data-stid]')
    ansCount = 0
    # 循环的每一个是每一道题目，如果有45道题，会循环 45次
    for sec in selectors:
        ansCount = ansCount + 1

        # 临时 使用40题作为案例分析
        # if ansCount != 40:
        #     continue

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


        insert_s_subject_sql = "insert into s_subject(paper_id,sub_no,sub_title) value (%s,%s,%s)"

        titleNo = titleNo[0:-1]
        ansTitleStr = ansTitleStr[1:-1]
        insert_s_subject_data = (s_paper_id, titleNo, ansTitleStr)
        sub_id = insertDb(insert_s_subject_sql, insert_s_subject_data)

        imgEl = driver.find_elements(By.CSS_SELECTOR, ".singleR img")
        imgList = [img.get_attribute("src") for img in imgEl]
        if len(imgList) > 0:

            for img in imgList:
                insert_s_pic_sql = "insert into s_pic(pic_url) value (%s)"
                insert_s_pic_data = (img)
                pic_id = insertDb(insert_s_pic_sql, insert_s_pic_data)

                insert_s_sub_pic_sql = "insert into s_sub_pic(sub_id,pic_id) value (%s,%s)"
                insert_s_sub_pic_data = (sub_id, pic_id)
                insertDb(insert_s_sub_pic_sql, insert_s_sub_pic_data)

        # 题目里的图片，按逗号分隔
        imgStr = ", ".join(imgList)

        print('题目：', titleNo, ansTitleStr, imgStr)

        # 这里处理选项
        chooseEl = driver.find_element_by_class_name('answerWrap')
        chooseList = chooseEl.find_elements_by_class_name('answerList')
        ansChCount = 0

        insert_choose_list = []
        for ch in chooseList:
            ansChCount = ansChCount + 1
            singleChList = ch.find_element_by_class_name('answerContent').find_elements_by_class_name(
                'answerContentList')
            chList = []
            for singlech in singleChList:
                chooseStr = singlech.find_element(By.TAG_NAME, "label").text.strip()
                chList.insert(ansChCount, chooseStr)

            print('第', ansChCount, '题', '选项分别是：', chList)
            insert_choose_list.insert(ansChCount, chList)

        # 这里处理答案

        answerEndEl = driver.find_element_by_class_name('answerEnd')
        daanList = answerEndEl.find_elements_by_class_name('daan_sty')

        daanCount = 0
        for daan in daanList:
            daanCount = daanCount + 1
            answer_elements = daan.find_elements(By.CLASS_NAME, "p1")

            daanTrue = ""
            daanMy = ""
            for answer_element in answer_elements:
                answer_type = answer_element.find_element(By.TAG_NAME, "span").text
                answer_text = answer_element.find_element(By.TAG_NAME, "span:nth-child(2)").text
                if answer_type == '正确答案':
                    daanTrue = answer_text
                if answer_type == '我的答案':
                    daanMy = answer_text

            print('第', daanCount, '题：正确答案是：', daanTrue, '，我的答案是：', daanMy)
            chList = insert_choose_list[daanCount - 1]
            insert_s_choose_sql = "insert into s_choose(sub_id,ch_a,ch_b,ch_c,ch_d,ch_true,ch_my) value (%s,%s,%s,%s,%s,%s,%s)"
            insert_s_choose_data = (sub_id, chList[0], chList[1], chList[2], chList[3], daanTrue, daanMy)
            ch_id = insertDb(insert_s_choose_sql, insert_s_choose_data)

            insert_s_sub_ch_sql = "insert into s_sub_ch(sub_id,ch_id) value (%s,%s)"
            insert_s_sub_ch_data = (sub_id, ch_id)
            insertDb(insert_s_sub_ch_sql, insert_s_sub_ch_data)

        # 这里获取解析与类型
        shitiDespEl = driver.find_element_by_class_name('shitiDesp')
        # 解析所有答案图片
        daanImgs = shitiDespEl.find_elements(By.CSS_SELECTOR, "img")
        daanImgList = [img.get_attribute("src") for img in daanImgs]

        if len(daanImgList) > 0:
            for img in daanImgList:
                insert_s_pic_sql = "insert into s_pic(pic_url) value (%s)"
                insert_s_pic_data = (img)
                pic_id = insertDb(insert_s_pic_sql, insert_s_pic_data)

                insert_s_sub_pic_sql = "insert into s_sub_ref_pic(sub_id,pic_id) value (%s,%s)"
                insert_s_sub_pic_data = (sub_id, pic_id)
                insertDb(insert_s_sub_pic_sql, insert_s_sub_pic_data)

        # 题目里的图片，按逗号分隔
        daanImg = ", ".join(daanImgList)

        jiexinewList = shitiDespEl.find_elements_by_class_name('jiexinew')
        spanDictList = []
        spanDictListCount = 0
        for jiexin in jiexinewList:
            spanDictListCount = spanDictListCount + 1
            spansL = jiexin.find_elements(By.XPATH, ".//span")
            spanDict = {}
            spanCount = 0

            spanKey = ""
            spanValue = ""
            for span in spansL:
                spanCount = spanCount + 1
                if spanCount % 2 == 0:
                    spanValue = span.text.strip()
                else:
                    spanKey = span.text.strip()
            spanDict[spanKey] = spanValue
            spanDictList.insert(spanDictListCount, spanDict)
        sub_tag = ""
        sub_info = ""
        sub_ref = ""
        for dict in spanDictList:
            for k, v in dict.items():
                if "所属知识点：" == k:
                    sub_tag = v
                elif "试题难度：" == k:
                    sub_info = v
                elif "参考解析1：" == k:
                    sub_ref = v

        sub_tag = sub_tag[0:-1]
        update_s_subject_sql = "update s_subject set sub_tag = %s , sub_info = %s , sub_ref = %s where id = %s"
        update_s_subject_data = (sub_tag, sub_info, sub_ref, sub_id)
        insertDb(update_s_subject_sql, update_s_subject_data)

        # 输出所有解析
        print(spanDictList)
        # 打印所有图片
        print(daanImg)



def closeBrew(driver):
    time.sleep(5)
    driver.quit()


def insertDb(insert_query, data):
    conn = pymysql.connect(host='39.105.177.10',
                           port=3388,
                           user='cloud',
                           passwd='cloud',
                           database='cloud',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    # 插入数据的 SQL 查询
    # insert_query = "INSERT INTO s_paper (p_type, p_title) VALUES (%s, %s)"
    # 数据值
    # data = ("综合题", "2024年05月系分公共基础测试卷 测试报告")
    # 执行插入操作
    cursor.execute(insert_query, data)
    # 提交事务
    conn.commit()
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    return cursor.lastrowid


def executeDb(insert_query):
    conn = pymysql.connect(host='39.105.177.10',
                           port=3388,
                           user='cloud',
                           passwd='cloud',
                           database='cloud',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    # 插入数据的 SQL 查询
    # insert_query = "INSERT INTO s_paper (p_type, p_title) VALUES (%s, %s)"
    # 数据值
    # data = ("综合题", "2024年05月系分公共基础测试卷 测试报告")
    # 执行插入操作
    cursor.execute(insert_query)
    # 提交事务
    conn.commit()
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()
    return cursor.lastrowid


# 初始化所有表
def initDb():
    drop_sql = """DROP TABLE IF EXISTS s_paper;
                CREATE TABLE s_paper (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    p_type VARCHAR(100) NOT NULL,
                    p_title VARCHAR(100) NOT NULL,
                    p_report_url VARCHAR(200),
                    p_do_url VARCHAR(200)
                );
                DROP TABLE IF EXISTS s_subject;
                CREATE TABLE s_subject (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    paper_id INT NOT NULL,
                    sub_no VARCHAR(100),
                    sub_title VARCHAR(2000),
                    choose_id INT,
                    sub_tag VARCHAR(100),
                    sub_info VARCHAR(100),
                    sub_ref VARCHAR(2000)
                );
                DROP TABLE IF EXISTS s_pic;
                CREATE TABLE s_pic (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    pic_url VARCHAR(500) NOT NULL
                );
                DROP TABLE IF EXISTS s_sub_pic;
                CREATE TABLE s_sub_pic (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sub_id INT NOT NULL,
                    pic_id INT NOT NULL
                );
                DROP TABLE IF EXISTS s_sub_ref_pic;
                CREATE TABLE s_sub_ref_pic (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sub_id INT NOT NULL,
                    pic_id INT NOT NULL
                );
                DROP TABLE IF EXISTS s_choose;
                CREATE TABLE s_choose (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sub_id INT,
                    ch_a VARCHAR(500) NOT NULL,
                    ch_b VARCHAR(500) NOT NULL,
                    ch_c VARCHAR(500) NOT NULL,
                    ch_d VARCHAR(500) NOT NULL,
                    ch_true VARCHAR(10) NOT NULL,
                    ch_my VARCHAR(10)
                );
                DROP TABLE IF EXISTS s_sub_ch;
                CREATE TABLE s_sub_ch (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sub_id INT NOT NULL,
                    ch_id INT NOT NULL
                );

    """
    executeDb(drop_sql)


driver = openBrew()
try:
    # initDb()
    doPach(driver)
except:
    print('程序执行异常！')
    traceback.print_exc()
finally:
    closeBrew(driver)
print('程序执行完成！')
