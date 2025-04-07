import tkinter as tk
import customtkinter as ctk

from includes.sec_data_info import sqlite3api as sqlapi
from includes.util.Logging import Logger
from includes.gui.styles import *


def add_room_popup(parent):
    """
        Fügt ein Popup-Fenster hinzu, das verwendet wird, um Daten für einen neuen Raum
        einzugeben, einschließlich Raumbezeichnung und Ort. Das Fenster bietet zusätzlich
        Optionen zur Bestätigung oder zum Abbrechen der Eingabe.

        :param parent: Das übergeordnete Fenster, auf dem das Popup-Fenster dargestellt wird.
        :type parent: tkinter.Tk oder tkinter.Frame

        :return: Entweder wird das Popup geschlossen ohne Aktion, oder die Eingaben werden
                 verarbeitet und einem extern definierten Datenbanksystem hinzugefügt.
        :rtype: None
    """
    add_popup = tk.Toplevel(parent)
    add_popup.title("Raum Hinzufügen")
    add_popup.transient(parent)
    add_popup.grab_set()
    add_popup.attributes('-topmost', 0)
    add_popup.configure(background="white")

    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    window_width = 650
    window_height = 650

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    add_popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    add_popup.resizable(False, False)

    try:
        from ._avatarManager import resource_path
        add_popup.iconbitmap(resource_path("includes/assets/srhIcon.ico"))
    except Exception as e:
        Logger('AddRoomPopup').debug(f"Fehler beim Laden des Icons: {e}")

    # Header
    header_frame_add_room_popup = tk.Frame(add_popup, background="#DF4807")
    header_frame_add_room_popup.grid(row=0, column=0, sticky="new")
    header_frame_add_room_popup.grid_columnconfigure(0, weight=1)

    header_label_add_room_popup = tk.Label(header_frame_add_room_popup,
        background="#00699a",
        text="Hinzufügen",
        foreground="white",
        font=("Arial", 40)
    )
    header_label_add_room_popup.grid(row=0, column=0, sticky=tk.NSEW)

    # Input Frame
    input_frame_add_room_popup = tk.Frame(add_popup, background="white")
    input_frame_add_room_popup.grid(row=1, column=0, pady=20, sticky=tk.NSEW)
    input_frame_add_room_popup.grid_columnconfigure(0, weight=1)
    input_frame_add_room_popup.grid_columnconfigure(1, weight=1)
    input_frame_add_room_popup.grid_columnconfigure(2, weight=1)

    #Raum Bezeichnung
    room_label_add_room_popup = tk.Label(input_frame_add_room_popup,
        text="Raum Bezeichnung",
        background="white",
        font=("Arial", size_add_room_popup)
    )
    room_label_add_room_popup.grid(row=0, column=0, padx=10, pady=20, sticky=tk.E)

    room_entry_add_room_popup = ctk.CTkEntry(input_frame_add_room_popup,
        fg_color="#d9d9d9",
        text_color="black",
        border_width=border,
        font=("Arial", size_add_room_popup),
        corner_radius=corner
    )
    room_entry_add_room_popup.grid(row=0, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    #Ort
    location_add_room_popup = tk.Label(input_frame_add_room_popup,
        text="Ort",
        background="white",
        font=("Arial", size_add_room_popup)
    )
    location_add_room_popup.grid(row=1, column=0, padx=10, pady=20, sticky=tk.E)

    location_entry_add_room_popup = ctk.CTkEntry(input_frame_add_room_popup,
        fg_color="#d9d9d9",
        text_color="black",
        border_width=border,
        font=("Arial", size_add_room_popup),
        corner_radius=corner
    )
    location_entry_add_room_popup.grid(row=1, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    error_label = tk.Label(input_frame_add_room_popup,
        text="",
        background="white",
        fg="darkred",
        font=("Arial", 14)
    )
    error_label.grid(row=5, column=0, columnspan=2, padx=0, pady=20, sticky=tk.E)

    # Buttons (anpassung benötigt)
    def submit_entry():
        if (not room_entry_add_room_popup.get() or room_entry_add_room_popup.get() == ""
                or not location_entry_add_room_popup.get() or location_entry_add_room_popup.get() == ""):
            error_label.configure(text="Bitte fülle alle Felder aus.")
        else:
            sqlapi.create_room(room_entry_add_room_popup.get(), location_entry_add_room_popup.get())
            from .AdminRoomWindow import AdminRoomWindow
            AdminRoomWindow.update_treeview_with_data()
            from .MainPage import MainPage
            MainPage.update_sidetree_with_data()
            add_popup.destroy()

    def exit_entry():
        add_popup.destroy()

    from ._avatarManager import resource_path
    parent.add_btn_add_item_popup = tk.PhotoImage(file=resource_path("includes/assets/HinzuBig_blue.png"))
    parent.exit_btn_add_item_popup = tk.PhotoImage(file=resource_path("includes/assets/AbbrechenButton.png"))

    button_frame_add_item_popup = tk.Frame(add_popup, background="white")
    button_frame_add_item_popup.grid(row=2, column=0, pady=20, sticky=tk.NSEW)
    button_frame_add_item_popup.grid_columnconfigure(0, weight=1)
    button_frame_add_item_popup.grid_columnconfigure(1, weight=1)

    exit_button_add_item_popup = tk.Button(button_frame_add_item_popup,
        image=parent.exit_btn_add_item_popup,
        bd=0,
        relief=tk.FLAT,
        bg="white",
        activebackground="white",
        cursor="hand2",
        command=exit_entry
    )
    exit_button_add_item_popup.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)

    submit_button_add_item_popup = tk.Button(button_frame_add_item_popup,
        image=parent.add_btn_add_item_popup,
        bd=0,
        relief=tk.FLAT,
        bg="white",
        activebackground="white",
        cursor="hand2",
        command=submit_entry
    )
    submit_button_add_item_popup.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

    # Grid Configuration
    add_popup.grid_rowconfigure(0, weight=1)  # Header
    add_popup.grid_rowconfigure(1, weight=2)  # Input-Bereich
    add_popup.grid_rowconfigure(2, weight=1)  # Buttons
    add_popup.grid_columnconfigure(0, weight=1)  # Zentriere alle Inhalte
