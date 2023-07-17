from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

category = input()
url_MOOC = f"https://www.icourse163.org/search.htm?search={category}#/"
driver.get(url_MOOC)

course_names = driver.find_elements(By.XPATH, '//span[@class=" u-course-name f-thide"]')
course_name_list = list()
for name in course_names:
    course_name_list.append(name.text)

course_links = driver.find_elements(By.XPATH, '//div[@class="cnt f-pr"]/a[@href]')
course_link_list = list()
for link in course_links:
    if link.get_attribute('href')[0] == '/':
        course_link_list.append(link.get_attribute('href')[2:])
    else:
        course_link_list.append(link.get_attribute('href'))

# course_intros = driver.find_elements(By.XPATH, '//span[@class="p5 brief f-ib f-f0 f-cb"]')
# course_intro_list = list()
# for intro in course_intros:
#     course_intro_list.append(intro.text)

course_info_list = zip(course_name_list, course_link_list)
for info in course_info_list:
    print(info)

# class CourseSpider:
#     def __init__(self, category):
#         self._category = category
#         self._options = Options()
#         self._options.add_argument('--headless')
#         self._driver = webdriver.Chrome(options=options)
#
#     def crape_name(self):
#         print("No Implementation(name)")
#
#     def crape_link(self):
#         print("No Implementation(link)")
#
#     def crape_intro(self):
#         print("No Implementation(intro)")
#
#
# # MOOC -
# class MOOCSpider(CourseSpider):
#     def __init__(self, category):
#         super(category)
#         self._url = f"https://www.icourse163.org/search.htm?search={category}#/"
#         self._driver.get(self._url)
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "j-side-operation")))
#         self._html_MOOC = self._driver.page_source
#         self._root_MOOC = etree.HTML(self._html_MOOC)
#
#     def crape_name(self):
#         pass
#
#     def crape_link(self):
#         pass
#
#     def crape_intro(self):
#         pass

# ---------------------------------------------------------------------
# iMOOC -
# from lxml import etree
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# options = Options()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)
#
# category = input()
# url_iMOOC = f"https://www.imooc.com/search/?words={category}"
# driver.get(url_iMOOC)
#
# wait = WebDriverWait(driver, 10)
# target_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "js-page-last")))
#
# html_iMOOC = driver.page_source
# print(html_iMOOC)

# ----------------------------------------------------------------------
# iCourse

# -----------------------------------------------------------------------
# HaoDaXue -
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# options = Options()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)
#
# category = input()
# url_HaoDaXue = f"https://www.cnmooc.org/portal/frontCourseIndex/course.mooc?k={category}"
# driver.get(url_HaoDaXue)
#
# html_HaoDaXue = driver.page_source
# print(html_HaoDaXue)

# ------------------------------------------------------------------------
# BiliBili
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# options = Options()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)
#
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# category = input()
# url_BiliBili = f"https://search.bilibili.com/all?keyword={category}"
# driver.get(url_BiliBili)
#
# wait = WebDriverWait(driver, 10)
# target_element = wait.until(EC.presence_of_element_located((By.ID, "biliMainFooter")))
#
# html_BiliBili = driver.page_source
# print(html_BiliBili)
