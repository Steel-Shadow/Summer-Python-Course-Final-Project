from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

category = input()
url_iMOOC = f"https://www.imooc.com/search/?words={category}"
driver.get(url_iMOOC)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div[3]/div[1]/div[3]")))
course_links = driver.find_elements(By.XPATH, '//a[@class="js-zhuge-allResult item-title js-result-item js-item-title "]')

course_link_list = list()
course_name_list = list()

for link in course_links:
    course_link_list.append(link.get_attribute('href'))
    course_name_list.append(link.text)

driver.close()

course_info_list = zip(course_name_list, course_link_list)
for info in course_info_list:
    print(info)

    # print(link.get_attribute('href') + " before click")
    # link.click()
    # driver.switch_to.window(driver.window_handles[-1])
    #
    # course_name = driver.find_elements(By.XPATH, '//div[@class="hd clearfix"]/h2')
    # course_intro = driver.find_elements(By.XPATH, '//div[@class="course-description course-wrap"]')
    # if len(course_name) == 0:
    #     course_name = driver.find_elements(By.XPATH, '//div[@class="title-box"]/h1')
    #     course_intro = driver.find_elements(By.XPATH, '//div[@class="title-box"]/h2')
    #     if len(course_intro) == 0:
    #         course_intro = driver.find_elements(By.XPATH, '//div[@class="content-box clearfix"]/h1')
    #     if len(course_name) == 0:
    #         course_name = driver.find_elements(By.XPATH, '//div[@class="header-box"]/h1')
    #         course_intro = driver.find_elements(By.XPATH, '//div[@class="header-box"]/h4')
    #         if len(course_name) == 0:
    #             course_name = driver.find_elements(By.XPATH, '//div[@class="title "]/span')
    #             course_intro = driver.find_elements(By.XPATH, '//div[@class="desc sem-need-hide"]')
    # if len(course_name) != 0:
    #     course_name_list.append(course_name[0].text)
    #     if len(course_intro) == 0:
    #         # print(driver.current_url + "  -----------------------------------------------------")
    #         course_intro_list.append('')
    #     else:
    #         course_intro_list.append(course_intro[0].text)
    # # print(test_tag[0].text)
    # # print('--------------------------------------------------------------------------------------------------------')
    #
    # driver.switch_to.window(driver.window_handles[0])



