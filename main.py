import json
import tkinter as tk
import json
from tkinter import font
from typing import Tuple

from includes.util.ConfigManager import ConfigManager, Configuration
from includes.util.Logging import Logger
from includes.pages import (LogInWindow)

logger: Logger = Logger('main')
config_manager:ConfigManager = ConfigManager('./DD-inv.config')


class ddINV(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Inventartool")
        self.configure(background="white")
        self.state("zoomed")

        def get_zoom_parameter():
            config: Configuration = config_manager.generate_configuration('Zoom indicator')
            try:
                saved_value = config.read_parameter('Zoom indicator')
                logger.debug(f"Zoom: {saved_value}")
                return saved_value

            except KeyError as e:
                logger.error(f"Zoom: {e}")
                return 1.0

        # Standard-Schriftgröße und Zoom-Faktor
        self.default_font_size = 12
        self.zoom_factor = get_zoom_parameter()
        self.custom_font = font.Font(family="Arial", size=self.default_font_size)

        # Set window dimensions and icon
        def load_resolution() -> Tuple[int, int]:
            """
            Lädt die gespeicherte Auflösung aus der JSON-Datei.
            """

            size:Configuration = config_manager.generate_configuration('Fenster Aufloesung')
            return (
                size.read_parameter('breite') if size.read_parameter('breite') != 'null' else 1080,
                size.read_parameter('hoehe') if size.read_parameter('hoehe')  != 'null' else 1920
            )

        screen_height, screen_width = load_resolution()  # Variablen anders benennen
        print(screen_width, screen_height)
        self.geometry(f'{screen_width}x{screen_height}+0+0')  # Korrigierter Aufruf
        from includes.pages._avatarManager import resource_path
        self.iconbitmap(resource_path("./includes/assets/srhIcon.ico"))

        from includes.pages._avatarManager import resource_path
        self.iconbitmap(resource_path("./includes/assets/srhIcon.ico"))

        # Container für Frames erstellen
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        logger.debug("MainFrame successfully created")  # Debug

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
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Text)):
                widget.configure(font=self.custom_font)

    def show_frame(self, cont):
        if cont not in self.frames:
            logger.debug(f"{cont.__name__} is being dynamically created.")  # Debug
            frame = cont(self.container, self)  # Frame erstellen
            self.frames[cont] = frame  # Zu Frames hinzufügen
            frame.grid(row=0, column=0, sticky="nsew")  # Layout konfigurieren

        frame = self.frames[cont]  # Existierenden Frame verwenden

        if isinstance(frame, tk.Frame):
            frame.tkraise()  # Frame sichtbar machen

            # Widgets im Frame aktualisieren
            self.update_frame_widgets(frame)

            if hasattr(frame, 'on_load') and callable(frame.on_load):
                logger.debug(f"on_load is being called for {cont.__name__}")  # Debug
                frame.on_load()


if __name__ == "__main__":
    app = ddINV()
    app.mainloop()
