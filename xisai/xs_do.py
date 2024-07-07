import xs_constans
from subject import subject_do

chooseSubjectModule = "当前您选择的模块是："


# 开始做题 输入需要获取的模块集合
def getSubject(subjectSet, driver):
    if xs_constans.do_mryl in subjectSet:
        # 每日一练
        print(chooseSubjectModule, xs_constans.do_mryl, 0)
        subject_do.selectSubject(driver, 0)

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
