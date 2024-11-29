import tkinter as tk
from tkinter import ttk
from datetime import datetime

#from tkcalendar import Calendar, DateEntry

import cache
import Datenbank.sqlite3api as db

LARGEFONT = ("Arial", 20)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"



def lend_popup(parent, data):
    """
    Creates a popup window that facilitates the lending process by allowing the user
    to input and confirm lending details such as item name, borrower, and lending date.
    The window is modal, non-resizable, and is positioned to the center of the screen.

    :param parent: The parent window that the popup will be associated with, which helps
                   in modal configuration and center positioning.
    :param data: A dictionary that contains initial data for the popup, specifically the
                 name of the item to be lent, which is pre-filled in the corresponding
                 entry field.
    :return: None
    """
    # Neues Fenster (Popup)
    popup = tk.Toplevel()
    popup.title("Ausleihen")
    popup.geometry("600x500")
    popup.transient(parent)
    popup.configure(background="white")
    popup.grab_set()  # Macht das Popup modal
    popup.attributes("-topmost", True)

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
        popup.iconbitmap("assets/srhIcon.ico")
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")

    # Funktion, um die Eingaben zu verarbeiten
    def confirm_lend():
        item = name_entry.get().strip()
        borrower = entry.get().strip()
        #lend_date = calEntry.get().strip()
        print(f"Item: {item}, Borrower: {borrower}, Date:")
        #lendupdate
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

    name_label = tk.Label(popup, text="Name", font=LARGEFONT, bg="white", anchor="w")
    name_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

    name_entry = tk.Entry(popup, font=LARGEFONT, bg=srhGrey, relief=tk.FLAT)
    name_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

    borrower_label = tk.Label(popup, text="Ausleiher", font=LARGEFONT, bg="white", anchor="w")
    borrower_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

    users = []
    for user in db.read_all_benutzer():
        users.append(user['Nutzername'])
    entry = ttk.Combobox(popup, font=("Arial", 16), values=users)
    entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
    entry.set(cache.user_name)

    label = tk.Label(popup, text="Ausleihdatum", font=LARGEFONT, bg="white", anchor="w")
    label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

    time_entry = tk.Entry(popup, font=LARGEFONT, bg=srhGrey, relief=tk.FLAT)
    time_entry.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

    popup.grid_columnconfigure(1, weight=1)  # Spalte 1 flexibel

    time_entry.insert(0, f'{datetime.now():%d.%m.%Y %H:%M}')
    name_entry.insert(0, data["name"])

    # Buttonbereich
    button_frame = tk.Frame(popup, bg="white")
    button_frame.grid(row=4, column=0, columnspan=2, pady=20)

    confirm_btn = tk.Button(
        button_frame, text="Bestätigen", font=LARGEFONT, bg="#DF4807", fg="white",
        relief=tk.FLAT, command=confirm_lend
    )
    confirm_btn.grid(row=0, column=0, padx=10)

    cancel_btn = tk.Button(
        button_frame, text="Abbrechen", font=LARGEFONT, bg=srhGrey, relief=tk.FLAT,
        command=popup.destroy
    )
    cancel_btn.grid(row=0, column=1, padx=10)
