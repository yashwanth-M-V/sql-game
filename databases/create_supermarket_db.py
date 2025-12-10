import sqlite3

DB_NAME = "supermarket.db"

# Connect and enable foreign keys
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

print("Rebuilding supermarket.db ...")

# =========================
# DROP TABLES
# =========================

tables = [
    "payments", "bill_items", "bills", "cart_items", "carts",
    "purchase_order_items", "purchase_orders", "inventory",
    "products", "categories", "suppliers", "customers", "employees"
]

for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table};")

# =========================
# CREATE TABLES
# =========================

cursor.executescript("""

CREATE TABLE categories (
    category_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name   TEXT NOT NULL
);

CREATE TABLE products (
    product_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name    TEXT NOT NULL,
    category_id     INTEGER,
    price           REAL,
    cost_price      REAL,
    barcode         TEXT,
    unit            TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE inventory (
    inventory_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id          INTEGER NOT NULL,
    quantity_in_stock   INTEGER DEFAULT 0,
    reorder_level       INTEGER DEFAULT 0,
    last_updated        TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE suppliers (
    supplier_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name   TEXT NOT NULL,
    contact         TEXT
);

CREATE TABLE purchase_orders (
    po_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id     INTEGER NOT NULL,
    order_date      TEXT DEFAULT CURRENT_TIMESTAMP,
    status          TEXT DEFAULT 'PENDING',
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE purchase_order_items (
    po_item_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    po_id           INTEGER NOT NULL,
    product_id      INTEGER NOT NULL,
    quantity        INTEGER NOT NULL,
    cost_price      REAL,
    FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE customers (
    customer_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT,
    phone           TEXT,
    email           TEXT
);

CREATE TABLE carts (
    cart_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id     INTEGER,
    created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE cart_items (
    cart_item_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id         INTEGER NOT NULL,
    product_id      INTEGER NOT NULL,
    quantity        INTEGER NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES carts(cart_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE bills (
    bill_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id     INTEGER,
    bill_date       TEXT DEFAULT CURRENT_TIMESTAMP,
    total_amount    REAL,
    discount        REAL,
    net_amount      REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE bill_items (
    bill_item_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id         INTEGER NOT NULL,
    product_id      INTEGER NOT NULL,
    quantity        INTEGER NOT NULL,
    selling_price   REAL,
    total_price     REAL,
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE payments (
    payment_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id         INTEGER NOT NULL,
    payment_method  TEXT NOT NULL,
    amount_paid     REAL NOT NULL,
    payment_date    TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id)
);

CREATE TABLE employees (
    employee_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    role            TEXT,
    phone           TEXT
);

""")

print("Tables created successfully.")

# =========================
# INSERT DATA
# =========================

# Insert categories
cursor.executescript("""
INSERT INTO categories (category_id, category_name) VALUES
(1, 'Beverages'), (2, 'Snacks'), (3, 'Dairy'), (4, 'Bakery'), (5, 'Produce'),
(6, 'Frozen Foods'), (7, 'Meat'), (8, 'Seafood'), (9, 'Personal Care'),
(10, 'Household'), (11, 'Baby Care'), (12, 'Pet Supplies'),
(13, 'Canned Goods'), (14, 'Condiments'), (15, 'Grains & Pasta'),
(16, 'Breakfast Foods'), (17, 'Cleaning Supplies'), (18, 'Stationery'),
(19, 'Electronics'), (20, 'Miscellaneous');
""")

