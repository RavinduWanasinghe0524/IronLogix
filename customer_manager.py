"""
Customer Management Module for BuildSmartOS
View and manage customer information, purchase history, and loyalty points
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import sqlite3
import csv
from datetime import datetime, timedelta

try:
    from language_manager import translate
except ImportError:
    def translate(key, fallback=None):
        return fallback or key


class CustomerManager(ctk.CTkToplevel):
    """Customer Management Window"""
    
    def __init__(self, parent, main_app):
        super().__init__(parent)
        
        self.main_app = main_app
        self.title("Customer Management - BuildSmartOS")
        self.geometry("1200x700")
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        # Database connection
        self.db_path = "buildsmart_hardware.db"
        
        # Current filter
        self.current_search = ""
        
        self.create_ui()
        self.load_customers()
        
    def create_ui(self):
        """Create the user interface"""
        
        # Title
        title = ctk.CTkLabel(
            self,
            text="👥 Customer Management",
            font=("Roboto", 24, "bold")
        )
        title.pack(pady=20)
        
        # Top controls frame
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Search box
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self.load_customers())
        
        search_entry = ctk.CTkEntry(
            controls_frame,
            placeholder_text="🔍 Search customers (name/phone)...",
            textvariable=self.search_var,
            width=400
        )
        search_entry.pack(side="left", padx=10, pady=10)
        
        # Action buttons
        add_btn = ctk.CTkButton(
            controls_frame,
            text="➕ Add Customer",
            command=self.add_customer,
            fg_color="#28a745",
            hover_color="#218838",
            width=140
        )
        add_btn.pack(side="right", padx=5)
        
        export_btn = ctk.CTkButton(
            controls_frame,
            text="📤 Export CSV",
            command=self.export_customers,
            width=140
        )
        export_btn.pack(side="right", padx=5)
        
        # Customers list frame
        self.customers_frame = ctk.CTkScrollableFrame(self, height=450)
        self.customers_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Stats footer
        self.stats_label = ctk.CTkLabel(
            self,
            text="",
            font=("Roboto", 12)
        )
        self.stats_label.pack(pady=10)
        
    def load_customers(self):
        """Load and display customers"""
        # Clear current display
        for widget in self.customers_frame.winfo_children():
            widget.destroy()
        
        # Get search value
        search_term = self.search_var.get().lower()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build query
            query = """
                SELECT c.id, c.phone_number, c.name, c.email, c.total_purchases, 
                       c.loyalty_points, c.created_date,
                       COUNT(DISTINCT t.id) as transaction_count
                FROM customers c
                LEFT JOIN transactions t ON c.id = t.customer_id
                WHERE 1=1
            """
            params = []
            
            if search_term:
                query += " AND (LOWER(c.name) LIKE ? OR c.phone_number LIKE ?)"
                params.extend([f"%{search_term}%", f"%{search_term}%"])
            
            query += " GROUP BY c.id ORDER BY c.total_purchases DESC"
            
            cursor.execute(query, params)
            customers = cursor.fetchall()
            
            # Create header
            self.create_customer_header()
            
            # Display customers
            for customer in customers:
                self.create_customer_row(customer)
            
            # Update stats
            total_customers = len(customers)
            total_value = sum(c[4] for c in customers)
            total_points = sum(c[5] for c in customers)
            active_customers = sum(1 for c in customers if c[7] > 0)
            
            self.stats_label.configure(
                text=f"👥 Total Customers: {total_customers} | 💰 Total Purchases: LKR {total_value:,.2f} | ⭐ Points: {total_points:,.0f} | ✅ Active: {active_customers}"
            )
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers: {e}")
    
    def create_customer_header(self):
        """Create table header"""
        header_frame = ctk.CTkFrame(self.customers_frame, fg_color="#2b2b2b")
        header_frame.pack(fill="x", pady=(0, 5))
        
        headers = [
            ("Name", 180),
            ("Phone", 120),
            ("Email", 180),
            ("Purchases", 110),
            ("Points", 80),
            ("Trans.", 70),
            ("Actions", 200)
        ]
        
        for text, width in headers:
            label = ctk.CTkLabel(
                header_frame,
                text=text,
                font=("Roboto", 12, "bold"),
                width=width
            )
            label.pack(side="left", padx=5, pady=5)
    
    def create_customer_row(self, customer):
        """Create a row for a customer"""
        c_id, phone, name, email, total_purchases, loyalty_points, created_date, trans_count = customer
        
        row_frame = ctk.CTkFrame(self.customers_frame)
        row_frame.pack(fill="x", pady=2)
        
        # Name
        name_label = ctk.CTkLabel(
            row_frame, 
            text=(name or "N/A")[:25], 
            width=180, 
            anchor="w"
        )
        name_label.pack(side="left", padx=5, pady=5)
        
        # Phone
        phone_label = ctk.CTkLabel(row_frame, text=phone, width=120)
        phone_label.pack(side="left", padx=5)
        
        # Email
        email_label = ctk.CTkLabel(row_frame, text=(email or "N/A")[:22], width=180)
        email_label.pack(side="left", padx=5)
        
        # Total Purchases
        purchases_label = ctk.CTkLabel(
            row_frame, 
            text=f"LKR {total_purchases:,.0f}", 
            width=110
        )
        purchases_label.pack(side="left", padx=5)
        
        # Loyalty Points
        points_label = ctk.CTkLabel(
            row_frame, 
            text=f"{loyalty_points:,.0f}", 
            width=80,
            text_color="#FFA726"
        )
        points_label.pack(side="left", padx=5)
        
        # Transaction Count
        trans_label = ctk.CTkLabel(row_frame, text=str(trans_count), width=70)
        trans_label.pack(side="left", padx=5)
        
        # Action buttons
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.pack(side="left", padx=5)
        
        view_btn = ctk.CTkButton(
            actions_frame,
            text="👁️ View",
            width=60,
            command=lambda: self.view_customer_details(customer),
            fg_color="#17a2b8",
            hover_color="#117a8b"
        )
        view_btn.pack(side="left", padx=2)
        
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="✏️ Edit",
            width=60,
            command=lambda: self.edit_customer(customer),
            fg_color="#007bff",
            hover_color="#0056b3"
        )
        edit_btn.pack(side="left", padx=2)
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            width=40,
            command=lambda: self.delete_customer(c_id, name or phone),
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        delete_btn.pack(side="left", padx=2)
    
    def add_customer(self):
        """Open dialog to add new customer"""
        CustomerDialog(self, self.db_path, callback=self.load_customers)
    
    def edit_customer(self, customer):
        """Open dialog to edit customer"""
        CustomerDialog(self, self.db_path, customer=customer, callback=self.load_customers)
    
    def view_customer_details(self, customer):
        """View customer details and purchase history"""
        CustomerDetailsWindow(self, customer, self.db_path)
    
    def delete_customer(self, customer_id, customer_name):
        """Delete a customer"""
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete customer '{customer_name}'?\n\nThis cannot be undone."
        )
        
        if result:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Check  if customer has transactions
                cursor.execute("SELECT COUNT(*) FROM transactions WHERE customer_id = ?", (customer_id,))
                trans_count = cursor.fetchone()[0]
                
                if trans_count > 0:
                    confirm_again = messagebox.askyesno(
                        "Customer Has Transactions",
                        f"This customer has {trans_count} transactions.\n\nDeleting may affect reports. Continue?"
                    )
                    if not confirm_again:
                        conn.close()
                        return
                
                cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", f"Customer '{customer_name}' deleted successfully!")
                self.load_customers()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete customer: {e}")
    
    def export_customers(self):
        """Export customers to CSV"""
        file_path = filedialog.asksaveasfilename(
            title="Save CSV File",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"customers_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if not file_path:
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT phone_number, name, email, total_purchases, loyalty_points, created_date
                FROM customers
                ORDER BY name
            """)
            
            customers = cursor.fetchall()
            conn.close()
            
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'phone_number', 'name', 'email', 'total_purchases', 
                    'loyalty_points', 'created_date'
                ])
                writer.writerows(customers)
            
            messagebox.showinfo("Success", f"Exported {len(customers)} customers to CSV!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV: {e}")


