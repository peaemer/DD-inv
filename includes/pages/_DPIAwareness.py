# Richtiges Skalieren der Schrift bei hoeherer Bildschirmaufloesung
# (e.g. FHD, WQHD, UHD, etc. [only for Windows!!])

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
