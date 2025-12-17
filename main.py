import customtkinter as ctk
import sqlite3
from tkinter import messagebox, simpledialog
from datetime import datetime
import json
import os

# Core imports with feature flags
LANG_AVAILABLE = False
THEMES_AVAILABLE = False
PDF_AVAILABLE = False
WHATSAPP_AVAILABLE = False
LOYALTY_AVAILABLE = False
ANALYTICS_AVAILABLE = False
ESTIMATOR_AVAILABLE = False
BARCODE_AVAILABLE = False
VOICE_AVAILABLE = False

# Import core modules
try:
    from language_manager import get_language_manager
    LANG_AVAILABLE = True
except ImportError:
    print("Language manager not available")

try:
    from themes import get_theme_manager
    THEMES_AVAILABLE = True
except ImportError:
    print("Themes not available")

try:
    import pdf_generator
    PDF_AVAILABLE = True
except ImportError:
    print("PDF generator not available - install reportlab")

try:
    from whatsapp_service import get_whatsapp_service
    WHATSAPP_AVAILABLE = True
except ImportError:
    print("WhatsApp service not available - install pywhatkit")

try:
    from loyalty_manager import get_loyalty_manager
    LOYALTY_AVAILABLE = True
except ImportError:
    print("Loyalty manager not available")

try:
    from analytics_dashboard import get_analytics_dashboard
    ANALYTICS_AVAILABLE = True
except ImportError:
    print("Analytics dashboard not available - install matplotlib and pandas")

try:
    from construction_estimator import get_construction_estimator
    ESTIMATOR_AVAILABLE = True
except ImportError:
    print("Construction estimator not available")

try:
    from barcode_scanner import get_barcode_scanner
    BARCODE_AVAILABLE = True
except ImportError:
    print("Barcode scanner not available - install opencv-python and pyzbar")

try:
    from voice_assistant import get_voice_assistant
    VOICE_AVAILABLE = True
except ImportError:
    print("Voice assistant not available - install SpeechRecognition and pyttsx3")

try:
    from product_manager import ProductManager
    PRODUCT_MANAGER_AVAILABLE = True
except ImportError:
    PRODUCT_MANAGER_AVAILABLE = False
    print("Product manager not available")

try:
    from customer_manager import CustomerManager
    CUSTOMER_MANAGER_AVAILABLE = True
except ImportError:
    CUSTOMER_MANAGER_AVAILABLE = False
    print("Customer manager not available")

try:
    from report_generator import ReportGenerator
    REPORT_GENERATOR_AVAILABLE = True
except ImportError:
    REPORT_GENERATOR_AVAILABLE = False
    print("Report generator not available")

try:
    from refund_manager import show_refund_manager
    REFUND_MANAGER_AVAILABLE = True
except ImportError:
    REFUND_MANAGER_AVAILABLE = False
    print("Refund manager not available")

# Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Fallback translate function if language manager not available
def translate(key, fallback=None):
    """Fallback translation function"""
    if LANG_AVAILABLE:
        from language_manager import translate as _translate
        return _translate(key, fallback)
    return fallback or key

