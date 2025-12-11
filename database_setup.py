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

    # CREATE PERFORMANCE INDEXES
    print("📊 Creating performance indexes...")
    
    # Product indexes for fast search and lookup
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_barcode ON products(barcode)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_stock ON products(stock_quantity)')
    
    # Customer indexes for fast lookup
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone_number)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_customers_name ON customers(name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_customers_points ON customers(loyalty_points)')
    
    # Transaction indexes for reporting and analytics
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date_time)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_customer ON transactions(customer_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(payment_status)')
    
    # Sales items indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sales_items_transaction ON sales_items(transaction_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sales_items_product ON sales_items(product_id)')
    
    # Credit sales indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_credit_sales_customer ON credit_sales(customer_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_credit_sales_status ON credit_sales(status)')
    
    # Loyalty transactions indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_loyalty_customer ON loyalty_transactions(customer_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_loyalty_date ON loyalty_transactions(date_time)')

    print("✅ Performance indexes created successfully.")

    # CREATE DATA INTEGRITY TRIGGERS
    print("🔒 Setting up data integrity triggers...")
    
    # Trigger to update customer total purchases
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_customer_purchases
        AFTER INSERT ON transactions
        FOR EACH ROW
        WHEN NEW.customer_id IS NOT NULL
        BEGIN
            UPDATE customers 
            SET total_purchases = total_purchases + NEW.total_amount
            WHERE id = NEW.customer_id;
        END;
    ''')
    
    # Trigger to prevent negative stock
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS prevent_negative_stock
        BEFORE UPDATE ON products
        FOR EACH ROW
        WHEN NEW.stock_quantity < 0
        BEGIN
            SELECT RAISE(ABORT, 'Stock quantity cannot be negative');
        END;
    ''')

    print("✅ Data integrity triggers created successfully.")

    conn.commit()
    print("✅ Database tables created successfully.")
    conn.close()

def backup_database(backup_name=None):
    """Create a backup of the database."""
    import shutil
    from datetime import datetime
    
    if backup_name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"buildsmart_backup_{timestamp}.db"
    
    try:
        # Create backups directory if it doesn't exist
        import os
        if not os.path.exists('backups'):
            os.makedirs('backups')
        
        backup_path = os.path.join('backups', backup_name)
        shutil.copy2(DB_NAME, backup_path)
        print(f"✅ Database backed up to: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return None

def validate_database():
    """Validate database schema and integrity."""
    conn = create_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    
    try:
        print("\n🔍 Validating database schema...")
        
        # Check required tables
        required_tables = [
            'products', 'customers', 'transactions', 'sales_items',
            'suppliers', 'loyalty_transactions', 'credit_sales', 'expenses'
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        missing_tables = [t for t in required_tables if t not in existing_tables]
        
        if missing_tables:
            print(f"❌ Missing tables: {', '.join(missing_tables)}")
            return False
        
        print(f"✅ All {len(required_tables)} required tables present")
        
        # Check for orphaned records
        cursor.execute('''
            SELECT COUNT(*) FROM sales_items 
            WHERE product_id NOT IN (SELECT id FROM products)
        ''')
        orphaned_items = cursor.fetchone()[0]
        
        if orphaned_items > 0:
            print(f"⚠️  Found {orphaned_items} orphaned sales items")
        else:
            print("✅ No orphaned records found")
        
        # Check data anomalies
        cursor.execute('SELECT COUNT(*) FROM products WHERE stock_quantity < 0')
        negative_stock = cursor.fetchone()[0]
        
        if negative_stock > 0:
            print(f"⚠️  Found {negative_stock} products with negative stock")
        else:
            print("✅ No negative stock found")
        
        conn.close()
        print("✅ Database validation complete\n")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Validation error: {e}")
        conn.close()
        return False

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
    print("=" * 60)
    print("🚀 BuildSmartOS Database Setup")
    print("=" * 60)
    
    # Create backup if database exists
    import os
    if os.path.exists(DB_NAME):
        print("\n📦 Creating backup before setup...")
        backup_database()
    
    # Create tables and indexes
    create_tables()
    
    # Add sample data
    add_dummy_data()
    
    # Validate database
    validate_database()
    
    print("=" * 60)
    print(f"🎉 System ready! Database file '{DB_NAME}' is configured.")
    print("=" * 60)
