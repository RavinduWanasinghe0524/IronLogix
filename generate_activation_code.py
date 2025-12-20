"""
Code Generator Tool for BuildSmartOS
Use this to generate activation codes for customers
"""
from license_manager import LicenseManager
import sys

def main():
    print("\n" + "="*60)
    print("  BuildSmartOS - Activation Code Generator")
    print("="*60)
    
    print("\nThis tool generates activation codes for customers.")
    print("You need the customer's Machine ID to generate a code.\n")
    
    lm = LicenseManager()
    
    choice = input("Choose option:\n1. Generate code for Machine ID\n2. Get my own Machine ID\n\nEnter choice (1 or 2): ")
    
    if choice == "1":
        machine_id = input("\nEnter customer's Machine ID: ").strip()
        if machine_id:
            code = lm.generate_activation_code(machine_id)
            print("\n" + "="*60)
            print(f"Activation Code: {code}")
            print("="*60)
            print("\nSend this code to the customer.")
            print("They can enter it in the license activation dialog.")
        else:
            print("Invalid Machine ID")
    
    elif choice == "2":
        machine_id = lm.get_machine_id()
        print("\n" + "="*60)
        print(f"Your Machine ID: {machine_id}")
        print("="*60)
        print("\nCustomers should send this ID to you to get activation code.")
        
        # Also show the code for this machine
        code = lm.generate_activation_code(machine_id)
        print(f"\nActivation Code for this machine: {code}")
    
    else:
        print("Invalid choice")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
