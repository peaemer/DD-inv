import tkinter

from includes.gui.popupFrames.SettingsPopupFrame import SettingsPopupFrame
from main import DDInv



class PopupFrameSupport(tkinter.Toplevel):
    """
        .
    """

    def __init__(self, parent, controller:DDInv):
        super().__init__(parent)
        self.title("Einstellungen")
        self.configure(background="white")  # Hintergrundfarbe
        self.transient(parent)  # Setzt Hauptfenster in Hintergrund
        self.grab_set()  # Fokus auf Popup
        self.attributes('-topmost', 0)  # Fenster immer im Vordergrund der Anwendung selbst

        # Bildschirmbreite und hoehe ermitteln (fenster mittig auf Bildschirm setzten)
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        window_width, window_height = 850, 600
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.resizable(False, False)  # Fenstergroeße anpassbar

        s = SettingsPopupFrame(self, controller, admin_mode=False)
        s.grid(row=0, column=0, sticky='nsew')