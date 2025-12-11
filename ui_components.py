"""
Reusable UI components for BuildSmartOS.
Modern, consistent UI elements built with CustomTkinter.
"""

import customtkinter as ctk
from tkinter import messagebox
import time
from threading import Thread


class ModernButton(ctk.CTkButton):
    """Enhanced button with hover effects and loading state."""
    
    def __init__(self, master, **kwargs):
        # Extract custom parameters
        self.icon = kwargs.pop('icon', None)
        self.loading_text = kwargs.pop('loading_text', 'Loading...')
        
        super().__init__(master, **kwargs)
        self.original_text = self.cget("text")
        self.is_loading = False
        
    def set_loading(self, loading=True):
        """Set button to loading state."""
        self.is_loading = loading
        if loading:
            self.configure(text=self.loading_text, state="disabled")
        else:
            self.configure(text=self.original_text, state="normal")


class ToastNotification:
    """Toast notification system for user feedback."""
    
    @staticmethod
    def show(parent, message, duration=3000, type="info"):
        """
        Show a toast notification.
        
        Args:
            parent: Parent window
            message: Message to display
            duration: Duration in milliseconds
            type: info, success, warning, error
        """
        # Color schemes
        colors = {
            "info": ("#3498db", "#ffffff"),
            "success": ("#2ecc71", "#ffffff"),
            "warning": ("#f39c12", "#ffffff"),
            "error": ("#e74c3c", "#ffffff")
        }
        
        bg_color, text_color = colors.get(type, colors["info"])
        
        # Create toast frame
        toast = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=8
        )
        
        # Icon based on type
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        icon = icons.get(type, "ℹ️")
        
        # Message label
        label = ctk.CTkLabel(
            toast,
            text=f"{icon} {message}",
            text_color=text_color,
            font=("Arial", 12, "bold")
        )
        label.pack(padx=20, pady=10)
        
        # Position at top center
        toast.place(relx=0.5, rely=0.05, anchor="n")
        
        # Auto-hide after duration
        def hide_toast():
            time.sleep(duration / 1000)
            try:
                toast.place_forget()
                toast.destroy()
            except:
                pass
        
        Thread(target=hide_toast, daemon=True).start()
        
        return toast


class LoadingSpinner:
    """Loading indicator widget."""
    
    def __init__(self, parent, message="Loading..."):
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        # Semi-transparent overlay
        self.overlay = ctk.CTkFrame(
            parent,
            fg_color=("gray85", "gray15"),
            corner_radius=10
        )
        
        # Loading message
        self.label = ctk.CTkLabel(
            self.overlay,
            text=f"⏳ {message}",
            font=("Arial", 14, "bold")
        )
        self.label.pack(padx=40, pady=30)
        
    def show(self):
        """Show loading indicator."""
        self.overlay.place(relx=0.5, rely=0.5, anchor="center")
        
    def hide(self):
        """Hide loading indicator."""
        try:
            self.overlay.place_forget()
        except:
            pass


class ConfirmDialog:
    """Confirmation dialog with custom styling."""
    
    @staticmethod
    def ask(title, message, icon="question"):
        """
        Show confirmation dialog.
        
        Returns:
            True if user confirms, False otherwise
        """
        return messagebox.askyesno(title, message, icon=icon)
    
    @staticmethod
    def show_info(title, message):
        """Show info message."""
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_warning(title, message):
        """Show warning message."""
        messagebox.showwarning(title, message)
    
    @staticmethod
    def show_error(title, message):
        """Show error message."""
        messagebox.showerror(title, message)


class ValidatedEntry(ctk.CTkEntry):
    """Entry widget with built-in validation indicator."""
    
    def __init__(self, master, validation_func=None, **kwargs):
        super().__init__(master, **kwargs)
        self.validation_func = validation_func
        self.is_valid = True
        
        if validation_func:
            self.bind("<FocusOut>", self.validate)
            self.bind("<KeyRelease>", self.on_key_release)
    
    def on_key_release(self, event):
        """Clear validation styling on key release."""
        self.configure(border_color=("gray60", "gray40"))
    
    def validate(self, event=None):
        """Validate input and show visual feedback."""
        if not self.validation_func:
            return True
        
        value = self.get()
        is_valid, result = self.validation_func(value)
        
        if is_valid:
            self.configure(border_color="green")
            self.is_valid = True
            return True
        else:
            self.configure(border_color="red")
            self.is_valid = False
            if isinstance(result, str):
                # Show error tooltip
                ToastNotification.show(self.master, result, type="error", duration=2000)
            return False
    
    def get_validated_value(self):
        """Get value if valid, None otherwise."""
        if self.validate():
            return self.get()
        return None


