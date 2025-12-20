"""
License Manager for BuildSmartOS
Handles trial period, activation codes, and trial reminders
"""
import json
import os
from datetime import datetime, timedelta
import hashlib
import uuid

# Master unlock code for admin/developer
MASTER_CODE = "72233559"

class LicenseManager:
    def __init__(self):
        self.license_file = "license.json"
        self.trial_days = 30
        self.license_data = self.load_license()
        self.last_reminder_file = ".last_reminder"
    
    def load_license(self):
        """Load license data from file"""
        if os.path.exists(self.license_file):
            try:
                with open(self.license_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # Create new license file for first run
        return self.create_trial_license()
    
    def create_trial_license(self):
        """Create new trial license"""
        machine_id = self.get_machine_id()
        install_date = datetime.now().isoformat()
        expiry_date = (datetime.now() + timedelta(days=self.trial_days)).isoformat()
        
        license_data = {
            "machine_id": machine_id,
            "install_date": install_date,
            "expiry_date": expiry_date,
            "trial_days": self.trial_days,
            "license_type": "trial",
            "activated": False,
            "activation_code": None,
            "activation_date": None
        }
        
        self.save_license(license_data)
        return license_data
    
    def save_license(self, data):
        """Save license data to file"""
        try:
            with open(self.license_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving license: {e}")
    
    def get_machine_id(self):
        """Get unique machine identifier"""
        try:
            # Use MAC address as machine ID
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                           for elements in range(0, 2*6, 2)][::-1])
            return hashlib.sha256(mac.encode()).hexdigest()[:16]
        except:
            return "UNKNOWN"
    
    def is_valid(self):
        """Check if license is valid"""
        # If activated with code, always valid
        if self.license_data.get("activated", False):
            return True, "Licensed"
        
        # Check trial period
        try:
            expiry_date = datetime.fromisoformat(self.license_data["expiry_date"])
            now = datetime.now()
            
            if now <= expiry_date:
                days_left = (expiry_date - now).days
                return True, f"Trial: {days_left} days remaining"
            else:
                return False, "Trial period expired"
        except:
            return False, "Invalid license"
    
    def get_days_remaining(self):
        """Get number of days remaining in trial"""
        if self.license_data.get("activated", False):
            return -1  # Unlimited
        
        try:
            expiry_date = datetime.fromisoformat(self.license_data["expiry_date"])
            now = datetime.now()
            days = (expiry_date - now).days
            return max(0, days)
        except:
            return 0
    
    def activate(self, activation_code):
        """Activate with code or master code"""
        # Check if master code
        if activation_code.strip() == MASTER_CODE:
            self.license_data["activated"] = True
            self.license_data["activation_code"] = "MASTER_CODE"
            self.license_data["activation_date"] = datetime.now().isoformat()
            self.license_data["license_type"] = "full"
            self.save_license(self.license_data)
            return True, "Master code accepted! Full access granted."
        
        # Verify activation code
        valid_code = self.generate_activation_code(self.license_data["machine_id"])
        
        if activation_code.strip().upper() == valid_code:
            self.license_data["activated"] = True
            self.license_data["activation_code"] = activation_code
            self.license_data["activation_date"] = datetime.now().isoformat()
            self.license_data["license_type"] = "full"
            self.save_license(self.license_data)
            return True, "License activated successfully!"
        else:
            return False, "Invalid activation code"
    
    def generate_activation_code(self, machine_id):
        """Generate activation code for a machine ID"""
        # Secret key - change this to your own secret
        secret = "BUILDSMART2025"
        combined = f"{machine_id}{secret}"
        code_hash = hashlib.sha256(combined.encode()).hexdigest()[:12].upper()
        
        # Format as XXXX-XXXX-XXXX
        return f"{code_hash[0:4]}-{code_hash[4:8]}-{code_hash[8:12]}"
    
    def get_license_info(self):
        """Get detailed license information"""
        info = {
            "machine_id": self.license_data.get("machine_id", "Unknown"),
            "license_type": self.license_data.get("license_type", "trial"),
            "activated": self.license_data.get("activated", False),
            "install_date": self.license_data.get("install_date", "Unknown"),
            "days_remaining": self.get_days_remaining()
        }
        
        if info["activated"]:
            info["activation_date"] = self.license_data.get("activation_date", "Unknown")
        else:
            info["expiry_date"] = self.license_data.get("expiry_date", "Unknown")
        
        return info
    
    def should_show_reminder(self):
        """Check if reminder should be shown today"""
        days_remaining = self.get_days_remaining()
        
        # Don't show reminders if activated
        if self.license_data.get("activated", False):
            return False, None
        
        # Show reminder at 10 days and every day from 5 days onwards
        if days_remaining <= 0:
            return True, "expired"
        elif days_remaining <= 5:
            return True, f"{days_remaining}_days"
        elif days_remaining == 10:
            return True, "10_days"
        
        return False, None
    
    def get_last_reminder_date(self):
        """Get the last date a reminder was shown"""
        try:
            if os.path.exists(self.last_reminder_file):
                with open(self.last_reminder_file, 'r') as f:
                    return f.read().strip()
        except:
            pass
        return None
    
    def save_reminder_date(self):
        """Save today's date as last reminder date"""
        try:
            with open(self.last_reminder_file, 'w') as f:
                f.write(datetime.now().strftime("%Y-%m-%d"))
        except:
            pass
    
    def should_show_reminder_today(self):
        """Check if we should show reminder today (not already shown)"""
        should_show, reminder_type = self.should_show_reminder()
        
        if not should_show:
            return False, None
        
        # Check if already shown today
        last_reminder = self.get_last_reminder_date()
        today = datetime.now().strftime("%Y-%m-%d")
        
        if last_reminder == today and reminder_type != "expired":
            return False, None
        
        return True, reminder_type
    
    def get_reminder_message(self, reminder_type):
        """Get reminder message based on type"""
        if reminder_type == "expired":
            return {
                "title": "Trial Period Expired",
                "message": (
                    "Your 30-day free trial has expired.\n\n"
                    "To continue using BuildSmartOS:\n\n"
                    "1. Note your Machine ID from the license dialog\n"
                    "2. Contact support: 077-XXXXXXX\n"
                    "3. Make payment: LKR 50,000 (one-time)\n"
                    "4. Receive activation code\n"
                    "5. Enter code to activate\n\n"
                    "Thank you for using BuildSmartOS!"
                ),
                "type": "error"
            }
        elif reminder_type == "10_days":
            return {
                "title": "Trial Reminder - 10 Days Left",
                "message": (
                    "Your BuildSmartOS trial will expire in 10 days.\n\n"
                    "To avoid interruption:\n\n"
                    "• Contact us early: 077-XXXXXXX\n"
                    "• Payment: LKR 50,000 (one-time)\n"
                    "• Get activation code\n"
                    "• Activate anytime before trial ends\n\n"
                    "Questions? We're here to help!"
                ),
                "type": "warning"
            }
        else:  # 5 days or less
            days = reminder_type.split("_")[0]
            return {
                "title": f"Trial Expiring - {days} Days Left!",
                "message": (
                    f"Your trial expires in {days} days.\n\n"
                    "⚠️ Action Required:\n\n"
                    "1. Contact: 077-XXXXXXX\n"
                    "2. Payment: LKR 50,000\n"
                    "3. Get activation code\n"
                    "4. Activate now\n\n"
                    "Don't lose access to your data!"
                ),
                "type": "warning"
            }
    
    def reset_trial(self, admin_code):
        """Reset trial period (admin only)"""
        # Admin code for resetting - change this to your own secret
        admin_secret = "ADMIN2025RESET"
        if admin_code == admin_secret:
            self.license_data = self.create_trial_license()
            return True, "Trial period reset successfully"
        else:
            return False, "Invalid admin code"

# Global instance
_license_manager = None

def get_license_manager():
    """Get or create license manager instance"""
    global _license_manager
    if _license_manager is None:
        _license_manager = LicenseManager()
    return _license_manager

# Tool to generate activation codes (for you to use)
def generate_code_for_machine(machine_id):
    """Generate activation code for a specific machine ID"""
    lm = LicenseManager()
    return lm.generate_activation_code(machine_id)

if __name__ == "__main__":
    # Test the license system
    lm = LicenseManager()
    print("="*60)
    print("License Manager Test")
    print("="*60)
    
    valid, msg = lm.is_valid()
    print(f"\nLicense Valid: {valid}")
    print(f"Status: {msg}")
    
    info = lm.get_license_info()
    print(f"\nMachine ID: {info['machine_id']}")
    print(f"License Type: {info['license_type']}")
    print(f"Days Remaining: {info['days_remaining']}")
    
    if not info['activated']:
        print(f"\nActivation Code for this machine:")
        print(f"{lm.generate_activation_code(info['machine_id'])}")
