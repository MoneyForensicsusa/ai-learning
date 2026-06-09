-- Good design: seperate tables for seperate things
CREATE TABLE customers (
id SERIAL PRIMARY KEY,
email TEXT UNIQUE NOT NULL,
name TEXT NOT NULL,
city TEXT,
created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
price DECIMAL(10,2) NOT NULL,
stock INTEGER DEFAULT 0
);

CREATE TABLE orders (
id SERIAL PRIMARY KEY,
customer_id INTEGER REFERENCES customers(id),
product_id INTEGER REFERENCES products(id),
quantity INTEGER NOT NULL,
ordered_at TIMESTAMP DEFAULT NOW()
);

-- insert test data
INSERT INTO customers (email, name, city) VALUES ('wonderfuleyeh25@gmail.com', 'Wonderful', 'Austin');
INSERT INTO products (name, price, stock) VALUES ('Laptop', 999.9, 10);
INSERT INTO orders (customer_id, product_id, quantity) VALUES (1, 1, 2);

SELECT * FROM orders;

INSERT INTO orders (customer_id, product_id, quantity) VALUES (999, 1, 1);

-- Create a reviews table
CREATE TABLE reviews (
id SERIAL PRIMARY KEY,
customer_id INTEGER REFERENCES customers(id),
product_id INTEGER REFERENCES products(id),
rating INTEGER,
comment TEXT,
created_at TIMESTAMP DEFAULT NOW()
);

SELECT * FROM reviews

INSERT INTO reviews (customer_id, product_id, rating, comment) VALUES (1, 1, 10, 'This is really good');

SELECT customers.name AS "Customer name", products.name AS "Product name", orders.quantity, orders.ordered_at FROM orders INNER JOIN customers ON customers.id = orders.customer_id
INNER JOIN products ON products.id = orders.product_id; 

INSERT INTO customers (email, name, city) VALUES ('w.eyeh@alineds.com', 'Wonder', 'Houston');
INSERT INTO products (name, price, stock) VALUES ('Iphone', 1200, 52);
INSERT INTO orders (customer_id, product_id, quantity) VALUES (2, 2, 1);
INSERT INTO reviews (customer_id, product_id, rating, comment) VALUES (2, 2, 6, 'This is good');

ALTER TABLE reviews ADD CONSTRAINT valid_rtaing
CHECK (rating >= 1 AND rating <= 5);

UPDATE reviews 
SET rating = 5 WHERE rating = 6;

ALTER TABLE reviews ADD CONSTRAINT valid_rating
CHECK (rating >= 1 AND rating <= 5);

UPDATE reviews
SET rating = 4 WHERE rating = 10;

ALTER TABLE reviews ADD CONSTRAINT valid_rating
CHECK (rating >= 1 AND rating <=5);

SELECT * FROM reviews ORDER BY id ASC;

