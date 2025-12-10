import sqlite3
from datetime import datetime

DB_NAME = "buildsmart_hardware.db"

def fix_sales_items_table():
    """Add missing unit_price column to sales_items table."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Check if unit_price column exists
        cursor.execute("PRAGMA table_info(sales_items)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'unit_price' not in columns:
            print("Adding missing 'unit_price' column to sales_items table...")
            
            # Add the unit_price column with a default value
            cursor.execute('''
                ALTER TABLE sales_items 
                ADD COLUMN unit_price REAL NOT NULL DEFAULT 0
            ''')
            
            # Update existing records to calculate unit_price from sub_total and quantity_sold
            cursor.execute('''
                UPDATE sales_items 
                SET unit_price = CASE 
                    WHEN quantity_sold > 0 THEN sub_total / quantity_sold 
                    ELSE 0 
                END
            ''')
            
            conn.commit()
            print("✅ Successfully added 'unit_price' column to sales_items table!")
            print("✅ Updated existing records with calculated unit prices.")
        else:
            print("ℹ️  Column 'unit_price' already exists in sales_items table.")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Error fixing database: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Starting database fix...")
    if fix_sales_items_table():
        print("🚀 Database fix completed successfully!")
    else:
        print("⚠️  Database fix failed. Please check the error messages above.")
