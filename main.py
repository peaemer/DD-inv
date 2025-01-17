import json
import tkinter as tk
import json
from tkinter import font
from includes.util.Logging import Logger
from includes.pages import (logInWindow)


logger: Logger = Logger('main')


class ddINV(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Inventartool")
        self.configure(background="white")
        self.state("zoomed")

        # Standard-Schriftgröße und Zoom-Faktor
        self.default_font_size = 12
        self.zoom_factor = 1.0
        self.custom_font = font.Font(family="Arial", size=self.default_font_size)

        # Set window dimensions and icon
        def load_resolution():
            """
            Lädt die gespeicherte Auflösung aus der JSON-Datei.
            """
            try:
                with open('config.json', 'r') as openfile:
                    # Reading from json file
                    json_object:dict[str,dict[str,str]] = json.load(openfile)
                    print(json_object)
                height = json_object['fenster groesse']["hoehe"]
                width = json_object['fenster groesse']["breite"]
                return height, width
            except (FileNotFoundError, json.JSONDecodeError):
                return 1920, 1080  # Standard-Auflösung zurückgeben, falls nichts gefunden wird

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
        self.show_frame(logInWindow)

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
