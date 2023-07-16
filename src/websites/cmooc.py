from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scraping(driver: WebDriver, course: str):
    # 导航到目标网页
    url = f"https://www.cmooc.com/?s={course}"  # 替换为目标网站的URL
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'newscontent')))

    courses = driver.find_elements(By.CLASS_NAME, 'course-list')

    output = list()
    for i in courses:
        t = i.find_element(By.TAG_NAME, 'a')
        title = t.get_attribute('title')
        link = t.get_attribute('href')

        output.append((title, link, ''))

    for i in output:
        print(i)
