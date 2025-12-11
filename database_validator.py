import sqlite3
from datetime import datetime
import os

DB_NAME = "buildsmart_hardware.db"

class DatabaseValidator:
    """Comprehensive database validation and health check utility."""
    
    def __init__(self):
        self.db_name = DB_NAME
        self.issues = []
        self.warnings = []
        self.stats = {}
        
    def connect(self):
        """Create database connection."""
        try:
            return sqlite3.connect(self.db_name)
        except sqlite3.Error as e:
            print(f"❌ Error connecting to database: {e}")
            return None
    
    def check_database_exists(self):
        """Check if database file exists."""
        if not os.path.exists(self.db_name):
            self.issues.append("Database file does not exist")
            return False
        
        file_size = os.path.getsize(self.db_name)
        self.stats['database_size_mb'] = round(file_size / (1024 * 1024), 2)
        print(f"✅ Database exists ({self.stats['database_size_mb']} MB)")
        return True
    
    def check_schema(self):
        """Verify all required tables and columns exist."""
        conn = self.connect()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        # Required tables with their critical columns
        required_schema = {
            'products': ['id', 'name', 'price_per_unit', 'stock_quantity', 'unit_type'],
            'customers': ['id', 'phone_number', 'loyalty_points'],
            'transactions': ['id', 'date_time', 'total_amount'],
            'sales_items': ['id', 'transaction_id', 'product_id', 'quantity_sold', 'unit_price'],
            'suppliers': ['id', 'name'],
            'loyalty_transactions': ['id', 'customer_id', 'points_change'],
            'credit_sales': ['id', 'transaction_id', 'customer_id', 'balance'],
            'expenses': ['id', 'date_time', 'amount']
        }
        
        print("\n📋 Checking database schema...")
        
        # Get existing tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        schema_valid = True
        
        for table, columns in required_schema.items():
            if table not in existing_tables:
                self.issues.append(f"Missing table: {table}")
                schema_valid = False
                print(f"❌ Missing table: {table}")
            else:
                # Check columns
                cursor.execute(f"PRAGMA table_info({table})")
                existing_columns = [col[1] for col in cursor.fetchall()]
                
                missing_columns = [col for col in columns if col not in existing_columns]
                if missing_columns:
                    self.issues.append(f"Table {table} missing columns: {', '.join(missing_columns)}")
                    schema_valid = False
                    print(f"❌ Table {table} missing columns: {', '.join(missing_columns)}")
                else:
                    print(f"✅ Table {table} OK")
        
        conn.close()
        return schema_valid
    
    def check_indexes(self):
        """Verify performance indexes exist."""
        conn = self.connect()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        print("\n📊 Checking performance indexes...")
        
        # Get existing indexes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        existing_indexes = [row[0] for row in cursor.fetchall()]
        
        # Expected indexes
        expected_indexes = [
            'idx_products_name',
            'idx_products_barcode',
            'idx_customers_phone',
            'idx_transactions_date',
            'idx_sales_items_transaction',
            'idx_sales_items_product'
        ]
        
        missing_indexes = [idx for idx in expected_indexes if idx not in existing_indexes]
        
        if missing_indexes:
            self.warnings.append(f"Missing indexes: {', '.join(missing_indexes)}")
            print(f"⚠️  Missing {len(missing_indexes)} performance indexes")
            for idx in missing_indexes:
                print(f"   - {idx}")
        else:
            print(f"✅ All {len(expected_indexes)} critical indexes present")
        
        conn.close()
        return len(missing_indexes) == 0
    
    def check_data_integrity(self):
        """Check for data integrity issues."""
        conn = self.connect()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        print("\n🔍 Checking data integrity...")
        
        integrity_checks = []
        
        # Check for orphaned sales_items
        cursor.execute('''
            SELECT COUNT(*) FROM sales_items 
            WHERE product_id NOT IN (SELECT id FROM products)
        ''')
        orphaned_sales = cursor.fetchone()[0]
        if orphaned_sales > 0:
            self.issues.append(f"Found {orphaned_sales} sales items with invalid product_id")
            integrity_checks.append(f"❌ {orphaned_sales} orphaned sales items")
        else:
            integrity_checks.append("✅ No orphaned sales items")
        
        # Check for orphaned transactions
        cursor.execute('''
            SELECT COUNT(*) FROM sales_items 
            WHERE transaction_id NOT IN (SELECT id FROM transactions)
        ''')
        orphaned_transactions = cursor.fetchone()[0]
        if orphaned_transactions > 0:
            self.issues.append(f"Found {orphaned_transactions} sales items with invalid transaction_id")
            integrity_checks.append(f"❌ {orphaned_transactions} orphaned transaction references")
        else:
            integrity_checks.append("✅ No orphaned transaction references")
        
        # Check for negative stock
        cursor.execute('SELECT COUNT(*), GROUP_CONCAT(name) FROM products WHERE stock_quantity < 0')
        result = cursor.fetchone()
        negative_stock_count = result[0]
        
        if negative_stock_count > 0:
            self.warnings.append(f"Found {negative_stock_count} products with negative stock")
            integrity_checks.append(f"⚠️  {negative_stock_count} products with negative stock")
        else:
            integrity_checks.append("✅ No negative stock quantities")
        
        # Check for invalid prices
        cursor.execute('SELECT COUNT(*) FROM products WHERE price_per_unit <= 0')
        invalid_prices = cursor.fetchone()[0]
        
        if invalid_prices > 0:
            self.warnings.append(f"Found {invalid_prices} products with invalid price")
            integrity_checks.append(f"⚠️  {invalid_prices} products with zero/negative price")
        else:
            integrity_checks.append("✅ All products have valid prices")
        
        # Check for transactions with zero amount
        cursor.execute('SELECT COUNT(*) FROM transactions WHERE total_amount <= 0')
        zero_transactions = cursor.fetchone()[0]
        
        if zero_transactions > 0:
            self.warnings.append(f"Found {zero_transactions} transactions with zero/negative amounts")
            integrity_checks.append(f"⚠️  {zero_transactions} suspicious transactions")
        else:
            integrity_checks.append("✅ All transactions have valid amounts")
        
        for check in integrity_checks:
            print(f"  {check}")
        
        conn.close()
        return len(self.issues) == 0
    
    def gather_statistics(self):
        """Gather database statistics."""
        conn = self.connect()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        print("\n📈 Database Statistics:")
        
        # Product stats
        cursor.execute('SELECT COUNT(*), SUM(stock_quantity * price_per_unit) FROM products')
        product_count, inventory_value = cursor.fetchone()
        self.stats['total_products'] = product_count
        self.stats['inventory_value'] = round(inventory_value or 0, 2)
        print(f"  📦 Products: {product_count:,}")
        print(f"  💰 Inventory Value: LKR {self.stats['inventory_value']:,.2f}")
        
        # Customer stats
        cursor.execute('SELECT COUNT(*), SUM(loyalty_points) FROM customers')
        customer_count, total_points = cursor.fetchone()
        self.stats['total_customers'] = customer_count
        self.stats['total_loyalty_points'] = total_points or 0
        print(f"  👥 Customers: {customer_count:,}")
        print(f"  🎁 Loyalty Points Issued: {self.stats['total_loyalty_points']:,}")
        
        # Transaction stats
        cursor.execute('''
            SELECT COUNT(*), SUM(total_amount), AVG(total_amount) 
            FROM transactions
        ''')
        trans_count, total_revenue, avg_transaction = cursor.fetchone()
        self.stats['total_transactions'] = trans_count or 0
        self.stats['total_revenue'] = round(total_revenue or 0, 2)
        self.stats['average_transaction'] = round(avg_transaction or 0, 2)
        print(f"  🧾 Transactions: {self.stats['total_transactions']:,}")
        print(f"  💵 Total Revenue: LKR {self.stats['total_revenue']:,.2f}")
        print(f"  📊 Average Transaction: LKR {self.stats['average_transaction']:,.2f}")
        
        # Low stock items
        cursor.execute('SELECT COUNT(*) FROM products WHERE stock_quantity <= reorder_level')
        low_stock = cursor.fetchone()[0]
        self.stats['low_stock_items'] = low_stock
        print(f"  ⚠️  Low Stock Items: {low_stock}")
        
        # Recent activity
        cursor.execute('''
            SELECT COUNT(*) FROM transactions 
            WHERE date_time >= date('now', '-7 days')
        ''')
        recent_trans = cursor.fetchone()[0]
        self.stats['transactions_last_7_days'] = recent_trans
        print(f"  📅 Transactions (Last 7 days): {recent_trans}")
        
        conn.close()
    
    def generate_report(self):
        """Generate comprehensive health report."""
        print("\n" + "=" * 60)
        print("📊 DATABASE HEALTH REPORT")
        print("=" * 60)
        
        if not self.issues and not self.warnings:
            print("\n✅ DATABASE STATUS: EXCELLENT")
            print("   No critical issues or warnings found.")
        elif not self.issues:
            print("\n⚠️  DATABASE STATUS: GOOD (WITH WARNINGS)")
            print(f"   Found {len(self.warnings)} warning(s)")
        else:
            print("\n❌ DATABASE STATUS: NEEDS ATTENTION")
            print(f"   Found {len(self.issues)} critical issue(s)")
        
        if self.issues:
            print("\n🔴 Critical Issues:")
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")
        
        if self.warnings:
            print("\n🟡 Warnings:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")
        
        print("\n" + "=" * 60)
        
        return len(self.issues) == 0
    
    def auto_fix_issues(self):
        """Attempt to automatically fix common issues."""
        conn = self.connect()
        if not conn:
            return False
        
        cursor = conn.cursor()
        fixed_count = 0
        
        print("\n🔧 Attempting to auto-fix issues...")
        
        try:
            # Fix negative stock (set to 0)
            cursor.execute('UPDATE products SET stock_quantity = 0 WHERE stock_quantity < 0')
            if cursor.rowcount > 0:
                print(f"  ✅ Fixed {cursor.rowcount} products with negative stock")
                fixed_count += cursor.rowcount
            
            # Fix zero/negative prices (this is more dangerous, so we skip)
            # Just report them for manual review
            
            conn.commit()
            conn.close()
            
            if fixed_count > 0:
                print(f"\n✅ Auto-fixed {fixed_count} issue(s)")
            else:
                print("\n  No auto-fixable issues found")
            
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error during auto-fix: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def run_full_validation(self, auto_fix=False):
        """Run complete database validation."""
        print("=" * 60)
        print("🔍 BUILDSMARTPOS DATABASE VALIDATOR")
        print("=" * 60)
        
        # Check database exists
        if not self.check_database_exists():
            print("\n❌ Database validation failed: Database file not found")
            return False
        
        # Check schema
        schema_valid = self.check_schema()
        
        # Check indexes
        indexes_valid = self.check_indexes()
        
        # Check data integrity
        integrity_valid = self.check_data_integrity()
        
        # Gather statistics
        self.gather_statistics()
        
        # Auto-fix if requested
        if auto_fix and (self.issues or self.warnings):
            self.auto_fix_issues()
            # Re-check after fixes
            self.issues = []
            self.warnings = []
            self.check_data_integrity()
        
        # Generate final report
        is_healthy = self.generate_report()
        
        return is_healthy


def main():
    """Main entry point."""
    import sys
    
    validator = DatabaseValidator()
    
    # Check if auto-fix flag is provided
    auto_fix = '--fix' in sys.argv or '-f' in sys.argv
    
    if auto_fix:
        print("⚠️  Auto-fix mode enabled\n")
    
    validator.run_full_validation(auto_fix=auto_fix)
    
    print("\n💡 Tip: Run with --fix or -f flag to automatically fix common issues")
    print()


if __name__ == "__main__":
    main()
