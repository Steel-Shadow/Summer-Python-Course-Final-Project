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

        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div[3]/div[1]/div[3]")))
        except:
            yield list()
            continue

        course_links = driver.find_elements(By.XPATH,
                                            '//a[@class="js-zhuge-allResult item-title js-result-item js-item-title "]')

        course_info_list = list()

        for link in course_links:
            course_info_list.append((link.text, link.get_attribute('href')))

        yield course_info_list

    driver.close()
