import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from . import subject_zjlx, subject_mryl
from . import connDB
from . import sql
import xs_main
import xs_driver

# 章节练习一共三页
selectPage = 3
selectDayPage = 100

paperReportUrlStr = '测试报告'
paperDoUrlStr = '重新做题'
paperDoStartUrlStr = '开始做题'
paperDoAgainUrlStr = '继续做题'

subjectTypeZH = '综合'
subjectTypeDAY = '综合-每日'
subjectTypeAL = '案例'
subjectTypeLW = '论文'


def selectSubject(driver, index):
    driver.implicitly_wait(5)
    time.sleep(0.5)
    # 点击开始做题
    driver.find_element(By.CSS_SELECTOR, ".xpc-menu-box").find_elements_by_tag_name("dl")[1].find_elements_by_tag_name(
        "dd")[2].click()
    # 对应做题
    driver.find_element(By.CSS_SELECTOR, ".xpc_tiku_tab .clearfix").find_elements_by_tag_name("li")[index].click()

    time.sleep(0.5)

    if 0 == index:
        mrylSubject(driver, index)
    if 3 == index:
        zjlxSubject(driver, index)


def mrylSubject(driver, index):
    driver.implicitly_wait(5)
    paperNo = 0
    pageIndex = 0
    # 循环一次 点击下一页
    for i in range(selectDayPage):
        pageIndex = pageIndex + 1

        subjectPageEl = driver.find_element(By.CSS_SELECTOR, '.xpc_tiku_allcontent').find_element(By.ID, "dataList")
        # 试卷标题
        paperTitleList = subjectPageEl.find_elements(By.TAG_NAME, 'tr')

        # 每一题
        # 当前遍历题的 下标，用于处理 继续做题时，页面跳转后重新定位到跳转呢按钮
        pageSubIndex = 0
        for pageEl in paperTitleList:
            pageSubIndex = pageSubIndex + 1
            paperNo = paperNo + 1

            # 获取测试标题
            paperTitle = pageEl.find_elements_by_tag_name("td")[0].text.strip()
            # 获取最右侧两个按钮超链接
            pageUrlEls = pageEl.find_elements_by_tag_name("td")[3].find_elements(By.TAG_NAME, 'a')

            paperReportUrl = ''
            paperDoUrl = ''

            pageAny = None

            # 最右侧每一个按钮
            for pageAnyUrl in pageUrlEls:
                urlName = pageAnyUrl.text.strip()
                url = ''
                # 章节练习 分析重新做题
                if index == 3:
                    url = pageAnyUrl.get_attribute('href')

                    if urlName == paperReportUrlStr:
                        paperReportUrl = url
                    elif urlName == paperDoUrlStr:
                        paperDoUrl = url
                # 每日一练 分析：继续做题、开始做题、重新做题
                if index == 0:
                    time.sleep(0.5)
                    if urlName == paperDoAgainUrlStr:
                        urlName = pageAnyUrl.text.strip()
                        paperDoUrl = xs_driver.xiSaiHomeUrl + pageAnyUrl.get_attribute('data-accessuri')
                        pageAny = pageAnyUrl
                    elif urlName == paperDoStartUrlStr:
                        url = pageAnyUrl.get_attribute('onclick')
                        start_index = url.find('(') + 1
                        end_index = url.find(')', start_index)
                        params = url[start_index:end_index]
                        urlName = pageAnyUrl.text.strip()
                        paperDoUrl = xs_driver.xiSaiHomeUrl + params.split(',')[1].strip()[1:-1]
                        pageAny = pageAnyUrl
                    elif urlName == paperDoUrlStr:
                        urlName = pageAnyUrl.text.strip()
                        paperDoUrl = pageAnyUrl.get_attribute('href')
                        pageAny = pageAnyUrl

            # 根据标题判断试卷类型
            paperType = ''
            if subjectTypeAL in paperTitle:
                # 案例题型
                paperType = subjectTypeAL
            elif subjectTypeLW in paperTitle:
                # 论文提醒
                paperType = subjectTypeLW
            else:
                if index == 0:
                    # 综合题型（每日一练）
                    paperType = subjectTypeDAY
                elif index == 3:
                    # 综合提醒（选择题）
                    paperType = subjectTypeZH

            # 查询数据库中是否插入次试卷
            result = connDB.querySQLParams(sql.select_count_s_paper_sql, (paperType, paperTitle))
            if result['ct'] > 0:
                print('[试卷已存在数据库中，跳过] 试卷主键：', paperNo, '试卷标题：', paperTitle, '试卷类型：', paperType, '测试报告：', paperReportUrl,
                      '重新做题：', paperDoUrl)
                continue


            # 这里可以做数据插入动作
            insert_s_paper_data = (paperType, paperTitle, paperReportUrl, paperDoUrl)
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
            # 1、进一步解析题目  注意：这里的  pageUrlEls 需要经过判断才可用点击
            # ---------------------------------------------------
            mrylSubjectDo(driver, pageUrlEls, pageAny, paperId, paperType, pageIndex, pageSubIndex, index)

            break
            # if xs_main.env == 'Test':
            #     break

        break
        # if xs_main.env == 'Test':
        #     break
        # if i != selectDayPage - 1:
        #     nextBtn = driver.find_element(By.LINK_TEXT, "下一页")
        #     nextBtn.click()
        #     time.sleep(3)


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
            zjlxSubjectDo(driver, pageUrlEls, paperId, paperType, index)

            if xs_main.env == 'Test':
                break

        if xs_main.env == 'Test':
            break
        if i != selectPage - 1:
            nextBtn = driver.find_element(By.LINK_TEXT, "下一页")
            nextBtn.click()
            time.sleep(0.5)