# Insert products
cursor.executescript("""
INSERT INTO products (product_id, product_name, category_id, price, cost_price, barcode, unit) VALUES
(1,'Whole Milk 1L',3,1.20,0.80,'100000000001','litre'),
(2,'Cheddar Cheese 200g',3,2.50,1.80,'100000000002','pack'),
(3,'White Bread Loaf',4,1.00,0.60,'100000000003','piece'),
(4,'Brown Bread Loaf',4,1.10,0.70,'100000000004','piece'),
(5,'Apple 1kg',5,2.00,1.20,'100000000005','kg'),
(6,'Banana 1kg',5,1.80,1.00,'100000000006','kg'),
(7,'Chicken Breast 500g',7,3.50,2.50,'100000000007','pack'),
(8,'Minced Beef 500g',7,4.00,2.80,'100000000008','pack'),
(9,'Coca-Cola 1.5L',1,1.60,1.00,'100000000009','bottle'),
(10,'Orange Juice 1L',1,1.40,0.90,'100000000010','carton'),
(11,'Potato Chips 150g',2,1.20,0.70,'100000000011','pack'),
(12,'Chocolate Bar 100g',2,1.00,0.60,'100000000012','bar'),
(13,'Frozen Peas 1kg',6,2.20,1.50,'100000000013','bag'),
(14,'Frozen Pizza',6,3.00,2.10,'100000000014','piece'),
(15,'Shampoo 250ml',9,3.50,2.00,'100000000015','bottle'),
(16,'Toothpaste 100ml',9,2.00,1.20,'100000000016','tube'),
(17,'Laundry Detergent 1kg',10,4.50,3.00,'100000000017','box'),
(18,'Rice 1kg',15,2.00,1.20,'100000000018','bag'),
(19,'Spaghetti 500g',15,1.30,0.80,'100000000019','pack'),
(20,'Tomato Ketchup 500ml',14,2.10,1.40,'100000000020','bottle');
""")

# Insert inventory
cursor.executescript("""
INSERT INTO inventory VALUES
(1,1,100,20,'2025-01-01 10:00:00'),
(2,2,80,15,'2025-01-01 10:05:00'),
(3,3,120,25,'2025-01-01 10:10:00'),
(4,4,90,20,'2025-01-01 10:15:00'),
(5,5,70,15,'2025-01-01 10:20:00'),
(6,6,60,15,'2025-01-01 10:25:00'),
(7,7,50,10,'2025-01-01 10:30:00'),
(8,8,40,10,'2025-01-01 10:35:00'),
(9,9,100,30,'2025-01-01 10:40:00'),
(10,10,90,25,'2025-01-01 10:45:00'),
(11,11,110,30,'2025-01-01 10:50:00'),
(12,12,95,25,'2025-01-01 10:55:00'),
(13,13,60,15,'2025-01-01 11:00:00'),
(14,14,55,15,'2025-01-01 11:05:00'),
(15,15,45,10,'2025-01-01 11:10:00'),
(16,16,70,15,'2025-01-01 11:15:00'),
(17,17,40,10,'2025-01-01 11:20:00'),
(18,18,80,20,'2025-01-01 11:25:00'),
(19,19,85,20,'2025-01-01 11:30:00'),
(20,20,65,15,'2025-01-01 11:35:00');
""")

# Insert suppliers
cursor.executescript("""
INSERT INTO suppliers VALUES
(1,'Fresh Farms Ltd','freshfarms@example.com'),
(2,'Dairy Direct','dairydirect@example.com'),
(3,'Bakers Hub','bakershub@example.com'),
(4,'Meat Masters','meatmasters@example.com'),
(5,'Oceanic Seafood','oceanic@example.com'),
(6,'Snack World','snackworld@example.com'),
(7,'Beverage Co','beverageco@example.com'),
(8,'Frozen Foods Inc','frozenfoods@example.com'),
(9,'Clean & Shine','cleanshine@example.com'),
(10,'Home Essentials','homeess@example.com'),
(11,'Health & Care','healthcare@example.com'),
(12,'Grain Traders','graintraders@example.com'),
(13,'Pasta & Co','pastaco@example.com'),
(14,'Condiment House','condiments@example.com'),
(15,'Green Garden','greengarden@example.com'),
(16,'Tech Retail','techretail@example.com'),
(17,'Paper Goods Ltd','papergoods@example.com'),
(18,'Pet Friends','petfriends@example.com'),
(19,'Baby World','babyworld@example.com'),
(20,'Misc Supplies','miscsupplies@example.com');
""")

# Insert purchase_orders
cursor.executescript("""
INSERT INTO purchase_orders VALUES
(1,1,'2025-01-02 09:00:00','RECEIVED'),
(2,2,'2025-01-02 09:15:00','RECEIVED'),
(3,3,'2025-01-02 09:30:00','RECEIVED'),
(4,4,'2025-01-02 09:45:00','RECEIVED'),
(5,5,'2025-01-02 10:00:00','RECEIVED'),
(6,6,'2025-01-02 10:15:00','RECEIVED'),
(7,7,'2025-01-02 10:30:00','RECEIVED'),
(8,8,'2025-01-02 10:45:00','RECEIVED'),
(9,9,'2025-01-02 11:00:00','RECEIVED'),
(10,10,'2025-01-02 11:15:00','RECEIVED'),
(11,11,'2025-01-03 09:00:00','RECEIVED'),
(12,12,'2025-01-03 09:15:00','RECEIVED'),
(13,13,'2025-01-03 09:30:00','RECEIVED'),
(14,14,'2025-01-03 09:45:00','RECEIVED'),
(15,15,'2025-01-03 10:00:00','RECEIVED'),
(16,16,'2025-01-03 10:15:00','PENDING'),
(17,17,'2025-01-03 10:30:00','PENDING'),
(18,18,'2025-01-03 10:45:00','PENDING'),
(19,19,'2025-01-03 11:00:00','PENDING'),
(20,20,'2025-01-03 11:15:00','PENDING');
""")

