"""
Barcode and QR Code Scanner for BuildSmartOS
Supports webcam scanning and image file scanning
"""
import cv2
from pyzbar import pyzbar
import threading
import queue

class BarcodeScanner:
    def __init__(self):
        self.is_scanning = False
        self.scan_queue = queue.Queue()
        self.camera = None
    
    def scan_from_camera(self, callback=None, camera_index=0):
        """Start continuous scanning from camera"""
        if self.is_scanning:
            return False, "Scanner already running"
        
        try:
            self.camera = cv2.VideoCapture(camera_index)
            self.is_scanning = True
            
            # Start scanning thread
            thread = threading.Thread(target=self._scan_loop, args=(callback,))
            thread.daemon = True
            thread.start()
            
            return True, "Scanner started"
            
        except Exception as e:
            return False, f"Camera access failed: {str(e)}"
    
    def _scan_loop(self, callback):
        """Main scanning loop"""
        while self.is_scanning:
            ret, frame = self.camera.read()
            
            if not ret:
                break
            
            # Decode barcodes
            barcodes = pyzbar.decode(frame)
            
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                barcode_type = barcode.type
                
                # Add to queue
                self.scan_queue.put({
                    'data': barcode_data,
                    'type': barcode_type
                })
                
                # Call callback if provided
                if callback:
                    callback(barcode_data, barcode_type)
                
                # Visual feedback
                cv2.rectangle(frame, (barcode.rect.left, barcode.rect.top),
                            (barcode.rect.left + barcode.rect.width, 
                             barcode.rect.top + barcode.rect.height),
                            (0, 255, 0), 2)
                
                # Display barcode data
                text = f"{barcode_type}: {barcode_data}"
                cv2.putText(frame, text, (barcode.rect.left, barcode.rect.top - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Display frame
            cv2.imshow('BuildSmart Barcode Scanner - Press Q to quit', frame)
            
            # Break on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.stop_scanning()
    
    def stop_scanning(self):
        """Stop camera scanning"""
        self.is_scanning = False
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
    
    def scan_image(self, image_path):
        """Scan barcode from image file"""
        try:
            image = cv2.imread(image_path)
            barcodes = pyzbar.decode(image)
            
            results = []
            for barcode in barcodes:
                results.append({
                    'data': barcode.data.decode('utf-8'),
                    'type': barcode.type
                })
            
            return True, results
            
        except Exception as e:
            return False, f"Image scan failed: {str(e)}"
    
    def get_scanned_code(self):
        """Get next scanned code from queue"""
        try:
            return self.scan_queue.get_nowait()
        except queue.Empty:
            return None
    
    def generate_qr_code(self, data, output_path="qr_code.png"):
        """Generate QR code for given data"""
        try:
            import qrcode
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(output_path)
            
            return True, output_path
            
        except Exception as e:
            return False, f"QR generation failed: {str(e)}"

# Global instance
_barcode_scanner = None

def get_barcode_scanner():
    """Get or create barcode scanner instance"""
    global _barcode_scanner
    if _barcode_scanner is None:
        _barcode_scanner = BarcodeScanner()
    return _barcode_scanner

# Quick scan function
def quick_scan_product(callback=None):
    """Quick function to scan a product barcode"""
    scanner = get_barcode_scanner()
    return scanner.scan_from_camera(callback)
