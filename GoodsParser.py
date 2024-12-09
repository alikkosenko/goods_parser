#!/usr/bin/python3


import config

# Стандартные библиотеки
import logging
import json
from time import sleep, time
# Бибилиотека bs4
from bs4 import BeautifulSoup
# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Настройка logging
logging.basicConfig(format='[+]%(asctime)s - %(message)s', level=logging.INFO)
logging.basicConfig(format='[!]%(asctime)s - %(message)s', level=logging.WARNING)


stocks_url = "https://shop.silpo.ua/all-offers?to=1&from=1"


def create_webdriver():
    logging.info('Creating webdriver')
    # настройка драйвера Chrome
    options = Options()
    options.add_argument("--window-size=1440,900")
    options.headless = config.HEADLESS
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(options=options, service=service) # создания драйвера Chrome
    driver.implicitly_wait(20)
    return driver # возвращает экземпляр webdriver


class GoodsParser:

    def __init__(self, delay=2, scroll_delay=0.2) -> None:

        self.products_dict = dict()         # Словарь со всеми найденными товарами
        self.delay = delay                  # Задержка перед началом парсинга
        self.scroll_delay = scroll_delay    # Задержка при скроллинге страницы
        self._driver = None                 # Драйвер браузера

    def create_products_dict(self) -> None:
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        products = soup.find_all(class_='product-card')

        logging.info("[+] We've got {} products".format(len(products)))

        good_id = 0

        for product in products:

            name = product.find(class_="product-card__title").text

            try:
                price = float(product.find(class_="ft-whitespace-nowrap ft-text-22 ft-font-bold").text[:-4])
            except AttributeError:
                price = None

            try:
                old_price = float(product.find(class_="ft-line-through ft-text-black-87 ft-typo-14-regular xl:ft-typo").text[:-4])
                profit = int(100 - price * 100 / old_price)
            except AttributeError:
                old_price = None
                profit = None

            weight = product.find(class_="ft-typo-14-semibold xl:ft-typo-16-semibold").text
            link = product["href"]
            picture = product.find("img")['src']

            self.products_dict[good_id] = dict(name=str(name),
                                               link="https://shop.silpo.ua" + link,
                                               picture=picture,
                                               price=price,
                                               old_price=old_price,
                                               profit=profit,
                                               weight=weight)
            good_id += 1

        logging.info("Products dictionary is ready")

    def parse_products_info(self, category_url) -> None:
        self._driver = create_webdriver()

        logging.info("Opening {} site...".format(category_url))
        self._driver.get(category_url)

        sleep(self.delay)

        height = 0
        page_height = self._driver.execute_script("return document.documentElement.scrollHeight")
        logging.info("Scrolling to the end of the page...")

        while height < page_height:
            page_height = self._driver.execute_script("return document.documentElement.scrollHeight")
            logging.info("Page Height = {}".format(page_height))
            sleep(self.scroll_delay)
            height += 200
            self._driver.execute_script("window.scrollTo(0, {})".format(height))
            logging.info("Height = {}".format(height))

#        try:
#           WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME,
#                                                                                    "pagination-link next disabled")))
#        except Exception as e:
#            print(e)

        logging.info("Site source code is ready")

    def parse_product_picture_url(self, URL) -> str:
        self._driver.get(URL)
        sleep(1)
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        img_url = soup.find(class_="slide selected previous").find("img").get("src")

        return img_url

    def save_to_file(self, filename="parse.json") -> None:
        if self.products_dict:
            products_json = json.dumps(self.products_dict, indent=4, ensure_ascii=False)
            with open(filename, "w", encoding="UTF-8") as f:
                f.write(products_json)
            logging.info("Saved products dictionary to {}".format(filename))
        else:
            logging.warning("Nothing to save to {}".format(filename))

    def retrieve(self, filename="parse.json") -> None:
        if not self.products_dict:
            with open(filename, encoding="UTF-8") as f:
                products_json = json.load(f)
                self.products_dict = dict(products_json)
        else:
            logging.warning("You already have loaded products")

    def sort(self) -> None:
        if self.products_dict:
            new_products_dict = dict(reversed(sorted(self.products_dict.items(),
                                                     key=lambda item: item[1]["profit"] if item[1]["profit"] else 0)))
            for good in new_products_dict.items():
                print(good)
        else:
            logging.warning("Cant sort empty dictionary")


if __name__ == "__main__":
    start = time()

    parser = GoodsParser()
    parser.parse_products_info(stocks_url)
    parser.create_products_dict()
    parser.save_to_file()

    end = time()
    t = end-start
    print("Script worked for {} seconds".format(int(t)))
