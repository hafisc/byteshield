"""
Home View
Welcome/Dashboard view
"""

import tkinter as tk
from src.config import COLORS


def create_home_view(parent):
    """
    Create home/welcome view
    
    Args:
        parent: Parent container frame
        
    Returns:
        tk.Frame: Home view frame
    """
    view = tk.Frame(parent, bg=COLORS["bg_dark"])
    
    welcome = tk.Label(
        view,
        text="Select a tool from the sidebar to get started",
        font=("Segoe UI", 14),
        bg=COLORS["bg_dark"],
        fg=COLORS["text_secondary"]
    )
    welcome.pack(expand=True, pady=50)
    
    return view
