"""
BuildSmartOS - Desktop Shortcut Creator
Creates Windows desktop shortcuts for easy access
"""

import os
import sys
from pathlib import Path

def create_shortcuts():
    """Create desktop shortcuts for BuildSmartOS"""
    
    try:
        # Get desktop path
        desktop = Path.home() / 'Desktop'
        
        # Get BuildSmartOS directory
        buildsmart_dir = Path(__file__).parent.absolute()
        python_exe = sys.executable
        
        # Create shortcuts using pywin32 (if available) or write .bat files
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            
            # 1. Main Application Shortcut
            shortcut1 = shell.CreateShortCut(str(desktop / "BuildSmartOS.lnk"))
            shortcut1.Targetpath = str(buildsmart_dir / "Run BuildSmartOS.bat")
            shortcut1.WorkingDirectory = str(buildsmart_dir)
            shortcut1.IconLocation = str(buildsmart_dir / "BuildSmartOS.ico") if (buildsmart_dir / "BuildSmartOS.ico").exists() else ""
            shortcut1.Description = "Launch BuildSmartOS POS System"
            shortcut1.save()
            print("✓ Created BuildSmartOS.lnk")
            
            # 2. Database Manager Shortcut
            shortcut2 = shell.CreateShortCut(str(desktop / "BuildSmartOS Database Manager.lnk"))
            shortcut2.Targetpath = python_exe
            shortcut2.Arguments = f'"{buildsmart_dir / "database_setup.py"}"'
            shortcut2.WorkingDirectory = str(buildsmart_dir)
            shortcut2.Description = "BuildSmartOS Database Management"
            shortcut2.save()
            print("✓ Created BuildSmartOS Database Manager.lnk")
            
            # 3. Backup Database Shortcut
            shortcut3 = shell.CreateShortCut(str(desktop / "Backup BuildSmartOS Database.lnk"))
            shortcut3.Targetpath = str(buildsmart_dir / "Backup Database.bat")
            shortcut3.WorkingDirectory = str(buildsmart_dir)
            shortcut3.Description = "Backup BuildSmartOS Database"
            shortcut3.save()
            print("✓ Created Backup BuildSmartOS Database.lnk")
            
            print("\nDesktop shortcuts created successfully!")
            return True
            
        except ImportError:
            # Fallback: Create batch file shortcuts
            print("pywin32 not available, creating batch file shortcuts...")
            
            # Create simple .bat files on desktop
            shortcuts = {
                "BuildSmartOS.bat": f'@echo off\ncd /d "{buildsmart_dir}"\ncall "Run BuildSmartOS.bat"',
                "BuildSmartOS Database.bat": f'@echo off\ncd /d "{buildsmart_dir}"\n"{python_exe}" database_setup.py\npause',
                "Backup Database.bat": f'@echo off\ncd /d "{buildsmart_dir}"\n"{python_exe}" database_setup.py\npause'
            }
            
            for name, content in shortcuts.items():
                shortcut_path = desktop / name
                with open(shortcut_path, 'w') as f:
                    f.write(content)
                print(f"✓ Created {name}")
            
            print("\nBatch file shortcuts created successfully!")
            return True
            
    except Exception as e:
        print(f"✗ Error creating shortcuts: {e}")
        return False

if __name__ == "__main__":
    print("Creating desktop shortcuts for BuildSmartOS...")
    print("="*50)
    create_shortcuts()
