#!/usr/bin/python3

#silpo.py

# Standard library
import logging
import json
import os
from dataclasses import asdict
from time import sleep, time
import re

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# my own modules
from goods_parser.config import Product, ProductCategory, shops
from base import ProductParser
from webdriver import create_webdriver
import goods_parser.storage.dbcursor as dbcursor


# Настройка logging
logging.basicConfig(format='[+]%(asctime)s - %(message)s', level=logging.INFO)
logging.basicConfig(format='[!]%(asctime)s - %(message)s', level=logging.WARNING)

stocks_url = "https://shop.silpo.ua/all-offers?to=1&from=1"


class SilpoCrawler(ProductParser):

    def __init__(self, delay=2, scroll_delay=0.2) -> None:
        super().__init__(delay, scroll_delay)
        self.name = "Silpo"
        self.shop_lnk = shops[self.name]
        self.categories_list = list()
        self._driver = create_webdriver()
        self.table_name = "Silpo_table"

    def save_to_db(self) -> None:
        print(self.products_list)
        cursor = dbcursor.DBCursor()
        for product in self.products_list:
            cursor.append_product(self.table_name, product)
        self.products_list.clear()

    def fill_products_list(self, product_category) -> bool:
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        products = soup.find_all(class_='product-card')

        logging.info("[+] We've got {} products".format(len(products)))

        for product in products:

            name = product.find(class_="product-card__title").text

            try:
                price = float(product.find(class_="product-card-price__displayPrice").text[:-4])
            except AttributeError:
                price = None
                return False

            try:
                old_price = float(product.find(class_="product-card-price__displayOldPrice").text[:-4])
                profit = int(100 - price * 100 / old_price)
            except AttributeError:
                old_price = None
                profit = None

            lnk = product["href"]
            picture_lnk = product.find("img")['src']

            self.products_list.append(Product(
                product_type=product_category,
                name=str(name),
                lnk=self.shop_lnk + lnk,
                picture_lnk=picture_lnk,
                price=price,
                old_price=old_price,
                profit=profit,
            )
            )

        logging.info("Products list is ready")
        return True

    def parse_page(self, cat_lnk) -> bool:
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

        if self.fill_products_list(product_category=cat_lnk):
            self.save_to_db()
            return True
        else:
            return False

    def parse_category(self, cat_lnk) -> None:
        self._driver.get(cat_lnk)
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        try:
            num_pages = int(soup.find(class_="pagination-item ng-star-inserted").text)
        except Exception:
            num_pages = 5
        for page in range(num_pages):  # number of pages to parse
            if not self.parse_page(cat_lnk + "?page={}".format(page + 1)):
                break

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
                    cat_id=id,
                    cat_lnk=self.shop_lnk + category["href"]
                )
            )
            id += 1

    def parse(self) -> None:
        self.parse_categories()
        for category in self.categories_list:
            self.parse_category(category.cat_lnk)


if __name__ == "__main__":
    SilpoCrawler().parse()
