"""
Premium Card Widget
Card component with elevation and premium styling
"""

import tkinter as tk
from src.config import COLORS, SPACING, BORDER


class PremiumCard(tk.Frame):
    """Premium card dengan elevation dan styling"""
    
    def __init__(self, parent, accent_color=COLORS["accent"], **kwargs):
        """
        Initialize premium card
        
        Args:
            parent: Parent widget
            accent_color: Color untuk accent bar
        """
        super().__init__(parent, **kwargs)
        
        self.config(
            bg=COLORS["card_bg"],
            relief=BORDER["radius_md"],
            bd=1,
            highlightthickness=0
        )
        
        # Accent bar di top
        self.accent_bar = tk.Frame(
            self,
            bg=accent_color,
            height=3
        )
        self.accent_bar.pack(fill="x")
        
        # Content container
        self.content = tk.Frame(
            self,
            bg=COLORS["card_bg"]
        )
        self.content.pack(fill="both", expand=True, padx=SPACING["lg"], pady=SPACING["md"])
    
    def add_title(self, text, icon=""):
        """Add title ke card"""
        title_text = f"{icon} {text}" if icon else text
        lbl = tk.Label(
            self.content,
            text=title_text,
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_primary"],
            anchor="w"
        )
        lbl.pack(fill="x", pady=(0, SPACING["sm"]))
        return lbl
    
    def add_body(self, text):
        """Add body text ke card"""
        lbl = tk.Label(
            self.content,
            text=text,
            font=("Segoe UI", 10),
            bg=COLORS["card_bg"],
            fg=COLORS["text_secondary"],
            anchor="w",
            justify="left"
        )
        lbl.pack(fill="x")
        return lbl