class BuildSmartPOS(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("BuildSmart OS - Sri Lanka's Smart Hardware POS")
        self.geometry("1400x900")
        
        # Initialize managers
        if LANG_AVAILABLE:
            self.lang_manager = get_language_manager()
        else:
            self.lang_manager = None
            
        if THEMES_AVAILABLE:
            self.theme_manager = get_theme_manager()
        else:
            self.theme_manager = None
            
        self.config = self.load_config()
        
        # Layout Configuration
        self.grid_columnconfigure(0, weight=3)  # Product List
        self.grid_columnconfigure(1, weight=1)  # Cart
        self.grid_rowconfigure(1, weight=1)     # Main content
        
        # Database Connection
        self.conn = sqlite3.connect("buildsmart_hardware.db")
        self.cursor = self.conn.cursor()
        
        # State
        self.cart = []
        self.current_customer_phone = None
        self.current_language = self.config.get("settings", {}).get("default_language", "english")
        if self.lang_manager:
            self.lang_manager.set_language(self.current_language)
        
        # UI Components
        self.create_top_bar()
        self.create_product_list_frame()
        self.create_cart_frame()
        
        # Load Initial Data
        self.load_products()
        self.check_low_stock()
    
    def load_config(self):
        """Load application configuration"""
        try:
            with open("config.json", 'r', encoding='utf-8') as f:
                 return json.load(f)
        except:
            return {}
    
    def create_top_bar(self):
        """Create top navigation bar with quick access buttons"""
        top_bar = ctk.CTkFrame(self, height=60, corner_radius=0)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
        top_bar.grid_columnconfigure(6, weight=1)  # Spacer
        
        # App Title
        title = ctk.CTkLabel(top_bar, text="🏪 BuildSmart OS", 
                            font=("Arial", 20, "bold"),
                            text_color="#2CC985")
        title.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # Language Selector
        lang_var = ctk.StringVar(value=self.current_language.capitalize())
        lang_menu = ctk.CTkOptionMenu(
            top_bar, 
            values=["English", "Sinhala", "Tamil"],
            variable=lang_var,
            command=self.change_language,
            width=120
        )
        lang_menu.grid(row=0, column=1, padx=5, pady=10)
        
        # Voice Command Button
        if VOICE_AVAILABLE:
            voice_btn = ctk.CTkButton(
                top_bar, text="🎤 Voice", width=100,
                command=self.activate_voice_command
            )
            voice_btn.grid(row=0, column=2, padx=5, pady=10)
        
        # Barcode Scanner Button
        if BARCODE_AVAILABLE:
            scan_btn = ctk.CTkButton(
                top_bar, text="📷 Scan", width=100,
                command=self.activate_barcode_scanner
            )
            scan_btn.grid(row=0, column=3, padx=5, pady=10)
        
        # Analytics Button
        analytics_btn = ctk.CTkButton(
            top_bar, text="📊 Analytics", width=100,
            command=self.show_analytics
        )
        analytics_btn.grid(row=0, column=4, padx=5, pady=10)
        
        # Construction Estimator Button
        estimator_btn = ctk.CTkButton(
            top_bar, text="🏗️ Estimator", width=100,
            command=self.show_construction_estimator
        )
        estimator_btn.grid(row=0, column=5, padx=5, pady=10)
        
        # Product Management Button
        products_btn = ctk.CTkButton(
            top_bar, text="📦 Products", width=100,
            command=self.show_product_manager,
            fg_color="#6610f2",
            hover_color="#520dc2"
        )
        products_btn.grid(row=0, column=6, padx=5, pady=10)
        
        # Customer Management Button
        customers_btn = ctk.CTkButton(
            top_bar, text="👥 Customers", width=100,
            command=self.show_customer_manager,
            fg_color="#fd7e14",
            hover_color="#e8590c"
        )
        customers_btn.grid(row=0, column=7, padx=5, pady=10)
        
        # Reports Button
        reports_btn = ctk.CTkButton(
            top_bar, text="📄 Reports", width=100,
            command=self.show_reports,
            fg_color="#20c997",
            hover_color="#17a673"
        )
        reports_btn.grid(row=0, column=8, padx=5, pady=10)
        
        # Refund Manager Button
        refund_btn = ctk.CTkButton(
            top_bar, text="🔄 Refunds", width=100,
            command=self.show_refund_manager,
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        refund_btn.grid(row=0, column=9, padx=5, pady=10)
    
    def create_product_list_frame(self):
        """Left Side: Scrollable list of products"""
        self.product_frame = ctk.CTkFrame(self, corner_radius=10)
        self.product_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Header with search
        header_frame = ctk.CTkFrame(self.product_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=10)
        
        self.lbl_title = ctk.CTkLabel(
            header_frame, 
            text=translate("available_products"),
            font=("Arial", 24, "bold")
        )
        self.lbl_title.pack(side="left", pady=10)
        
        # Search box
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_products())
        search_entry = ctk.CTkEntry(
            header_frame,
            placeholder_text=translate("search_products"),
            textvariable=self.search_var,
            width=300
        )
        search_entry.pack(side="right", padx=10)
        
        # Scrollable Container for Products
        self.scroll_products = ctk.CTkScrollableFrame(self.product_frame)
        self.scroll_products.pack(fill="both", expand=True, padx=10, pady=10)
    
    def create_cart_frame(self):
        """Right Side: Cart and Checkout"""
        self.cart_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#2B2B2B")
        self.cart_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Cart Header
        self.lbl_cart = ctk.CTkLabel(
            self.cart_frame,
            text=translate("current_cart"),
            font=("Arial", 24, "bold")
        )
        self.lbl_cart.pack(pady=10)
        
        # Customer Info Frame
        customer_frame = ctk.CTkFrame(self.cart_frame, fg_color="transparent")
        customer_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(customer_frame, text="📱", font=("Arial", 16)).pack(side="left")
        self.customer_btn = ctk.CTkButton(
            customer_frame,
            text="Add Customer",
            command=self.add_customer_info,
            width=200,
            height=30
        )
        self.customer_btn.pack(side="left", padx=5)
        
        # Cart Items List
        self.cart_items_frame = ctk.CTkScrollableFrame(self.cart_frame, height=400)
        self.cart_items_frame.pack(fill="x", padx=10, pady=5)
        
        # Total Section
        self.lbl_total = ctk.CTkLabel(
            self.cart_frame,
            text=f"{translate('total')}: LKR 0.00",
            font=("Arial", 20, "bold"),
            text_color="#2CC985"
        )
        self.lbl_total.pack(pady=20)
        
        # Loyalty Points Display
        self.lbl_loyalty = ctk.CTkLabel(
            self.cart_frame,
            text="",
            font=("Arial", 12),
            text_color="#FFA726"
        )
        self.lbl_loyalty.pack(pady=5)
        
        # WhatsApp Checkbox
        self.whatsapp_var = ctk.BooleanVar(value=False)
        whatsapp_check = ctk.CTkCheckBox(
            self.cart_frame,
            text=translate("send_whatsapp"),
            variable=self.whatsapp_var
        )
        whatsapp_check.pack(pady=5)
        
        # Checkout Button
        self.btn_checkout = ctk.CTkButton(
            self.cart_frame,
            text=translate("checkout"),
            font=("Arial", 18, "bold"),
            height=50,
            fg_color="#2CC985",
            hover_color="#24A36B",
            command=self.checkout_action
        )
        self.btn_checkout.pack(side="bottom", fill="x", padx=20, pady=20)
    
    def load_products(self, search_term=""):
        """Fetch products from DB and display them"""
        for widget in self.scroll_products.winfo_children():
            widget.destroy()
        
        try:
            if search_term:
                self.cursor.execute("""
                    SELECT id, name, price_per_unit, unit_type, stock_quantity, category
                    FROM products
                    WHERE LOWER(name) LIKE LOWER(?) OR LOWER(category) LIKE LOWER(?)
                    ORDER BY name
                """, (f"%{search_term}%", f"%{search_term}%"))
            else:
                self.cursor.execute("""
                    SELECT id, name, price_per_unit, unit_type, stock_quantity, category
                    FROM products
                    ORDER BY category, name
                """)
            
            products = self.cursor.fetchall()
            
            current_category = None
            for product in products:
                p_id, name, price, unit, stock, category = product
                
                # Category header
                if category and category != current_category:
                    cat_label = ctk.CTkLabel(
                        self.scroll_products,
                        text=f"📦 {category}",
                        font=("Arial", 14, "bold"),
                        text_color="#2CC985",
                        anchor="w"
                    )
                    cat_label.pack(fill="x", padx=5, pady=(10, 5))
                    current_category = category
                
                self.create_product_card(p_id, name, price, unit, stock)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load products: {e}")
    
    def filter_products(self):
        """Filter products based on search"""
        search_term = self.search_var.get()
        self.load_products(search_term)
    
    def create_product_card(self, p_id, name, price, unit, stock):
        """Create a card widget for a single product"""
        card = ctk.CTkFrame(self.scroll_products, fg_color="#3A3A3A", corner_radius=8)
        card.pack(fill="x", pady=5, padx=5)
        
        # Product Name
        lbl_name = ctk.CTkLabel(card, text=name, font=("Arial", 16, "bold"), anchor="w")
        lbl_name.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        # Price & Stock
        stock_color = "#2CC985" if stock > 10 else "#FFA726" if stock > 0 else "#CF6679"
        lbl_info = ctk.CTkLabel(
            card,
            text=f"LKR {price:.2f} / {unit}\n{translate('stock')}: {stock}",
            font=("Arial", 12),
            text_color=stock_color,
            justify="right"
        )
        lbl_info.pack(side="right", padx=10)
        
        # Add to Cart Button
        if stock > 0:
            btn_add = ctk.CTkButton(
                card, text="+", width=40, height=40, font=("Arial", 18),
                command=lambda: self.add_to_cart(p_id, name, price, stock)
            )
            btn_add.pack(side="right", padx=5)
        else:
            lbl_out = ctk.CTkLabel(
                card, text=translate("out_of_stock"),
                text_color="red", font=("Arial", 10, "bold")
            )
            lbl_out.pack(side="right", padx=5)
    
    def add_to_cart(self, p_id, name, price, max_stock):
        """Add item to cart or increase quantity"""
        for item in self.cart:
            if item['id'] == p_id:
                if item['qty'] < max_stock:
                    item['qty'] += 1
                    item['subtotal'] = item['qty'] * price
                    self.update_cart_ui()
                else:
                    messagebox.showwarning("Stock Limit", f"Only {max_stock} available!")
                return
        
        # Add new item
        self.cart.append({
            'id': p_id,
            'name': name,
            'price': price,
            'qty': 1,
            'subtotal': price
        })
        self.update_cart_ui()
    
    def update_cart_ui(self):
        """Refresh the cart list and total"""
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()
        
        total = 0
        for item in self.cart:
            row = ctk.CTkFrame(self.cart_items_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            txt = f"{item['name']} x{item['qty']}"
            price_txt = f"{item['subtotal']:.2f}"
            
            ctk.CTkLabel(row, text=txt, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=price_txt, anchor="e").pack(side="right", padx=5)
            
            # Remove button
            remove_btn = ctk.CTkButton(
                row, text="✖", width=25, height=25,
                fg_color="transparent", hover_color="#CF6679",
                command=lambda i=item: self.remove_from_cart(i)
            )
            remove_btn.pack(side="right", padx=2)
            
            total += item['subtotal']
        
        self.lbl_total.configure(text=f"{translate('total')}: LKR {total:.2f}")
        
        # Update loyalty points estimate
        if self.current_customer_phone and LOYALTY_AVAILABLE:
            loyalty_mgr = get_loyalty_manager()
            points = loyalty_mgr.calculate_points(total)
            self.lbl_loyalty.configure(
                text=f"⭐ +{points} {translate('loyalty_points')}"
            )
        else:
            self.lbl_loyalty.configure(text="")
    
    def remove_from_cart(self, item):
        """Remove item from cart"""
        self.cart.remove(item)
        self.update_cart_ui()
    
    def add_customer_info(self):
        """Add customer phone number"""
        phone = simpledialog.askstring(
            "Customer Info",
            translate("customer_phone") + ":",
            parent=self
        )
        
        if phone:
            self.current_customer_phone = phone
            self.customer_btn.configure(text=f"📱 {phone}")
            self.update_cart_ui()
    
    def checkout_action(self):
        """Process the transaction"""
        if not self.cart:
            messagebox.showinfo(
                translate("empty_cart"),
                translate("add_items_before_checkout")
            )
            return
        
        # Check if WhatsApp is enabled but no customer phone
        if self.whatsapp_var.get() and not self.current_customer_phone:
            response = messagebox.askyesno(
                "Customer Phone Required",
                "WhatsApp is enabled but no customer phone number added.\n\n" +
                "Would you like to add a customer phone number now?"
            )
            if response:
                self.add_customer_info()
                # Check again after adding
                if not self.current_customer_phone:
                    messagebox.showwarning(
                        "Phone Required",
                        "WhatsApp cannot be sent without a phone number.\n" +
                        "Either add a phone number or uncheck WhatsApp."
                    )
                    return
            else:
                messagebox.showwarning(
                    "WhatsApp Disabled",
                    "WhatsApp will not be sent without a phone number.\n" +
                    "Proceeding with checkout without WhatsApp."
                )
                self.whatsapp_var.set(False)
        
        total_amount = sum(item['subtotal'] for item in self.cart)
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # Get customer ID if phone provided
            customer_id = None
            if self.current_customer_phone:
                self.cursor.execute(
                    "SELECT id FROM customers WHERE phone_number = ?",
                    (self.current_customer_phone,)
                )
                result = self.cursor.fetchone()
                if result:
                    customer_id = result[0]
                else:
                    # Create new customer
                    name = simpledialog.askstring(
                        "Customer Name",
                        "Enter customer name (optional):",
                        parent=self
                    )
                    self.cursor.execute(
                        "INSERT INTO customers (phone_number, name) VALUES (?, ?)",
                        (self.current_customer_phone, name or "")
                    )
                    customer_id = self.cursor.lastrowid
            
            # Create Transaction with customer phone for refund lookup
            self.cursor.execute(
                """INSERT INTO transactions (date_time, customer_id, customer_phone, total_amount, payment_method) 
                   VALUES (?, ?, ?, ?, ?)""",
                (date_time, customer_id, self.current_customer_phone, total_amount, 'Cash')
            )
            transaction_id = self.cursor.lastrowid
            
            # Add Sales Items & Update Stock
            for item in self.cart:
                self.cursor.execute(
                    """INSERT INTO sales_items 
                    (transaction_id, product_id, quantity_sold, unit_price, sub_total) 
                    VALUES (?, ?, ?, ?, ?)""",
                    (transaction_id, item['id'], item['qty'], item['price'], item['subtotal'])
                )
                
                self.cursor.execute(
                    "UPDATE products SET stock_quantity = stock_quantity - ? WHERE id = ?",
                    (item['qty'], item['id'])
                )
            
            self.conn.commit()
            
            # Add Loyalty Points
            if customer_id and LOYALTY_AVAILABLE and self.config.get("features", {}).get("loyalty_enabled", True):
                loyalty_mgr = get_loyalty_manager()
                success, result = loyalty_mgr.add_points(
                    self.current_customer_phone,
                    total_amount,
                    transaction_id
                )
                if success:
                    points_msg = f"\n⭐ Earned {result['points_earned']} points!"
                else:
                    points_msg = ""
            else:
                points_msg = ""
            
            # Generate PDF
            pdf_path = None
            if PDF_AVAILABLE:
                pdf_path = pdf_generator.generate_bill(
                    transaction_id,
                    self.cart,
                    total_amount,
                    date_time,
                    customer_name=self.current_customer_phone
                )
            
            # Send WhatsApp (async to prevent UI freeze)
            if self.whatsapp_var.get() and self.current_customer_phone:
                if WHATSAPP_AVAILABLE and self.config.get("features", {}).get("whatsapp_enabled", True):
                    whatsapp_service = get_whatsapp_service()
                    # Send in background thread to avoid freezing UI
                    success, msg = whatsapp_service.send_invoice_async(
                        self.current_customer_phone,
                        transaction_id,
                        total_amount,
                        self.cart,
                        pdf_path
                    )
                    whatsapp_msg = f"\n📱 {msg}"
                else:
                    whatsapp_msg = ""
            else:
                whatsapp_msg = ""
            
            # Success message
            msg = f"{translate('transaction_complete')}"
            if pdf_path:
                msg += f"\n{translate('bill_saved_to')} {pdf_path}"
            msg += points_msg + whatsapp_msg
            
            messagebox.showinfo("Success", msg)
            
            # Reset
            self.cart = []
            self.current_customer_phone = None
            self.customer_btn.configure(text="Add Customer")
            self.whatsapp_var.set(False)
            self.update_cart_ui()
            self.load_products()
            
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Transaction failed: {e}")
    
    def check_low_stock(self):
        """Check and alert for low stock items"""
        try:
            self.cursor.execute("""
                SELECT name, stock_quantity, reorder_level
                FROM products
                WHERE stock_quantity <= reorder_level
            """)
            low_stock_items = self.cursor.fetchall()
            
            if low_stock_items:
                msg = f"⚠️ {translate('low_stock_alert')}\n\n"
                for item in low_stock_items[:5]:
                    msg += f"• {item[0]}: {item[1]} {translate('stock')}\n"
                
                if len(low_stock_items) > 5:
                    msg += f"\n...and {len(low_stock_items) - 5} more"
                
                # Show after a delay
                self.after(2000, lambda: messagebox.showwarning("Low Stock", msg))
        except:
            pass
    
    def change_language(self, language):
        """Change application language"""
        if not self.lang_manager:
            return
            
        lang_map = {"English": "english", "Sinhala": "sinhala", "Tamil": "tamil"}
        self.current_language = lang_map.get(language, "english")
        self.lang_manager.set_language(self.current_language)
        
        # Refresh UI
        self.refresh_ui_text()
    
    def refresh_ui_text(self):
        """Refresh all UI text after language change"""
        self.lbl_title.configure(text=translate("available_products"))
        self.lbl_cart.configure(text=translate("current_cart"))
        self.btn_checkout.configure(text=translate("checkout"))
        self.load_products()
    
    def activate_voice_command(self):
        """Activate voice command interface"""
        if not VOICE_AVAILABLE:
            messagebox.showinfo("Not Available", "Voice features require additional libraries")
            return
        
        messagebox.showinfo(
            "Voice Command",
            "Speak your command...\n\nExamples:\n- Add cement\n- Search paint\n- Checkout"
        )
        # Voice command implementation would go here
    
    def activate_barcode_scanner(self):
        """Activate barcode scanner"""
        if not BARCODE_AVAILABLE:
            messagebox.showinfo("Not Available", "Barcode scanner requires opencv-python and pyzbar")
            return
        
        messagebox.showinfo(
            "Barcode Scanner",
            "Point camera at barcode/QR code"
        )
        # Barcode scanner implementation would go here
    
    def show_analytics(self):
        """Show analytics dashboard"""
        if not ANALYTICS_AVAILABLE:
            messagebox.showinfo("Not Available", "Analytics module not loaded")
            return
            
        analytics = get_analytics_dashboard()
        summary = analytics.get_sales_summary(30)
        
        if summary:
            msg = f"📊 Sales Analytics (Last 30 Days)\n\n"
            msg += f"Today's Sales: LKR {summary['today_sales']:,.2f}\n"
            msg += f"This Month: LKR {summary['month_sales']:,.2f}\n"
            msg += f"Period Sales: LKR {summary['period_sales']:,.2f}\n"
            msg += f"Transactions: {summary['transaction_count']}\n"
            msg += f"Avg Transaction: LKR {summary['avg_transaction']:,.2f}\n\n"
            
            if summary['top_products']:
                msg += "Top Selling Products:\n"
                for i, (name, qty, revenue) in enumerate(summary['top_products'][:5], 1):
                    msg += f"{i}. {name}: {qty} units\n"
            
            messagebox.showinfo("Analytics", msg)
        else:
            messagebox.showinfo("Analytics", "No sales data available")
    
    def show_product_manager(self):
        """Show product management interface"""
        if not PRODUCT_MANAGER_AVAILABLE:
            messagebox.showinfo("Not Available", "Product manager module not loaded")
            return
        
        ProductManager(self, self)
    
    def show_customer_manager(self):
        """Show customer management interface"""
        if not CUSTOMER_MANAGER_AVAILABLE:
            messagebox.showinfo("Not Available", "Customer manager module not loaded")
            return
        
        CustomerManager(self, self)
    
    def show_reports(self):
        """Show report generator"""
        if not REPORT_GENERATOR_AVAILABLE:
            messagebox.showinfo("Not Available", "Report generator module not loaded")
            return
        
        ReportGenerator(self, self)
    
    def show_construction_estimator(self):
        """Show construction estimator"""
        if not ESTIMATOR_AVAILABLE:
            messagebox.showinfo("Not Available", "Construction estimator module not loaded")
            return
            
        estimator = get_construction_estimator()
        project_types = estimator.get_project_types()
        
        # Create simple dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Construction Estimator")
        dialog.geometry("500x400")
        
        ctk.CTkLabel(
            dialog,
            text="🏗️ Construction Project Estimator",
            font=("Arial", 18, "bold")
        ).pack(pady=20)
        
        # Project type selection
        ctk.CTkLabel(dialog, text="Select Project Type:").pack(pady=5)
        project_var = ctk.StringVar(value=project_types[0][1])
        project_menu = ctk.CTkOptionMenu(
            dialog,
            values=[pt[1] for pt in project_types],
            variable=project_var,
            width=300
        )
        project_menu.pack(pady=10)
        
        # Area input
        ctk.CTkLabel(dialog, text="Area (Square Feet):").pack(pady=5)
        area_entry = ctk.CTkEntry(dialog, width=300)
        area_entry.pack(pady=10)
        
        def calculate():
            try:
                area = float(area_entry.get())
                project_key = [k for k, v in project_types if v == project_var.get()][0]
                
                success, result = estimator.estimate_project(project_key, area)
                
                if success:
                    msg = f"Project: {result['project_name']}\n"
                    msg += f"Area: {result['area_sqft']} sqft\n\n"
                    msg += f"Material Cost: LKR {result['material_cost']:,.2f}\n"
                    msg += f"Labor Cost: LKR {result['labor_cost']:,.2f}\n"
                    msg += f"Contingency (10%): LKR {result['contingency']:,.2f}\n\n"
                    msg += f"TOTAL: LKR {result['grand_total']:,.2f}\n"
                    msg += f"Cost per sqft: LKR {result['cost_per_sqft']:,.2f}"
                    
                    messagebox.showinfo("Estimate", msg)
                else:
                    messagebox.showerror("Error", result)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid area")
        
        ctk.CTkButton(
            dialog, text="Calculate",
            command=calculate,
            width=200, height=40
        ).pack(pady=20)
    
    def show_refund_manager(self):
        """Show refund management interface"""
        if not REFUND_MANAGER_AVAILABLE:
            messagebox.showinfo("Not Available", "Refund manager module not loaded")
            return
        
        show_refund_manager(self)

if __name__ == "__main__":
    app = BuildSmartPOS()
    app.mainloop()
