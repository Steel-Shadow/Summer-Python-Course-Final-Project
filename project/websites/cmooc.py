from typing import Iterable

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .driver import init_driver


def scraping(keyword_collections: Iterable[str]):
    driver = init_driver()

    for keyword in keyword_collections:
        url = f"https://www.cmooc.com/?s={keyword}"  # 替换为目标网站的URL
        driver.get(url)

        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, "newscontent"))
            )
        except:
            yield list()
            continue

        courses = driver.find_elements(By.CLASS_NAME, "course-list")

        course_info_list = list()
        for i in courses:
            t = i.find_element(By.TAG_NAME, "a")
            title = t.get_attribute("title")
            link = t.get_attribute("href")
            school = i.find_element(By.XPATH, './/*[@class="course-nm course-sch"]').text
            course_info_list.append(("cmooc", title, link, school))

        yield course_info_list

    driver.close()


if __name__ == '__main__':
    for i in scraping(["java"]):
        print(i)
