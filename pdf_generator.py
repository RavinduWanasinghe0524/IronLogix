from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import json
from datetime import datetime

def load_config():
    """Load configuration"""
    try:
        with open("config.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def generate_bill(transaction_id, cart_items, total_amount, date_time, customer_name=None, discount=0, language='english'):
    """
    Generates a professional PDF bill for the transaction.
    cart_items: List of dicts with name, qty, price, subtotal
    """
    if not os.path.exists("bills"):
        os.makedirs("bills")

    config = load_config()
    business = config.get('business', {})

    filename = f"bills/bill_{transaction_id}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Colors
    primary_color = (44/255, 201/255, 133/255)  # Green
    dark_gray = (0.2, 0.2, 0.2)

    # Header Box
    c.setFillColorRGB(*primary_color)
    c.rect(0, height - 120, width, 120, fill=1, stroke=0)
    
    c.setFillColorRGB(1, 1, 1)  # White text
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, business.get('name', 'BuildSmart Hardware Store'))
    
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 70, business.get('address', '123 Main Street, Ratnapura'))
    c.drawString(50, height - 85, f"Phone: {business.get('phone', '077-1234567')}")
    if business.get('email'):
        c.drawString(50, height - 100, f"Email: {business.get('email')}")
    
    # Invoice Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(width - 180, height - 60, "INVOICE")

    # Reset to black
    c.setFillColorRGB(*dark_gray)

    # Bill Details Section
    y = height - 150
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, f"Invoice No:")
    c.setFont("Helvetica", 11)
    c.drawString(150, y, f"#{transaction_id}")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(width - 250, y, f"Date:")
    c.setFont("Helvetica", 11)
    c.drawString(width - 200, y, date_time)
    
    y -= 20
    if customer_name:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, f"Customer:")
        c.setFont("Helvetica", 11)
        c.drawString(150, y, customer_name)
        y -= 10

    y -= 30
    c.setStrokeColorRGB(*dark_gray)
    c.line(50, y, width - 50, y)

    # Table Header
    y -= 25
    c.setFillColorRGB(*primary_color)
    c.rect(50, y - 5, width - 100, 25, fill=1, stroke=0)
    
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(60, y + 5, "Item")
    c.drawString(320, y + 5, "Quantity")
    c.drawString(420, y + 5, "Price")
    c.drawString(500, y + 5, "Total")

    # Items
    y -= 30
    c.setFillColorRGB(*dark_gray)
    c.setFont("Helvetica", 10)
    
    for i, item in enumerate(cart_items):
        # Alternate row colors
        if i % 2 == 0:
            c.setFillColorRGB(0.97, 0.97, 0.97)
            c.rect(50, y - 3, width - 100, 18, fill=1, stroke=0)
        
        c.setFillColorRGB(*dark_gray)
        name = item['name'][:35]  # Truncate long names
        qty = item['qty']
        price = item['price']
        subtotal = item['subtotal']
        
        c.drawString(60, y, name)
        c.drawString(330, y, str(qty))
        c.drawString(420, y, f"LKR {price:.2f}")
        c.drawString(500, y, f"LKR {subtotal:.2f}")
        y -= 20

    # Totals Box
    y -= 20
    c.setStrokeColorRGB(*dark_gray)
    c.line(360, y, width - 50, y)
    
    y -= 25
    c.setFont("Helvetica", 11)
    c.drawString(380, y, "Subtotal:")
    c.drawString(500, y, f"LKR {total_amount + discount:.2f}")
    
    if discount > 0:
        y -= 20
        c.drawString(380, y, "Discount:")
        c.setFillColorRGB(0.8, 0, 0)
        c.drawString(500, y, f"- LKR {discount:.2f}")
        c.setFillColorRGB(*dark_gray)
    
    y -= 20
    c.line(360, y + 5, width - 50, y + 5)
    
    y -= 25
    c.setFont("Helvetica-Bold", 14)
    c.drawString(380, y, "Grand Total:")
    c.setFillColorRGB(*primary_color)
    c.drawString(500, y, f"LKR {total_amount:.2f}")

    # Footer
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(width/2, 60, "Thank you for your business!")
    c.drawCentredString(width/2, 45, "Powered by BuildSmart OS - Sri Lanka's Smart Hardware POS")
    c.drawCentredString(width/2, 30, "For support: info@buildsmart.lk")

    c.save()
    return filename

def generate_quotation(quote_id, items, total_amount, customer_name, valid_until):
    """Generate a quotation PDF"""
    if not os.path.exists("quotations"):
        os.makedirs("quotations")
    
    filename = f"quotations/quote_{quote_id}.pdf"
    # Similar structure to bill but with "QUOTATION" title
    # Implementation can be added based on need
    return filename
