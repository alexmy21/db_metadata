import sqlite3
import os
from pathlib import Path
from datetime import datetime, timedelta
import random

def create_sample_database():
    """Create a sample SQLite database with 15 tables - E-commerce themed"""
    # Ensure database directory exists
    db_dir = Path(__file__).parent.parent.parent / 'database'
    db_dir.mkdir(exist_ok=True)
    
    db_path = db_dir / 'sqlite_test'
    
    # Delete existing database to start fresh (if not locked)
    try:
        if db_path.exists():
            db_path.unlink()
    except PermissionError:
        print("Warning: Database file is locked. Will overwrite instead.")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop all existing tables if they exist
    cursor.execute("PRAGMA foreign_keys = OFF")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
    cursor.execute("PRAGMA foreign_keys = ON")
    conn.commit()

    
    # ========== TABLE 1: Customers ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            address TEXT,
            city TEXT,
            country TEXT DEFAULT 'USA',
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # ========== TABLE 2: Categories ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE,
            description TEXT,
            parent_category_id INTEGER,
            FOREIGN KEY (parent_category_id) REFERENCES categories(category_id)
        )
    """)
    
    # ========== TABLE 3: Products ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            price REAL NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            description TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """)
    
    # ========== TABLE 4: Orders ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            shipping_address TEXT,
            payment_method TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)
    
    # ========== TABLE 5: Order Items ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            unit_price REAL NOT NULL CHECK(unit_price >= 0),
            subtotal REAL NOT NULL CHECK(subtotal >= 0),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)
    
    # ========== TABLE 6: Suppliers ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL UNIQUE,
            contact_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            address TEXT,
            city TEXT,
            country TEXT DEFAULT 'USA',
            rating REAL CHECK(rating >= 0 AND rating <= 5),
            is_active BOOLEAN DEFAULT 1
        )
    """)
    
    # ========== TABLE 7: Departments ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            department_id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_name TEXT NOT NULL UNIQUE,
            manager_name TEXT,
            budget REAL CHECK(budget >= 0),
            description TEXT,
            created_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # ========== TABLE 8: Employees ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            department_id INTEGER NOT NULL,
            position TEXT NOT NULL,
            salary REAL NOT NULL CHECK(salary > 0),
            hire_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (department_id) REFERENCES departments(department_id)
        )
    """)
    
    # ========== TABLE 9: Reviews ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            review_text TEXT,
            review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_verified_purchase BOOLEAN DEFAULT 0,
            helpful_count INTEGER DEFAULT 0 CHECK(helpful_count >= 0),
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)
    
    # ========== TABLE 10: Shipping Methods ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipping_methods (
            shipping_method_id INTEGER PRIMARY KEY AUTOINCREMENT,
            method_name TEXT NOT NULL UNIQUE,
            description TEXT,
            base_cost REAL NOT NULL CHECK(base_cost >= 0),
            estimated_days INTEGER NOT NULL CHECK(estimated_days > 0),
            is_available BOOLEAN DEFAULT 1
        )
    """)
    
    # ========== TABLE 11: Payment Transactions ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payment_transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            amount REAL NOT NULL CHECK(amount > 0),
            payment_method TEXT NOT NULL,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'completed', 'failed', 'refunded')),
            transaction_reference TEXT UNIQUE,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )
    """)
    
    # ========== TABLE 12: Inventory Log ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity_change INTEGER NOT NULL,
            change_type TEXT NOT NULL CHECK(change_type IN ('purchase', 'sale', 'adjustment', 'return')),
            reference_id INTEGER,
            notes TEXT,
            log_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            employee_id INTEGER,
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        )
    """)
    
    # ========== TABLE 13: Discounts ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS discounts (
            discount_id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            description TEXT,
            discount_percentage REAL CHECK(discount_percentage >= 0 AND discount_percentage <= 100),
            discount_amount REAL CHECK(discount_amount >= 0),
            start_date DATETIME NOT NULL,
            end_date DATETIME NOT NULL,
            min_purchase_amount REAL DEFAULT 0,
            max_uses INTEGER,
            times_used INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            CHECK(end_date > start_date)
        )
    """)
    
    # ========== TABLE 14: Wishlists ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wishlists (
            wishlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            added_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            priority INTEGER DEFAULT 1 CHECK(priority >= 1 AND priority <= 5),
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            UNIQUE(customer_id, product_id)
        )
    """)
    
    # ========== TABLE 15: Addresses ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS addresses (
            address_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            address_type TEXT NOT NULL CHECK(address_type IN ('billing', 'shipping', 'both')),
            street_address TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT,
            postal_code TEXT NOT NULL,
            country TEXT DEFAULT 'USA' NOT NULL,
            is_default BOOLEAN DEFAULT 0,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)
    
    # Create indexes for better performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_employees_department ON employees(department_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_product ON reviews(product_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_customer ON reviews(customer_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_payment_transactions_order ON payment_transactions(order_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_inventory_log_product ON inventory_log(product_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_wishlists_customer ON wishlists(customer_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_addresses_customer ON addresses(customer_id);")

    
    # ========== INSERT SAMPLE DATA ==========
    
    # Insert sample customers
    cursor.execute("""
        INSERT INTO customers (first_name, last_name, email, phone, address, city, country) VALUES 
        ('John', 'Doe', 'john.doe@email.com', '555-0101', '123 Main St', 'New York', 'USA'),
        ('Jane', 'Smith', 'jane.smith@email.com', '555-0102', '456 Oak Ave', 'Los Angeles', 'USA'),
        ('Robert', 'Johnson', 'robert.j@email.com', '555-0103', '789 Pine Rd', 'Chicago', 'USA'),
        ('Emily', 'Brown', 'emily.brown@email.com', '555-0104', '321 Elm St', 'Houston', 'USA'),
        ('Michael', 'Wilson', 'michael.w@email.com', '555-0105', '654 Maple Dr', 'Phoenix', 'USA'),
        ('Sarah', 'Davis', 'sarah.davis@email.com', '555-0106', '987 Cedar Ln', 'Philadelphia', 'USA'),
        ('David', 'Martinez', 'david.m@email.com', '555-0107', '147 Birch Ct', 'San Antonio', 'USA'),
        ('Lisa', 'Anderson', 'lisa.a@email.com', '555-0108', '258 Spruce Way', 'San Diego', 'USA')
    """)
    
    # Insert sample categories
    cursor.execute("""
        INSERT INTO categories (category_name, description) VALUES 
        ('Electronics', 'Electronic devices and gadgets'),
        ('Computers', 'Laptops, desktops, and accessories'),
        ('Audio', 'Headphones, speakers, and audio equipment'),
        ('Clothing', 'Fashion and apparel'),
        ('Home & Garden', 'Home improvement and garden supplies'),
        ('Books', 'Physical and digital books'),
        ('Sports', 'Sports equipment and fitness gear'),
        ('Toys', 'Toys and games for all ages')
    """)
    
    # Insert sample products
    cursor.execute("""
        INSERT INTO products (product_name, category_id, price, stock_quantity, description, is_active) VALUES 
        ('Laptop Pro 15"', 2, 1299.99, 45, 'High-performance laptop with 16GB RAM', 1),
        ('Wireless Mouse', 2, 29.99, 150, 'Ergonomic wireless mouse', 1),
        ('Mechanical Keyboard', 2, 89.99, 75, 'RGB mechanical gaming keyboard', 1),
        ('USB-C Hub', 2, 49.99, 120, '7-in-1 USB-C hub adapter', 1),
        ('Bluetooth Headphones', 3, 199.99, 60, 'Noise-cancelling wireless headphones', 1),
        ('Portable Speaker', 3, 79.99, 85, 'Waterproof Bluetooth speaker', 1),
        ('Smart Watch', 1, 349.99, 50, 'Fitness tracking smartwatch', 1),
        ('Phone Case', 1, 19.99, 200, 'Protective phone case', 1),
        ('Cotton T-Shirt', 4, 24.99, 300, 'Comfortable cotton t-shirt', 1),
        ('Running Shoes', 7, 89.99, 100, 'Lightweight running shoes', 1),
        ('Yoga Mat', 7, 34.99, 80, 'Non-slip yoga mat', 1),
        ('Garden Tools Set', 5, 59.99, 40, 'Complete garden tools set', 1),
        ('Programming Book', 6, 44.99, 65, 'Learn Python programming', 1),
        ('Board Game', 8, 39.99, 90, 'Strategy board game for families', 1),
        ('Action Figure', 8, 24.99, 150, 'Collectible action figure', 1)
    """)
    
    # Insert sample orders
    cursor.execute("""
        INSERT INTO orders (customer_id, total_amount, status, shipping_address, payment_method) VALUES 
        (1, 1329.98, 'delivered', '123 Main St, New York, USA', 'credit_card'),
        (2, 309.98, 'shipped', '456 Oak Ave, Los Angeles, USA', 'paypal'),
        (3, 149.97, 'pending', '789 Pine Rd, Chicago, USA', 'credit_card'),
        (4, 449.98, 'processing', '321 Elm St, Houston, USA', 'debit_card'),
        (5, 89.98, 'delivered', '654 Maple Dr, Phoenix, USA', 'credit_card'),
        (1, 219.98, 'delivered', '123 Main St, New York, USA', 'credit_card'),
        (6, 124.98, 'shipped', '987 Cedar Ln, Philadelphia, USA', 'paypal'),
        (7, 349.99, 'pending', '147 Birch Ct, San Antonio, USA', 'credit_card'),
        (8, 179.97, 'delivered', '258 Spruce Way, San Diego, USA', 'debit_card'),
        (2, 44.99, 'delivered', '456 Oak Ave, Los Angeles, USA', 'paypal')
    """)
    
    # Insert sample order items
    cursor.execute("""
        INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES 
        (1, 1, 1, 1299.99, 1299.99),
        (1, 2, 1, 29.99, 29.99),
        (2, 5, 1, 199.99, 199.99),
        (2, 6, 1, 79.99, 79.99),
        (2, 2, 1, 29.99, 29.99),
        (3, 9, 6, 24.99, 149.94),
        (4, 7, 1, 349.99, 349.99),
        (4, 3, 1, 89.99, 89.99),
        (5, 11, 1, 34.99, 34.99),
        (5, 10, 1, 89.99, 89.99),
        (6, 5, 1, 199.99, 199.99),
        (6, 8, 1, 19.99, 19.99),
        (7, 10, 1, 89.99, 89.99),
        (7, 11, 1, 34.99, 34.99),
        (8, 7, 1, 349.99, 349.99),
        (9, 13, 4, 44.99, 179.96),
        (10, 13, 1, 44.99, 44.99)
    """)
    
    # ========== INSERT DATA FOR NEW TABLES ==========
    
    # Insert 20 suppliers
    cursor.execute("""
        INSERT INTO suppliers (company_name, contact_name, email, phone, address, city, country, rating, is_active) VALUES 
        ('TechParts Inc', 'James Brown', 'james@techparts.com', '555-1001', '100 Tech Blvd', 'San Jose', 'USA', 4.5, 1),
        ('Global Electronics', 'Maria Garcia', 'maria@globalelec.com', '555-1002', '200 Circuit Ave', 'Austin', 'USA', 4.8, 1),
        ('Audio Solutions', 'David Lee', 'david@audiosol.com', '555-1003', '300 Sound St', 'Nashville', 'USA', 4.2, 1),
        ('Fashion Wholesale', 'Emma Wilson', 'emma@fashionwh.com', '555-1004', '400 Style Rd', 'New York', 'USA', 4.6, 1),
        ('Book Distributors', 'Oliver Taylor', 'oliver@bookdist.com', '555-1005', '500 Page Ln', 'Boston', 'USA', 4.7, 1),
        ('Sports Gear Co', 'Sophia Anderson', 'sophia@sportsgear.com', '555-1006', '600 Active Way', 'Denver', 'USA', 4.4, 1),
        ('Toy Factory', 'Noah Martinez', 'noah@toyfactory.com', '555-1007', '700 Play St', 'Charlotte', 'USA', 4.3, 1),
        ('Smart Devices Ltd', 'Ava Thomas', 'ava@smartdev.com', '555-1008', '800 Innovation Dr', 'Seattle', 'USA', 4.9, 1),
        ('Component Supply', 'Liam Jackson', 'liam@compsupply.com', '555-1009', '900 Part Ave', 'Portland', 'USA', 4.1, 1),
        ('Gadget World', 'Isabella White', 'isabella@gadgetworld.com', '555-1010', '1000 Tech Pkwy', 'San Francisco', 'USA', 4.6, 1),
        ('Premium Audio', 'Mason Harris', 'mason@premiumaudio.com', '555-1011', '1100 Sound Cir', 'Los Angeles', 'USA', 4.8, 1),
        ('Apparel Direct', 'Charlotte Martin', 'charlotte@appareldir.com', '555-1012', '1200 Fashion Blvd', 'Miami', 'USA', 4.5, 1),
        ('Book Masters', 'Ethan Thompson', 'ethan@bookmasters.com', '555-1013', '1300 Library Ln', 'Chicago', 'USA', 4.7, 1),
        ('Fitness Plus', 'Amelia Garcia', 'amelia@fitnessplus.com', '555-1014', '1400 Gym Rd', 'Dallas', 'USA', 4.4, 1),
        ('Kids Toys Ltd', 'Lucas Rodriguez', 'lucas@kidstoys.com', '555-1015', '1500 Play Ave', 'Atlanta', 'USA', 4.2, 1),
        ('Digital Parts', 'Mia Martinez', 'mia@digitalparts.com', '555-1016', '1600 Circuit Way', 'Phoenix', 'USA', 4.6, 1),
        ('Sound Systems', 'Benjamin Lee', 'benjamin@soundsys.com', '555-1017', '1700 Audio Dr', 'San Diego', 'USA', 4.5, 1),
        ('Style Imports', 'Harper Wilson', 'harper@styleimports.com', '555-1018', '1800 Trend St', 'Las Vegas', 'USA', 4.3, 1),
        ('Media Books', 'Elijah Moore', 'elijah@mediabooks.com', '555-1019', '1900 Read Blvd', 'Seattle', 'USA', 4.8, 1),
        ('Active Life', 'Evelyn Taylor', 'evelyn@activelife.com', '555-1020', '2000 Sport Ln', 'Houston', 'USA', 4.7, 1)
    """)
    
    # Insert 20 departments
    cursor.execute("""
        INSERT INTO departments (department_name, manager_name, budget, description) VALUES 
        ('Sales', 'Jennifer Adams', 500000.00, 'Customer sales and relationships'),
        ('Marketing', 'Michael Chen', 350000.00, 'Marketing and brand management'),
        ('IT', 'Sarah Johnson', 600000.00, 'Information technology and systems'),
        ('Human Resources', 'Robert Williams', 250000.00, 'HR and employee management'),
        ('Finance', 'Patricia Brown', 400000.00, 'Financial planning and accounting'),
        ('Customer Service', 'Linda Davis', 300000.00, 'Customer support operations'),
        ('Warehouse', 'James Miller', 450000.00, 'Inventory and logistics'),
        ('Product Development', 'Elizabeth Wilson', 550000.00, 'New product research'),
        ('Quality Assurance', 'William Moore', 280000.00, 'Quality control and testing'),
        ('Legal', 'Barbara Taylor', 320000.00, 'Legal compliance and contracts'),
        ('Research', 'Richard Anderson', 480000.00, 'Market and product research'),
        ('Operations', 'Susan Thomas', 520000.00, 'Business operations management'),
        ('Procurement', 'Joseph Jackson', 350000.00, 'Purchasing and supplier relations'),
        ('Shipping', 'Margaret White', 380000.00, 'Order fulfillment and shipping'),
        ('Design', 'Charles Harris', 290000.00, 'Product and graphic design'),
        ('Training', 'Jessica Martin', 220000.00, 'Employee training programs'),
        ('Analytics', 'Daniel Thompson', 410000.00, 'Data analysis and reporting'),
        ('Security', 'Karen Garcia', 340000.00, 'Physical and cyber security'),
        ('Facilities', 'Thomas Martinez', 310000.00, 'Building and facility management'),
        ('Communications', 'Nancy Robinson', 270000.00, 'Internal and external communications')
    """)
    
    # Insert 20 employees
    cursor.execute("""
        INSERT INTO employees (first_name, last_name, email, phone, department_id, position, salary, is_active) VALUES 
        ('Alex', 'Johnson', 'alex.johnson@company.com', '555-2001', 1, 'Sales Manager', 75000.00, 1),
        ('Rachel', 'Smith', 'rachel.smith@company.com', '555-2002', 2, 'Marketing Specialist', 62000.00, 1),
        ('Tom', 'Brown', 'tom.brown@company.com', '555-2003', 3, 'Software Engineer', 95000.00, 1),
        ('Jessica', 'Davis', 'jessica.davis@company.com', '555-2004', 4, 'HR Coordinator', 58000.00, 1),
        ('Mark', 'Wilson', 'mark.wilson@company.com', '555-2005', 5, 'Financial Analyst', 72000.00, 1),
        ('Amy', 'Martinez', 'amy.martinez@company.com', '555-2006', 6, 'Support Representative', 48000.00, 1),
        ('Chris', 'Garcia', 'chris.garcia@company.com', '555-2007', 7, 'Warehouse Supervisor', 55000.00, 1),
        ('Lauren', 'Rodriguez', 'lauren.rodriguez@company.com', '555-2008', 8, 'Product Manager', 88000.00, 1),
        ('Kevin', 'Hernandez', 'kevin.hernandez@company.com', '555-2009', 9, 'QA Engineer', 68000.00, 1),
        ('Nicole', 'Lopez', 'nicole.lopez@company.com', '555-2010', 10, 'Legal Counsel', 105000.00, 1),
        ('Brian', 'Gonzalez', 'brian.gonzalez@company.com', '555-2011', 11, 'Research Analyst', 64000.00, 1),
        ('Michelle', 'Perez', 'michelle.perez@company.com', '555-2012', 12, 'Operations Manager', 82000.00, 1),
        ('Jason', 'Turner', 'jason.turner@company.com', '555-2013', 13, 'Procurement Specialist', 61000.00, 1),
        ('Amanda', 'Phillips', 'amanda.phillips@company.com', '555-2014', 14, 'Shipping Coordinator', 52000.00, 1),
        ('Ryan', 'Campbell', 'ryan.campbell@company.com', '555-2015', 15, 'Senior Designer', 78000.00, 1),
        ('Stephanie', 'Parker', 'stephanie.parker@company.com', '555-2016', 16, 'Training Manager', 69000.00, 1),
        ('Eric', 'Evans', 'eric.evans@company.com', '555-2017', 17, 'Data Analyst', 73000.00, 1),
        ('Ashley', 'Edwards', 'ashley.edwards@company.com', '555-2018', 18, 'Security Officer', 56000.00, 1),
        ('Brandon', 'Collins', 'brandon.collins@company.com', '555-2019', 19, 'Facilities Manager', 65000.00, 1),
        ('Melissa', 'Stewart', 'melissa.stewart@company.com', '555-2020', 20, 'Communications Director', 85000.00, 1)
    """)
    
    # Insert 20 reviews
    cursor.execute("""
        INSERT INTO reviews (product_id, customer_id, rating, review_text, is_verified_purchase, helpful_count) VALUES 
        (1, 1, 5, 'Excellent laptop! Works perfectly for all my needs.', 1, 15),
        (1, 2, 4, 'Great performance but a bit pricey.', 1, 8),
        (2, 3, 5, 'Best mouse I have ever used. Very comfortable.', 1, 12),
        (3, 4, 5, 'Amazing keyboard with great RGB lighting!', 1, 20),
        (4, 5, 4, 'Good hub with all the ports I need.', 1, 6),
        (5, 6, 5, 'Outstanding noise cancellation. Worth every penny!', 1, 25),
        (5, 7, 4, 'Great sound quality but battery could be better.', 1, 10),
        (6, 8, 5, 'Perfect for outdoor use. Very durable!', 1, 18),
        (7, 1, 5, 'Love this smartwatch! Tracks everything perfectly.', 1, 22),
        (8, 2, 3, 'Decent case but not as protective as expected.', 1, 3),
        (9, 3, 5, 'Very comfortable t-shirt. Great fabric quality.', 1, 14),
        (10, 4, 5, 'Best running shoes ever! Very lightweight.', 1, 19),
        (11, 5, 4, 'Good yoga mat with excellent grip.', 1, 7),
        (12, 6, 5, 'Complete set with everything you need for gardening.', 1, 11),
        (13, 7, 5, 'Excellent book for learning Python. Highly recommend!', 1, 28),
        (14, 8, 4, 'Fun board game for the whole family.', 1, 9),
        (15, 1, 5, 'Great collectible figure with amazing detail.', 1, 13),
        (2, 4, 5, 'This mouse is so smooth and responsive!', 1, 16),
        (3, 5, 4, 'Good keyboard but a bit loud for office use.', 1, 5),
        (7, 6, 5, 'Smartwatch exceeded my expectations!', 1, 21)
    """)
    
    # Insert 20 shipping methods
    cursor.execute("""
        INSERT INTO shipping_methods (method_name, description, base_cost, estimated_days, is_available) VALUES 
        ('Standard Ground', 'Regular ground shipping', 5.99, 7, 1),
        ('Expedited Shipping', 'Faster delivery option', 12.99, 3, 1),
        ('Two-Day Air', 'Guaranteed 2-day delivery', 19.99, 2, 1),
        ('Next Day Air', 'Overnight delivery', 29.99, 1, 1),
        ('Economy Shipping', 'Slowest but cheapest option', 3.99, 10, 1),
        ('Priority Mail', 'USPS Priority service', 8.99, 5, 1),
        ('Express Mail', 'USPS Express service', 24.99, 1, 1),
        ('International Standard', 'Standard international shipping', 35.00, 14, 1),
        ('International Express', 'Fast international shipping', 65.00, 5, 1),
        ('Freight Shipping', 'For large/heavy items', 45.00, 10, 1),
        ('Local Pickup', 'Pick up at store', 0.00, 1, 1),
        ('Same Day Delivery', 'Delivered same day', 39.99, 1, 1),
        ('White Glove Service', 'Premium handling and delivery', 99.99, 3, 1),
        ('Pallet Shipping', 'Full pallet delivery', 125.00, 7, 1),
        ('Overnight Express', 'Fastest overnight option', 49.99, 1, 1),
        ('Weekend Delivery', 'Saturday/Sunday delivery', 22.99, 2, 1),
        ('Signature Required', 'Requires signature on delivery', 15.99, 5, 1),
        ('Insurance Included', 'Fully insured shipping', 18.99, 5, 1),
        ('Green Shipping', 'Carbon-neutral shipping', 9.99, 8, 1),
        ('Military Shipping', 'APO/FPO addresses', 12.99, 12, 1)
    """)
    
    # Insert 20 payment transactions
    cursor.execute("""
        INSERT INTO payment_transactions (order_id, amount, payment_method, status, transaction_reference) VALUES 
        (1, 1329.98, 'credit_card', 'completed', 'TXN-2024-001'),
        (2, 309.98, 'paypal', 'completed', 'TXN-2024-002'),
        (3, 149.97, 'credit_card', 'pending', 'TXN-2024-003'),
        (4, 449.98, 'debit_card', 'completed', 'TXN-2024-004'),
        (5, 89.98, 'credit_card', 'completed', 'TXN-2024-005'),
        (6, 219.98, 'credit_card', 'completed', 'TXN-2024-006'),
        (7, 124.98, 'paypal', 'completed', 'TXN-2024-007'),
        (8, 349.99, 'credit_card', 'pending', 'TXN-2024-008'),
        (9, 179.97, 'debit_card', 'completed', 'TXN-2024-009'),
        (10, 44.99, 'paypal', 'completed', 'TXN-2024-010'),
        (1, 1329.98, 'credit_card', 'refunded', 'TXN-2024-011'),
        (2, 309.98, 'paypal', 'completed', 'TXN-2024-012'),
        (3, 149.97, 'credit_card', 'failed', 'TXN-2024-013'),
        (4, 449.98, 'debit_card', 'completed', 'TXN-2024-014'),
        (5, 89.98, 'credit_card', 'completed', 'TXN-2024-015'),
        (6, 219.98, 'credit_card', 'completed', 'TXN-2024-016'),
        (7, 124.98, 'paypal', 'pending', 'TXN-2024-017'),
        (8, 349.99, 'credit_card', 'completed', 'TXN-2024-018'),
        (9, 179.97, 'debit_card', 'completed', 'TXN-2024-019'),
        (10, 44.99, 'paypal', 'completed', 'TXN-2024-020')
    """)
    
    # Insert 20 inventory log entries
    cursor.execute("""
        INSERT INTO inventory_log (product_id, quantity_change, change_type, reference_id, notes, employee_id) VALUES 
        (1, 50, 'purchase', 1, 'Initial stock purchase', 7),
        (2, 200, 'purchase', 2, 'Bulk order from supplier', 7),
        (3, 100, 'purchase', 3, 'Restocking keyboards', 7),
        (1, -1, 'sale', 1, 'Sold via order #1', 7),
        (2, -1, 'sale', 1, 'Sold via order #1', 7),
        (5, -1, 'sale', 2, 'Sold via order #2', 7),
        (6, -1, 'sale', 2, 'Sold via order #2', 7),
        (9, -6, 'sale', 3, 'Sold via order #3', 7),
        (7, 75, 'purchase', 4, 'New smartwatch shipment', 7),
        (8, 250, 'purchase', 5, 'Phone case bulk order', 7),
        (10, 150, 'purchase', 6, 'Running shoes restock', 7),
        (11, -1, 'sale', 5, 'Sold via order #5', 7),
        (3, 5, 'return', 4, 'Customer return - defective', 7),
        (5, -10, 'adjustment', NULL, 'Damage during transport', 7),
        (12, 60, 'purchase', 7, 'Garden tools arrival', 7),
        (13, 100, 'purchase', 8, 'Book shipment', 7),
        (14, 120, 'purchase', 9, 'Board games restock', 7),
        (15, 200, 'purchase', 10, 'Action figures bulk', 7),
        (4, -2, 'sale', 6, 'USB hubs sold', 7),
        (7, -2, 'sale', 8, 'Smartwatches sold', 7)
    """)
    
    # Insert 20 discounts
    cursor.execute("""
        INSERT INTO discounts (code, description, discount_percentage, discount_amount, start_date, end_date, min_purchase_amount, max_uses, times_used, is_active) VALUES 
        ('WELCOME10', '10% off for new customers', 10.0, NULL, '2024-01-01', '2024-12-31', 50.00, 1000, 45, 1),
        ('SUMMER25', '25% summer sale', 25.0, NULL, '2024-06-01', '2024-08-31', 100.00, 500, 123, 1),
        ('FREESHIP', 'Free shipping code', NULL, 10.00, '2024-01-01', '2024-12-31', 75.00, 2000, 567, 1),
        ('HOLIDAY20', '20% holiday discount', 20.0, NULL, '2024-11-01', '2024-12-31', 150.00, 800, 234, 1),
        ('SAVE50', 'Save $50 on orders over $500', NULL, 50.00, '2024-01-01', '2024-12-31', 500.00, 300, 89, 1),
        ('FLASH15', 'Flash sale 15% off', 15.0, NULL, '2024-03-01', '2024-03-31', 25.00, 1500, 678, 0),
        ('LOYALTY30', '30% loyalty reward', 30.0, NULL, '2024-01-01', '2024-12-31', 200.00, 100, 67, 1),
        ('CLEARANCE40', '40% clearance event', 40.0, NULL, '2024-09-01', '2024-09-30', 0.00, 2000, 1234, 0),
        ('SAVE100', '$100 off orders over $1000', NULL, 100.00, '2024-01-01', '2024-12-31', 1000.00, 50, 12, 1),
        ('SPRING20', '20% spring sale', 20.0, NULL, '2024-03-01', '2024-05-31', 80.00, 1000, 456, 0),
        ('WEEKEND10', 'Weekend special 10% off', 10.0, NULL, '2024-01-01', '2024-12-31', 30.00, 5000, 2345, 1),
        ('BULK25', '25% bulk purchase discount', 25.0, NULL, '2024-01-01', '2024-12-31', 300.00, 200, 78, 1),
        ('STUDENT15', '15% student discount', 15.0, NULL, '2024-01-01', '2024-12-31', 25.00, 3000, 1456, 1),
        ('EARLYBIRD', 'Early bird $20 off', NULL, 20.00, '2024-01-01', '2024-12-31', 100.00, 1000, 345, 1),
        ('VIP35', '35% VIP member discount', 35.0, NULL, '2024-01-01', '2024-12-31', 250.00, 100, 89, 1),
        ('BOGO', 'Buy one get 50% off second', 50.0, NULL, '2024-01-01', '2024-12-31', 0.00, 10000, 3456, 1),
        ('REFER20', '20% referral bonus', 20.0, NULL, '2024-01-01', '2024-12-31', 50.00, 500, 234, 1),
        ('BIRTHDAY25', '25% birthday discount', 25.0, NULL, '2024-01-01', '2024-12-31', 0.00, NULL, 678, 1),
        ('NEWYEAR50', 'New Year $50 off', NULL, 50.00, '2024-01-01', '2024-01-31', 200.00, 1000, 567, 0),
        ('CYBER40', 'Cyber Monday 40% off', 40.0, NULL, '2024-11-25', '2024-11-30', 100.00, 5000, 2345, 0)
    """)
    
    # Insert 20 wishlist entries
    cursor.execute("""
        INSERT INTO wishlists (customer_id, product_id, priority, notes) VALUES 
        (1, 7, 5, 'Want for birthday'),
        (1, 5, 4, 'Need for gym'),
        (2, 1, 5, 'Saving up for this'),
        (2, 10, 3, 'For marathon training'),
        (3, 3, 4, 'Upgrade my setup'),
        (3, 6, 2, 'Nice to have'),
        (4, 9, 1, 'Summer wardrobe'),
        (4, 12, 3, 'For garden project'),
        (5, 13, 5, 'Learning to code'),
        (5, 14, 2, 'Family game night'),
        (6, 15, 1, 'For my collection'),
        (6, 4, 4, 'Need more USB ports'),
        (7, 11, 5, 'Starting yoga'),
        (7, 2, 3, 'Replace old mouse'),
        (8, 8, 2, 'Phone protection'),
        (8, 7, 5, 'Fitness tracking'),
        (1, 10, 3, 'Running shoes'),
        (2, 12, 2, 'Gardening hobby'),
        (3, 13, 4, 'Educational reading'),
        (4, 5, 5, 'Music lover gift')
    """)
    
    # Insert 20 addresses
    cursor.execute("""
        INSERT INTO addresses (customer_id, address_type, street_address, city, state, postal_code, country, is_default) VALUES 
        (1, 'both', '123 Main St', 'New York', 'NY', '10001', 'USA', 1),
        (1, 'shipping', '789 Work Plaza', 'New York', 'NY', '10002', 'USA', 0),
        (2, 'both', '456 Oak Ave', 'Los Angeles', 'CA', '90001', 'USA', 1),
        (2, 'billing', '222 Business Rd', 'Los Angeles', 'CA', '90002', 'USA', 0),
        (3, 'both', '789 Pine Rd', 'Chicago', 'IL', '60601', 'USA', 1),
        (3, 'shipping', '333 Office St', 'Chicago', 'IL', '60602', 'USA', 0),
        (4, 'both', '321 Elm St', 'Houston', 'TX', '77001', 'USA', 1),
        (4, 'shipping', '444 Second Home', 'Houston', 'TX', '77002', 'USA', 0),
        (5, 'both', '654 Maple Dr', 'Phoenix', 'AZ', '85001', 'USA', 1),
        (5, 'billing', '555 Company Ave', 'Phoenix', 'AZ', '85002', 'USA', 0),
        (6, 'both', '987 Cedar Ln', 'Philadelphia', 'PA', '19101', 'USA', 1),
        (6, 'shipping', '666 Warehouse Blvd', 'Philadelphia', 'PA', '19102', 'USA', 0),
        (7, 'both', '147 Birch Ct', 'San Antonio', 'TX', '78201', 'USA', 1),
        (7, 'shipping', '777 Vacation Home', 'San Antonio', 'TX', '78202', 'USA', 0),
        (8, 'both', '258 Spruce Way', 'San Diego', 'CA', '92101', 'USA', 1),
        (8, 'billing', '888 PO Box 123', 'San Diego', 'CA', '92102', 'USA', 0),
        (1, 'shipping', '999 Parents House', 'Boston', 'MA', '02101', 'USA', 0),
        (2, 'shipping', '111 Friends Place', 'Seattle', 'WA', '98101', 'USA', 0),
        (3, 'billing', '222 Old Address', 'Denver', 'CO', '80201', 'USA', 0),
        (4, 'shipping', '333 Gift Destination', 'Miami', 'FL', '33101', 'USA', 0)
    """)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f'Sample database created successfully at {db_path}')
    print('Database contains 15 tables with the following record counts:')
    print('  - customers: 8 records')
    print('  - categories: 8 records')
    print('  - products: 15 records')
    print('  - orders: 10 records')
    print('  - order_items: 17 records')
    print('  - suppliers: 20 records')
    print('  - departments: 20 records')
    print('  - employees: 20 records')
    print('  - reviews: 20 records')
    print('  - shipping_methods: 20 records')
    print('  - payment_transactions: 20 records')
    print('  - inventory_log: 20 records')
    print('  - discounts: 20 records')
    print('  - wishlists: 20 records')
    print('  - addresses: 20 records')
    return db_path

if __name__ == '__main__':
    create_sample_database()
