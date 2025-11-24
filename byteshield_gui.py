"""
ByteShield - System Cleaner & Virus Scanner
Aplikasi desktop untuk membersihkan file sampah dan scan virus di Windows

Author: Hafis
Version: 1.0
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import os
import shutil
import subprocess
import threading
from pathlib import Path
from datetime import datetime


class ByteShieldApp(tk.Tk):
    """Main application class untuk ByteShield"""
    
    def __init__(self):
        super().__init__()
        
        # Konfigurasi window utama
        self.title("ByteShield - System Cleaner & Virus Check")
        self.geometry("700x600")
        self.resizable(False, False)
        
        # Flag untuk tracking proses
        self.is_running = False
        
        # Setup GUI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup semua komponen GUI"""
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header Frame
        header_frame = tk.Frame(self, bg="#2C3E50", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Judul aplikasi
        title_label = tk.Label(
            header_frame,
            text="🛡️ ByteShield",
            font=("Segoe UI", 24, "bold"),
            bg="#2C3E50",
            fg="white"
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="by Hafis - Pembersih Sistem & Virus Scanner",
            font=("Segoe UI", 10),
            bg="#2C3E50",
            fg="#BDC3C7"
        )
        subtitle_label.pack()
        
        # Main Content Frame
        content_frame = tk.Frame(self, bg="#ECF0F1")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Button Frame
        button_frame = tk.Frame(content_frame, bg="#ECF0F1")
        button_frame.pack(pady=(0, 15))
        
        # Tombol 1: Bersihkan Cache/Temp
        self.btn_clean = ttk.Button(
            button_frame,
            text="🧹 Bersihkan Cache/Temp",
            command=self.start_clean,
            width=25
        )
        self.btn_clean.grid(row=0, column=0, padx=5, pady=5)
        
        # Tombol 2: Quick Scan Virus
        self.btn_scan = ttk.Button(
            button_frame,
            text="🔍 Quick Scan Virus",
            command=self.start_scan,
            width=25
        )
        self.btn_scan.grid(row=0, column=1, padx=5, pady=5)
        
        # Tombol 3: Bersihkan + Scan
        self.btn_both = ttk.Button(
            button_frame,
            text="⚡ Bersihkan + Scan",
            command=self.start_both,
            width=25
        )
        self.btn_both.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(
            content_frame,
            mode='indeterminate',
            length=660
        )
        self.progress.pack(pady=(0, 10))
        
        # Log Area Frame
        log_frame = tk.LabelFrame(
            content_frame,
            text="📋 Log Proses",
            bg="#ECF0F1",
            font=("Segoe UI", 10, "bold")
        )
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # ScrolledText untuk log
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Consolas", 9),
            bg="#FFFFFF",
            fg="#2C3E50"
        )
        self.log_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Tag untuk warna log
        self.log_text.tag_config("INFO", foreground="#27AE60")
        self.log_text.tag_config("WARN", foreground="#F39C12")
        self.log_text.tag_config("ERROR", foreground="#E74C3C")
        self.log_text.tag_config("SUCCESS", foreground="#2ECC71", font=("Consolas", 9, "bold"))
        
        # Welcome message
        self.log("=" * 70)
        self.log("Selamat datang di ByteShield! 🛡️", "INFO")
        self.log("Pilih salah satu tombol di atas untuk memulai.", "INFO")
        self.log("=" * 70)
        
    def log(self, message, tag=""):
        """Menulis pesan ke log area dengan auto-scroll"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        # Update di main thread
        self.log_text.insert(tk.END, log_message, tag)
        self.log_text.see(tk.END)
        self.update_idletasks()
        
    def disable_buttons(self):
        """Disable semua tombol saat proses berjalan"""
        self.btn_clean.config(state="disabled")
        self.btn_scan.config(state="disabled")
        self.btn_both.config(state="disabled")
        
    def enable_buttons(self):
        """Enable semua tombol setelah proses selesai"""
        self.btn_clean.config(state="normal")
        self.btn_scan.config(state="normal")
        self.btn_both.config(state="normal")
        
    def start_progress(self):
        """Mulai progress bar"""
        self.progress.start(10)
        
    def stop_progress(self):
        """Stop progress bar"""
        self.progress.stop()
        
    # ==================== FUNGSI PEMBERSIHAN ====================
    
    def clean_folder(self, path):
        """
        Membersihkan isi folder tertentu
        
        Args:
            path: Path folder yang akan dibersihkan
        """
        folder_path = Path(path)
        
        # Cek apakah folder ada
        if not folder_path.exists():
            self.log(f"[INFO] Folder tidak ditemukan: {path}", "INFO")
            return
            
        self.log(f"Membersihkan folder: {path}", "INFO")
        
        deleted_count = 0
        error_count = 0
        
        # Iterasi semua isi folder
        try:
            for item in folder_path.iterdir():
                try:
                    if item.is_file() or item.is_symlink():
                        # Hapus file
                        item.unlink()
                        deleted_count += 1
                    elif item.is_dir():
                        # Hapus folder
                        shutil.rmtree(item, ignore_errors=True)
                        deleted_count += 1
                except Exception as e:
                    self.log(f"[WARN] Gagal hapus {item}: {str(e)}", "WARN")
                    error_count += 1
                    
            self.log(f"✓ Berhasil hapus {deleted_count} item dari {folder_path.name}", "INFO")
            if error_count > 0:
                self.log(f"⚠ {error_count} item gagal dihapus (mungkin sedang dipakai)", "WARN")
                
        except Exception as e:
            self.log(f"[ERROR] Gagal mengakses folder {path}: {str(e)}", "ERROR")
            
    def clean_junk(self):
        """Membersihkan semua file sampah di Windows"""
        self.log("\n" + "=" * 70)
        self.log("🧹 MULAI PEMBERSIHAN FILE SAMPAH", "INFO")
        self.log("=" * 70)
        
        # Daftar folder yang akan dibersihkan
        temp_folders = [
            os.environ.get("TEMP"),
            os.environ.get("TMP"),
            r"C:\Windows\Temp",
            os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "Temp"),
            os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "Prefetch"),
        ]
        
        # Hapus duplicate
        temp_folders = list(set(filter(None, temp_folders)))
        
        # Bersihkan setiap folder
        for folder in temp_folders:
            self.clean_folder(folder)
            
        self.log("\n" + "=" * 70)
        self.log("✅ PEMBERSIHAN SELESAI!", "SUCCESS")
        self.log("=" * 70)
        
    # ==================== FUNGSI WINDOWS DEFENDER ====================
    
    def run_defender_quick_scan(self):
        """Menjalankan Windows Defender Quick Scan"""
        self.log("\n" + "=" * 70)
        self.log("🔍 MEMULAI WINDOWS DEFENDER QUICK SCAN", "INFO")
        self.log("=" * 70)
        
        # Path ke MpCmdRun.exe
        defender_paths = [
            r"C:\Program Files\Windows Defender\MpCmdRun.exe",
            r"C:\ProgramData\Microsoft\Windows Defender\Platform\*\MpCmdRun.exe"
        ]
        
        defender_path = None
        
        # Cari MpCmdRun.exe
        for path_pattern in defender_paths:
            if "*" in path_pattern:
                # Expand wildcard
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
            self.log("[ERROR] MpCmdRun.exe tidak ditemukan.", "ERROR")
            self.log("[ERROR] Pastikan Windows Defender terinstall dengan benar.", "ERROR")
            self.log("[INFO] Lokasi yang dicek:", "INFO")
            for p in defender_paths:
                self.log(f"  - {p}", "INFO")
            return
            
        self.log(f"[INFO] Menggunakan: {defender_path}", "INFO")
        self.log("[INFO] Scan dimulai... (ini mungkin butuh beberapa menit)", "INFO")
        
        try:
            # Jalankan scan
            result = subprocess.run(
                [defender_path, "-Scan", "-ScanType", "1"],
                capture_output=True,
                text=True,
                check=False
            )
            
            # Log hasil
            if result.returncode == 0:
                self.log("[INFO] Quick Scan selesai dengan sukses! ✓", "SUCCESS")
            else:
                self.log(f"[WARN] Scan selesai dengan kode: {result.returncode}", "WARN")
                
            self.log("[INFO] Cek Windows Security untuk detail lengkap hasil scan.", "INFO")
            
            # Tampilkan output jika ada
            if result.stdout:
                self.log("\n--- Output Windows Defender ---", "INFO")
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        self.log(line, "INFO")
                        
        except Exception as e:
            self.log(f"[ERROR] Gagal menjalankan Windows Defender: {str(e)}", "ERROR")
            
        self.log("\n" + "=" * 70)
        self.log("✅ SCAN SELESAI!", "SUCCESS")
        self.log("=" * 70)
        
    # ==================== THREAD HANDLERS ====================
    
    def start_clean(self):
        """Handler untuk tombol Bersihkan Cache"""
        if self.is_running:
            self.log("[WARN] Proses sedang berjalan, tunggu sebentar...", "WARN")
            return
            
        self.is_running = True
        self.disable_buttons()
        self.start_progress()
        
        # Jalankan di thread terpisah
        thread = threading.Thread(target=self.clean_thread, daemon=True)
        thread.start()
        
    def clean_thread(self):
        """Thread untuk proses pembersihan"""
        try:
            self.clean_junk()
        finally:
            self.after(0, self.finish_process)
            
    def start_scan(self):
        """Handler untuk tombol Quick Scan"""
        if self.is_running:
            self.log("[WARN] Proses sedang berjalan, tunggu sebentar...", "WARN")
            return
            
        self.is_running = True
        self.disable_buttons()
        self.start_progress()
        
        # Jalankan di thread terpisah
        thread = threading.Thread(target=self.scan_thread, daemon=True)
        thread.start()
        
    def scan_thread(self):
        """Thread untuk proses scan"""
        try:
            self.run_defender_quick_scan()
        finally:
            self.after(0, self.finish_process)
            
    def start_both(self):
        """Handler untuk tombol Bersihkan + Scan"""
        if self.is_running:
            self.log("[WARN] Proses sedang berjalan, tunggu sebentar...", "WARN")
            return
            
        self.is_running = True
        self.disable_buttons()
        self.start_progress()
        
        # Jalankan di thread terpisah
        thread = threading.Thread(target=self.both_thread, daemon=True)
        thread.start()
        
    def both_thread(self):
        """Thread untuk proses pembersihan + scan"""
        try:
            self.clean_junk()
            self.run_defender_quick_scan()
        finally:
            self.after(0, self.finish_process)
            
    def finish_process(self):
        """Dipanggil setelah proses selesai"""
        self.stop_progress()
        self.enable_buttons()
        self.is_running = False
        self.log("\n💚 Semua proses selesai! ByteShield siap digunakan lagi.\n", "SUCCESS")


# ==================== MAIN PROGRAM ====================

def main():
    """Entry point aplikasi"""
    app = ByteShieldApp()
    app.mainloop()


if __name__ == "__main__":
    main()


# ==================== CARA BUILD KE .EXE ====================
#
# 1. Install PyInstaller dulu:
#    pip install pyinstaller
#
# 2. Build tanpa console (recommended untuk aplikasi GUI):
#    pyinstaller --onefile --noconsole --name ByteShield byteshield_gui.py
#
# 3. Build dengan console (untuk debugging):
#    pyinstaller --onefile --name ByteShield byteshield_gui.py
#
# 4. File .exe akan ada di folder 'dist/'
#
# 5. (Opsional) Tambahkan icon:
#    pyinstaller --onefile --noconsole --icon=icon.ico --name ByteShield byteshield_gui.py
#
# CATATAN:
# - Jalankan sebagai Administrator untuk hasil optimal
# - Windows Defender mungkin perlu izin admin
# - File .exe akan berukuran ~10-15 MB
