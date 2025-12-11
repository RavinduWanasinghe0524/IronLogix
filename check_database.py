import sqlite3

DB_NAME = "buildsmart_hardware.db"

def check_database_schema():
    """Comprehensive database schema check"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        print("="*60)
        print("DATABASE SCHEMA VERIFICATION")
        print("="*60)
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\nFound {len(tables)} tables:\n")
        
        for table in tables:
            table_name = table[0]
            print(f"\n{'='*60}")
            print(f"Table: {table_name}")
            print(f"{'='*60}")
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print(f"{'Column Name':<20} {'Type':<15} {'Not Null':<10} {'Default'}")
            print("-"*60)
            for col in columns:
                col_id, name, col_type, not_null, default_val, pk = col
                not_null_str = "YES" if not_null else "NO"
                default_str = str(default_val) if default_val else ""
                print(f"{name:<20} {col_type:<15} {not_null_str:<10} {default_str}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"\nRecords: {count}")
        
        conn.close()
        print(f"\n{'='*60}")
        print("✅ Database schema check complete!")
        print(f"{'='*60}\n")
        
    except sqlite3.Error as e:
        print(f"❌ Error checking database: {e}")

if __name__ == "__main__":
    check_database_schema()
