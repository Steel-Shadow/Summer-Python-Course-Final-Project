from selenium.webdriver.common.by import By
from src.websites.driver import init_driver

from typing import Iterable


def scraping(keyword_collections: Iterable[str]):
    driver = init_driver()

    for course in keyword_collections:
        # 导航到目标网页
        url = f"https://search.bilibili.com/all?keyword={course}"  # 替换为目标网站的URL
        driver.get(url)

        courses = driver.find_elements(By.CLASS_NAME, 'bili-video-card__info--right')
        course_info_list = list()

        i = 0
        while i < 5 and i < len(courses):
            e = courses[i]
            title = e.find_element(By.TAG_NAME, 'a')
            link = title.get_attribute('href')
            detail = e.text.removeprefix(title.text + '\n')
            course_info_list.append((title.text, link, detail))
            i += 1

        for info in course_info_list:
            print(info)

    driver.close()
