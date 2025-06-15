import logging
import json
import os
from dataclasses import asdict
from time import sleep, time

# Бибилиотека bs4
from bs4 import BeautifulSoup

import config
# my own modules
from config import Product, ProductCategory
from ProductParser import ProductParser
from WebDriver import create_webdriver
import DBCursor

from selenium.webdriver.common.by import By

economy_link = "https://www.atbmarket.com/catalog/388-aktsiya-7-dniv"


class ATBCrawler(ProductParser):
    def __init__(self, delay=2, scroll_delay=0.2) -> None:
        super().__init__(delay, scroll_delay)
        self.name = "ATB"
        self.shop_lnk = config.shops[self.name]
        self.categories_list = list()
        self._driver = create_webdriver()
        self.table_name = "Atb_table"

    def save_to_db(self) -> None:
        print(self.products_list)
        cursor = DBCursor.DBCursor()
        for product in self.products_list:
            cursor.append_product(self.table_name, product)
        self.products_list.clear()

    def fill_products_list(self, product_category) -> None:
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        products = soup.find_all("article", class_=["catalog-item", "js-product-container"])

        logging.info("[+] We've got {} products".format(len(products)))

        for product in products:

            name = product.find(class_="catalog-item__info").text

            try:
                price = float(product.find(class_="product-price__top")['value'])
            except AttributeError:
                price = None

            try:
                old_price = float(product.find(class_="product-price__bottom")['value'])
                profit = int(100 - price * 100 / old_price)
            except (AttributeError, ValueError, TypeError):
                old_price = None
                profit = None

            lnk = product.find(class_="catalog-item__photo-link")['href']
            picture_lnk = lnk

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
        self.save_to_db()

    def parse_category(self, cat_lnk) -> None:
        self._driver.get(cat_lnk)
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        try:
            btns = soup.find_all("li", class_=["product-pagination__item"])
            print(btns)
            nums = list()
            for btn in btns:
                nums.append(btn.find(class_="product-pagination__link").text)
                print(nums)
            num_pages = int(max(nums))
            print("I am her and num of pages is {}".format(num_pages))
        except Exception as e:
            num_pages = 6
            print(e)
        for page in range(num_pages):  # number of pages to parse
            print(num_pages)
            self.parse_page(cat_lnk + "?page={}".format(page + 1))

    def parse_categories(self):
        self._driver.get(self.shop_lnk)
        sleep(self.delay)
        self._driver.find_element(By.CLASS_NAME, "catalog-button--store.catalog-button").click()
        sleep(self.delay)
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        menu = soup.find_all(class_="category-menu__link-wrap")
        for category in menu:
            id = 0
            print(category)
            self.categories_list.append(
                ProductCategory(
                    cat_id=id,
                    cat_lnk=self.shop_lnk + category["href"]
                )
            )
            id += 1

    def parse(self) -> None:
        for c in config.categories:
            self.parse_category(c["ATB"])


if __name__ == "__main__":
    ATBCrawler().parse()
