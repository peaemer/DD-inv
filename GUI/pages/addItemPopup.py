import tkinter as tk
from tkinter import ttk

import Datenbank.sqlite3api as db
import cache


def addItemPopup(parent):
    """
    Creates a popup window for adding a new item. The popup window includes
    fields for entering details such as the service tag, type, room, name,
    and damage condition of an item. The window is configured to remain
    on top and block interactions with the main application window until it
    is closed. A submit button allows submission of the entered details,
    and an exit button allows closing of the popup without submitting.

    :param parent: The parent window to which the popup belongs, providing
        context for display and blocking interactions.
    :type parent: tk.Tk or tk.Toplevel

    :return: Returns the Toplevel widget that represents the popup window.
    :rtype: tk.Toplevel
    """
    # Toplevel-Fenster erstellen
    addPopup = tk.Toplevel(parent)
    addPopup.title("Neuer Eintrag")
    addPopup.transient(parent)  # Popup bleibt im Vordergrund des Hauptfensters
    addPopup.grab_set()         # Blockiere Interaktionen mit dem Hauptfenster
    addPopup.attributes('-topmost', True)  # Erzwinge den Fokus auf das Popup
    addPopup.configure(background="white")

    # Bildschirmbreite und -höhe ermitteln
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Fensterbreite und -höhe definieren
    window_width = 650
    window_height = 650

    # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    addPopup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    addPopup.resizable(False, False)

    # Icon setzen (optional)
    try:
        addPopup.iconbitmap("assets/srhIcon.ico")
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")

    # Erstelle einen Header-Bereich
    headerFrameAddItemPopup = tk.Frame(addPopup, height=10, background="#DF4807")
    headerFrameAddItemPopup.grid(row=0, column=0, columnspan=2, sticky=tk.W + tk.E + tk.N)

    # Spaltenkonfiguration für Zentrierung im Frame
    headerFrameAddItemPopup.grid_columnconfigure(0, weight=1)

    # Füge ein zentriertes Label hinzu
    headerLabelAddItemPopup = tk.Label(headerFrameAddItemPopup, background="#DF4807",
                                       text="Erstellen", foreground="white", font=("Arial", 40))
    headerLabelAddItemPopup.grid(row=0, column=0, sticky=tk.NSEW)

    # Input-Frame
    inputFrameAddItemPopup = tk.Frame(addPopup, background="white")
    inputFrameAddItemPopup.grid(row=1, column=0, pady=20)

    inputFrameAddItemPopup.grid_columnconfigure(0, weight=1)  # Zentriere das Input-Frame
    inputFrameAddItemPopup.grid_columnconfigure(1, weight=1)

    sizeAddItemPopup = 16

    # Label und Eingabefeld hinzufügen
    serviceTagLabelAddItemPopup = tk.Label(inputFrameAddItemPopup, text="Service Tag", background="white",
                                           font=("Arial", sizeAddItemPopup))
    serviceTagLabelAddItemPopup.grid(row=0, column=0, padx=0, pady=20, sticky=tk.E)

    serviceTagEntryAddItemPopup = tk.Entry(inputFrameAddItemPopup, background="#d9d9d9",
                                           font=("Arial", sizeAddItemPopup), bd=0)
    serviceTagEntryAddItemPopup.grid(row=0, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Typ
    typeLabelAddItemPopup = tk.Label(inputFrameAddItemPopup, text="Typ", background="white",
                                     font=("Arial", sizeAddItemPopup))
    typeLabelAddItemPopup.grid(row=1, column=0, padx=0, pady=20, sticky=tk.E)

    typeEntryAddItemPopup = tk.Entry(inputFrameAddItemPopup, background="#d9d9d9", font=("Arial", sizeAddItemPopup),
                                     bd=0)
    typeEntryAddItemPopup.grid(row=1, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Raum (Dropdown-Menü)
    roomLabelAddItemPopup = tk.Label(inputFrameAddItemPopup, text="Raum", background="white",
                                     font=("Arial", sizeAddItemPopup))
    roomLabelAddItemPopup.grid(row=2, column=0, padx=0, pady=20, sticky=tk.E)

    # Combobox statt Entry
    roomValues = ["Raum 101", "Raum 102", "Raum 201", "Raum 202"]  # Beispieleinträge
    roomComboboxAddItemPopup = ttk.Combobox(inputFrameAddItemPopup, values=roomValues, font=("Arial", sizeAddItemPopup))
    roomComboboxAddItemPopup.grid(row=2, column=1, padx=20, pady=20, sticky=tk.W + tk.E)
    roomComboboxAddItemPopup.set("Raum auswählen")  # Platzhalter

    # Name
    nameLabelAddItemPopup = tk.Label(inputFrameAddItemPopup, text="Name", background="white",
                                     font=("Arial", sizeAddItemPopup))
    nameLabelAddItemPopup.grid(row=3, column=0, padx=0, pady=20, sticky=tk.E)

    nameEntryAddItemPopup = tk.Entry(inputFrameAddItemPopup, background="#d9d9d9", font=("Arial", sizeAddItemPopup),
                                     bd=0)
    nameEntryAddItemPopup.grid(row=3, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Beschädigung
    damagedLabelAddItemPopup = tk.Label(inputFrameAddItemPopup, text="Beschädigung", background="white",
                                        font=("Arial", sizeAddItemPopup))
    damagedLabelAddItemPopup.grid(row=4, column=0, padx=0, pady=20, sticky=tk.E)

    damagedButtonAddItemPopup = tk.Entry(inputFrameAddItemPopup, background="#d9d9d9", font=("Arial", sizeAddItemPopup),
                                         bd=0)
    damagedButtonAddItemPopup.grid(row=4, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Funktion zum Eintrag hinzufügen
    def submitEntry():
        """
        Display a popup window to allow users to add a new hardware item to the
        inventory system. The function creates a user interface for input fields
        where users can specify details about the hardware item such as
        service tag, type, room location, name, and damage status. Upon
        submission, the inputs are saved to the database and the main page
        treeview is updated to reflect the new entry.

        :param parent: The parent window or component to which the popup belongs.
        :type parent: Widget
        :return: None
        """
        # add device
        # tag, typ,raum,name,damage
        tag = serviceTagEntryAddItemPopup.get() if serviceTagEntryAddItemPopup.get() else ""
        type = typeEntryAddItemPopup.get() if typeEntryAddItemPopup.get() else ""
        room = roomEntryAddItemPopup.get() if roomEntryAddItemPopup.get() else ""
        name = nameEntryAddItemPopup.get() if nameEntryAddItemPopup.get() else ""
        damage = damagedButtonAddItemPopup.get() if damagedButtonAddItemPopup.get() else ""
        db.create_hardware(tag,type,name,damage,None,room)
        from .mainPage import mainPage
        mainPage.update_treeview_with_data(data=None)
        addPopup.destroy()

    def exitEntry():
        """
        Displays a popup window to add an item.

        The function initializes and displays a popup window
        that allows users to add a new item to a predefined list.
        The popup will include necessary input fields and buttons
        for user interaction.

        :param parent: The parent widget that this popup will be
                       attached to. It is usually a reference to
                       a tkinter frame or window.
        :type parent: tkinter.Tk or tkinter.Widget
        """
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
