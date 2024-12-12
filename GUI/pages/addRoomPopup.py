import tkinter as tk
from tkinter import ttk, messagebox
import Datenbank.sqlite3api as db
import string, random

from GUI.pages import roomDetailsWindow


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
        add_popup.iconbitmap("assets/srhIcon.ico")
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")

    # Header
    header_frame_add_room_popup = tk.Frame(add_popup, background="#DF4807")
    header_frame_add_room_popup.grid(row=0, column=0, sticky="new")
    header_frame_add_room_popup.grid_columnconfigure(0, weight=1)

    header_label_add_room_popup = tk.Label(
        header_frame_add_room_popup, background="#DF4807",
        text="Hinzufügen", foreground="white", font=("Arial", 40)
    )
    header_label_add_room_popup.grid(row=0, column=0, sticky=tk.NSEW)

    # Input Frame
    input_frame_add_room_popup = tk.Frame(add_popup, background="white")
    input_frame_add_room_popup.grid(row=1, column=0, pady=20, sticky=tk.NSEW)
    input_frame_add_room_popup.grid_columnconfigure(0, weight=1)
    input_frame_add_room_popup.grid_columnconfigure(1, weight=1)

    size_add_room_popup = 16

    #Raum Bezeichnung
    room_label_add_room_popup = tk.Label(
        input_frame_add_room_popup, text="Raum Bezeichnung", background="white",
        font=("Arial", size_add_room_popup)
    )
    room_label_add_room_popup.grid(row=0, column=0, padx=10, pady=20, sticky=tk.E)

    room_entry_add_room_popup = tk.Entry(
        input_frame_add_room_popup, background="#d9d9d9",
        font=("Arial", size_add_room_popup), bd=0
    )
    room_entry_add_room_popup.grid(row=0, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    #Ort
    location_add_room_popup = tk.Label(
        input_frame_add_room_popup, text="Ort", background="white",
        font=("Arial", size_add_room_popup)
    )
    location_add_room_popup.grid(row=1, column=0, padx=10, pady=20, sticky=tk.E)

    location_entry_add_room_popup = tk.Entry(
        input_frame_add_room_popup, background="#d9d9d9",
        font=("Arial", size_add_room_popup), bd=0
    )
    location_entry_add_room_popup.grid(row=1, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Buttons (anpassung benötigt)
    def submit_entry():
        """
        Fügt ein Popup-Fenster hinzu, mit dem ein Benutzer Räume in einer Anwendung anlegen
        oder bearbeiten kann. Diese Funktion überprüft die Eingaben des Benutzers und erstellt
        einen neuen Benutzer in der Datenbank mit einem generierten Passwort, falls die
        Eingaben korrekt sind. Zeigt bei Erfolg eine Meldung an und aktualisiert die
        Daten in der Adminansicht.

        :parameter parent: Referenz auf das Eltern-Widget.
        :type parent: tkinter Widget

        :raises None: Keine spezifischen Ausnahmen werden behandelt.

        :return: Gibt keinen Wert zurück.
        """
        pw = str(''.join(random.choices(string.ascii_letters, k=7)))
        if not room_entry_add_room_popup.get() or room_entry_add_room_popup.get() == "" or not role_combobox_add_user_popup.get() or role_combobox_add_user_popup.get() == "Rolle auswählen":
            error_label.configure(text="Please enter all required fields")
        else:
            db.create_benutzer(room_entry_add_room_popup.get(), pw, location_entry_add_room_popup.get())
            messagebox.showinfo(title="Added User", message="Nutzername: "+room_entry_add_room_popup.get()+"\nNew password: " + pw)
            from .adminRoomWindow import adminRoomWindow
            adminRoomWindow.update_treeview_with_data()
            add_popup.destroy()

    def exit_entry():
        """
        Öffnet ein Popup-Fenster, um einem Eltern-Widget einen neuen Raum hinzuzufügen.
        Diese Funktion dient zur benutzerfreundlichen Eingabe und Überprüfung von Raumdaten
        innerhalb der Anwendung.

        :param parent: Das Eltern-Widget, auf dem das Popup erstellt wird. Wird verwendet,
                       um sicherzustellen, dass das Popup korrekt in der GUI-Hierarchie
                       platziert wird.
        :type parent: Widget
        :return: Gibt nichts zurück.
        """
        add_popup.destroy()

    parent.add_btn_add_item_popup = tk.PhotoImage(file="assets/Hinzu.png")
    parent.exit_btn_add_item_popup = tk.PhotoImage(file="assets/AbbrechenButton.png")

    button_frame_add_item_popup = tk.Frame(add_popup, background="white")
    button_frame_add_item_popup.grid(row=2, column=0, pady=20, sticky=tk.NSEW)
    button_frame_add_item_popup.grid_columnconfigure(0, weight=1)
    button_frame_add_item_popup.grid_columnconfigure(1, weight=1)

    exit_button_add_item_popup = tk.Button(
        button_frame_add_item_popup, image=parent.exit_btn_add_item_popup,
        bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=exit_entry
    )
    exit_button_add_item_popup.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)

    submit_button_add_item_popup = tk.Button(
        button_frame_add_item_popup, image=parent.add_btn_add_item_popup,
        bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=submit_entry
    )
    submit_button_add_item_popup.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

    # Grid Configuration
    add_popup.grid_rowconfigure(0, weight=1)  # Header
    add_popup.grid_rowconfigure(1, weight=2)  # Input-Bereich
    add_popup.grid_rowconfigure(2, weight=1)  # Buttons
    add_popup.grid_columnconfigure(0, weight=1)  # Zentriere alle Inhalte
