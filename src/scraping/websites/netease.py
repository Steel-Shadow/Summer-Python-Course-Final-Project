from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.scraping.websites.driver import init_driver

driver = init_driver()


def scraping(keyword: str):
    # 导航到目标网页
    url = f"https://open.163.com/newview/search/{keyword}"  # 替换为目标网站的URL
    driver.get(url)

    try:
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div[2]/div[1]/div[3]')))
    except:
        return list()

    courses = driver.find_elements(By.CLASS_NAME, 'card-link')

    course_info_list = list()
    for i in courses:
        link = i.find_element(By.TAG_NAME, 'a')
        course_info_list.append(('netease', link.get_attribute('title'), link.get_attribute('href'), ''))

    return course_info_list


def close():
    driver.close()


if __name__ == '__main__':
    print(scraping('操作系统'))
