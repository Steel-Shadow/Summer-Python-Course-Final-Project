from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Iterable

from src.websites.driver import init_driver


def scraping(keyword_collections: Iterable[str]):
    driver = init_driver()

    for keyword in keyword_collections:
        # 导航到目标网页
        url = "https://www.icourses.cn/oc/"  # 替换为目标网站的URL
        driver.get(url)

        # 输入搜索框
        search_box = driver.find_element(By.ID, 'searchInput')
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        # 显式等待 搜索结果
        try:
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'icourse-desc-title')))
        except:
            yield list()
            continue

        courses = driver.find_elements(By.CLASS_NAME, 'icourse-desc')
        course_info_list = list()
        for i in courses:
            title = i.find_element(By.CLASS_NAME, 'icourse-desc-title')
            link = title.get_attribute('href')
            course_info_list.append((title.text, link))

        yield course_info_list

    driver.close()
