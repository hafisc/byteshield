"""
Windows Defender Scanner Module
Logic untuk running Windows Defender scans
"""

import os
import subprocess
import glob


def run_defender_quick_scan(log_callback=None, status_callback=None):
    """
    Menjalankan Windows Defender Quick Scan
    
    Args:
        log_callback: Function untuk logging
        status_callback: Function untuk update status
        
    Returns:
        bool: True jika scan berhasil
    """
    if log_callback:
        log_callback("\n>>> INITIATING VIRUS SCAN", "HEADER")
    
    if status_callback:
        status_callback("🔍 Scanning for Threats...")
    
    # Path ke MpCmdRun.exe
    defender_paths = [
        r"C:\Program Files\Windows Defender\MpCmdRun.exe",
        r"C:\ProgramData\Microsoft\Windows Defender\Platform\*\MpCmdRun.exe"
    ]
    
    defender_path = None
    
    # Cari MpCmdRun.exe
    for path_pattern in defender_paths:
        if "*" in path_pattern:
            matches = glob.glob(path_pattern)
            if matches:
                defender_path = matches[0]
                break
        else:
            if os.path.exists(path_pattern):
                defender_path = path_pattern
                break
    
    if not defender_path:
        if log_callback:
            log_callback("ERROR: Windows Defender not found!", "ERROR")
            log_callback("[ERROR] Pastikan Windows Defender terinstall dengan benar.", "ERROR")
        return False
    
    if log_callback:
        log_callback(f"[INFO] Menggunakan: {defender_path}", "INFO")
        log_callback("Defender Engine: Linked", "INFO")
        log_callback("Running Quick Scan...", "INFO")
    
    try:
        result = subprocess.run(
            [defender_path, "-Scan", "-ScanType", "1"],
            capture_output=True,
            text=True,
            check=False,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        if result.returncode == 0:
            if log_callback:
                log_callback("Scan Result: NO THREATS FOUND", "SUCCESS")
        else:
            if log_callback:
                log_callback(f"Scan Result: Code {result.returncode} (Check Security Center)", "WARN")
        
        if log_callback:
            log_callback(">>> SCAN COMPLETE", "HEADER")
        
        return True
    except Exception as e:
        if log_callback:
            log_callback(f"Scan Error: {str(e)}", "ERROR")
            log_callback(">>> SCAN COMPLETE", "HEADER")
        return False
