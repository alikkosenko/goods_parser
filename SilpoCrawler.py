#!/usr/bin/python3

# Стандартные библиотеки
import logging
import json
import os
from dataclasses import asdict
from time import sleep, time

from ansible_collections.community.general.plugins.module_utils.net_tools.pritunl.api import pritunl_auth_request
# Бибилиотека bs4
from bs4 import BeautifulSoup
# my own modules
from config import Product, ProductCategory
from ProductParser import ProductParser
from WebDriver import create_webdriver
import DBCursor

from selenium.webdriver.common.by import By

# Настройка logging
logging.basicConfig(format='[+]%(asctime)s - %(message)s', level=logging.INFO)
logging.basicConfig(format='[!]%(asctime)s - %(message)s', level=logging.WARNING)


stocks_url = "https://shop.silpo.ua/all-offers?to=1&from=1"


class SilpoCrawler(ProductParser):

    def __init__(self, delay=2, scroll_delay=0.2) -> None:
        super().__init__(delay, scroll_delay)
        self.shop_lnk = "https://shop.silpo.ua"
        self.categories_list = list()
        self._driver = create_webdriver()

    def fill_products_list(self, product_category) -> None:
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        products = soup.find_all(class_='product-card')

        logging.info("[+] We've got {} products".format(len(products)))

        for product in products:

            name = product.find(class_="product-card__title").text

            try:
                price = float(product.find(class_="product-card-price__displayPrice").text[:-4])
            except AttributeError:
                price = None

            try:
                old_price = float(product.find(class_="product-card-price__displayOldPrice").text[:-4])
                profit = int(100 - price * 100 / old_price)
            except AttributeError:
                old_price = None
                profit = None

            weight = product.find(class_="ft-typo-14-semibold xl:ft-typo-16-semibold").text
            lnk = product["href"]
            picture_lnk = product.find("img")['src']

            self.products_list.append(Product(
                product_type = product_category,
                name         = str(name),
                lnk          = self.shop_lnk + lnk,
                picture_lnk  = picture_lnk,
                price        = price,
                old_price    = old_price,
                profit       = profit,
                weight       = weight
            )
            )

        logging.info("Products list is ready")

    def parse_page(self, cat_lnk) -> None:
        logging.info("Opening {} site...".format(cat_lnk))
        self._driver.get(cat_lnk)
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

        logging.info("Page source code is ready")

        self.fill_products_list(product_category=cat_lnk)

        
    def parse_category(self, cat_lnk) -> None:
        self._driver.get(cat_lnk)
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        try:
            num_pages = int(soup.find(class_="pagination-item ng-star-inserted").text)
        except Exception:
            num_pages = 5
        for page in range(2) if num_pages > 5 else range(1): # number of pages to parse
            self.parse_page(cat_lnk + "?page={}".format(page + 1))
        self.save_to_db()
                

    def save_to_file(self, filename="parse.json") -> None:
        if self.products_list:
            for product in self.products_list:
                with open(filename, "a+", encoding="UTF-8") as f:
                    json.dump(asdict(product), f, indent=4, ensure_ascii=False)
            logging.info("Saved products dictionary to {}".format(filename))
        else:
            logging.warning("Nothing to save to {}".format(filename))

        self.products_list.clear()

    def retrieve(self, filename="parse.json") -> None:
        for filename in list(os.listdir()):
            if filename[-4:] == "json":
                with open(filename, "r", encoding="UTF-8") as f:
                    data = json.load(f)
                    self.products_list.append(Product(**data))

    def save_to_db(self) -> None:
        for product in self.products_list:
            DBCursor.append_product(product)

    def parse_categories(self):
        self._driver.get(self.shop_lnk)
        sleep(self.delay)
        self._driver.find_element(By.ID, "category-menu-button").click()
        sleep(self.delay)
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        menu = soup.find_all(class_="menu-categories__link")
        for category in menu:
            id = 0
            self.categories_list.append(
                ProductCategory(
                    cat_id  = id,
                    cat_lnk = self.shop_lnk + category["href"]
                )
            )
            id += 1



    def parse(self) -> None:
        self.parse_categories()
        for category in self.categories_list:
            self.parse_category(category.cat_lnk)



if __name__ == "__main__":
    SilpoCrawler().parse()
