import psutil

def check_cpu():
    """ Misst die CPU_Auslastung und gibt den Prozentwert zurück. """
    return psutil.cpu_percent(interval=1)
