"""
Terminal View
Terminal output view dengan scrolled text
"""

import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from src.config import COLORS


def create_terminal_view(parent):
    """
    Create terminal output view
    
    Args:
        parent: Parent container frame
        
    Returns:
        tuple: (view_frame, log_text_widget)
    """
    view = tk.Frame(parent, bg=COLORS["bg_dark"])
    
    log_container = tk.LabelFrame(
        view,
        text=" TERMINAL OUTPUT ",
        font=("Consolas", 10, "bold"),
        bg=COLORS["bg_dark"],
        fg=COLORS["text_secondary"],
        bd=1,
        relief="solid"
    )
    log_container.pack(fill="both", expand=True)
    
    log_text = scrolledtext.ScrolledText(
        log_container,
        wrap=tk.WORD,
        font=("Consolas", 10),
        bg=COLORS["terminal_bg"],
        fg=COLORS["text_primary"],
        bd=0,
        padx=10,
        pady=10,
        insertbackground="white"
    )
    log_text.pack(fill="both", expand=True)
    
    # Tag Colors
    log_text.tag_config("INFO", foreground=COLORS["text_primary"])
    log_text.tag_config("WARN", foreground="#FCD34D")
    log_text.tag_config("ERROR", foreground=COLORS["danger"])
    log_text.tag_config("SUCCESS", foreground=COLORS["success"])
    log_text.tag_config("HEADER", foreground=COLORS["accent"], font=("Consolas", 10, "bold"))
    
    return view, log_text


def log_message(log_text, message, tag="INFO"):
    """
    Helper function untuk logging
    
    Args:
        log_text: ScrolledText widget
        message: Message to log
        tag: Tag name for color coding
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"
    log_text.insert(tk.END, log_message, tag)
    log_text.see(tk.END)
    log_text.master.master.update_idletasks()
