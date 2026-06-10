import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def get_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn


def get_customer_orders(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT customers.name, products.name, orders.quantity
        FROM orders
        INNER JOIN customers ON orders.customer_id = customers.id
        INNER JOIN products ON orders.product_id = products.id
        WHERE orders.customer_id = %s''',
        (customer_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
orders = get_customer_orders(2)
for order in orders:
    print(f'Customer: {order[0]}, Product: {order[1]}, Quantity: {order[2]}')

