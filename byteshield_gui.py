"""
ByteShield - System Cleaner & Virus Scanner
Aplikasi desktop untuk membersihkan file sampah dan scan virus di Windows

Author: Hafis
Version: 2.0 (Gen Z Edition)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import os
import shutil
import subprocess
import threading
from pathlib import Path
from datetime import datetime
import ctypes

# Warna Tema (Cyberpunk / Dark Mode)
COLORS = {
    "bg_dark": "#0F172A",       # Background utama (Very Dark Blue)
    "sidebar": "#1E293B",       # Sidebar background
    "accent": "#38BDF8",        # Biru Muda (Cyan)
    "accent_hover": "#0EA5E9",  # Biru lebih gelap untuk hover
    "danger": "#F43F5E",        # Merah Pinkish
    "success": "#34D399",       # Hijau Mint
    "text_main": "#F8FAFC",     # Putih
    "text_sec": "#94A3B8",      # Abu-abu
    "terminal_bg": "#020617",   # Hitam pekat untuk log
    "button_bg": "#334155"      # Warna tombol default
}

class ModernButton(tk.Button):
    """Custom Button dengan Hover Effect"""
    def __init__(self, master, text, icon, command, color=COLORS["button_bg"], hover_color=COLORS["accent_hover"], **kwargs):
        super().__init__(master, **kwargs)
        self.color = color
        self.hover_color = hover_color
        self.command = command
        
        self.config(
            text=f" {icon}  {text}",
            font=("Segoe UI", 11, "bold"),
            bg=self.color,
            fg="white",
            activebackground=self.hover_color,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
            anchor="w",  # Align kiri
            command=self.on_click
        )
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, e):
        if self['state'] != 'disabled':
            self.config(bg=self.hover_color)
            
    def on_leave(self, e):
        if self['state'] != 'disabled':
            self.config(bg=self.color)

    def on_click(self):
        if self.command:
            self.command()

class ByteShieldApp(tk.Tk):
    """Main application class untuk ByteShield"""
    
    def __init__(self):
        super().__init__()
        
        # Konfigurasi window utama
        self.title("ByteShield // System Optimizer")
        self.geometry("900x650")
        self.configure(bg=COLORS["bg_dark"])
        
        # Enable Dark Title Bar (Windows 10/11 hack)
        try:
            self.update()
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ctypes.windll.user32.GetParent
            hwnd = get_parent(self.winfo_id())
            rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
            value = 2
            value = ctypes.c_int(value)
            set_window_attribute(hwnd, rendering_policy, ctypes.byref(value), ctypes.sizeof(value))
        except:
            pass

        # Flag untuk tracking proses
        self.is_running = False
        
        # System Info Storage
        self.system_info = {}
        
        # Current View (terminal / sysinfo)
        self.current_view = "terminal"
        
        # Setup GUI
        self.setup_ui()
        
        # Auto-scan sistem saat startup (di thread terpisah biar ga ngelag)
        threading.Thread(target=self.initial_system_scan, daemon=True).start()
        
    def setup_ui(self):
        """Setup semua komponen GUI dengan layout Sidebar"""
        
        # ================= SIDEBAR (KIRI) =================
        sidebar = tk.Frame(self, bg=COLORS["sidebar"], width=250)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False) # Tahan ukuran sidebar
        
        # Logo / Header Sidebar
        logo_frame = tk.Frame(sidebar, bg=COLORS["sidebar"], pady=30)
        logo_frame.pack(fill="x")
        
        lbl_logo = tk.Label(
            logo_frame, 
            text="🛡️", 
            font=("Segoe UI Emoji", 40), 
            bg=COLORS["sidebar"], 
            fg="white"
        )
        lbl_logo.pack()
        
        lbl_title = tk.Label(
            logo_frame, 
            text="ByteShield", 
            font=("Segoe UI", 20, "bold"), 
            bg=COLORS["sidebar"], 
            fg="white"
        )
        lbl_title.pack(pady=(10, 0))
        
        lbl_subtitle = tk.Label(
            logo_frame, 
            text="v2.0 by Hafis", 
            font=("Segoe UI", 9), 
            bg=COLORS["sidebar"], 
            fg=COLORS["text_sec"]
        )
        lbl_subtitle.pack()

        # Menu Buttons di Sidebar
        menu_frame = tk.Frame(sidebar, bg=COLORS["sidebar"], pady=20)
        menu_frame.pack(fill="x", padx=15)
        
        self.btn_clean = ModernButton(
            menu_frame,
            text="Bersihin Sampah",
            icon="🧹",
            command=self.start_clean,
            color=COLORS["sidebar"],
            hover_color=COLORS["accent"]
        )
        self.btn_clean.pack(fill="x", pady=5)
        
        self.btn_scan = ModernButton(
            menu_frame,
            text="Cek Virus",
            icon="🔍",
            command=self.start_scan,
            color=COLORS["sidebar"],
            hover_color=COLORS["accent"]
        )
        self.btn_scan.pack(fill="x", pady=5)
        
        self.btn_both = ModernButton(
            menu_frame,
            text="Gas Semuanya",
            icon="⚡",
            command=self.start_both,
            color=COLORS["sidebar"],
            hover_color=COLORS["success"]
        )
        self.btn_both.pack(fill="x", pady=5)
        
        # Separator
        sep = tk.Frame(menu_frame, bg=COLORS["text_sec"], height=1)
        sep.pack(fill="x", pady=10)
        
        # System Info Button
        self.btn_sysinfo = ModernButton(
            menu_frame,
            text="System Info",
            icon="💻",
            command=self.show_system_info,
            color=COLORS["sidebar"],
            hover_color=COLORS["accent"]
        )
        self.btn_sysinfo.pack(fill="x", pady=5)

        # System Info Panel (dynamic)
        info_frame = tk.LabelFrame(
            sidebar,
            text=" System Info ",
            font=("Consolas", 9, "bold"),
            bg=COLORS["sidebar"],
            fg=COLORS["text_sec"],
            bd=1,
            relief="solid"
        )
        info_frame.pack(fill="x", padx=15, pady=(30, 10))
        
        self.lbl_os = tk.Label(
            info_frame,
            text="OS: Scanning...",
            font=("Consolas", 8),
            bg=COLORS["sidebar"],
            fg=COLORS["text_main"],
            anchor="w"
        )
        self.lbl_os.pack(fill="x", padx=8, pady=2)
        
        self.lbl_cpu = tk.Label(
            info_frame,
            text="CPU: Scanning...",
            font=("Consolas", 8),
            bg=COLORS["sidebar"],
            fg=COLORS["text_main"],
            anchor="w"
        )
        self.lbl_cpu.pack(fill="x", padx=8, pady=2)
        
        self.lbl_ram = tk.Label(
            info_frame,
            text="RAM: Scanning...",
            font=("Consolas", 8),
            bg=COLORS["sidebar"],
            fg=COLORS["text_main"],
            anchor="w"
        )
        self.lbl_ram.pack(fill="x", padx=8, pady=2)
        
        self.lbl_disk = tk.Label(
            info_frame,
            text="Disk: Scanning...",
            font=("Consolas", 8),
            bg=COLORS["sidebar"],
            fg=COLORS["text_main"],
            anchor="w"
        )
        self.lbl_disk.pack(fill="x", padx=8, pady=2)

        # Footer Sidebar
        lbl_footer = tk.Label(
            sidebar,
            text="System Status: ONLINE",
            font=("Consolas", 8),
            bg=COLORS["sidebar"],
            fg=COLORS["success"]
        )
        lbl_footer.pack(side="bottom", pady=20)

        # ================= CONTENT (KANAN) =================
        self.content_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        self.content_frame.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        # Status Header Frame
        status_frame = tk.Frame(self.content_frame, bg=COLORS["bg_dark"])
        status_frame.pack(fill="x", pady=(0, 20))

        self.lbl_status = tk.Label(
            status_frame,
            text="👋 Ready to Optimize!",
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["bg_dark"],
            fg="white",
            anchor="w"
        )
        self.lbl_status.pack(fill="x")
        
        # Progress Bar Custom Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Horizontal.TProgressbar",
            troughcolor=COLORS["terminal_bg"],
            background=COLORS["accent"],
            borderwidth=0,
            thickness=6
        )
        
        self.progress = ttk.Progressbar(
            status_frame,
            mode='indeterminate',
            style="Horizontal.TProgressbar",
            length=100
        )
        # Progress bar di-pack nanti saat butuh
        
        # Container untuk views yang bisa di-switch
        self.view_container = tk.Frame(self.content_frame, bg=COLORS["bg_dark"])
        self.view_container.pack(fill="both", expand=True)
        
        # ===== VIEW 1: TERMINAL =====
        self.terminal_view = tk.Frame(self.view_container, bg=COLORS["bg_dark"])
        
        log_container = tk.LabelFrame(
            self.terminal_view,
            text=" TERMINAL OUTPUT ",
            font=("Consolas", 10, "bold"),
            bg=COLORS["bg_dark"],
            fg=COLORS["text_sec"],
            bd=1,
            relief="solid"
        )
        log_container.pack(fill="both", expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_container,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg=COLORS["terminal_bg"],
            fg=COLORS["text_main"],
            bd=0,
            padx=10,
            pady=10,
            insertbackground="white"
        )
        self.log_text.pack(fill="both", expand=True)
        
        # Tag Colors
        self.log_text.tag_config("INFO", foreground=COLORS["text_main"])
        self.log_text.tag_config("WARN", foreground="#FCD34D")
        self.log_text.tag_config("ERROR", foreground=COLORS["danger"])
        self.log_text.tag_config("SUCCESS", foreground=COLORS["success"])
        self.log_text.tag_config("HEADER", foreground=COLORS["accent"], font=("Consolas", 10, "bold"))
        
        # ===== VIEW 2: SYSTEM INFO =====
        self.sysinfo_view = tk.Frame(self.view_container, bg=COLORS["bg_dark"])
        self.setup_sysinfo_view()
        
        # Show terminal view by default
        self.terminal_view.pack(fill="both", expand=True)
        
        # Initial Log
        self.log("ByteShield v2.0 initialized...", "HEADER")
        self.log("Preparing system scan...", "INFO")

    # ================= VIEW MANAGEMENT =================
    
    def setup_sysinfo_view(self):
        """Setup halaman System Info dengan detail lengkap"""
        
        # Title
        title = tk.Label(
            self.sysinfo_view,
            text="💻 System Information",
            font=("Segoe UI", 20, "bold"),
            bg=COLORS["bg_dark"],
            fg="white",
            anchor="w"
        )
        title.pack(fill="x", pady=(0, 20))
        
        # Scrollable frame untuk konten
        canvas = tk.Canvas(self.sysinfo_view, bg=COLORS["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.sysinfo_view, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["bg_dark"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Info Cards Container
        self.info_cards_container = scrollable_frame
        
        # Placeholder while scanning
        self.sysinfo_placeholder = tk.Label(
            scrollable_frame,
            text="⏳ Scanning system...",
            font=("Segoe UI", 14),
            bg=COLORS["bg_dark"],
            fg=COLORS["text_sec"]
        )
        self.sysinfo_placeholder.pack(expand=True, pady=100)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_system_info(self):
        """Switch ke view System Info"""
        if self.current_view == "sysinfo":
            return  # Already showing
            
        self.current_view = "sysinfo"
        self.lbl_status.config(text="💻 System Information", fg="white")
        
        # Hide terminal, show sysinfo
        self.terminal_view.pack_forget()
        self.sysinfo_view.pack(fill="both", expand=True)
        
        # Update sysinfo content
        self.update_sysinfo_display()
    
    def show_terminal(self):
        """Switch ke view Terminal"""
        if self.current_view == "terminal":
            return
            
        self.current_view = "terminal"
        self.lbl_status.config(text="👋 Ready to Optimize!", fg="white")
        
        # Hide sysinfo, show terminal
        self.sysinfo_view.pack_forget()
        self.terminal_view.pack(fill="both", expand=True)
    
    def update_sysinfo_display(self):
        """Update tampilan System Info dengan data terbaru"""
        # Remove placeholder
        if self.sysinfo_placeholder:
            self.sysinfo_placeholder.destroy()
            self.sysinfo_placeholder = None
        
        # Clear existing cards
        for widget in self.info_cards_container.winfo_children():
            widget.destroy()
        
        # Create info cards
        info_items = [
            ("🖥️ Operating System", self.system_info.get('os', 'Unknown'), COLORS["accent"]),
            ("⚙️ Processor", self.system_info.get('cpu', 'Unknown'), COLORS["success"]),
            ("💾 Memory (RAM)", self.system_info.get('ram', 'Unknown'), COLORS["danger"]),
            ("💿 Storage (C:)", self.system_info.get('disk', 'Unknown'), "#A78BFA"),
        ]
        
        for icon_title, value, color in info_items:
            card = tk.Frame(
                self.info_cards_container,
                bg=COLORS["sidebar"],
                bd=0,
                relief="solid"
            )
            card.pack(fill="x", pady=10)
            
            # Accent bar
            accent_bar = tk.Frame(card, bg=color, width=5)
            accent_bar.pack(side="left", fill="y")
            
            # Content
            content = tk.Frame(card, bg=COLORS["sidebar"])
            content.pack(side="left", fill="both", expand=True, padx=15, pady=15)
            
            lbl_title = tk.Label(
                content,
                text=icon_title,
                font=("Segoe UI", 12, "bold"),
                bg=COLORS["sidebar"],
                fg=COLORS["text_sec"],
                anchor="w"
            )
            lbl_title.pack(fill="x")
            
            lbl_value = tk.Label(
                content,
                text=value,
                font=("Segoe UI", 14),
                bg=COLORS["sidebar"],
                fg="white",
                anchor="w"
            )
            lbl_value.pack(fill="x", pady=(5, 0))
        
        # Back button
        btn_back = tk.Button(
            self.info_cards_container,
            text="← Back to Terminal",
            font=("Segoe UI", 11),
            bg=COLORS["button_bg"],
            fg="white",
            activebackground=COLORS["accent"],
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.show_terminal
        )
        btn_back.pack(fill="x", pady=20)

    # ================= LOGIC (Sama seperti sebelumnya) =================
    
    def log(self, message, tag="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_message, tag)
        self.log_text.see(tk.END)
        self.update_idletasks()
        
    def set_status(self, text, color="white"):
        self.lbl_status.config(text=text, fg=color)

    def disable_buttons(self):
        for btn in [self.btn_clean, self.btn_scan, self.btn_both]:
            btn.config(state="disabled", cursor="arrow", bg=COLORS["sidebar"])

    def enable_buttons(self):
        for btn in [self.btn_clean, self.btn_scan, self.btn_both]:
            btn.config(state="normal", cursor="hand2")
    
    def switch_to_terminal_on_action(self):
        """Auto switch ke terminal saat ada aksi clean/scan"""
        if self.current_view != "terminal":
            self.show_terminal()

    def start_progress(self):
        self.progress.pack(fill="x", pady=(10, 0))
        self.progress.start(10)
        
    def stop_progress(self):
        self.progress.stop()
        self.progress.pack_forget()

    # ================= SYSTEM SCAN FUNCTIONS =================
    
    def get_system_info(self):
        """Mengambil informasi sistem Windows"""
        info = {}
        
        try:
            # OS Info
            import platform
            info['os'] = f"{platform.system()} {platform.release()}"
            
            # CPU Info
            try:
                import wmi
                c = wmi.WMI()
                for processor in c.Win32_Processor():
                    info['cpu'] = processor.Name.strip()
                    break
            except:
                # Fallback jika wmi ga ada
                info['cpu'] = platform.processor() or "Unknown CPU"
            
            # RAM Info
            try:
                import psutil
                ram = psutil.virtual_memory()
                total_gb = ram.total / (1024**3)
                used_gb = ram.used / (1024**3)
                info['ram'] = f"{used_gb:.1f}GB / {total_gb:.1f}GB ({ram.percent}%)"
            except:
                # Fallback manual via WMI
                try:
                    c = wmi.WMI()
                    total_ram = 0
                    for mem in c.Win32_ComputerSystem():
                        total_ram = int(mem.TotalPhysicalMemory) / (1024**3)
                    info['ram'] = f"{total_ram:.1f}GB"
                except:
                    info['ram'] = "Unknown"
            
            # Disk Info (C: drive)
            try:
                import psutil
                disk = psutil.disk_usage('C:')
                free_gb = disk.free / (1024**3)
                total_gb = disk.total / (1024**3)
                info['disk'] = f"{free_gb:.1f}GB free / {total_gb:.1f}GB ({disk.percent}%)"
            except:
                try:
                    import shutil
                    total, used, free = shutil.disk_usage("C:")
                    free_gb = free / (1024**3)
                    total_gb = total / (1024**3)
                    info['disk'] = f"{free_gb:.1f}GB free / {total_gb:.1f}GB"
                except:
                    info['disk'] = "Unknown"
                    
        except Exception as e:
            self.log(f"System scan error: {str(e)}", "ERROR")
            
        return info
    
    def initial_system_scan(self):
        """Scan sistem otomatis saat startup"""
        self.after(0, lambda: self.log("\n>>> SYSTEM SCAN INITIATED", "HEADER"))
        self.after(0, lambda: self.log("Analyzing system configuration...", "INFO"))
        
        # Get system info
        info = self.get_system_info()
        self.system_info = info
        
        # Update UI (harus di main thread)
        if info.get('os'):
            self.after(0, lambda: self.lbl_os.config(text=f"OS: {info['os'][:20]}"))
            self.after(0, lambda: self.log(f"Operating System: {info['os']}", "INFO"))
        
        if info.get('cpu'):
            cpu_short = info['cpu'][:25] + "..." if len(info['cpu']) > 25 else info['cpu']
            self.after(0, lambda: self.lbl_cpu.config(text=f"CPU: {cpu_short}"))
            self.after(0, lambda: self.log(f"Processor: {info['cpu']}", "INFO"))
        
        if info.get('ram'):
            self.after(0, lambda: self.lbl_ram.config(text=f"RAM: {info['ram']}"))
            self.after(0, lambda: self.log(f"Memory: {info['ram']}", "INFO"))
        
        if info.get('disk'):
            self.after(0, lambda: self.lbl_disk.config(text=f"Disk: {info['disk']}"))
            self.after(0, lambda: self.log(f"Storage (C:): {info['disk']}", "INFO"))
        
        self.after(0, lambda: self.log(">>> SYSTEM SCAN COMPLETE", "HEADER"))
        self.after(0, lambda: self.log("Waiting for user command...", "INFO"))


    # --- CLEANING LOGIC ---
    def clean_folder(self, path):
        folder_path = Path(path)
        if not folder_path.exists():
            return
            
        self.log(f"Scanning: {path}...", "INFO")
        deleted_count = 0
        
        try:
            for item in folder_path.iterdir():
                try:
                    if item.is_file() or item.is_symlink():
                        item.unlink()
                        deleted_count += 1
                    elif item.is_dir():
                        shutil.rmtree(item, ignore_errors=True)
                        deleted_count += 1
                except:
                    pass # Silent fail biar log ga penuh spam
            
            if deleted_count > 0:
                self.log(f"Yeeted {deleted_count} items from {folder_path.name}", "SUCCESS")
                
        except Exception as e:
            self.log(f"Access Denied: {path}", "WARN")

    def clean_junk(self):
        self.log("\n>>> INITIATING CLEANUP PROTOCOL", "HEADER")
        self.set_status("🧹 Cleaning System...", COLORS["accent"])
        
        temp_folders = [
            os.environ.get("TEMP"),
            os.environ.get("TMP"),
            r"C:\Windows\Temp",
            os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "Temp"),
            os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "Prefetch"),
        ]
        temp_folders = list(set(filter(None, temp_folders)))
        
        for folder in temp_folders:
            self.clean_folder(folder)
            
        self.log(">>> CLEANUP COMPLETE", "HEADER")

    # --- DEFENDER LOGIC ---
    def run_defender_quick_scan(self):
        self.log("\n>>> INITIATING VIRUS SCAN", "HEADER")
        self.set_status("🔍 Scanning for Threats...", COLORS["accent"])
        
        defender_paths = [
            r"C:\Program Files\Windows Defender\MpCmdRun.exe",
            r"C:\ProgramData\Microsoft\Windows Defender\Platform\*\MpCmdRun.exe"
        ]
        
        defender_path = None
        for path_pattern in defender_paths:
            if "*" in path_pattern:
                import glob
                matches = glob.glob(path_pattern)
                if matches:
                    defender_path = matches[0]
                    break
            else:
                if os.path.exists(path_pattern):
                    defender_path = path_pattern
                    break
                    
        if not defender_path:
            self.log("ERROR: Windows Defender not found!", "ERROR")
            return
            
        self.log("Defender Engine: Linked", "INFO")
        self.log("Running Quick Scan...", "INFO")
        
        try:
            result = subprocess.run(
                [defender_path, "-Scan", "-ScanType", "1"],
                capture_output=True,
                text=True,
                check=False,
                creationflags=subprocess.CREATE_NO_WINDOW # Sembunyikan window cmd
            )
            
            if result.returncode == 0:
                self.log("Scan Result: NO THREATS FOUND", "SUCCESS")
            else:
                self.log(f"Scan Result: Code {result.returncode} (Check Security Center)", "WARN")
                
        except Exception as e:
            self.log(f"Scan Error: {str(e)}", "ERROR")
            
        self.log(">>> SCAN COMPLETE", "HEADER")

    # --- THREADING ---
    def start_clean(self):
        if self.is_running: return
        self.switch_to_terminal_on_action()
        self.is_running = True
        self.disable_buttons()
        self.start_progress()
        threading.Thread(target=self.clean_thread, daemon=True).start()
        
    def clean_thread(self):
        try: self.clean_junk()
        finally: self.after(0, self.finish_process)
            
    def start_scan(self):
        if self.is_running: return
        self.switch_to_terminal_on_action()
        self.is_running = True
        self.disable_buttons()
        self.start_progress()
        threading.Thread(target=self.scan_thread, daemon=True).start()
        
    def scan_thread(self):
        try: self.run_defender_quick_scan()
        finally: self.after(0, self.finish_process)
            
    def start_both(self):
        if self.is_running: return
        self.switch_to_terminal_on_action()
        self.is_running = True
        self.disable_buttons()
        self.start_progress()
        threading.Thread(target=self.both_thread, daemon=True).start()
        
    def both_thread(self):
        try:
            self.clean_junk()
            self.run_defender_quick_scan()
        finally:
            self.after(0, self.finish_process)
            
    def finish_process(self):
        self.stop_progress()
        self.enable_buttons()
        self.is_running = False
        self.set_status("✨ All Done! System Clean.", COLORS["success"])
        self.log("\nWaiting for next command...", "INFO")

def main():
    app = ByteShieldApp()
    app.mainloop()

if __name__ == "__main__":
    main()
