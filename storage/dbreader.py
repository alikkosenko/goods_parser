import sqlite3 


conn = sqlite3.connect("products.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM Silpo_table")
print(cursor.fetchall())
"""


cursor.execute("DELETE FROM Silpo_table;")
conn.commit()
"""
