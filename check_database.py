import sqlite3
from datetime import datetime
import json

DB_NAME = "buildsmart_hardware.db"

def check_database_schema():
    """Comprehensive database schema check with enhanced reporting."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        print("=" * 70)
        print("🔍 BUILDSMART DATABASE SCHEMA VERIFICATION")
        print("=" * 70)
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Database: {DB_NAME}")
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\n📊 Found {len(tables)} table(s)\n")
        
        summary_data = {
            'timestamp': datetime.now().isoformat(),
            'database': DB_NAME,
            'tables': {}
        }
        
        total_records = 0
        
        for table in tables:
            table_name = table[0]
            print(f"\n{'═' * 70}")
            print(f"📋 Table: {table_name.upper()}")
            print(f"{'═' * 70}")
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print(f"\n{'Column Name':<25} {'Type':<15} {'Not Null':<10} {'Default'}")
            print("-" * 70)
            
            column_info = []
            for col in columns:
                col_id, name, col_type, not_null, default_val, pk = col
                not_null_str = "YES" if not_null else "NO"
                default_str = str(default_val) if default_val else ""
                pk_indicator = " 🔑" if pk else ""
                print(f"{(name + pk_indicator):<25} {col_type:<15} {not_null_str:<10} {default_str}")
                
                column_info.append({
                    'name': name,
                    'type': col_type,
                    'not_null': bool(not_null),
                    'default': default_val,
                    'primary_key': bool(pk)
                })
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            total_records += count
            
            # Get indexes for this table
            cursor.execute(f"PRAGMA index_list({table_name})")
            indexes = cursor.fetchall()
            
            print(f"\n📊 Records: {count:,}")
            
            if indexes:
                print(f"📇 Indexes: {len(indexes)}")
                for idx in indexes:
                    idx_name = idx[1]
                    print(f"   - {idx_name}")
            else:
                print("📇 Indexes: None")
            
            # Get sample data for non-empty tables
            if count > 0 and count <= 5:
                print(f"\n📝 Sample Data (showing all {count} record(s)):")
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                samples = cursor.fetchall()
                for i, sample in enumerate(samples, 1):
                    print(f"   Record {i}: {sample[:3]}...")  # Show first 3 fields
            elif count > 0:
                print(f"\n📝 Sample Data (showing 3 of {count} records):")
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                samples = cursor.fetchall()
                for i, sample in enumerate(samples, 1):
                    print(f"   Record {i}: {sample[:3]}...")
            
            # Store in summary
            summary_data['tables'][table_name] = {
                'columns': column_info,
                'record_count': count,
                'indexes': [idx[1] for idx in indexes]
            }
        
        # Overall statistics
        print(f"\n{'═' * 70}")
        print("📈 OVERALL DATABASE STATISTICS")
        print(f"{'═' * 70}")
        print(f"📊 Total Tables: {len(tables)}")
        print(f"📊 Total Records: {total_records:,}")
        
        # Check for indexes
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index'")
        index_count = cursor.fetchone()[0]
        print(f"📇 Total Indexes: {index_count}")
        
        # Check for triggers
        cursor.execute("SELECT name FROM sqlite_master WHERE type='trigger'")
        triggers = [row[0] for row in cursor.fetchall()]
        trigger_count = len(triggers)
        print(f"⚡ Total Triggers: {trigger_count}")
        if triggers:
            for trg in triggers:
                print(f"   - {trg}")
        
        summary_data['triggers'] = triggers
        summary_data['stats'] = {
            'table_count': len(tables),
            'record_count': total_records,
            'index_count': index_count,
            'trigger_count': trigger_count
        }

        # Business Intelligence
        print(f"\n{'═' * 70}")
        print("💼 BUSINESS INTELLIGENCE")
        print(f"{'═' * 70}")
        
        # Revenue stats
        cursor.execute("SELECT SUM(total_amount) FROM transactions WHERE payment_status = 'Paid'")
        total_revenue = cursor.fetchone()[0] or 0
        print(f"💰 Total Revenue: LKR {total_revenue:,.2f}")
        
        # Inventory value
        cursor.execute("SELECT SUM(stock_quantity * price_per_unit) FROM products")
        inventory_value = cursor.fetchone()[0] or 0
        print(f"📦 Inventory Value: LKR {inventory_value:,.2f}")
        
        # Customer stats
        cursor.execute("SELECT COUNT(*) FROM customers")
        customer_count = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(loyalty_points) FROM customers")
        total_points = cursor.fetchone()[0] or 0
        print(f"👥 Total Customers: {customer_count:,}")
        print(f"🎁 Loyalty Points Issued: {total_points:,}")
        
        # Low stock alert
        cursor.execute("SELECT COUNT(*) FROM products WHERE stock_quantity <= reorder_level")
        low_stock = cursor.fetchone()[0]
        if low_stock > 0:
            print(f"⚠️  Low Stock Items: {low_stock}")
            cursor.execute("""
                SELECT name, stock_quantity, reorder_level 
                FROM products 
                WHERE stock_quantity <= reorder_level 
                LIMIT 5
            """)
            low_stock_items = cursor.fetchall()
            for item in low_stock_items:
                print(f"   - {item[0]}: {item[1]} (reorder at {item[2]})")
        
        conn.close()
        
        # Export summary to JSON
        try:
            with open('database_check_report.json', 'w') as f:
                json.dump(summary_data, f, indent=2)
            print(f"\n💾 Report exported to: database_check_report.json")
        except Exception as e:
            print(f"\n⚠️  Could not export report: {e}")
        
        print(f"\n{'═' * 70}")
        print("✅ Database schema check complete!")
        print(f"{'═' * 70}\n")
        
    except sqlite3.Error as e:
        print(f"❌ Error checking database: {e}")
    except FileNotFoundError:
        print(f"❌ Database file '{DB_NAME}' not found!")
        print("💡 Run 'python database_setup.py' to create the database.")

if __name__ == "__main__":
    check_database_schema()
