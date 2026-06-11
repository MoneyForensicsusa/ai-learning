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
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    SELECT customers.name, products.name, orders.quantity
                    FROM orders
                    INNER JOIN customers ON orders.customer_id = customers.id
                    INNER JOIN products ON orders.product_id = products.id
                    WHERE orders.customer_id = %s''',
                    (customer_id,)
                )
                rows = cursor.fetchall()
        return rows
    except psycopg2.OperationalError:
        print(f"Cannot connect to database: {e}")
        return[]

    
orders = get_customer_orders(2)
for order in orders:
    print(f'Customer: {order[0]}, Product: {order[1]}, Quantity: {order[2]}')

def add_order(customer_id, product_id, quantity):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO orders (customer_id, product_id, quantity)
                    VALUES (%s, %s, %s)
                    RETURNING id''',
                    (customer_id, product_id, quantity))
                new_id = cursor.fetchone()[0]
                conn.commit()
        return new_id
    except psycopg2.OperationalError:
        print(f"Cannot connect to database: {e}")
        return None
new_id = add_order(2, 1, 5)
print(new_id)