from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.websites.driver import init_driver
from typing import Iterable


def scraping(keyword_collections: Iterable[str]):
    driver = init_driver()

    for keyword in keyword_collections:
        url = f"https://www.cnmooc.org/portal/frontCourseIndex/course.mooc?keyWord={keyword}"

        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "view-list")))
        # print(driver.page_source)
        course_links = driver.find_elements(By.XPATH, '//div[@class="view-img"]')
        course_names = driver.find_elements(By.XPATH, '//a[@class="link-default link-course-detail"]')

        course_link_list = list()
        course_name_list = list()

        for link in course_links:
            course_link_list.append("https://www.cnmooc.org" + link.get_attribute('href'))

        for name in course_names:
            course_name_list.append(name.text)

        course_info_list = zip(course_name_list, course_link_list)
        for info in course_info_list:
            print(info)

    driver.close()
