import customtkinter as ctk
from typing import Tuple
from tkinter import font
import logging

from includes.util.ConfigManager import ConfigManager, Configuration
from includes.pages import (LogInWindow)

config_manager:ConfigManager = ConfigManager('./DD-inv.config')
logger = logging.getLogger(__name__)

class ddINV(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Inventartool")
        self.geometry("1920x1080")  # Standardgröße für CTk-Fenster
        self.attributes("-topmost", False)
        self._state_before_windows_set_titlebar_color = 'zoomed'  # die Anwendung im Vollbild starten

        # Standard-Schriftgröße und Zoom-Faktor
        self.default_font_size = 16
        self.zoom_factor = 3.0
        self.custom_font = font.Font(family="Arial", size=self.default_font_size)

        # Fenster-Auflösung laden
        def load_resolution() -> Tuple[int, int]:
            """
            Lädt die gespeicherte Auflösung aus der JSON-Datei.
            """
            size: Configuration = config_manager.generate_configuration('Fenster Aufloesung')
            return (
                size.read_parameter('breite') if size.read_parameter('breite') != 'null' else 1080,
                size.read_parameter('hoehe') if size.read_parameter('hoehe') != 'null' else 1920
            )

        screen_height, screen_width = load_resolution()
        print(screen_width, screen_height)
        self.geometry(f'{screen_width}x{screen_height}+0+0')

        from includes.pages._avatarManager import resource_path
        self.iconbitmap(resource_path("./includes/assets/srhIcon.ico"))

        # Container für Frames erstellen
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        logger.debug("MainFrame successfully created")

        self.frames = {}

        # Login-Fenster zuerst laden
        self.show_frame(LogInWindow)

    def update_zoom(self, value):
        """Aktualisiert die Zoomstufe basierend auf dem Wert des Schiebereglers."""
        self.zoom_factor = float(value)
        new_font_size = int(self.default_font_size * self.zoom_factor)
        self.custom_font.configure(size=new_font_size)

        # Alle Frames aktualisieren
        for frame in self.frames.values():
            self.update_frame_widgets(frame)

    def update_frame_widgets(self, frame):
        """Passt alle Widgets im gegebenen Frame an die aktuelle Zoomstufe an."""
        for widget in frame.winfo_children():
            if isinstance(widget, (ctk.CTkLabel, ctk.CTkButton, ctk.CTkEntry, ctk.CTkTextbox)):
                widget.configure(font=self.custom_font)

    def show_frame(self, cont):
        if cont not in self.frames:
            logger.debug(f"{cont.__name__} is being dynamically created.")
            frame = cont(self.container, self)  # Frame erstellen
            self.frames[cont] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        frame = self.frames[cont]

        if isinstance(frame, ctk.CTkFrame):
            frame.tkraise()

            # Widgets im Frame aktualisieren
            self.update_frame_widgets(frame)

            if hasattr(frame, 'on_load') and callable(frame.on_load):
                logger.debug(f"on_load is being called for {cont.__name__}")
                frame.on_load()

if __name__ == "__main__":
    app = ddINV()
    app.mainloop()
