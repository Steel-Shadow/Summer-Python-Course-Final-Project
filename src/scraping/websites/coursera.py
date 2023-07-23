from line_profiler_pycharm import profile
from selenium.webdriver.common.by import By

from src.scraping.websites.driver import init_driver

driver = init_driver()


@profile
def scraping(keyword: str):
    url_coursera = f"https://www.coursera.org/search?query={keyword}"
    driver.get(url_coursera)

    courses = driver.find_elements(By.XPATH, '//li[@class="cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76"]')

    course_info_list = list()
    for i in courses:
        name = i.find_element(By.XPATH, './/h2[@class="cds-119 css-h1jogs cds-121"]').text
        link = i.find_element(By.XPATH, "./div/a").get_attribute('href')
        school = i.find_element(By.XPATH, './/span[@class="cds-119 css-1mru19s cds-121"]').text
        course_info_list.append(('coursera', name, link, school))

    return course_info_list


def close():
    driver.close()
