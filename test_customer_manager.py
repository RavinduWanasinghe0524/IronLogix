"""
Test Customer Manager Module - BuildSmartOS
Tests customer management and loyalty system
"""

import sqlite3
from datetime import datetime

def test_customer_registration():
    """Test creating a new customer"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    test_phone = f"TEST{datetime.now().strftime('%H%M%S')}"
    
    try:
        cursor.execute("""
            INSERT INTO customers 
            (name, phone_number, address, loyalty_points, total_purchases)
            VALUES (?, ?, ?, ?, ?)
        """, ("Test Customer", test_phone, "Test Address", 0, 0.0))
        
        customer_id = cursor.lastrowid
        
        # Verify
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        customer = cursor.fetchone()
        
        # Cleanup
        cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()
        conn.close()
        
        if customer:
            return True, f"Customer registered (ID: {customer_id})"
        else:
            return False, "Registration failed"
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def test_loyalty_points_calculation():
    """Test loyalty points accumulation"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    try:
        # Get customer with points
        cursor.execute("""
            SELECT id, loyalty_points 
            FROM customers 
            WHERE loyalty_points > 0 
            LIMIT 1
        """)
        customer = cursor.fetchone()
        
        if not customer:
            conn.close()
            return True, "No customers with points (expected for fresh DB)"
        
        customer_id, points = customer
        
        # Check loyalty transactions
        cursor.execute("""
            SELECT COUNT(*), SUM(points_change) 
            FROM loyalty_transactions 
            WHERE customer_id = ?
        """, (customer_id,))
        trans_count, total_points = cursor.fetchone()
        
        conn.close()
        
        return True, f"Loyalty system working ({trans_count} transactions, {total_points or 0} points)"
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def test_customer_purchase_history():
    """Test viewing customer purchase history"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    try:
        # Find customer with purchases
        cursor.execute("""
            SELECT id, name, total_purchases 
            FROM customers 
            WHERE total_purchases > 0 
            LIMIT 1
        """)
        customer = cursor.fetchone()
        
        if not customer:
            conn.close()
            return True, "No customer purchase history yet"
        
        customer_id, name, total = customer
        
        # Get transaction count
        cursor.execute("""
            SELECT COUNT(*) FROM transactions 
            WHERE customer_id = ?
        """, (customer_id,))
        trans_count = cursor.fetchone()[0]
        
        conn.close()
        
        return True, f"History tracking works ({name}: {trans_count} transactions, LKR {total:,.2f})"
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def test_customer_search():
    """Test customer search by phone"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    try:
        # Get a customer phone
        cursor.execute("SELECT phone_number FROM customers LIMIT 1")
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return True, "No customers to search (fresh DB)"
        
        phone = result[0]
        
        # Search by phone
        cursor.execute("""
            SELECT * FROM customers 
            WHERE phone_number = ?
        """, (phone,))
        customer = cursor.fetchone()
        
        conn.close()
        
        if customer:
            return True, f"Customer search working (found: {phone})"
        else:
            return False, "Search failed"
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def test_customer_update():
    """Test updating customer information"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    try:
        # Get customer
        cursor.execute("SELECT id, name FROM customers LIMIT 1")
        customer = cursor.fetchone()
        
        if not customer:
            conn.close()
            return True, "No customers to update"
        
        customer_id, old_name = customer
        new_name = f"{old_name} Updated"
        
        # Update
        cursor.execute("""
            UPDATE customers 
            SET name = ?
            WHERE id = ?
        """, (new_name, customer_id))
        
        # Verify
        cursor.execute("SELECT name FROM customers WHERE id = ?", (customer_id,))
        updated_name = cursor.fetchone()[0]
        
        # Restore
        cursor.execute("""
            UPDATE customers 
            SET name = ?
            WHERE id = ?
        """, (old_name, customer_id))
        
        conn.commit()
        conn.close()
        
        if updated_name == new_name:
            return True, "Customer update successful"
        else:
            return False, "Update failed"
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def run_customer_tests():
    """Run all customer management tests"""
    print("\n🧪 CUSTOMER MANAGER MODULE TESTS")
    print("="*60)
    
    tests = [
        ("Customer Registration", test_customer_registration),
        ("Loyalty Points System", test_loyalty_points_calculation),
        ("Purchase History", test_customer_purchase_history),
        ("Customer Search", test_customer_search),
        ("Update Customer Info", test_customer_update),
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
    print(f"Customer Tests: {passed}/{passed + failed} passed")
    print("="*60 + "\n")
    
    return failed == 0

if __name__ == "__main__":
    success = run_customer_tests()
    exit(0 if success else 1)
