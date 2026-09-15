import psutil
import time
import logging

def get_top_processes(limit=2):
    """
    Ermittelt die Top-Verbraucher für CPU und RAM mit korrektem Sampling.
    Verwendet einen Zwei-Schritte-Ansatz, damit cpu_percent() nicht 0.0 liefert.
    """
    procs = []
    
    # 1. Schritt: Prozesse einsammeln und Baseline für cpu_percent() initialisieren
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            # Baseline setzen (erster Aufruf gibt meist 0.0 zurück, startet aber den Timer)
            p.cpu_percent(interval=None)
            procs.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Kurze Messpause, damit psutil die Differenz berechnen kann (100 ms reichen völlig)
    time.sleep(0.1)

    process_list = []
    
    # 2. Schritt: Echte Werte einsammeln
    for p in procs:
        try:
            cpu = p.cpu_percent(interval=None)
            ram = p.memory_percent()
            
            process_list.append({
                'pid': p.info['pid'],
                'name': p.info['name'] or 'Unbekannt',
                'cpu_percent': cpu,
                'ram_percent': ram if ram is not None else 0.0
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Nach CPU-Auslastung und RAM sortieren
    top_cpu = sorted(process_list, key=lambda x: x['cpu_percent'], reverse=True)[:limit]
    top_ram = sorted(process_list, key=lambda x: x['ram_percent'], reverse=True)[:limit]

    return top_cpu, top_ram