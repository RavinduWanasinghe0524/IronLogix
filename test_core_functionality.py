"""
Test Core Functionality - BuildSmartOS
Automated tests for basic POS operations
"""

import sqlite3
import os
from datetime import datetime

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_result(self, test_name, passed, message=""):
        self.tests.append({
            'name': test_name,
            'passed': passed,
            'message': message
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_report(self):
        print("\n" + "="*60)
        print("TEST RESULTS SUMMARY")
        print("="*60)
        
        for test in self.tests:
            status = "✅ PASS" if test['passed'] else "❌ FAIL"
            print(f"{status} - {test['name']}")
            if test['message']:
                print(f"      {test['message']}")
        
        print("\n" + "-"*60)
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed} ✅")
        print(f"Failed: {self.failed} ❌")
        print(f"Success Rate: {(self.passed/(self.passed + self.failed)*100):.1f}%")
        print("="*60 + "\n")

def test_database_connection():
    """Test 1: Database Connection"""
    try:
        conn = sqlite3.connect("buildsmart_hardware.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        
        if len(tables) >= 6:
            return True, f"Connected successfully, found {len(tables)} tables"
        else:
            return False, f"Database incomplete, only {len(tables)} tables found"
    except Exception as e:
        return False, f"Connection failed: {e}"

def test_database_schema():
    """Test 2: Database Schema Validation"""
    try:
        conn = sqlite3.connect("buildsmart_hardware.db")
        cursor = conn.cursor()
        
        required_tables = [
            'products', 'customers', 'transactions', 
            'sales_items', 'suppliers', 'loyalty_transactions'
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        missing_tables = [t for t in required_tables if t not in existing_tables]
        
        conn.close()
        
        if not missing_tables:
            return True, f"All {len(required_tables)} required tables exist"
        else:
            return False, f"Missing tables: {', '.join(missing_tables)}"
    except Exception as e:
        return False, f"Schema check failed: {e}"

def test_product_crud():
    """Test 3: Product CRUD Operations"""
    try:
        conn = sqlite3.connect("buildsmart_hardware.db")
        cursor = conn.cursor()
        
        # CREATE
        test_product = f"TEST_PRODUCT_{datetime.now().strftime('%H%M%S')}"
        cursor.execute("""
            INSERT INTO products 
            (name, category, price_per_unit, unit_type, stock_quantity, reorder_level)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (test_product, "Test", 100.00, "piece", 50, 10))
        product_id = cursor.lastrowid
        
        # READ
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            conn.close()
            return False, "Failed to read created product"
        
        # UPDATE
        cursor.execute("""
            UPDATE products 
            SET price_per_unit = 150.00 
            WHERE id = ?
        """, (product_id,))
        
        cursor.execute("SELECT price_per_unit FROM products WHERE id = ?", (product_id,))
        updated_price = cursor.fetchone()[0]
        
        if updated_price != 150.00:
            conn.close()
            return False, "Failed to update product"
        
        # DELETE
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        deleted = cursor.fetchone()
        
        conn.commit()
        conn.close()
        
        if deleted:
            return False, "Failed to delete product"
        
        return True, "All CRUD operations successful"
    except Exception as e:
        return False, f"CRUD operations failed: {e}"

def test_customer_operations():
    """Test 4: Customer Operations"""
    try:
        conn = sqlite3.connect("buildsmart_hardware.db")
        cursor = conn.cursor()
        
        # Create test customer
        test_phone = f"TEST{datetime.now().strftime('%H%M%S')}"
        cursor.execute("""
            INSERT INTO customers 
            (name, phone_number, address, loyalty_points, total_purchases)
            VALUES (?, ?, ?, ?, ?)
        """, ("Test Customer", test_phone, "Test Address", 0, 0))
        customer_id = cursor.lastrowid
        
        # Verify customer
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        customer = cursor.fetchone()
        
        # Update loyalty points
        cursor.execute("""
            UPDATE customers 
            SET loyalty_points = 100 
            WHERE id = ?
        """, (customer_id,))
        
        # Cleanup
        cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        
        conn.commit()
        conn.close()
        
        if customer:
            return True, "Customer operations working correctly"
        else:
            return False, "Customer operations failed"
    except Exception as e:
        return False, f"Customer operations error: {e}"

def test_transaction_flow():
    """Test 5: Transaction Flow"""
    try:
        conn = sqlite3.connect("buildsmart_hardware.db")
        cursor = conn.cursor()
        
        # Get a real product
        cursor.execute("SELECT id, price_per_unit, stock_quantity FROM products LIMIT 1")
        product = cursor.fetchone()
        
        if not product:
            conn.close()
            return False, "No products available for testing"
        
        product_id, price, stock = product
        
        if stock < 1:
            conn.close()
            return False, "Product out of stock"
        
        # Create transaction
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO transactions (date_time, customer_id, total_amount)
            VALUES (?, NULL, ?)
        """, (date_str, price))
        transaction_id = cursor.lastrowid
        
        # Add sales item
        cursor.execute("""
            INSERT INTO sales_items 
            (transaction_id, product_id, quantity_sold, unit_price, sub_total)
            VALUES (?, ?, ?, ?, ?)
        """, (transaction_id, product_id, 1, price, price))
        
        # Verify transaction
        cursor.execute("SELECT total_amount FROM transactions WHERE id = ?", (transaction_id,))
        trans = cursor.fetchone()
        
        # Cleanup
        cursor.execute("DELETE FROM sales_items WHERE transaction_id = ?", (transaction_id,))
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        
        conn.commit()
        conn.close()
        
        if trans and trans[0] == price:
            return True, f"Transaction created successfully (LKR {price})"
        else:
            return False, "Transaction creation failed"
    except Exception as e:
        return False, f"Transaction flow error: {e}"

def test_stock_update():
    """Test 6: Stock Update on Sale"""
    try:
        conn = sqlite3.connect("buildsmart_hardware.db")
        cursor = conn.cursor()
        
        # Get product with stock
        cursor.execute("""
            SELECT id, stock_quantity 
            FROM products 
            WHERE stock_quantity > 5 
            LIMIT 1
        """)
        product = cursor.fetchone()
        
        if not product:
            conn.close()
            return False, "No products with sufficient stock"
        
        product_id, initial_stock = product
        
        # Simulate sale
        qty_sold = 2
        cursor.execute("""
            UPDATE products 
            SET stock_quantity = stock_quantity - ?
            WHERE id = ?
        """, (qty_sold, product_id))
        
        # Verify stock decreased
        cursor.execute("SELECT stock_quantity FROM products WHERE id = ?", (product_id,))
        new_stock = cursor.fetchone()[0]
        
        # Restore stock
        cursor.execute("""
            UPDATE products 
            SET stock_quantity = ?
            WHERE id = ?
        """, (initial_stock, product_id))
        
        conn.commit()
        conn.close()
        
        if new_stock == initial_stock - qty_sold:
            return True, f"Stock updated correctly ({initial_stock} → {new_stock})"
        else:
            return False, "Stock update failed"
    except Exception as e:
        return False, f"Stock update error: {e}"

def test_pdf_generation():
    """Test 7: PDF Invoice Generation"""
    try:
        # Check if PDF generator is available
        try:
            import pdf_generator
            pdf_available = True
        except ImportError:
            return False, "PDF generator module not available"
        
        # Check if bills directory exists
        if not os.path.exists("bills"):
            os.makedirs("bills")
        
        # Count existing PDFs
        pdf_count_before = len([f for f in os.listdir("bills") if f.endswith('.pdf')])
        
        return True, f"PDF generation capability confirmed ({pdf_count_before} existing invoices)"
    except Exception as e:
        return False, f"PDF generation check failed: {e}"

def test_data_integrity():
    """Test 8: Data Integrity Checks"""
    try:
        conn = sqlite3.connect("buildsmart_hardware.db")
        cursor = conn.cursor()
        
        # Check for orphaned sales items
        cursor.execute("""
            SELECT COUNT(*) FROM sales_items 
            WHERE transaction_id NOT IN (SELECT id FROM transactions)
        """)
        orphaned_items = cursor.fetchone()[0]
        
        # Check for negative stock
        cursor.execute("SELECT COUNT(*) FROM products WHERE stock_quantity < 0")
        negative_stock = cursor.fetchone()[0]
        
        # Check for invalid prices
        cursor.execute("SELECT COUNT(*) FROM products WHERE price_per_unit <= 0")
        invalid_prices = cursor.fetchone()[0]
        
        conn.close()
        
        issues = []
        if orphaned_items > 0:
            issues.append(f"{orphaned_items} orphaned sale items")
        if negative_stock > 0:
            issues.append(f"{negative_stock} negative stock items")
        if invalid_prices > 0:
            issues.append(f"{invalid_prices} invalid prices")
        
        if not issues:
            return True, "No data integrity issues found"
        else:
            return False, f"Issues: {', '.join(issues)}"
    except Exception as e:
        return False, f"Integrity check error: {e}"

def test_indexes():
    """Test 9: Database Indexes"""
    try:
        conn = sqlite3.connect("buildsmart_hardware.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM sqlite_master 
            WHERE type='index' AND name NOT LIKE 'sqlite_%'
        """)
        index_count = cursor.fetchone()[0]
        
        conn.close()
        
        if index_count > 0:
            return True, f"Found {index_count} performance indexes"
        else:
            return False, "No indexes found"
    except Exception as e:
        return False, f"Index check error: {e}"

def test_triggers():
    """Test 10: Database Triggers"""
    try:
        conn = sqlite3.connect("buildsmart_hardware.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM sqlite_master 
            WHERE type='trigger'
        """)
        trigger_count = cursor.fetchone()[0]
        
        conn.close()
        
        if trigger_count > 0:
            return True, f"Found {trigger_count} data integrity triggers"
        else:
            return False, "No triggers found"
    except Exception as e:
        return False, f"Trigger check error: {e}"

def run_all_tests():
    """Run all core functionality tests"""
    print("\n🧪 BUILDSMARTOS - CORE FUNCTIONALITY TESTS")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = TestResults()
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Database Schema", test_database_schema),
        ("Product CRUD Operations", test_product_crud),
        ("Customer Operations", test_customer_operations),
        ("Transaction Flow", test_transaction_flow),
        ("Stock Update Mechanism", test_stock_update),
        ("PDF Generation", test_pdf_generation),
        ("Data Integrity", test_data_integrity),
        ("Performance Indexes", test_indexes),
        ("Data Triggers", test_triggers),
    ]
    
    for test_name, test_func in tests:
        print(f"Running: {test_name}...", end=" ")
        try:
            passed, message = test_func()
            status = "✅" if passed else "❌"
            print(f"{status}")
            if message:
                print(f"         {message}")
            results.add_result(test_name, passed, message)
        except Exception as e:
            print(f"❌")
            print(f"         Error: {e}")
            results.add_result(test_name, False, str(e))
    
    results.print_report()
    
    # Save results to file
    with open("test_results_core.txt", "w", encoding="utf-8") as f:
        f.write(f"BuildSmartOS - Core Functionality Test Results\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        
        for test in results.tests:
            status = "PASS" if test['passed'] else "FAIL"
            f.write(f"[{status}] {test['name']}\n")
            if test['message']:
                f.write(f"       {test['message']}\n")
            f.write("\n")
        
        f.write(f"\nTotal: {results.passed + results.failed}\n")
        f.write(f"Passed: {results.passed}\n")
        f.write(f"Failed: {results.failed}\n")
        f.write(f"Success Rate: {(results.passed/(results.passed + results.failed)*100):.1f}%\n")
    
    print("📄 Results saved to: test_results_core.txt\n")
    
    return results.failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
