from typing import Iterable

from selenium.webdriver.common.by import By

from .driver import init_driver


def scraping(keyword_collections: Iterable[str]):
    driver = init_driver()

    for keyword in keyword_collections:
        url_ke = f"https://ke.qq.com/course/list/{keyword}"
        driver.get(url_ke)

        course_links = driver.find_elements(By.XPATH, '//section[@class="course-card-expo-wrapper"]/a[@href]')
        course_names = driver.find_elements(By.XPATH, '//div[@class="kc-course-card-content"]/h3[@title]')

        course_platform_list = list()
        course_name_list = list()
        course_link_list = list()
        course_college_list = list()

        for link in course_links:
            course_platform_list.append('tencent')
            course_college_list.append('')
            course_link_list.append(link.get_attribute('href'))

        for name in course_names:
            course_name_list.append(name.text)

        course_info_list = list(zip(course_platform_list, course_name_list, course_link_list, course_college_list))

        yield course_info_list

    driver.close()


if __name__ == '__main__':
    for i in scraping(["java"]):
        print(i)