class StatusBar(ctk.CTkFrame):
    """Bottom status bar showing connection status, time, and user info."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, height=30, **kwargs)
        
        # Database status
        self.db_status = ctk.CTkLabel(
            self,
            text="🔌 Database: Connected",
            font=("Arial", 10)
        )
        self.db_status.pack(side="left", padx=10)
        
        # Separator
        sep1 = ctk.CTkLabel(self, text="|", font=("Arial", 10))
        sep1.pack(side="left", padx=5)
        
        # User info
        self.user_label = ctk.CTkLabel(
            self,
            text="👤 User: Admin",
            font=("Arial", 10)
        )
        self.user_label.pack(side="left", padx=5)
        
        # Separator
        sep2 = ctk.CTkLabel(self, text="|", font=("Arial", 10))
        sep2.pack(side="left", padx=5)
        
        # Time display
        self.time_label = ctk.CTkLabel(
            self,
            text="🕐 --:--:--",
            font=("Arial", 10)
        )
        self.time_label.pack(side="right", padx=10)
        
        # Start time update
        self.update_time()
    
    def update_time(self):
        """Update time display."""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"🕐 {current_time}")
        self.after(1000, self.update_time)
    
    def set_database_status(self, connected=True):
        """Update database connection status."""
        if connected:
            self.db_status.configure(
                text="🔌 Database: Connected",
                text_color="green"
            )
        else:
            self.db_status.configure(
                text="⚠️ Database: Disconnected",
                text_color="red"
            )
    
    def set_user(self, username):
        """Update user display."""
        self.user_label.configure(text=f"👤 User: {username}")


class SearchBar(ctk.CTkFrame):
    """Enhanced search bar with clear button."""
    
    def __init__(self, master, search_callback=None, placeholder="Search...", **kwargs):
        super().__init__(master, **kwargs)
        
        self.search_callback = search_callback
        
        # Search icon
        icon_label = ctk.CTkLabel(self, text="🔍", font=("Arial", 14))
        icon_label.pack(side="left", padx=(5, 0))
        
        # Search entry
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            width=300
        )
        self.entry.pack(side="left", padx=5, fill="x", expand=True)
        self.entry.bind("<KeyRelease>", self.on_search)
        
        # Clear button
        self.clear_btn = ctk.CTkButton(
            self,
            text="✖",
            width=30,
            command=self.clear_search
        )
        self.clear_btn.pack(side="left", padx=(0, 5))
        self.clear_btn.pack_forget()  # Hide initially
    
    def on_search(self, event=None):
        """Handle search event."""
        search_term = self.entry.get()
        
        if search_term:
            self.clear_btn.pack(side="left", padx=(0, 5))
        else:
            self.clear_btn.pack_forget()
        
        if self.search_callback:
            self.search_callback(search_term)
    
    def clear_search(self):
        """Clear search field."""
        self.entry.delete(0, "end")
        self.clear_btn.pack_forget()
        if self.search_callback:
            self.search_callback("")
    
    def get(self):
        """Get search term."""
        return self.entry.get()


class ProgressBar(ctk.CTkFrame):
    """Animated progress bar."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, height=20, **kwargs)
        
        self.progress = ctk.CTkProgressBar(self, width=300)
        self.progress.pack(pady=5, padx=10, fill="x", expand=True)
        self.progress.set(0)
        
        self.label = ctk.CTkLabel(self, text="0%", font=("Arial", 10))
        self.label.pack()
    
    def set(self, value):
        """Set progress value (0-1)."""
        self.progress.set(value)
        self.label.configure(text=f"{int(value * 100)}%")
    
    def start(self):
        """Start indeterminate progress."""
        self.progress.start()
        self.label.configure(text="Loading...")
    
    def stop(self):
        """Stop indeterminate progress."""
        self.progress.stop()
        self.set(1.0)


class IconButton(ctk.CTkButton):
    """Button with icon and tooltip."""
    
    def __init__(self, master, icon, tooltip="", **kwargs):
        super().__init__(master, text=icon, width=40, **kwargs)
        self.tooltip = tooltip
        
        if tooltip:
            self.bind("<Enter>", self.show_tooltip)
            self.bind("<Leave>", self.hide_tooltip)
        
        self.tooltip_window = None
    
    def show_tooltip(self, event=None):
        """Show tooltip on hover."""
        if not self.tooltip:
            return
        
        x = self.winfo_rootx() + 25
        y = self.winfo_rooty() + 25
        
        self.tooltip_window = ctk.CTkToplevel(self)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        label = ctk.CTkLabel(
            self.tooltip_window,
            text=self.tooltip,
            font=("Arial", 10)
        )
        label.pack(padx=5, pady=2)
    
    def hide_tooltip(self, event=None):
        """Hide tooltip."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


# Utility function to create card-style frames
def create_card(parent, title=None, **kwargs):
    """Create a card-style frame with optional title."""
    card = ctk.CTkFrame(parent, corner_radius=10, **kwargs)
    
    if title:
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(10, 5), padx=10, anchor="w")
    
    return card
