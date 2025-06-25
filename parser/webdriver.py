#!/usr/bin/env python3

"""
WebDriver: simple class for webdriver
"""

import logging

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# chromedriver_py
from chromedriver_py import binary_path
import undetected_chromedriver as uc

import goods_parser.config as config
from time import sleep
logging.basicConfig(format='[+]%(asctime)s - %(message)s', level=logging.INFO)


def create_webdriver():
    logging.info('Creating webdriver')

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    """
    if config.HEADLESS:
        options.add_argument("--headless")
    """
    options.add_argument("--window-size=1440,1500")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/131.0.0.0 Safari/537.36')


    #service = webdriver.ChromeService(executable_path=binary_path)
    #driver = uc.Chrome(version_main=131, options=options, service=service)  # Creating Chrome driver
    driver = uc.Chrome(version_main=131, options=options)  # Creating Chrome driver
    driver.implicitly_wait(20)
    return driver


if __name__ == "__main__":
    driver = create_webdriver()
    driver.get("https://silpo.ua/category/pyvo-4503")
    sleep(20)
