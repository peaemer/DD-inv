import tkinter as tk
import threading
from tkinter import mainloop
import customtkinter as ctk
import includes
from includes.pages._styles import *

from includes.pages import (logInWindow,
                            mainPage,
                            userDetailsWindow,
                            detailsWindow,
                            roomDetailsWindow,
                            customMessageBoxDelete,
                            adminRoomWindow,
                            adminUserWindow,
                            adminRoleWindow)


class ddINV(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Inventartool")
        self.configure(background="white")
        self.state("zoomed")

        # Set window dimensions and icon
        self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0')
        self.minsize(1280, 720)
        self.maxsize(1920, 1080)
        from includes.pages._avatarManager import resource_path
        self.iconbitmap(resource_path("./includes/assets/srhIcon.ico"))

        # Create a container for frames
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: MainFrame successfully created") # Debug

        self.frames = {}

        # Load the login window first
        self.show_frame(logInWindow)

    def show_frame(self, cont):
        if cont not in self.frames:
            print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: {cont.__name__} is being dynamically created.") # Debug
            frame = cont(self.container, self)  # Frame erstellen
            self.frames[cont] = frame  # Zu Frames hinzufügen
            frame.grid(row=0, column=0, sticky="nsew")  # Layout konfigurieren

        frame = self.frames[cont]  # Existierenden Frame verwenden

        if isinstance(frame, tk.Frame):
            frame.tkraise()  # Frame sichtbar machen

            if hasattr(frame, 'on_load') and callable(frame.on_load):
                print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: on_load is being called for {cont.__name__}")  # Debug
                frame.on_load()

if __name__ == "__main__":
    app = ddINV()
    app.mainloop()