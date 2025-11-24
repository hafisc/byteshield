"""
Scan View
Halaman untuk virus scanning
"""

import tkinter as tk
from tkinter import ttk
from src.config import COLORS


def create_scan_view(parent, start_callback):
    """
    Create virus scan view
    
    Args:
        parent: Parent container frame
        start_callback: Callback function saat tombol Start diklik
        
    Returns:
        tk.Frame: Scan view frame
    """
    view = tk.Frame(parent, bg=COLORS["bg_dark"])
    
    canvas = tk.Canvas(view, bg=COLORS["bg_dark"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(view, orient="vertical", command=canvas.yview)
    content = tk.Frame(canvas, bg=COLORS["bg_dark"])
    
    content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=content, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    tk.Label(content, text="🔍 Virus Quick Scan", font=("Segoe UI", 20, "bold"), bg=COLORS["bg_dark"], fg="white", anchor="w").pack(fill="x", pady=(0, 10))
    tk.Label(content, text="Quick security scan using Windows Defender", font=("Segoe UI", 11), bg=COLORS["bg_dark"], fg=COLORS["text_secondary"], anchor="w").pack(fill="x", pady=(0, 20))
    
    # Info card
    info_card = tk.Frame(content, bg=COLORS["card_bg"], bd=1, relief="solid")
    info_card.pack(fill="x", pady=(0, 20))
    tk.Frame(info_card, bg=COLORS["accent"], height=3).pack(fill="x")
    
    info_content = tk.Frame(info_card, bg=COLORS["card_bg"])
    info_content.pack(fill="x", padx=15, pady=15)
    tk.Label(info_content, text="ℹ️ Scan Information", font=("Segoe UI", 12, "bold"), bg=COLORS["card_bg"], fg="white", anchor="w").pack(fill="x")
    
    info_items = [
        ("Engine:", "Windows Defender"),
        ("Scan Type:", "Quick Scan"),
        ("Target:", "System memory + Startup files"),
        ("Estimated Time:", "2-5 minutes")
    ]
    
    for label, value in info_items:
        row = tk.Frame(info_content, bg=COLORS["card_bg"])
        row.pack(fill="x", pady=3)
        tk.Label(row, text=label, font=("Segoe UI", 10, "bold"), bg=COLORS["card_bg"], fg=COLORS["text_secondary"], anchor="w", width=15).pack(side="left")
        tk.Label(row, text=value, font=("Segoe UI", 10), bg=COLORS["card_bg"], fg="white", anchor="w").pack(side="left")
    
    # Note
    note_card = tk.Frame(content, bg=COLORS["card_bg"], bd=1, relief="solid")
    note_card.pack(fill="x", pady=(0, 20))
    tk.Frame(note_card, bg="#FCD34D", height=3).pack(fill="x")
    
    note_content = tk.Frame(note_card, bg=COLORS["card_bg"])
    note_content.pack(fill="x", padx=15, pady=15)
    tk.Label(note_content, text="💡 Note", font=("Segoe UI", 11, "bold"), bg=COLORS["card_bg"], fg="#FCD34D", anchor="w").pack(fill="x")
    tk.Label(note_content, text="Administrator privileges may be required for complete scan", font=("Segoe UI", 9), bg=COLORS["card_bg"], fg=COLORS["text_primary"], anchor="w").pack(fill="x", pady=(5, 0))
    
    tk.Button(content, text="🚀 Start Scanning", font=("Segoe UI", 14, "bold"), bg=COLORS["success"], fg="white", activebackground=COLORS["accent"], activeforeground="white", relief="flat", bd=0, padx=30, pady=15, cursor="hand2", command=start_callback).pack(fill="x", pady=10)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return view
