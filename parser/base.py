#!/usr/bin/env python3

"""
Goods Parser: parent class for every parser
"""

import logging
from bs4 import BeautifulSoup
from typing import Any, Dict, List, Optional
from webdriver import create_webdriver

import goods_parser.config as config

class BaseParser:
    """ Basic parser with common logic """

    def __init__(self, _driver, name, shop_url, table_name) -> None:
        self.products_list = list()
        self._driver = create_webdriver()
        self.delay = config.delay
        self.scroll_delay = config.scroll_delay
        self.name = name
        self.shop_url = config.shops[self.name]['url']
        self.table_name = table_name

    def fill_products_list(self, cat_lnk, card_c, name_c, price_c, oprice_c, href_c) -> bool:
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        products = soup.find_all(class_=card_c)

        logging.info("[+] We've got {} products from {}".format(len(products), product_category))

        for product in products:

            name = product.find(class_=title_c).text

            try:
                price = float(product.find(class_=price_c).text[:-4])
            except AttributeError:
                logging.warn("[!!!] Product {} has no price, returning...".format(name))
                price = None
                return False

            try:
                old_price = float(product.find(class_=oprice_c).text[:-4])
                profit = int(100 - price * 100 / old_price)
            except AttributeError:
                old_price = None
                profit = None

            lnk = product[href_c]
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
        logging.info("[+] Opening {} site...".format(cat_lnk))
        self._driver.get(cat_lnk)
        sleep(self.delay)

        height = 0
        page_height = self._driver.execute_script("return document.documentElement.scrollHeight")
        logging.info("[+] Scrolling to the end of the page...")

        while height < page_height:
            page_height = self._driver.execute_script("return document.documentElement.scrollHeight")
            logging.info("[.] Page Height = {}".format(page_height))
            sleep(self.scroll_delay)
            height += 200
            self._driver.execute_script("window.scrollTo(0, {})".format(height))
            logging.info("[.] Height = {}".format(height))

        logging.info("[+] Page source code is ready")

        if self.fill_products_list(product_category=cat_lnk):
            self.save_to_db()
            return True
        else:
            return False

    def parse_category(self, cat_lnk, num_c) -> None:
        self._driver.get(cat_lnk)
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        try:
            num_pages = int(soup.find(class_=num_c).text)
        except Exception:
            num_pages = 5
        for page in range(num_pages):  # number of pages to parse
            if not self.parse_page(cat_lnk + "?page={}".format(page + 1)):
                break

    def save_to_db(self) -> None:
        cursor = dbcursor.DBCursor()
        for product in self.products_list:
            cursor.append_product(self.table_name, product)
        self.products_list.clear()

    def run(self) -> None:
        pass
