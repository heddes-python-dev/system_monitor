import logging
from logging.handlers import RotatingFileHandler

# Zentrale Einstellungen (direkt auf Modulebene, damit alle Funktionen sie nutzen können)
LOG_DATEI = "system_monitor.log"
INTERVALL_SEKUNDEN = 60
CPU_SCHWELLENWERT = 70
RAM_SCHWELLENWERT = 85
DISK_SCHWELLENWERT = 85
TEMP_SCHWELLENWERT = 75  # Temperatur-Schwellenwert in °C
WARNUNG_NACH_MESSUNGEN = 2

POPUP_AKTIVIERT = False  # Popup-Benachrichtigungen aktivieren/deaktivieren

def setup_logging():
    """Konfiguriert das rotierende Logging zentral."""
    logger = logging.getLogger()
    if any(getattr(handler, "system_monitor_handler", False)
           for handler in logger.handlers):
        return

    log_handler = RotatingFileHandler(
        LOG_DATEI, 
        maxBytes=1 * 1024 * 1024,  # 1 Megabyte
        backupCount=3,             # 3 Backups
        encoding="utf-8"
    )
    log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.setLevel(logging.INFO)
    log_handler.system_monitor_handler = True
    logger.addHandler(log_handler)