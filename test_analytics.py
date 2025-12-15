"""
Test Analytics Dashboard - BuildSmartOS
Tests analytics calculations and data visualization capabilities
"""

import sqlite3
from datetime import datetime, timedelta

def test_sales_summary():
    """Test sales summary calculations"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    try:
        # Today's sales
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            SELECT SUM(total_amount), COUNT(*) 
            FROM transactions 
            WHERE date(date_time) = ?
        """, (today,))
        today_sales, today_count = cursor.fetchone()
        
        # This month's sales
        month_start = datetime.now().replace(day=1).strftime("%Y-%m-%d")
        cursor.execute("""
            SELECT SUM(total_amount), COUNT(*) 
            FROM transactions 
            WHERE date(date_time) >= ?
        """, (month_start,))
        month_sales, month_count = cursor.fetchone()
        
        # All time total
        cursor.execute("SELECT SUM(total_amount), COUNT(*) FROM transactions")
        total_sales, total_count = cursor.fetchone()
        
        conn.close()
        
        msg = f"Today: LKR {today_sales or 0:,.2f} ({today_count or 0} sales), "
        msg += f"Month: LKR {month_sales or 0:,.2f} ({month_count or 0} sales), "
        msg += f"Total: LKR {total_sales or 0:,.2f} ({total_count or 0} sales)"
        
        return True, msg
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def test_top_products():
    """Test top selling products analysis"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT p.name, SUM(si.quantity_sold) as total_qty, SUM(si.sub_total) as revenue
            FROM sales_items si
            JOIN products p ON si.product_id = p.id
            GROUP BY p.name
            ORDER BY total_qty DESC
            LIMIT 5
        """)
        top_products = cursor.fetchall()
        
        conn.close()
        
        if top_products:
            msg = f"Top 5 products identified: "
            msg += f"{top_products[0][0]} ({top_products[0][1]} units, LKR {top_products[0][2]:,.2f})"
            return True, msg
        else:
            return True, "No sales data yet for top products"
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def test_revenue_trends():
    """Test revenue trend analysis"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    try:
        # Last 7 days
        cursor.execute("""
            SELECT date(date_time) as sale_date, SUM(total_amount) as daily_total
            FROM transactions
            WHERE date(date_time) >= date('now', '-7 days')
            GROUP BY sale_date
            ORDER BY sale_date DESC
        """)
        daily_sales = cursor.fetchall()
        
        conn.close()
        
        if daily_sales:
            return True, f"Trend analysis working ({len(daily_sales)} days of data)"
        else:
            return True, "No recent sales for trend analysis"
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def test_avg_transaction_value():
    """Test average transaction calculations"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT AVG(total_amount), MIN(total_amount), MAX(total_amount)
            FROM transactions
        """)
        avg, min_val, max_val = cursor.fetchone()
        
        conn.close()
        
        if avg:
            msg = f"Avg: LKR {avg:,.2f}, Min: LKR {min_val:,.2f}, Max: LKR {max_val:,.2f}"
            return True, msg
        else:
            return True, "No transactions for average calculation"
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def test_category_performance():
    """Test category-wise sales performance"""
    conn = sqlite3.connect("buildsmart_hardware.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT p.category, SUM(si.sub_total) as category_revenue, COUNT(*) as item_count
            FROM sales_items si
            JOIN products p ON si.product_id = p.id
            WHERE p.category IS NOT NULL
            GROUP BY p.category
            ORDER BY category_revenue DESC
        """)
        categories = cursor.fetchall()
        
        conn.close()
        
        if categories:
            top_cat = categories[0]
            return True, f"Top category: {top_cat[0]} (LKR {top_cat[1]:,.2f}, {top_cat[2]} items)"
        else:
            return True, "No category data yet"
    except Exception as e:
        conn.close()
        return False, f"Error: {e}"

def test_matplotlib_available():
    """Test if matplotlib is available for charting"""
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        return True, f"Matplotlib {matplotlib.__version__} available for charts"
    except ImportError:
        return False, "Matplotlib not available"

def test_pandas_available():
    """Test if pandas is available for data analysis"""
    try:
        import pandas as pd
        import numpy as np
        return True, f"Pandas {pd.__version__} and NumPy {np.__version__} available"
    except ImportError:
        return False, "Pandas/NumPy not available"

def run_analytics_tests():
    """Run all analytics tests"""
    print("\n🧪 ANALYTICS DASHBOARD TESTS")
    print("="*60)
    
    tests = [
        ("Sales Summary", test_sales_summary),
        ("Top Products Analysis", test_top_products),
        ("Revenue Trends", test_revenue_trends),
        ("Average Transaction", test_avg_transaction_value),
        ("Category Performance", test_category_performance),
        ("Matplotlib Availability", test_matplotlib_available),
        ("Pandas Availability", test_pandas_available),
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
    print(f"Analytics Tests: {passed}/{passed + failed} passed")
    print("="*60 + "\n")
    
    return failed == 0

if __name__ == "__main__":
    success = run_analytics_tests()
    exit(0 if success else 1)
