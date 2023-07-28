from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .driver import init_driver

driver = init_driver()


def scraping(keyword: str):
    # 导航到目标网页
    url = f"https://www.cmooc.com/?s={keyword}"  # 替换为目标网站的URL
    driver.get(url)

    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, "newscontent"))
        )
    except:
        return list()

    courses = driver.find_elements(By.CLASS_NAME, "course-list")

    course_info_list = list()
    for i in courses:
        t = i.find_element(By.TAG_NAME, "a")
        title = t.get_attribute("title")
        link = t.get_attribute("href")
        school = i.find_element(By.XPATH, './/*[@class="course-nm course-sch"]').text
        course_info_list.append(("cmooc", title, link, school))

    return course_info_list


def driver_quit():
    driver.quit()
