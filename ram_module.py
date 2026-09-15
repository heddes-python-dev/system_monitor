import psutil

def check_ram():
    """ Misst die RAM-Auslastung und gibt den Prozentwert zurück. """
    return psutil.virtual_memory().percent
