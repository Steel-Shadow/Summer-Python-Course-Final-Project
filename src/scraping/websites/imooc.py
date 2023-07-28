from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .driver import init_driver

driver = init_driver()


def scraping(keyword: str):
    url = f"https://www.imooc.com/search/?words={keyword}"
    driver.get(url)

    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div[3]/div[1]/div[3]")))
    except:
        return list()

    course_links = driver.find_elements(By.XPATH,
                                        '//a[@class="js-zhuge-allResult item-title js-result-item js-item-title "]')

    course_info_list = list()

    for link in course_links:
        course_info_list.append(('imooc', link.text, link.get_attribute('href'), ''))

    return course_info_list


def driver_quit():
    driver.quit()
