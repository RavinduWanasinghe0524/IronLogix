"""
License Manager for BuildSmartOS
Handles trial period and activation codes
"""
import json
import os
from datetime import datetime, timedelta
import hashlib
import uuid

class LicenseManager:
    def __init__(self):
        self.license_file = "license.json"
        self.trial_days = 30
        self.license_data = self.load_license()
    
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
        """Activate with code"""
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
