"""
Report Generator Module for BuildSmartOS
Generate comprehensive business reports in text and CSV formats
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import sqlite3
import csv
from datetime import datetime, timedelta
import os


class ReportGenerator(ctk.CTkToplevel):
    """Report Generator Window"""
    
    def __init__(self, parent, main_app):
        super().__init__(parent)
        
        self.main_app = main_app
        self.title("Report Generator - BuildSmartOS")
        self.geometry("1000x700")
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        # Database connection
        self.db_path = "buildsmart_hardware.db"
        
        self.create_ui()
        
    def create_ui(self):
        """Create the user interface"""
        
        # Title
        title = ctk.CTkLabel(
            self,
            text="📊 Report Generator",
            font=("Roboto", 24, "bold")
        )
        title.pack(pady=20)
        
        # Report types frame
        types_frame = ctk.CTkFrame(self)
        types_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left side - report selection
        selection_frame = ctk.CTkFrame(types_frame, width=300)
        selection_frame.pack(side="left", fill="y", padx=(0, 10), pady=10)
        
        ctk.CTkLabel(
            selection_frame,
            text="Select Report Type",
            font=("Roboto", 16, "bold")
        ).pack(pady=10)
        
        # Report types
        reports = [
            ("📈 Daily Sales Report", self.generate_daily_sales),
            ("📅 Monthly Sales Report", self.generate_monthly_sales),
            ("📊 Product Performance", self.generate_product_performance),
            ("💰 Profit Analysis", self.generate_profit_analysis),
            ("👥 Customer Report", self.generate_customer_report),
            ("📦 Inventory Report", self.generate_inventory_report),
            ("⚠️ Low Stock Alert", self.generate_low_stock_report),
            ("💳 Payment Methods", self.generate_payment_methods_report),
            ("🏆 Top Customers", self.generate_top_customers_report),
            ("📉 Sales Trends (7 Days)", self.generate_sales_trend_report),
        ]
        
        for text, command in reports:
            btn = ctk.CTkButton(
                selection_frame,
                text=text,
                command=command,
                anchor="w",
                height=40
            )
            btn.pack(fill="x", padx=10, pady=5)
        
        # Right side - report display
        self.report_frame = ctk.CTkScrollableFrame(types_frame)
        self.report_frame.pack(side="right", fill="both", expand=True, pady=10)
        
        # Display initial message
        self.report_text = ctk.CTkTextbox(self.report_frame, font=("Courier New", 11))
        self.report_text.pack(fill="both", expand=True)
        self.report_text.insert("1.0", "Select a report type from the left to generate a report...")
        self.report_text.configure(state="disabled")
        
        # Export buttons frame
        export_frame = ctk.CTkFrame(self)
        export_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            export_frame,
            text="📄 Export as TXT",
            command=self.export_txt,
            width=150,
            height=40
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            export_frame,
            text="📊 Export as CSV",
            command=self.export_csv,
            width=150,
            height=40
        ).pack(side="left", padx=5)
        
        self.current_report_data = None
        self.current_report_type = None
    
    def display_report(self, title, content, data=None):
        """Display report in the text area"""
        self.report_text.configure(state="normal")
        self.report_text.delete("1.0", "end")
        
        # Header
        header = "="*80 + "\n"
        header += f"{title}\n"
        header += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += "="*80 + "\n\n"
        
        self.report_text.insert("1.0", header + content)
        self.report_text.configure(state="disabled")
        
        self.current_report_data = data
        self.current_report_type = title
    
    def generate_daily_sales(self):
        """Generate daily sales report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Get transactions
            cursor.execute("""
                SELECT t.id, t.date_time, t.total_amount, t.payment_method,
                       c.name, c.phone_number
                FROM transactions t
                LEFT JOIN customers c ON t.customer_id = c.id
                WHERE DATE(t.date_time) = ?
                ORDER BY t.date_time DESC
            """, (today,))
            
            transactions = cursor.fetchall()
            
            # Calculate stats
            total_sales = sum(t[2] for t in transactions)
            transaction_count = len(transactions)
            avg_transaction = total_sales / transaction_count if transaction_count > 0 else 0
            
            # Build report
            content = f"Date: {today}\n\n"
            content += f"Total Sales: LKR {total_sales:,.2f}\n"
            content += f"Transactions: {transaction_count}\n"
            content += f"Average Transaction: LKR {avg_transaction:,.2f}\n\n"
            content += "-"*80 + "\n"
            content += f"{'Time':<20} {'Customer':<25} {'Amount':<15} {'Payment'}\n"
            content += "-"*80 + "\n"
            
            for trans in transactions:
                trans_id, date_time, amount, payment, cust_name, cust_phone = trans
                time = date_time.split()[1] if ' ' in date_time else date_time
                customer = cust_name or cust_phone or "Walk-in"
                content += f"{time:<20} {customer[:24]:<25} {f'LKR {amount:,.2f}':<15} {payment or 'Cash'}\n"
            
            conn.close()
            
            self.display_report("DAILY SALES REPORT", content, transactions)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def generate_monthly_sales(self):
        """Generate monthly sales report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current month
            now = datetime.now()
            month_start = now.replace(day=1).strftime('%Y-%m-%d')
            
            # Get monthly data
            cursor.execute("""
                SELECT DATE(date_time) as sale_date,
                       COUNT(*) as transactions,
                       SUM(total_amount) as daily_sales
                FROM transactions
                WHERE DATE(date_time) >= ?
                GROUP BY DATE(date_time)
                ORDER BY sale_date
            """, (month_start,))
            
            daily_data = cursor.fetchall()
            
            # Total stats
            total_sales = sum(d[2] for d in daily_data)
            total_transactions = sum(d[1] for d in daily_data)
            avg_daily = total_sales / len(daily_data) if daily_data else 0
            
            # Build report
            content = f"Month: {now.strftime('%B %Y')}\n\n"
            content += f"Total Sales: LKR {total_sales:,.2f}\n"
            content += f"Total Transactions: {total_transactions}\n"
            content += f"Average Daily Sales: LKR {avg_daily:,.2f}\n"
            content += f"Trading Days: {len(daily_data)}\n\n"
            content += "-"*80 + "\n"
            content += f"{'Date':<15} {'Transactions':<15} {'Sales'}\n"
            content += "-"*80 + "\n"
            
            for date, trans_count, sales in daily_data:
                content += f"{date:<15} {trans_count:<15} LKR {sales:,.2f}\n"
            
            conn.close()
            
            self.display_report("MONTHLY SALES REPORT", content, daily_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def generate_product_performance(self):
        """Generate product performance report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT p.name, p.category,
                       COUNT(si.id) as times_sold,
                       SUM(si.quantity_sold) as total_quantity,
                       SUM(si.sub_total) as total_revenue,
                       p.stock_quantity
                FROM products p
                LEFT JOIN sales_items si ON p.id = si.product_id
                GROUP BY p.id
                ORDER BY total_revenue DESC
            """)
            
            products = cursor.fetchall()
            
            # Build report
            content = f"Total Products: {len(products)}\n\n"
            content += "-"*100 + "\n"
            content += f"{'Product':<35} {'Category':<15} {'Qty Sold':<12} {'Revenue':<18} {'Stock'}\n"
            content += "-"*100 + "\n"
            
            for prod in products:
                name, category, times_sold, quantity, revenue, stock = prod
                quantity = quantity or 0
                revenue = revenue or 0
                content += f"{name[:34]:<35} {(category or 'N/A')[:14]:<15} {quantity:<12.0f} {f'LKR {revenue:,.2f}':<18} {stock:.0f}\n"
            
            conn.close()
            
            self.display_report("PRODUCT PERFORMANCE REPORT", content, products)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def generate_profit_analysis(self):
        """Generate profit analysis report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT p.name, p.category,
                       SUM(si.quantity_sold) as quantity_sold,
                       p.cost_price, p.price_per_unit,
                       SUM(si.sub_total) as revenue,
                       SUM(si.quantity_sold * p.cost_price) as cost
                FROM sales_items si
                JOIN products p ON si.product_id = p.id
                GROUP BY si.product_id
                ORDER BY (SUM(si.sub_total) - SUM(si.quantity_sold * p.cost_price)) DESC
            """)
            
            products = cursor.fetchall()
            
            total_revenue = sum(p[5] for p in products)
            total_cost = sum(p[6] for p in products)
            total_profit = total_revenue - total_cost
            profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
            
            # Build report
            content = f"Total Revenue: LKR {total_revenue:,.2f}\n"
            content += f"Total Cost: LKR {total_cost:,.2f}\n"
            content += f"Total Profit: LKR {total_profit:,.2f}\n"
            content += f"Profit Margin: {profit_margin:.2f}%\n\n"
            content += "-"*110 + "\n"
            content += f"{'Product':<30} {'Category':<12} {'Qty':<8} {'Revenue':<16} {'Cost':<16} {'Profit':<16} {'Margin'}\n"
            content += "-"*110 + "\n"
            
            for prod in products:
                name, category, qty, cost_price, sell_price, revenue, cost = prod
                profit = revenue - cost
                margin = (profit / revenue * 100) if revenue > 0 else 0
                
                content += f"{name[:29]:<30} {(category or 'N/A')[:11]:<12} {qty:<8.0f} "
                content += f"{f'LKR {revenue:,.0f}':<16} {f'LKR {cost:,.0f}':<16} "
                content += f"{f'LKR {profit:,.0f}':<16} {margin:.1f}%\n"
            
            conn.close()
            
            self.display_report("PROFIT ANALYSIS REPORT", content, products)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def generate_customer_report(self):
        """Generate customer report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT c.name, c.phone_number, c.total_purchases, c.loyalty_points,
                       COUNT(t.id) as transaction_count,
                       MAX(t.date_time) as last_purchase
                FROM customers c
                LEFT JOIN transactions t ON c.id = t.customer_id
                GROUP BY c.id
                ORDER BY c.total_purchases DESC
            """)
            
            customers = cursor.fetchall()
            
            total_customers = len(customers)
            total_value = sum(c[2] for c in customers)
            active_customers = sum(1 for c in customers if c[4] > 0)
            
            # Build report
            content = f"Total Customers: {total_customers}\n"
            content += f"Active Customers: {active_customers}\n"
            content += f"Total Customer Value: LKR {total_value:,.2f}\n"
            content += f"Average Value: LKR {total_value/total_customers if total_customers > 0 else 0:,.2f}\n\n"
            content += "-"*105 + "\n"
            content += f"{'Name':<25} {'Phone':<15} {'Purchases':<16} {'Points':<10} {'Trans.':<10} {'Last Purchase'}\n"
            content += "-"*105 + "\n"
            
            for cust in customers:
                name, phone, purchases, points, trans_count, last_purchase = cust
                last = last_purchase[:10] if last_purchase else "Never"
                content += f"{(name or 'N/A')[:24]:<25} {phone:<15} {f'LKR {purchases:,.0f}':<16} "
                content += f"{points:<10.0f} {trans_count:<10} {last}\n"
            
            conn.close()
            
            self.display_report("CUSTOMER REPORT", content, customers)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def generate_inventory_report(self):
        """Generate inventory valuation report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, category, stock_quantity, cost_price, price_per_unit,
                       (stock_quantity * cost_price) as cost_value,
                       (stock_quantity * price_per_unit) as selling_value
                FROM products
                WHERE stock_quantity > 0
                ORDER BY cost_value DESC
            """)
            
            products = cursor.fetchall()
            
            total_cost = sum(p[5] for p in products)
            total_selling = sum(p[6] for p in products)
            potential_profit = total_selling - total_cost
            
            # Build report
            content = f"Items in Stock: {len(products)}\n"
            content += f"Total Inventory Cost: LKR {total_cost:,.2f}\n"
            content += f"Total Selling Value: LKR {total_selling:,.2f}\n"
            content += f"Potential Profit: LKR {potential_profit:,.2f}\n\n"
            content += "-"*110 + "\n"
            content += f"{'Product':<30} {'Category':<12} {'Stock':<10} {'Cost/Unit':<14} {'Cost Value':<16} {'Sell Value'}\n"
            content += "-"*110 + "\n"
            
            for prod in products:
                name, category, stock, cost_price, sell_price, cost_val, sell_val = prod
                content += f"{name[:29]:<30} {(category or 'N/A')[:11]:<12} {stock:<10.0f} "
                content += f"{f'LKR {cost_price:,.0f}':<14} {f'LKR {cost_val:,.0f}':<16} LKR {sell_val:,.0f}\n"
            
            conn.close()
            
            self.display_report("INVENTORY VALUATION REPORT", content, products)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def generate_low_stock_report(self):
        """Generate low stock alert report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, category, stock_quantity, reorder_level, 
                       price_per_unit, supplier_id
                FROM products
                WHERE stock_quantity <= reorder_level
                ORDER BY (reorder_level - stock_quantity) DESC
            """)
            
            products = cursor.fetchall()
            
            # Build report
            content = f"⚠️ Low Stock Items: {len(products)}\n\n"
            
            if not products:
                content += "All products are adequately stocked!\n"
            else:
                content += "-"*90 + "\n"
                content += f"{'Product':<35} {'Category':<15} {'Stock':<10} {'Reorder':<10} {'Status'}\n"
                content += "-"*90 + "\n"
                
                for prod in products:
                    name, category, stock, reorder, price, supplier = prod
                    shortage = reorder - stock
                    status = "CRITICAL" if stock <= reorder * 0.5 else "LOW"
                    content += f"{name[:34]:<35} {(category or 'N/A')[:14]:<15} {stock:<10.0f} {reorder:<10} {status}\n"
            
            conn.close()
            
            self.display_report("LOW STOCK ALERT REPORT", content, products)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def generate_payment_methods_report(self):
        """Generate payment methods breakdown"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT payment_method, COUNT(*) as count, SUM(total_amount) as total
                FROM transactions
                GROUP BY payment_method
                ORDER BY total DESC
            """)
            
            methods = cursor.fetchall()
            
            total_amount = sum(m[2] for m in methods)
            
            # Build report
            content = f"Total Sales: LKR {total_amount:,.2f}\n\n"
            content += "-"*70 + "\n"
            content += f"{'Payment Method':<25} {'Transactions':<18} {'Amount':<20} {'%'}\n"
            content += "-"*70 + "\n"
            
            for method, count, amount in methods:
                percentage = (amount / total_amount * 100) if total_amount > 0 else 0
                content += f"{(method or 'Cash'):<25} {count:<18} {f'LKR {amount:,.2f}':<20} {percentage:.1f}%\n"
            
            conn.close()
            
            self.display_report("PAYMENT METHODS REPORT", content, methods)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def generate_top_customers_report(self):
        """Generate top customers report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT c.name, c.phone_number, c.total_purchases, 
                       COUNT(t.id) as transactions,
                       AVG(t.total_amount) as avg_transaction
                FROM customers c
                JOIN transactions t ON c.id = t.customer_id
                GROUP BY c.id
                ORDER BY c.total_purchases DESC
                LIMIT 20
            """)
            
            customers = cursor.fetchall()
            
            # Build report
            content = f"Top 20 Customers by Purchase Value\n\n"
            content += "-"*95 + "\n"
            content += f"{'Rank':<6} {'Name':<25} {'Phone':<15} {'Total':<18} {'Trans.':<10} {'Avg'}\n"
            content += "-"*95 + "\n"
            
            for i, cust in enumerate(customers, 1):
                name, phone, total, trans, avg in cust
                content += f"{i:<6} {(name or 'N/A')[:24]:<25} {phone:<15} {f'LKR {total:,.0f}':<18} {trans:<10} LKR {avg:,.0f}\n"
            
            conn.close()
            
            self.display_report("TOP CUSTOMERS REPORT", content, customers)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def generate_sales_trend_report(self):
        """Generate 7-day sales trend"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Last 7 days
            dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
            
            daily_sales = []
            for date in dates:
                cursor.execute("""
                    SELECT COUNT(*), COALESCE(SUM(total_amount), 0)
                    FROM transactions
                    WHERE DATE(date_time) = ?
                """, (date,))
                count, total = cursor.fetchone()
                daily_sales.append((date, count, total))
            
            total_week = sum(d[2] for d in daily_sales)
            avg_daily = total_week / 7
            
            # Build report
            content = f"7-Day Sales Trend\n\n"
            content += f"Total Week Sales: LKR {total_week:,.2f}\n"
            content += f"Average Daily: LKR {avg_daily:,.2f}\n\n"
            content += "-"*70 + "\n"
            content += f"{'Date':<15} {'Day':<12} {'Transactions':<15} {'Sales'}\n"
            content += "-"*70 + "\n"
            
            for date_str, count, total in daily_sales:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                day_name = date_obj.strftime('%A')
                content += f"{date_str:<15} {day_name:<12} {count:<15} LKR {total:,.2f}\n"
            
            conn.close()
            
            self.display_report("SALES TREND REPORT (7 DAYS)", content, daily_sales)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def export_txt(self):
        """Export current report as TXT"""
        if not self.current_report_type:
            messagebox.showinfo("No Report", "Generate a report first before exporting.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Report as TXT",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"{self.current_report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if file_path:
            try:
                content = self.report_text.get("1.0", "end")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Report exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
    
    def export_csv(self):
        """Export current report data as CSV"""
        if not self.current_report_data:
            messagebox.showinfo("No Data", "This report cannot be exported as CSV.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Report as CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"{self.current_report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(self.current_report_data)
                messagebox.showinfo("Success", f"Report exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")


if __name__ == "__main__":
    # Test the module
    app = ctk.CTk()
    app.withdraw()
    ReportGenerator(app, app)
    app.mainloop()
