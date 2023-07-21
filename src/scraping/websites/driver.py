from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


def init_driver() -> WebDriver:
    options = Options()
    # 无头
    options.add_argument('--headless')
    # 禁用图片显示
    prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
    options.add_experimental_option("prefs", prefs)

    return webdriver.Chrome(options=options)
