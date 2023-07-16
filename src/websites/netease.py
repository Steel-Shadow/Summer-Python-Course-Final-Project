from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scraping(driver: WebDriver, course: str):
    # 导航到目标网页
    url = f"https://open.163.com/newview/search/{course}"  # 替换为目标网站的URL
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div[2]/div[1]/div[3]')))

    courses = driver.find_elements(By.CLASS_NAME, 'type-card')

    output = list()
    for i in courses:
        link = i.find_element(By.TAG_NAME, 'a').get_attribute('href')
        t = i.find_element(By.CLASS_NAME, 'info').find_elements(By.CLASS_NAME, 'subname')
        output.append((t[0].text, link, t[1].text))

    for i in output:
        print(i)
