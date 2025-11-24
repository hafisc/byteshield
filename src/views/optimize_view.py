"""
Optimize View
Halaman untuk full optimization (clean + scan)
"""

import tkinter as tk
from tkinter import ttk
from src.config import COLORS


def create_optimize_view(parent, start_callback):
    """
    Create full optimization view
    
    Args:
        parent: Parent container frame
        start_callback: Callback function saat tombol Start diklik
        
    Returns:
        tk.Frame: Optimize view frame
    """
    view = tk.Frame(parent, bg=COLORS["bg_dark"])
    
    canvas = tk.Canvas(view, bg=COLORS["bg_dark"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(view, orient="vertical", command=canvas.yview)
    content = tk.Frame(canvas, bg=COLORS["bg_dark"])
    
    content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=content, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    tk.Label(content, text="⚡ Full System Optimization", font=("Segoe UI", 20, "bold"), bg=COLORS["bg_dark"], fg="white", anchor="w").pack(fill="x", pady=(0, 10))
    tk.Label(content, text="Complete cleanup and security scan in one go", font=("Segoe UI", 11), bg=COLORS["bg_dark"], fg=COLORS["text_secondary"], anchor="w").pack(fill="x", pady=(0, 20))
    
    # Timeline
    timeline_card = tk.Frame(content, bg=COLORS["card_bg"], bd=1, relief="solid")
    timeline_card.pack(fill="x", pady=(0, 20))
    tk.Frame(timeline_card, bg=COLORS["success"], height=3).pack(fill="x")
    
    timeline_content = tk.Frame(timeline_card, bg=COLORS["card_bg"])
    timeline_content.pack(fill="x", padx=15, pady=15)
    tk.Label(timeline_content, text="📋 Process Timeline", font=("Segoe UI", 12, "bold"), bg=COLORS["card_bg"], fg="white", anchor="w").pack(fill="x")
    
    steps = [
        ("1️⃣", "Clean junk files", "Remove temp files and cache"),
        ("2️⃣", "Quick virus scan", "Scan for malware and threats")
    ]
    
    for num, title, desc in steps:
        step_frame = tk.Frame(timeline_content, bg=COLORS["card_bg"])
        step_frame.pack(fill="x", pady=8)
        tk.Label(step_frame, text=num, font=("Segoe UI", 16), bg=COLORS["card_bg"], fg=COLORS["success"]).pack(side="left", padx=(0, 10))
        
        text_frame = tk.Frame(step_frame, bg=COLORS["card_bg"])
        text_frame.pack(side="left", fill="x", expand=True)
        tk.Label(text_frame, text=title, font=("Segoe UI", 10, "bold"), bg=COLORS["card_bg"], fg="white", anchor="w").pack(fill="x")
        tk.Label(text_frame, text=desc, font=("Segoe UI", 9), bg=COLORS["card_bg"], fg=COLORS["text_secondary"], anchor="w").pack(fill="x")
    
    # Estimated time
    time_card = tk.Frame(content, bg=COLORS["card_bg"], bd=1, relief="solid")
    time_card.pack(fill="x", pady=(0, 20))
    tk.Frame(time_card, bg=COLORS["accent"], height=3).pack(fill="x")
    
    time_content = tk.Frame(time_card, bg=COLORS["card_bg"])
    time_content.pack(fill="x", padx=15, pady=15)
    
    row = tk.Frame(time_content, bg=COLORS["card_bg"])
    row.pack(fill="x")
    tk.Label(row, text="⏱️ Estimated Time:", font=("Segoe UI", 11, "bold"), bg=COLORS["card_bg"], fg="white").pack(side="left")
    tk.Label(row, text="3-10 minutes", font=("Segoe UI", 11), bg=COLORS["card_bg"], fg=COLORS["accent"]).pack(side="left", padx=(10, 0))
    
    tk.Button(content, text="🚀 Start Optimization", font=("Segoe UI", 14, "bold"), bg=COLORS["success"], fg="white", activebackground=COLORS["accent"], activeforeground="white", relief="flat", bd=0, padx=30, pady=15, cursor="hand2", command=start_callback).pack(fill="x", pady=10)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return view