class CustomerDialog(ctk.CTkToplevel):
    """Dialog for adding/editing customers"""
    
    def __init__(self, parent, db_path, customer=None, callback=None):
        super().__init__(parent)
        
        self.db_path = db_path
        self.customer = customer
        self.callback = callback
        
        self.title("Edit Customer" if customer else "Add New Customer")
        self.geometry("500x550")
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        self.create_form()
        
        if customer:
            self.populate_form()
    
    def create_form(self):
        """Create the customer form"""
        
        # Title
        title_text = "Edit Customer" if self.customer else "Add New Customer"
        title = ctk.CTkLabel(self, text=title_text, font=("Roboto", 20, "bold"))
        title.pack(pady=20)
        
        # Form frame
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Phone Number
        ctk.CTkLabel(form_frame, text="Phone Number *", anchor="w").pack(fill="x", pady=(10, 2), padx=10)
        self.phone_entry = ctk.CTkEntry(form_frame, placeholder_text="0771234567")
        self.phone_entry.pack(fill="x", pady=(0, 5), padx=10)
        
        # Name
        ctk.CTkLabel(form_frame, text="Name", anchor="w").pack(fill="x", pady=(10, 2), padx=10)
        self.name_entry = ctk.CTkEntry(form_frame, placeholder_text="Customer Name")
        self.name_entry.pack(fill="x", pady=(0, 5), padx=10)
        
        # Email
        ctk.CTkLabel(form_frame, text="Email", anchor="w").pack(fill="x", pady=(10, 2), padx=10)
        self.email_entry = ctk.CTkEntry(form_frame, placeholder_text="customer@example.com")
        self.email_entry.pack(fill="x", pady=(0, 5), padx=10)
        
        # Address
        ctk.CTkLabel(form_frame, text="Address", anchor="w").pack(fill="x", pady=(10, 2), padx=10)
        self.address_entry = ctk.CTkTextbox(form_frame, height=100)
        self.address_entry.pack(fill="x", pady=(0, 5), padx=10)
        
        # Loyalty Points (only for edit)
        if self.customer:
            ctk.CTkLabel(form_frame, text="Loyalty Points", anchor="w").pack(fill="x", pady=(10, 2), padx=10)
            self.points_entry = ctk.CTkEntry(form_frame, placeholder_text="0")
            self.points_entry.pack(fill="x", pady=(0, 5), padx=10)
        
        # Buttons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Save Customer",
            command=self.save_customer,
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
    
    def populate_form(self):
        """Populate form with existing customer data"""
        if not self.customer:
            return
        
        c_id, phone, name, email, total_purchases, loyalty_points, created_date, trans_count = self.customer
        
        self.phone_entry.insert(0, phone)
        self.name_entry.insert(0, name or "")
        self.email_entry.insert(0, email or "")
        
        # Load address from database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT address FROM customers WHERE id = ?", (c_id,))
            result = cursor.fetchone()
            if result and result[0]:
                self.address_entry.insert("1.0", result[0])
            conn.close()
        except:
            pass
        
        if hasattr(self, 'points_entry'):
            self.points_entry.insert(0, str(loyalty_points))
    
    def save_customer(self):
        """Save customer to database"""
        # Validate
        phone = self.phone_entry.get().strip()
        if not phone:
            messagebox.showerror("Error", "Phone number is required!")
            return
        
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get("1.0", "end").strip()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if self.customer:  # Update existing
                customer_id = self.customer[0]
                
                # Update points if modified
                if hasattr(self, 'points_entry'):
                    try:
                        points = int(self.points_entry.get())
                        cursor.execute("""
                            UPDATE customers 
                            SET name=?, email=?, address=?, loyalty_points=?
                            WHERE id=?
                        """, (name, email, address, points, customer_id))
                    except ValueError:
                        cursor.execute("""
                            UPDATE customers 
                            SET name=?, email=?, address=?
                            WHERE id=?
                        """, (name, email, address, customer_id))
                else:
                    cursor.execute("""
                        UPDATE customers 
                        SET name=?, email=?, address=?
                        WHERE id=?
                    """, (name, email, address, customer_id))
                
                message = "Customer updated successfully!"
            else:  # Insert new
                cursor.execute("""
                    INSERT INTO customers (phone_number, name, email, address)
                    VALUES (?, ?, ?, ?)
                """, (phone, name, email, address))
                message = "Customer added successfully!"
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", message)
            
            if self.callback:
                self.callback()
            
            self.destroy()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Phone number already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save customer: {e}")


