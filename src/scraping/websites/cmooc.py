from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Iterable
from src.scraping.websites.driver import init_driver


def scraping(keyword_collections: Iterable[str]):
    driver = init_driver()

    for course in keyword_collections:
        # 导航到目标网页
        url = f"https://www.cmooc.com/?s={course}"  # 替换为目标网站的URL
        driver.get(url)

        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, 'newscontent')))
        except:
            yield list()
            continue

        courses = driver.find_elements(By.CLASS_NAME, 'course-list')

        course_info_list = list()
        for i in courses:
            t = i.find_element(By.TAG_NAME, 'a')
            title = t.get_attribute('title')
            link = t.get_attribute('href')

            course_info_list.append((title, link))

        yield course_info_list

    driver.close()
