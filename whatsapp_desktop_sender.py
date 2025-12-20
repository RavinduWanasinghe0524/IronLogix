"""
WhatsApp Desktop Sender for BuildSmartOS
Automates WhatsApp Desktop app using pyautogui to send PDFs
"""
import pyautogui
import time
import os
import subprocess
import psutil


class WhatsAppDesktopSender:
    def __init__(self):
        self.whatsapp_paths = [
            r"C:\Users\{}\AppData\Local\WhatsApp\WhatsApp.exe",
            r"C:\Program Files\WindowsApps\WhatsApp\WhatsApp.exe"
        ]
        self.process_name = "WhatsApp.exe"
    
    def find_whatsapp_path(self):
        """Find WhatsApp Desktop executable path"""
        import getpass
        username = getpass.getuser()
        
        for path_template in self.whatsapp_paths:
            path = path_template.format(username)
            if os.path.exists(path):
                return path
        
        # Try to find in WindowsApps (may require special handling)
        try:
            import winreg
            # Check if installed from Microsoft Store
            store_path = r"C:\Program Files\WindowsApps"
            if os.path.exists(store_path):
                for folder in os.listdir(store_path):
                    if "WhatsApp" in folder:
                        exe_path = os.path.join(store_path, folder, "WhatsApp.exe")
                        if os.path.exists(exe_path):
                            return exe_path
        except:
            pass
        
        return None
    
    def is_whatsapp_installed(self):
        """Check if WhatsApp Desktop is installed"""
        return self.find_whatsapp_path() is not None
    
    def is_whatsapp_running(self):
        """Check if WhatsApp Desktop is currently running"""
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] == self.process_name:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False
    
    def open_whatsapp(self):
        """Open WhatsApp Desktop if not already running"""
        if self.is_whatsapp_running():
            return True, "WhatsApp Desktop is already running"
        
        whatsapp_path = self.find_whatsapp_path()
        if not whatsapp_path:
            return False, "WhatsApp Desktop is not installed. Please install from Microsoft Store."
        
        try:
            # Open WhatsApp using the protocol handler (more reliable)
            os.startfile("whatsapp://")
            time.sleep(3)  # Wait for WhatsApp to open
            return True, "WhatsApp Desktop opened successfully"
        except Exception as e:
            try:
                # Fallback: try direct executable
                subprocess.Popen([whatsapp_path])
                time.sleep(3)
                return True, "WhatsApp Desktop opened successfully"
            except Exception as e2:
                return False, f"Failed to open WhatsApp Desktop: {str(e2)}"
    
    def send_pdf(self, phone_number, pdf_path, message=None):
        """
        Send PDF file via WhatsApp Desktop using GUI automation
        
        Args:
            phone_number: Phone number with country code (e.g., +94775580679)
            pdf_path: Absolute path to PDF file
            message: Optional message caption
            
        Returns:
            (success, message) tuple
        """
        try:
            # Validate PDF exists
            if not os.path.exists(pdf_path):
                return False, f"PDF file not found: {pdf_path}"
            
            # Ensure WhatsApp is running
            if not self.is_whatsapp_running():
                success, msg = self.open_whatsapp()
                if not success:
                    return False, msg
                time.sleep(2)
            
            # Wait a moment for WhatsApp to be ready
            time.sleep(1)
            
            # Use WhatsApp URI scheme to open chat directly
            # Format: whatsapp://send?phone=94775580679
            clean_phone = phone_number.replace('+', '').replace(' ', '').replace('-', '')
            whatsapp_uri = f"whatsapp://send?phone={clean_phone}"
            
            try:
                os.startfile(whatsapp_uri)
                time.sleep(2)  # Wait for chat to open
            except Exception as e:
                return False, f"Failed to open chat: {str(e)}"
            
            # Now we need to attach the file using keyboard shortcuts
            # This is more reliable than clicking
            
            # Step 1: Attach file using Ctrl+N (or clicking attach button)
            # Note: WhatsApp Desktop uses different shortcuts
            # We'll use the clip icon or keyboard
            
            # Click in the message input area first to ensure focus
            pyautogui.hotkey('ctrl', 'f')  # Open search (to reset focus)
            time.sleep(0.5)
            pyautogui.press('escape')  # Close search
            time.sleep(0.5)
            
            # Attach file - we'll simulate clicking the attach button and then selecting document
            # The attach button is usually on the left side of the message input
            # We'll use Tab to navigate to it
            
            # Alternative: Use clipboard approach
            # Copy file path to clipboard and paste in file dialog
            import win32clipboard
            
            # Open attach menu using keyboard shortcut or clicking
            # WhatsApp Desktop: Click the attach button (paperclip icon)
            # The attach button location varies, so we'll use keyboard approach
            
            # Press Tab several times to reach attach button (or use mouse)
            # For now, let's use Ctrl+Shift+D as a potential shortcut, or simulate clicking
            
            # Simpler approach: Use pyautogui to find and click the attach icon
            # But this requires knowing the icon position
            
            # Most reliable: Use keyboard to open file dialog
            # In WhatsApp Desktop, we can:
            # 1. Click in message box
            # 2. Use Ctrl+Shift+O or click attach button
            
            # Let's use a more direct approach: simulate the attach process
            try:
                # Click somewhere in the chat window to focus
                screen_width, screen_height = pyautogui.size()
                # Click in center-bottom area where message box usually is
                pyautogui.click(screen_width // 2, screen_height - 100)
                time.sleep(0.3)
                
                # Look for attach button (paperclip) - it's usually left of message input
                # We'll click at approximate position
                attach_x = screen_width // 2 - 300
                attach_y = screen_height - 50
                pyautogui.click(attach_x, attach_y)
                time.sleep(0.5)
                
                # Now click on "Document" option (usually appears above)
                doc_x = attach_x
                doc_y = attach_y - 150
                pyautogui.click(doc_x, doc_y)
                time.sleep(0.5)
                
                # File dialog should open - type the path
                abs_pdf_path = os.path.abspath(pdf_path)
                
                # Copy path to clipboard
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(abs_pdf_path)
                win32clipboard.CloseClipboard()
                
                # In file dialog, paste the path
                time.sleep(0.5)
                pyautogui.hotkey('ctrl', 'v')  # Paste path
                time.sleep(0.3)
                pyautogui.press('enter')  # Open file
                time.sleep(1)
                
                # Add caption if provided
                if message:
                    # Type message in caption box
                    time.sleep(0.5)
                    pyautogui.write(message, interval=0.05)
                    time.sleep(0.3)
                
                # Send the file (press Enter or click Send button)
                pyautogui.press('enter')
                time.sleep(1)
                
                return True, f"PDF sent successfully to {phone_number}"
                
            except Exception as e:
                return False, f"Error during file attach process: {str(e)}"
        
        except Exception as e:
            return False, f"WhatsApp Desktop sender error: {str(e)}"


# Global instance
_desktop_sender = None

def get_desktop_sender():
    """Get or create Desktop sender instance"""
    global _desktop_sender
    if _desktop_sender is None:
        _desktop_sender = WhatsAppDesktopSender()
    return _desktop_sender

def is_whatsapp_installed():
    """Check if WhatsApp Desktop is installed"""
    sender = get_desktop_sender()
    return sender.is_whatsapp_installed()

def is_whatsapp_running():
    """Check if WhatsApp Desktop is running"""
    sender = get_desktop_sender()
    return sender.is_whatsapp_running()
