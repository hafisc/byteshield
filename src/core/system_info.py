"""
System Information Module
Logic untuk mengambil info sistem Windows
"""

import platform
import shutil


def get_system_info():
    """
    Mengambil informasi sistem Windows
    
    Returns:
        dict: Dictionary dengan key os, cpu, ram, disk
    """
    info = {}
    
    try:
        # OS Info
        info['os'] = f"{platform.system()} {platform.release()}"
        
        # CPU Info
        try:
            import wmi
            c = wmi.WMI()
            for processor in c.Win32_Processor():
                info['cpu'] = processor.Name.strip()
                break
        except:
            info['cpu'] = platform.processor() or "Unknown CPU"
        
        # RAM Info
        try:
            import psutil
            ram = psutil.virtual_memory()
            total_gb = ram.total / (1024**3)
            used_gb = ram.used / (1024**3)
            info['ram'] = f"{used_gb:.1f}GB / {total_gb:.1f}GB ({ram.percent}%)"
        except:
            try:
                import wmi
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
                total, used, free = shutil.disk_usage("C:")
                free_gb = free / (1024**3)
                total_gb = total / (1024**3)
                info['disk'] = f"{free_gb:.1f}GB free / {total_gb:.1f}GB"
            except:
                info['disk'] = "Unknown"
    except Exception as e:
        pass
    
    return info
