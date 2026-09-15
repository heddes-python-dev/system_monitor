import tkinter as tk
from tkinter import ttk

def starte_gui(on_closing_callback):
    """Startet das Hauptfenster der Anwendung mit Live-Metriken."""
    root = tk.Tk()
    root.title("Modularer System Monitor")
    root.geometry("450x330")
    root.resizable(False, False)

    # Titel
    label_titel = ttk.Label(root, text="System Monitor aktiv", font=("Arial", 14, "bold"))
    label_titel.pack(pady=15)

    # Rahmen für Live-Werte
    frame_metrics = ttk.LabelFrame(root, text=" Live-Werte ", padding=12)
    frame_metrics.pack(fill="x", padx=20, pady=5)

    lbl_cpu = ttk.Label(frame_metrics, text="CPU-Auslastung: -- %", font=("Arial", 10))
    lbl_cpu.pack(anchor="w", pady=3)

    lbl_ram = ttk.Label(frame_metrics, text="RAM-Auslastung: -- %", font=("Arial", 10))
    lbl_ram.pack(anchor="w", pady=3)

    lbl_disk = ttk.Label(frame_metrics, text="Festplattennutzung: -- %", font=("Arial", 10))
    lbl_disk.pack(anchor="w", pady=3)

    lbl_temp = ttk.Label(frame_metrics, text="CPU-Temperatur: -- °C", font=("Arial", 10))
    lbl_temp.pack(anchor="w", pady=3)

    # Beenden-Button
    btn_beenden = ttk.Button(root, text="Programm beenden", command=lambda: on_closing_callback(root))
    btn_beenden.pack(pady=15)

    # Schließen-Event abfangen
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing_callback(root))

    # Wir geben das Fenster und ein Dictionary mit den Labels zurück, damit main.py sie füttern kann
    labels = {
        'cpu': lbl_cpu,
        'ram': lbl_ram,
        'disk': lbl_disk,
        'temp': lbl_temp
    }
    
    return root, labels