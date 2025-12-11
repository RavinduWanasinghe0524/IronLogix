"""
Construction Project Estimator for Sri Lankan Market
Calculate material costs for common construction projects
"""
import sqlite3
import json

class ConstructionEstimator:
    def __init__(self, db_name="buildsmart_hardware.db"):
        self.db_name = db_name
        
        # Standard material requirements per square foot for Sri Lankan construction
        self.material_templates = {
            "basic_house": {
                "name": "Basic House (Ground Floor)",
                "materials_per_sqft": {
                    "cement_bags": 0.4,  # Tokyo cement bags
                    "sand_cubes": 0.04,  # River sand
                    "metal_kg": 4.0,     # Steel bars
                    "bricks": 8.0,       # Clay bricks
                    "tiles_sqft": 1.1,   # Floor tiles (10% wastage)
                },
                "labor_cost_per_sqft": 1500  # LKR
            },
            "two_story_house": {
                "name": "Two Story House",
                "materials_per_sqft": {
                    "cement_bags": 0.5,
                    "sand_cubes": 0.05,
                    "metal_kg": 5.5,
                    "bricks": 10.0,
                    "tiles_sqft": 1.1,
                },
                "labor_cost_per_sqft": 1800
            },
            "boundary_wall": {
                "name": "Boundary Wall (per running foot, 6ft height)",
                "materials_per_sqft": {
                    "cement_bags": 0.3,
                    "sand_cubes": 0.03,
                    "bricks": 12.0,
                    "metal_kg": 1.5,
                },
                "labor_cost_per_sqft": 800
            },
            "roofing": {
                "name": "Roofing (Asbestos/Metal sheets)",
                "materials_per_sqft": {
                    "roofing_sheets": 1.15,  # 15% wastage
                    "metal_kg": 0.5,          # Support structure
                    "cement_bags": 0.1,
                },
                "labor_cost_per_sqft": 500
            }
        }
    
    def get_product_price(self, search_term):
        """Get product price from database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, price_per_unit, unit_type
                FROM products
                WHERE LOWER(name) LIKE LOWER(?)
                LIMIT 1
            """, (f"%{search_term}%",))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return result
            return None
            
        except Exception as e:
            print(f"Error fetching price: {e}")
            return None
    
    def estimate_project(self, project_type, area_sqft, include_labor=True):
        """Estimate costs for a construction project"""
        try:
            if project_type not in self.material_templates:
                return False, f"Unknown project type. Available: {list(self.material_templates.keys())}"
            
            template = self.material_templates[project_type]
            materials_needed = {}
            material_costs = {}
            total_material_cost = 0
            
            # Calculate material quantities
            for material, qty_per_sqft in template["materials_per_sqft"].items():
                total_qty = qty_per_sqft * area_sqft
                materials_needed[material] = round(total_qty, 2)
                
                # Try to get price from database
                price_info = self.get_product_price(material.replace('_', ' '))
                
                if price_info:
                    name, price, unit = price_info
                    cost = total_qty * price
                    material_costs[material] = {
                        'quantity': round(total_qty, 2),
                        'unit_price': price,
                        'unit_type': unit,
                        'total_cost': round(cost, 2),
                        'product_name': name
                    }
                    total_material_cost += cost
                else:
                    # Use estimated prices if not in database
                    estimated_prices = {
                        'cement_bags': 2300,
                        'sand_cubes': 18000,
                        'metal_kg': 250,
                        'bricks': 25,
                        'tiles_sqft': 150,
                        'roofing_sheets': 1200
                    }
                    est_price = estimated_prices.get(material, 0)
                    cost = total_qty * est_price
                    material_costs[material] = {
                        'quantity': round(total_qty, 2),
                        'unit_price': est_price,
                        'unit_type': 'unit',
                        'total_cost': round(cost, 2),
                        'product_name': material.replace('_', ' ').title(),
                        'estimated': True
                    }
                    total_material_cost += cost
            
            # Calculate labor cost
            labor_cost = 0
            if include_labor:
                labor_cost = template["labor_cost_per_sqft"] * area_sqft
            
            # Calculate totals
            subtotal = total_material_cost + labor_cost
            contingency = subtotal * 0.10  # 10% contingency
            grand_total = subtotal + contingency
            
            return True, {
                'project_name': template['name'],
                'area_sqft': area_sqft,
                'materials': material_costs,
                'material_cost': round(total_material_cost, 2),
                'labor_cost': round(labor_cost, 2),
                'subtotal': round(subtotal, 2),
                'contingency': round(contingency, 2),
                'grand_total': round(grand_total, 2),
                'cost_per_sqft': round(grand_total / area_sqft, 2)
            }
            
        except Exception as e:
            return False, f"Estimation failed: {e}"
    
    def get_project_types(self):
        """Get available project types"""
        return [(key, template['name']) for key, template in self.material_templates.items()]
    
    def estimate_custom(self, materials_dict):
        """
        Estimate cost for custom material list
        materials_dict format: {'product_name': quantity, ...}
        """
        try:
            total_cost = 0
            breakdown = {}
            
            for product_name, quantity in materials_dict.items():
                price_info = self.get_product_price(product_name)
                
                if price_info:
                    name, price, unit = price_info
                    cost = quantity * price
                    breakdown[product_name] = {
                        'quantity': quantity,
                        'unit_price': price,
                        'unit_type': unit,
                        'total_cost': round(cost, 2),
                        'product_name': name
                    }
                    total_cost += cost
                else:
                    breakdown[product_name] = {
                        'error': 'Product not found in database'
                    }
            
            return True, {
                'materials': breakdown,
                'total_cost': round(total_cost, 2)
            }
            
        except Exception as e:
            return False, f"Custom estimation failed: {e}"

# Global instance
_construction_estimator = None

def get_construction_estimator():
    """Get or create construction estimator instance"""
    global _construction_estimator
    if _construction_estimator is None:
        _construction_estimator = ConstructionEstimator()
    return _construction_estimator
