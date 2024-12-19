import tkinter as tk
from tkinter import ttk
from datetime import datetime

#from tkcalendar import Calendar, DateEntry

import cache
from ._styles import *
from includes.sec_data_info import sqlite3api as db
from main import ddINV

def lend_popup(parent, data, controller: ddINV):
    """
    Erstellt ein modales Popup-Fenster zur Verwaltung von Ausleihvorgängen. Das Fenster
    zeigt ein Formular zur Eingabe von Ausleihdetails, einschließlich Name des Objekts,
    Name des Ausleihers und gegebenenfalls ein Ausleihdatum. Es bietet zwei
    Interaktionsmöglichkeiten: Bestätigung, die die Eingaben verarbeitet und das Fenster
    schließt, oder Abbruch, um die Aktion abzubrechen und das Fenster zu schließen.

    :param parent: Das übergeordnete Fenster, aus dem das Popup geöffnet wird
      :type parent: tk.Tk oder tk.Toplevel
    :param data: Ein Wörterbuch mit vorkonfigurierten Daten für die Ausleihe.
      Es enthält mindestens den Schlüssel "name", der den Namen des ausgeliehenen
      Objekts angibt.
      :type data: dict
    :return: Gibt keine Werte zurück.
    """
    # Neues Fenster (Popup)
    popup = tk.Toplevel()
    popup.title("Ausleihen")
    popup.geometry("600x500")
    popup.transient(parent)
    popup.configure(background="white")
    popup.grab_set()  # Macht das Popup modal
    popup.attributes("-topmost", 0)

    # Bildschirmbreite und -höhe ermitteln
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Fensterbreite und -höhe definieren
    window_width = 650
    window_height = 650

    # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    popup.resizable(False, False)

    # Icon setzen (optional)
    try:
        from ._avatarManager import resource_path
        popup.iconbitmap(resource_path("./includes/assets/srhIcon.ico"))
    except Exception as e:
        print(f"{debug_ANSI_style+"DEBUG"+ANSI_style_END}: Fehler beim Laden des Icons: {e}")

    # Funktion, um die Eingaben zu verarbeiten
    def confirm_lend():
        """
        Zeigt ein Ausleih-Popup-Fenster, das es ermöglicht, Daten über einen auszuleihenden
        Artikel und den Entleiher einzugeben. Nach Bestätigung wird das Popup geschlossen
        und die Daten der Konsole ausgegeben.

        :param parent: Das übergeordnete Fenster, zu dem das Popup gehört.
        :type parent: tkinter.Tk oder tkinter.Toplevel
        :param data: Zusätzliche Daten, die beim Erstellen des Popups verwendet werden können.

        :rtype: None
        :return: Gibt nichts zurück.
        """
        item = name_entry.get().strip()
        borrower = entry.get().strip()
        lend_date = time_entry.get().strip()
        print(f"{debug_ANSI_style+"DEBUG"+ANSI_style_END}: Item: {item}, Borrower: {borrower}, Date:")
        print(cache.selected_ID)
        db.create_ausleih_historie(cache.selected_ID, borrower, lend_date)
        db.update_hardware_by_ID(cache.selected_ID, neue_Ausgeliehen_von=borrower)
        from .mainPage import mainPage
        mainPage.update_treeview_with_data()
        controller.show_frame(mainPage)
        popup.destroy()  # Schließt das Popup nach Bestätigung


    # Grid-Layout konfigurieren
    popup.grid_rowconfigure(0, weight=0)  # Titelzeile
    popup.grid_rowconfigure(1, weight=0)  # Formularzeilen
    popup.grid_rowconfigure(2, weight=0)  # Formularzeilen
    popup.grid_rowconfigure(3, weight=0)  # Formularzeilen
    popup.grid_rowconfigure(4, weight=1)  # Buttonzeile
    popup.grid_columnconfigure(1, weight=1)  # Spalte 1 flexibel


    # Titelbereich
    title_label = tk.Label(
        popup, text="Ausleihen", font=("Arial", 35), bg="#DF4807", fg="white"
    )
    title_label.grid(row=0, column=0, columnspan=2, ipady=10, sticky="new")


    item_var = tk.StringVar()
    item_var.set("Itemplatzhalter") #funktion zum eifügen des Namens

    user_var = tk.StringVar()
    user_var.set(cache.user_name) #funktion zum eifügen des Namens



    # Formularbereich

    name_label = tk.Label(popup, text="Name", font=lend_font, bg="white", anchor="w")
    name_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

    name_entry = tk.Entry(popup, font=lend_font, bg=srhGrey, relief=tk.FLAT)
    name_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

    borrower_label = tk.Label(popup, text="Ausleiher", font=lend_font, bg="white", anchor="w")
    borrower_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")


    if cache.user_group == "Admin":
        users = []
        for user in db.read_all_benutzer():
            users.append(user['Nutzername'])
        entry = ttk.Combobox(popup, font=("Arial", 16), values=users)
        entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        entry.set(cache.user_name)
    else:
        entry_var = tk.StringVar()
        entry_var.set(cache.user_name)
        entry = tk.Entry(popup, font=lend_font, bg=srhGrey, relief=tk.FLAT, textvariable=entry_var, state="disabled")
        entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

    label = tk.Label(popup, text="Ausleihdatum", font=lend_font, bg="white", anchor="w")
    label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

    time_entry = tk.Entry(popup, font=lend_font, bg=srhGrey, relief=tk.FLAT)
    time_entry.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

    popup.grid_columnconfigure(1, weight=1)  # Spalte 1 flexibel

    time_entry.insert(0, f'{datetime.now():%d.%m.%Y %H:%M}')
    name_entry.insert(0, data["name"])

    # Buttonbereich
    button_frame = tk.Frame(popup, bg="white")
    button_frame.grid(row=4, column=0, columnspan=2, pady=20)

    confirm_btn = tk.Button(
        button_frame, text="Bestätigen", font=lend_font, bg="#DF4807", fg="white",
        relief=tk.FLAT, command=confirm_lend
    )
    confirm_btn.grid(row=0, column=0, padx=10)

    cancel_btn = tk.Button(
        button_frame, text="Abbrechen", font=lend_font, bg=srhGrey, relief=tk.FLAT,
        command=popup.destroy
    )
    cancel_btn.grid(row=0, column=1, padx=10)
