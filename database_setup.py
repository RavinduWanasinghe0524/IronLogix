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

    # 1. ENHANCED PRODUCTS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price_per_unit REAL NOT NULL,
            cost_price REAL DEFAULT 0,
            stock_quantity REAL NOT NULL,
            unit_type TEXT NOT NULL,
            reorder_level INTEGER DEFAULT 10,
            barcode TEXT UNIQUE,
            supplier_id INTEGER,
            image_path TEXT,
            description TEXT,
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
        )
    ''')

    # 2. CUSTOMERS TABLE (Enhanced with loyalty)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT UNIQUE NOT NULL,
            name TEXT,
            email TEXT,
            address TEXT,
            total_purchases REAL DEFAULT 0,
            loyalty_points INTEGER DEFAULT 0,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 3. TRANSACTIONS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TEXT NOT NULL,
            customer_id INTEGER,
            total_amount REAL NOT NULL,
            discount_amount REAL DEFAULT 0,
            payment_method TEXT DEFAULT 'Cash',
            payment_status TEXT DEFAULT 'Paid',
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')

    # 4. SALES_ITEMS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER,
            product_id INTEGER,
            quantity_sold REAL NOT NULL,
            unit_price REAL NOT NULL,
            sub_total REAL NOT NULL,
            FOREIGN KEY (transaction_id) REFERENCES transactions (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    # 5. SUPPLIERS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_person TEXT,
            phone_number TEXT,
            email TEXT,
            address TEXT,
            total_purchases REAL DEFAULT 0,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 6. LOYALTY TRANSACTIONS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loyalty_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            points_change INTEGER NOT NULL,
            transaction_id INTEGER,
            description TEXT,
            date_time TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (transaction_id) REFERENCES transactions (id)
        )
    ''')

    # 7. CREDIT SALES TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credit_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            amount_paid REAL DEFAULT 0,
            balance REAL NOT NULL,
            due_date TEXT,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (transaction_id) REFERENCES transactions (id),
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')

    # 8. EXPENSES TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            payment_method TEXT DEFAULT 'Cash'
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

    # Add sample supplier
    cursor.execute('''
        INSERT INTO suppliers (name, contact_person, phone_number)
        VALUES ('Ceylon Hardware Suppliers', 'Mr. Silva', '077-1234567')
    ''')
    supplier_id = cursor.lastrowid

    # Enhanced Sample Hardware Data with cost prices and barcodes
    hardware_items = [
        ("Tokyo Super Cement 50kg", "Cement", 2300.00, 2100.00, 100, "Bag", "BAR001", supplier_id),
        ("River Sand (Sudda)", "Sand", 18000.00, 16000.00, 50, "Cube", "BAR002", supplier_id),
        ("Asbestos Sheet 8ft", "Roofing", 1200.00, 1000.00, 200, "Sheet", "BAR003", supplier_id),
        ("Dulux Brilliant White 4L", "Paints", 4500.00, 3800.00, 25, "Bucket", "BAR004", supplier_id),
        ("Wiring Cable 1mm (Kelani)", "Electrical", 8500.00, 7200.00, 10, "Roll", "BAR005", supplier_id),
        ("Steel Bars 12mm", "Metal", 250.00, 220.00, 500, "Kg", "BAR006", supplier_id),
        ("Clay Bricks", "Bricks", 25.00, 20.00, 5000, "Unit", "BAR007", supplier_id),
        ("Floor Tiles 2x2", "Tiles", 150.00, 120.00, 300, "Sqft", "BAR008", supplier_id),
        ("PVC Pipe 1 inch", "Plumbing", 380.00, 320.00, 80, "Unit", "BAR009", supplier_id),
        ("Electrical Switches", "Electrical", 120.00, 95.00, 150, "Unit", "BAR010", supplier_id)
    ]

    cursor.executemany('''
        INSERT INTO products (name, category, price_per_unit, cost_price, stock_quantity, unit_type, barcode, supplier_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', hardware_items)

    # Add sample customer
    cursor.execute('''
        INSERT INTO customers (phone_number, name, loyalty_points, total_purchases)
        VALUES ('0771234567', 'Kasun Perera', 150, 45000.00)
    ''')

    conn.commit()
    print("✅ Dummy hardware data added.")
    conn.close()

if __name__ == "__main__":
    create_tables()
    add_dummy_data()
    print(f"🚀 System ready! Database file '{DB_NAME}' created.")