# Insert purchase_order_items
cursor.executescript("""
INSERT INTO purchase_order_items VALUES
(1,1,1,50,0.80),(2,1,9,40,1.00),
(3,2,2,40,1.80),(4,2,11,60,0.70),
(5,3,3,70,0.60),(6,3,4,60,0.70),
(7,4,7,40,2.50),(8,4,8,35,2.80),
(9,5,5,50,1.20),(10,5,6,45,1.00),
(11,6,13,30,1.50),(12,6,14,30,2.10),
(13,7,15,40,2.00),(14,7,16,50,1.20),
(15,8,17,30,3.00),(16,8,18,40,1.20),
(17,9,19,45,0.80),(18,9,20,35,1.40),
(19,10,9,30,1.00),(20,10,10,30,0.90),
(21,11,1,40,0.80),(22,11,2,30,1.80),
(23,12,3,40,0.60),(24,12,4,35,0.70),
(25,13,5,30,1.20),(26,13,6,30,1.00),
(27,14,7,20,2.50),(28,14,8,20,2.80),
(29,15,11,50,0.70),(30,15,12,50,0.60),
(31,16,13,25,1.50),(32,16,14,25,2.10),
(33,17,15,30,2.00),(34,17,16,30,1.20),
(35,18,17,20,3.00),(36,18,18,30,1.20),
(37,19,19,30,0.80),(38,19,20,25,1.40),
(39,20,9,20,1.00),(40,20,10,20,0.90);
""")

# Insert customers
cursor.executescript("""
INSERT INTO customers VALUES
(1,'Alice Johnson','07000000001','alice@example.com'),
(2,'Bob Smith','07000000002','bob@example.com'),
(3,'Charlie Brown','07000000003','charlie@example.com'),
(4,'Diana Prince','07000000004','diana@example.com'),
(5,'Ethan Hunt','07000000005','ethan@example.com'),
(6,'Fiona Gallagher','07000000006','fiona@example.com'),
(7,'George Miller','07000000007','george@example.com'),
(8,'Hannah Lee','07000000008','hannah@example.com'),
(9,'Ian Wright','07000000009','ian@example.com'),
(10,'Julia Roberts','07000000010','julia@example.com'),
(11,'Kevin Hart','07000000011','kevin@example.com'),
(12,'Laura King','07000000012','laura@example.com'),
(13,'Michael Scott','07000000013','michael@example.com'),
(14,'Nina Dobrev','07000000014','nina@example.com'),
(15,'Oscar Wilde','07000000015','oscar@example.com'),
(16,'Paula Adams','07000000016','paula@example.com'),
(17,'Quentin Blake','07000000017','quentin@example.com'),
(18,'Rachel Green','07000000018','rachel@example.com'),
(19,'Sam Wilson','07000000019','sam@example.com'),
(20,'Tina Turner','07000000020','tina@example.com');
""")

# Insert carts
cursor.executescript("""
INSERT INTO carts VALUES
(1,1,'2025-01-05 10:00:00'),
(2,2,'2025-01-05 10:05:00'),
(3,3,'2025-01-05 10:10:00'),
(4,4,'2025-01-05 10:15:00'),
(5,5,'2025-01-05 10:20:00'),
(6,6,'2025-01-05 10:25:00'),
(7,7,'2025-01-05 10:30:00'),
(8,8,'2025-01-05 10:35:00'),
(9,9,'2025-01-05 10:40:00'),
(10,10,'2025-01-05 10:45:00'),
(11,11,'2025-01-05 11:00:00'),
(12,12,'2025-01-05 11:05:00'),
(13,13,'2025-01-05 11:10:00'),
(14,14,'2025-01-05 11:15:00'),
(15,15,'2025-01-05 11:20:00'),
(16,16,'2025-01-05 11:25:00'),
(17,17,'2025-01-05 11:30:00'),
(18,18,'2025-01-05 11:35:00'),
(19,19,'2025-01-05 11:40:00'),
(20,20,'2025-01-05 11:45:00');
""")

