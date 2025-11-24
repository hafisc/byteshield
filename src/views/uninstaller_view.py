"""
Uninstaller View - Premium Edition
Display installed programs dengan table dan uninstall functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from src.config import COLORS, SPACING, FONTS
from src.widgets.premium_card import PremiumCard


def create_uninstaller_view(parent, uninstall_callback):
    """
    Create uninstaller view dengan program list
    
    Args:
        parent: Parent container frame
        uninstall_callback: Callback function untuk uninstall program
        
    Returns:
        tuple: (view_frame, programs_tree, refresh_callback)
    """
    view = tk.Frame(parent, bg=COLORS["bg_dark"])
    
    # === HERO TITLE ===
    tk.Label(
        view,
        text="📦 Program Uninstaller",
        font=(FONTS["family"], FONTS["size_hero"], FONTS["weight_bold"]),
        bg=COLORS["bg_dark"],
        fg=COLORS["text_primary"],
        anchor="w"
    ).pack(fill="x", pady=(0, SPACING["xs"]))
    
    tk.Label(
        view,
        text="Uninstall programs easily - including stubborn apps",
        font=(FONTS["family"], FONTS["size_body"]),
        bg=COLORS["bg_dark"],
        fg=COLORS["text_secondary"],
        anchor="w"
    ).pack(fill="x", pady=(0, SPACING["xl"]))
    
    # === INFO CARD ===
    info_card = PremiumCard(view, accent_color=COLORS["info"])
    info_card.pack(fill="x", pady=(0, SPACING["md"]))
    
    info_card.add_title("How It Works", "ℹ️")
    info_card.add_body(
        "• Select a program from the list below\n"
        "• Click 'Uninstall' to remove it normally\n"
        "• Some programs may require confirmation dialogs"
    )
    
    # === ACTION BAR ===
    action_bar = tk.Frame(view, bg=COLORS["bg_dark"])
    action_bar.pack(fill="x", pady=(0, SPACING["md"]))
    
    # Search box
    search_frame = tk.Frame(action_bar, bg=COLORS["bg_dark"])
    search_frame.pack(side="left", fill="x", expand=True)
    
    tk.Label(
        search_frame,
        text="🔍 Search:",
        font=(FONTS["family"], 10),
        bg=COLORS["bg_dark"],
        fg=COLORS["text_secondary"]
    ).pack(side="left", padx=(0, SPACING["sm"]))
    
    search_var = tk.StringVar()
    search_entry = tk.Entry(
        search_frame,
        textvariable=search_var,
        font=(FONTS["family"], 10),
        bg=COLORS["card_bg"],
        fg=COLORS["text_primary"],
        insertbackground=COLORS["accent"],
        relief="flat",
        bd=2
    )
    search_entry.pack(side="left", fill="x", expand=True, ipady=5)
    
    # Refresh button
    btn_refresh = tk.Button(
        action_bar,
        text="🔄 Refresh",
        font=(FONTS["family"], 10, FONTS["weight_bold"]),
        bg=COLORS["accent"],
        fg=COLORS["text_primary"],
        activebackground=COLORS["accent_hover"],
        relief="flat",
        bd=0,
        padx=SPACING["md"],
        pady=8,
        cursor="hand2"
    )
    btn_refresh.pack(side="right", padx=(SPACING["sm"], 0))
    
    # === PROGRAMS TABLE ===
    table_frame = tk.Frame(view, bg=COLORS["card_bg"], bd=2, relief="groove")
    table_frame.pack(fill="both", expand=True, pady=(0, SPACING["md"]))
    
    # Table style
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Uninstaller.Treeview",
        background=COLORS["terminal_bg"],
        foreground=COLORS["text_primary"],
        fieldbackground=COLORS["terminal_bg"],
        borderwidth=0,
        font=(FONTS["family"], 9)
    )
    style.configure(
        "Uninstaller.Treeview.Heading",
        background=COLORS["card_bg"],
        foreground=COLORS["accent"],
        borderwidth=0,
        font=(FONTS["family"], 10, FONTS["weight_bold"])
    )
    style.map("Uninstaller.Treeview", background=[("selected", COLORS["accent_glow"])])
    
    # Create treeview with scrollbars
    tree_container = tk.Frame(table_frame, bg=COLORS["terminal_bg"])
    tree_container.pack(fill="both", expand=True)
    
    # Scrollbars
    vsb = ttk.Scrollbar(tree_container, orient="vertical")
    hsb = ttk.Scrollbar(tree_container, orient="horizontal")
    
    # Treeview
    programs_tree = ttk.Treeview(
        tree_container,
        columns=("name", "publisher", "version", "size"),
        show="headings",
        style="Uninstaller.Treeview",
        yscrollcommand=vsb.set,
        xscrollcommand=hsb.set,
        selectmode="browse"
    )
    
    vsb.config(command=programs_tree.yview)
    hsb.config(command=programs_tree.xview)
    
    # Column headings
    programs_tree.heading("name", text="Program Name")
    programs_tree.heading("publisher", text="Publisher")
    programs_tree.heading("version", text="Version")
    programs_tree.heading("size", text="Size")
    
    # Column widths
    programs_tree.column("name", width=300, anchor="w")
    programs_tree.column("publisher", width=200, anchor="w")
    programs_tree.column("version", width=100, anchor="center")
    programs_tree.column("size", width=100, anchor="e")
    
    # Pack scrollbars and tree
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    programs_tree.pack(side="left", fill="both", expand=True)
    
    # Loading label (shown while scanning)
    loading_label = tk.Label(
        table_frame,
        text="⏳ Scanning installed programs...\nThis may take a few seconds",
        font=(FONTS["family"], 12),
        bg=COLORS["terminal_bg"],
        fg=COLORS["text_secondary"]
    )
    
    # === BUTTONS ===
    button_frame = tk.Frame(view, bg=COLORS["bg_dark"])
    button_frame.pack(fill="x")
    
    btn_uninstall = tk.Button(
        button_frame,
        text="🗑️  Uninstall Selected",
        font=(FONTS["family"], 12, FONTS["weight_bold"]),
        bg=COLORS["danger"],
        fg=COLORS["text_primary"],
        activebackground=COLORS["danger_glow"],
        activeforeground=COLORS["text_primary"],
        relief="raised",
        bd=2,
        padx=SPACING["lg"],
        pady=SPACING["sm"],
        cursor="hand2",
        state="disabled"
    )
    btn_uninstall.pack(side="left", expand=True, fill="x", padx=(0, SPACING["xs"]))
    
    # Future: Force uninstall button (disabled for now)
    btn_force = tk.Button(
        button_frame,
        text="⚠️ Force Uninstall",
        font=(FONTS["family"], 12, FONTS["weight_bold"]),
        bg=COLORS["button_bg"],
        fg=COLORS["text_disabled"],
        relief="raised",
        bd=2,
        padx=SPACING["lg"],
        pady=SPACING["sm"],
        state="disabled"
    )
    btn_force.pack(side="left", expand=True, fill="x", padx=(SPACING["xs"], 0))
    
    # === HELPER FUNCTIONS ===
    
    def on_program_select(event):
        """Enable uninstall button when program selected"""
        selection = programs_tree.selection()
        if selection:
            btn_uninstall.config(state="normal")
        else:
            btn_uninstall.config(state="disabled")
    
    programs_tree.bind("<<TreeviewSelect>>", on_program_select)
    
    def on_uninstall_click():
        """Handle uninstall button click"""
        selection = programs_tree.selection()
        if not selection:
            return
        
        item = programs_tree.item(selection[0])
        program_name = item['values'][0]
        
        # Confirm
        result = messagebox.askyesno(
            "Confirm Uninstall",
            f"Are you sure you want to uninstall:\n\n{program_name}\n\nThis will execute the program's uninstaller.",
            icon="warning"
        )
        
        if result:
            uninstall_callback(selection[0], programs_tree)
    
    btn_uninstall.config(command=on_uninstall_click)
    
    def on_search(*args):
        """Filter programs based on search"""
        # TODO: Implement search filtering
        pass
    
    search_var.trace("w", on_search)
    
    return view, programs_tree, loading_label, btn_refresh, search_var


def populate_programs_tree(tree, programs, loading_label=None):
    """
    Populate treeview dengan installed programs
    
    Args:
        tree: Treeview widget
        programs: List of program dicts
        loading_label: Loading label to hide after loading
    """
    # Clear existing
    for item in tree.get_children():
        tree.delete(item)
    
    # Add programs
    for prog in programs:
        tree.insert(
            "",
            "end",
            values=(
                prog['name'],
                prog['publisher'] or "Unknown",
                prog['version'] or "-",
                prog['size'] or "-"
            ),
            tags=(prog,)  # Store full program info in tags
        )
    
    # Hide loading label
    if loading_label:
        loading_label.place_forget()
