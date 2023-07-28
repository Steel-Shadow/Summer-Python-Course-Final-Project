from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .driver import init_driver

driver = init_driver()


def scraping(keyword: str):
    url = f"https://www.cnmooc.org/portal/frontCourseIndex/course.mooc?k={keyword}"
    driver.get(url)

    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, "view-item")))
    except:  # 超时返回空
        return list()

    courses = driver.find_elements(By.CLASS_NAME, 'view-item')

    course_info_list = list()
    for i in courses:
        link = 'https://www.cnmooc.org' + i.find_element(By.XPATH, './/div[@class="view-img"]').get_attribute('href')
        name = i.find_element(By.XPATH, './/a[@class="link-default link-course-detail"]').text
        school = i.find_element(By.XPATH, './/*[@class="t-school substr"]').text
        course_info_list.append(('haodaxue', name, link, school))

    return course_info_list


def driver_quit():
    driver.quit()
