import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from . import subject_zjlx
from . import connDB
from . import sql
import xs_main

# 章节练习一共三页
selectPage = 3
paperReportUrlStr = '测试报告'
paperDoUrlStr = '重新做题'
paperDoStartUrlStr = '开始做题'
paperDoAgainUrlStr = '继续做题'

subjectTypeZH = '综合'
subjectTypeAL = '案例'
subjectTypeLW = '论文'

def selectSubject(driver, index):
    time.sleep(0.5)
    # 点击开始做题
    driver.find_element(By.CSS_SELECTOR, ".xpc-menu-box").find_elements_by_tag_name("dl")[1].find_elements_by_tag_name(
        "dd")[2].click()
    # 对应做题
    driver.find_element(By.CSS_SELECTOR, ".xpc_tiku_tab .clearfix").find_elements_by_tag_name("li")[index].click()

    time.sleep(0.5)

    if 0 == index:
        zjlxSubject(driver, index)
    if 3 == index:
        zjlxSubject(driver, index)



# 章节练习
def zjlxSubject(driver, index):
    # 循环一次 点击下一页

    for i in range(selectPage):

        subjectPageEl = driver.find_element(By.CSS_SELECTOR, '.xpc_tiku_allcontent').find_element(By.ID, "dataList")
        # 试卷标题
        paperTitleList = subjectPageEl.find_elements(By.TAG_NAME, 'tr')

        # 获取 [测试报告] 连接
        # paperReportUrlList = subjectPageEl.find_element(By.ID, "dataList").find_elements_by_xpath(
        #     './/a[contains(@class, "tiku-list-item-fr") and contains(text(), "测试报告")]')
        # 获取 [重新做题] 连接
        # paperDoUrlList = subjectPageEl.find_element(By.ID, "dataList").find_elements_by_xpath(
        #     './/a[contains(@class, "tiku-list-item-fr") and contains(text(), "重新做题")]')

        for pageEl in paperTitleList:
            # 获取测试标题
            paperTitle = pageEl.find_element_by_css_selector(".ti_item > div").text.strip()
            # 获取最右侧两个按钮超链接
            pageUrlEls = pageEl.find_elements_by_tag_name("td")[3].find_elements(By.TAG_NAME, 'a')

            paperReportUrl = ''
            paperDoUrl = ''

            for pageAnyUrl in pageUrlEls:

                url = pageAnyUrl.get_attribute('href')
                urlName = pageAnyUrl.text.strip()

                againOrStartUrl = pageAnyUrl.get_attribute('onclick')

                # url 如果为 javascript:void(0); 则标识为空
                print(urlName, url, againOrStartUrl)

                if urlName == paperReportUrlStr:
                    paperReportUrl = url
                elif urlName == paperDoUrlStr:
                    paperDoUrl = url

                if urlName == paperDoAgainUrlStr or urlName == paperDoStartUrlStr:
                    paperDoUrl = url


            # 根据标题判断试卷类型
            paperType = ''
            if subjectTypeAL in paperTitle:
                # 案例题型
                paperType = subjectTypeAL
            elif subjectTypeLW in paperTitle:
                # 论文提醒
                paperType = subjectTypeLW
            else:
                # 综合提醒（选择题）
                paperType = subjectTypeZH

            # 这里可以做数据插入动作
            insert_s_paper_data = (paperTitle, paperType, paperReportUrl, paperDoUrl)
            paperId = connDB.executeSQLParams(sql.insert_s_paper_sql, insert_s_paper_data)

            print('试卷主键：', paperId, '试卷标题：', paperTitle, '试卷类型：', paperType, '测试报告：', paperReportUrl,
                  '重新做题：', paperDoUrl)

            if index == 3:
                # 如果为章节练习，只获取测试报告
                if paperReportUrl is None:
                    print('这套试卷没有做过，暂不支持进一步爬取')
                    continue
            if index == 0:
                if paperDoUrl is None:
                    print('这套试卷没有做过，暂不支持进一步爬取')
                    continue


            # ---------------------------------------------------
            # 1、进一步解析题目
            # ---------------------------------------------------
            subjectDo(driver, pageUrlEls, paperId, paperType, index)

            if xs_main.env == 'Test':
                break

        if xs_main.env == 'Test':
            break
        if i != selectPage - 1:
            nextBtn = driver.find_element(By.LINK_TEXT, "下一页")
            nextBtn.click()
            time.sleep(0.5)


# driver 全局对象用于跳转
# pageUrlEls 用于找到对应跳转按钮
def subjectDo(driver, pageUrlEls, paperId, paperType ,index):
    # 将每一题的右侧按钮传递过来， 并点击重新做题
    openFlag = True
    for pageAnyUrl in pageUrlEls:
        urlName = pageAnyUrl.text.strip()
        if urlName == paperReportUrlStr:
            openFlag = False
            # 如果是 重新做题按钮，点击跳转
            pageAnyUrl.click()
            # 点击后，立即跳跃
            break

    if openFlag:
        # 如果没有找到重新做题按钮，没有跳转，则直接返回
        return

    # 获取所有页面
    # 这里的 driver 对象必须是全局 driver 对象！
    all_handles = driver.window_handles
    # 　切换到新页面中
    new_window_handle = None
    for handle in all_handles:
        if handle != driver.current_window_handle:
            new_window_handle = handle
            driver.switch_to.window(new_window_handle)

            # 找到查看解析按钮， 最长等待 5 秒
            getAna = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='rep_new_Buts']/a"))
            )

            getAna.click()

            # ---------------------------------------------------
            # 2、进一步解析具体选择题
            # ---------------------------------------------------
            if paperType == subjectTypeZH:
                subject_zjlx.getZhSubject(driver, paperId)
            elif paperType == subjectTypeAL:
                print('当前类型不支持：', paperType)
            elif paperType == subjectTypeLW:
                print('当前类型不支持：', paperType)
            # 关闭此页面
            driver.close()
    # 跳转到首页 - 拿回 driver 对象
    driver.switch_to.window(driver.window_handles[0])

