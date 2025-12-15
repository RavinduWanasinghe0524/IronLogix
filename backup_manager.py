"""
Automatic Backup Manager for BuildSmartOS
Handles scheduled database backups and cleanup of old backups
"""
import os
import shutil
import sqlite3
from datetime import datetime, timedelta
import threading
import time
from config_manager import get_config

# Try to import schedule for automated backups
try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False
    print("⚠️ schedule not available - automated backups disabled")

class BackupManager:
    def __init__(self, db_path="buildsmart_hardware.db", backup_dir="backups"):
        self.db_path = db_path
        self.backup_dir = backup_dir
        self.running = False
        self.backup_thread = None
        
        # Create backup directory if it doesn't exist
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self):
        """Create a backup of the database"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"buildsmart_backup_{timestamp}.db"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # Create backup using SQLite backup API for safety
            source = sqlite3.connect(self.db_path)
            dest = sqlite3.connect(backup_path)
            
            source.backup(dest)
            
            source.close()
            dest.close()
            
            print(f"✅ Backup created: {backup_path}")
            
            # Cleanup old backups
            self.cleanup_old_backups()
            
            return True, backup_path
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False, str(e)
    
    def cleanup_old_backups(self):
        """Remove old backups beyond max count"""
        try:
            max_backups = get_config("backup.max_backup_count", 30)
            
            # Get all backup files
            backups = []
            for filename in os.listdir(self.backup_dir):
                if filename.startswith("buildsmart_backup_") and filename.endswith(".db"):
                    filepath = os.path.join(self.backup_dir, filename)
                    backups.append((filepath, os.path.getmtime(filepath)))
            
            # Sort by modification time (newest first)
            backups.sort(key=lambda x: x[1], reverse=True)
            
            # Remove old backups
            if len(backups) > max_backups:
                for filepath, _ in backups[max_backups:]:
                    try:
                        os.remove(filepath)
                        print(f"🗑️ Removed old backup: {os.path.basename(filepath)}")
                    except Exception as e:
                        print(f"Error removing backup {filepath}: {e}")
        
        except Exception as e:
            print(f"Error during backup cleanup: {e}")
    
    def restore_backup(self, backup_path):
        """Restore database from a backup file"""
        try:
            if not os.path.exists(backup_path):
                return False, "Backup file not found"
            
            # Create a backup of current database before restoring
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            current_backup = f"buildsmart_before_restore_{timestamp}.db"
            shutil.copy2(self.db_path, os.path.join(self.backup_dir, current_backup))
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            
            print(f"✅ Database restored from: {backup_path}")
            print(f"📦 Previous database saved as: {current_backup}")
            
            return True, "Restore successful"
        except Exception as e:
            return False, str(e)
    
    def list_backups(self):
        """List all available backups"""
        try:
            backups = []
            for filename in os.listdir(self.backup_dir):
                if filename.startswith("buildsmart_backup_") and filename.endswith(".db"):
                    filepath = os.path.join(self.backup_dir, filename)
                    file_size = os.path.getsize(filepath)
                    modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    backups.append({
                        'filename': filename,
                        'filepath': filepath,
                        'size_mb': file_size / (1024 * 1024),
                        'date': modified_time
                    })
            
            # Sort by date (newest first)
            backups.sort(key=lambda x: x['date'], reverse=True)
            return backups
        except Exception as e:
            print(f"Error listing backups: {e}")
            return []
    
    def schedule_automatic_backups(self):
        """Schedule automatic backups based on configuration"""
        if not SCHEDULE_AVAILABLE:
            print("⚠️ schedule module not available - automatic backups disabled")
            print("   Install with: pip install schedule")
            return
        
        if not get_config("backup.auto_backup_enabled", True):
            print("⚠️ Automatic backups are disabled in configuration")
            return
        
        interval_hours = get_config("backup.backup_interval_hours", 24)
        
        # Schedule backup
        schedule.every(interval_hours).hours.do(self.create_backup)
        
        # Also backup daily at 2 AM
        schedule.every().day.at("02:00").do(self.create_backup)
        
        print(f"📅 Automatic backups scheduled every {interval_hours} hours")
        
        # Run scheduler in background thread
        self.running = True
        self.backup_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.backup_thread.start()
    
    def _run_scheduler(self):
        """Run the scheduler in background"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def stop_automatic_backups(self):
        """Stop automatic backup scheduler"""
        self.running = False
        if SCHEDULE_AVAILABLE:
            schedule.clear()
        print("🛑 Automatic backups stopped")

# Global instance
_backup_manager = None

def get_backup_manager():
    """Get or create global backup manager instance"""
    global _backup_manager
    if _backup_manager is None:
        _backup_manager = BackupManager()
    return _backup_manager

def create_backup():
    """Quick backup function"""
    return get_backup_manager().create_backup()

def restore_backup(backup_path):
    """Quick restore function"""
    return get_backup_manager().restore_backup(backup_path)

def list_backups():
    """Quick list backups function"""
    return get_backup_manager().list_backups()
