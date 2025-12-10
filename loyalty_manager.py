"""
Customer Loyalty Program Manager for BuildSmartOS
Track customer points and rewards
"""
import sqlite3
import json
from datetime import datetime

class LoyaltyManager:
    def __init__(self, db_name="buildsmart_hardware.db"):
        self.db_name = db_name
        self.config = self.load_config()
        self.points_per_100 = self.config.get("loyalty", {}).get("points_per_100_lkr", 1)
        self.reward_threshold = self.config.get("loyalty", {}).get("reward_threshold", 500)
        self.reward_value = self.config.get("loyalty", {}).get("reward_value", 100)
    
    def load_config(self):
        """Load configuration"""
        try:
            with open("config.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def calculate_points(self, amount):
        """Calculate loyalty points for purchase amount"""
        return int((amount / 100) * self.points_per_100)
    
    def add_points(self, phone_number, amount, transaction_id=None):
        """Add loyalty points for a customer"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Check if customer exists
            cursor.execute("SELECT id, loyalty_points FROM customers WHERE phone_number = ?", (phone_number,))
            result = cursor.fetchone()
            
            points_earned = self.calculate_points(amount)
            
            if result:
                # Update existing customer
                customer_id, current_points = result
                new_points = current_points + points_earned
                
                cursor.execute("""
                    UPDATE customers 
                    SET loyalty_points = ?, total_purchases = total_purchases + ?
                    WHERE id = ?
                """, (new_points, amount, customer_id))
            else:
                # Create new customer
                cursor.execute("""
                    INSERT INTO customers (phone_number, loyalty_points, total_purchases)
                    VALUES (?, ?, ?)
                """, (phone_number, points_earned, amount))
                customer_id = cursor.lastrowid
                new_points = points_earned
            
            # Record points transaction
            cursor.execute("""
                INSERT INTO loyalty_transactions (customer_id, points_change, transaction_id, description)
                VALUES (?, ?, ?, ?)
            """, (customer_id, points_earned, transaction_id, f"Purchase LKR {amount:.2f}"))
            
            conn.commit()
            conn.close()
            
            return True, {
                'points_earned': points_earned,
                'total_points': new_points,
                'can_redeem': new_points >= self.reward_threshold
            }
            
        except Exception as e:
            return False, f"Error adding points: {e}"
    
    def redeem_points(self, phone_number, points_to_redeem=None):
        """Redeem loyalty points for discount"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, loyalty_points FROM customers WHERE phone_number = ?", (phone_number,))
            result = cursor.fetchone()
            
            if not result:
                return False, "Customer not found"
            
            customer_id, current_points = result
            
            # Use threshold points if not specified
            if points_to_redeem is None:
                points_to_redeem = self.reward_threshold
            
            if current_points < points_to_redeem:
                return False, f"Insufficient points. Available: {current_points}"
            
            # Calculate discount value
            discount_value = (points_to_redeem / self.reward_threshold) * self.reward_value
            
            # Deduct points
            new_points = current_points - points_to_redeem
            cursor.execute("UPDATE customers SET loyalty_points = ? WHERE id = ?", (new_points, customer_id))
            
            # Record redemption
            cursor.execute("""
                INSERT INTO loyalty_transactions (customer_id, points_change, description)
                VALUES (?, ?, ?)
            """, (customer_id, -points_to_redeem, f"Redeemed for LKR {discount_value:.2f} discount"))
            
            conn.commit()
            conn.close()
            
            return True, {
                'points_redeemed': points_to_redeem,
                'discount_value': discount_value,
                'remaining_points': new_points
            }
            
        except Exception as e:
            return False, f"Error redeeming points: {e}"
    
    def get_customer_points(self, phone_number):
        """Get customer's current loyalty points"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT loyalty_points, total_purchases, name
                FROM customers WHERE phone_number = ?
            """, (phone_number,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                points, purchases, name = result
                return True, {
                    'points': points,
                    'total_purchases': purchases,
                    'name': name,
                    'can_redeem': points >= self.reward_threshold,
                    'next_reward_points': self.reward_threshold - (points % self.reward_threshold)
                }
            else:
                return False, "Customer not found"
                
        except Exception as e:
            return False, f"Error: {e}"
    
    def get_top_customers(self, limit=10):
        """Get top loyalty customers"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT phone_number, name, loyalty_points, total_purchases
                FROM customers
                ORDER BY loyalty_points DESC
                LIMIT ?
            """, (limit,))
            
            customers = cursor.fetchall()
            conn.close()
            
            return True, customers
            
        except Exception as e:
            return False, f"Error: {e}"

# Global instance
_loyalty_manager = None

def get_loyalty_manager():
    """Get or create loyalty manager instance"""
    global _loyalty_manager
    if _loyalty_manager is None:
        _loyalty_manager = LoyaltyManager()
    return _loyalty_manager
