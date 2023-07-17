from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.websites.driver import init_driver

from typing import Iterable


def scraping(keyword_collections: Iterable[str]):
    driver = init_driver()

    for keyword in keyword_collections:
        url = f"https://www.imooc.com/search/?words={keyword}"
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div[3]/div[1]/div[3]")))
        course_links = driver.find_elements(By.XPATH,
                                            '//a[@class="js-zhuge-allResult item-title js-result-item js-item-title "]')

        course_link_list = list()
        course_name_list = list()

        for link in course_links:
            course_link_list.append(link.get_attribute('href'))
            course_name_list.append(link.text)

        course_info_list = zip(course_name_list, course_link_list)
        for info in course_info_list:
            print(info)

    driver.close()
