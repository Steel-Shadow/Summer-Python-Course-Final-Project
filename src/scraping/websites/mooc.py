from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.scraping.websites.driver import init_driver

driver = init_driver()


def scraping(keyword: str):
    url = f"https://www.icourse163.org/search.htm?search={keyword}#/"
    driver.get(url)

    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class=" u-course-name f-thide"]')))
    except:
        return list()

    courses = driver.find_elements(By.XPATH, '//div[@class="cnt f-pr"]')

    course_info_list = list()
    for i in courses:
        name = i.find_element(By.XPATH, './/span[@class=" u-course-name f-thide"]')
        link = i.find_element(By.XPATH, './a[@href]')

        try:
            school = i.find_element(By.XPATH, './/a[@class="t21 f-fc9"]').text
        except:
            continue

        if link.get_attribute('href')[0] == '/':
            course_info_list.append(('mooc', name.text, link.get_attribute('href')[2:], school))
        else:
            course_info_list.append(('mooc', name.text, link.get_attribute('href'), school))

    return course_info_list


def close():
    driver.close()
