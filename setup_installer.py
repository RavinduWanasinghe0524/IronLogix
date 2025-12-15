"""
BuildSmartOS - Automated Installation Script
Handles dependency installation, database setup, and initial configuration
"""

import subprocess
import sys
import os
from pathlib import Path
import json

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.YELLOW}ℹ {text}{Colors.RESET}")

def print_step(step_num, text):
    """Print step message"""
    print(f"\n{Colors.BOLD}Step {step_num}: {text}{Colors.RESET}")

def check_python_version():
    """Check if Python version is compatible"""
    print_step(1, "Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install required Python packages"""
    print_step(2, "Installing dependencies...")
    
    # Essential packages
    essential_packages = [
        'customtkinter',
        'reportlab',
        'matplotlib',
        'pandas',
        'numpy',
        'qrcode[pil]'
    ]
    
    print_info(f"Installing {len(essential_packages)} essential packages...")
    
    try:
        # Install essential packages
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install',
            '--upgrade', '--no-cache-dir'
        ] + essential_packages)
        
        print_success("All essential packages installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print_step(3, "Creating directories...")
    
    directories = ['bills', 'reports', 'backups', 'translations']
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print_success(f"Created {directory}/ directory")
        else:
            print_info(f"{directory}/ directory already exists")
    
    return True

def setup_database(include_sample_data=True):
    """Initialize database"""
    print_step(4, "Setting up database...")
    
    try:
        # Run database setup
        result = subprocess.run([sys.executable, 'database_setup.py'],
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success("Database created successfully")
            
            if include_sample_data:
                print_info("Generating sample data for demonstration...")
                sample_result = subprocess.run([sys.executable, 'generate_test_data.py'],
                                             capture_output=True, text=True)
                
                if sample_result.returncode == 0:
                    print_success("Sample data generated")
                else:
                    print_error("Failed to generate sample data (optional)")
            
            return True
        else:
            print_error("Database setup failed")
            print(result.stderr)
            return False
            
    except Exception as e:
        print_error(f"Error setting up database: {e}")
        return False

def create_config_if_missing():
    """Create default config.json if it doesn't exist"""
    print_step(5, "Checking configuration...")
    
    config_path = Path('config.json')
    
    if config_path.exists():
        print_info("config.json already exists")
        return True
    
    print_info("Creating default config.json...")
    
    default_config = {
        "business": {
            "name": "Your Hardware Store",
            "address": "123 Main Street, Colombo, Sri Lanka",
            "phone": "077-1234567",
            "email": "info@yourstore.lk"
        },
        "settings": {
            "default_language": "english",
            "theme": "dark",
            "currency": "LKR"
        },
        "features": {
            "whatsapp_enabled": True,
            "voice_enabled": False,
            "barcode_enabled": False,
            "cloud_backup": False
        }
    }
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)
        
        print_success("Default configuration created")
        print_info("You can customize config.json with your business details")
        return True
        
    except Exception as e:
        print_error(f"Failed to create config.json: {e}")
        return False

def create_desktop_shortcuts():
    """Create desktop shortcuts (Windows)"""
    print_step(6, "Creating desktop shortcuts...")
    
    try:
        result = subprocess.run([sys.executable, 'create_shortcuts.py'],
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success("Desktop shortcuts created")
            return True
        else:
            print_info("Shortcut creation skipped (optional)")
            return True
            
    except FileNotFoundError:
        print_info("create_shortcuts.py not found (optional feature)")
        return True
    except Exception as e:
        print_info(f"Shortcut creation skipped: {e}")
        return True

def verify_installation():
    """Verify installation integrity"""
    print_step(7, "Verifying installation...")
    
    checks = []
    
    # Check database exists
    if Path('buildsmart_hardware.db').exists():
        print_success("Database file present")
        checks.append(True)
    else:
        print_error("Database file missing")
        checks.append(False)
    
    # Check config exists
    if Path('config.json').exists():
        print_success("Configuration file present")
        checks.append(True)
    else:
        print_error("Configuration file missing")
        checks.append(False)
    
    # Check directories
    for directory in ['bills', 'reports', 'backups']:
        if Path(directory).exists():
            checks.append(True)
        else:
            print_error(f"{directory}/ directory missing")
            checks.append(False)
    
    # Try importing essential packages
    try:
        import customtkinter
        import reportlab
        import matplotlib
        import pandas
        print_success("Essential packages importable")
        checks.append(True)
    except ImportError as e:
        print_error(f"Package import failed: {e}")
        checks.append(False)
    
    return all(checks)

def print_completion_message():
    """Print installation completion message"""
    print_header("Installation Complete!")
    
    print(f"{Colors.GREEN}BuildSmartOS has been successfully installed!{Colors.RESET}\n")
    
    print(f"{Colors.BOLD}Next Steps:{Colors.RESET}")
    print(f"{Colors.YELLOW}1.{Colors.RESET} Double-click 'Run BuildSmartOS.bat' to start the application")
    print(f"{Colors.YELLOW}2.{Colors.RESET} Complete the first-run configuration wizard")
    print(f"{Colors.YELLOW}3.{Colors.RESET} Customize config.json with your business details\n")
    
    print(f"{Colors.BOLD}Quick Start:{Colors.RESET}")
    print(f"  • {Colors.BLUE}python main.py{Colors.RESET} - Launch application")
    print(f"  • {Colors.BLUE}python database_setup.py{Colors.RESET} - Backup database")
    print(f"  • See {Colors.BLUE}QUICKSTART_GUIDE.md{Colors.RESET} for detailed guide\n")
    
    print(f"{Colors.BOLD}Documentation:{Colors.RESET}")
    print(f"  • USER_MANUAL.md - Complete user guide")
    print(f"  • TROUBLESHOOTING.md - Fix common issues")
    print(f"  • DEVELOPER_GUIDE.md - Technical reference\n")

def main():
    """Main installation process"""
    print_header("BuildSmartOS Installation")
    print(f"{Colors.BOLD}Sri Lanka's Smart Hardware POS System{Colors.RESET}\n")
    
    print("This installer will:")
    print("  • Check Python version compatibility")
    print("  • Install required dependencies")
    print("  • Set up database")
    print("  • Create necessary directories")
    print("  • Generate sample data")
    print("  • Create desktop shortcuts\n")
    
    input(f"{Colors.YELLOW}Press Enter to begin installation...{Colors.RESET}")
    
    # Installation steps
    steps = [
        ("Check Python version", check_python_version),
        ("Install dependencies", install_dependencies),
        ("Create directories", create_directories),
        ("Setup database", lambda: setup_database(include_sample_data=True)),
        ("Create configuration", create_config_if_missing),
        ("Create shortcuts", create_desktop_shortcuts),
        ("Verify installation", verify_installation)
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        try:
            if not step_func():
                failed_steps.append(step_name)
        except Exception as e:
            print_error(f"Error in {step_name}: {e}")
            failed_steps.append(step_name)
    
    # Final status
    print("\n" + "="*60)
    
    if not failed_steps:
        print_completion_message()
        return 0
    else:
        print_header("Installation Issues Detected")
        print_error("The following steps encountered problems:")
        for step in failed_steps:
            print(f"  • {step}")
        print(f"\n{Colors.YELLOW}See TROUBLESHOOTING.md for solutions{Colors.RESET}\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Installation cancelled by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
