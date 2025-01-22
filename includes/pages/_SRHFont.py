import ctypes
import os


def load_font(font_path):
    """
    Registriert eine .ttf-Schriftart temporär für die Verwendung in Tkinter.
    Funktioniert nur auf Windows.
    """
    if os.name == 'nt':  # Windows
        FR_PRIVATE = 0x10
        FR_NOT_ENUM = 0x20
        # Temporär die Schriftart laden
        success = ctypes.windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)
        if success == 0:
            raise RuntimeError(f"Fehler beim Laden der Schriftart: {font_path_headline} & {font_path_Text}")

# Pfad zur .ttf-Datei
font_path_headline = "assets/SRH_Schrift_Headline/App/SRHHeadline_A_Bd.ttf"
font_path_Text = "assets/SRH_Schrift_Text/App/SRHText_A_Bd.ttf"
    
# Temporär die Schriftart registrieren
load_font(font_path_Text)
load_font(font_path_headline)

# Setzen einer Variable für die Customfont
SRHHeadline = font_path_headline
SRHText = font_path_Text