class CustomerDetailsWindow(ctk.CTkToplevel):
    """Window showing customer details and purchase history"""
    
    def __init__(self, parent, customer, db_path):
        super().__init__(parent)
        
        self.customer = customer
        self.db_path = db_path
        
        c_id, phone, name, email, total_purchases, loyalty_points, created_date, trans_count = customer
        
        self.title(f"Customer: {name or phone}")
        self.geometry("900x600")
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        # Header
        header = ctk.CTkLabel(
            self,
            text=f"👤 {name or 'Customer'} - {phone}",
            font=("Roboto", 22, "bold")
        )
        header.pack(pady=20)
        
        # Customer info cards
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        # Stats
        stats = [
            ("💰 Total Purchases", f"LKR {total_purchases:,.2f}"),
            ("⭐ Loyalty Points", f"{loyalty_points:,.0f}"),
            ("🧾 Transactions", str(trans_count)),
            ("📅 Customer Since", created_date[:10] if created_date else "N/A")
        ]
        
        for i, (label, value) in enumerate(stats):
            card = ctk.CTkFrame(info_frame)
            card.pack(side="left", expand=True, padx=5, pady=5)
            
            ctk.CTkLabel(card, text=label, font=("Roboto", 11)).pack(pady=(10, 2))
            ctk.CTkLabel(card, text=value, font=("Roboto", 16, "bold"), text_color="#2CC985").pack(pady=(0, 10))
        
        # Purchase history
        history_label = ctk.CTkLabel(
            self,
            text="📜 Purchase History",
            font=("Roboto", 18, "bold")
        )
        history_label.pack(pady=(20, 10))
        
        # History frame
        history_frame = ctk.CTkScrollableFrame(self, height=300)
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.load_purchase_history(history_frame, c_id)
        
        # Close button
        close_btn = ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy,
            width=200,
            height=40
        )
        close_btn.pack(pady=20)
    
    def load_purchase_history(self, parent, customer_id):
        """Load and display purchase history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.id, t.date_time, t.total_amount, t.payment_method,
                       COUNT(si.id) as item_count
                FROM transactions t
                LEFT JOIN sales_items si ON t.id = si.transaction_id
                WHERE t.customer_id = ?
                GROUP BY t.id
                ORDER BY t.date_time DESC
                LIMIT 50
            """, (customer_id,))
            
            transactions = cursor.fetchall()
            conn.close()
            
            if not transactions:
                ctk.CTkLabel(
                    parent,
                    text="No purchase history available",
                    font=("Roboto", 14)
                ).pack(pady=20)
                return
            
            # Header
            header_frame = ctk.CTkFrame(parent, fg_color="#2b2b2b")
            header_frame.pack(fill="x", pady=(0, 5))
            
            headers = [("Date/Time", 180), ("Items", 60), ("Amount", 120), ("Payment", 100)]
            for text, width in headers:
                ctk.CTkLabel(
                    header_frame,
                    text=text,
                    font=("Roboto", 12, "bold"),
                    width=width
                ).pack(side="left", padx=10, pady=5)
            
            # Transactions
            for trans in transactions:
                trans_id, date_time, amount, payment, item_count = trans
                
                row = ctk.CTkFrame(parent)
                row.pack(fill="x", pady=2)
                
                ctk.CTkLabel(row, text=date_time, width=180, anchor="w").pack(side="left", padx=10, pady=5)
                ctk.CTkLabel(row, text=str(item_count), width=60).pack(side="left", padx=10)
                ctk.CTkLabel(row, text=f"LKR {amount:,.2f}", width=120).pack(side="left", padx=10)
                ctk.CTkLabel(row, text=payment or "Cash", width=100).pack(side="left", padx=10)
                
        except Exception as e:
            ctk.CTkLabel(
                parent,
                text=f"Error loading history: {e}",
                font=("Roboto", 12),
                text_color="red"
            ).pack(pady=20)


if __name__ == "__main__":
    # Test the module
    app = ctk.CTk()
    app.withdraw()
    CustomerManager(app, app)
    app.mainloop()
