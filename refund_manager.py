"""
BuildSmartOS - Refund Manager
Search transactions and process refunds
"""

import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_NAME = "buildsmart_hardware.db"

def show_refund_manager(parent):
    """Display refund management window"""
    
    # Create refund window
    refund_window = ctk.CTkToplevel(parent)
    refund_window.title("Refund Manager")
    refund_window.geometry("1000x700")
    
    # Database connection
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Main container
    main_frame = ctk.CTkFrame(refund_window)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Title
    title_label = ctk.CTkLabel(
        main_frame,
        text="🔄 Refund Manager",
        font=("Arial", 24, "bold")
    )
    title_label.pack(pady=10)
    
    # Search section
    search_frame = ctk.CTkFrame(main_frame)
    search_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkLabel(
        search_frame,
        text="Search Transactions:",
        font=("Arial", 14, "bold")
    ).pack(pady=5)
    
    # Search options
    search_options_frame = ctk.CTkFrame(search_frame)
    search_options_frame.pack(fill="x", padx=20, pady=10)
    
    # Search by customer phone
    ctk.CTkLabel(search_options_frame, text="Customer Phone:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    phone_entry = ctk.CTkEntry(search_options_frame, width=200, placeholder_text="0771234567")
    phone_entry.grid(row=0, column=1, padx=5, pady=5)
    
    # Search by transaction ID
    ctk.CTkLabel(search_options_frame, text="Transaction ID:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    transaction_id_entry = ctk.CTkEntry(search_options_frame, width=150, placeholder_text="12345")
    transaction_id_entry.grid(row=0, column=3, padx=5, pady=5)
    
    # Search by date range
    ctk.CTkLabel(search_options_frame, text="Date From:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    date_from_entry = ctk.CTkEntry(search_options_frame, width=150, placeholder_text="YYYY-MM-DD")
    date_from_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ctk.CTkLabel(search_options_frame, text="Date To:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    date_to_entry = ctk.CTkEntry(search_options_frame, width=150, placeholder_text="YYYY-MM-DD")
    date_to_entry.grid(row=1, column=3, padx=5, pady=5)
    
    # Quick date buttons
    quick_date_frame = ctk.CTkFrame(search_frame)
    quick_date_frame.pack(pady=5)
    
    def set_today():
        today = datetime.now().strftime("%Y-%m-%d")
        date_from_entry.delete(0, "end")
        date_from_entry.insert(0, today)
        date_to_entry.delete(0, "end")
        date_to_entry.insert(0, today)
    
    def set_last_7_days():
        today = datetime.now()
        week_ago = today - timedelta(days=7)
        date_from_entry.delete(0, "end")
        date_from_entry.insert(0, week_ago.strftime("%Y-%m-%d"))
        date_to_entry.delete(0, "end")
        date_to_entry.insert(0, today.strftime("%Y-%m-%d"))
    
    def set_last_30_days():
        today = datetime.now()
        month_ago = today - timedelta(days=30)
        date_from_entry.delete(0, "end")
        date_from_entry.insert(0, month_ago.strftime("%Y-%m-%d"))
        date_to_entry.delete(0, "end")
        date_to_entry.insert(0, today.strftime("%Y-%m-%d"))
    
    ctk.CTkButton(quick_date_frame, text="Today", command=set_today, width=100).pack(side="left", padx=5)
    ctk.CTkButton(quick_date_frame, text="Last 7 Days", command=set_last_7_days, width=100).pack(side="left", padx=5)
    ctk.CTkButton(quick_date_frame, text="Last 30 Days", command=set_last_30_days, width=100).pack(side="left", padx=5)
    
    # Results section
    results_frame = ctk.CTkFrame(main_frame)
    results_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    ctk.CTkLabel(
        results_frame,
        text="Search Results:",
        font=("Arial", 14, "bold")
    ).pack(pady=5)
    
    # Results list
    results_text = ctk.CTkTextbox(results_frame, height=300, font=("Courier", 11))
    results_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Selected transaction details
    selected_transaction_id = [None]  # Using list to allow modification in nested functions
    
    details_frame = ctk.CTkFrame(main_frame)
    details_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkLabel(
        details_frame,
        text="Transaction Details:",
        font=("Arial", 14, "bold")
    ).pack(pady=5)
    
    details_text = ctk.CTkTextbox(details_frame, height=150, font=("Courier", 11))
    details_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def search_transactions():
        """Search for transactions based on criteria"""
        results_text.delete("1.0", "end")
        details_text.delete("1.0", "end")
        selected_transaction_id[0] = None
        
        # Build query
        query = """
            SELECT t.id, t.date_time, t.customer_phone, t.total_amount, t.payment_method,
                   COALESCE(r.refund_amount, 0) as refunded,
                   CASE WHEN r.id IS NOT NULL THEN 'REFUNDED' ELSE 'ACTIVE' END as status
            FROM transactions t
            LEFT JOIN refunds r ON t.id = r.transaction_id
            WHERE 1=1
        """
        params = []
        
        # Add filters
        phone = phone_entry.get().strip()
        if phone:
            query += " AND t.customer_phone LIKE ?"
            params.append(f"%{phone}%")
        
        trans_id = transaction_id_entry.get().strip()
        if trans_id:
            query += " AND t.id = ?"
            params.append(trans_id)
        
        date_from = date_from_entry.get().strip()
        if date_from:
            query += " AND DATE(t.date_time) >= ?"
            params.append(date_from)
        
        date_to = date_to_entry.get().strip()
        if date_to:
            query += " AND DATE(t.date_time) <= ?"
            params.append(date_to)
        
        query += " ORDER BY t.date_time DESC LIMIT 50"
        
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            if not results:
                results_text.insert("1.0", "No transactions found.\n")
                return
            
            # Display results
            header = f"{'ID':<6} {'Date':<20} {'Customer':<15} {'Amount':<12} {'Refunded':<12} {'Status':<10}\n"
            results_text.insert("1.0", header)
            results_text.insert("end", "=" * 90 + "\n")
            
            for row in results:
                trans_id, date, phone, amount, payment, refunded, status = row
                phone_display = phone if phone else "Walk-in"
                line = f"{trans_id:<6} {date:<20} {phone_display:<15} LKR {amount:<8.2f} LKR {refunded:<8.2f} {status:<10}\n"
                results_text.insert("end", line)
            
            results_text.insert("end", f"\nTotal: {len(results)} transaction(s) found\n")
            results_text.insert("end", "\nDouble-click a transaction ID to view details\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")
    
    def view_transaction_details(event=None):
        """View details of selected transaction"""
        try:
            # Get selected line
            index = results_text.index("insert")
            line_num = int(index.split('.')[0])
            line = results_text.get(f"{line_num}.0", f"{line_num}.end")
            
            # Skip header and separator lines
            if line_num <= 2 or "=" in line or "Total:" in line or "Double-click" in line:
                return
            
            # Extract transaction ID (first column)
            trans_id = line.split()[0]
            if not trans_id.isdigit():
                return
            
            selected_transaction_id[0] = int(trans_id)
            
            # Get transaction details
            cursor.execute("""
                SELECT t.id, t.date_time, t.customer_phone, t.total_amount, t.payment_method
                FROM transactions t
                WHERE t.id = ?
            """, (trans_id,))
            
            trans = cursor.fetchone()
            if not trans:
                return
            
            # Get transaction items
            cursor.execute("""
                SELECT si.product_id, p.name, si.quantity, si.unit_price, si.subtotal
                FROM sales_items si
                JOIN products p ON si.product_id = p.id
                WHERE si.transaction_id = ?
            """, (trans_id,))
            
            items = cursor.fetchall()
            
            # Check for existing refund
            cursor.execute("""
                SELECT refund_amount, refund_reason, refund_date
                FROM refunds
                WHERE transaction_id = ?
            """, (trans_id,))
            
            refund = cursor.fetchone()
            
            # Display details
            details_text.delete("1.0", "end")
            details_text.insert("1.0", f"TRANSACTION #{trans[0]}\n")
            details_text.insert("end", "=" * 70 + "\n")
            details_text.insert("end", f"Date: {trans[1]}\n")
            details_text.insert("end", f"Customer: {trans[2] if trans[2] else 'Walk-in Customer'}\n")
            details_text.insert("end", f"Payment: {trans[4]}\n")
            details_text.insert("end", f"Total: LKR {trans[3]:.2f}\n\n")
            
            details_text.insert("end", "ITEMS:\n")
            details_text.insert("end", "-" * 70 + "\n")
            for item in items:
                details_text.insert("end", f"{item[1]}\n")
                details_text.insert("end", f"  Qty: {item[2]} x LKR {item[3]:.2f} = LKR {item[4]:.2f}\n")
            
            if refund:
                details_text.insert("end", "\n" + "=" * 70 + "\n")
                details_text.insert("end", "⚠️ REFUND PROCESSED\n")
                details_text.insert("end", f"Refund Amount: LKR {refund[0]:.2f}\n")
                details_text.insert("end", f"Reason: {refund[1]}\n")
                details_text.insert("end", f"Date: {refund[2]}\n")
            
        except Exception as e:
            pass  # Silently ignore selection errors
    
    # Bind double-click to view details
    results_text.bind("<Double-Button-1>", view_transaction_details)
    
    def process_refund():
        """Process refund for selected transaction"""
        if not selected_transaction_id[0]:
            messagebox.showwarning("No Selection", "Please select a transaction first by double-clicking it in the results.")
            return
        
        trans_id = selected_transaction_id[0]
        
        # Check if already refunded
        cursor.execute("SELECT id FROM refunds WHERE transaction_id = ?", (trans_id,))
        if cursor.fetchone():
            messagebox.showerror("Already Refunded", "This transaction has already been refunded.")
            return
        
        # Get transaction amount
        cursor.execute("SELECT total_amount FROM transactions WHERE id = ?", (trans_id,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "Transaction not found.")
            return
        
        total_amount = result[0]
        
        # Refund dialog
        refund_dialog = ctk.CTkToplevel(refund_window)
        refund_dialog.title("Process Refund")
        refund_dialog.geometry("400x350")
        refund_dialog.grab_set()
        
        ctk.CTkLabel(
            refund_dialog,
            text=f"Process Refund for Transaction #{trans_id}",
            font=("Arial", 16, "bold")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            refund_dialog,
            text=f"Transaction Amount: LKR {total_amount:.2f}",
            font=("Arial", 14)
        ).pack(pady=10)
        
        # Refund amount
        ctk.CTkLabel(refund_dialog, text="Refund Amount:", font=("Arial", 12)).pack(pady=5)
        refund_amount_entry = ctk.CTkEntry(refund_dialog, width=200)
        refund_amount_entry.insert(0, str(total_amount))
        refund_amount_entry.pack(pady=5)
        
        # Refund reason
        ctk.CTkLabel(refund_dialog, text="Refund Reason:", font=("Arial", 12)).pack(pady=5)
        reason_entry = ctk.CTkEntry(refund_dialog, width=300, placeholder_text="e.g., Product defective, Wrong item")
        reason_entry.pack(pady=5)
        
        # Restore stock checkbox
        restore_stock_var = ctk.BooleanVar(value=True)
        restore_stock_check = ctk.CTkCheckBox(
            refund_dialog,
            text="Restore product stock",
            variable=restore_stock_var
        )
        restore_stock_check.pack(pady=10)
        
        def confirm_refund():
            try:
                refund_amount = float(refund_amount_entry.get())
                reason = reason_entry.get().strip()
                
                if refund_amount <= 0 or refund_amount > total_amount:
                    messagebox.showerror("Invalid Amount", f"Refund amount must be between 0 and {total_amount}")
                    return
                
                if not reason:
                    messagebox.showerror("Missing Reason", "Please provide a reason for the refund")
                    return
                
                # Process refund
                cursor.execute("""
                    INSERT INTO refunds (transaction_id, refund_amount, refund_reason, refund_date)
                    VALUES (?, ?, ?, ?)
                """, (trans_id, refund_amount, reason, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                
                # Restore stock if requested
                if restore_stock_var.get():
                    cursor.execute("""
                        SELECT product_id, quantity
                        FROM sales_items
                        WHERE transaction_id = ?
                    """, (trans_id,))
                    
                    items = cursor.fetchall()
                    for product_id, qty in items:
                        cursor.execute("""
                            UPDATE products
                            SET stock = stock + ?
                            WHERE id = ?
                        """, (qty, product_id))
                
                conn.commit()
                
                messagebox.showinfo(
                    "Refund Processed",
                    f"Refund of LKR {refund_amount:.2f} has been processed successfully.\n\n"
                    f"Transaction #{trans_id}\n"
                    f"Reason: {reason}"
                )
                
                refund_dialog.destroy()
                search_transactions()  # Refresh results
                
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid refund amount")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process refund: {e}")
                conn.rollback()
        
        # Buttons
        button_frame = ctk.CTkFrame(refund_dialog)
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="Process Refund",
            command=confirm_refund,
            fg_color="green",
            width=150
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=refund_dialog.destroy,
            width=150
        ).pack(side="left", padx=10)
    
    # Action buttons
    action_frame = ctk.CTkFrame(main_frame)
    action_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkButton(
        action_frame,
        text="🔍 Search",
        command=search_transactions,
        font=("Arial", 14, "bold"),
        height=40,
        width=150
    ).pack(side="left", padx=10)
    
    ctk.CTkButton(
        action_frame,
        text="🔄 Process Refund",
        command=process_refund,
        font=("Arial", 14, "bold"),
        height=40,
        width=180,
        fg_color="orange"
    ).pack(side="left", padx=10)
    
    ctk.CTkButton(
        action_frame,
        text="❌ Close",
        command=refund_window.destroy,
        font=("Arial", 14),
        height=40,
        width=120
    ).pack(side="right", padx=10)
    
    # Create refunds table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS refunds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER NOT NULL,
            refund_amount REAL NOT NULL,
            refund_reason TEXT,
            refund_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (transaction_id) REFERENCES transactions(id)
        )
    """)
    conn.commit()
    
    # Set default date range to last 30 days
    set_last_30_days()

if __name__ == "__main__":
    # Test the refund manager
    root = ctk.CTk()
    root.withdraw()
    show_refund_manager(root)
    root.mainloop()
