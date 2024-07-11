import xs_constans
from subject import subject_do
from xisai.subject import connDB, sql

chooseSubjectModule = "当前您选择的模块是："

# 可以重试20次
errMrylAgain = 20


# 开始做题 输入需要获取的模块集合
def getSubject(subjectSet, driver):
    if xs_constans.do_mryl in subjectSet:
        # 每日一练
        print(chooseSubjectModule, xs_constans.do_mryl, 0)
        for i in range(errMrylAgain):
            try:
                subject_do.selectSubject(driver, 0)
            except Exception as e:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                resultId = connDB.querySQL(sql.select_max_paper_id_sql)
                errPaperId = resultId['id']

                resultTitle = connDB.querySQL(sql.select_max_paper_title_sql)
                errPaperTitle = resultTitle['p_title']
                print('==============> 失败的 paperId：', errPaperId, ' ======> 失败的 Title ：', errPaperTitle)

                connDB.executeSQLParams(sql.insert_s_err_sql, (errPaperTitle))

                connDB.executeSQLParams(sql.delete_init_choose_sql, (errPaperId))
                connDB.executeSQLParams(sql.delete_init_pic_sql1, (errPaperId))
                connDB.executeSQLParams(sql.delete_init_pic_sql2, (errPaperId))
                connDB.executeSQLParams(sql.delete_init_sub_ch_sql, (errPaperId))
                connDB.executeSQLParams(sql.delete_init_sub_pic_sql, (errPaperId))
                connDB.executeSQLParams(sql.delete_init_sub_ref_pic_sql, (errPaperId))
                connDB.executeSQLParams(sql.delete_init_subject_sql, (errPaperId))
                connDB.executeSQLParams(sql.delete_init_paper_sql, (errPaperId))
                print('当前已失败：', i, '次：错误原因是', e)



    if xs_constans.do_lnzt in subjectSet:
        # 历年真题
        print(chooseSubjectModule, xs_constans.do_lnzt, 1)
        subject_do.selectSubject(driver, 1)

    if xs_constans.do_mnsj in subjectSet:
        # 模拟试卷
        print(chooseSubjectModule, xs_constans.do_mnsj, 2)
        subject_do.selectSubject(driver, 2)

    if xs_constans.do_zjlx in subjectSet:
        # 章节练习
        print(chooseSubjectModule, xs_constans.do_zjlx, 3)
        subject_do.selectSubject(driver, 3)

    if xs_constans.do_zsdp in subjectSet:
        # 知识点评
        print(chooseSubjectModule, xs_constans.do_zsdp, 4)
        subject_do.selectSubject(driver, 4)

    if xs_constans.do_gpkd in subjectSet:
        # 高频考点
        print(chooseSubjectModule, xs_constans.do_gpkd, 5)
        subject_do.selectSubject(driver, 5)

    if xs_constans.do_gpct in subjectSet:
        # 高频错题
        print(chooseSubjectModule, xs_constans.do_gpct, 6)
        subject_do.selectSubject(driver, 6)

    if xs_constans.do_lwfw in subjectSet:
        # 论文范文
        print(chooseSubjectModule, xs_constans.do_lwfw, 7)
        subject_do.selectSubject(driver, 7)

