#!/usr/bin/env python3

"""
Goods Parser: parent class for every parser
"""

import logging


class ProductParser:

    def __init__(self, delay, scroll_delay) -> None:
        self.products_list = list()
        self.delay = delay
        self.scroll_delay = scroll_delay

    def fill_products_list(self, cat_lnk, card_c, name_c, title_c, price_c, oprice_c) -> bool:
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        products = soup.find_all(class_='product-card')

        logging.info("[+] We've got {} products from {}".format(len(products), product_category))

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

    def save_to_db(self) -> None:
        pass

    def sort(self) -> None:
        pass

    def parse_page(self, cat_lnk) -> None:
        pass

    def parse_category(self, cat_lnk) -> None:
        pass


    def parse(self) -> None:
        pass
