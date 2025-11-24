"""
System Info View
Halaman untuk menampilkan informasi sistem
"""

import tkinter as tk
from tkinter import ttk
from src.config import COLORS


def create_sysinfo_view(parent):
    """
    Create system information view
    
    Args:
        parent: Parent container frame
        
    Returns:
        tuple: (view_frame, info_cards_container, placeholder_label)
    """
    view = tk.Frame(parent, bg=COLORS["bg_dark"])
    
    tk.Label(view, text="💻 System Information", font=("Segoe UI", 20, "bold"), bg=COLORS["bg_dark"], fg="white", anchor="w").pack(fill="x", pady=(0, 20))
    
    canvas = tk.Canvas(view, bg=COLORS["bg_dark"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(view, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLORS["bg_dark"])
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    placeholder = tk.Label(scrollable_frame, text="⏳ Scanning system...", font=("Segoe UI", 14), bg=COLORS["bg_dark"], fg=COLORS["text_secondary"])
    placeholder.pack(expand=True, pady=100)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return view, scrollable_frame, placeholder


def update_sysinfo_display(container, placeholder, system_info):
    """
    Update system info display dengan data
    
    Args:
        container: Container frame untuk info cards
        placeholder: Placeholder label (akan dihapus)
        system_info: Dict with system information
    """
    if placeholder:
        placeholder.destroy()
    
    for widget in container.winfo_children():
        widget.destroy()
    
    info_items = [
        ("🖥️ Operating System", system_info.get('os', 'Unknown'), COLORS["accent"]),
        ("⚙️ Processor", system_info.get('cpu', 'Unknown'), COLORS["success"]),
        ("💾 Memory (RAM)", system_info.get('ram', 'Unknown'), COLORS["danger"]),
        ("💿 Storage (C:)", system_info.get('disk', 'Unknown'), "#A78BFA"),
    ]
    
    for icon_title, value, color in info_items:
        card = tk.Frame(container, bg=COLORS["sidebar"], bd=0, relief="solid")
        card.pack(fill="x", pady=10)
        
        tk.Frame(card, bg=color, width=5).pack(side="left", fill="y")
        
        content = tk.Frame(card, bg=COLORS["sidebar"])
        content.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        tk.Label(content, text=icon_title, font=("Segoe UI", 12, "bold"), bg=COLORS["sidebar"], fg=COLORS["text_secondary"], anchor="w").pack(fill="x")
        tk.Label(content, text=value, font=("Segoe UI", 14), bg=COLORS["sidebar"], fg="white", anchor="w").pack(fill="x", pady=(5, 0))
