#!/usr/bin/env python3

'''
Goods Parser: parent class for every parser
'''


class ProductParser:

    def __init__(self, delay, scroll_delay) -> None:
        self.products_list = list()
        self.delay = delay
        self.scroll_delay = scroll_delay

    def fill_products_list(self, product_category:str) -> None:
       pass

    def save_to_db(self) -> None:
        pass

    def retrieve_from_db(self) -> None:
        pass

    def sort(self) -> None:
        pass

    def parse_page(self, cat_lnk):
        pass

    def parse_category(self, cat_lnk) -> None:
        pass

    def parse_categories(self):
        pass

    def parse(self) -> None:
        pass