from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import os
import json
from datetime import datetime
import io

try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False
    print("⚠️  qrcode not available - install with 'pip install qrcode[pil]' for QR code support")

def load_config():
    """Load configuration"""
    try:
        with open("config.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def generate_qr_code(data):
    """Generate QR code image in memory."""
    if not QR_AVAILABLE:
        return None
    
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to ImageReader for reportlab
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        return ImageReader(img_buffer)
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None

def generate_bill(transaction_id, cart_items, total_amount, date_time, customer_name=None, 
                  discount=0, language='english', payment_method='Cash'):
    """
    Generates a professional PDF bill with QR code verification.
    
    Args:
        transaction_id: Transaction ID
        cart_items: List of dicts with name, qty, price, subtotal
        total_amount: Final total amount after discount
        date_time: Transaction date/time
        customer_name: Customer name (optional)
        discount: Discount amount
        language: Invoice language
        payment_method: Payment method used
    
    Returns:
        str: Path to generated PDF file
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
    light_gray = (0.95, 0.95, 0.95)

    # Header Box with gradient effect
    c.setFillColorRGB(*primary_color)
    c.rect(0, height - 130, width, 130, fill=1, stroke=0)
    
    c.setFillColorRGB(1, 1, 1)  # White text
    c.setFont("Helvetica-Bold", 26)
    c.drawString(50, height - 50, business.get('name', 'BuildSmart Hardware Store'))
    
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 75, business.get('address', '123 Main Street, Ratnapura'))
    c.drawString(50, height - 92, f"📞 {business.get('phone', '077-1234567')}")
    if business.get('email'):
        c.drawString(50, height - 109, f"📧 {business.get('email')}")
    
    # Invoice Title with box
    inv_box_x = width - 200
    c.setFillColorRGB(1, 1, 1)
    c.roundRect(inv_box_x, height - 100, 150, 40, 5, fill=1, stroke=0)
    c.setFillColorRGB(*primary_color)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(inv_box_x + 75, height - 75, "INVOICE")

    # Reset to black
    c.setFillColorRGB(*dark_gray)

    # QR Code for verification (if available)
    if QR_AVAILABLE:
        qr_data = f"BuildSmart-{transaction_id}-{date_time}-{total_amount}"
        qr_image = generate_qr_code(qr_data)
        if qr_image:
            qr_size = 80
            c.drawImage(qr_image, width - 130, height - 240, qr_size, qr_size)
            c.setFont("Helvetica", 8)
            c.drawCentredString(width - 90, height - 250, "Scan to verify")

    # Bill Details Section
    y = height - 165
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, f"Invoice No:")
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(*primary_color)
    c.drawString(150, y, f"#{str(transaction_id).zfill(6)}")
    c.setFillColorRGB(*dark_gray)
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(320, y, f"Date:")
    c.setFont("Helvetica", 11)
    c.drawString(370, y, date_time)
    
    y -= 22
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, f"Payment Method:")
    c.setFont("Helvetica", 11)
    c.drawString(180, y, payment_method)
    
    if customer_name:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(320, y, f"Customer:")
        c.setFont("Helvetica", 11)
        c.drawString(400, y, str(customer_name)[:25])

    y -= 35
    c.setStrokeColorRGB(*dark_gray)
    c.setLineWidth(2)
    c.line(50, y, width - 50, y)
    c.setLineWidth(1)

    # Table Header with enhanced styling
    y -= 30
    c.setFillColorRGB(*primary_color)
    c.roundRect(50, y - 5, width - 100, 25, 3, fill=1, stroke=0)
    
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(60, y + 5, "Item Description")
    c.drawString(320, y + 5, "Qty")
    c.drawString(400, y + 5, "Unit Price")
    c.drawString(500, y + 5, "Total")

    # Items with alternating colors
    y -= 30
    c.setFont("Helvetica", 10)
    
    for i, item in enumerate(cart_items):
        # Alternate row colors
        if i % 2 == 0:
            c.setFillColorRGB(*light_gray)
            c.roundRect(50, y - 5, width - 100, 20, 2, fill=1, stroke=0)
        
        c.setFillColorRGB(*dark_gray)
        name = str(item.get('name', ''))[:40]  # Truncate long names
        qty = item.get('qty', 0)
        price = item.get('price', 0)
        subtotal = item.get('subtotal', 0)
        
        c.drawString(60, y, name)
        c.drawString(330, y, str(qty))
        c.drawString(405, y, f"LKR {price:,.2f}")
        c.drawString(505, y, f"LKR {subtotal:,.2f}")
        y -= 22

    # Totals Box with enhanced styling
    y -= 25
    c.setStrokeColorRGB(*dark_gray)
    c.setLineWidth(1)
    c.line(350, y, width - 50, y)
    
    y -= 25
    c.setFont("Helvetica", 11)
    c.drawString(370, y, "Subtotal:")
    c.drawRightString(width - 60, y, f"LKR {(total_amount + discount):,.2f}")
    
    if discount > 0:
        y -= 22
        c.drawString(370, y, "Discount:")
        c.setFillColorRGB(0.8, 0.1, 0.1)
        c.drawRightString(width - 60, y, f"- LKR {discount:,.2f}")
        c.setFillColorRGB(*dark_gray)
    
    y -= 5
    c.setLineWidth(2)
    c.line(350, y, width - 50, y)
    
    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(370, y, "GRAND TOTAL:")
    c.setFillColorRGB(*primary_color)
    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(width - 60, y, f"LKR {total_amount:,.2f}")
    c.setFillColorRGB(*dark_gray)

    # Terms & Conditions Box
    y -= 50
    if y > 150:  # Only if there's space
        c.setFont("Helvetica-Bold", 9)
        c.drawString(50, y, "Terms & Conditions:")
        c.setFont("Helvetica", 8)
        y -= 15
        c.drawString(50, y, "• All sales are final unless product is defective")
        y -= 12
        c.drawString(50, y, "• Returns accepted within 7 days with original receipt")
        y -= 12
        c.drawString(50, y, "• Warranty terms as per manufacturer")

    # Footer with branding
    footer_y = 80
    c.setFillColorRGB(*primary_color)
    c.rect(0, 0, width, 70, fill=1, stroke=0)
    
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, footer_y - 20, "Thank You for Your Business!")
    c.setFont("Helvetica", 9)
    c.drawCentredString(width/2, footer_y - 35, "Powered by BuildSmart OS - Sri Lanka's Smart Hardware POS")
    c.drawCentredString(width/2, footer_y - 48, "For support: info@buildsmart.lk | +94 77 123 4567")

    c.save()
    print(f"✅ Invoice #{transaction_id} generated: {filename}")
    return filename

def generate_quotation(quote_id, items, total_amount, customer_name, valid_until):
    """Generate a quotation PDF"""
    if not os.path.exists("quotations"):
        os.makedirs("quotations")
    
    filename = f"quotations/quote_{quote_id}.pdf"
    # Similar structure to bill but with "QUOTATION" title
    # Implementation can be added based on need
    return filename
