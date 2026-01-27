"""
Initialize Demo Database

Creates a sample SQLite database with demo data for testing.
"""
import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path


def init_demo_database(db_path: str = 'data/database.db'):
    """Initialize demo database with sample data"""
    # Ensure directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.executescript('''
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            status INTEGER DEFAULT 1
        );

        -- Products table
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        -- Orders table
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        -- Order items table
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );

        -- Page views table
        CREATE TABLE IF NOT EXISTS page_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            page_path TEXT NOT NULL,
            view_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            duration_seconds INTEGER,
            device_type TEXT
        );
    ''')

    # Check if data already exists
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] > 0:
        print('Database already contains data. Skipping initialization.')
        conn.close()
        return

    # Insert sample users
    users = [
        ('alice', 'alice@example.com'),
        ('bob', 'bob@example.com'),
        ('charlie', 'charlie@example.com'),
        ('diana', 'diana@example.com'),
        ('eve', 'eve@example.com'),
        ('frank', 'frank@example.com'),
        ('grace', 'grace@example.com'),
        ('henry', 'henry@example.com'),
        ('ivy', 'ivy@example.com'),
        ('jack', 'jack@example.com'),
    ]

    for i, (username, email) in enumerate(users):
        created_at = datetime.now() - timedelta(days=random.randint(1, 365))
        cursor.execute(
            'INSERT INTO users (username, email, created_at, status) VALUES (?, ?, ?, ?)',
            (username, email, created_at, 1)
        )

    # Insert sample products
    categories = ['电子产品', '服装', '食品', '家居', '图书']
    products = [
        ('iPhone 15', '电子产品', 7999.00, 50),
        ('MacBook Pro', '电子产品', 14999.00, 30),
        ('AirPods Pro', '电子产品', 1999.00, 100),
        ('iPad Air', '电子产品', 4799.00, 45),
        ('运动T恤', '服装', 199.00, 200),
        ('牛仔裤', '服装', 399.00, 150),
        ('羽绒服', '服装', 899.00, 80),
        ('运动鞋', '服装', 599.00, 120),
        ('坚果礼盒', '食品', 128.00, 500),
        ('有机牛奶', '食品', 68.00, 1000),
        ('咖啡豆', '食品', 98.00, 300),
        ('智能台灯', '家居', 299.00, 60),
        ('空气净化器', '家居', 1999.00, 40),
        ('Python编程', '图书', 89.00, 200),
        ('数据分析入门', '图书', 69.00, 150),
    ]

    for name, category, price, stock in products:
        cursor.execute(
            'INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)',
            (name, category, price, stock)
        )

    # Insert sample orders
    statuses = ['pending', 'paid', 'shipped', 'completed', 'cancelled']

    for _ in range(100):
        user_id = random.randint(1, len(users))
        order_date = datetime.now() - timedelta(days=random.randint(0, 90))
        status = random.choices(statuses, weights=[0.1, 0.15, 0.2, 0.5, 0.05])[0]

        # Calculate total from items
        num_items = random.randint(1, 4)
        total = 0
        item_data = []

        for _ in range(num_items):
            product_id = random.randint(1, len(products))
            quantity = random.randint(1, 3)
            unit_price = products[product_id - 1][2]
            total += unit_price * quantity
            item_data.append((product_id, quantity, unit_price))

        cursor.execute(
            'INSERT INTO orders (user_id, total_amount, order_date, status) VALUES (?, ?, ?, ?)',
            (user_id, total, order_date, status)
        )

        order_id = cursor.lastrowid

        for product_id, quantity, unit_price in item_data:
            cursor.execute(
                'INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
                (order_id, product_id, quantity, unit_price)
            )

    # Insert sample page views
    pages = ['/', '/products', '/products/detail', '/cart', '/checkout', '/user/profile', '/search']
    devices = ['desktop', 'mobile', 'tablet']

    for _ in range(500):
        user_id = random.choice([None, random.randint(1, len(users))])
        page_path = random.choice(pages)
        view_time = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        duration = random.randint(5, 300)
        device = random.choice(devices)

        cursor.execute(
            'INSERT INTO page_views (user_id, page_path, view_time, duration_seconds, device_type) VALUES (?, ?, ?, ?, ?)',
            (user_id, page_path, view_time, duration, device)
        )

    conn.commit()
    conn.close()

    print(f'Demo database initialized at {db_path}')
    print('Tables created: users, products, orders, order_items, page_views')
    print(f'Sample data: {len(users)} users, {len(products)} products, 100 orders, 500 page views')


if __name__ == '__main__':
    init_demo_database()
