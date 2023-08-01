from typing import Iterable

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .driver import init_driver


def scraping(keyword_collections: Iterable[str]):
    driver = init_driver()

    for keyword in keyword_collections:
        url = f"https://www.cnmooc.org/portal/frontCourseIndex/course.mooc?k={keyword}"
        driver.get(url)

        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, "view-item")))
        except:
            yield list()
            continue

        courses = driver.find_elements(By.CLASS_NAME, 'view-item')

        course_info_list = list()
        for i in courses:
            link = 'https://www.cnmooc.org' + i.find_element(By.XPATH, './/div[@class="view-img"]').get_attribute(
                'href')
            name = i.find_element(By.XPATH, './/a[@class="link-default link-course-detail"]').text
            school = i.find_element(By.XPATH, './/*[@class="t-school substr"]').text
            course_info_list.append(('haodaxue', name, link, school))

        yield course_info_list

    driver.close()
