# System Monitor

Ein modularer Systemmonitor fuer Linux und Windows. Die Anwendung ueberwacht CPU, Arbeitsspeicher, Festplattenbelegung und CPU-Temperatur und zeigt die aktuellen Werte in einer kleinen Tkinter-GUI an.

Bei anhaltender Ueberschreitung eines Schwellenwerts werden die wichtigsten Prozesse ermittelt und eine Warnung ins Log geschrieben. Optional koennen Warnungen als Popup angezeigt werden.

## Funktionen

- CPU-Auslastung mit konfigurierbarem Schwellenwert
- RAM-Auslastung
- Belegung des Systemlaufwerks
- CPU-Temperatur, sofern Sensorwerte verfuegbar sind
- Top-Prozesse nach CPU- und RAM-Verbrauch
- Thread-sichere Kommunikation zwischen Monitoring und GUI
- Entprellte Warnungen gegen einzelne kurze Lastspitzen
- Rotierendes Logfile mit drei Sicherungsdateien
- PyInstaller-Spezifikation fuer eine eigenstaendige Anwendung

## Architektur

```text
main.py
├── cpu_module.py       CPU-Messung
├── ram_module.py       RAM-Messung
├── disk_module.py      Festplattenbelegung
├── temp_module.py      Temperatursensoren
├── process_module.py   Top-Prozesse
├── gui_module.py       Tkinter-Oberflaeche
├── popup_module.py     Optionale Warnfenster
└── config.py           Einstellungen und Logging
```

Der Monitoring-Worker misst die Systemwerte im Hintergrund. Ergebnisse werden ueber eine Queue an den Tkinter-Hauptthread uebergeben. Dadurch bleiben GUI-Zugriffe thread-sicher.

## Voraussetzungen

- Python 3.10 oder neuer
- `psutil`
- Tkinter

Unter Debian/Ubuntu kann Tkinter bei Bedarf installiert werden:

```bash
sudo apt install python3-tk
```

Python-Abhaengigkeit installieren:

```bash
python3 -m pip install psutil
```

## Start

Linux und Windows mit Python:

```bash
cd .../system_monitor
python3 main.py
```

Unter Windows kann alternativ `python main.py` verwendet werden. Als eigenstaendige Anwendung:

- Linux: `dist/main`
- Windows: `dist/main.exe`

Der Build muss auf dem jeweiligen Zielsystem erfolgen:

```bash
python3 -m pip install pyinstaller
python3 -m PyInstaller --clean --noconfirm main.spec
```

Unter Windows PowerShell lauten die entsprechenden Befehle `python -m pip install pyinstaller` und `python -m PyInstaller --clean --noconfirm main.spec`. Die fertige EXE liegt danach in `dist/`.

Das Fenster kann waehrend der Ueberwachung geoeffnet bleiben oder minimiert werden. Zum Beenden das Fenster schliessen oder den Beenden-Button verwenden.

## Konfiguration

Die Einstellungen stehen in [config.py](config.py):

| Einstellung | Bedeutung | Aktueller Wert |
|---|---|---:|
| `INTERVALL_SEKUNDEN` | Zeit zwischen Messungen | `60` |
| `CPU_SCHWELLENWERT` | CPU-Warnschwelle in Prozent | `70` |
| `RAM_SCHWELLENWERT` | RAM-Warnschwelle in Prozent | `85` |
| `DISK_SCHWELLENWERT` | Warnschwelle fuer das Systemlaufwerk | `85` |
| `TEMP_SCHWELLENWERT` | Temperatur-Warnschwelle in Grad Celsius | `75` |
| `WARNUNG_NACH_MESSUNGEN` | Benoetigte aufeinanderfolgende Warnmessungen | `2` |
| `POPUP_AKTIVIERT` | Optionale Warnfenster | `False` |

Die CPU-Messung selbst verwendet ein einsekundiges Sampling. Daher dauert ein kompletter Messzyklus etwas laenger als nur das konfigurierte Intervall.

## Logging

Die Anwendung schreibt nach `system_monitor.log`. Die Logdatei wird bei einer Groesse von 1 MB rotiert; bis zu drei Backups bleiben erhalten.

Beim Start als EXE liegt die Logdatei im `dist/`-Verzeichnis neben der Anwendung.

Das Log enthaelt:

- Messwerte und Warnungen
- PID, Name und Verbrauch der Top-Prozesse
- Fehler inklusive Stacktrace
- Start und sauberes Herunterfahren

## Build mit PyInstaller

Die mitgelieferte [main.spec](main.spec) kann fuer einen Build verwendet werden:

```bash
python3 -m pip install pyinstaller
pyinstaller main.spec
```

Das Ergebnis liegt anschliessend im Verzeichnis `dist/`.

## Bekannte Grenzen

- Unter Linux haengt die Temperaturanzeige von verfuegbaren Sensoren und psutil-Unterstuetzung ab.
- Es wird das Systemlaufwerk ueberwacht, nicht automatisch jede Partition.
- Prozess-CPU-Werte werden in einem kurzen separaten Sampling ermittelt und sind daher eine Momentaufnahme.
- Die GUI ist bewusst klein gehalten und bietet keine historische Diagrammansicht.

## Lizenz

Dieses Projekt enthaelt derzeit keine separate Lizenzdatei.
