# prepare_db.py
import sqlite3
conn = sqlite3.connect("sample.db")
c = conn.cursor()
c.executescript("""
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;

CREATE TABLE customers(
  id INTEGER PRIMARY KEY,
  name TEXT,
  country TEXT,
  signup_date DATE
);

CREATE TABLE orders(
  id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  amount REAL,
  order_date DATE,
  FOREIGN KEY(customer_id) REFERENCES customers(id)
);

INSERT INTO customers(name, country, signup_date) VALUES
('Rahul','India','2024-03-01'),
('Sneha','India','2024-02-10'),
('Zara','UK','2024-05-12');

INSERT INTO orders(customer_id, amount, order_date) VALUES
(1, 120.50, '2024-03-12'),
(2, 75.00, '2024-04-05'),
(1, 200.00, '2024-10-10');
""")
conn.commit()
conn.close()
print("sample.db prepared.")
