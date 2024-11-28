import tkinter as tk
<<<<<<< HEAD
=======
from tkinter import ttk

import Datenbank.sqlite3api as db
import cache

>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13

def addItemPopup(parent):

    # Toplevel-Fenster erstellen
    popup = tk.Toplevel(parent)
    popup.title("Neuer Eintrag")
    popup.transient(parent)  # Popup bleibt im Vordergrund des Hauptfensters
    popup.grab_set()         # Blockiere Interaktionen mit dem Hauptfenster
    popup.attributes('-topmost', True)  # Erzwinge den Fokus auf das Popup

    # Bildschirmbreite und -höhe ermitteln
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Fensterbreite und -höhe definieren
    window_width = 960  # Halb von 1920
    window_height = 540  # Halb von 1080

    # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Setze die Fenstergröße und Position
    popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    popup.resizable(False, False)

    # Icon setzen (optional)
    try:
        popup.iconbitmap("assets/srhIcon.ico")
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")

    # Label und Eingabefeld hinzufügen
    label = tk.Label(popup, text="Füge einen neuen Eintrag hinzu:")
    label.pack(pady=10)

    entry = tk.Entry(popup)
    entry.pack(pady=5)

    # Funktion zum Eintrag hinzufügen
    def submitEntry():
        # add device
        # tag, typ,raum,name,damage
        tag = serviceTagEntryAddItemPopup.get() if serviceTagEntryAddItemPopup.get() else ""
        type = typeEntryAddItemPopup.get() if typeEntryAddItemPopup.get() else ""
        room = roomEntryAddItemPopup.get() if roomEntryAddItemPopup.get() else ""
        name = nameEntryAddItemPopup.get() if nameEntryAddItemPopup.get() else ""
        damage = damagedButtonAddItemPopup.get() if damagedButtonAddItemPopup.get() else ""
        db.create_hardware(tag,type,name,damage,None,room)
        from .mainPage import mainPage
        mainPage.update_treeview_with_data()
        addPopup.destroy()

    def exitEntry():
        print("Vorgang abgebrochen")
        addPopup.destroy()

    parent.addBtnAddItemPopup = tk.PhotoImage(file="assets/ErstellenButton.png")
    parent.exitBtnAddItemPopup = tk.PhotoImage(file="assets/AbbrechenButton.png")

    # Buttons in ein separates Frame
    buttonFrameAddItemPopup = tk.Frame(addPopup, background="white")
    buttonFrameAddItemPopup.grid(row=2, column=0, pady=20)

    exitButtonAddItemPopup = tk.Button(buttonFrameAddItemPopup, image=parent.exitBtnAddItemPopup,
                                       bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=exitEntry)
    exitButtonAddItemPopup.pack(side=tk.LEFT, padx=10)  # Links platzieren

    submitButtonAddItemPopup = tk.Button(buttonFrameAddItemPopup, image=parent.addBtnAddItemPopup,
                                         bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=submitEntry)
    submitButtonAddItemPopup.pack(side=tk.LEFT, padx=10)  # Neben Exit-Button platzieren

    addPopup.grid_rowconfigure(0, weight=0)
    addPopup.grid_rowconfigure(1, weight=1)
    addPopup.grid_rowconfigure(2, weight=0)
    addPopup.grid_rowconfigure(3, weight=1)
    addPopup.grid_columnconfigure(0, weight=1)
