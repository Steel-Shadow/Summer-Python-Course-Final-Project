from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scraping(driver: WebDriver, course: str):
    # 导航到目标网页
    url = "https://www.icourses.cn/oc/"  # 替换为目标网站的URL
    driver.get(url)

    # 输入搜索框
    search_box = driver.find_element(By.ID, 'searchInput')
    search_box.clear()
    search_box.send_keys(course)
    search_box.send_keys(Keys.RETURN)

    # 显式等待 搜索结果
    try:
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'icourse-desc')))
    except:
        driver.quit()
        return

    courses = driver.find_elements(By.CLASS_NAME, 'icourse-desc')
    output = list()
    for i in courses:
        title = i.find_element(By.CLASS_NAME, 'icourse-desc-title')
        link = title.get_attribute('href')
        detail = i.text.removeprefix(title.text + '\n')
        output.append((title.text, link, detail))

    for i in output:
        print(i)
