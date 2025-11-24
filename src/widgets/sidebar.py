"""
Sidebar Widget
Navigation sidebar dengan menu dan quick stats
"""

import tkinter as tk
from src.config import COLORS, APP_NAME, APP_VERSION, APP_AUTHOR, APP_SUBTITLE, SPACING, FONTS
from src.widgets.modern_button import ModernButton


class Sidebar:
    """Sidebar component dengan menu, stats, dan footer"""
    
    def __init__(self, parent, callbacks):
        """
        Initialize sidebar
        
        Args:
            parent: Parent window
            callbacks: Dict dengan callbacks untuk menu buttons
                {
                    'clean': callback_function,
                    'scan': callback_function,
                    'optimize': callback_function,
                    'sysinfo': callback_function
                }
        """
        self.frame = tk.Frame(parent, bg=COLORS["sidebar"], width=250)
        self.frame.pack(side="left", fill="y")
        self.frame.pack_propagate(False)
        
        self._setup_header()
        self._setup_menu(callbacks)
        self._setup_stats()
        self._setup_footer()
        
    def _setup_header(self):
        """Setup logo dan header"""
        logo_frame = tk.Frame(self.frame, bg=COLORS["sidebar"], pady=30)
        logo_frame.pack(fill="x")
        
        tk.Label(logo_frame, text="🛡️", font=("Segoe UI Emoji", 40), bg=COLORS["sidebar"], fg="white").pack()
        tk.Label(logo_frame, text=APP_NAME, font=("Segoe UI", 20, "bold"), bg=COLORS["sidebar"], fg="white").pack(pady=(10, 0))
        tk.Label(logo_frame, text=f"v{APP_VERSION} {APP_SUBTITLE}", font=("Segoe UI", 9), bg=COLORS["sidebar"], fg=COLORS["text_secondary"]).pack()
        tk.Label(logo_frame, text=f"by {APP_AUTHOR}", font=("Segoe UI", 8), bg=COLORS["sidebar"], fg=COLORS["text_tertiary"]).pack()
    
    def _setup_menu(self, callbacks):
        """Setup menu buttons"""
        menu_frame = tk.Frame(self.frame, bg=COLORS["sidebar"], pady=20)
        menu_frame.pack(fill="x", padx=15)
        
        self.btn_clean = ModernButton(menu_frame, text="Bersihin Sampah", icon="🧹", command=callbacks.get('clean'), color=COLORS["sidebar"], hover_color=COLORS["accent"])
        self.btn_clean.pack(fill="x", pady=5)
        
        self.btn_scan = ModernButton(menu_frame, text="Cek Virus", icon="🔍", command=callbacks.get('scan'), color=COLORS["sidebar"], hover_color=COLORS["accent"])
        self.btn_scan.pack(fill="x", pady=5)
        
        self.btn_optimize = ModernButton(menu_frame, text="Gas Semuanya", icon="⚡", command=callbacks.get('optimize'), color=COLORS["sidebar"], hover_color=COLORS["success"])
        self.btn_optimize.pack(fill="x", pady=5)
        
        tk.Frame(menu_frame, bg=COLORS["divider"], height=1).pack(fill="x", pady=10)
        
        # NEW: Uninstaller button
        self.btn_uninstaller = ModernButton(menu_frame, text="Uninstaller", icon="📦", command=callbacks.get('uninstaller'), color=COLORS["sidebar"], hover_color=COLORS["accent"])
        self.btn_uninstaller.pack(fill="x", pady=5)
        
        self.btn_sysinfo = ModernButton(menu_frame, text="System Info", icon="💻", command=callbacks.get('sysinfo'), color=COLORS["sidebar"], hover_color=COLORS["accent"])
        self.btn_sysinfo.pack(fill="x", pady=5)
    
    def _setup_stats(self):
        """Setup quick stats panel"""
        info_frame = tk.LabelFrame(self.frame, text=" Quick Stats ", font=("Consolas", 9, "bold"), bg=COLORS["sidebar"], fg=COLORS["text_secondary"], bd=1, relief="solid")
        info_frame.pack(fill="x", padx=15, pady=(30, 10))
        
        self.lbl_os = tk.Label(info_frame, text="OS: Scanning...", font=("Consolas", 8), bg=COLORS["sidebar"], fg=COLORS["text_primary"], anchor="w")
        self.lbl_os.pack(fill="x", padx=8, pady=2)
        
        self.lbl_ram = tk.Label(info_frame, text="RAM: Scanning...", font=("Consolas", 8), bg=COLORS["sidebar"], fg=COLORS["text_primary"], anchor="w")
        self.lbl_ram.pack(fill="x", padx=8, pady=2)
        
        self.lbl_disk = tk.Label(info_frame, text="Disk: Scanning...", font=("Consolas", 8), bg=COLORS["sidebar"], fg=COLORS["text_primary"], anchor="w")
        self.lbl_disk.pack(fill="x", padx=8, pady=2)
    
    def _setup_footer(self):
        """Setup footer"""
        tk.Label(self.frame, text="System Status: ONLINE", font=("Consolas", 8), bg=COLORS["sidebar"], fg=COLORS["success"]).pack(side="bottom", pady=20)
    
    def update_stats(self, os=None, ram=None, disk=None):
        """Update quick stats panel"""
        if os:
            self.lbl_os.config(text=f"OS: {os[:20]}")
        if ram:
            self.lbl_ram.config(text=f"RAM: {ram}")
        if disk:
            self.lbl_disk.config(text=f"Disk: {disk}")
    
    def disable_buttons(self):
        """Disable semua menu buttons"""
        for btn in [self.btn_clean, self.btn_scan, self.btn_optimize]:
            btn.config(state="disabled", cursor="arrow", bg=COLORS["sidebar"])
    
    def enable_buttons(self):
        """Enable semua menu buttons"""
        for btn in [self.btn_clean, self.btn_scan, self.btn_optimize]:
            btn.config(state="normal", cursor="hand2")
