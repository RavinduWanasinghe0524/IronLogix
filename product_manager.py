"""
Product Management Module for BuildSmartOS
Complete CRUD operations for product inventory
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import sqlite3
import csv
from datetime import datetime
import os

try:
    from language_manager import translate
except ImportError:
    def translate(key, fallback=None):
        return fallback or key


class ProductManager(ctk.CTkToplevel):
    """Product Management Window"""
    
    def __init__(self, parent, main_app):
        super().__init__(parent)
        
        self.main_app = main_app
        self.title("Product Management - BuildSmartOS")
        self.geometry("1200x700")
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        # Database connection
        self.db_path = "buildsmart_hardware.db"
        
        # Current filter
        self.current_search = ""
        self.current_category = "All"
        
        self.create_ui()
        self.load_products()
        
    def create_ui(self):
        """Create the user interface"""
        
        # Title
        title = ctk.CTkLabel(
            self,
            text="📦 Product Management",
            font=("Roboto", 24, "bold")
        )
        title.pack(pady=20)
        
        # Top controls frame
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Search box
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self.load_products())
        
        search_entry = ctk.CTkEntry(
            controls_frame,
            placeholder_text="🔍 Search products...",
            textvariable=self.search_var,
            width=300
        )
        search_entry.pack(side="left", padx=10, pady=10)
        
        # Category filter
        self.category_var = ctk.StringVar(value="All")
        categories = self.get_categories()
        
        category_menu = ctk.CTkOptionMenu(
            controls_frame,
            values=categories,
            variable=self.category_var,
            command=lambda x: self.load_products()
        )
        category_menu.pack(side="left", padx=10)
        
        # Action buttons
        add_btn = ctk.CTkButton(
            controls_frame,
            text="➕ Add Product",
            command=self.add_product,
            fg_color="#28a745",
            hover_color="#218838",
            width=140
        )
        add_btn.pack(side="right", padx=5)
        
        export_btn = ctk.CTkButton(
            controls_frame,
            text="📤 Export CSV",
            command=self.export_products,
            width=140
        )
        export_btn.pack(side="right", padx=5)
        
        import_btn = ctk.CTkButton(
            controls_frame,
            text="📥 Import CSV",
            command=self.import_products,
            width=140
        )
        import_btn.pack(side="right", padx=5)
        
        # Products list frame
        self.products_frame = ctk.CTkScrollableFrame(self, height=450)
        self.products_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Stats footer
        self.stats_label = ctk.CTkLabel(
            self,
            text="",
            font=("Roboto", 12)
        )
        self.stats_label.pack(pady=10)
        
    def get_categories(self):
        """Get all unique categories from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM products WHERE category IS NOT NULL ORDER BY category")
            categories = ["All"] + [row[0] for row in cursor.fetchall()]
            conn.close()
            return categories
        except Exception as e:
            print(f"Error getting categories: {e}")
            return ["All"]
    
    def load_products(self):
        """Load and display products"""
        # Clear current display
        for widget in self.products_frame.winfo_children():
            widget.destroy()
        
        # Get search and filter values
        search_term = self.search_var.get().lower()
        category = self.category_var.get()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build query
            query = "SELECT id, name, category, price_per_unit, cost_price, stock_quantity, unit_type, barcode, reorder_level FROM products WHERE 1=1"
            params = []
            
            if search_term:
                query += " AND (LOWER(name) LIKE ? OR LOWER(category) LIKE ? OR barcode LIKE ?)"
                params.extend([f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"])
            
            if category != "All":
                query += " AND category = ?"
                params.append(category)
            
            query += " ORDER BY name"
            
            cursor.execute(query, params)
            products = cursor.fetchall()
            
            # Create header
            self.create_product_header()
            
            # Display products
            for product in products:
                self.create_product_row(product)
            
            # Update stats
            total_value = sum(p[3] * p[5] for p in products)
            low_stock = sum(1 for p in products if p[5] <= p[8])
            
            self.stats_label.configure(
                text=f"📊 Total Products: {len(products)} | 💰 Inventory Value: LKR {total_value:,.2f} | ⚠️ Low Stock: {low_stock}"
            )
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {e}")
    
    def create_product_header(self):
        """Create table header"""
        header_frame = ctk.CTkFrame(self.products_frame, fg_color="#2b2b2b")
        header_frame.pack(fill="x", pady=(0, 5))
        
        headers = [
            ("Name", 200),
            ("Category", 120),
            ("Price", 100),
            ("Cost", 100),
            ("Stock", 80),
            ("Unit", 80),
            ("Barcode", 120),
            ("Actions", 180)
        ]
        
        for text, width in headers:
            label = ctk.CTkLabel(
                header_frame,
                text=text,
                font=("Roboto", 12, "bold"),
                width=width
            )
            label.pack(side="left", padx=5, pady=5)
    
    def create_product_row(self, product):
        """Create a row for a product"""
        p_id, name, category, price, cost, stock, unit, barcode, reorder = product
        
        row_frame = ctk.CTkFrame(self.products_frame)
        row_frame.pack(fill="x", pady=2)
        
        # Color code based on stock
        if stock <= reorder:
            row_frame.configure(fg_color="#3d2020")  # Red tint for low stock
        
        # Name
        name_label = ctk.CTkLabel(row_frame, text=name[:30], width=200, anchor="w")
        name_label.pack(side="left", padx=5, pady=5)
        
        # Category
        cat_label = ctk.CTkLabel(row_frame, text=category or "N/A", width=120)
        cat_label.pack(side="left", padx=5)
        
        # Price
        price_label = ctk.CTkLabel(row_frame, text=f"LKR {price:,.2f}", width=100)
        price_label.pack(side="left", padx=5)
        
        # Cost
        cost_label = ctk.CTkLabel(row_frame, text=f"LKR {cost:,.2f}", width=100)
        cost_label.pack(side="left", padx=5)
        
        # Stock
        stock_label = ctk.CTkLabel(row_frame, text=f"{stock:.0f}", width=80)
        stock_label.pack(side="left", padx=5)
        
        # Unit
        unit_label = ctk.CTkLabel(row_frame, text=unit, width=80)
        unit_label.pack(side="left", padx=5)
        
        # Barcode
        barcode_label = ctk.CTkLabel(row_frame, text=barcode or "N/A", width=120)
        barcode_label.pack(side="left", padx=5)
        
        # Action buttons
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.pack(side="left", padx=5)
        
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="✏️ Edit",
            width=70,
            command=lambda: self.edit_product(product),
            fg_color="#007bff",
            hover_color="#0056b3"
        )
        edit_btn.pack(side="left", padx=2)
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️ Delete",
            width=70,
            command=lambda: self.delete_product(p_id, name),
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        delete_btn.pack(side="left", padx=2)
    
    def add_product(self):
        """Open dialog to add new product"""
        ProductDialog(self, self.db_path, callback=self.load_products)
    
    def edit_product(self, product):
        """Open dialog to edit product"""
        ProductDialog(self, self.db_path, product=product, callback=self.load_products)
    
    def delete_product(self, product_id, product_name):
        """Delete a product"""
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{product_name}'?\n\nThis cannot be undone."
        )
        
        if result:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Check if product has sales
                cursor.execute("SELECT COUNT(*) FROM sales_items WHERE product_id = ?", (product_id,))
                sales_count = cursor.fetchone()[0]
                
                if sales_count > 0:
                    confirm_again = messagebox.askyesno(
                        "Product Has Sales",
                        f"This product has {sales_count} sales records.\n\nDeleting it may affect reports. Continue?"
                    )
                    if not confirm_again:
                        conn.close()
                        return
                
                cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", f"Product '{product_name}' deleted successfully!")
                self.load_products()
                
                # Refresh main app if available
                if hasattr(self.main_app, 'load_products'):
                    self.main_app.load_products()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product: {e}")
    
    def import_products(self):
        """Import products from CSV"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                imported = 0
                skipped = 0
                
                for row in csv_reader:
                    try:
                        cursor.execute("""
                            INSERT INTO products (name, category, price_per_unit, cost_price, stock_quantity, 
                                                unit_type, barcode, reorder_level)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            row.get('name', ''),
                            row.get('category', ''),
                            float(row.get('price_per_unit', 0)),
                            float(row.get('cost_price', 0)),
                            float(row.get('stock_quantity', 0)),
                            row.get('unit_type', 'Unit'),
                            row.get('barcode', ''),
                            int(row.get('reorder_level', 10))
                        ))
                        imported += 1
                    except Exception as e:
                        print(f"Skipped row: {e}")
                        skipped += 1
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo(
                    "Import Complete",
                    f"Imported: {imported} products\nSkipped: {skipped} rows"
                )
                
                self.load_products()
                if hasattr(self.main_app, 'load_products'):
                    self.main_app.load_products()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import CSV: {e}")
    
    def export_products(self):
        """Export products to CSV"""
        file_path = filedialog.asksaveasfilename(
            title="Save CSV File",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"products_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if not file_path:
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, category, price_per_unit, cost_price, stock_quantity, 
                       unit_type, barcode, reorder_level
                FROM products
                ORDER BY name
            """)
            
            products = cursor.fetchall()
            conn.close()
            
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'name', 'category', 'price_per_unit', 'cost_price', 
                    'stock_quantity', 'unit_type', 'barcode', 'reorder_level'
                ])
                writer.writerows(products)
            
            messagebox.showinfo("Success", f"Exported {len(products)} products to CSV!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV: {e}")


class ProductDialog(ctk.CTkToplevel):
    """Dialog for adding/editing products"""
    
    def __init__(self, parent, db_path, product=None, callback=None):
        super().__init__(parent)
        
        self.db_path = db_path
        self.product = product
        self.callback = callback
        
        self.title("Edit Product" if product else "Add New Product")
        self.geometry("500x650")
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        self.create_form()
        
        if product:
            self.populate_form()
    
    def create_form(self):
        """Create the product form"""
        
        # Title
        title_text = "Edit Product" if self.product else "Add New Product"
        title = ctk.CTkLabel(self, text=title_text, font=("Roboto", 20, "bold"))
        title.pack(pady=20)
        
        # Form frame
        form_frame = ctk.CTkScrollableFrame(self, height=450)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Product Name
        self.create_field(form_frame, "Product Name *", "name_entry", "e.g., Cement 50kg")
        
        # Category
        self.create_field(form_frame, "Category", "category_entry", "e.g., Building Materials")
        
        # Price
        self.create_field(form_frame, "Selling Price (LKR) *", "price_entry", "0.00")
        
        # Cost Price
        self.create_field(form_frame, "Cost Price (LKR)", "cost_entry", "0.00")
        
        # Stock Quantity
        self.create_field(form_frame, "Stock Quantity *", "stock_entry", "0")
        
        # Unit Type
        self.create_field(form_frame, "Unit Type *", "unit_entry", "e.g., kg, Unit, Bag")
        
        # Barcode
        self.create_field(form_frame, "Barcode/SKU", "barcode_entry", "Optional")
        
        # Reorder Level
        self.create_field(form_frame, "Reorder Level", "reorder_entry", "10")
        
        # Description
        ctk.CTkLabel(form_frame, text="Description", anchor="w").pack(fill="x", pady=(10, 2))
        self.description_entry = ctk.CTkTextbox(form_frame, height=80)
        self.description_entry.pack(fill="x", pady=(0, 10))
        
        # Buttons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Save Product",
            command=self.save_product,
            fg_color="#28a745",
            hover_color="#218838",
            height=40
        )
        save_btn.pack(side="left", expand=True, padx=5)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="❌ Cancel",
            command=self.destroy,
            fg_color="#6c757d",
            hover_color="#5a6268",
            height=40
        )
        cancel_btn.pack(side="left", expand=True, padx=5)
    
    def create_field(self, parent, label_text, attr_name, placeholder):
        """Create a form field"""
        ctk.CTkLabel(parent, text=label_text, anchor="w").pack(fill="x", pady=(10, 2))
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder)
        entry.pack(fill="x", pady=(0, 5))
        setattr(self, attr_name, entry)
    
    def populate_form(self):
        """Populate form with existing product data"""
        if not self.product:
            return
        
        p_id, name, category, price, cost, stock, unit, barcode, reorder = self.product
        
        self.name_entry.insert(0, name)
        self.category_entry.insert(0, category or "")
        self.price_entry.insert(0, str(price))
        self.cost_entry.insert(0, str(cost))
        self.stock_entry.insert(0, str(stock))
        self.unit_entry.insert(0, unit)
        self.barcode_entry.insert(0, barcode or "")
        self.reorder_entry.insert(0, str(reorder))
    
    def save_product(self):
        """Save product to database"""
        # Validate
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Product name is required!")
            return
        
        try:
            price = float(self.price_entry.get())
            cost = float(self.cost_entry.get() or 0)
            stock = float(self.stock_entry.get())
            reorder = int(self.reorder_entry.get() or 10)
        except ValueError:
            messagebox.showerror("Error", "Invalid numeric values!")
            return
        
        unit = self.unit_entry.get().strip()
        if not unit:
            messagebox.showerror("Error", "Unit type is required!")
            return
        
        category = self.category_entry.get().strip()
        barcode = self.barcode_entry.get().strip()
        description = self.description_entry.get("1.0", "end").strip()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if self.product:  # Update existing
                product_id = self.product[0]
                cursor.execute("""
                    UPDATE products 
                    SET name=?, category=?, price_per_unit=?, cost_price=?, 
                        stock_quantity=?, unit_type=?, barcode=?, reorder_level=?, description=?
                    WHERE id=?
                """, (name, category, price, cost, stock, unit, barcode, reorder, description, product_id))
                message = "Product updated successfully!"
            else:  # Insert new
                cursor.execute("""
                    INSERT INTO products (name, category, price_per_unit, cost_price, 
                                        stock_quantity, unit_type, barcode, reorder_level, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, category, price, cost, stock, unit, barcode, reorder, description))
                message = "Product added successfully!"
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", message)
            
            if self.callback:
                self.callback()
            
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save product: {e}")


if __name__ == "__main__":
    # Test the module
    app = ctk.CTk()
    app.withdraw()
    ProductManager(app, app)
    app.mainloop()
