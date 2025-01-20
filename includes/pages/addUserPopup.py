import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from .Searchbar.Logging import Logger
from ..CTkScrollableDropdown import *
from includes.sec_data_info import sqlite3api as db
import string, random
from ._styles import *

def add_user_popup(parent):
    """
    Erstellt ein Popup-Fenster, mit dem ein neuer Benutzer hinzugefügt werden kann. Das Fenster
    ermöglicht die Eingabe von Benutzername, E-Mail und Rolle, sowie deren Validierung und
    Speicherung in der Datenbank. Zudem ist es möglich, das Popup über die vorhandenen Schaltflächen
    abzubrechen oder die Eingaben zu speichern.

    :param parent: Das übergeordnete Tkinter-Fenster, an das das Popup angehängt wird.
    :type parent: tk.Tk oder tk.Toplevel
    :return: None
    """
    add_popup = tk.Toplevel(parent)
    add_popup.title("User Hinzufügen")
    add_popup.transient(parent)
    add_popup.grab_set()
    add_popup.attributes('-topmost', 0)
    add_popup.configure(background="white")

    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    logger:Logger = Logger('AddUserPopup')

    window_width = 650
    window_height = 650

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    add_popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    add_popup.resizable(False, False)

    try:
        from ._avatarManager import resource_path
        add_popup.iconbitmap(resource_path("./includes/assets/srhIcon.ico"))
    except Exception as e:
        logger.error(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: Fehler beim Laden des Icons: {e}")

    # Header
    header_frame_add_item_popup = tk.Frame(add_popup, background="#00699a")
    header_frame_add_item_popup.grid(row=0, column=0,columnspan=3, sticky="new")
    header_frame_add_item_popup.grid_columnconfigure(0, weight=1)

    header_label_add_item_popup = tk.Label(
        header_frame_add_item_popup, background="#00699a",
        text="Hinzufügen", foreground="white", font=("Arial", 40)
    )
    header_label_add_item_popup.grid(row=0, column=0, sticky=tk.NSEW)

    size_add_user_popup = 16

    # Username
    username_label_add_user_popup = tk.Label(
        add_popup, text="Username", background="white",
        font=("Arial", size_add_user_popup)
    )
    username_label_add_user_popup.grid(row=1, column=0, padx=10, pady=0, sticky=tk.E)

    username_entry_add_user_popup = ctk.CTkEntry(add_popup,
                                             fg_color="#d9d9d9",
                                             text_color="black",
                                             border_width=border,
                                             corner_radius=corner)
    username_entry_add_user_popup.grid(row=1, column=1, padx=20, pady=0, sticky=tk.W + tk.E)

    # Email
    email_add_user_popup = tk.Label(add_popup,
                                    text="E-Mail", background="white",
                                    font=("Arial", size_add_user_popup))
    email_add_user_popup.grid(row=2, column=0, padx=10, pady=0, sticky=tk.E)

    email_entry_add_user_popup = ctk.CTkEntry(add_popup,
                                             fg_color="#d9d9d9",
                                             text_color="black",
                                             border_width=border,
                                             corner_radius=corner)
    email_entry_add_user_popup.grid(row=2, column=1, padx=20, pady=0, sticky=tk.W + tk.E)

    # Rolle
    role_label_add_user_popup = tk.Label(
        add_popup, text="Rolle", background="white",
        font=("Arial", size_add_user_popup)
    )
    role_label_add_user_popup.grid(row=3, column=0, padx=10, pady=0, sticky=tk.E)

    role_values = []
    for room in db.read_all_rollen():
        role_values.append(room['Rolle'])
    role_combobox_add_user_popup = ctk.CTkComboBox(
        add_popup,
        font=("Arial", size_add_user_popup),text_color="black", corner_radius=corner,button_color=srhGrey ,fg_color=srhGrey,border_width=border,
        state="readonly")
    CTkScrollableDropdownFrame(role_combobox_add_user_popup, values=role_values, button_color=srhGrey,  # BUGGY
                               frame_corner_radius=corner, fg_color=srhGrey,
                               text_color="black", frame_border_width=comboborder, frame_border_color=srhGreyHover,
                               justify="left")

    role_combobox_add_user_popup.grid(row=3, column=1, padx=20, pady=0, sticky=tk.W + tk.E)
    role_combobox_add_user_popup.set("Rolle auswählen")


    error_label = tk.Label(add_popup, text="", background="white",fg="darkred",font=("Arial", 14))
    error_label.grid(row=4, column=0,columnspan=3, padx=0, pady=0)

    # Buttons
    def submit_entry():
        """
        Erstellt den Benutzer-Popup-Dialog für die Hinzufügung eines neuen Benutzers.

        Diese Funktion öffnet ein Popup-Fenster für die Benutzerinteraktion. Es erhält die Nutzereingaben für den Benutzernamen,
        eine Rolle und eine optionale E-Mail-Adresse. Nach der Bestätigung der Eingabe wird der Benutzer in der Datenbank erstellt
        und ein neues Passwort generiert. Wenn die Eingabefelder nicht korrekt ausgefüllt werden, wird eine
        Fehlermeldung angezeigt.

        :param parent: Der übergeordnete GUI-Komponent, der als Bezugspunkt für das Popup verwendet wird

        :raises ValueError: Wenn eines der benötigten Felder nicht ausgefüllt ist, wird eine Fehlernachricht angezeigt

        :return: Es wird kein Wert zurückgegeben
        """
        pw = str(''.join(random.choices(string.ascii_letters, k=7)))
        if not username_entry_add_user_popup.get() or username_entry_add_user_popup.get() == "" or not role_combobox_add_user_popup.get() or role_combobox_add_user_popup.get() == "Rolle auswählen":
            error_label.configure(text="Bitte fülle alle Felder aus (Nutzername)")
        else:
            db.create_benutzer(username_entry_add_user_popup.get(), pw, email_entry_add_user_popup.get(), role_combobox_add_user_popup.get())
            messagebox.showinfo(title="Added User", message="Nutzername: "+username_entry_add_user_popup.get()+"\nNew password: " + pw)
            from .adminUserWindow import adminUserWindow
            adminUserWindow.update_treeview_with_data()
            add_popup.destroy()

    def exit_entry():
        """
        Die Funktion `add_user_popup` erzeugt ein Popup-Fenster zur Eingabe und Erstellung eines neuen Benutzers.
        Es wird ein Eltern-Widget übergeben, an dem das Popup angebunden wird.

        :param parent: Das übergeordnete Widget, an welches das Popup gebunden werden soll.
        :type parent: Widget
        """
        add_popup.destroy()

    from ._avatarManager import resource_path
    parent.add_btn_add_item_popup = tk.PhotoImage(file=resource_path("./includes/assets/HinzuBig_blue.png"))
    parent.exit_btn_add_item_popup = tk.PhotoImage(file=resource_path("./includes/assets/AbbrechenButton.png"))

    button_frame_add_item_popup = tk.Frame(add_popup, background="white")
    button_frame_add_item_popup.grid(row=5, column=0, pady=20,columnspan=3, sticky=tk.NSEW)
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
    add_popup.grid_rowconfigure(1, weight=1)  # Input-Bereich
    add_popup.grid_rowconfigure(2, weight=1)  # Buttons
    add_popup.grid_rowconfigure(3, weight=1)  # Buttons
    add_popup.grid_rowconfigure(4, weight=1)  # Buttons
    add_popup.grid_columnconfigure(0, weight=1)  # Zentriere alle Inhalte
    add_popup.grid_columnconfigure(1, weight=1)  # Zentriere alle Inhalte
    add_popup.grid_columnconfigure(2, weight=1)  # Zentriere alle Inhalte
