import tkinter as tk
import customtkinter as ctk
from ._styles import *


class customMessageBoxLogin:
    def __init__(self, parent, title, message):
        self.title = title
        self.message = message

        msg_box = tk.Toplevel(parent)
        msg_box.title(title)
        msg_box.transient(parent)  # Popup bleibt im Vordergrund des Hauptfensters
        msg_box.grab_set()  # Blockiere Interaktionen mit dem Hauptfenster
        msg_box.attributes('-topmost', 0)
        msg_box.configure(background="white")

        # Bildschirmbreite und -höhe ermitteln
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        # Fensterbreite und -höhe definieren
        window_width = 350
        window_height = 80

        # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        msg_box.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        msg_box.resizable(False, False)

        try:
            msg_box.iconbitmap("includes/assets/srhIcon.ico")
        except Exception as e:
            print(f"Fehler beim Laden des Icons: {e}")

        #def für die Enterfunktion
        def on_enter_error(event):
            """
            Schließe das Error Fenster beim drücken der Entertaste.
            """
            msg_box.destroy()

        error_msg = tk.Frame(msg_box, background="white")
        error_msg.grid(row=0,
                       column=0,
                       columnspan=1,
                       sticky="nesw")

        msg = ctk.CTkLabel(error_msg,
                           text=message,
                           text_color="black",
                           font=("Arial", 20),
                           justify="center")
        msg.grid(row=1, column=0, padx=15, pady=5, sticky="nesw")

        self.btn_press_destroy = ctk.CTkButton(error_msg,
                                               text="OK",
                                               border_width=0,
                                               fg_color=srhOrange,
                                               command=msg_box.destroy)
        self.btn_press_destroy.grid(row=2, column=0, padx=40, pady=10)

        # Bind die Enter-Taste
        self.btn_press_destroy.bind("<Return>", lambda event: msg_box.destroy())

        error_msg.grid_rowconfigure(0, weight=0)
        error_msg.grid_rowconfigure(1, weight=1)
        error_msg.grid_columnconfigure(0, weight=1)
        error_msg.grid_columnconfigure(1, weight=0)

