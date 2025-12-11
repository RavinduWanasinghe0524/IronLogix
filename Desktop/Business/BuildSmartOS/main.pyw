import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from datetime import datetime
try:
    import pdf_generator
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("Warning: reportlab not found. PDF generation disabled.")

# Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BuildSmartPOS(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("BuildSmart OS - Hardware POS")
        self.geometry("1200x800")
        
        # Layout Configuration
        self.grid_columnconfigure(0, weight=3) # Product List Area
        self.grid_columnconfigure(1, weight=1) # Cart Area
        self.grid_rowconfigure(0, weight=1)

        # Database Connection
        self.conn = sqlite3.connect("buildsmart_hardware.db")
        self.cursor = self.conn.cursor()

        # State
        self.cart = [] # List of dicts: {id, name, price, qty, subtotal}

        # UI Components
        self.create_product_list_frame()
        self.create_cart_frame()
        
        # Load Initial Data
        self.load_products()

    def create_product_list_frame(self):
        """Left Side: Scrollable list of products"""
        self.product_frame = ctk.CTkFrame(self, corner_radius=10)
        self.product_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Header
        self.lbl_title = ctk.CTkLabel(self.product_frame, text="Available Products", font=("Arial", 24, "bold"))
        self.lbl_title.pack(pady=10)

        # Scrollable Container for Products
        self.scroll_products = ctk.CTkScrollableFrame(self.product_frame)
        self.scroll_products.pack(fill="both", expand=True, padx=10, pady=10)

    def create_cart_frame(self):
        """Right Side: Cart and Checkout"""
        self.cart_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#2B2B2B")
        self.cart_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Cart Header
        self.lbl_cart = ctk.CTkLabel(self.cart_frame, text="Current Cart", font=("Arial", 24, "bold"))
        self.lbl_cart.pack(pady=10)

        # Cart Items List
        self.cart_items_frame = ctk.CTkScrollableFrame(self.cart_frame, height=400)
        self.cart_items_frame.pack(fill="x", padx=10, pady=5)
        
        # Total Section
        self.lbl_total = ctk.CTkLabel(self.cart_frame, text="Total: LKR 0.00", font=("Arial", 20, "bold"), text_color="#2CC985")
        self.lbl_total.pack(pady=20)

        # Checkout Button
        self.btn_checkout = ctk.CTkButton(self.cart_frame, text="CHECKOUT", font=("Arial", 18, "bold"), 
                                          height=50, fg_color="#2CC985", hover_color="#24A36B",
                                          command=self.checkout_action)
        self.btn_checkout.pack(side="bottom", fill="x", padx=20, pady=20)

    def load_products(self):
        """Fetch products from DB and display them"""
        # Clear existing widgets
        for widget in self.scroll_products.winfo_children():
            widget.destroy()

        try:
            self.cursor.execute("SELECT id, name, price_per_unit, unit_type, stock_quantity FROM products")
            products = self.cursor.fetchall()

            for product in products:
                p_id, name, price, unit, stock = product
                self.create_product_card(p_id, name, price, unit, stock)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load products: {e}")

    def create_product_card(self, p_id, name, price, unit, stock):
        """Create a card widget for a single product"""
        card = ctk.CTkFrame(self.scroll_products, fg_color="#3A3A3A", corner_radius=8)
        card.pack(fill="x", pady=5, padx=5)

        # Product Name
        lbl_name = ctk.CTkLabel(card, text=name, font=("Arial", 16, "bold"), anchor="w")
        lbl_name.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        # Price & Stock
        lbl_info = ctk.CTkLabel(card, text=f"LKR {price:.2f} / {unit}\nStock: {stock}", font=("Arial", 12), text_color="#AAAAAA", justify="right")
        lbl_info.pack(side="right", padx=10)

        # Add to Cart Button
        if stock > 0:
            btn_add = ctk.CTkButton(card, text="+", width=40, height=40, font=("Arial", 18),
                                    command=lambda: self.add_to_cart(p_id, name, price, stock))
            btn_add.pack(side="right", padx=5)
        else:
            lbl_out = ctk.CTkLabel(card, text="OUT OF STOCK", text_color="red", font=("Arial", 10, "bold"))
            lbl_out.pack(side="right", padx=5)

    def add_to_cart(self, p_id, name, price, max_stock):
        """Add item to cart or increase quantity"""
        # Check if item already in cart
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
        # Clear current list
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
            
            total += item['subtotal']

        self.lbl_total.configure(text=f"Total: LKR {total:.2f}")

    def checkout_action(self):
        """Process the transaction"""
        if not self.cart:
            messagebox.showinfo("Empty Cart", "Add items before checking out.")
            return

        total_amount = sum(item['subtotal'] for item in self.cart)
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # 1. Create Transaction
            self.cursor.execute("INSERT INTO transactions (date_time, total_amount) VALUES (?, ?)", 
                                (date_time, total_amount))
            transaction_id = self.cursor.lastrowid

            # 2. Add Sales Items & Update Stock
            for item in self.cart:
                self.cursor.execute("INSERT INTO sales_items (transaction_id, product_id, quantity_sold, sub_total) VALUES (?, ?, ?, ?)",
                                    (transaction_id, item['id'], item['qty'], item['subtotal']))
                
                # Deduct Stock
                self.cursor.execute("UPDATE products SET stock_quantity = stock_quantity - ? WHERE id = ?", 
                                    (item['qty'], item['id']))

            self.conn.commit()

            # 3. Generate PDF
            if PDF_AVAILABLE:
                pdf_path = pdf_generator.generate_bill(transaction_id, self.cart, total_amount, date_time)
                msg = f"Transaction Complete!\nBill saved to: {pdf_path}"
            else:
                msg = "Transaction Complete!\n(PDF generation skipped - library missing)"
            
            messagebox.showinfo("Success", msg)
            
            # 4. Reset
            self.cart = []
            self.update_cart_ui()
            self.load_products() # Refresh stock display

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Transaction failed: {e}")

if __name__ == "__main__":
    app = BuildSmartPOS()
    app.mainloop()
