import logging
import threading
import sys
import queue
import config
from cpu_module import check_cpu
from ram_module import check_ram
from disk_module import check_disk
from temp_module import check_temp
from process_module import get_top_processes
from popup_module import zeige_popup
from gui_module import starte_gui

config.setup_logging()

stop_event = threading.Event()
popup_queue = queue.Queue()
status_queue = queue.Queue(maxsize=1)


def publish_status(metrics):
    """Hält ausschließlich den aktuellsten Status für die GUI bereit."""
    try:
        status_queue.get_nowait()
        status_queue.task_done()
    except queue.Empty:
        pass

    try:
        status_queue.put_nowait(metrics)
    except queue.Full:
        pass

def monitor_loop():
    """Die Überwachungsschleife im Hintergrund."""
    logging.info("Hintergrund-Überwachung gestartet.")
    aufeinanderfolgende_warnungen = 0
    warnung_aktiv = False
    
    while not stop_event.is_set():
        try:
            aktive_warnungen = []

            cpu_usage = check_cpu()
            ram_usage = check_ram()
            disk_usage = check_disk()
            max_temp = check_temp()

            publish_status({
                'cpu': cpu_usage,
                'ram': ram_usage,
                'disk': disk_usage,
                'temp': max_temp
            })

            # Schwellenwerte prüfen
            if cpu_usage > config.CPU_SCHWELLENWERT:
                aktive_warnungen.append(f"CPU-Auslastung ({cpu_usage}%)")
            if ram_usage > config.RAM_SCHWELLENWERT:
                aktive_warnungen.append(f"RAM-Auslastung ({ram_usage}%)")
            if disk_usage > config.DISK_SCHWELLENWERT:
                aktive_warnungen.append(f"Festplattennutzung ({disk_usage}%)")
            if max_temp is not None and max_temp > config.TEMP_SCHWELLENWERT:
                aktive_warnungen.append(f"CPU-Temperatur ({max_temp}°C)")

            if aktive_warnungen:
                aufeinanderfolgende_warnungen += 1
            else:
                aufeinanderfolgende_warnungen = 0
                warnung_aktiv = False

            if (aktive_warnungen
                    and aufeinanderfolgende_warnungen >= config.WARNUNG_NACH_MESSUNGEN
                    and not warnung_aktiv):
                warnung_aktiv = True
                ausloeser_text = ", ".join(aktive_warnungen)
                logging.warning(f"WARNUNG ausgelöst durch: {ausloeser_text}")
                
                top_cpu, top_ram = get_top_processes(limit=2)
                logging.warning("--- Top CPU-Verbraucher ---")
                for p in top_cpu:
                    logging.warning(
                        f"  -> Prozess: {p['name']} (PID: {p['pid']}, "
                        f"{p['cpu_percent']:.1f}% CPU)"
                    )

                logging.warning("--- Top RAM-Verbraucher ---")
                for p in top_ram:
                    logging.warning(
                        f"  -> Prozess: {p['name']} (PID: {p['pid']}, "
                        f"{p['ram_percent']:.1f}% RAM)"
                    )

                popup_queue.put(("System-Monitor Alarm!", f"Achtung!\n{ausloeser_text}\n\nDetails stehen im Log."))
            elif not aktive_warnungen:
                logging.info("Systemauslastung im normalen Bereich.")

        except Exception as e:
            logging.error(f"Unerwarteter Fehler im Überwachungsprozess: {e}", exc_info=True)

        stop_event.wait(config.INTERVALL_SEKUNDEN)

    logging.info("Hintergrund-Überwachung wurde beendet.")

def process_queues(root, labels):
    """Verarbeitet sowohl Pop-ups als auch Live-Metriken absolut thread-sicher im Hauptthread."""
    
    # 1. Pop-ups prüfen
    try:
        while True:
            titel, nachricht = popup_queue.get_nowait()
            zeige_popup(titel, nachricht, parent=root)
            popup_queue.task_done()
    except queue.Empty:
        pass

    # 2. Live-Werte für die GUI abholen
    try:
        while True:
            metrics = status_queue.get_nowait()
            labels['cpu'].config(text=f"CPU-Auslastung: {metrics['cpu']}%")
            labels['ram'].config(text=f"RAM-Auslastung: {metrics['ram']}%")
            labels['disk'].config(text=f"Festplattennutzung: {metrics['disk']}%")
            
            temp_text = f"{metrics['temp']} °C" if metrics['temp'] is not None else "Nicht verfügbar"
            labels['temp'].config(text=f"CPU-Temperatur: {temp_text}")
            
            status_queue.task_done()
    except queue.Empty:
        pass
    
    # Wiederholen, solange das Programm läuft
    if not stop_event.is_set():
        root.after(100, lambda: process_queues(root, labels))

def on_closing(root):
    logging.info("Fenster wird geschlossen. Fahre Programm herunter...")
    stop_event.set()
    root.destroy()

if __name__ == "__main__":
    logging.info("System-Monitor mit Live-GUI wird gestartet.")

    # 1. GUI-Fenster initialisieren und Labels empfangen
    root, labels = starte_gui(on_closing)

    # 2. Überwachung im Hintergrund-Thread starten
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()

    # 3. Queue-Verarbeitung im Hauptthread starten
    root.after(100, lambda: process_queues(root, labels))

    # 4. Tkinter-Hauptschleife starten
    root.mainloop()

    monitor_thread.join(timeout=2)
    
    logging.info("Programm vollständig heruntergefahren.")
    sys.exit(0)