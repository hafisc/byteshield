"""
File Cleaner Module
Logic untuk membersihkan file sampah
"""

import os
import shutil
from pathlib import Path


def clean_folder(path, log_callback=None):
    """
    Membersihkan isi folder tertentu
    
    Args:
        path: Path folder yang akan dibersihkan
        log_callback: Function untuk logging (optional)
    
    Returns:
        tuple: (deleted_count, error_count)
    """
    folder_path = Path(path)
    
    if not folder_path.exists():
        if log_callback:
            log_callback(f"[INFO] Folder tidak ditemukan: {path}", "INFO")
        return 0, 0
    
    if log_callback:
        log_callback(f"Scanning: {path}...", "INFO")
    
    deleted_count = 0
    error_count = 0
    
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
                error_count += 1
        
        if deleted_count > 0 and log_callback:
            log_callback(f"Yeeted {deleted_count} items from {folder_path.name}", "SUCCESS")
    except Exception as e:
        if log_callback:
            log_callback(f"Access Denied: {path}", "WARN")
        error_count += 1
    
    return deleted_count, error_count


def clean_junk(log_callback=None, status_callback=None):
    """
    Membersihkan semua file sampah di Windows
    
    Args:
        log_callback: Function untuk logging
        status_callback: Function untuk update status
    """
    if log_callback:
        log_callback("\n>>> INITIATING CLEANUP PROTOCOL", "HEADER")
    
    if status_callback:
        status_callback("🧹 Cleaning System...")
    
    # Daftar folder target
    temp_folders = [
        os.environ.get("TEMP"),
        os.environ.get("TMP"),
        r"C:\Windows\Temp",
        os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "Temp"),
        os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "Prefetch"),
    ]
    
    # Hapus duplicate dan None
    temp_folders = list(set(filter(None, temp_folders)))
    
    # Bersihkan setiap folder
    total_deleted = 0
    for folder in temp_folders:
        deleted, _ = clean_folder(folder, log_callback)
        total_deleted += deleted
    
    if log_callback:
        log_callback(">>> CLEANUP COMPLETE", "HEADER")
    
    return total_deleted
