import tkinter as tk
import customtkinter as ctk
import cache
from ._styles import *

class MessageBoxStore:
    msg_box = None
    msg_frame = None

def customMessageBox(parent, title, message, **buttons):
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
    window_width = 460
    window_height = 100

    # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    msg_box.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    msg_box.resizable(False, False)

    #try:
    #    msg_box.iconbitmap("includes/assets/srhIcon.ico")
    #except Exception as e:
    #    logger.debug(f"Error while loading icon {e}")

    cache.msgbox = msg_box

    msg_frame = tk.Frame(msg_box, background="white")
    MessageBoxStore.msg_frame = msg_frame

    msg_frame.grid(row=0,
                  column=0,
                  columnspan=1,
                  sticky="nesw")

    msg = ctk.CTkLabel(msg_frame,
                       text=message,
                       text_color="black",
                       font=("Arial", 20),
                       justify="center")
    msg.pack(side="left")
    #msg.grid(row=0, column=0, padx=15, pady=5, sticky="nesw", columnspan=2)

    btn_int = 0
    for i, button in enumerate(buttons):
        button = buttons[button][i]
        #button.grid(row=1, column=btn_int, padx=0, pady=10)
        button.pack(side="left")
        msg_frame.grid_columnconfigure(btn_int, weight=1)
        btn_int += 1

    cancel = ctk.CTkButton(msg_frame,
                           text="Abbrechen",
                           border_width=0,
                           fg_color=srhGrey,
                           cursor="hand2",
                           text_color="black",
                           command=msg_box.destroy)
    #cancel.grid(row=1, column=btn_int+1, padx=0, pady=10)
    cancel.pack(side="right")

    msg_frame.grid_rowconfigure(0, weight=0)
    msg_frame.grid_rowconfigure(1, weight=0)
    msg_frame.grid_columnconfigure(btn_int+1, weight=1)