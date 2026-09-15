import sys
import psutil

def check_disk():
    """Ermittelt die Festplattennutzung plattformunabhängig (Windows/Linux)."""
    if sys.platform.startswith('win'):
        disk_path = 'C:\\'  # Windows-Standardlaufwerk
    else:
        disk_path = '/'     # Linux/Unix-Wurzelverzeichnis
        
    return psutil.disk_usage(disk_path).percent