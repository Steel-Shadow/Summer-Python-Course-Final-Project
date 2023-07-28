from selenium.webdriver.common.by import By

from .driver import init_driver

driver = init_driver()


def scraping(keyword: str):
    url_ke = f"https://ke.qq.com/course/list/{keyword}"
    driver.get(url_ke)

    course_links = driver.find_elements(By.XPATH, '//section[@class="course-card-expo-wrapper"]/a[@href]')
    course_names = driver.find_elements(By.XPATH, '//div[@class="kc-course-card-content"]/h3[@title]')

    course_platform_list = list()
    course_name_list = list()
    course_link_list = list()
    course_college_list = list()

    for link in course_links:
        course_platform_list.append('腾讯课堂')
        course_college_list.append('')
        course_link_list.append(link.get_attribute('href'))

    for name in course_names:
        course_name_list.append(name.text)

    course_info = list(zip(course_platform_list, course_name_list, course_link_list, course_college_list))
    return course_info


def driver_quit():
    driver.quit()
