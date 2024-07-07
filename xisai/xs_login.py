import time

from selenium.webdriver.common.by import By

# 测试使用账号及密码
account = "15279151605"
password = "Abc123"


# 登录模块
def login(driver):
    # 找到整个登录框
    login_el = driver.find_element(By.CSS_SELECTOR, ".ecv2_loginTabs .hd .clearfix")
    # 选择第三个 使用密码登录
    login_el.find_elements_by_tag_name("li")[2].click()

    # 手动填入账号
    driver.find_element(By.ID, "account").send_keys(account)

    # 这里无法填入密码，并提交验证，此时只能借助人为形式，手动点击登录按钮，进行登录验证
    # 只有 8 秒时间输入密码并点击登录
    time.sleep(8)

    # 关闭提示按钮
    driver.find_element(By.ID, "wj_modal").find_element(By.CSS_SELECTOR, ".wj_closepop_new").click()
    print('此时已经登录成功啦')
