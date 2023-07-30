from typing import Iterable

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .driver import init_driver


def scraping(keyword_collections: Iterable[str]):
    driver = init_driver()

    for keyword in keyword_collections:
        url = f"https://search.bilibili.com/all?keyword={keyword}"  # 替换为目标网站的URL
        driver.get(url)

        try:
            WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "bili-video-card__info--right"))
            )
        except:
            yield list()
            continue

        courses = driver.find_elements(By.CLASS_NAME, "bili-video-card__info--right")
        course_info_list = list()

        i = 0
        while i < 10 and i < len(courses):
            e = courses[i]
            title = e.find_element(By.TAG_NAME, "a")
            link = title.get_attribute("href")
            course_info_list.append(("bilibili", title.text, link, ''))
            i += 1

        yield course_info_list

    driver.close()
