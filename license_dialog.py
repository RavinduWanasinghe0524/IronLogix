"""
License Activation Dialog for BuildSmartOS
"""
import customtkinter as ctk
from tkinter import messagebox
from license_manager import get_license_manager

class LicenseDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("BuildSmartOS - License Activation")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self.license_manager = get_license_manager()
        self.activated = False
        
        self.create_ui()
        
        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def create_ui(self):
        """Create the license dialog UI"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="#1f538d", corner_radius=0)
        header_frame.pack(fill="x", pady=0)
        
        ctk.CTkLabel(
            header_frame,
            text="🔐 BuildSmartOS License",
            font=("Arial", 24, "bold"),
            text_color="white"
        ).pack(pady=20)
        
        # Content frame
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # License info
        info = self.license_manager.get_license_info()
        
        if info["activated"]:
            self.show_activated_info(content, info)
        else:
            self.show_trial_info(content, info)
    
    def show_trial_info(self, parent, info):
        """Show trial period information"""
        days_left = info["days_remaining"]
        
        # Trial status
        status_frame = ctk.CTkFrame(parent, fg_color="#2d2d2d", corner_radius=10)
        status_frame.pack(fill="x", pady=10)
        
        if days_left > 0:
            ctk.CTkLabel(
                status_frame,
                text=f"📅 Trial Period: {days_left} days remaining",
                font=("Arial", 16, "bold"),
                text_color="#4CAF50"
            ).pack(pady=15)
        else:
            ctk.CTkLabel(
                status_frame,
                text="⚠️ Trial Period Expired",
                font=("Arial", 16, "bold"),
                text_color="#f44336"
            ).pack(pady=15)
        
        # Machine ID
        ctk.CTkLabel(
            parent,
            text="Machine ID:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(15, 5))
        
        machine_frame = ctk.CTkFrame(parent, fg_color="#2d2d2d")
        machine_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            machine_frame,
            text=info["machine_id"],
            font=("Arial", 11),
            text_color="#888"
        ).pack(pady=10)
        
        # Activation code entry
        ctk.CTkLabel(
            parent,
            text="Enter Activation Code:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(15, 5))
        
        self.code_entry = ctk.CTkEntry(
            parent,
            placeholder_text="XXXX-XXXX-XXXX",
            height=40,
            font=("Arial", 14)
        )
        self.code_entry.pack(fill="x", pady=(0, 15))
        
        # Buttons
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=10)
        
        activate_btn = ctk.CTkButton(
            button_frame,
            text="Activate License",
            command=self.activate_license,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        activate_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        if days_left > 0:
            continue_btn = ctk.CTkButton(
                button_frame,
                text="Continue Trial",
                command=self.continue_trial,
                height=40,
                font=("Arial", 14),
                fg_color="#666",
                hover_color="#555"
            )
            continue_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        # Contact info
        ctk.CTkLabel(
            parent,
            text="For activation code, contact: support@buildsmart.lk",
            font=("Arial", 10),
            text_color="#888"
        ).pack(pady=10)
    
    def show_activated_info(self, parent, info):
        """Show activated license information"""
        # Status
        status_frame = ctk.CTkFrame(parent, fg_color="#2d2d2d", corner_radius=10)
        status_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            status_frame,
            text="✅ Licensed Version",
            font=("Arial", 18, "bold"),
            text_color="#4CAF50"
        ).pack(pady=20)
        
        # Info
        info_text = f"""
Machine ID: {info['machine_id']}

License Type: Full License
Activation Date: {info.get('activation_date', 'Unknown')[:10]}

Thank you for using BuildSmartOS!
        """
        
        ctk.CTkLabel(
            parent,
            text=info_text,
            font=("Arial", 12),
            justify="left"
        ).pack(pady=20)
        
        # Close button
        ctk.CTkButton(
            parent,
            text="Close",
            command=self.close_activated,
            height=40,
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        self.activated = True
    
    def activate_license(self):
        """Activate with entered code"""
        code = self.code_entry.get().strip()
        
        if not code:
            messagebox.showwarning("Missing Code", "Please enter an activation code")
            return
        
        success, message = self.license_manager.activate(code)
        
        if success:
            messagebox.showinfo("Success", message)
            self.activated = True
            self.destroy()
        else:
            messagebox.showerror("Activation Failed", message)
    
    def continue_trial(self):
        """Continue with trial"""
        self.activated = True
        self.destroy()
    
    def close_activated(self):
        """Close dialog for activated license"""
        self.activated = True
        self.destroy()

def show_license_dialog(parent):
    """Show license dialog and return if can continue"""
    dialog = LicenseDialog(parent)
    parent.wait_window(dialog)
    return dialog.activated
