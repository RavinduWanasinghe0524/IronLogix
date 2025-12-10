"""
Sales Analytics Dashboard for BuildSmartOS
Comprehensive business intelligence and reporting
"""
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

class AnalyticsDashboard:
    def __init__(self, db_name="buildsmart_hardware.db"):
        self.db_name = db_name
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def get_sales_summary(self, days=30):
        """Get sales summary for specified period"""
        try:
            conn = sqlite3.connect(self.db_name)
            
            # Today's sales
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COALESCE(SUM(total_amount), 0)
                FROM transactions
                WHERE DATE(date_time) = DATE('now')
            """)
            today_sales = cursor.fetchone()[0]
            
            # This month's sales
            cursor.execute("""
                SELECT COALESCE(SUM(total_amount), 0)
                FROM transactions
                WHERE strftime('%Y-%m', date_time) = strftime('%Y-%m', 'now')
            """)
            month_sales = cursor.fetchone()[0]
            
            # Period sales
            cursor.execute("""
                SELECT COALESCE(SUM(total_amount), 0), COUNT(*)
                FROM transactions
                WHERE DATE(date_time) >= DATE('now', '-' || ? || ' days')
            """, (days,))
            period_sales, transaction_count = cursor.fetchone()
            
            # Top selling products
            cursor.execute("""
                SELECT p.name, SUM(si.quantity_sold) as total_qty, SUM(si.sub_total) as revenue
                FROM sales_items si
                JOIN products p ON si.product_id = p.id
                JOIN transactions t ON si.transaction_id = t.id
                WHERE DATE(t.date_time) >= DATE('now', '-' || ? || ' days')
                GROUP BY p.id
                ORDER BY total_qty DESC
                LIMIT 10
            """, (days,))
            top_products = cursor.fetchall()
            
            # Low stock items
            cursor.execute("""
                SELECT name, stock_quantity, reorder_level
                FROM products
                WHERE stock_quantity <= reorder_level
                ORDER BY stock_quantity ASC
            """)
            low_stock = cursor.fetchall()
            
            conn.close()
            
            return {
                'today_sales': round(today_sales, 2),
                'month_sales': round(month_sales, 2),
                'period_sales': round(period_sales, 2),
                'transaction_count': transaction_count,
                'avg_transaction': round(period_sales / transaction_count, 2) if transaction_count > 0 else 0,
                'top_products': top_products,
                'low_stock_items': low_stock
            }
            
        except Exception as e:
            print(f"Analytics error: {e}")
            return None
    
    def generate_sales_chart(self, days=30):
        """Generate sales chart"""
        try:
            conn = sqlite3.connect(self.db_name)
            
            query = """
                SELECT DATE(date_time) as date, SUM(total_amount) as daily_sales
                FROM transactions
                WHERE DATE(date_time) >= DATE('now', '-' || ? || ' days')
                GROUP BY DATE(date_time)
                ORDER BY date
            """
            
            df = pd.read_sql_query(query, conn, params=(days,))
            conn.close()
            
            if df.empty:
                return None
            
            # Create chart
            plt.figure(figsize=(12, 6))
            plt.plot(df['date'], df['daily_sales'], marker='o', linewidth=2, markersize=6)
            plt.title(f'Sales Trend - Last {days} Days', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Sales (LKR)', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save chart
            chart_path = os.path.join(self.reports_dir, 'sales_trend.png')
            plt.savefig(chart_path, dpi=100)
            plt.close()
            
            return chart_path
            
        except Exception as e:
            print(f"Chart generation error: {e}")
            return None
    
    def generate_category_chart(self, days=30):
        """Generate sales by category pie chart"""
        try:
            conn = sqlite3.connect(self.db_name)
            
            query = """
                SELECT p.category, SUM(si.sub_total) as category_sales
                FROM sales_items si
                JOIN products p ON si.product_id = p.id
                JOIN transactions t ON si.transaction_id = t.id
                WHERE DATE(t.date_time) >= DATE('now', '-' || ? || ' days')
                  AND p.category IS NOT NULL
                GROUP BY p.category
                ORDER BY category_sales DESC
            """
            
            df = pd.read_sql_query(query, conn, params=(days,))
            conn.close()
            
            if df.empty:
                return None
            
            # Create pie chart
            plt.figure(figsize=(10, 8))
            plt.pie(df['category_sales'], labels=df['category'], autopct='%1.1f%%', startangle=90)
            plt.title(f'Sales by Category - Last {days} Days', fontsize=16, fontweight='bold')
            plt.axis('equal')
            plt.tight_layout()
            
            # Save chart
            chart_path = os.path.join(self.reports_dir, 'category_sales.png')
            plt.savefig(chart_path, dpi=100)
            plt.close()
            
            return chart_path
            
        except Exception as e:
            print(f"Category chart error: {e}")
            return None
    
    def get_profit_analysis(self, days=30):
        """Calculate profit margins"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Get products with profit margins
            cursor.execute("""
                SELECT 
                    p.name,
                    p.cost_price,
                    p.price_per_unit,
                    (p.price_per_unit - p.cost_price) as profit_per_unit,
                    CASE 
                        WHEN p.cost_price > 0 THEN 
                            ((p.price_per_unit - p.cost_price) / p.cost_price * 100)
                        ELSE 0
                    END as profit_margin_percent,
                    COALESCE(SUM(si.quantity_sold), 0) as units_sold,
                    COALESCE(SUM(si.sub_total), 0) as revenue
                FROM products p
                LEFT JOIN sales_items si ON p.id = si.product_id
                LEFT JOIN transactions t ON si.transaction_id = t.id 
                    AND DATE(t.date_time) >= DATE('now', '-' || ? || ' days')
                WHERE p.cost_price IS NOT NULL AND p.cost_price > 0
                GROUP BY p.id
                ORDER BY profit_margin_percent DESC
            """, (days,))
            
            products = cursor.fetchall()
            conn.close()
            
            return products
            
        except Exception as e:
            print(f"Profit analysis error: {e}")
            return []
    
    def generate_report(self, days=30):
        """Generate comprehensive PDF report"""
        try:
            summary = self.get_sales_summary(days)
            sales_chart = self.generate_sales_chart(days)
            category_chart = self.generate_category_chart(days)
            
            return {
                'summary': summary,
                'sales_chart': sales_chart,
                'category_chart': category_chart,
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            print(f"Report generation error: {e}")
            return None
    
    def get_hourly_sales_pattern(self):
        """Analyze sales patterns by hour"""
        try:
            conn = sqlite3.connect(self.db_name)
            
            query = """
                SELECT 
                    CAST(strftime('%H', date_time) AS INTEGER) as hour,
                    COUNT(*) as transaction_count,
                    SUM(total_amount) as total_sales
                FROM transactions
                WHERE DATE(date_time) >= DATE('now', '-30 days')
                GROUP BY hour
                ORDER BY hour
            """
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            return df.to_dict('records')
            
        except Exception as e:
            print(f"Hourly pattern error: {e}")
            return []

# Global instance
_analytics_dashboard = None

def get_analytics_dashboard():
    """Get or create analytics dashboard instance"""
    global _analytics_dashboard
    if _analytics_dashboard is None:
        _analytics_dashboard = AnalyticsDashboard()
    return _analytics_dashboard
