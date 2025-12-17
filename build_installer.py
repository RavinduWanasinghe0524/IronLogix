"""
BuildSmartOS - Automated Build Script
Creates standalone executable using PyInstaller
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def build_executable():
    """Build standalone executable with PyInstaller"""
    print_header("BuildSmartOS - Build Process")
    
    print("Step 1: Installing PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    print("\nStep 2: Creating version info...")
    create_version_info()
    
    print("\nStep 3: Building executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=BuildSmartOS",
        "--onefile",  # Single file
        "--windowed",  # No console
        "--add-data=config.json;.",
        "--add-data=translations;translations",
        "--add-data=database_setup.py;.",
        "--add-data=first_run_wizard.py;.",
        "--hidden-import=customtkinter",
        "--hidden-import=PIL._imagingt",
        "--hidden-import=reportlab.pdfgen",
        "main.py"
    ]
    
    subprocess.run(cmd, check=True)
    
    print("\n✅ Build complete!")
    print(f"\n📦 Executable location: dist\\BuildSmartOS.exe")
    print(f"📊 Size: ~{os.path.getsize('dist/BuildSmartOS.exe') / (1024*1024):.1f} MB")

def create_version_info():
    """Create version information file"""
    version_info = """
# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'BuildSmart Technologies'),
        StringStruct(u'FileDescription', u'BuildSmartOS - Hardware POS System'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'BuildSmartOS'),
        StringStruct(u'LegalCopyright', u'© 2024 BuildSmart Technologies'),
        StringStruct(u'OriginalFilename', u'BuildSmartOS.exe'),
        StringStruct(u'ProductName', u'BuildSmartOS'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    with open('version_info.txt', 'w') as f:
        f.write(version_info)

if __name__ == "__main__":
    try:
        build_executable()
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)
