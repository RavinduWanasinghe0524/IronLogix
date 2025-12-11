"""
Error handling and logging utilities for BuildSmartOS.
Provides centralized error handling, logging, and crash recovery.
"""

import logging
import traceback
import os
from datetime import datetime
from functools import wraps
import json

# Create logs directory if it doesn't exist
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Configure logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Error log
error_logger = logging.getLogger('error')
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'error_log.txt'), encoding='utf-8')
error_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
error_logger.addHandler(error_handler)

# Transaction log
transaction_logger = logging.getLogger('transaction')
transaction_logger.setLevel(logging.INFO)
transaction_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'transaction_log.txt'), encoding='utf-8')
transaction_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
transaction_logger.addHandler(transaction_handler)

# Audit trail
audit_logger = logging.getLogger('audit')
audit_logger.setLevel(logging.INFO)
audit_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'audit_trail.txt'), encoding='utf-8')
audit_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
audit_logger.addHandler(audit_handler)

# System log
system_logger = logging.getLogger('system')
system_logger.setLevel(logging.INFO)
system_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'system_log.txt'), encoding='utf-8')
system_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
system_logger.addHandler(system_handler)


def log_error(error, context="", show_traceback=True):
    """
    Log an error with context information.
    
    Args:
        error: The exception object
        context: Additional context about where/when the error occurred
        show_traceback: Whether to include full traceback in log
    """
    error_msg = f"{context}: {str(error)}"
    error_logger.error(error_msg)
    
    if show_traceback:
        error_logger.error(traceback.format_exc())
    
    return error_msg


def log_transaction(transaction_id, customer_id, amount, items_count, payment_method="Cash"):
    """Log a successful transaction."""
    transaction_logger.info(
        f"Transaction #{transaction_id} | Customer: {customer_id or 'Walk-in'} | "
        f"Amount: LKR {amount:.2f} | Items: {items_count} | Payment: {payment_method}"
    )


def log_audit(action, user="System", details=""):
    """Log an audit trail event."""
    audit_logger.info(f"Action: {action} | User: {user} | Details: {details}")


def log_system(message, level="INFO"):
    """Log a system event."""
    if level == "INFO":
        system_logger.info(message)
    elif level == "WARNING":
        system_logger.warning(message)
    elif level == "ERROR":
        system_logger.error(message)


def handle_exception(exc_type, exc_value, exc_traceback):
    """
    Global exception handler for uncaught exceptions.
    Can be set as sys.excepthook.
    """
    if issubclass(exc_type, KeyboardInterrupt):
        # Don't log keyboard interrupts
        return
    
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    error_logger.critical(f"UNCAUGHT EXCEPTION:\n{error_msg}")
    
    # Save crash report
    crash_report = {
        'timestamp': datetime.now().isoformat(),
        'type': exc_type.__name__,
        'message': str(exc_value),
        'traceback': error_msg
    }
    
    crash_file = os.path.join(LOGS_DIR, f"crash_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(crash_file, 'w') as f:
        json.dump(crash_report, f, indent=2)
    
    print(f"\n❌ A critical error occurred. Details saved to {crash_file}")


def safe_execute(func):
    """
    Decorator to wrap functions in try-except and log errors.
    Returns None if function fails.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_error(e, f"Error in {func.__name__}")
            return None
    return wrapper


def safe_database_operation(func):
    """
    Decorator for database operations that need transaction support.
    Automatically rolls back on error.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # If func has a connection parameter, try to rollback
            if 'conn' in kwargs:
                conn = kwargs['conn']
            elif len(args) > 0 and hasattr(args[0], 'rollback'):
                conn = args[0]
            
            if conn:
                try:
                    conn.rollback()
                    log_system("Database transaction rolled back", "WARNING")
                except:
                    pass
            
            log_error(e, f"Database error in {func.__name__}")
            raise
    return wrapper


class ErrorRecovery:
    """Handles automatic recovery from common errors."""
    
    @staticmethod
    def save_cart_state(cart_items, customer_info=None):
        """Save current cart state for recovery."""
        try:
            recovery_file = os.path.join(LOGS_DIR, 'cart_recovery.json')
            state = {
                'timestamp': datetime.now().isoformat(),
                'cart_items': cart_items,
                'customer_info': customer_info
            }
            with open(recovery_file, 'w') as f:
                json.dump(state, f, indent=2)
            log_system("Cart state saved for recovery")
            return True
        except Exception as e:
            log_error(e, "Error saving cart state")
            return False
    
    @staticmethod
    def load_cart_state():
        """Load saved cart state."""
        try:
            recovery_file = os.path.join(LOGS_DIR, 'cart_recovery.json')
            if os.path.exists(recovery_file):
                with open(recovery_file, 'r') as f:
                    state = json.load(f)
                log_system("Cart state recovered")
                return state
        except Exception as e:
            log_error(e, "Error loading cart state")
        return None
    
    @staticmethod
    def clear_cart_state():
        """Clear saved cart state after successful checkout."""
        try:
            recovery_file = os.path.join(LOGS_DIR, 'cart_recovery.json')
            if os.path.exists(recovery_file):
                os.remove(recovery_file)
                log_system("Cart recovery state cleared")
        except Exception as e:
            log_error(e, "Error clearing cart state")


class InputValidator:
    """Validates user inputs before database operations."""
    
    @staticmethod
    def validate_quantity(quantity, max_quantity=None):
        """Validate product quantity."""
        try:
            qty = float(quantity)
            if qty <= 0:
                return False, "Quantity must be greater than 0"
            if max_quantity and qty > max_quantity:
                return False, f"Quantity exceeds available stock ({max_quantity})"
            return True, qty
        except ValueError:
            return False, "Invalid quantity format"
    
    @staticmethod
    def validate_phone_number(phone):
        """Validate Sri Lankan phone number."""
        # Remove spaces and dashes
        phone = phone.replace(" ", "").replace("-", "")
        
        # Check if it's a valid Sri Lankan number
        if len(phone) < 9:
            return False, "Phone number too short"
        
        # Sri Lankan mobile numbers start with 07 or +947
        if phone.startswith('+94'):
            phone = '0' + phone[3:]
        
        if not phone.startswith('0'):
            return False, "Phone number must start with 0 or +94"
        
        if len(phone) != 10:
            return False, "Phone number must be 10 digits"
        
        if not phone.isdigit():
            return False, "Phone number must contain only digits"
        
        return True, phone
    
    @staticmethod
    def validate_price(price):
        """Validate price value."""
        try:
            price_val = float(price)
            if price_val < 0:
                return False, "Price cannot be negative"
            return True, price_val
        except ValueError:
            return False, "Invalid price format"
    
    @staticmethod
    def validate_discount(discount, total_amount):
        """Validate discount value."""
        try:
            discount_val = float(discount)
            if discount_val < 0:
                return False, "Discount cannot be negative"
            if discount_val > total_amount:
                return False, "Discount cannot exceed total amount"
            return True, discount_val
        except ValueError:
            return False, "Invalid discount format"
    
    @staticmethod
    def validate_email(email):
        """Basic email validation."""
        if not email or '@' not in email:
            return False, "Invalid email format"
        
        parts = email.split('@')
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return False, "Invalid email format"
        
        if '.' not in parts[1]:
            return False, "Invalid email domain"
        
        return True, email


# Initialize system
log_system("BuildSmartOS error handling initialized", "INFO")
