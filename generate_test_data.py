"""
Generate Test Data for BuildSmartOS
Creates realistic sample data for testing all features
"""

import sqlite3
import random
from datetime import datetime, timedelta

def generate_test_data():
    """Generate comprehensive test data for BuildSmartOS"""
    
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    print("🔧 Generating Test Data for BuildSmartOS...\n")
    
    # Clear existing test data (optional - commented out for safety)
    # cursor.execute("DELETE FROM sales_items")
    # cursor.execute("DELETE FROM transactions")
    # cursor.execute("DELETE FROM loyalty_transactions")
    # cursor.execute("DELETE FROM credit_sales")
    # cursor.execute("DELETE FROM customers WHERE phone_number LIKE 'TEST%'")
    # cursor.execute("DELETE FROM products WHERE name LIKE 'TEST%'")
    
    # =====================
    # 1. Test Products
    # =====================
    print("📦 Adding Test Products...")
    
    test_products = [
        # Cement Products
        ("Portland Cement 50kg", "Cement", 1850.00, "bag", 150, 20),
        ("Ultra Tech Cement 50kg", "Cement", 1950.00, "bag", 120, 15),
        ("Sanstha Cement 50kg", "Cement", 1800.00, "bag", 100, 15),
        
        # Paint Products
        ("Dulux White Emulsion 4L", "Paint", 4500.00, "can", 50, 10),
        ("Nippon Paint Red 4L", "Paint", 4200.00, "can", 40, 10),
        ("Asian Paints Blue 4L", "Paint", 4300.00, "can", 35, 8),
        ("Paint Brush Set", "Paint", 850.00, "set", 60, 15),
        
        # Tools
        ("Hammer 500g", "Tools", 650.00, "piece", 80, 20),
        ("Screwdriver Set 6pcs", "Tools", 1200.00, "set", 45, 10),
        ("Electric Drill Machine", "Tools", 8500.00, "piece", 25, 5),
        ("Measuring Tape 5m", "Tools", 350.00, "piece", 100, 25),
        ("Spirit Level 24inch", "Tools", 1850.00, "piece", 30, 8),
        
        # Steel & Iron
        ("Steel Rod 12mm", "Steel", 950.00, "kg", 500, 50),
        ("Steel Rod 16mm", "Steel", 980.00, "kg", 400, 50),
        ("Binding Wire 1kg", "Steel", 280.00, "kg", 200, 30),
        ("Welding Rod 3mm", "Steel", 450.00, "kg", 150, 25),
        
        # Sand & Aggregates
        ("River Sand", "Aggregates", 4500.00, "cube", 20, 3),
        ("Metal Chips", "Aggregates", 5200.00, "cube", 15, 3),
        ("Bricks Red", "Aggregates", 28.00, "piece", 5000, 500),
        
        # Electrical
        ("Electrical Wire 2.5mm", "Electrical", 85.00, "meter", 500, 50),
        ("LED Bulb 15W", "Electrical", 350.00, "piece", 120, 20),
        ("Switch Board 2-way", "Electrical", 280.00, "piece", 80, 15),
        ("Circuit Breaker 32A", "Electrical", 850.00, "piece", 50, 10),
        
        # Plumbing
        ("PVC Pipe 1inch", "Plumbing", 95.00, "foot", 300, 40),
        ("PVC Pipe 2inch", "Plumbing", 185.00, "foot", 250, 35),
        ("Elbow Joint 1inch", "Plumbing", 35.00, "piece", 200, 30),
        ("Water Tank 500L", "Plumbing", 12500.00, "piece", 15, 3),
        
        # Hardware
        ("Door Lock Set", "Hardware", 2500.00, "set", 40, 8),
        ("Window Handle", "Hardware", 450.00, "piece", 60, 12),
        ("Nails 2inch", "Hardware", 180.00, "kg", 100, 20),
        ("Screws Assorted Box", "Hardware", 650.00, "box", 75, 15),
    ]
    
    product_ids = []
    for name, category, price, unit, stock, reorder in test_products:
        try:
            cursor.execute("""
                INSERT INTO products (name, category, price_per_unit, unit_type, stock_quantity, reorder_level)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, category, price, unit, stock, reorder))
            product_ids.append(cursor.lastrowid)
        except sqlite3.IntegrityError:
            # Product might already exist
            cursor.execute("SELECT id FROM products WHERE name = ?", (name,))
            result = cursor.fetchone()
            if result:
                product_ids.append(result[0])
    
    print(f"   ✅ Added {len(product_ids)} products")
    
    # =====================
    # 2. Test Customers
    # =====================
    print("\n👥 Adding Test Customers...")
    
    test_customers = [
        ("Nimal Perera", "0771234567", "Colombo", 1500),
        ("Kamal Silva", "0772345678", "Kandy", 2500),
        ("Saman Fernando", "0773456789", "Galle", 800),
        ("Ranjith Gunasekara", "0774567890", "Negombo", 3200),
        ("Sunil Jayawardena", "0775678901", "Matara", 1200),
        ("Ajith Rajapaksa", "0776789012", "Kurunegala", 500),
        ("Pradeep Kumara", "0777890123", "Anuradhapura", 1800),
        ("Chaminda Lakmal", "0778901234", "Ratnapura", 950),
        ("Thilak Bandara", "0779012345", "Jaffna", 2100),
        ("Mahesh Weerasinghe", "0770123456", "Batticaloa", 1650),
    ]
    
    customer_ids = []
    for name, phone, address, points in test_customers:
        try:
            cursor.execute("""
                INSERT INTO customers (name, phone_number, address, loyalty_points, total_purchases)
                VALUES (?, ?, ?, ?, 0)
            """, (name, phone, address, points))
            customer_ids.append(cursor.lastrowid)
        except sqlite3.IntegrityError:
            cursor.execute("SELECT id FROM customers WHERE phone_number = ?", (phone,))
            result = cursor.fetchone()
            if result:
                customer_ids.append(result[0])
    
    print(f"   ✅ Added {len(customer_ids)} customers")
    
    # =====================
    # 3. Test Transactions
    # =====================
    print("\n💰 Generating Test Transactions...")
    
    transaction_count = 30
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)
    
    for i in range(transaction_count):
        # Random date within last 60 days
        random_days = random.randint(0, 60)
        trans_date = end_date - timedelta(days=random_days)
        date_str = trans_date.strftime("%Y-%m-%d %H:%M:%S")
        
        # Random customer (sometimes None for walk-in)
        customer_id = random.choice(customer_ids + [None, None])  # 30% walk-in
        
        # Create transaction
        cursor.execute("""
            INSERT INTO transactions (date_time, customer_id, total_amount)
            VALUES (?, ?, 0)
        """, (date_str, customer_id))
        transaction_id = cursor.lastrowid
        
        # Add 1-5 random items to transaction
        num_items = random.randint(1, 5)
        total_amount = 0
        
        for _ in range(num_items):
            product_id = random.choice(product_ids)
            
            # Get product details
            cursor.execute("""
                SELECT name, price_per_unit, stock_quantity 
                FROM products WHERE id = ?
            """, (product_id,))
            product = cursor.fetchone()
            
            if product and product[2] > 0:  # Has stock
                qty = random.randint(1, min(5, product[2]))
                unit_price = product[1]
                subtotal = qty * unit_price
                
                # Add sale item
                cursor.execute("""
                    INSERT INTO sales_items 
                    (transaction_id, product_id, quantity_sold, unit_price, sub_total)
                    VALUES (?, ?, ?, ?, ?)
                """, (transaction_id, product_id, qty, unit_price, subtotal))
                
                # Update stock
                cursor.execute("""
                    UPDATE products 
                    SET stock_quantity = stock_quantity - ?
                    WHERE id = ?
                """, (qty, product_id))
                
                total_amount += subtotal
        
        # Update transaction total
        cursor.execute("""
            UPDATE transactions 
            SET total_amount = ?
            WHERE id = ?
        """, (total_amount, transaction_id))
        
        # Add loyalty points if customer transaction
        if customer_id and total_amount > 0:
            points = int(total_amount / 100)  # 1 point per 100 LKR
            cursor.execute("""
                UPDATE customers 
                SET loyalty_points = loyalty_points + ?,
                    total_purchases = total_purchases + ?
                WHERE id = ?
            """, (points, total_amount, customer_id))
            
            cursor.execute("""
                INSERT INTO loyalty_transactions 
                (customer_id, transaction_id, points_change, description, date_time)
                VALUES (?, ?, ?, ?, ?)
            """, (customer_id, transaction_id, points, "Purchase points", date_str))
    
    print(f"   ✅ Generated {transaction_count} transactions")
    
    # =====================
    # 4. Test Credit Sales (Skip for now - requires valid transactions)
    # =====================
    print("\n💳 Skipping Credit Sales (requires transaction correlation)...")
    
    # Commit all changes
    conn.commit()
    
    # =====================
    # 5. Summary Report
    # =====================
    print("\n" + "="*50)
    print("📊 TEST DATA GENERATION COMPLETE")
    print("="*50)
    
    cursor.execute("SELECT COUNT(*) FROM products")
    print(f"   Products: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM customers")
    print(f"   Customers: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM transactions")
    print(f"   Transactions: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM sales_items")
    print(f"   Sale Items: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM credit_sales")
    print(f"   Credit Sales: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT SUM(total_amount) FROM transactions")
    total_sales = cursor.fetchone()[0] or 0
    print(f"   Total Revenue: LKR {total_sales:,.2f}")
    
    print("\n✅ Database ready for testing!\n")
    
    conn.close()

if __name__ == "__main__":
    try:
        generate_test_data()
    except Exception as e:
        print(f"\n❌ Error generating test data: {e}")
        import traceback
        traceback.print_exc()
