import sqlite3

# function that adds product information using parameterized query
def add_product(name, price, category):
    with sqlite3.connect("july_learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (name, price, category) VALUES (?, ?, ?)',(name, price, category))

add_product('orange_juice', 50, 'fruits')

# function that reyurns all products in a particular category as a list of tuples
def get_by_category(category):
    with sqlite3.connect("july_learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE category = ?', (category,))
        rows = cursor.fetchall()
    return rows

products = get_by_category('fruits')
for product in products:
    print(product)
    print("-------\n")

# function that returns all products above a given price, and sorted by desc price
def get_expensive(min_price):
    with sqlite3.connect("july_learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE price > ? ORDER BY price DESC', (min_price,))
        rows = cursor.fetchall()
    return rows
products = get_expensive(51)
print(products)