import time

from selenium.webdriver.common.by import By
from . import subject_zjlx


def selectSubject(driver, index):
    time.sleep(0.5)
    # 点击开始做题
    driver.find_element(By.CSS_SELECTOR, ".xpc-menu-box").find_elements_by_tag_name("dl")[1].find_elements_by_tag_name(
        "dd")[2].click()
    # 对应做题
    driver.find_element(By.CSS_SELECTOR, ".xpc_tiku_tab .clearfix").find_elements_by_tag_name("li")[index].click()

    time.sleep(0.5)

    if 3 == index:
        subject_zjlx.zjlxSubject(driver)
