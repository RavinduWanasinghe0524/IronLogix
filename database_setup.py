import sqlite3
from datetime import datetime

# Database Name
DB_NAME = "buildsmart_hardware.db"

def create_connection():
    """Establish a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables():
    """Create the necessary tables for the Hardware OS."""
    conn = create_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    # 1. PRODUCTS TABLE
    # Note: 'unit_type' is critical for hardware (e.g., 'kg', 'cube', 'sheet', 'packet')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price_per_unit REAL NOT NULL,
            stock_quantity REAL NOT NULL,
            unit_type TEXT NOT NULL,
            reorder_level INTEGER DEFAULT 10
        )
    ''')

    # 2. CUSTOMERS TABLE (For WhatsApp Invoicing)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT UNIQUE NOT NULL,
            name TEXT,
            total_purchases REAL DEFAULT 0
        )
    ''')

    # 3. TRANSACTIONS TABLE (The Head of the Bill)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TEXT NOT NULL,
            customer_id INTEGER,
            total_amount REAL NOT NULL,
            payment_method TEXT DEFAULT 'Cash',
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')

    # 4. SALES_ITEMS TABLE (The Body of the Bill - what items were in one transaction)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER,
            product_id INTEGER,
            quantity_sold REAL NOT NULL,
            sub_total REAL NOT NULL,
            FOREIGN KEY (transaction_id) REFERENCES transactions (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    conn.commit()
    print("✅ Database tables created successfully.")
    conn.close()

def add_dummy_data():
    """Add some sample hardware items to test the system."""
    conn = create_connection()
    cursor = conn.cursor()

    # Check if data already exists
    cursor.execute("SELECT count(*) FROM products")
    if cursor.fetchone()[0] > 0:
        print("ℹ️  Data already exists. Skipping dummy data.")
        conn.close()
        return

    # Sample Hardware Data
    hardware_items = [
        ("Tokyo Super Cement 50kg", "Cement", 2300.00, 100, "Bag"),
        ("River Sand (Sudda)", "Sand", 18000.00, 50, "Cube"),
        ("Asbestos Sheet 8ft", "Roofing", 1200.00, 200, "Sheet"),
        ("Dulux Brilliant White 4L", "Paints", 4500.00, 25, "Bucket"),
        ("Wiring Cable 1mm (Kelani)", "Electrical", 8500.00, 10, "Roll")
    ]

    cursor.executemany('''
        INSERT INTO products (name, category, price_per_unit, stock_quantity, unit_type)
        VALUES (?, ?, ?, ?, ?)
    ''', hardware_items)

    conn.commit()
    print("✅ Dummy hardware data added.")
    conn.close()

if __name__ == "__main__":
    create_tables()
    add_dummy_data()
    print(f"🚀 System ready! Database file '{DB_NAME}' created.")
