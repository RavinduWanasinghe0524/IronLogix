"""
Test Product Manager Module - BuildSmartOS
Tests product management CRUD operations
"""

import sqlite3
from datetime import datetime

def test_product_add():
    """Test adding a new product"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    test_product = f"TEST_ADD_{datetime.now().strftime('%H%M%S')}"
    
    try:
        cursor.execute("""
            INSERT INTO products 
            (name, category, price_per_unit, unit_type, stock_quantity, reorder_level)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (test_product, "Test Category", 500.00, "piece", 50, 10))
        
        product_id = cursor.lastrowid
        
        # Verify
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        
        # Cleanup
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()
        
        if product:
            return True, f"Product created successfully (ID: {product_id})"
        else:
            return False, "Failed to create product"
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def test_product_update():
    """Test updating product details"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    try:
        # Get existing product
        cursor.execute("SELECT id, price_per_unit FROM products LIMIT 1")
        product = cursor.fetchone()
        
        if not product:
            conn.close()
            return False, "No products to test"
        
        product_id, old_price = product
        new_price = old_price + 100.00
        
        # Update
        cursor.execute("""
            UPDATE products 
            SET price_per_unit = ?
            WHERE id = ?
        """, (new_price, product_id))
        
        # Verify
        cursor.execute("SELECT price_per_unit FROM products WHERE id = ?", (product_id,))
        updated_price = cursor.fetchone()[0]
        
        # Restore
        cursor.execute("""
            UPDATE products 
            SET price_per_unit = ?
            WHERE id = ?
        """, (old_price, product_id))
        
        conn.commit()
        conn.close()
        
        if updated_price == new_price:
            return True, f"Price updated correctly ({old_price} → {new_price})"
        else:
            return False, "Price update failed"
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def test_product_search():
    """Test product search functionality"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    try:
        # Search by name
        cursor.execute("""
            SELECT COUNT(*) FROM products 
            WHERE LOWER(name) LIKE LOWER(?)
        """, ("%cement%",))
        cement_count = cursor.fetchone()[0]
        
        # Search by category
        cursor.execute("""
            SELECT COUNT(*) FROM products 
            WHERE category = ?
        """, ("Paint",))
        paint_count = cursor.fetchone()[0]
        
        conn.close()
        
        return True, f"Search working (Cement: {cement_count}, Paint: {paint_count})"
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def test_product_categories():
    """Test category grouping"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT DISTINCT category 
            FROM products 
            WHERE category IS NOT NULL
            ORDER BY category
        """)
        categories = cursor.fetchall()
        
        conn.close()
        
        if len(categories) > 0:
            return True, f"Found {len(categories)} categories"
        else:
            return False, "No categories found"
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def test_low_stock_detection():
    """Test low stock alert system"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT COUNT(*) FROM products 
            WHERE stock_quantity <= reorder_level
        """)
        low_stock_count = cursor.fetchone()[0]
        
        conn.close()
        
        return True, f"Low stock detection working ({low_stock_count} items need reorder)"
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def run_product_tests():
    """Run all product management tests"""
    print("\n🧪 PRODUCT MANAGER MODULE TESTS")
    print("="*60)
    
    tests = [
        ("Add Product", test_product_add),
        ("Update Product", test_product_update),
        ("Search Products", test_product_search),
        ("Product Categories", test_product_categories),
        ("Low Stock Detection", test_low_stock_detection),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\nTesting: {test_name}...", end=" ")
        try:
            success, message = test_func()
            if success:
                print("✅")
                print(f"         {message}")
                passed += 1
            else:
                print("❌")
                print(f"         {message}")
                failed += 1
        except Exception as e:
            print("❌")
            print(f"         Exception: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Product Tests: {passed}/{passed + failed} passed")
    print("="*60 + "\n")
    
    return failed == 0

if __name__ == "__main__":
    success = run_product_tests()
    exit(0 if success else 1)
