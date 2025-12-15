"""
Configuration Manager for BuildSmartOS
Handles loading and saving configuration from config.json and .env files
"""
import json
import os
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = {}
        load_dotenv()  # Load .env file
        self.load_config()
    
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                # Create default config
                self.config = self.get_default_config()
                self.save_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = self.get_default_config()
    
    def get_default_config(self):
        """Return default configuration"""
        return {
            "business": {
                "name": os.getenv("BUSINESS_NAME", "BuildSmart Hardware Store"),
                "address": os.getenv("BUSINESS_ADDRESS", "123 Main Street, Ratnapura"),
                "phone": os.getenv("BUSINESS_PHONE", "077-1234567"),
                "email": os.getenv("BUSINESS_EMAIL", "info@buildsmart.lk"),
                "logo_path": "assets/logo.png"
            },
            "settings": {
                "default_language": "english",
                "currency": "LKR",
                "tax_rate": 0.0,
                "theme": "dark"
            },
            "features": {
                "whatsapp_enabled": os.getenv("ENABLE_WHATSAPP", "true").lower() == "true",
                "voice_enabled": os.getenv("ENABLE_VOICE", "true").lower() == "true",
                "barcode_enabled": os.getenv("ENABLE_BARCODE", "true").lower() == "true",
                "loyalty_enabled": os.getenv("ENABLE_LOYALTY", "true").lower() == "true",
                "ai_predictions_enabled": os.getenv("ENABLE_AI_PREDICTIONS", "true").lower() == "true",
                "cloud_backup_enabled": os.getenv("ENABLE_CLOUD_BACKUP", "false").lower() == "true"
            },
            "loyalty": {
                "points_per_100_lkr": int(os.getenv("LOYALTY_POINTS_PER_100_LKR", "1")),
                "reward_threshold": int(os.getenv("LOYALTY_REWARD_THRESHOLD", "500")),
                "reward_value": int(os.getenv("LOYALTY_REWARD_VALUE", "100"))
            },
            "whatsapp": {
                "country_code": os.getenv("WHATSAPP_COUNTRY_CODE", "+94"),
                "send_delay_seconds": int(os.getenv("WHATSAPP_SEND_DELAY", "15"))
            },
            "backup": {
                "auto_backup_enabled": os.getenv("AUTO_BACKUP_ENABLED", "true").lower() == "true",
                "backup_interval_hours": int(os.getenv("AUTO_BACKUP_INTERVAL_HOURS", "24")),
                "max_backup_count": int(os.getenv("MAX_BACKUP_COUNT", "30"))
            },
            "api_keys": {
                "google_drive_credentials": os.getenv("GOOGLE_DRIVE_CREDENTIALS", ""),
                "twilio_account_sid": os.getenv("TWILIO_ACCOUNT_SID", ""),
                "twilio_auth_token": os.getenv("TWILIO_AUTH_TOKEN", "")
            }
        }
    
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, path, default=None):
        """
        Get configuration value by path (e.g., 'business.name')
        
        Args:
            path: Dot-separated path to config value
            default: Default value if not found
        
        Returns:
            Configuration value or default
        """
        keys = path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, path, value):
        """
        Set configuration value by path (e.g., 'business.name')
        
        Args:
            path: Dot-separated path to config value
            value: Value to set
        
        Returns:
            True if successful, False otherwise
        """
        keys = path.split('.')
        config = self.config
        
        # Navigate to the parent
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the value
        config[keys[-1]] = value
        return self.save_config()
    
    def reload(self):
        """Reload configuration from file"""
        self.load_config()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.get_default_config()
        return self.save_config()

# Global instance
_config_manager = None

def get_config_manager():
    """Get or create global config manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

def get_config(path, default=None):
    """Quick access to configuration values"""
    return get_config_manager().get(path, default)

def set_config(path, value):
    """Quick access to set configuration values"""
    return get_config_manager().set(path, value)
