"""
Program Uninstaller Module
Get installed programs dari Windows Registry dan uninstall functionality
"""

import winreg
import subprocess
import os
from pathlib import Path


def get_installed_programs():
    """
    Get list installed programs dari Windows Registry
    
    Returns:
        list: List of dicts dengan program info
            [{
                'name': str,
                'publisher': str,
                'version': str,
                'install_date': str,
                'install_location': str,
                'uninstall_string': str,
                'size': str
            }, ...]
    """
    programs = []
    
    # Registry paths to check
    registry_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]
    
    for hkey, path in registry_paths:
        try:
            registry_key = winreg.OpenKey(hkey, path)
            
            # Iterate through all subkeys
            for i in range(winreg.QueryInfoKey(registry_key)[0]):
                try:
                    subkey_name = winreg.EnumKey(registry_key, i)
                    subkey = winreg.OpenKey(registry_key, subkey_name)
                    
                    # Read program info
                    try:
                        name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        
                        # Skip if no name or is Windows update
                        if not name or "KB" in name or "Update for" in name:
                            continue
                        
                        program = {
                            'name': name,
                            'publisher': '',
                            'version': '',
                            'install_date': '',
                            'install_location': '',
                            'uninstall_string': '',
                            'size': ''
                        }
                        
                        # Try to get additional info
                        try:
                            program['publisher'] = winreg.QueryValueEx(subkey, "Publisher")[0]
                        except:
                            pass
                        
                        try:
                            program['version'] = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                        except:
                            pass
                        
                        try:
                            program['install_date'] = winreg.QueryValueEx(subkey, "InstallDate")[0]
                        except:
                            pass
                        
                        try:
                            program['install_location'] = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                        except:
                            pass
                        
                        try:
                            program['uninstall_string'] = winreg.QueryValueEx(subkey, "UninstallString")[0]
                        except:
                            pass
                        
                        try:
                            size_kb = int(winreg.QueryValueEx(subkey, "EstimatedSize")[0])
                            size_mb = size_kb / 1024
                            if size_mb > 1024:
                                program['size'] = f"{size_mb/1024:.1f} GB"
                            else:
                                program['size'] = f"{size_mb:.1f} MB"
                        except:
                            pass
                        
                        # Only add if has uninstall string
                        if program['uninstall_string']:
                            programs.append(program)
                    
                    except OSError:
                        pass
                    
                    winreg.CloseKey(subkey)
                
                except OSError:
                    continue
            
            winreg.CloseKey(registry_key)
        
        except OSError:
            continue
    
    # Remove duplicates (same name)
    seen = set()
    unique_programs = []
    for prog in programs:
        if prog['name'] not in seen:
            seen.add(prog['name'])
            unique_programs.append(prog)
    
    # Sort by name
    unique_programs.sort(key=lambda x: x['name'].lower())
    
    return unique_programs


def uninstall_program(program_info, log_callback=None):
    """
    Uninstall program menggunakan uninstall string dari registry
    
    Args:
        program_info: Dict dengan program info (must have uninstall_string)
        log_callback: Callback function untuk logging
        
    Returns:
        bool: True jika berhasil
    """
    uninstall_string = program_info.get('uninstall_string', '')
    
    if not uninstall_string:
        if log_callback:
            log_callback(f"No uninstall string found for {program_info['name']}", "ERROR")
        return False
    
    if log_callback:
        log_callback(f"\n>>> UNINSTALLING: {program_info['name']}", "HEADER")
        log_callback(f"Publisher: {program_info.get('publisher', 'Unknown')}", "INFO")
        log_callback(f"Version: {program_info.get('version', 'Unknown')}", "INFO")
        log_callback(f"Executing uninstall command...", "INFO")
    
    try:
        # Run uninstall string
        # Some uninstall strings include quotes, handle that
        if uninstall_string.startswith('"'):
            # Extract exe path and arguments
            parts = uninstall_string.split('"')
            exe_path = parts[1] if len(parts) > 1 else uninstall_string
            args = parts[2].strip() if len(parts) > 2 else ""
            
            if args:
                subprocess.run(f'"{exe_path}" {args}', shell=True, check=False)
            else:
                subprocess.run(exe_path, shell=True, check=False)
        else:
            subprocess.run(uninstall_string, shell=True, check=False)
        
        if log_callback:
            log_callback("Uninstall command executed successfully", "SUCCESS")
            log_callback("Note: Some programs may require manual confirmation", "WARN")
        
        return True
    
    except Exception as e:
        if log_callback:
            log_callback(f"Error during uninstall: {str(e)}", "ERROR")
        return False


def force_uninstall(program_info, log_callback=None):
    """
    Force uninstall program - delete registry entries and leftover files
    
    ⚠️ DANGEROUS OPERATION - Use with caution!
    
    Args:
        program_info: Dict dengan program info
        log_callback: Callback function untuk logging
        
    Returns:
        bool: True jika berhasil
    """
    if log_callback:
        log_callback(f"\n>>> FORCE UNINSTALLING: {program_info['name']}", "HEADER")
        log_callback("⚠️ WARNING: This will forcefully remove program entries and files!", "WARN")
    
    success = True
    
    # TODO: Implement registry deletion
    # TODO: Implement leftover files deletion
    # TODO: Create backup before deletion
    
    if log_callback:
        log_callback("Force uninstall feature coming soon...", "WARN")
        log_callback("For now, use standard uninstall", "INFO")
    
    return success
