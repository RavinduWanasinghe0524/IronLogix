"""
BuildSmartOS - First Run Configuration Wizard
Interactive setup wizard for initial configuration
"""

import customtkinter as ctk
from tkinter import messagebox
import json
import os
from pathlib import Path

class FirstRunWizard(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("BuildSmartOS - First Run Setup")
        self.geometry("700x700")
        self.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Setup variables
        self.current_step = 0
        self.total_steps = 6  # Added product setup step
        
        # Configuration data
        self.config_data = {
            "business": {
                "name": "",
                "address": "",
                "phone": "",
                "email": ""
            },
            "settings": {
                "default_language": "english",
                "theme": "dark",
                "currency": "LKR"
            },
            "features": {
                "whatsapp_enabled": True,
                "voice_enabled": False,
                "barcode_enabled": False,
                "cloud_backup": False
            }
        }
        
        # Load existing config if present
        self.load_existing_config()
        
        # Create UI
        self.create_ui()
        
        # Show first step
        self.show_step(0)
    
    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_existing_config(self):
        """Load existing configuration if available"""
        config_path = Path('config.json')
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                    # Merge existing data
                    if 'business' in existing:
                        self.config_data['business'].update(existing['business'])
                    if 'settings' in existing:
                        self.config_data['settings'].update(existing['settings'])
                    if 'features' in existing:
                        self.config_data['features'].update(existing['features'])
            except:
                pass
    
    def create_ui(self):
        """Create wizard UI"""
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="#1f538d")
        self.header_frame.pack(fill="x", padx=0, pady=0)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="BuildSmartOS Setup Wizard",
            font=("Arial", 24, "bold"),
            text_color="white"
        )
        self.title_label.pack(pady=20)
        
        # Progress bar
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.pack(fill="x", padx=20, pady=10)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Step 1 of 5",
            font=("Arial", 12)
        )
        self.progress_label.pack()
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=5)
        self.progress_bar.set(0.2)
        
        # Content frame (container for all steps)
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Navigation buttons
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(fill="x", padx=20, pady=20)
        
        self.back_btn = ctk.CTkButton(
            self.nav_frame,
            text="← Back",
            command=self.previous_step,
            state="disabled"
        )
        self.back_btn.pack(side="left", padx=5)
        
        self.next_btn = ctk.CTkButton(
            self.nav_frame,
            text="Next →",
            command=self.next_step
        )
        self.next_btn.pack(side="right", padx=5)
        
        self.finish_btn = ctk.CTkButton(
            self.nav_frame,
            text="Finish",
            command=self.finish_setup,
            fg_color="green"
        )
        # Don't pack finish button yet
    
    def show_step(self, step):
        """Show specific wizard step"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Update progress
        self.current_step = step
        self.progress_label.configure(text=f"Step {step + 1} of {self.total_steps}")
        self.progress_bar.set((step + 1) / self.total_steps)
        
        # Update navigation buttons
        self.back_btn.configure(state="normal" if step > 0 else "disabled")
        
        # Show appropriate step
        if step == 0:
            self.show_welcome()
        elif step == 1:
            self.show_business_info()
        elif step == 2:
            self.show_preferences()
        elif step == 3:
            self.show_product_setup()
        elif step == 4:
            self.show_features()
        elif step == 5:
            self.show_summary()
    
    def show_welcome(self):
        """Welcome step"""
        title = ctk.CTkLabel(
            self.content_frame,
            text="Welcome to BuildSmartOS!",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=20)
        
        welcome_text = """
        🏪 Sri Lanka's First Smart Hardware POS System
        
        This wizard will help you set up BuildSmartOS for your business.
        
        We'll configure:
        • Your business information
        • Application preferences
        • Optional features
        • Sample data for demonstration
        
        The setup takes about 2 minutes to complete.
        
        Click 'Next' to begin...
        """
        
        text_label = ctk.CTkLabel(
            self.content_frame,
            text=welcome_text,
            font=("Arial", 14),
            justify="left"
        )
        text_label.pack(pady=20)
    
    def show_business_info(self):
        """Business information step"""
        title = ctk.CTkLabel(
            self.content_frame,
            text="Business Information",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)
        
        subtitle = ctk.CTkLabel(
            self.content_frame,
            text="Enter your business details (these will appear on invoices)",
            font=("Arial", 12)
        )
        subtitle.pack(pady=5)
        
        # Form frame
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        # Business Name
        ctk.CTkLabel(form_frame, text="Business Name:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(20, 5))
        self.business_name = ctk.CTkEntry(form_frame, width=400)
        self.business_name.insert(0, self.config_data['business']['name'])
        self.business_name.pack(padx=20, pady=5)
        
        # Address
        ctk.CTkLabel(form_frame, text="Address:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 5))
        self.business_address = ctk.CTkEntry(form_frame, width=400)
        self.business_address.insert(0, self.config_data['business']['address'])
        self.business_address.pack(padx=20, pady=5)
        
        # Phone
        ctk.CTkLabel(form_frame, text="Phone:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 5))
        self.business_phone = ctk.CTkEntry(form_frame, width=400)
        self.business_phone.insert(0, self.config_data['business']['phone'])
        self.business_phone.pack(padx=20, pady=5)
        
        # Email
        ctk.CTkLabel(form_frame, text="Email:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 5))
        self.business_email = ctk.CTkEntry(form_frame, width=400)
        self.business_email.insert(0, self.config_data['business']['email'])
        self.business_email.pack(padx=20, pady=5)
    
    def show_preferences(self):
        """Application preferences step"""
        title = ctk.CTkLabel(
            self.content_frame,
            text="Application Preferences",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)
        
        # Language
        lang_frame = ctk.CTkFrame(self.content_frame)
        lang_frame.pack(pady=10, padx=40, fill="x")
        
        ctk.CTkLabel(lang_frame, text="Default Language:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=10)
        self.language_var = ctk.StringVar(value=self.config_data['settings']['default_language'])
        
        lang_menu = ctk.CTkOptionMenu(
            lang_frame,
            values=["english", "sinhala", "tamil"],
            variable=self.language_var
        )
        lang_menu.pack(padx=20, pady=10)
        
        # Theme
        theme_frame = ctk.CTkFrame(self.content_frame)
        theme_frame.pack(pady=10, padx=40, fill="x")
        
        ctk.CTkLabel(theme_frame, text="Theme:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=10)
        self.theme_var = ctk.StringVar(value=self.config_data['settings']['theme'])
        
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["dark", "light"],
            variable=self.theme_var
        )
        theme_menu.pack(padx=20, pady=10)
        
        # Sample data
        sample_frame = ctk.CTkFrame(self.content_frame)
        sample_frame.pack(pady=10, padx=40, fill="x")
        
        self.sample_data_var = ctk.BooleanVar(value=True)
        sample_check = ctk.CTkCheckBox(
            sample_frame,
            text="Generate sample data for demonstration (recommended for first-time users)",
            variable=self.sample_data_var,
            font=("Arial", 12)
        )
        sample_check.pack(padx=20, pady=20)
    
    def show_product_setup(self):
        """Initial product setup step"""
        title = ctk.CTkLabel(
            self.content_frame,
            text="Initial Inventory Setup",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)
        
        subtitle = ctk.CTkLabel(
            self.content_frame,
            text="Add some starter products now or skip and add them later",
            font=("Arial", 12)
        )
        subtitle.pack(pady=5)
        
        # Initialize products list if not exists
        if not hasattr(self, 'starter_products'):
            self.starter_products = []
        
        # Products frame
        products_frame = ctk.CTkFrame(self.content_frame)
        products_frame.pack(pady=10, padx=40, fill="x")
        
        # Products list display
        list_label = ctk.CTkLabel(
            products_frame,
            text=f"Products to add ({len(self.starter_products)}):",
            font=("Arial", 12, "bold")
        )
        list_label.pack(pady=10, padx=20, anchor="w")
        
        # Scrollable product list - LIMITED HEIGHT to ensure buttons show
        self.product_list_frame = ctk.CTkScrollableFrame(products_frame, height=150)
        self.product_list_frame.pack(fill="x", padx=20, pady=5)
        
        self.refresh_product_list()
        
        # Add product form
        add_frame = ctk.CTkFrame(products_frame, fg_color="transparent")
        add_frame.pack(fill="x", padx=20, pady=10)
        
        # Product name
        name_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        name_frame.pack(side="left", padx=5)
        ctk.CTkLabel(name_frame, text="Name:", font=("Arial", 10)).pack()
        self.product_name_entry = ctk.CTkEntry(name_frame, width=150, placeholder_text="e.g., Cement 50kg")
        self.product_name_entry.pack()
        
        # Price
        price_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        price_frame.pack(side="left", padx=5)
        ctk.CTkLabel(price_frame, text="Price (LKR):", font=("Arial", 10)).pack()
        self.product_price_entry = ctk.CTkEntry(price_frame, width=80, placeholder_text="1850")
        self.product_price_entry.pack()
        
        # Stock
        stock_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        stock_frame.pack(side="left", padx=5)
        ctk.CTkLabel(stock_frame, text="Stock:", font=("Arial", 10)).pack()
        self.product_stock_entry = ctk.CTkEntry(stock_frame, width=60, placeholder_text="50")
        self.product_stock_entry.pack()
        
        # Category
        category_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        category_frame.pack(side="left", padx=5)
        ctk.CTkLabel(category_frame, text="Category:", font=("Arial", 10)).pack()
        self.product_category_var = ctk.StringVar(value="Cement")
        category_menu = ctk.CTkOptionMenu(
            category_frame,
            values=["Cement", "Bricks", "Aggregates", "Electrical", "Paint", "Tools", "Other"],
            variable=self.product_category_var,
            width=100
        )
        category_menu.pack()
        
        # Add button
        add_btn = ctk.CTkButton(
            add_frame,
            text="Add",
            width=60,
            command=self.add_starter_product,
            fg_color="#2CC985",
            hover_color="#24A36B"
        )
        add_btn.pack(side="left", padx=5, pady=25)
        
        # Helper text
        helper = ctk.CTkLabel(
            products_frame,
            text="💡 Tip: You can always add more products later from the Products menu",
            font=("Arial", 10),
            text_color="gray"
        )
        helper.pack(pady=5)
    
    def add_starter_product(self):
        """Add product to starter list"""
        name = self.product_name_entry.get().strip()
        price = self.product_price_entry.get().strip()
        stock = self.product_stock_entry.get().strip()
        category = self.product_category_var.get()
        
        if not name or not price or not stock:
            messagebox.showwarning("Required Fields", "Please fill in name, price, and stock")
            return
        
        try:
            price_val = float(price)
            stock_val = int(stock)
            
            if price_val <= 0 or stock_val < 0:
                raise ValueError("Invalid values")
            
            # Add to list
            self.starter_products.append({
                'name': name,
                'price': price_val,
                'stock': stock_val,
                'category': category
            })
            
            # Clear form
            self.product_name_entry.delete(0, 'end')
            self.product_price_entry.delete(0, 'end')
            self.product_stock_entry.delete(0, 'end')
            
            # Refresh display
            self.refresh_product_list()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for price and stock")
    
    def refresh_product_list(self):
        """Refresh the product list display"""
        for widget in self.product_list_frame.winfo_children():
            widget.destroy()
        
        if not self.starter_products:
            ctk.CTkLabel(
                self.product_list_frame,
                text="No products added yet. Add some products above or skip this step.",
                text_color="gray",
                font=("Arial", 10)
            ).pack(pady=20)
        else:
            for i, product in enumerate(self.starter_products):
                row = ctk.CTkFrame(self.product_list_frame, fg_color="#3A3A3A", corner_radius=5)
                row.pack(fill="x", pady=2, padx=5)
                
                text = f"{product['name']} - LKR {product['price']:.2f} ({product['stock']} in stock)"
                ctk.CTkLabel(row, text=text, anchor="w").pack(side="left", padx=10, pady=5)
                
                ctk.CTkLabel(row, text=f"[{product['category']}]", text_color="#2CC985").pack(side="left", padx=5)
                
                # Remove button
                remove_btn = ctk.CTkButton(
                    row,
                    text="✖",
                    width=30,
                    height=25,
                    fg_color="transparent",
                    hover_color="#CF6679",
                    command=lambda idx=i: self.remove_starter_product(idx)
                )
                remove_btn.pack(side="right", padx=5)
    
    def remove_starter_product(self, index):
        """Remove product from starter list"""
        if 0 <= index < len(self.starter_products):
            self.starter_products.pop(index)
            self.refresh_product_list()
    
    def save_starter_products(self):
        """Save starter products to database"""
        try:
            import sqlite3
            conn = sqlite3.connect('buildsmart_hardware.db')
            cursor = conn.cursor()
            
            for product in self.starter_products:
                cursor.execute("""
                    INSERT INTO products (name, category, price_per_unit, unit_type, stock_quantity, reorder_level)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    product['name'],
                    product['category'],
                    product['price'],
                    'unit',  # Default unit type
                    product['stock'],
                    10  # Default reorder level
                ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error saving starter products: {e}")
    
    def show_features(self):
        """Optional features step"""
        title = ctk.CTkLabel(
            self.content_frame,
            text="Optional Features",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)
        
        subtitle = ctk.CTkLabel(
            self.content_frame,
            text="Enable or disable optional features (can be changed later)",
            font=("Arial", 12)
        )
        subtitle.pack(pady=5)
        
        features_frame = ctk.CTkFrame(self.content_frame)
        features_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # WhatsApp
        self.whatsapp_var = ctk.BooleanVar(value=self.config_data['features']['whatsapp_enabled'])
        whatsapp_check = ctk.CTkCheckBox(
            features_frame,
            text="WhatsApp Invoice Sending",
            variable=self.whatsapp_var,
            font=("Arial", 12)
        )
        whatsapp_check.pack(anchor="w", padx=20, pady=10)
        
        ctk.CTkLabel(
            features_frame,
            text="  Send invoices to customers via WhatsApp",
            font=("Arial", 10),
            text_color="gray"
        ).pack(anchor="w", padx=40, pady=(0, 10))
        
        # Voice
        self.voice_var = ctk.BooleanVar(value=self.config_data['features']['voice_enabled'])
        voice_check = ctk.CTkCheckBox(
            features_frame,
            text="Voice Commands (requires microphone)",
            variable=self.voice_var,
            font=("Arial", 12)
        )
        voice_check.pack(anchor="w", padx=20, pady=10)
        
        ctk.CTkLabel(
            features_frame,
            text="  Control application with voice commands",
            font=("Arial", 10),
            text_color="gray"
        ).pack(anchor="w", padx=40, pady=(0, 10))
        
        # Barcode
        self.barcode_var = ctk.BooleanVar(value=self.config_data['features']['barcode_enabled'])
        barcode_check = ctk.CTkCheckBox(
            features_frame,
            text="Barcode Scanner (requires webcam)",
            variable=self.barcode_var,
            font=("Arial", 12)
        )
        barcode_check.pack(anchor="w", padx=20, pady=10)
        
        ctk.CTkLabel(
            features_frame,
            text="  Scan product barcodes with camera",
            font=("Arial", 10),
            text_color="gray"
        ).pack(anchor="w", padx=40, pady=(0, 10))
        
        # Cloud backup
        self.cloud_var = ctk.BooleanVar(value=self.config_data['features']['cloud_backup'])
        cloud_check = ctk.CTkCheckBox(
            features_frame,
            text="Cloud Backup (requires Google Drive API)",
            variable=self.cloud_var,
            font=("Arial", 12)
        )
        cloud_check.pack(anchor="w", padx=20, pady=10)
        
        ctk.CTkLabel(
            features_frame,
            text="  Automatic backup to Google Drive",
            font=("Arial", 10),
            text_color="gray"
        ).pack(anchor="w", padx=40, pady=(0, 10))
    
    def show_summary(self):
        """Summary step"""
        title = ctk.CTkLabel(
            self.content_frame,
            text="Setup Summary",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)
        
        # Collect data
        self.collect_configuration()
        
        summary_text = f"""
        Business Name: {self.config_data['business']['name'] or 'Not specified'}
        Address: {self.config_data['business']['address'] or 'Not specified'}
        Phone: {self.config_data['business']['phone'] or 'Not specified'}
        Email: {self.config_data['business']['email'] or 'Not specified'}
        
        Language: {self.config_data['settings']['default_language'].title()}
        Theme: {self.config_data['settings']['theme'].title()}
        
        Features Enabled:
        • WhatsApp: {'Yes' if self.config_data['features']['whatsapp_enabled'] else 'No'}
        • Voice Commands: {'Yes' if self.config_data['features']['voice_enabled'] else 'No'}
        • Barcode Scanner: {'Yes' if self.config_data['features']['barcode_enabled'] else 'No'}
        • Cloud Backup: {'Yes' if self.config_data['features']['cloud_backup'] else 'No'}
        
        Click 'Finish' to complete setup and launch BuildSmartOS!
        """
        
        summary_label = ctk.CTkTextbox(
            self.content_frame,
            font=("Arial", 12),
            height=320
        )
        summary_label.pack(pady=20, padx=40, fill="both", expand=True)
        summary_label.insert("1.0", summary_text)
        summary_label.configure(state="disabled")
        
        # Update navigation
        self.next_btn.pack_forget()
        self.finish_btn.pack(side="right", padx=5)
    
    def collect_configuration(self):
        """Collect configuration from form fields"""
        # Business info (if on that step or later)
        if hasattr(self, 'business_name'):
            self.config_data['business']['name'] = self.business_name.get()
            self.config_data['business']['address'] = self.business_address.get()
            self.config_data['business']['phone'] = self.business_phone.get()
            self.config_data['business']['email'] = self.business_email.get()
        
        # Preferences
        if hasattr(self, 'language_var'):
            self.config_data['settings']['default_language'] = self.language_var.get()
            self.config_data['settings']['theme'] = self.theme_var.get()
        
        # Features
        if hasattr(self, 'whatsapp_var'):
            self.config_data['features']['whatsapp_enabled'] = self.whatsapp_var.get()
            self.config_data['features']['voice_enabled'] = self.voice_var.get()
            self.config_data['features']['barcode_enabled'] = self.barcode_var.get()
            self.config_data['features']['cloud_backup'] = self.cloud_var.get()
    
    def next_step(self):
        """Move to next step"""
        # Validate current step if needed
        if self.current_step == 1:  # Business info
            self.collect_configuration()
            if not self.config_data['business']['name']:
                messagebox.showwarning("Validation", "Please enter your business name")
                return
        
        if self.current_step < self.total_steps - 1:
            self.show_step(self.current_step + 1)
    
    def previous_step(self):
        """Move to previous step"""
        if self.current_step > 0:
            # Save current data
            self.collect_configuration()
            self.show_step(self.current_step - 1)
    
    def finish_setup(self):
        """Complete setup and save configuration"""
        try:
            # Save configuration
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2)
            
            # Add starter products to database
            if hasattr(self, 'starter_products') and self.starter_products:
                self.save_starter_products()
            
            # Generate sample data if requested
            if hasattr(self, 'sample_data_var') and self.sample_data_var.get():
                try:
                    import subprocess
                    import sys
                    subprocess.run([sys.executable, 'generate_test_data.py'], 
                                 capture_output=True, timeout=30)
                except:
                    pass  # Optional, don't fail if it doesn't work
            
            # Create first-run marker
            Path('.configured').touch()
            
            products_msg = f"\n\n✅ {len(self.starter_products)} products added to inventory!" if hasattr(self, 'starter_products') and self.starter_products else ""
            
            messagebox.showinfo(
                "Setup Complete",
                f"BuildSmartOS has been configured successfully!{products_msg}\n\n"
                "The application will now start.\n\n"
                "You can change these settings later in config.json"
            )
            
            # Close wizard
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")

def run_wizard():
    """Run the configuration wizard"""
    app = FirstRunWizard()
    app.mainloop()

if __name__ == "__main__":
    run_wizard()
