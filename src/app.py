"""
ByteShield Main Application
Main application class yang mengkoordinasikan semua components
"""

import tkinter as tk
from tkinter import ttk
import threading
import ctypes

from src.config import COLORS, APP_TITLE
from src.widgets.sidebar import Sidebar
from src.views.home_view import create_home_view
from src.views.terminal_view import create_terminal_view, log_message
from src.views.clean_view import create_clean_view
from src.views.scan_view import create_scan_view
from src.views.optimize_view import create_optimize_view
from src.views.sysinfo_view import create_sysinfo_view, update_sysinfo_display
from src.core.cleaner import clean_junk
from src.core.scanner import run_defender_quick_scan
from src.core.system_info import get_system_info


class ByteShieldApp(tk.Tk):
    """Main application class"""
    
    def __init__(self):
        super().__init__()
        
        self.title(APP_TITLE)
        self.geometry("900x650")
        self.configure(bg=COLORS["bg_dark"])
        
        # Enable Dark Title Bar (Windows 10/11)
        self._enable_dark_titlebar()
        
        # Application state
        self.is_running = False
        self.system_info = {}
        self.current_view = "home"
        
        # Setup UI
        self._setup_ui()
        
        # Auto-scan sistem
        threading.Thread(target=self._initial_system_scan, daemon=True).start()
    
    def _enable_dark_titlebar(self):
        """Enable dark title bar untuk Windows 10/11"""
        try:
            self.update()
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ctypes.windll.user32.GetParent
            hwnd = get_parent(self.winfo_id())
            value = ctypes.c_int(2)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except:
            pass
    
    def _setup_ui(self):
        """Setup semua UI components"""
        # Sidebar
        self.sidebar = Sidebar(self, {
            'clean': self.show_clean_view,
            'scan': self.show_scan_view,
            'optimize': self.show_optimize_view,
            'sysinfo': self.show_sysinfo_view
        })
        
        # Content area
        content_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        content_frame.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        # Status header
        status_frame = tk.Frame(content_frame, bg=COLORS["bg_dark"])
        status_frame.pack(fill="x", pady=(0, 20))
        
        self.lbl_status = tk.Label(status_frame, text="👋 Welcome to ByteShield!", font=("Segoe UI", 24, "bold"), bg=COLORS["bg_dark"], fg="white", anchor="w")
        self.lbl_status.pack(fill="x")
        
        # Progress bar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Horizontal.TProgressbar", troughcolor=COLORS["terminal_bg"], background=COLORS["accent"], borderwidth=0, thickness=6)
        
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate', style="Horizontal.TProgressbar", length=100)
        
        # View container
        self.view_container = tk.Frame(content_frame, bg=COLORS["bg_dark"])
        self.view_container.pack(fill="both", expand=True)
        
        # Create all views
        self.home_view = create_home_view(self.view_container)
        
        # Clean view dengan inline logging
        from src.views.clean_view import log_to_clean_view, show_clean_log_area, clear_clean_log
        clean_result = create_clean_view(self.view_container, self.start_clean)
        self.clean_view = clean_result[0]
        self.clean_log_widget = clean_result[1]
        self.clean_log_frame = clean_result[2]
        self.clean_progress_frame = clean_result[3]
        self.clean_progress_bar = clean_result[4]
        self.clean_btn_start = clean_result[5]
        
        # Other views
        self.scan_view = create_scan_view(self.view_container, self.start_scan)
        self.optimize_view = create_optimize_view(self.view_container, self.start_optimize)
        
        self.sysinfo_view, self.sysinfo_container, self.sysinfo_placeholder = create_sysinfo_view(self.view_container)
        self.terminal_view, self.log_text = create_terminal_view(self.view_container)
        
        # Show home by default
        self.home_view.pack(fill="both", expand=True)
        
        # Initial logs
        self.log("ByteShield v2.0 initialized...", "HEADER")
        self.log("Preparing system scan...", "INFO")
    
    # ============ VIEW MANAGEMENT ============
    
    def _hide_all_views(self):
        """Hide semua views"""
        for view in [self.home_view, self.clean_view, self.scan_view, self.optimize_view, self.sysinfo_view, self.terminal_view]:
            view.pack_forget()
    
    def show_clean_view(self):
        """Show clean view"""
        self.current_view = "clean"
        self.lbl_status.config(text="🧹 Clean Junk Files")
        self._hide_all_views()
        self.clean_view.pack(fill="both", expand=True)
    
    def show_scan_view(self):
        """Show scan view"""
        self.current_view = "scan"
        self.lbl_status.config(text="🔍 Virus Quick Scan")
        self._hide_all_views()
        self.scan_view.pack(fill="both", expand=True)
    
    def show_optimize_view(self):
        """Show optimize view"""
        self.current_view = "optimize"
        self.lbl_status.config(text="⚡ Full Optimization")
        self._hide_all_views()
        self.optimize_view.pack(fill="both", expand=True)
    
    def show_sysinfo_view(self):
        """Show system info view"""
        self.current_view = "sysinfo"
        self.lbl_status.config(text="💻 System Information")
        self._hide_all_views()
        self.sysinfo_view.pack(fill="both", expand=True)
        update_sysinfo_display(self.sysinfo_container, self.sysinfo_placeholder, self.system_info)
        self.sysinfo_placeholder = None
    
    def show_terminal(self):
        """Show terminal view"""
        self.current_view = "terminal"
        self.lbl_status.config(text="📟 Terminal Output")
        self._hide_all_views()
        self.terminal_view.pack(fill="both", expand=True)
    
    # ============ HELPER FUNCTIONS ============
    
    def log(self, message, tag="INFO"):
        """Log message ke terminal"""
        log_message(self.log_text, message, tag)
    
    def set_status(self, text):
        """Update status header"""
        self.lbl_status.config(text=text)
    
    def start_progress(self):
        """Start progress bar"""
        self.progress.pack(fill="x", pady=(10, 0))
        self.progress.start(10)
    
    def stop_progress(self):
        """Stop progress bar"""
        self.progress.stop()
        self.progress.pack_forget()
    
    # ============ SYSTEM SCAN ============
    
    def _initial_system_scan(self):
        """System scan saat startup"""
        self.after(0, lambda: self.log("\n>>> SYSTEM SCAN INITIATED", "HEADER"))
        self.after(0, lambda: self.log("Analyzing system configuration...", "INFO"))
        
        info = get_system_info()
        self.system_info = info
        
        # Update UI
        if info.get('os'):
            self.after(0, lambda: self.sidebar.update_stats(os=info['os']))
            self.after(0, lambda: self.log(f"Operating System: {info['os']}", "INFO"))
        
        if info.get('ram'):
            self.after(0, lambda: self.sidebar.update_stats(ram=info['ram']))
            self.after(0, lambda: self.log(f"Memory: {info['ram']}", "INFO"))
        
        if info.get('disk'):
            self.after(0, lambda: self.sidebar.update_stats(disk=info['disk']))
            self.after(0, lambda: self.log(f"Storage (C:): {info['disk']}", " INFO"))
        
        self.after(0, lambda: self.log(">>> SYSTEM SCAN COMPLETE", "HEADER"))
        self.after(0, lambda: self.log("Waiting for user command...", "INFO"))
    
    # ============ PROCESS EXECUTORS ============
    
    def start_clean(self):
        """Start cleaning process dengan inline logging"""
        if self.is_running:
            return
        
        # Jangan switch ke terminal, stay di clean view
        # Show log area dan progress
        from src.views.clean_view import show_clean_log_area, clear_clean_log, log_to_clean_view
        clear_clean_log(self.clean_log_widget)
        show_clean_log_area(self.clean_log_frame)
        
        # Show progress bar
        self.clean_progress_frame.pack(fill="x", pady=(10, 0))
        self.clean_progress_bar.start(10)
        
        # Disable button
        self.clean_btn_start.config(state="disabled", text="⏳ Cleaning...", bg=COLORS["button_bg"])
        
        self.is_running = True
        self.sidebar.disable_buttons()
        threading.Thread(target=self._clean_thread_inline, daemon=True).start()
    
    def _clean_thread(self):
        """Clean thread (untuk terminal mode)"""
        try:
            clean_junk(log_callback=self.log, status_callback=self.set_status)
        finally:
            self.after(0, self._finish_process)
    
    def _clean_thread_inline(self):
        """Clean thread dengan inline logging"""
        from src.views.clean_view import log_to_clean_view
        
        def inline_log(msg, tag="INFO"):
            self.after(0, lambda: log_to_clean_view(self.clean_log_widget, msg, tag))
        
        try:
            clean_junk(log_callback=inline_log, status_callback=None)
        finally:
            self.after(0, self._finish_clean_process)
    
    def start_scan(self):
        """Start scanning process"""
        if self.is_running:
            return
        
        self.show_terminal()
        self.is_running = True
        self.sidebar.disable_buttons()
        self.start_progress()
        threading.Thread(target=self._scan_thread, daemon=True).start()
    
    def _scan_thread(self):
        """Scan thread"""
        try:
            run_defender_quick_scan(log_callback=self.log, status_callback=self.set_status)
        finally:
            self.after(0, self._finish_process)
    
    def start_optimize(self):
        """Start full optimization"""
        if self.is_running:
            return
        
        self.show_terminal()
        self.is_running = True
        self.sidebar.disable_buttons()
        self.start_progress()
        threading.Thread(target=self._optimize_thread, daemon=True).start()
    
    def _optimize_thread(self):
        """Optimize thread"""
        try:
            clean_junk(log_callback=self.log, status_callback=self.set_status)
            run_defender_quick_scan(log_callback=self.log, status_callback=self.set_status)
        finally:
            self.after(0, self._finish_process)
    
    def _finish_clean_process(self):
        """Finish clean process (inline mode)"""
        from src.views.clean_view import log_to_clean_view
        
        # Stop progress
        self.clean_progress_bar.stop()
        self.clean_progress_frame.pack_forget()
        
        # Re-enable button
        self.clean_btn_start.config(state="normal", text="🚀 Start Cleaning", bg=COLORS["success"])
        
        # Enable sidebar
        self.sidebar.enable_buttons()
        self.is_running = False
        
        # Final log
        log_to_clean_view(self.clean_log_widget, "\n✨ Cleaning complete! System optimized.", "SUCCESS")
    
    def _finish_process(self):
        """Finish process handler (untuk terminal mode)"""
        self.stop_progress()
        self.sidebar.enable_buttons()
        self.is_running = False
        self.set_status("✨ All Done! System Clean.")
        self.log("\nWaiting for next command...", "INFO")
