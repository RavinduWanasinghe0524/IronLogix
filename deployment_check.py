"""
Pre-Deployment Final Check
Runs all tests and generates a deployment readiness report
"""
import subprocess
import sys
import json
from datetime import datetime

def run_test(test_name, test_file):
    """Run a test file and return results"""
    print(f"\nRunning {test_name}...")
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Test timed out"
    except Exception as e:
        return False, "", str(e)

def check_files_exist():
    """Check all required files exist"""
    import os
    
    required_files = [
        'main.py',
        'whatsapp_service.py',
        'config.json',
        'database_setup.py',
        'product_manager.py',
        'customer_manager.py',
        'buildsmart_hardware.db'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    return len(missing) == 0, missing

def generate_deployment_report():
    """Generate comprehensive deployment report"""
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*20 + "BuildSmartOS Deployment Readiness Report" + " "*18 + "║")
    print("╚" + "═"*78 + "╝")
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'tests': {},
        'files_check': {},
        'overall_status': 'UNKNOWN'
    }
    
    print("\n[1/4] Checking Required Files...")
    files_ok, missing_files = check_files_exist()
    report['files_check']['status'] = 'PASS' if files_ok else 'FAIL'
    report['files_check']['missing'] = missing_files
    
    if files_ok:
        print("✓ All required files present")
    else:
        print(f"❌ Missing files: {', '.join(missing_files)}")
    
    print("\n[2/4] Running System Tests...")
    success, stdout, stderr = run_test("System Test", "test_system.py")
    report['tests']['system'] = {
        'status': 'PASS' if success else 'FAIL',
        'output': stdout[:500] if stdout else stderr[:500]
    }
    
    if success:
        print("✓ System tests PASSED")
    else:
        print("❌ System tests FAILED")
    
    print("\n[3/4] Running WhatsApp Tests...")
    success, stdout, stderr = run_test("WhatsApp Test", "test_whatsapp_edge_cases.py")
    report['tests']['whatsapp'] = {
        'status': 'PASS' if success else 'FAIL',
        'output': stdout[:500] if stdout else stderr[:500]
    }
    
    if success:
        print("✓ WhatsApp tests PASSED")
    else:
        print("❌ WhatsApp tests FAILED")
    
    print("\n[4/4] Checking Configuration...")
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        config_ok = all([
            'business' in config,
            'whatsapp' in config,
            'features' in config
        ])
        
        report['config'] = {
            'status': 'PASS' if config_ok else 'FAIL',
            'whatsapp_enabled': config.get('features', {}).get('whatsapp_enabled', False)
        }
        
        if config_ok:
            print("✓ Configuration valid")
        else:
            print("❌ Configuration incomplete")
    except Exception as e:
        report['config'] = {'status': 'FAIL', 'error': str(e)}
        print(f"❌ Configuration error: {e}")
        config_ok = False
    
    # Overall status
    all_passed = (
        files_ok and
        report['tests']['system']['status'] == 'PASS' and
        report['tests']['whatsapp']['status'] == 'PASS' and
        config_ok
    )
    
    report['overall_status'] = 'READY' if all_passed else 'NOT READY'
    
    # Print summary
    print("\n" + "="*80)
    print("DEPLOYMENT READINESS SUMMARY")
    print("="*80)
    
    print(f"\nFiles Check:       {report['files_check']['status']}")
    print(f"System Tests:      {report['tests']['system']['status']}")
    print(f"WhatsApp Tests:    {report['tests']['whatsapp']['status']}")
    print(f"Configuration:     {report['config']['status']}")
    
    print("\n" + "-"*80)
    print(f"OVERALL STATUS: {report['overall_status']}")
    print("-"*80)
    
    if all_passed:
        print("\n✓ System is READY for deployment!")
        print("\nNext Steps:")
        print("1. Test with real WhatsApp number")
        print("2. Verify WhatsApp Web is logged in")
        print("3. Create backup of database")
        print("4. Train users on the system")
        print("5. Deploy to production")
    else:
        print("\n❌ System is NOT READY for deployment")
        print("\nRequired Actions:")
        if not files_ok:
            print(f"  - Install missing files: {', '.join(missing_files)}")
        if report['tests']['system']['status'] == 'FAIL':
            print("  - Fix system test failures")
        if report['tests']['whatsapp']['status'] == 'FAIL':
            print("  - Fix WhatsApp test failures")
        if not config_ok:
            print("  - Fix configuration issues")
    
    # Save report
    try:
        with open('deployment_readiness_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        print("\n📄 Detailed report saved to: deployment_readiness_report.json")
    except Exception as e:
        print(f"\n⚠️  Could not save report: {e}")
    
    return all_passed

if __name__ == "__main__":
    try:
        ready = generate_deployment_report()
        sys.exit(0 if ready else 1)
    except Exception as e:
        print(f"\n❌ Deployment check failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
