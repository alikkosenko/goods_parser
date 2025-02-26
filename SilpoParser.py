#!/usr/bin/env python3

'''
SilpoParser
'''

import logging
from SilpoCrawler import SilpoCrawler, stocks_url

goods_info_dict = {
    "beer": {"units-postfix": "л"}
}


beer_url = "https://shop.silpo.ua/all-offers?filter_CATEGORY=(38)&to=3&from=1"


if __name__ == "__main__":
    parser = SilpoCrawler(delay=10)
    while True:
        print("Выбери действие:\n 0 - ВЫХОД\n 1 - Обновить базу данных\n 2 - Вывести базу данных")
        action_num = int(input("Действие:"))
        if action_num == 0:
            break
        elif action_num == 1:
            parser.parse_products_info(beer_url)
            parser.create_products_dict()
        elif action_num == 2:
            parser.sort()
        else:
            break


#parser.retrieve("profit_parse.json")
#parser.parse_products_info(beer_url)
#parser.create_products_dict()
#parser.save_to_file("beer_parse.json")
#parser.sort()

