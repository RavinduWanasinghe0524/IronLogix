"""
System Health Monitor for BuildSmartOS
Monitors system health, database integrity, and disk space
"""
import os
import sqlite3
from datetime import datetime
from config_manager import get_config

# Try to import psutil for system monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️ psutil not available - system monitoring features limited")

class HealthMonitor:
    def __init__(self, db_path="buildsmart_hardware.db"):
        self.db_path = db_path
        self.health_status = {}
    
    def check_database_health(self):
        """Check database integrity and accessibility"""
        issues = []
        
        try:
            # Check if database exists
            if not os.path.exists(self.db_path):
                issues.append("❌ Database file not found")
                return False, issues
            
            # Check if database is accessible
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Run integrity check
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            
            if result[0] != "ok":
                issues.append(f"❌ Database integrity check failed: {result[0]}")
            
            # Check table existence
            required_tables = ['products', 'customers', 'transactions', 'sales_items']
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            for table in required_tables:
                if table not in existing_tables:
                    issues.append(f"❌ Missing required table: {table}")
            
            # Check database size
            db_size_mb = os.path.getsize(self.db_path) / (1024 * 1024)
            if db_size_mb > 1000:  # Warn if DB > 1GB
                issues.append(f"⚠️ Large database size: {db_size_mb:.2f} MB")
            
            conn.close()
            
            if not issues:
                return True, ["✅ Database health check passed"]
            else:
                return False, issues
        
        except Exception as e:
            issues.append(f"❌ Database error: {str(e)}")
            return False, issues
    
    def check_disk_space(self):
        """Check available disk space"""
        issues = []
        
        if not PSUTIL_AVAILABLE:
            issues.append("⚠️ psutil not installed - disk space check unavailable")
            return False, issues
        
        try:
            # Get disk usage for current directory
            disk = psutil.disk_usage(os.path.dirname(os.path.abspath(self.db_path)))
            
            free_space_gb = disk.free / (1024 ** 3)
            percent_used = disk.percent
            
            if percent_used > 90:
                issues.append(f"❌ Critical: Disk space {percent_used}% full")
            elif percent_used > 80:
                issues.append(f"⚠️ Warning: Disk space {percent_used}% full")
            
            if free_space_gb < 1:
                issues.append(f"❌ Critical: Only {free_space_gb:.2f} GB free")
            elif free_space_gb < 5:
                issues.append(f"⚠️ Warning: Only {free_space_gb:.2f} GB free")
            
            if not issues:
                issues.append(f"✅ Disk space: {free_space_gb:.2f} GB free ({100-percent_used:.1f}% available)")
            
            return len([i for i in issues if i.startswith("❌")]) == 0, issues
        
        except Exception as e:
            return False, [f"❌ Disk space check failed: {str(e)}"]
    
    def check_memory_usage(self):
        """Check system memory usage"""
        issues = []
        
        if not PSUTIL_AVAILABLE:
            issues.append("⚠️ psutil not installed - memory check unavailable")
            return False, issues
        
        try:
            memory = psutil.virtual_memory()
            percent_used = memory.percent
            available_gb = memory.available / (1024 ** 3)
            
            if percent_used > 90:
                issues.append(f"❌ Critical: Memory {percent_used}% full")
            elif percent_used > 80:
                issues.append(f"⚠️ Warning: Memory {percent_used}% full")
            
            if available_gb < 0.5:
                issues.append(f"❌ Low memory: {available_gb:.2f} GB available")
            
            if not issues:
                issues.append(f"✅ Memory: {available_gb:.2f} GB available ({100-percent_used:.1f}% free)")
            
            return len([i for i in issues if i.startswith("❌")]) == 0, issues
        
        except Exception as e:
            return False, [f"❌ Memory check failed: {str(e)}"]
    
    def check_backup_health(self):
        """Check backup status"""
        issues = []
        
        try:
            backup_dir = "backups"
            
            if not os.path.exists(backup_dir):
                issues.append("⚠️ No backup directory found")
                return False, issues
            
            # Get latest backup
            backups = []
            for filename in os.listdir(backup_dir):
                if filename.startswith("buildsmart_backup_") and filename.endswith(".db"):
                    filepath = os.path.join(backup_dir, filename)
                    backups.append((filepath, os.path.getmtime(filepath)))
            
            if not backups:
                issues.append("⚠️ No backups found")
                return False, issues
            
            # Check latest backup age
            latest_backup = max(backups, key=lambda x: x[1])
            latest_backup_time = datetime.fromtimestamp(latest_backup[1])
            hours_old = (datetime.now() - latest_backup_time).total_seconds() / 3600
            
            if hours_old > 48:
                issues.append(f"⚠️ Latest backup is {hours_old:.1f} hours old")
            else:
                issues.append(f"✅ Latest backup: {hours_old:.1f} hours ago")
            
            issues.append(f"✅ Total backups: {len(backups)}")
            
            return True, issues
        
        except Exception as e:
            return False, [f"❌ Backup check failed: {str(e)}"]
    
    def run_full_health_check(self):
        """Run all health checks"""
        print("🏥 Running System Health Check...\n")
        
        results = {}
        
        # Database health
        print("📊 Checking Database Health...")
        db_ok, db_issues = self.check_database_health()
        results['database'] = {'ok': db_ok, 'issues': db_issues}
        for issue in db_issues:
            print(f"   {issue}")
        print()
        
        # Disk space
        print("💾 Checking Disk Space...")
        disk_ok, disk_issues = self.check_disk_space()
        results['disk'] = {'ok': disk_ok, 'issues': disk_issues}
        for issue in disk_issues:
            print(f"   {issue}")
        print()
        
        # Memory
        print("🧠 Checking Memory Usage...")
        mem_ok, mem_issues = self.check_memory_usage()
        results['memory'] = {'ok': mem_ok, 'issues': mem_issues}
        for issue in mem_issues:
            print(f"   {issue}")
        print()
        
        # Backups
        print("📦 Checking Backup Status...")
        backup_ok, backup_issues = self.check_backup_health()
        results['backups'] = {'ok': backup_ok, 'issues': backup_issues}
        for issue in backup_issues:
            print(f"   {issue}")
        print()
        
        # Summary
        all_ok = all(r['ok'] for r in results.values())
        critical_issues = sum(1 for r in results.values() 
                            for issue in r['issues'] 
                            if issue.startswith("❌"))
        
        if all_ok:
            print("✅ All health checks passed!")
        else:
            print(f"⚠️ Health check completed with {critical_issues} critical issue(s)")
        
        return results
    
    def get_system_stats(self):
        """Get system statistics"""
        stats = {}
        
        try:
            # Database size
            if os.path.exists(self.db_path):
                stats['db_size_mb'] = os.path.getsize(self.db_path) / (1024 * 1024)
            
            if PSUTIL_AVAILABLE:
                # Disk usage
                disk = psutil.disk_usage(os.path.dirname(os.path.abspath(self.db_path)))
                stats['disk_total_gb'] = disk.total / (1024 ** 3)
                stats['disk_used_gb'] = disk.used / (1024 ** 3)
                stats['disk_free_gb'] = disk.free / (1024 ** 3)
                stats['disk_percent'] = disk.percent
                
                # Memory usage
                memory = psutil.virtual_memory()
                stats['memory_total_gb'] = memory.total / (1024 ** 3)
                stats['memory_available_gb'] = memory.available / (1024 ** 3)
                stats['memory_percent'] = memory.percent
                
                # CPU usage
                stats['cpu_percent'] = psutil.cpu_percent(interval=1)
            else:
                stats['note'] = 'Install psutil for system monitoring'
            
        except Exception as e:
            print(f"Error getting system stats: {e}")
        
        return stats

# Global instance
_health_monitor = None

def get_health_monitor():
    """Get or create global health monitor instance"""
    global _health_monitor
    if _health_monitor is None:
        _health_monitor = HealthMonitor()
    return _health_monitor

def run_health_check():
    """Quick health check function"""
    return get_health_monitor().run_full_health_check()

if __name__ == "__main__":
    # Run health check when script is executed directly
    run_health_check()
