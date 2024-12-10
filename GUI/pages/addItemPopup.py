import tkinter as tk
from tkinter import ttk

import Datenbank.sqlite3api as db
import cache


def add_item_popup(parent):
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
    add_popup = tk.Toplevel(parent)
    add_popup.title("Neuer Eintrag")
    add_popup.transient(parent)  # Popup bleibt im Vordergrund des Hauptfensters
    add_popup.grab_set()         # Blockiere Interaktionen mit dem Hauptfenster
    add_popup.attributes('-topmost', True)  # Erzwinge den Fokus auf das Popup
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

    # Icon setzen (optional)
    try:
        add_popup.iconbitmap("assets/srhIcon.ico")
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")

    # Erstelle einen Header-Bereich
    header_frame_add_item_popup = tk.Frame(add_popup, height=10, background="#DF4807")
    header_frame_add_item_popup.grid(row=0, column=0, columnspan=2, sticky=tk.W + tk.E + tk.N)

    # Spaltenkonfiguration für Zentrierung im Frame
    header_frame_add_item_popup.grid_columnconfigure(0, weight=1)

    # Füge ein zentriertes Label hinzu
    header_label_add_item_popup = tk.Label(header_frame_add_item_popup, background="#DF4807",
                                       text="Erstellen", foreground="white", font=("Arial", 40))
    header_label_add_item_popup.grid(row=0, column=0, sticky=tk.NSEW)

    # Input-Frame
    input_frame_add_item_popup = tk.Frame(add_popup, background="white")
    input_frame_add_item_popup.grid(row=1, column=0, pady=20)

    input_frame_add_item_popup.grid_columnconfigure(0, weight=1)  # Zentriere das Input-Frame
    input_frame_add_item_popup.grid_columnconfigure(1, weight=1)

    size_add_item_popup = 16

    # Label und Eingabefeld hinzufügen
    service_tag_label_add_item_popup = tk.Label(input_frame_add_item_popup, text="Service Tag", background="white",
                                           font=("Arial", size_add_item_popup))
    service_tag_label_add_item_popup.grid(row=0, column=0, padx=0, pady=20, sticky=tk.E)

    service_tag_entry_add_item_popup = tk.Entry(input_frame_add_item_popup, background="#d9d9d9",
                                           font=("Arial", size_add_item_popup), bd=0)
    service_tag_entry_add_item_popup.grid(row=0, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Typ
    type_label_add_item_popup = tk.Label(input_frame_add_item_popup, text="Typ", background="white",
                                     font=("Arial", size_add_item_popup))
    type_label_add_item_popup.grid(row=1, column=0, padx=0, pady=20, sticky=tk.E)

    type_entry_add_item_popup = tk.Entry(input_frame_add_item_popup, background="#d9d9d9", font=("Arial", size_add_item_popup),
                                     bd=0)
    type_entry_add_item_popup.grid(row=1, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Raum (Dropdown-Menü)
    room_label_add_item_popup = tk.Label(input_frame_add_item_popup, text="Raum", background="white",
                                     font=("Arial", size_add_item_popup))
    room_label_add_item_popup.grid(row=2, column=0, padx=0, pady=20, sticky=tk.E)

    # Combobox statt Entry
    room_values = []
    for room in db.fetch_all_rooms():
        room_values.append(room['Raum']+" - "+room['Ort'])
    room_combobox_add_item_popup = ttk.Combobox(input_frame_add_item_popup, values=room_values, font=("Arial", size_add_item_popup))
    room_combobox_add_item_popup.grid(row=2, column=1, padx=20, pady=20, sticky=tk.W + tk.E)
    room_combobox_add_item_popup.set("Raum auswählen")  # Platzhalter

    # Name
    name_label_add_item_popup = tk.Label(input_frame_add_item_popup, text="Name", background="white",
                                     font=("Arial", size_add_item_popup))
    name_label_add_item_popup.grid(row=3, column=0, padx=0, pady=20, sticky=tk.E)

    name_entry_add_item_popup = tk.Entry(input_frame_add_item_popup, background="#d9d9d9", font=("Arial", size_add_item_popup),
                                     bd=0)
    name_entry_add_item_popup.grid(row=3, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Beschädigung
    damaged_label_add_item_popup = tk.Label(input_frame_add_item_popup, text="Beschädigung", background="white",
                                        font=("Arial", size_add_item_popup))
    damaged_label_add_item_popup.grid(row=4, column=0, padx=0, pady=20, sticky=tk.E)

    damaged_button_add_item_popup = tk.Entry(input_frame_add_item_popup, background="#d9d9d9", font=("Arial", size_add_item_popup),
                                         bd=0)
    damaged_button_add_item_popup.grid(row=4, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Funktion zum Eintrag hinzufügen
    def submit_entry():
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
        tag = service_tag_entry_add_item_popup.get() if service_tag_entry_add_item_popup.get() else ""
        type = type_entry_add_item_popup.get() if type_entry_add_item_popup.get() else ""
        room = room_combobox_add_item_popup.get() if room_combobox_add_item_popup.get() else ""
        name = name_entry_add_item_popup.get() if name_entry_add_item_popup.get() else ""
        damage = damaged_button_add_item_popup.get() if damaged_button_add_item_popup.get() else ""
        db.create_hardware(tag,type,name,damage,None,room)
        from .mainPage import mainPage
        mainPage.update_treeview_with_data(data=None)
        add_popup.destroy()

    def exit_entry():
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
        add_popup.destroy()

    parent.add_btn_add_item_popup = tk.PhotoImage(file="assets/ErstellenButton.png")
    parent.exit_btn_add_item_popup = tk.PhotoImage(file="assets/AbbrechenButton.png")

    # Buttons in ein separates Frame
    button_frame_add_item_popup = tk.Frame(add_popup, background="white")
    button_frame_add_item_popup.grid(row=2, column=0, pady=20)

    exit_button_add_item_popup = tk.Button(button_frame_add_item_popup, image=parent.exit_btn_add_item_popup,
                                       bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=exit_entry)
    exit_button_add_item_popup.pack(side=tk.LEFT, padx=10)  # Links platzieren

    submit_button_add_item_popup = tk.Button(button_frame_add_item_popup, image=parent.add_btn_add_item_popup,
                                         bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=submit_entry)
    submit_button_add_item_popup.pack(side=tk.LEFT, padx=10)  # Neben Exit-Button platzieren

    add_popup.grid_rowconfigure(0, weight=0)
    add_popup.grid_rowconfigure(1, weight=1)
    add_popup.grid_rowconfigure(2, weight=0)
    add_popup.grid_rowconfigure(3, weight=1)
    add_popup.grid_columnconfigure(0, weight=1)
