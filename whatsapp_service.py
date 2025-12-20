"""
WhatsApp Invoice Service for BuildSmartOS
Sends invoices via WhatsApp using pywhatkit
"""
import pywhatkit as kit
import json
import os
import threading
from datetime import datetime, timedelta

class WhatsAppService:
    def __init__(self):
        self.config = self.load_config()
        self.country_code = self.config.get("whatsapp", {}).get("country_code", "+94")
        self.send_delay = self.config.get("whatsapp", {}).get("send_delay_seconds", 15)
        self.enabled = self.config.get("features", {}).get("whatsapp_enabled", True)
    
    def load_config(self):
        """Load configuration"""
        try:
            with open("config.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def format_phone_number(self, phone):
        """Format phone number for WhatsApp"""
        # Store if it starts with + before cleaning
        has_plus = phone.strip().startswith('+')
        
        # Remove spaces, dashes, and other characters
        phone = ''.join(filter(str.isdigit, phone))
        
        # If already had +, it's international format, just add + back
        if has_plus:
            return '+' + phone
        
        # If starts with 0, replace with country code
        if phone.startswith('0'):
            phone = self.country_code + phone[1:]
        elif not phone.startswith(self.country_code.replace('+', '')):
            phone = self.country_code + phone
        
        return phone
    
    def send_invoice(self, phone_number, transaction_id, total_amount, items_list, pdf_path=None):
        """Send invoice via WhatsApp"""
        if not self.enabled:
            return False, "WhatsApp service is disabled"
        
        try:
            # Validate phone number
            if not phone_number:
                return False, "Phone number is required"
            
            # Format phone number
            formatted_phone = self.format_phone_number(phone_number)
            
            # Validate formatted number
            if not formatted_phone or len(formatted_phone) < 10:
                return False, f"Invalid phone number format: {phone_number}"
            
            # Create message
            business_name = self.config.get("business", {}).get("name", "BuildSmart Hardware")
            message = self.create_invoice_message(business_name, transaction_id, total_amount, items_list)
            
            # Calculate send time (current time + delay)
            now = datetime.now()
            send_time = now + timedelta(seconds=self.send_delay)
            hour = send_time.hour
            minute = send_time.minute
            
            # Validate time (pywhatkit requires future time)
            if send_time <= now:
                send_time = now + timedelta(seconds=20)
                hour = send_time.hour
                minute = send_time.minute
            
            # Send message with error handling
            try:
                kit.sendwhatmsg(formatted_phone, message, hour, minute, wait_time=15, tab_close=True, close_time=3)
                return True, f"Invoice sent via WhatsApp to {formatted_phone}"
            except Exception as send_error:
                # Log the specific sending error
                error_msg = str(send_error)
                if "web.whatsapp.com" in error_msg.lower():
                    return False, "WhatsApp Web not accessible. Please ensure browser is open and WhatsApp Web is logged in."
                elif "internet" in error_msg.lower():
                    return False, "Internet connection issue. Please check your connection."
                else:
                    return False, f"WhatsApp send error: {error_msg}"
            
        except Exception as e:
            return False, f"WhatsApp service error: {str(e)}"
    
    def send_invoice_async(self, phone_number, transaction_id, total_amount, items_list, pdf_path=None, callback=None):
        """Send invoice via WhatsApp asynchronously in background thread"""
        def send_in_background():
            import time
            retry_count = 0
            max_retries = 2
            
            while retry_count <= max_retries:
                try:
                    success, message = self.send_invoice(phone_number, transaction_id, total_amount, items_list, pdf_path)
                    if callback:
                        callback(success, message)
                    return
                except Exception as e:
                    retry_count += 1
                    if retry_count <= max_retries:
                        time.sleep(5)  # Wait 5 seconds before retry
                        continue
                    else:
                        if callback:
                            callback(False, f"WhatsApp send failed after {max_retries} retries: {str(e)}")
        
        # Start background thread
        thread = threading.Thread(target=send_in_background, daemon=True)
        thread.start()
        
        return True, "WhatsApp invoice is being sent in background..."
    
    def create_invoice_message(self, business_name, transaction_id, total_amount, items_list):
        """Create formatted invoice message"""
        message = f"🏪 *{business_name}*\n"
        message += f"━━━━━━━━━━━━━━━━━━\n"
        message += f"📄 Invoice #{transaction_id}\n"
        message += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        message += f"*Items:*\n"
        
        for item in items_list:
            name = item.get('name', 'Item')
            qty = item.get('qty', 1)
            subtotal = item.get('subtotal', 0)
            message += f"• {name} x{qty} - LKR {subtotal:.2f}\n"
        
        message += f"\n━━━━━━━━━━━━━━━━━━\n"
        message += f"*💰 Total: LKR {total_amount:.2f}*\n\n"
        message += f"Thank you for your business! 🙏\n"
        message += f"_Powered by BuildSmart OS_"
        
        return message
    
    def send_low_stock_alert(self, phone_number, product_name, current_stock):
        """Send low stock alert"""
        if not self.enabled:
            return False, "WhatsApp service is disabled"
        
        try:
            # Validate phone number
            if not phone_number:
                return False, "Phone number is required"
            
            formatted_phone = self.format_phone_number(phone_number)
            
            # Validate formatted number
            if not formatted_phone or len(formatted_phone) < 10:
                return False, f"Invalid phone number format: {phone_number}"
            
            message = f"⚠️ *LOW STOCK ALERT*\n\n"
            message += f"Product: *{product_name}*\n"
            message += f"Current Stock: *{current_stock}*\n\n"
            message += f"Please reorder soon!\n"
            message += f"_BuildSmart OS Alert System_"
            
            now = datetime.now()
            send_time = now + timedelta(seconds=self.send_delay)
            
            # Validate time
            if send_time <= now:
                send_time = now + timedelta(seconds=20)
            
            try:
                kit.sendwhatmsg(formatted_phone, message, send_time.hour, send_time.minute, 
                              wait_time=15, tab_close=True, close_time=3)
                return True, "Low stock alert sent"
            except Exception as send_error:
                error_msg = str(send_error)
                if "web.whatsapp.com" in error_msg.lower():
                    return False, "WhatsApp Web not accessible for alert"
                else:
                    return False, f"Alert send failed: {error_msg}"
            
        except Exception as e:
            return False, f"Alert service error: {str(e)}"

# Global instance
_whatsapp_service = None

def get_whatsapp_service():
    """Get or create WhatsApp service instance"""
    global _whatsapp_service
    if _whatsapp_service is None:
        _whatsapp_service = WhatsAppService()
    return _whatsapp_service
