"""
BuildSmartOS Startup Script
Performs system checks and launches the application
"""
import sys
import os
import sqlite3
from datetime import datetime

def print_banner():
    """Print startup banner"""
    print("\n" + "="*60)
    print("🏪 BuildSmartOS - Hardware Store Management System")
    print("="*60 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_modules = {
        'customtkinter': 'Core UI',
        'PIL': 'Image Processing',
        'reportlab': 'PDF Generation',
        'sqlite3': 'Database'
    }
    
    optional_modules = {
        'pywhatkit': 'WhatsApp Integration',
        'speech_recognition': 'Voice Commands',
        'cv2': 'Barcode Scanner',
        'matplotlib': 'Analytics',
        'pandas': 'Data Processing',
        'sklearn': 'AI Predictions'
    }
    
    missing_required = []
    missing_optional = []
    
    # Check required modules
    for module, description in required_modules.items():
        try:
            __import__(module)
            print(f"   ✅ {description}")
        except ImportError:
            print(f"   ❌ {description} (missing: {module})")
            missing_required.append(module)
    
    # Check optional modules
    for module, description in optional_modules.items():
        try:
            __import__(module)
            print(f"   ✅ {description} (optional)")
        except ImportError:
            print(f"   ⚠️ {description} (optional, missing: {module})")
            missing_optional.append(module)
    
    if missing_required:
        print(f"\n❌ Missing required dependencies: {', '.join(missing_required)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    if missing_optional:
        print(f"\n⚠️ Some optional features won't be available")
        print("   To enable all features, run: pip install -r requirements.txt")
    
    return True

def check_database():
    """Check database connection and integrity"""
    print("\n🔍 Checking database...")
    
    db_path = "buildsmart_hardware.db"
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"   ⚠️ Database not found. Creating new database...")
        try:
            from database_setup import create_tables
            create_tables()
            print(f"   ✅ Database created successfully")
        except Exception as e:
            print(f"   ❌ Failed to create database: {e}")
            return False
    else:
        print(f"   ✅ Database file found")
    
    # Test database connection
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check required tables
        required_tables = ['products', 'customers', 'transactions', 'sales_items']
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        missing_tables = [t for t in required_tables if t not in existing_tables]
        
        if missing_tables:
            print(f"   ⚠️ Missing tables: {', '.join(missing_tables)}")
            print(f"   Recreating database schema...")
            conn.close()
            
            try:
                from database_setup import create_tables
                create_tables()
                print(f"   ✅ Database schema updated")
            except Exception as e:
                print(f"   ❌ Failed to update schema: {e}")
                return False
        else:
            print(f"   ✅ All required tables present")
        
        # Check integrity
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        if result[0] == "ok":
            print(f"   ✅ Database integrity OK")
        else:
            print(f"   ⚠️ Database integrity issue: {result[0]}")
        
        conn.close()
        return True
    
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False

def check_directories():
    """Check and create required directories"""
    print("\n🔍 Checking directories...")
    
    required_dirs = {
        'backups': 'Database backups',
        'bills': 'Generated invoices',
        'reports': 'Sales reports',
        'logs': 'System logs',
        'translations': 'Language files'
    }
    
    for dir_path, description in required_dirs.items():
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
                print(f"   ✅ Created {description} directory")
            except Exception as e:
                print(f"   ⚠️ Could not create {dir_path}: {e}")
        else:
            print(f"   ✅ {description} directory exists")
    
    return True

def check_config():
    """Check configuration file"""
    print("\n🔍 Checking configuration...")
    
    config_file = "config.json"
    
    if not os.path.exists(config_file):
        print(f"   ⚠️ Config file not found. Creating default...")
        try:
            from config_manager import get_config_manager
            config_mgr = get_config_manager()
            print(f"   ✅ Default configuration created")
        except Exception as e:
            print(f"   ⚠️ Could not create config: {e}")
            print(f"   ℹ️ App will use built-in defaults")
    else:
        print(f"   ✅ Configuration file found")
    
    return True

def create_initial_backup():
    """Create an initial backup before starting"""
    print("\n📦 Creating startup backup...")
    
    try:
        from backup_manager import create_backup
        success, result = create_backup()
        if success:
            print(f"   ✅ Backup created: {result}")
        else:
            print(f"   ⚠️ Backup failed: {result}")
    except Exception as e:
        print(f"   ⚠️ Could not create backup: {e}")
    
    return True

def launch_application():
    """Launch the main application"""
    print("\n🚀 Launching BuildSmartOS...\n")
    
    try:
        from main import BuildSmartPOS
        app = BuildSmartPOS()
        app.mainloop()
    except Exception as e:
        print(f"\n❌ Failed to launch application: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    """Main startup sequence"""
    print_banner()
    
    # Perform checks
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Database", check_database),
        ("Directories", check_directories),
        ("Configuration", check_config),
        ("Backup", create_initial_backup)
    ]
    
    for check_name, check_func in checks:
        if not check_func():
            print(f"\n❌ {check_name} check failed. Please fix the issues and try again.")
            input("\nPress Enter to exit...")
            sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ All system checks passed!")
    print("="*60)
    
    # Launch application
    success = launch_application()
    
    if not success:
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
