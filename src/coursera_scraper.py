from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re


options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

category = input()
url_coursera = f"https://www.coursera.org/search?query={category}&"
pattern = r'"href":"(.*?)"'
driver.get(url_coursera)
# wait = WebDriverWait(driver, 10)
# wait.until(EC.presence_of_element_located(()))

course_links = driver.find_elements(By.XPATH, '//div[@class="css-1cj5od"]/a')
course_names = driver.find_elements(By.XPATH, '//h2[@class="cds-119 css-h1jogs cds-121"]')

course_link_list = list()
course_name_list = list()

for link in course_links:
    link_str = re.search(pattern, link.get_attribute('data-click-value'))
    course_link_list.append("https://www.coursera.org" + link_str.group(1))

for name in course_names:
    course_name_list.append(name.text)

course_info_list = zip(course_name_list[1:], course_link_list)
for info in course_info_list:
    print(info)