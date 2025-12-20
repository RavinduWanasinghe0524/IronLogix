"""
Comprehensive System Test for BuildSmartOS
Tests all critical functionality before deployment
"""
import sys
import sqlite3
import json
from datetime import datetime

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_database():
    """Test database connectivity and structure"""
    print_section("DATABASE TEST")
    try:
        conn = sqlite3.connect("buildsmart_hardware.db")
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['products', 'customers', 'transactions', 'sales_items']
        missing = [t for t in required_tables if t not in tables]
        
        if missing:
            print(f"[X] Missing tables: {', '.join(missing)}")
            return False
        
        print(f"[OK] All required tables exist: {len(tables)} tables found")
        
        # Check products
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        print(f"[OK] Products in database: {product_count}")
        
        # Check customers
        cursor.execute("SELECT COUNT(*) FROM customers")
        customer_count = cursor.fetchone()[0]
        print(f"[OK] Customers in database: {customer_count}")
        
        # Check transactions
        cursor.execute("SELECT COUNT(*) FROM transactions")
        transaction_count = cursor.fetchone()[0]
        print(f"[OK] Transactions in database: {transaction_count}")
        
        conn.close()
        print("[OK] Database test PASSED")
        return True
        
    except Exception as e:
        print(f"[X] Database test FAILED: {e}")
        return False

def test_config():
    """Test configuration file"""
    print_section("CONFIGURATION TEST")
    try:
        with open("config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Check required sections
        required = ['business', 'settings', 'features', 'whatsapp']
        missing = [s for s in required if s not in config]
        
        if missing:
            print(f"[X] Missing config sections: {', '.join(missing)}")
            return False
        
        print(f"[OK] Config loaded successfully")
        print(f"  Business: {config['business']['name']}")
        print(f"  WhatsApp Enabled: {config['features']['whatsapp_enabled']}")
        print(f"  Country Code: {config['whatsapp']['country_code']}")
        print(f"  Loyalty Enabled: {config['features']['loyalty_enabled']}")
        
        print("[OK] Configuration test PASSED")
        return True
        
    except Exception as e:
        print(f"[X] Configuration test FAILED: {e}")
        return False

def test_whatsapp():
    """Test WhatsApp service"""
    print_section("WHATSAPP SERVICE TEST")
    try:
        from whatsapp_service import WhatsAppService
        
        service = WhatsAppService()
        print(f"[OK] WhatsApp Service initialized")
        print(f"  Enabled: {service.enabled}")
        print(f"  Country Code: {service.country_code}")
        
        # Test phone formatting
        test_cases = [
            ("0771234567", "+94771234567"),
            ("+94771234567", "+94771234567"),
            ("077-123-4567", "+94771234567"),
        ]
        
        all_passed = True
        for input_num, expected in test_cases:
            result = service.format_phone_number(input_num)
            if result == expected:
                print(f"  [OK] {input_num} -> {result}")
            else:
                print(f"  [X] {input_num} -> {result} (expected {expected})")
                all_passed = False
        
        # Test message creation
        test_items = [{'name': 'Test Item', 'qty': 1, 'subtotal': 100.00}]
        message = service.create_invoice_message("Test Business", "TXN001", 100.00, test_items)
        
        if message and "Test Business" in message:
            print(f"[OK] Message creation works")
        else:
            print(f"[X] Message creation failed")
            all_passed = False
        
        if all_passed:
            print("[OK] WhatsApp service test PASSED")
        else:
            print("[X] WhatsApp service test FAILED")
        
        return all_passed
        
    except ImportError:
        print("[!]  WhatsApp service not available (pywhatkit not installed)")
        return True  # Not critical
    except Exception as e:
        print(f"[X] WhatsApp service test FAILED: {e}")
        return False

def test_imports():
    """Test all module imports"""
    print_section("MODULE IMPORT TEST")
    
    modules = {
        'customtkinter': 'Core UI',
        'sqlite3': 'Database',
        'json': 'Configuration',
        'datetime': 'Date/Time',
    }
    
    optional_modules = {
        'pywhatkit': 'WhatsApp',
        'reportlab': 'PDF Generation',
        'matplotlib': 'Analytics',
        'pandas': 'Data Analysis',
        'pyttsx3': 'Voice Assistant',
        'cv2': 'Barcode Scanner'
    }
    
    all_passed = True
    
    # Test required modules
    for module, purpose in modules.items():
        try:
            __import__(module)
            print(f"[OK] {purpose}: {module}")
        except ImportError:
            print(f"[X] {purpose}: {module} - REQUIRED")
            all_passed = False
    
    # Test optional modules
    print("\nOptional Modules:")
    for module, purpose in optional_modules.items():
        try:
            __import__(module)
            print(f"[OK] {purpose}: {module}")
        except ImportError:
            print(f"[!]  {purpose}: {module} - Optional")
    
    if all_passed:
        print("\n[OK] Core module import test PASSED")
    else:
        print("\n[X] Core module import test FAILED")
    
    return all_passed

def test_main_modules():
    """Test main application modules"""
    print_section("APPLICATION MODULES TEST")
    
    modules_to_test = [
        ('product_manager', 'Product Manager'),
        ('customer_manager', 'Customer Manager'),
        ('report_generator', 'Report Generator'),
        ('pdf_generator', 'PDF Generator'),
        ('loyalty_manager', 'Loyalty Manager'),
    ]
    
    all_passed = True
    for module_name, display_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"[OK] {display_name}")
        except ImportError as e:
            print(f"[X] {display_name}: {e}")
            all_passed = False
        except Exception as e:
            print(f"[!]  {display_name}: {e}")
    
    if all_passed:
        print("[OK] Application modules test PASSED")
    else:
        print("[X] Some application modules FAILED")
    
    return all_passed

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("     BuildSmartOS System Test")
    print("="*60)
    
    results = {}
    
    # Run tests
    results['imports'] = test_imports()
    results['config'] = test_config()
    results['database'] = test_database()
    results['whatsapp'] = test_whatsapp()
    results['modules'] = test_main_modules()
    
    # Summary
    print_section("TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for test_name, result in results.items():
        status = "[PASSED]" if result else "[FAILED]"
        print(f"{test_name.upper():20s}: {status}")
    
    print("\n" + "-"*60)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("-"*60)
    
    if failed == 0:
        print("\n[SUCCESS] ALL TESTS PASSED - System is ready for deployment!")
        return 0
    else:
        print(f"\n[FAILED] {failed} TEST(S) FAILED - Please fix issues before deployment")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
