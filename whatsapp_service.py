"""
WhatsApp Invoice Service for BuildSmartOS
Sends invoices via WhatsApp using pywhatkit
"""
import pywhatkit as kit
import json
import os
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
        # Remove spaces, dashes, and other characters
        phone = ''.join(filter(str.isdigit, phone))
        
        # If starts with 0, replace with country code
        if phone.startswith('0'):
            phone = self.country_code + phone[1:]
        elif not phone.startswith('+'):
            phone = self.country_code + phone
        
        return phone
    
    def send_invoice(self, phone_number, transaction_id, total_amount, items_list, pdf_path=None):
        """Send invoice via WhatsApp"""
        if not self.enabled:
            return False, "WhatsApp service is disabled"
        
        try:
            # Format phone number
            formatted_phone = self.format_phone_number(phone_number)
            
            # Create message
            business_name = self.config.get("business", {}).get("name", "BuildSmart Hardware")
            message = self.create_invoice_message(business_name, transaction_id, total_amount, items_list)
            
            # Calculate send time (current time + delay)
            now = datetime.now()
            send_time = now + timedelta(seconds=self.send_delay)
            hour = send_time.hour
            minute = send_time.minute
            
            # Send message
            kit.sendwhatmsg(formatted_phone, message, hour, minute, wait_time=10, tab_close=True)
            
            return True, f"Invoice scheduled to send via WhatsApp to {formatted_phone}"
            
        except Exception as e:
            return False, f"WhatsApp send failed: {str(e)}"
    
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
            formatted_phone = self.format_phone_number(phone_number)
            
            message = f"⚠️ *LOW STOCK ALERT*\n\n"
            message += f"Product: *{product_name}*\n"
            message += f"Current Stock: *{current_stock}*\n\n"
            message += f"Please reorder soon!\n"
            message += f"_BuildSmart OS Alert System_"
            
            now = datetime.now()
            send_time = now + timedelta(seconds=self.send_delay)
            
            kit.sendwhatmsg(formatted_phone, message, send_time.hour, send_time.minute, 
                          wait_time=10, tab_close=True)
            
            return True, "Low stock alert sent"
            
        except Exception as e:
            return False, f"Alert send failed: {str(e)}"

# Global instance
_whatsapp_service = None

def get_whatsapp_service():
    """Get or create WhatsApp service instance"""
    global _whatsapp_service
    if _whatsapp_service is None:
        _whatsapp_service = WhatsAppService()
    return _whatsapp_service
