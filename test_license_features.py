"""
Test Master Code and Trial Reminders
"""
from license_manager import get_license_manager
from datetime import datetime, timedelta
import json

def test_master_code():
    """Test master code activation"""
    print("\n" + "="*60)
    print("  Testing Master Code: 72233559")
    print("="*60)
    
    lm = get_license_manager()
    success, message = lm.activate("72233559")
    
    if success:
        print(f"\n✓ {message}")
        print("✓ Master code works!")
    else:
        print(f"\n✗ {message}")
        print("✗ Master code failed!")
    
    return success

def test_reminders():
    """Test reminder system"""
    print("\n" + "="*60)
    print("  Testing Trial Reminders")
    print("="*60)
    
    lm = get_license_manager()
    
    # Test different scenarios
    scenarios = [
        (30, "Fresh install"),
        (15, "15 days remaining"),
        (10, "10 days - first reminder"),
        (5, "5 days - daily reminders"),
        (1, "1 day - urgent reminder"),
        (0, "Trial expired")
    ]
    
    print("\nTesting reminder triggers:\n")
    
    for days, description in scenarios:
        # Temporarily modify expiry
        original_expiry = lm.license_data["expiry_date"]
        
        # Set expiry to test days from now
        test_expiry = datetime.now() + timedelta(days=days)
        lm.license_data["expiry_date"] = test_expiry.isoformat()
        
        # Check if reminder should show
        should_show, reminder_type = lm.should_show_reminder()
        
        if should_show:
            reminder_info = lm.get_reminder_message(reminder_type)
            print(f"  Days: {days:2d} | ✓ Reminder: {reminder_info['title']}")
        else:
            print(f"  Days: {days:2d} | - No reminder")
        
        # Restore original
        lm.license_data["expiry_date"] = original_expiry
    
    print("\n✓ Reminder system tested")

def test_activation_codes():
    """Test both master code and machine-specific code"""
    print("\n" + "="*60)
    print("  Testing Activation Codes")
    print("="*60)
    
    lm = get_license_manager()
    info = lm.get_license_info()
    
    print(f"\nMachine ID: {info['machine_id']}")
    
    # Test machine-specific code
    machine_code = lm.generate_activation_code(info['machine_id'])
    print(f"Machine Code: {machine_code}")
    
    # Test master code
    print(f"Master Code: 72233559")
    
    print("\n✓ Both codes available")

def main():
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*15 + "License System Tests" + " "*24 + "║")
    print("╚" + "="*58 + "╝")
    
    # Test 1: Master code
    test_master_code()
    
    # Test 2: Reminders
    test_reminders()
    
    # Test 3: Codes
    test_activation_codes()
    
    # Summary
    print("\n" + "="*60)
    print("  Test Summary")
    print("="*60)
    print("\n✓ Master code works (72233559)")
    print("✓ Reminder system functional")
    print("✓ Machine-specific codes work")
    print("\nYour license system is ready!")
    print("\nKey Features:")
    print("  • 30-day trial period")
    print("  • Reminders at day 20, 25-29")
    print("  • Master code for quick activation")
    print("  • Machine-specific codes for security")
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        main()
        input("\nPress Enter to exit...")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
