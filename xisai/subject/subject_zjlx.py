import time

from selenium.webdriver.common.by import By

from . import connDB
from . import sql




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

        # 获取题目中的 选择题
        # -----------------------------------------------
        # 选择题插入操作 及 选择题正确选项、我的选项  涉及表： s_choose  s_sub_ch
        # -----------------------------------------------
        chooseList = driver.find_element_by_class_name('answerWrap').find_element_by_class_name(
            'answerList').find_element_by_class_name('answerContent').find_elements_by_class_name(
            'answerContentList')

        # 存储四个元素  每个元素 包括选项 和 正确答案
        chList = []
        ansChCount = 0
        # 循环遍历 4个 选择题
        for chooseAns in chooseList:
            ansChCount = ansChCount + 1
            chooseStr = chooseAns.find_element(By.TAG_NAME, "label").text.strip()
            chList.insert(ansChCount, chooseStr)

        # 获取 正确的选择题 和 我的选择题
        chooseTrueEl = driver.find_element_by_class_name('answerEnd').find_elements_by_class_name('daan_sty')
        # 选择题下标 1代表A 2代表B
        chooseIndex = 0
        for choose in chooseTrueEl:
            chooseIndex = chooseIndex + 1
            answer_elements = choose.find_elements(By.CLASS_NAME, "p1")

            # 正确答案
            chTrue = ""
            # 我的答案 可能为空
            chMy = ""

            # 循环获取 4个 选择题的答案
            for answer_element in answer_elements:
                answer_type = answer_element.find_element(By.TAG_NAME, "span").text
                answer_text = answer_element.find_element(By.TAG_NAME, "span:nth-child(2)").text
                if answer_type == '正确答案':
                    chTrue = answer_text
                if answer_type == '我的答案':
                    chMy = answer_text

            # 插入 选项表 s_choose 获取选项 chId
            insert_s_choose_data = (subId, chList[0], chList[1], chList[2], chList[3], chTrue, chMy)
            print(chList[0], chList[1], chList[2], chList[3], '【正确答案：', chTrue, '】 【我的答案:', chMy, '】')
            chId = connDB.executeSQLParams(sql.insert_s_choose_sql, insert_s_choose_data)

            # 插入 题目表选项表  关联表 s_sub_ch
            insert_s_sub_ch_data = (subId, chId)
            connDB.executeSQLParams(sql.insert_s_sub_ch_sql, insert_s_sub_ch_data)

        # -----------------------------------------------
        # 获取题目中的 解析、解析中的图片 更新 s_subject (sub_tag sub_info sub_ref)
        # 存在于解析中的图片，也一并保存在 s_pic 但是关联表和题目不一致 s_sub_ref_pic
        # -----------------------------------------------

        shitiDespEl = driver.find_element_by_class_name('shitiDesp')
        # 解析所有答案图片
        daanImgs = shitiDespEl.find_elements(By.CSS_SELECTOR, "img")
        daanImgList = [img.get_attribute("src") for img in daanImgs]

        # 插入解析中的图片信息到 s_pic 和 s_sub_ref_pic
        if len(daanImgList) > 0:
            for img in daanImgList:
                insert_s_pic_data = (img)
                picId = connDB.executeSQLParams(sql.insert_s_pic_sql, insert_s_pic_data)

                insert_s_sub_ref_pic_data = (subId, picId)
                connDB.executeSQLParams(sql.insert_s_sub_ref_pic_sql, insert_s_sub_ref_pic_data)

        # 题目里的图片，按逗号分隔
        daanImg = ", ".join(daanImgList)

        # 获取解析列表
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

        # 分别获取所属知识点
        subTag = ""
        # 分别获取试题难度
        subInfo = ""
        # 分别获取参考解析1 、2、3、4  （可能存在多个解析内容）
        subRef = ""
        for dict in spanDictList:
            for k, v in dict.items():
                # 空值不处理
                if v is None:
                    continue

                if "所属知识点：" == k:
                    subTag = v
                elif "试题难度：" == k:
                    subInfo = v

                if "参考解析1：" == k:
                    subRef = v
                if "参考解析2：" == k:
                    subRef = subRef + v
                if "参考解析3：" == k:
                    subRef = subRef + v
                if "参考解析4：" == k:
                    subRef = subRef + v

        # 去掉末尾分号
        subTag = subTag[0:-1]
        update_s_subject_data = (subTag, subInfo, subRef, subId)

        # 最后 update 题目表，完成所有更新
        connDB.executeSQLParams(sql.update_s_subject_sql, update_s_subject_data)

        # 打印解析内容，及解析中包含的图片
        print(spanDictList, daanImg)
