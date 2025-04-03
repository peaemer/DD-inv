import importlib
import tkinter as tk
from tkinter import font
from typing import Tuple, Any

from includes.util import Preprocessor
from includes.util import Paths
from includes.util.ConfigManager import ConfigManager, Configuration
from includes.util.Logging import Logger


logger: Logger = Logger('main')

config_manager:ConfigManager = ConfigManager(Paths.app_files_path_string + r'\DD-inv.config', ['Fenster Aufloesung', 'Regeln fuer neue Passwoerter', 'Suchleiste', 'Admin Debug Mode', 'Zoom indicator'])


class DdInv(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Inventartool")
        self.configure(background="white")
        self.state("zoomed")

        def get_zoom_parameter():
            config: Configuration = config_manager.generate_configuration('Zoom indicator')
            try:
                saved_value = config.read_parameter('Zoom indicator', generate_if_missing=True, gen_initial_value='1')
                logger.debug(f"Zoom parameter got from JSON-File {saved_value}")  # Debug-Ausgabe
                # Falls der geladene Wert 0.0 oder ungültig ist, auf den Standardwert 1.0 setzen
                zoom_value = float(saved_value) if saved_value and float(saved_value) > 0 else 1.0
                return zoom_value
            except KeyError as e:
                logger.error(f"Zoom KeyError: {e}")
                return 1.0  # Standardwert

        # Standard-Schriftgröße und Zoom-Faktor
        self.default_font_size = 16
        self.zoom_factor = get_zoom_parameter()
        logger.debug(f"Zoom factor initialized with: {self.zoom_factor}")
        self.custom_font = font.Font(family="Arial", size=self.default_font_size)

        # Set window dimensions and icon
        def load_resolution() -> Tuple[int, int]:
            """
            Lädt die gespeicherte Auflösung aus der JSON-Datei.
            """
            size:Configuration = config_manager.generate_configuration('Fenster Aufloesung')
            return (
                int(size.read_parameter('breite', generate_if_missing=True, gen_initial_value='1080')),
                int(size.read_parameter('hoehe', generate_if_missing=True, gen_initial_value='1920'))
            )

        screen_height, screen_width = load_resolution()
        self.geometry(f'{screen_width}x{screen_height}+0+0')

        self.iconbitmap(Paths.assets_path("srhIcon.ico"))


        # Container für Frames erstellen
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        logger.debug("MainFrame successfully created")  # Debug

        self.frames:dict = {}

        # Login-Fenster zuerst laden
        from includes.gui.pages.LoginPage import LoginPage
        self.show_frame(LoginPage)

    def update_zoom(self, value):
        """Aktualisiert die Zoomstufe basierend auf dem Wert des Schiebereglers."""
        self.zoom_factor = float(value)  # Setze den neuen Zoom-Faktor
        logger.debug(f"Neue Zoom-Stufe: {self.zoom_factor}")  # Debug-Ausgabe
        new_font_size = int(self.default_font_size * self.zoom_factor)  # Berechne die neue Schriftgröße
        self.custom_font.configure(size=new_font_size)  # Ändere die Schriftgröße

        # Alle Frames aktualisieren
        for frame in self.frames.values():
            self.update_frame_widgets(frame)

    def update_frame_widgets(self, frame):
        """
            Passt alle Widgets im gegebenen Frame an die aktuelle Zoomstufe an.
        """
        for widget in frame.winfo_children():
            # Überprüfe, ob das Widget eines der Ziel-Widgets ist (Label, Button, Entry, Text)
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Text)):
                widget.configure(font=self.custom_font)  # Setze die Schriftart des Widgets

        # Aktualisiere das Layout und die Widgets im Frame, um sicherzustellen, dass alle Änderungen angewendet werden
        frame.update_idletasks()  # Stellt sicher, dass Layout und Widgets neu berechnet werden

    def show_frame(self, page_type:type) -> Any:
        #if not issubclass(page_type, IPage):
        #    raise RuntimeError(f"Page type {page_type} is not a subclass of IPage")

        if page_type not in self.frames.keys():
            logger.debug(f"{page_type.__name__} is being dynamically created.")  # Debug

            page_instance = page_type(self.container, self)  # Frame erstellen
            self.frames[page_type] = page_instance  # Zu Frames hinzufügen
            page_instance.grid(row=0, column=0, sticky="nsew")  # Layout konfigurieren

        page_instance = self.frames[page_type]  # Existierenden Frame verwenden
        from includes.gui.pages.IPage import IPage
        if issubclass(page_type, IPage):
            logger.debug(f'page type {page_instance.__class__.__name__} is a subclass of IPage')
            page_instance.tkraise()  # Frame sichtbar machen

            # Widgets im Frame aktualisieren
            self.update_frame_widgets(page_instance)

            if hasattr(page_instance, 'on_load') and callable(page_instance.on_load):
                logger.debug(f"on_load is being called for {page_type.__name__}")  # Debug
                page_instance.on_load()
        return page_instance

if __name__ == "__main__":
    Preprocessor.run()
    app = DdInv()
    app.mainloop()
