"""
Test WhatsApp Service
Tests the WhatsApp functionality independently
"""
import sys
from whatsapp_service import WhatsAppService

def test_whatsapp_service():
    print("Testing WhatsApp Service...")
    print("-" * 50)
    
    # Initialize service
    service = WhatsAppService()
    print(f"✓ WhatsApp Service initialized")
    print(f"  - Enabled: {service.enabled}")
    print(f"  - Country Code: {service.country_code}")
    print(f"  - Send Delay: {service.send_delay} seconds")
    
    # Test phone formatting
    test_numbers = [
        "0771234567",
        "771234567",
        "+94771234567",
        "077-123-4567"
    ]
    
    print("\n✓ Phone number formatting test:")
    for num in test_numbers:
        formatted = service.format_phone_number(num)
        print(f"  {num} -> {formatted}")
    
    # Test message creation
    test_items = [
        {'name': 'Cement 50kg', 'qty': 2, 'subtotal': 3400.00},
        {'name': 'Sand per cube', 'qty': 1, 'subtotal': 5000.00}
    ]
    
    message = service.create_invoice_message(
        "BuildSmart Hardware",
        "TXN001",
        8400.00,
        test_items
    )
    
    print("\n✓ Invoice message generated:")
    print("-" * 50)
    print(message)
    print("-" * 50)
    
    # Test configuration
    print(f"\n✓ Configuration loaded:")
    print(f"  Business Name: {service.config.get('business', {}).get('name', 'N/A')}")
    print(f"  WhatsApp Enabled: {service.config.get('features', {}).get('whatsapp_enabled', False)}")
    
    print("\n" + "=" * 50)
    print("WhatsApp Service Test Complete!")
    print("=" * 50)
    print("\nNOTE: Actual sending test requires:")
    print("  1. WhatsApp Web to be logged in")
    print("  2. A valid phone number")
    print("  3. Browser automation permissions")
    print("\nTo test actual sending, use a real phone number")
    print("and ensure WhatsApp Web is accessible.")
    
    return True

if __name__ == "__main__":
    try:
        test_whatsapp_service()
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
