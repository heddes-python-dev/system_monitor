from tkinter import messagebox
import logging
import config

def zeige_popup(titel, nachricht, parent=None):
    """Zeigt ein grafisches Pop-up an, falls in der config.py aktiviert."""
    # Prüfen, ob Pop-ups laut Konfiguration überhaupt erlaubt sind
    if not getattr(config, 'POPUP_AKTIVIERT', False):
        return
        
    try:
        messagebox.showwarning(titel, nachricht, parent=parent)
    except Exception as e:
        logging.error(f"Konnte kein Pop-up anzeigen: {e}", exc_info=True)