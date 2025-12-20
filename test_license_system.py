"""
Quick Test for License System
"""
import os
from license_manager import LicenseManager

def test_license_system():
    print("\n" + "="*60)
    print("  License System Test")
    print("="*60)
    
    lm = LicenseManager()
    
    # Test 1: Check if license file created
    print("\n[Test 1] License file creation")
    if os.path.exists("license.json"):
        print("  [OK] License file exists")
    else:
        print("  [FAIL] License file not found")
    
    # Test 2: Check trial validity
    print("\n[Test 2] Trial period check")
    valid, status = lm.is_valid()
    print(f"  Status: {status}")
    if valid:
        print("  [OK] License is valid")
    else:
        print("  [FAIL] License is invalid")
    
    # Test 3: Get license info
    print("\n[Test 3] License information")
    info = lm.get_license_info()
    print(f"  Machine ID: {info['machine_id']}")
    print(f"  License Type: {info['license_type']}")
    print(f"  Days Remaining: {info['days_remaining']}")
    print(f"  Activated: {info['activated']}")
    
    # Test 4: Generate activation code
    print("\n[Test 4] Activation code generation")
    code = lm.generate_activation_code(info['machine_id'])
    print(f"  Generated Code: {code}")
    print("  [OK] Code generated successfully")
    
    # Test 5: Test activation
    print("\n[Test 5] License activation")
    success, message = lm.activate(code)
    if success:
        print(f"  [OK] {message}")
    else:
        print(f"  [FAIL] {message}")
    
    # Test 6: Verify activation
    print("\n[Test 6] Verify activation")
    valid, status = lm.is_valid()
    print(f"  Status: {status}")
    if valid and status == "Licensed":
        print("  [OK] License activated and verified")
    else:
        print("  [FAIL] Activation verification failed")
    
    print("\n" + "="*60)
    print("License System Test Complete!")
    print("="*60)
    
    # Show final status
    final_info = lm.get_license_info()
    print(f"\nFinal Status:")
    print(f"  License Type: {final_info['license_type']}")
    print(f"  Activated: {final_info['activated']}")
    if final_info['activated']:
        print(f"  Activation Date: {final_info.get('activation_date', 'Unknown')}")
    
    return True

if __name__ == "__main__":
    test_license_system()
    input("\nPress Enter to exit...")
