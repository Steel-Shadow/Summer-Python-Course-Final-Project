from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.scraping.websites.driver import init_driver
from typing import Iterable


def scraping(keyword_collections: Iterable[str]):
    driver = init_driver()

    for keyword in keyword_collections:
        url = f"https://www.icourse163.org/search.htm?search={keyword}#/"
        driver.get(url)

        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class=" u-course-name f-thide"]')))
        except:
            yield list()
            continue

        course_names = driver.find_elements(By.XPATH, '//span[@class=" u-course-name f-thide"]')
        course_links = driver.find_elements(By.XPATH, '//div[@class="cnt f-pr"]/a[@href]')

        course_info_list = list()
        for i in range(len(course_names)):
            name = course_names[i]
            link = course_links[i]

            if link.get_attribute('href')[0] == '/':
                course_info_list.append((name.text, link.get_attribute('href')[2:]))
            else:
                course_info_list.append((name.text, link.get_attribute('href')))

        yield course_info_list

    driver.close()