# Insert cart_items
cursor.executescript("""
INSERT INTO cart_items VALUES
(1,1,1,2),(2,1,3,1),
(3,2,9,3),(4,2,11,2),
(5,3,5,1),(6,3,6,1),
(7,4,7,2),(8,4,10,1),
(9,5,2,1),(10,5,12,3),
(11,6,13,1),(12,6,14,2),
(13,7,15,1),(14,7,16,1),
(15,8,17,1),(16,8,18,2),
(17,9,19,2),(18,9,20,1),
(19,10,9,2),(20,10,10,2),
(21,11,1,1),(22,11,2,1),
(23,12,3,2),(24,12,4,1),
(25,13,5,2),(26,13,6,2),
(27,14,7,1),(28,14,8,1),
(29,15,11,3),(30,15,12,2),
(31,16,13,1),(32,16,14,1),
(33,17,15,2),(34,17,16,2),
(35,18,17,1),(36,18,18,1),
(37,19,19,2),(38,19,20,2),
(39,20,9,1),(40,20,10,1);
""")

# Insert bills
cursor.executescript("""
INSERT INTO bills VALUES
(1,1,'2025-01-05 12:00:00',10.00,0.50,9.50),
(2,2,'2025-01-05 12:10:00',15.00,1.00,14.00),
(3,3,'2025-01-05 12:20:00',8.00,0.00,8.00),
(4,4,'2025-01-05 12:30:00',20.00,2.00,18.00),
(5,5,'2025-01-05 12:40:00',5.50,0.50,5.00),
(6,6,'2025-01-05 12:50:00',12.00,1.20,10.80),
(7,7,'2025-01-05 13:00:00',18.00,1.00,17.00),
(8,8,'2025-01-05 13:10:00',9.00,0.00,9.00),
(9,9,'2025-01-05 13:20:00',22.00,2.20,19.80),
(10,10,'2025-01-05 13:30:00',7.00,0.00,7.00),
(11,11,'2025-01-06 11:00:00',11.50,0.50,11.00),
(12,12,'2025-01-06 11:10:00',16.00,1.00,15.00),
(13,13,'2025-01-06 11:20:00',19.00,2.00,17.00),
(14,14,'2025-01-06 11:30:00',6.00,0.00,6.00),
(15,15,'2025-01-06 11:40:00',13.50,1.50,12.00),
(16,16,'2025-01-06 11:50:00',21.00,3.00,18.00),
(17,17,'2025-01-06 12:00:00',9.50,0.50,9.00),
(18,18,'2025-01-06 12:10:00',14.00,1.00,13.00),
(19,19,'2025-01-06 12:20:00',25.00,2.50,22.50),
(20,20,'2025-01-06 12:30:00',5.00,0.00,5.00);
""")

