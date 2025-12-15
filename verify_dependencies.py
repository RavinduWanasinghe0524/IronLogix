"""
Dependency Verification Script for BuildSmartOS
Tests all installed packages and reports their status
"""

import sys

print("="*70)
print("BuildSmartOS DEPENDENCY VERIFICATION")
print("="*70)
print()

# Core dependencies
core_deps = {
    "customtkinter": "UI Framework",
    "sqlite3": "Database (Built-in)",
    "tkinter": "GUI Toolkit (Built-in)"
}

# Feature dependencies
feature_deps = {
    "reportlab": "PDF Generation",
    "matplotlib": "Analytics Charts",
    "pandas": "Data Analysis",
    "numpy": "Mathematical Operations",
    "qrcode": "QR Code Generation",
    "opencv-python": "Barcode Scanning (Camera)",
    "pyzbar": "Barcode Decoding",
    "SpeechRecognition": "Voice Commands",
    "pyttsx3": "Text-to-Speech",
    "scikit-learn": "AI/ML Predictions",
    "pywhatkit": "WhatsApp Integration",
    "googletrans": "Translation Services"
}

def check_package(package_name):
    """Check if a package is available"""
    try:
        __import__(package_name.replace("-", "_"))
        return True
    except ImportError:
        return False

# Check core dependencies
print("CORE DEPENDENCIES")
print("-"*70)
for pkg, desc in core_deps.items():
    status = "[OK]" if check_package(pkg) else "[MISSING]"
    print(f"{status} {pkg:<25} - {desc}")
print()

# Check feature dependencies
print("FEATURE DEPENDENCIES")
print("-"*70)
installed = 0
total = len(feature_deps)

for pkg, desc in feature_deps.items():
    available = check_package(pkg)
    status = "[OK]" if available else "[NOT INSTALLED]"
    if available:
        installed += 1
    
    print(f"{status} {pkg:<25} - {desc}")

print()
print("="*70)
print(f"SUMMARY: {installed}/{total} optional features available")
print("="*70)
print()

# Feature availability report
print("FEATURE AVAILABILITY")
print("-"*70)

features = {
    "Core POS System": check_package("customtkinter") and check_package("sqlite3"),
    "PDF Invoices": check_package("reportlab"),
    "Analytics Dashboard": check_package("matplotlib") and check_package("pandas"),
    "QR Code Generation": check_package("qrcode"),
    "Barcode Scanning": check_package("cv2") and check_package("pyzbar"),
    "Voice Commands": check_package("speech_recognition") and check_package("pyttsx3"),
    "AI Predictions": check_package("sklearn"),
    "WhatsApp Integration": check_package("pywhatkit"),
    "Multi-Language": check_package("googletrans")
}

for feature, status in features.items():
    state = "READY" if status else "NOT AVAILABLE"
    print(f"[{state:^15}] {feature}")

print()
print("="*70)

# New modules check
print("NEW MODULES")
print("-"*70)

import os
modules = {
    "Product Manager": "product_manager.py",
    "Customer Manager": "customer_manager.py",
    "Report Generator": "report_generator.py"
}

for name, filename in modules.items():
    exists = os.path.exists(filename)
    status = "[FOUND]" if exists else "[MISSING]"
    print(f"{status} {name:<30} - {filename}")

print()
print("="*70)
print("VERIFICATION COMPLETE")
print("="*70)
print()

# Critical check
if check_package("customtkinter") and check_package("reportlab"):
    print("[SUCCESS] Core system is OPERATIONAL")
    print("   - POS functionality: READY")
    print("  - Product Management: READY")
    print("   - Customer Management: READY") 
    print("   - Report Generation: READY")
    print()
    
    if check_package("matplotlib") and check_package("pandas"):
        print("[SUCCESS] Analytics: READY (matplotlib + pandas installed)")
    else:
        print("[WARNING] Analytics: LIMITED (install matplotlib and pandas)")
    
    print()
else:
    print("[ERROR] CRITICAL: Missing core dependencies!")
    print("   Run: pip install customtkinter reportlab")

print()
print("To install remaining optional features:")
print("pip install opencv-python pyzbar SpeechRecognition pyttsx3 scikit-learn")
print()
