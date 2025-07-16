import sqlite3
from datetime import datetime

def add_product(name, quantity, price):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
              (name, quantity, price))
    conn.commit()
    conn.close()

def edit_product(product_id, name, quantity, price):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("UPDATE products SET name=?, quantity=?, price=? WHERE id=?",
              (name, quantity, price, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return products

def get_low_stock(threshold=5):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE quantity <= ?", (threshold,))
    items = c.fetchall()
    conn.close()
    return items

def record_sale(product_id, quantity_sold):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?",
              (quantity_sold, product_id))
    c.execute("INSERT INTO sales (product_id, quantity_sold, sale_date) VALUES (?, ?, ?)",
              (product_id, quantity_sold, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_sales_summary():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute('''SELECT products.name, SUM(sales.quantity_sold), 
                 SUM(sales.quantity_sold * products.price)
                 FROM sales JOIN products ON sales.product_id = products.id
                 GROUP BY sales.product_id''')
    summary = c.fetchall()
    conn.close()
    return summary
