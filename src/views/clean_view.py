"""
Clean View - Premium Edition
Halaman untuk membersihkan file sampah dengan premium UI
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
from src.config import COLORS, SPACING, FONTS
from src.widgets.premium_card import PremiumCard


def create_clean_view(parent, start_callback):
    """
    Create premium clean junk files view
    
    Args:
        parent: Parent container frame
        start_callback: Callback function saat tombol Start diklik
        
    Returns:
        tuple: (view_frame, log_widget, progress_widget, btn_start)
    """
    view = tk.Frame(parent, bg=COLORS["bg_dark"])
    
    # Scrollable canvas
    canvas = tk.Canvas(view, bg=COLORS["bg_dark"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(view, orient="vertical", command=canvas.yview)
    content = tk.Frame(canvas, bg=COLORS["bg_dark"])
    
    content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=content, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # === HERO TITLE ===
    tk.Label(
        content,
        text="🧹 Clean Junk Files",
        font=(FONTS["family"], FONTS["size_hero"], FONTS["weight_bold"]),
        bg=COLORS["bg_dark"],
        fg=COLORS["text_primary"],
        anchor="w"
    ).pack(fill="x", pady=(0, SPACING["xs"]))
    
    tk.Label(
        content,
        text="Remove temporary files and cache to free up disk space",
        font=(FONTS["family"], FONTS["size_body"]),
        bg=COLORS["bg_dark"],
        fg=COLORS["text_secondary"],
        anchor="w"
    ).pack(fill="x", pady=(0, SPACING["xl"]))
    
    # === WARNING CARD ===
    warning_card = PremiumCard(content, accent_color=COLORS["danger"])
    warning_card.pack(fill="x", pady=(0, SPACING["md"]))
    
    warning_card.add_title("Before You Start", "⚠️")
    warning_card.add_body(
        "• Close all running applications\n"
        "• Files will be permanently deleted\n"
        "• Process may take a few minutes"
    )
    
    # === TARGET LOCATIONS CARD ===
    target_card = PremiumCard(content, accent_color=COLORS["accent"])
    target_card.pack(fill="x", pady=(0, SPACING["xl"]))
    
    target_card.add_title("Target Locations", "📂")
    
    # Create grid untuk locations
    locations_frame = tk.Frame(target_card.content, bg=COLORS["card_bg"])
    locations_frame.pack(fill="x", pady=(SPACING["sm"], 0))
    
    locations = [
        ("📁", "%TEMP%", "User temporary files"),
        ("📁", "%TMP%", "System temporary files"),
        ("📁", "Windows\\Temp", "Windows temp folder"),
        ("📁", "Prefetch", "Prefetch cache")
    ]
    
    for icon, path, desc in locations:
        loc_frame = tk.Frame(locations_frame, bg=COLORS["card_bg"])
        loc_frame.pack(fill="x", pady=SPACING["xs"])
        
        tk.Label(
            loc_frame,
            text=f"{icon} {path}",
            font=(FONTS["family_mono"], 10, FONTS["weight_bold"]),
            bg=COLORS["card_bg"],
            fg=COLORS["accent_light"],
            anchor="w"
        ).pack(side="left")
        
        tk.Label(
            loc_frame,
            text=f" — {desc}",
            font=(FONTS["family"], FONTS["size_small"]),
            bg=COLORS["card_bg"],
            fg=COLORS["text_tertiary"],
            anchor="w"
        ).pack(side="left")
    
    # === ACTION SECTION ===
    action_frame = tk.Frame(content, bg=COLORS["bg_dark"])
    action_frame.pack(fill="x", pady=(0, SPACING["md"]))
    
    # Premium Start Button
    btn_start = tk.Button(
        action_frame,
        text="🚀  Start Cleaning",
        font=(FONTS["family"], 14, FONTS["weight_bold"]),
        bg=COLORS["success"],
        fg=COLORS["text_primary"],
        activebackground=COLORS["success_glow"],
        activeforeground=COLORS["text_primary"],
        relief="raised",
        bd=2,
        padx=SPACING["xl"],
        pady=SPACING["md"],
        cursor="hand2",
        command=start_callback
    )
    btn_start.pack(fill="x")
    
    # Bind hover effects
    def btn_hover(e):
        if btn_start['state'] != 'disabled':
            btn_start.config(bg=COLORS["success_glow"])
    
    def btn_leave(e):
        if btn_start['state'] != 'disabled':
            btn_start.config(bg=COLORS["success"])
    
    btn_start.bind("<Enter>", btn_hover)
    btn_start.bind("<Leave>", btn_leave)
    
    # Progress frame (hidden by default)
    progress_frame = tk.Frame(action_frame, bg=COLORS["bg_dark"])
    
    style = ttk.Style()
    style.configure(
        "CleanProgress.Horizontal.TProgressbar",
        troughcolor=COLORS["terminal_bg"],
        background=COLORS["accent"],
        borderwidth=0,
        thickness=5
    )
    
    progress_bar = ttk.Progressbar(
        progress_frame,
        mode='indeterminate',
        style="CleanProgress.Horizontal.TProgressbar"
    )
    progress_bar.pack(fill="x", pady=(SPACING["sm"], 0))
    
    # === LOG AREA (collapsible) ===
    log_frame = tk.LabelFrame(
        content,
        text=" 📋 Cleaning Log ",
        font=(FONTS["family_mono"], 10, FONTS["weight_bold"]),
        bg=COLORS["bg_dark"],
        fg=COLORS["text_secondary"],
        bd=2,
        relief="groove"
    )
    
    log_text = scrolledtext.ScrolledText(
        log_frame,
        wrap=tk.WORD,
        font=(FONTS["family_mono"], 9),
        bg=COLORS["terminal_bg"],
        fg=COLORS["text_primary"],
        bd=0,
        padx=SPACING["md"],
        pady=SPACING["md"],
        height=14,
        insertbackground=COLORS["accent"],
        state="disabled"
    )
    log_text.pack(fill="both", expand=True)
    
    # Enhanced tag colors
    log_text.tag_config("INFO", foreground=COLORS["text_primary"])
    log_text.tag_config("WARN", foreground=COLORS["warning"])
    log_text.tag_config("ERROR", foreground=COLORS["danger"])
    log_text.tag_config("SUCCESS", foreground=COLORS["success"])
    log_text.tag_config("HEADER", foreground=COLORS["accent"], font=(FONTS["family_mono"], 10, FONTS["weight_bold"]))
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return view, log_text, log_frame, progress_frame, progress_bar, btn_start


def log_to_clean_view(log_widget, message, tag="INFO"):
    """Log message to clean view"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"
    
    log_widget.config(state="normal")
    log_widget.insert(tk.END, log_message, tag)
    log_widget.see(tk.END)
    log_widget.config(state="disabled")
    log_widget.update_idletasks()


def show_clean_log_area(log_frame):
    """Show log area"""
    log_frame.pack(fill="both", expand=True, pady=(SPACING["lg"], 0))


def hide_clean_log_area(log_frame):
    """Hide log area"""
    log_frame.pack_forget()


def clear_clean_log(log_widget):
    """Clear log"""
    log_widget.config(state="normal")
    log_widget.delete("1.0", tk.END)
    log_widget.config(state="disabled")
