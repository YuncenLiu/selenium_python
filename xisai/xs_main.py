import xs_driver
import xs_login
import xs_constans
import xs_do
from subject import connDB

# 如果为 Test 则只获取第一页，第一套试卷
# env = 'Test'
env = 'Pro'

# 2024-07-05
# 方法入口
if __name__ == '__main__':

    # 初始化数据库
    # connDB.initDb()
    # 获取 selenium 对象服务，并打开浏览器
    driver = xs_driver.getDriver()
    # try:
    # 配置全局对象
    # 隐式等待 如果取元素的时候，如果找不到找不到整个元素，我最多等5秒，超过5秒就一场（推荐）
    driver.implicitly_wait(5)

    # 登录
    xs_login.login(driver)

    # 需要爬取的范围
    subjectSet = set()
    subjectSet.add(xs_constans.do_mryl)
    # subjectSet.add(xs_constans.do_lnzt)
    # subjectSet.add(xs_constans.do_mnsj)
    # subjectSet.add(xs_constans.do_zjlx)
    # subjectSet.add(xs_constans.do_zsdp)
    # subjectSet.add(xs_constans.do_gpkd)
    # subjectSet.add(xs_constans.do_gpct)
    # subjectSet.add(xs_constans.do_lwfw)
    xs_do.getSubject(subjectSet, driver)


    # except Exception as e:
    #     print("程序异常:", e)
    #     # 在此处可以处理或重新引发异常
    #     raise  # 重新引发异常到上层调用
    # finally:
    #     # 关闭
    #     xs_driver.closeBrew(driver)
