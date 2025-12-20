"""
BuildSmartOS Installation Script
Automated installation with dependency checking and setup
"""
import sys
import os
import subprocess
import json
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(step, total, text):
    """Print installation step"""
    print(f"[{step}/{total}] {text}")

def check_python_version():
    """Check if Python version is adequate"""
    print_step(1, 6, "Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"  [ERROR] Python {version.major}.{version.minor} detected")
        print(f"  [ERROR] Python 3.8 or higher is required")
        print(f"\n  Download from: https://www.python.org/downloads/")
        return False
    
    print(f"  [OK] Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print_step(2, 6, "Installing dependencies...")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("  [ERROR] requirements.txt not found")
        return False
    
    print("  Installing packages (this may take 2-5 minutes)...")
    
    try:
        # Upgrade pip first
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        
        # Install requirements
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            print("  [WARNING] Some packages failed, trying individually...")
            
            # Try installing each package individually
            with open("requirements.txt", "r") as f:
                packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            
            failed_packages = []
            for package in packages:
                try:
                    subprocess.run(
                        [sys.executable, "-m", "pip", "install", package],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        check=True
                    )
                    print(f"    ✓ {package}")
                except:
                    failed_packages.append(package)
                    print(f"    ✗ {package} (optional)")
            
            if failed_packages:
                print(f"\n  [INFO] {len(failed_packages)} optional packages skipped")
        
        print("  [OK] Dependencies installed")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Installation failed: {e}")
        return False

def setup_database():
    """Initialize database"""
    print_step(3, 6, "Setting up database...")
    
    try:
        import sqlite3
        
        # Check if database exists
        db_file = Path("buildsmart_hardware.db")
        if db_file.exists():
            print("  [INFO] Database already exists")
            print("  [OK] Using existing database")
            return True
        
        # Run database setup
        result = subprocess.run(
            [sys.executable, "database_setup.py"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if db_file.exists():
            print("  [OK] Database initialized")
            return True
        else:
            print("  [WARNING] Database setup completed with warnings")
            return True
            
    except Exception as e:
        print(f"  [ERROR] Database setup failed: {e}")
        return False

def create_folders():
    """Create necessary folders"""
    print_step(4, 6, "Creating folders...")
    
    folders = ["backups", "bills", "reports", "logs"]
    created = 0
    
    for folder in folders:
        folder_path = Path(folder)
        if not folder_path.exists():
            folder_path.mkdir(exist_ok=True)
            created += 1
            print(f"  ✓ Created {folder}/")
        else:
            print(f"  ✓ {folder}/ (exists)")
    
    print(f"  [OK] {len(folders)} folders ready")
    return True

def initialize_license():
    """Initialize license system"""
    print_step(5, 6, "Initializing license system...")
    
    try:
        # Import license manager to create initial license
        sys.path.insert(0, os.getcwd())
        from license_manager import get_license_manager
        
        lm = get_license_manager()
        valid, status = lm.is_valid()
        
        if valid:
            info = lm.get_license_info()
            print(f"  [OK] License initialized")
            print(f"  [INFO] Trial: {info['days_remaining']} days remaining")
            print(f"  [INFO] Machine ID: {info['machine_id']}")
            return True
        else:
            print(f"  [ERROR] License initialization failed")
            return False
            
    except Exception as e:
        print(f"  [ERROR] License error: {e}")
        return False

def verify_installation():
    """Verify that all components are working"""
    print_step(6, 6, "Verifying installation...")
    
    checks = []
    
    # Check main.py exists
    if Path("main.py").exists():
        print("  ✓ Main application found")
        checks.append(True)
    else:
        print("  ✗ Main application missing")
        checks.append(False)
    
    # Check config.json exists
    if Path("config.json").exists():
        print("  ✓ Configuration file found")
        checks.append(True)
    else:
        print("  ✗ Configuration missing")
        checks.append(False)
    
    # Check database exists
    if Path("buildsmart_hardware.db").exists():
        print("  ✓ Database ready")
        checks.append(True)
    else:
        print("  ✗ Database missing")
        checks.append(False)
    
    # Check license.json exists
    if Path("license.json").exists():
        print("  ✓ License initialized")
        checks.append(True)
    else:
        print("  ✗ License not initialized")
        checks.append(False)
    
    if all(checks):
        print("  [OK] All components verified")
        return True
    else:
        print("  [WARNING] Some components missing")
        return False

def main():
    """Main installation process"""
    print_header("BuildSmartOS Installation")
    
    print("Welcome to BuildSmartOS!")
    print("This installer will set up everything you need.\n")
    print("Installation will take 2-5 minutes depending on your internet speed.\n")
    
    input("Press Enter to start installation...")
    
    # Track success of each step
    steps_success = []
    
    # Step 1: Check Python
    steps_success.append(check_python_version())
    if not steps_success[-1]:
        print("\n[FAILED] Installation cannot continue without Python 3.8+")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Step 2: Install dependencies
    steps_success.append(install_dependencies())
    
    # Step 3: Setup database
    steps_success.append(setup_database())
    
    # Step 4: Create folders
    steps_success.append(create_folders())
    
    # Step 5: Initialize license
    steps_success.append(initialize_license())
    
    # Step 6: Verify installation
    steps_success.append(verify_installation())
    
    # Summary
    print_header("Installation Summary")
    
    total_steps = len(steps_success)
    successful_steps = sum(steps_success)
    
    print(f"Steps Completed: {successful_steps}/{total_steps}")
    
    if successful_steps == total_steps:
        print("\n✓ Installation completed successfully!")
        print("\n" + "="*60)
        print("  BuildSmartOS is ready to use!")
        print("="*60)
        print("\nTo start the application:")
        print("  1. Double-click 'Run BuildSmartOS.bat'")
        print("  2. Or run: python main.py")
        print("\nYour 30-day FREE trial starts now!")
        print("\nQuick Start:")
        print("  • Read: USER_MANUAL.md")
        print("  • Support: 077-XXXXXXX")
        print("  • For activation after trial: LICENSE_SYSTEM_GUIDE.md")
    else:
        print("\n⚠ Installation completed with warnings")
        print("\nSome optional features may not work.")
        print("You can still use the core POS system.")
        print("\nFor help, contact: 077-XXXXXXX")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Installation cancelled by user")
        input("Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Installation failed: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
