from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def init_driver():
    options = Options()

    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 禁用图片显示
    prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
    options.add_experimental_option("prefs", prefs)

    return webdriver.Chrome(options=options)
