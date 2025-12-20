"""
Quick Test Suite for BuildSmartOS
Run this before giving the system to ensure everything works
"""
import sys
import os

def main():
    print("\n" + "="*70)
    print("  BuildSmartOS Quick Test - Pre-Delivery Check")
    print("="*70)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Database exists
    print("\n[Test 1] Checking database...")
    tests_total += 1
    if os.path.exists("buildsmart_hardware.db"):
        print("  [OK] Database file found")
        tests_passed += 1
    else:
        print("  [FAIL] Database file missing")
    
    # Test 2: Config exists
    print("\n[Test 2] Checking configuration...")
    tests_total += 1
    if os.path.exists("config.json"):
        print("  [OK] Configuration file found")
        tests_passed += 1
    else:
        print("  [FAIL] Configuration file missing")
    
    # Test 3: Core modules import
    print("\n[Test 3] Testing core modules...")
    tests_total += 1
    try:
        import customtkinter
        import sqlite3
        from whatsapp_service import WhatsAppService
        print("  [OK] All core modules import successfully")
        tests_passed += 1
    except Exception as e:
        print(f"  [FAIL] Module import error: {e}")
    
    # Test 4: Database connectivity
    print("\n[Test 4] Testing database connectivity...")
    tests_total += 1
    try:
        import sqlite3
        conn = sqlite3.connect("buildsmart_hardware.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"  [OK] Database accessible ({count} products)")
        tests_passed += 1
    except Exception as e:
        print(f"  [FAIL] Database error: {e}")
    
    # Test 5: WhatsApp service
    print("\n[Test 5] Testing WhatsApp service...")
    tests_total += 1
    try:
        from whatsapp_service import WhatsAppService
        ws = WhatsAppService()
        test_phone = ws.format_phone_number("0771234567")
        if test_phone == "+94771234567":
            print("  [OK] WhatsApp service functional")
            tests_passed += 1
        else:
            print(f"  [FAIL] Phone formatting incorrect: {test_phone}")
    except Exception as e:
        print(f"  [FAIL] WhatsApp service error: {e}")
    
    # Test 6: PDF Generator
    print("\n[Test 6] Testing PDF generator...")
    tests_total += 1
    try:
        import pdf_generator
        print("  [OK] PDF generator available")
        tests_passed += 1
    except Exception as e:
        print(f"  [FAIL] PDF generator error: {e}")
    
    # Summary
    print("\n" + "="*70)
    print(f"TEST RESULTS: {tests_passed}/{tests_total} tests passed")
    print("="*70)
    
    if tests_passed == tests_total:
        print("\n[SUCCESS] All tests passed! System is ready for delivery.")
        print("\nFinal Steps:")
        print("  1. Test with real WhatsApp number (make sure WhatsApp Web is logged in)")
        print("  2. Process a test transaction")
        print("  3. Verify PDF generation works")
        print("  4. Create database backup")
        print("  5. Brief the user on the system")
        return 0
    else:
        print(f"\n[WARNING] {tests_total - tests_passed} test(s) failed.")
        print("Please fix issues before delivery.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
