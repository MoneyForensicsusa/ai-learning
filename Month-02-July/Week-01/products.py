import sqlite3

# function that adds product information using parameterized query
def add_product(name, price, category):
    conn = sqlite3.connect('july_learning.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO products (name, price, category) VALUES (?, ?, ?)',(name, price, category))
    conn.commit()
    conn.close()
add_product('orange_juice', 50, 'fruits')