def mrylSubjectDo(driver, pageUrlEls, pageAny, paperId, paperType, pageIndex, pageSubIndex, index):
    driver.implicitly_wait(5)
    # 将每一题的右侧按钮传递过来， 并点击重新做题
    openFlag = True

    # 判断是否为继续做题，继续做题会信弹出窗口点击
    if pageAny.text.strip() == paperDoAgainUrlStr:

        current_url = driver.current_url

        original_window = driver.current_window_handle
        driver.execute_script("window.open();")
        # 获取所有窗口的句柄
        all_windows = driver.window_handles
        # 寻找新窗口的句柄，排除原始窗口
        new_window = None
        for window in all_windows:
            if window != original_window:
                new_window = window
                break
        driver.switch_to.window(new_window)
        driver.get(current_url)
        time.sleep(1)

        # 跳转到之前反转的页面，翻的页面数越多，重复翻的时长越长
        for i in range(pageIndex - 1):
            nextBtn = driver.find_element(By.LINK_TEXT, "下一页")
            nextBtn.click()
            time.sleep(1)

        pageEl = \
            driver.find_element(By.CSS_SELECTOR, '.xpc_tiku_allcontent').find_element(By.ID, "dataList").find_elements(
                By.TAG_NAME, 'tr')[pageSubIndex - 1]
        pageUrlEls = pageEl.find_elements_by_tag_name("td")[3].find_elements(By.TAG_NAME, 'a')
        for pageAnyUrl in pageUrlEls:
            urlName = pageAnyUrl.text.strip()
            if urlName == paperDoAgainUrlStr:
                pageAnyUrl.click()
                doAgainEl = \
                    driver.find_element(By.CSS_SELECTOR, '.layui-layer-content').find_element(By.CSS_SELECTOR,
                                                                                              '.continue-wrap').find_elements(
                        By.TAG_NAME, 'a')[1]
                # 二次确认，点击重新考试
                doAgainEl.click()
                time.sleep(0.5)

                mrylGetSubjectDo(driver, paperId)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(0.5)
    else:
        # 点击后跳转到新页面
        pageAny.click()
        # 在新页面中进行操作，都需要这一个步骤
        all_handles = driver.window_handles
        new_window_handle = None
        for handle in all_handles:
            if handle != driver.current_window_handle:
                new_window_handle = handle
                driver.switch_to.window(new_window_handle)

                mrylGetSubjectDo(driver, paperId)
                driver.close()
                time.sleep(0.5)
        # 跳转到首页 - 拿回 driver 对象
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.5)


# 在每日一练中间页面环境点击 "练习模式" 进入题库
def mrylGetSubjectDo(driver, paperId):
    getAna = driver.find_element(By.CSS_SELECTOR, '.ecv2_btns').find_elements(By.TAG_NAME, 'a')[1]
    getAna.click()
    subject_mryl.getZhSubject(driver, paperId)


# 章节练习
# driver 全局对象用于跳转
# pageUrlEls 用于找到对应跳转按钮
def zjlxSubjectDo(driver, pageUrlEls, paperId, paperType, index):
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
