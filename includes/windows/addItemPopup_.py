import json
import tkinter as tk

from includes.util.Logging import Logger
from ._styles import *
import cache
import customtkinter as ctk
from ..CTkScrollableDropdown import *
from includes.sec_data_info import sqlite3api as db
from ..util import Paths


def add_item_popup(parent):
    """
    Erstellt ein Popup-Fenster, um ein neues Hardware-Element
    in das Inventarsystem einzufügen. Dabei wird eine Benutzeroberfläche
    erstellt, in der verschiedene Eingabefelder für die Eigenschaften
    des Hardware-Elements (z. B. Service-Tag, Typ, Raum, Name, Zustand)
    bereitgestellt werden.

    Die Funktion dient der zentralisierten Erfassung neuer Daten
    direkt durch die Benutzeroberfläche. Sie verarbeitet die Eingaben
    und speichert diese gegebenenfalls in einer Datenbank ab. Zudem
    wird ein Datenbank-Eintrag erstellt und die Hauptansicht entsprechend
    aktualisiert.

    :param parent: Das Hauptfenster oder Widget, zu dem dieses Popup gehört.
    :return: Rückgabe ist nicht definiert, da die Funktion keine expliziten
             Werte zurückgibt.
    """
    # Toplevel-Fenster erstellen
    add_popup = tk.Toplevel(parent)
    add_popup.title("Neuer Eintrag")
    add_popup.transient(parent)  # Popup bleibt im Vordergrund des Hauptfensters
    add_popup.grab_set()  # Blockiere Interaktionen mit dem Hauptfenster
    add_popup.attributes('-topmost', 0)
    add_popup.configure(background="white")

    # Bildschirmbreite und -höhe ermitteln
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Fensterbreite und -höhe definieren
    window_width = 650
    window_height = 650

    # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    add_popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    add_popup.resizable(False, False)

    logger:Logger = Logger('addItemPopup')

    # Icon setzen (optional)
    try:
        from ._avatarManager import resource_path
        add_popup.iconbitmap(Paths.assets_path("srhIcon.ico"))
    except Exception as e:
        logger.debug(f"Fehler beim Laden des Icons: {e}")

    # Erstelle einen Header-Bereich
    header_frame_add_item_popup = tk.Frame(add_popup,
        height=10,
        background="#DF4807"
    )
    header_frame_add_item_popup.grid(row=0, column=0, columnspan=3, sticky=tk.W + tk.E + tk.N)

    # Spaltenkonfiguration für Zentrierung im Frame
    header_frame_add_item_popup.grid_columnconfigure(0, weight=1)

    # Füge ein zentriertes Label hinzu
    header_label_add_item_popup = tk.Label(header_frame_add_item_popup,
        background="#DF4807",
        text="Erstellen",
        foreground="white",
        font=("Arial", 40)
    )
    header_label_add_item_popup.grid(row=0, column=0, sticky=tk.NSEW)

    # Label und Eingabefeld hinzufügen
    service_tag_label_add_item_popup = tk.Label(add_popup,
        text="Service Tag",
        background="white",
        font=("Arial", size_add_item_popup)
    )
    service_tag_label_add_item_popup.grid(row=1, column=0, padx=0, pady=20, sticky=tk.E)

    service_tag_entry_add_item_popup = ctk.CTkEntry(add_popup,
        border_width=0,
        text_color="black",
        fg_color=srh_grey,
        font=("Arial", size_add_item_popup),
        corner_radius=corner
    )
    service_tag_entry_add_item_popup.grid(row=1, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Typ
    type_label_add_item_popup = tk.Label(add_popup,
        text="Typ",
        background="white",
        font=("Arial", size_add_item_popup)
    )
    type_label_add_item_popup.grid(row=2, column=0, padx=0, pady=20, sticky=tk.E)

    type_entry_add_item_popup = ctk.CTkEntry(add_popup,
        border_width=0,
        text_color="black",
        fg_color=srh_grey,
        font=("Arial", size_add_item_popup),
        corner_radius=corner
    )
    type_entry_add_item_popup.grid(row=2, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Raum (Dropdown-Menü)
    room_label_add_item_popup = tk.Label(add_popup,
        text="Raum", background="white",
        font=("Arial", size_add_item_popup)
    )
    room_label_add_item_popup.grid(row=3, column=0, padx=0, pady=20, sticky=tk.E)

    # Combobox statt Entry
    room_values = []
    for room in db.fetch_all_rooms():
        room_values.append(room['Raum'])
    room_combobox_add_item_popup = ctk.CTkComboBox(add_popup,
        values=room_values,
        font=("Arial", size_add_item_popup),
        fg_color=srh_grey,
        text_color="black",
        button_color=srh_grey,
        corner_radius=corner,
        border_width=0,
        state="readonly"
    )
    room_combobox_add_item_popup.grid(row=3, column=1, padx=20, pady=20, sticky="ew")

    CTkScrollableDropdownFrame(room_combobox_add_item_popup,
        values=room_values,
        button_color=srh_grey,  #BUGGY
        frame_corner_radius=corner,
        fg_color=srh_grey,
        text_color="black",
        frame_border_width=comboborder,
        frame_border_color=srh_grey_hover,
        justify="left"
    )

    # Name
    name_label_add_item_popup = tk.Label(
        add_popup,
        text="Name",
        background="white",
        font=("Arial", size_add_item_popup)
    )
    name_label_add_item_popup.grid(row=4, column=0, padx=0, pady=20, sticky=tk.E)

    name_entry_add_item_popup = ctk.CTkEntry(
        add_popup,
        border_width=0,
        text_color="black",
        fg_color=srh_grey,
        font=("Arial", size_add_item_popup),
        corner_radius=corner
    )
    name_entry_add_item_popup.grid(row=4, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Beschädigung
    damaged_label_add_item_popup = tk.Label(
        add_popup,
        text="Beschädigung",
        background="white",
        font=("Arial", size_add_item_popup)
    )
    damaged_label_add_item_popup.grid(row=5, column=0, padx=0, pady=20, sticky=tk.E)

    damaged_button_add_item_popup = ctk.CTkEntry(
        add_popup,
        border_width=0,
        text_color="black",
        fg_color=srh_grey,
        font=("Arial", size_add_item_popup),
        corner_radius=corner
    )
    damaged_button_add_item_popup.grid(row=5, column=1, padx=20, pady=20, sticky=tk.E + tk.W)

    error_label = tk.Label(
        add_popup,
        text="",
        background="white",
        fg="darkred",
        font=("Arial", 14)
    )
    error_label.grid(row=6, column=0,columnspan=2, padx=0, pady=20, sticky=tk.E)

    # Funktion zum Eintrag hinzufügen
    def submit_entry():
        """
        Zeigt ein Popup-Fenster zum Hinzufügen eines neuen Geräts an und verarbeitet die Eingabe.

        Zusammenfassung:
        Dieses Popup-Fenster ermöglicht es dem Benutzer, ein neues Gerät mit bestimmten Attributen
        hinzuzufügen. Benutzer müssen die erforderlichen Felder ausfüllen, um sicherzustellen, dass
        das Gerät erfolgreich zur Datenbank hinzugefügt wird. Falls ein erforderliches Feld fehlt,
        wird eine Fehlermeldung angezeigt.

        Funktionen:
        - Ermöglicht die Eingabe von Attributen wie "service tag", "type", "room", "name" und "damage".
        - Validiert die Benutzereingaben auf Pflichtfelder.
        - Fügt das neue Gerät zur Datenbank hinzu, wenn alle Pflichtfelder ausgefüllt wurden.
        - Aktualisiert die Benutzeroberfläche mit den neuesten Daten.
        - Schließt das Popup, sobald der Eintrag erfolgreich verarbeitet wurde.

        :parameter parent: Das Eltern-Widget, auf dem das Popup aufgerufen wird.
        :typ parent: tkinter.Widget

        :return: Nichts.
        """
        # add device
        # tag, typ,raum,name,damage
        tag = service_tag_entry_add_item_popup.get() if service_tag_entry_add_item_popup.get() else ""
        type = type_entry_add_item_popup.get() if type_entry_add_item_popup.get() else ""
        room = room_combobox_add_item_popup.get() if room_combobox_add_item_popup.get() else ""
        name = name_entry_add_item_popup.get() if name_entry_add_item_popup.get() else ""
        damage = damaged_button_add_item_popup.get() if damaged_button_add_item_popup.get() else ""
        metadata:str = json.dumps(list[dict[str,str]]([{"erstellt von":cache.user_name}]))
        if type == "" or room == "Raum auswählen" or name == "":
            error_label.configure(text="Bitte fülle alle Felder aus (Typ, Raum, Name)")
        else:
            logger.debug(db.create_hardware(tag,type,name,damage,"",room, metadata))
            from .MainPage import MainPage
            MainPage.update_treeview_with_data(data=None)
            MainPage.update_sidetree_with_data()
            add_popup.destroy()

    def exit_entry():
        """
        Zeigt ein Fenster an, mit dem der Benutzer einen neuen Artikel hinzufügen
        kann. Diese Funktion erstellt und zeigt ein Pop-up-Fenster, das genutzt
        werden kann, um benutzerspezifische Eingaben entgegenzunehmen.

        :param parent: Das Eltern-Widget, zu dem dieses Pop-up-Fenster gehört
                       (normalerweise ein Tkinter-Fenster oder -Dialog).
                       Es wird verwendet, um das Pop-up-Fenster relativ dazu zu
                       positionieren.
        :type parent: tk.Widget
        :return: Kehrt nach der Interaktion des Benutzers und dem Hinzufügen eines
                 Artikels zurück, führt keine explizite Rückgabe von Werten durch.
        :rtype: None
        """
        add_popup.destroy()

    from ._avatarManager import resource_path
    parent.add_btn_add_item_popup = tk.PhotoImage(file=Paths.assets_path("ErstellenButton.png"))
    parent.exit_btn_add_item_popup = tk.PhotoImage(file=Paths.assets_path("AbbrechenButton.png"))

    # Buttons in ein separates Frame
    button_frame_add_item_popup = tk.Frame(add_popup, background="white")
    button_frame_add_item_popup.grid(row=7, column=0,columnspan=3, pady=20)

    exit_button_add_item_popup = tk.Button(button_frame_add_item_popup,
        image=parent.exit_btn_add_item_popup,
        bd=0,
        relief=tk.FLAT,
        bg="white",
        cursor="hand2",
        activebackground="white",
        command=exit_entry
    )
    exit_button_add_item_popup.grid(row=0, column=0)  # Links platzieren

    submit_button_add_item_popup = tk.Button(button_frame_add_item_popup,
        image=parent.add_btn_add_item_popup,
        bd=0,
        relief=tk.FLAT,
        bg="white",
        cursor="hand2",
        activebackground="white",
        command=submit_entry
    )
    submit_button_add_item_popup.grid(row=0, column=1)  # Neben Exit-Button platzieren

    add_popup.grid_rowconfigure(0, weight=0)
    add_popup.grid_rowconfigure(1, weight=1)
    add_popup.grid_rowconfigure(2, weight=0)
    add_popup.grid_rowconfigure(3, weight=1)
    add_popup.grid_columnconfigure(0, weight=1)
    add_popup.grid_columnconfigure(1, weight=1)
    add_popup.grid_columnconfigure(2, weight=1)