# Insert bill_items
cursor.executescript("""
INSERT INTO bill_items VALUES
(1,1,1,2,1.20,2.40),(2,1,3,1,1.00,1.00),(3,1,9,2,1.60,3.20),
(4,2,5,2,2.00,4.00),(5,2,6,2,1.80,3.60),(6,2,11,3,1.20,3.60),
(7,3,2,1,2.50,2.50),(8,3,12,3,1.00,3.00),(9,3,10,1,1.40,1.40),
(10,4,7,2,3.50,7.00),(11,4,8,2,4.00,8.00),(12,4,13,2,2.20,4.40),
(13,5,3,1,1.00,1.00),(14,5,9,2,1.60,3.20),(15,5,11,1,1.20,1.20),
(16,6,14,2,3.00,6.00),(17,6,15,1,3.50,3.50),(18,6,16,1,2.00,2.00),
(19,7,17,1,4.50,4.50),(20,7,18,2,2.00,4.00),(21,7,19,2,1.30,2.60),
(22,8,20,2,2.10,4.20),(23,8,9,1,1.60,1.60),(24,8,10,2,1.40,2.80),
(25,9,1,2,1.20,2.40),(26,9,2,2,2.50,5.00),(27,9,11,4,1.20,4.80),
(28,10,5,1,2.00,2.00),(29,10,6,2,1.80,3.60),(30,10,12,1,1.00,1.00),
(31,11,3,2,1.00,2.00),(32,11,9,2,1.60,3.20),(33,11,10,1,1.40,1.40),
(34,12,7,1,3.50,3.50),(35,12,8,1,4.00,4.00),(36,12,13,3,2.20,6.60),
(37,13,14,2,3.00,6.00),(38,13,15,1,3.50,3.50),(39,13,16,1,2.00,2.00),
(40,14,17,1,4.50,4.50),(41,14,18,1,2.00,2.00),(42,14,19,1,1.30,1.30),
(43,15,20,2,2.10,4.20),(44,15,9,1,1.60,1.60),(45,15,10,2,1.40,2.80),
(46,16,1,3,1.20,3.60),(47,16,2,2,2.50,5.00),(48,16,11,4,1.20,4.80),
(49,17,5,1,2.00,2.00),(50,17,6,2,1.80,3.60),(51,17,12,1,1.00,1.00),
(52,18,3,2,1.00,2.00),(53,18,4,1,1.10,1.10),(54,18,9,2,1.60,3.20),
(55,19,7,2,3.50,7.00),(56,19,8,2,4.00,8.00),(57,19,13,2,2.20,4.40),
(58,20,11,1,1.20,1.20),(59,20,12,2,1.00,2.00),(60,20,10,1,1.40,1.40);
""")

# Insert payments
cursor.executescript("""
INSERT INTO payments VALUES
(1,1,'CASH',9.50,'2025-01-05 12:05:00'),
(2,2,'CARD',14.00,'2025-01-05 12:15:00'),
(3,3,'CASH',8.00,'2025-01-05 12:25:00'),
(4,4,'CARD',18.00,'2025-01-05 12:35:00'),
(5,5,'CASH',5.00,'2025-01-05 12:45:00'),
(6,6,'CARD',10.80,'2025-01-05 12:55:00'),
(7,7,'UPI',17.00,'2025-01-05 13:05:00'),
(8,8,'CASH',9.00,'2025-01-05 13:15:00'),
(9,9,'CARD',19.80,'2025-01-05 13:25:00'),
(10,10,'CASH',7.00,'2025-01-05 13:35:00'),
(11,11,'CARD',11.00,'2025-01-06 11:05:00'),
(12,12,'UPI',15.00,'2025-01-06 11:15:00'),
(13,13,'CARD',17.00,'2025-01-06 11:25:00'),
(14,14,'CASH',6.00,'2025-01-06 11:35:00'),
(15,15,'CARD',12.00,'2025-01-06 11:45:00'),
(16,16,'UPI',18.00,'2025-01-06 11:55:00'),
(17,17,'CASH',9.00,'2025-01-06 12:05:00'),
(18,18,'CARD',13.00,'2025-01-06 12:15:00'),
(19,19,'CARD',22.50,'2025-01-06 12:25:00'),
(20,20,'CASH',5.00,'2025-01-06 12:35:00');
""")

# Insert employees
cursor.executescript("""
INSERT INTO employees VALUES
(1,'Emma Thompson','Cashier','07100000001'),
(2,'Liam Johnson','Cashier','07100000002'),
(3,'Olivia Brown','Stock Manager','07100000003'),
(4,'Noah Davis','Supervisor','07100000004'),
(5,'Ava Wilson','Cashier','07100000005'),
(6,'William Taylor','Inventory Clerk','07100000006'),
(7,'Sophia Anderson','Customer Service','07100000007'),
(8,'James Thomas','Cashier','07100000008'),
(9,'Isabella Jackson','Store Manager','07100000009'),
(10,'Benjamin White','Security','07100000010'),
(11,'Mia Harris','Cashier','07100000011'),
(12,'Lucas Martin','Stock Assistant','07100000012'),
(13,'Charlotte Thompson','Cashier','07100000013'),
(14,'Henry Garcia','Cleaner','07100000014'),
(15,'Amelia Martinez','Cashier','07100000015'),
(16,'Alexander Robinson','IT Support','07100000016'),
(17,'Harper Clark','HR','07100000017'),
(18,'Daniel Rodriguez','Assistant Manager','07100000018'),
(19,'Evelyn Lewis','Cashier','07100000019'),
(20,'Matthew Lee','Cashier','07100000020');
""")

conn.commit()
conn.close()

print("supermarket.db created successfully!")
