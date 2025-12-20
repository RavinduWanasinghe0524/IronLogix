"""
First Run Wizard for BuildSmartOS
Guides users through initial setup including WhatsApp Desktop configuration
"""
import customtkinter as ctk
from tkinter import messagebox
import json
import os


class FirstRunWizard(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("BuildSmartOS - First Time Setup")
        self.geometry("700x550")
        self.resizable(False, False)
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.winfo_screenheight() // 2) - (550 // 2)
        self.geometry(f"700x550+{x}+{y}")
        
        self.current_step = 0
        self.config_data = {
            "business": {
                "name": "BuildSmart Hardware",
                "address": "",
                "phone": ""
            },
            "whatsapp": {
                "connected": False,
                "country_code": "+94"
            },
            "features": {
                "whatsapp_enabled": True
            },
            "settings": {
                "default_language": "english"
            }
        }
        
        self.show_welcome_screen()
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.winfo_children():
            widget.destroy()
    
    def show_welcome_screen(self):
        """Welcome screen"""
        self.clear_window()
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="🏪 Welcome to BuildSmartOS!",
            font=("Arial", 28, "bold"),
            text_color="#2CC985"
        )
        header.pack(pady=40)
        
        # Description
        desc = ctk.CTkLabel(
            self,
            text="Sri Lanka's Smart Hardware POS System\n\n" +
                 "This wizard will help you set up BuildSmartOS for your business.\n\n" +
                 "We'll configure:\n" +
                 "  • Business Information\n" +
                 "  • WhatsApp Integration (Optional)\n" +
                 "  • System Preferences",
            font=("Arial", 14),
            justify="left"
        )
        desc.pack(pady=20)
        
        # Next button
        next_btn = ctk.CTkButton(
            self,
            text="Let's Get Started →",
            command=self.show_business_info,
            width=200,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="#2CC985",
            hover_color="#24A36B"
        )
        next_btn.pack(pady=40)
    
    def show_business_info(self):
        """Business information screen"""
        self.clear_window()
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="Business Information",
            font=("Arial", 24, "bold")
        )
        header.pack(pady=30)
        
        # Form frame
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        # Business Name
        ctk.CTkLabel(form_frame, text="Business Name:", font=("Arial", 14)).pack(anchor="w", pady=(10, 5))
        self.business_name_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        self.business_name_entry.insert(0, "BuildSmart Hardware")
        self.business_name_entry.pack(pady=(0, 15))
        
        # Address
        ctk.CTkLabel(form_frame, text="Address (Optional):", font=("Arial", 14)).pack(anchor="w", pady=(10, 5))
        self.address_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        self.address_entry.pack(pady=(0, 15))
        
        # Phone
        ctk.CTkLabel(form_frame, text="Business Phone (Optional):", font=("Arial", 14)).pack(anchor="w", pady=(10, 5))
        self.phone_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        self.phone_entry.pack(pady=(0, 15))
        
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        back_btn = ctk.CTkButton(
            btn_frame, text="← Back",
            command=self.show_welcome_screen,
            width=150, height=40
        )
        back_btn.pack(side="left", padx=10)
        
        next_btn = ctk.CTkButton(
            btn_frame, text="Next →",
            command=self.save_business_info,
            width=150, height=40,
            fg_color="#2CC985",
            hover_color="#24A36B"
        )
        next_btn.pack(side="left", padx=10)
    
    def save_business_info(self):
        """Save business information and move to WhatsApp setup"""
        self.config_data["business"]["name"] = self.business_name_entry.get() or "BuildSmart Hardware"
        self.config_data["business"]["address"] = self.address_entry.get()
        self.config_data["business"]["phone"] = self.phone_entry.get()
        
        self.show_whatsapp_setup()
    
    def show_whatsapp_setup(self):
        """WhatsApp Desktop setup screen"""
        self.clear_window()
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="📱 WhatsApp Integration",
            font=("Arial", 24, "bold")
        )
        header.pack(pady=30)
        
        # Description
        desc_frame = ctk.CTkFrame(self)
        desc_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        desc = ctk.CTkLabel(
            desc_frame,
            text="Connect WhatsApp Desktop to send invoices automatically!\n\n" +
                 "Requirements:\n" +
                 "  ✓ WhatsApp Desktop app installed (from Microsoft Store)\n" +
                 "  ✓ Logged in with your business WhatsApp number\n\n" +
                 "BuildSmartOS will use YOUR WhatsApp to send invoices to customers.\n" +
                 "This is optional but recommended for better customer service!",
            font=("Arial", 13),
            justify="left"
        )
        desc.pack(pady=20, padx=20)
        
        # Check if WhatsApp Desktop is installed
        try:
            from whatsapp_desktop_sender import is_whatsapp_installed, is_whatsapp_running
            
            if is_whatsapp_installed():
                status_text = "✅ WhatsApp Desktop is installed"
                status_color = "#2CC985"
                
                if is_whatsapp_running():
                    status_text += "\n✅ WhatsApp Desktop is running"
                else:
                    status_text += "\n⚠️ WhatsApp Desktop is not running. Please open it."
                    status_color = "#FFA726"
            else:
                status_text = "❌ WhatsApp Desktop is NOT installed\n" +
                            "Please install from Microsoft Store to use this feature."
                status_color = "#CF6679"
        except:
            status_text = "⚠️ Cannot detect WhatsApp Desktop status"
            status_color = "#FFA726"
        
        status_label = ctk.CTkLabel(
            desc_frame,
            text=status_text,
            font=("Arial", 12, "bold"),
            text_color=status_color
        )
        status_label.pack(pady=10)
        
        # Enable WhatsApp checkbox
        self.whatsapp_enabled_var = ctk.BooleanVar(value=True)
        checkbox = ctk.CTkCheckBox(
            desc_frame,
            text="Enable WhatsApp for invoices",
            variable=self.whatsapp_enabled_var,
            font=("Arial", 13)
        )
        checkbox.pack(pady=15)
        
        # Instructions
        instructions = ctk.CTkLabel(
            desc_frame,
            text="Make sure WhatsApp Desktop is:\n" +
                 "1. Installed from Microsoft Store\n" +
                 "2. Logged in with your phone (scan QR code)\n" +
                 "3. Running in the background",
            font=("Arial", 11),
            text_color="#888888",
            justify="left"
        )
        instructions.pack(pady=10)
        
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        back_btn = ctk.CTkButton(
            btn_frame, text="← Back",
            command=self.show_business_info,
            width=150, height=40
        )
        back_btn.pack(side="left", padx=10)
        
        finish_btn = ctk.CTkButton(
            btn_frame, text="Finish Setup ✓",
            command=self.finish_setup,
            width=150, height=40,
            fg_color="#2CC985",
            hover_color="#24A36B"
        )
        finish_btn.pack(side="left", padx=10)
    
    def finish_setup(self):
        """Complete setup and save configuration"""
        # Save WhatsApp preference
        self.config_data["features"]["whatsapp_enabled"] = self.whatsapp_enabled_var.get()
        
        # Try to detect WhatsApp status
        try:
            from whatsapp_desktop_sender import is_whatsapp_installed, is_whatsapp_running
            self.config_data["whatsapp"]["connected"] = is_whatsapp_installed() and is_whatsapp_running()
        except:
            self.config_data["whatsapp"]["connected"] = False
        
        # Save config.json
        try:
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            return
        
        # Create .configured marker file
        try:
            with open(".configured", 'w') as f:
                f.write("BuildSmartOS configured\n")
        except:
            pass
        
        # Show completion message
        self.show_completion()
    
    def show_completion(self):
        """Show completion screen"""
        self.clear_window()
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="🎉 Setup Complete!",
            font=("Arial", 28, "bold"),
            text_color="#2CC985"
        )
        header.pack(pady=50)
        
        # Success message
        msg = ctk.CTkLabel(
            self,
            text="BuildSmartOS is ready to use!\n\n" +
                 "You can now:\n" +
                 "  • Manage products and inventory\n" +
                 "  • Process sales\n" +
                 "  • Send invoices via WhatsApp\n" +
                 "  • View analytics and reports\n\n" +
                 "Click 'Start BuildSmartOS' to begin!",
            font=("Arial", 14),
            justify="center"
        )
        msg.pack(pady=30)
        
        # Start button
        start_btn = ctk.CTkButton(
            self,
            text="Start BuildSmartOS →",
            command=self.destroy,
            width=250,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="#2CC985",
            hover_color="#24A36B"
        )
        start_btn.pack(pady=30)


if __name__ == "__main__":
    # Set appearance
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    app = FirstRunWizard()
    app.mainloop()
