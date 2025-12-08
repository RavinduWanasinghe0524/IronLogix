from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_bill(transaction_id, cart_items, total_amount, date_time):
    """
    Generates a PDF bill for the transaction.
    cart_items: List of tuples (product_name, quantity, price, subtotal)
    """
    if not os.path.exists("bills"):
        os.makedirs("bills")

    filename = f"bills/bill_{transaction_id}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "BuildSmart Hardware Store")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, "123 Main Street, Ratnapura")
    c.drawString(50, height - 85, "Phone: 077-1234567")
    
    c.line(50, height - 100, width - 50, height - 100)

    # Bill Details
    c.drawString(50, height - 130, f"Bill No: {transaction_id}")
    c.drawString(400, height - 130, f"Date: {date_time}")

    # Table Header
    y = height - 170
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Item")
    c.drawString(250, y, "Qty")
    c.drawString(350, y, "Price")
    c.drawString(450, y, "Total")
    c.line(50, y - 5, width - 50, y - 5)

    # Items
    y -= 25
    c.setFont("Helvetica", 12)
    for item in cart_items:
        name = item['name']
        qty = item['qty']
        price = item['price']
        subtotal = item['subtotal']
        
        c.drawString(50, y, name[:25]) # Truncate long names
        c.drawString(250, y, str(qty))
        c.drawString(350, y, f"{price:.2f}")
        c.drawString(450, y, f"{subtotal:.2f}")
        y -= 20

    # Total
    c.line(50, y - 10, width - 50, y - 10)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(350, y - 40, "Grand Total:")
    c.drawString(450, y - 40, f"LKR {total_amount:.2f}")

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 50, "Thank you for your business!")
    c.drawString(50, 35, "Powered by BuildSmart OS")

    c.save()
    return filename
