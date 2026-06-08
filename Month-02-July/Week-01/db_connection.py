import sqlite3

# connect to the database
conn = sqlite3.connect("july_learning.db")
cursor = conn.cursor()

# Create a table if it dosent exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL,
        category TEXT
    )
""")
conn.commit()

# Insert a row safely with parameterised query
product = ('Laptop', 999.99, 'Electronics')
cursor.execute('INSERT INTO products (name, price, category) VALUES (?, ?, ?)', product)
conn.commit()

#Query and fetch results
cursor.execute('Select * FROM products')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Adding a fetch_one function
cursor.execute('SELECT * FROM products WHERE category = ?', ('Electronics',))
row = cursor.fetchone()
print('First match:', row)

#close the connection
conn.close()