#!/usr/bin/env python3

import sqlite3

from config import Product




class DBCursor:

    def __init__(self):
        self.conn = sqlite3.connect("products.db")
        self.cursor = self.conn.cursor()

    def create_db(self):
        self.cursor.execute(
        """
            CREATE TABLE Products(
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_type VARCHAR,
                name VARCHAR,
                price FLOAT,
                old_price FLOAT,
                profit INTEGER,
                weight VARCHAR,
                lnk VARCHAR,
                picture_lnk VARCHAR
            )
        """
        )

        self.conn.commit()

    def receive_products(self):
        self.cursor.execute('''
            SELECT * FROM Products WHERE product_type == ?;
        ''', ("https://silpo.ua/category/pyvo-4503?page=1",))
        data = self.cursor.fetchall()
        products = [Product(*item) for item in data]
        return products

    def append_product(self, product):
        self.cursor.execute('''INSERT INTO Products( 
                    product_type, 
                    name, 
                    price, 
                    old_price, 
                    profit, 
                    weight, 
                    lnk, 
                    picture_lnk
                    )
                    VALUES 
                    (
                    ?,?,?,?,?,?,?,?
                    )''', tuple(product.__dict__.values()))
        self.conn.commit()



#if __name__ == "__main__":
    #receive_products()
