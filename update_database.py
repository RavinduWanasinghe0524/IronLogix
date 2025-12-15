"""
Update existing database to add customer_phone column to transactions
"""
import sqlite3

DB_NAME = "buildsmart_hardware.db"

def update_database():
    """Add customer_phone column to transactions table"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(transactions)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'customer_phone' not in columns:
            print("Adding customer_phone column to transactions table...")
            cursor.execute("ALTER TABLE transactions ADD COLUMN customer_phone TEXT")
            conn.commit()
            print("✅ Column added successfully!")
        else:
            print("✅ Column already exists")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_database()
