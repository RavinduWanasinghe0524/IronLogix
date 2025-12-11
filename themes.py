"""
Theme Manager for BuildSmartOS
Custom color themes and modern UI components
"""
import customtkinter as ctk

class ThemeManager:
    def __init__(self):
        # Color schemes
        self.themes = {
            "dark": {
                "primary": "#2CC985",      # Green accent
                "secondary": "#1F6AA5",    # Blue
                "background": "#1E1E1E",   # Dark bg
                "surface": "#2B2B2B",      # Card bg
                "surface_variant": "#3A3A3A",  # Lighter surface
                "text_primary": "#FFFFFF",
                "text_secondary": "#AAAAAA",
                "error": "#CF6679",
                "warning": "#FFA726",
                "success": "#2CC985"
            },
            "light": {
                "primary": "#1F6AA5",
                "secondary": "#2CC985",
                "background": "#F5F5F5",
                "surface": "#FFFFFF",
                "surface_variant": "#E0E0E0",
                "text_primary": "#212121",
                "text_secondary": "#757575",
                "error": "#B00020",
                "warning": "#F57C00",
                "success": "#4CAF50"
            }
        }
        
        self.current_theme = "dark"
        ctk.set_appearance_mode(self.current_theme.capitalize())
    
    def get_color(self, color_name):
        """Get color from current theme"""
        return self.themes[self.current_theme].get(color_name, "#000000")
    
    def switch_theme(self):
        """Toggle between light and dark themes"""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        ctk.set_appearance_mode(self.current_theme.capitalize())
        return self.current_theme
    
    def create_card_frame(self, parent, **kwargs):
        """Create a themed card frame"""
        return ctk.CTkFrame(
            parent,
            fg_color=self.get_color("surface_variant"),
            corner_radius=8,
            **kwargs
        )
    
    def create_primary_button(self, parent, text, command=None, **kwargs):
        """Create a themed primary button"""
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=self.get_color("primary"),
            hover_color=self.get_color("secondary"),
            corner_radius=6,
            font=("Arial", 14, "bold"),
            **kwargs
        )
    
    def create_icon_button(self, parent, text, command=None, **kwargs):
        """Create a small icon-style button"""
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=40,
            height=40,
            corner_radius=6,
            **kwargs
        )
    
    def create_label(self, parent, text, size=12, bold=False, **kwargs):
        """Create a themed label"""
        font_style = "bold" if bold else "normal"
        return ctk.CTkLabel(
            parent,
            text=text,
            font=("Arial", size, font_style),
            text_color=self.get_color("text_primary"),
            **kwargs
        )
    
    def create_entry(self, parent, placeholder="", **kwargs):
        """Create a themed entry field"""
        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            corner_radius=6,
            **kwargs
        )

# Global instance
_theme_manager = None

def get_theme_manager():
    """Get or create theme manager instance"""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
