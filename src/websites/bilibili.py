from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


def scraping(driver: WebDriver, course: str):
    # 导航到目标网页
    url = f"https://search.bilibili.com/all?keyword={course}"  # 替换为目标网站的URL
    driver.get(url)

    courses = driver.find_elements(By.CLASS_NAME, 'bili-video-card__info--right')
    output = list()

    i = 0
    while i < 24 and i < len(courses):
        e = courses[i]
        title = e.find_element(By.TAG_NAME, 'a')
        link = title.get_attribute('href')
        detail = e.text.removeprefix(title.text + '\n')
        output.append((title.text, link, detail))
        i += 1

    for i in output:
        print(i)
