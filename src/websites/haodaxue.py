from line_profiler_pycharm import profile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.websites.driver import init_driver
from typing import Iterable


@profile
def scraping(keyword_collections: Iterable[str]):
    driver = init_driver()

    for keyword in keyword_collections:
        url = f"https://www.cnmooc.org/portal/frontCourseIndex/course.mooc?k={keyword}"

        driver.get(url)

        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, "view-item")))
        except:  # 超时返回空
            yield list()
            continue

        course_links = driver.find_elements(By.XPATH, '//div[@class="view-img"]')
        course_names = driver.find_elements(By.XPATH, '//a[@class="link-default link-course-detail"]')

        course_link_list = list()
        course_name_list = list()

        for link in course_links:
            course_link_list.append("https://www.cnmooc.org" + link.get_attribute('href'))

        for name in course_names:
            course_name_list.append(name.text)

        course_info_list = zip(course_name_list, course_link_list)
        yield course_info_list

    driver.close()
