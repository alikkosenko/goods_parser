#!/usr/bin/env python3

'''
WebDriver: simple class for webdriver
'''

import logging

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# chromedriver_py
from chromedriver_py import binary_path


logging.basicConfig(format='[+]%(asctime)s - %(message)s', level=logging.INFO)


def create_webdriver():
    logging.info('Creating webdriver')
    options = Options() # Settings for Chromedriver
    options.add_argument("--window-size=1440,1500")
    #options.add_argument("--headless")
    service = webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(options=options, service=service) # создания драйвера Chrome
    driver.implicitly_wait(20)
    return driver
