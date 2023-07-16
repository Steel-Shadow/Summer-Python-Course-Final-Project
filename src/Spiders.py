from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.websites import icourses, bilibili, netease, cmooc


class Spiders:
    __options = Options()
    __options.add_argument('--headless')

    # 浏览器驱动
    driver = webdriver.Chrome(options=__options)
    # 网页 -> 抓取函数
    websites_scraping = {
        'icourses': icourses.scraping,
        'bilibili': bilibili.scraping,
        'netease ': netease.scraping,
        'cmooc': cmooc.scraping
    }

    @classmethod
    def scraping(cls, site: str, course: str):
        scraping = cls.websites_scraping.get(site)
        scraping(cls.driver, course)

    @classmethod
    def driver_close(cls):
        cls.driver.close()


if __name__ == '__main__':
    for i in Spiders.websites_scraping:
        Spiders.scraping(i, '操作系统')
        print('----------')
