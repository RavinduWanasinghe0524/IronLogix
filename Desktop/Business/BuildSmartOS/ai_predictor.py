"""
AI-Powered Sales Predictor for BuildSmartOS
Uses machine learning to forecast sales and optimize inventory
"""
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pickle
import os

class AIPredictor:
    def __init__(self, db_name="buildsmart_hardware.db"):
        self.db_name = db_name
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = "models/sales_predictor.pkl"
        
        # Create models directory
        os.makedirs("models", exist_ok=True)
        
        # Load existing model if available
        self.load_model()
    
    def get_sales_data(self, days=90):
        """Get historical sales data"""
        try:
            conn = sqlite3.connect(self.db_name)
            
            query = """
                SELECT 
                    DATE(t.date_time) as date,
                    p.id as product_id,
                    p.name as product_name,
                    p.category,
                    SUM(si.quantity_sold) as quantity,
                    SUM(si.sub_total) as revenue
                FROM transactions t
                JOIN sales_items si ON t.id = si.transaction_id
                JOIN products p ON si.product_id = p.id
                WHERE DATE(t.date_time) >= DATE('now', '-' || ? || ' days')
                GROUP BY DATE(t.date_time), p.id
                ORDER BY date DESC
            """
            
            df = pd.read_sql_query(query, conn, params=(days,))
            conn.close()
            
            return df
            
        except Exception as e:
            print(f"Error fetching sales data: {e}")
            return pd.DataFrame()
    
    def prepare_features(self, df):
        """Prepare features for ML model"""
        if df.empty:
            return None, None
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Extract features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_month'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['week_of_year'] = df['date'].dt.isocalendar().week
        
        # Features and target
        feature_cols = ['day_of_week', 'day_of_month', 'month', 'week_of_year', 'product_id']
        X = df[feature_cols].values
        y = df['quantity'].values
        
        return X, y
    
    def train_model(self, days=90):
        """Train the sales prediction model"""
        try:
            df = self.get_sales_data(days)
            
            if df.empty or len(df) < 10:
                return False, "Insufficient data for training (need at least 10 sales records)"
            
            X, y = self.prepare_features(df)
            
            if X is None:
                return False, "Feature preparation failed"
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model = LinearRegression()
            self.model.fit(X_scaled, y)
            
            # Calculate accuracy
            score = self.model.score(X_scaled, y)
            
            # Save model
            self.save_model()
            
            return True, f"Model trained successfully (R² score: {score:.2f})"
            
        except Exception as e:
            return False, f"Training failed: {e}"
    
    def predict_sales(self, product_id, days_ahead=7):
        """Predict future sales for a product"""
        try:
            if self.model is None:
                # Try to train model
                success, msg = self.train_model()
                if not success:
                    return False, msg
            
            predictions = []
            today = datetime.now()
            
            for i in range(1, days_ahead + 1):
                future_date = today + timedelta(days=i)
                
                features = np.array([[
                    future_date.weekday(),
                    future_date.day,
                    future_date.month,
                    future_date.isocalendar()[1],
                    product_id
                ]])
                
                features_scaled = self.scaler.transform(features)
                predicted_qty = self.model.predict(features_scaled)[0]
                
                predictions.append({
                    'date': future_date.strftime('%Y-%m-%d'),
                    'predicted_quantity': max(0, round(predicted_qty, 2))
                })
            
            return True, predictions
            
        except Exception as e:
            return False, f"Prediction failed: {e}"
    
    def recommend_reorder(self, reorder_days=14):
        """Recommend products that need reordering"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Get all products with current stock
            cursor.execute("""
                SELECT id, name, stock_quantity, reorder_level
                FROM products
                WHERE stock_quantity > 0
            """)
            
            products = cursor.fetchall()
            conn.close()
            
            recommendations = []
            
            for product in products:
                p_id, name, current_stock, reorder_level = product
                
                # Predict sales for next reorder_days
                success, predictions = self.predict_sales(p_id, reorder_days)
                
                if success:
                    total_predicted = sum(p['predicted_quantity'] for p in predictions)
                    
                    # Check if stock will run low
                    if current_stock < total_predicted or current_stock <= reorder_level:
                        recommendations.append({
                            'product_id': p_id,
                            'product_name': name,
                            'current_stock': current_stock,
                            'predicted_demand': round(total_predicted, 2),
                            'recommended_order': max(reorder_level, round(total_predicted - current_stock + reorder_level, 2)),
                            'urgency': 'HIGH' if current_stock < reorder_level else 'MEDIUM'
                        })
            
            # Sort by urgency
            recommendations.sort(key=lambda x: (x['urgency'] == 'HIGH', -x['recommended_order']), reverse=True)
            
            return True, recommendations
            
        except Exception as e:
            return False, f"Recommendation failed: {e}"
    
    def analyze_trends(self, product_id=None):
        """Analyze sales trends"""
        try:
            df = self.get_sales_data(90)
            
            if df.empty:
                return False, "No sales data available"
            
            if product_id:
                df = df[df['product_id'] == product_id]
            
            # Calculate trends
            df['date'] = pd.to_datetime(df['date'])
            
            # Weekly aggregation
            weekly = df.groupby(df['date'].dt.to_period('W')).agg({
                'quantity': 'sum',
                'revenue': 'sum'
            }).reset_index()
            
            # Calculate trend
            if len(weekly) >= 2:
                recent_avg = weekly.tail(4)['quantity'].mean()
                older_avg = weekly.head(4)['quantity'].mean()
                
                if older_avg > 0:
                    trend_percent = ((recent_avg - older_avg) / older_avg) * 100
                else:
                    trend_percent = 0
                
                trend = 'INCREASING' if trend_percent > 5 else 'DECREASING' if trend_percent < -5 else 'STABLE'
            else:
                trend = 'INSUFFICIENT DATA'
                trend_percent = 0
            
            return True, {
                'trend': trend,
                'trend_percent': round(trend_percent, 2),
                'total_sales': df['quantity'].sum(),
                'total_revenue': df['revenue'].sum(),
                'average_daily': round(df.groupby('date')['quantity'].sum().mean(), 2)
            }
            
        except Exception as e:
            return False, f"Trend analysis failed: {e}"
    
    def save_model(self):
        """Save trained model to disk"""
        try:
            data = {
                'model': self.model,
                'scaler': self.scaler
            }
            with open(self.model_path, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"Model save failed: {e}")
    
    def load_model(self):
        """Load trained model from disk"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.model = data['model']
                    self.scaler = data['scaler']
                return True
        except Exception as e:
            print(f"Model load failed: {e}")
        return False

# Global instance
_ai_predictor = None

def get_ai_predictor():
    """Get or create AI predictor instance"""
    global _ai_predictor
    if _ai_predictor is None:
        _ai_predictor = AIPredictor()
    return _ai_predictor
