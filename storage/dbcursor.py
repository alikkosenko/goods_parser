#!/usr/bin/env python3

import sqlite3

from config import Product
import re


class DBCursor:

    def __init__(self) -> None:
        self.conn = sqlite3.connect("products.db")
        self.cursor = self.conn.cursor()

    def create_table(self, table_name="Products") -> None:
        self.cursor.execute(
            """
            CREATE TABLE {}(
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_type VARCHAR,
                name VARCHAR,
                price FLOAT,
                old_price FLOAT,
                profit INTEGER,
                lnk VARCHAR,
                picture_lnk VARCHAR
            )
        """.format(table_name)
        )

        self.conn.commit()

    def receive_products(self, table_name, product_type=None) -> list[Product]:
        """
        :param table_name:
        :param product_type:
        :return:
        """
        """
        Написать отдельное формирование строки запроса в зависимости от 
        получаемых (или не получаемых) аргументов метода.
        """
        self.cursor.execute(f'''
            SELECT * FROM {table_name} WHERE product_type == {product_type};
        ''' if product_type else f'''SELECT * FROM {table_name};''')
        data = self.cursor.fetchall()
        products = [Product(*item[1:]) for item in data]
        return products

    def append_product(self, table_name, product):
        self.cursor.execute('''INSERT INTO {}( 
                    product_type, 
                    name, 
                    price, 
                    old_price, 
                    profit, 
                    lnk, 
                    )
                    VALUES 
                    (
                    ?,?,?,?,?,?
                    )'''.format(table_name), tuple(product.__dict__.values()))
        self.conn.commit()


if __name__ == "__main__":
    conn = DBCursor()
    conn.create_table("Silpo_table")
    conn.create_table("ATB_table")
    p = re.compile("^\n+|\n+$")
    for i in conn.receive_products(table_name="Atb_table"):
        print(re.sub(r"^\n+|\n+$|\n+Закінчується", "", i.name))
