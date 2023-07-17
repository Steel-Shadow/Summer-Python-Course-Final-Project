from selenium.webdriver.common.by import By
from src.websites.driver import init_driver
from typing import Iterable


def scraping(keyword_collections: Iterable[str]):
    driver = init_driver()

    for keyword in keyword_collections:
        url = f"https://www.icourse163.org/search.htm?search={keyword}#/"
        driver.get(url)

        course_names = driver.find_elements(By.XPATH, '//span[@class=" u-course-name f-thide"]')
        course_name_list = list()
        for name in course_names:
            course_name_list.append(name.text)

        course_links = driver.find_elements(By.XPATH, '//div[@class="cnt f-pr"]/a[@href]')
        course_link_list = list()
        for link in course_links:
            if link.get_attribute('href')[0] == '/':
                course_link_list.append(link.get_attribute('href')[2:])
            else:
                course_link_list.append(link.get_attribute('href'))

        course_info_list = zip(course_name_list, course_link_list)
        for info in course_info_list:
            print(info)

    driver.close()
