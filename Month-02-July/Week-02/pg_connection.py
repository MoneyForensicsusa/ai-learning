import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

cursor = conn.cursor()

cursor.execute(
    'INSERT INTO customers (email, name, city) VALUES (%s, %s, %s)',
    ('alicia@gmail.com', 'Alicia', 'New York')
)
conn.commit()

cursor.execute(
    'SELECT id, name, city FROM customers WHERE city = %s', ('New York',))
rows = cursor.fetchall()
for row in rows:
    print(f'ID: {row[0]}, Name: {row[1]}, City: {row[2]}')

conn.close()
