import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from . import connDB
from . import sql
import main

# 章节练习一共三页
selectPage = 3
paperReportUrlStr = '测试报告'
paperDoUrlStr = '重新做题'

subjectTypeZH = '综合'
subjectTypeAL = '案例'
subjectTypeLW = '论文'


# 章节练习
def zjlxSubject(driver):
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
                if urlName == paperReportUrlStr:
                    paperReportUrl = url
                elif urlName == paperDoUrlStr:
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
                  '重新做题：',
                  paperDoUrl)

            if paperReportUrl is None:
                print('这套试卷没有做过，暂不支持进一步爬取')
                continue

            # ---------------------------------------------------
            # 1、进一步解析题目
            # ---------------------------------------------------
            subjectDo(driver, pageUrlEls, paperId, paperType)

            if main.env == 'Test':
                break

        if main.env == 'Test':
            break
        if i != selectPage - 1:
            nextBtn = driver.find_element(By.LINK_TEXT, "下一页")
            nextBtn.click()
            time.sleep(0.5)


# driver 全局对象用于跳转
# pageUrlEls 用于找到对应跳转按钮
def subjectDo(driver, pageUrlEls, paperId, paperType):
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
                getZhSubject(driver, paperId)
            elif paperType == subjectTypeAL:
                print('当前类型不支持：', paperType)
            elif paperType == subjectTypeLW:
                print('当前类型不支持：', paperType)
            # 关闭此页面
            driver.close()
    # 跳转到首页 - 拿回 driver 对象
    driver.switch_to.window(driver.window_handles[0])


# 获取综合类型题库
def getZhSubject(driver, paperId):
    # 找到左侧的所有题目
    selectors = driver.find_element(By.CSS_SELECTOR, ".cbnWrap").find_elements_by_css_selector('span[data-stid]')

    # 循环的每一个是每一道题目，如果有45道题，会循环 45次
    for sec in selectors:

        # 点击选中对应题目编号
        sec.click()
        # 当前题号
        subjectNumber = sec.text.strip()
        time.sleep(0.2)

        # 选择题El标签
        subjectEl = driver.find_element_by_class_name('single-content')

        # 题号 第几题（单选）最顶部分题目
        subjectNo = subjectEl.find_element_by_class_name('lh2').text.strip()

        # 题目主体部分由 div 或 p 标签构成，不确定 可能都有、也可能都没有。
        sub_elements = subjectEl.find_elements_by_css_selector('.singleR')
        ansTitleSet = set()
        if sub_elements:
            for p in sub_elements:
                ansTitleSet.add(p.text.strip())
            for div in sub_elements:
                ansTitleSet.add(div.text.strip())

        # 将题目拼接起来，去掉前后两个双引号
        subjectTitle = str(ansTitleSet)[2:-2]

        print("试卷编号：{}，题编号：{}，题号：{}，题目：{}".format(paperId, subjectNumber, subjectNo, subjectTitle))
        # 题目编号不写入数据库
        # 向 s_subject 表插入数据
        insert_s_subject_data = (paperId, subjectNo, subjectTitle)
        # 获取到的 sub_id 是 s_subject 自增主键
        subId = connDB.executeSQLParams(sql.insert_s_subject_sql, insert_s_subject_data)

        # 获取题目中的 Images 图片连接
        # -----------------------------------------------
        # 图片插入操作 及 题目和图片关联表插入操作  涉及表： s_pic  s_sub_pic
        # -----------------------------------------------
        imgEl = driver.find_elements(By.CSS_SELECTOR, ".singleR img")
        imgList = [img.get_attribute("src") for img in imgEl]
        if len(imgList) > 0:
            for img in imgList:
                insert_s_pic_dat = img

                # 数据库插入 s_pic 表，返回的 pic_id 插入到 s_sub_pic 关联表
                picId = connDB.executeSQLParams(sql.insert_s_pic_sql, insert_s_pic_dat)
                insert_s_sub_pic_data = (subId, picId)
                connDB.executeSQLParams(sql.insert_s_sub_pic_sql, insert_s_sub_pic_data)

        imgListStr = ", ".join(imgList)
        print('题目中涉及的图片:', imgListStr)

        # 处理选择题
        # 获取选择题列表
        chooseList = driver.find_element_by_class_name('answerWrap').find_element_by_class_name(
            'answerList').find_element_by_class_name('answerContent').find_elements_by_class_name(
            'answerContentList')

        # 存储四个元素  每个元素 包括选项 和 正确答案
        insertChooseList = []
        chList = []

        ansChCount = 0
        # 存储选项

        # 循环遍历 4个 选择题

        for chooseAns in chooseList:
            ansChCount = ansChCount + 1
            chooseStr = chooseAns.find_element(By.TAG_NAME, "label").text.strip()
            chList.insert(ansChCount, chooseStr)

        insertChooseList.insert(ansChCount, chList)

        # daanList = driver.find_element_by_class_name('answerEnd').find_elements_by_class_name('daan_sty')

        # daanCount = 0
        # for daan in daanList:
        #     daanCount = daanCount + 1
        #     answer_elements = daan.find_elements(By.CLASS_NAME, "p1")
        #
        #     daanTrue = ""
        #     daanMy = ""
        #     for answer_element in answer_elements:
        #         answer_type = answer_element.find_element(By.TAG_NAME, "span").text
        #         answer_text = answer_element.find_element(By.TAG_NAME, "span:nth-child(2)").text
        #         if answer_type == '正确答案':
        #             daanTrue = answer_text
        #         if answer_type == '我的答案':
        #             daanMy = answer_text
        #
        #     print('第', daanCount, '题：正确答案是：', daanTrue, '，我的答案是：', daanMy)
        #     chList = insert_choose_list[daanCount - 1]
        #     insert_s_choose_sql = "insert into s_choose(sub_id,ch_a,ch_b,ch_c,ch_d,ch_true,ch_my) value (%s,%s,%s,%s,%s,%s,%s)"
        #     insert_s_choose_data = (sub_id, chList[0], chList[1], chList[2], chList[3], daanTrue, daanMy)
        #     ch_id = insertDb(insert_s_choose_sql, insert_s_choose_data)
        #
        #     insert_s_sub_ch_sql = "insert into s_sub_ch(sub_id,ch_id) value (%s,%s)"
        #     insert_s_sub_ch_data = (sub_id, ch_id)
        #     insertDb(insert_s_sub_ch_sql, insert_s_sub_ch_data)
