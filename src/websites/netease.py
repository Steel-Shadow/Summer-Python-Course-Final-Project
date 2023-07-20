from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.websites.driver import init_driver
from typing import Iterable


def scraping(keyword_collections: Iterable[str]):
    driver = init_driver()

    for keyword in keyword_collections:
        # 导航到目标网页
        url = f"https://open.163.com/newview/search/{keyword}"  # 替换为目标网站的URL
        driver.get(url)

        try:
            WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div[2]/div[1]/div[3]')))
        except:
            yield list()
            continue

        courses = driver.find_elements(By.CLASS_NAME, 'card-link')

        course_info_list = list()
        for i in courses:
            link = i.find_element(By.TAG_NAME, 'a')
            course_info_list.append((link.get_attribute('title'), link.get_attribute('href')))

        yield course_info_list

    driver.close()
