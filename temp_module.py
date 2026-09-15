import sys
import psutil
import logging

def check_temp():
    """Ermittelt die höchste CPU-Temperatur (hauptsächlich für Linux)."""
    if not sys.platform.startswith('linux'):
        return None
        
    try:
        temps = psutil.sensors_temperatures()
        all_temps = [
            sensor.current
            for sensors in temps.values()
            for sensor in sensors
            if sensor.current is not None
        ]
        return max(all_temps) if all_temps else None
    except Exception as e:
        logging.error(f"Fehler beim Abrufen der Temperaturdaten: {e}")
        
    return None