import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox

from includes.pages.Searchbar.Logging import Logger
from includes.sec_data_info import sqlite3api as db
import string, random


def add_role_popup(parent):
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
    add_popup.title("Rolle Hinzufügen")
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
    add_popup.resizable(True, True)

    try:
        add_popup.iconbitmap("includes/assets/srhIcon.ico")
    except Exception as e:
        Logger('AddRolePopup').error(f"Fehler beim Laden des Icons: {e}")

    # Header
    header_frame_add_role_popup = tk.Frame(add_popup, background="#DF4807")
    header_frame_add_role_popup.grid(row=0, column=0, sticky="new")
    header_frame_add_role_popup.grid_columnconfigure(0, weight=1)

    header_label_add_role_popup = tk.Label(
        header_frame_add_role_popup, background="#00699a",
        text="Hinzufügen", foreground="white", font=("Arial", 40)
    )
    header_label_add_role_popup.grid(row=0, column=0, sticky=tk.NSEW)

    # Input Frame
    input_frame_add_role_popup = tk.Frame(add_popup, background="white")
    input_frame_add_role_popup.grid(row=1, column=0, pady=20, sticky=tk.NSEW)
    input_frame_add_role_popup.grid_columnconfigure(0, weight=1)
    input_frame_add_role_popup.grid_columnconfigure(1, weight=1)

    size_add_role_popup = 14

    # Admin
    admin = tk.Label(input_frame_add_role_popup,
                     text="Rollenname",
                     font=("Arial", size_add_role_popup),
                     background="white")
    admin.grid(row=0, column=0, pady=10, sticky="new")

    parent.role_name_entry = ctk.CTkEntry(input_frame_add_role_popup,
                                          fg_color="#d9d9d9",
                                          text_color="black",
                                          border_width=0)
    parent.role_name_entry.grid(row=0, column=1, columnspan=2, pady=10, sticky="new")

    # Ansehen
    view_label_roles_window = tk.Label(input_frame_add_role_popup,
                                       text="Ansehen",
                                       font=("Arial", size_add_role_popup), background="white")
    view_label_roles_window.grid(column=0, row=1, sticky=tk.W + tk.E, pady=10)

    parent.view = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.view.grid(column=1, row=1, sticky=tk.W + tk.E, pady=10)

    # Rolle Loeschbar
    delete_rl_label_roles_window = tk.Label(input_frame_add_role_popup, text="Rolle Löschbar",
                                            font=("Arial", size_add_role_popup), background="white")
    delete_rl_label_roles_window.grid(column=0, row=2, sticky=tk.W + tk.E, pady=10)

    parent.delete_rl = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.delete_rl.grid(column=1, row=2, sticky=tk.W + tk.E, pady=10)

    # Admin Feature
    feature_label_roles_window = tk.Label(input_frame_add_role_popup, text="Admin Feature",
                                          font=("Arial", size_add_role_popup), background="white")
    feature_label_roles_window.grid(column=0, row=3, sticky=tk.W + tk.E, pady=10)

    parent.feature = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.feature.grid(column=1, row=3, sticky=tk.W + tk.E, pady=10)

    # Loeschen
    delete_label_roles_window = tk.Label(input_frame_add_role_popup, text="Löschen",
                                         font=("Arial", size_add_role_popup), background="white")
    delete_label_roles_window.grid(column=0, row=4, sticky=tk.W + tk.E, pady=10)

    parent.delete = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.delete.grid(column=1, row=4, sticky=tk.W + tk.E, pady=10)

    # Bearbeiten
    edit_label_roles_window = tk.Label(input_frame_add_role_popup, text="Bearbeiten",
                                       font=("Arial", size_add_role_popup), background="white")
    edit_label_roles_window.grid(column=0, row=5, sticky=tk.W + tk.E, pady=10)

    parent.edit = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.edit.grid(column=1, row=5, sticky=tk.W + tk.E, pady=10)

    # Erstellen
    create_label_roles_window = tk.Label(input_frame_add_role_popup, text="Erstellen",
                                         font=("Arial", size_add_role_popup), background="white")
    create_label_roles_window.grid(column=0, row=6, sticky=tk.W + tk.E, pady=10)

    parent.create = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.create.grid(column=1, row=6, sticky=tk.W + tk.E, pady=10)

    # Gruppe Loeschen
    delete_g_label_roles_window = tk.Label(input_frame_add_role_popup, text="Gruppe Löschen",
                                           font=("Arial", size_add_role_popup), background="white")
    delete_g_label_roles_window.grid(column=0, row=7, sticky=tk.W + tk.E, pady=10)

    parent.delete_g = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.delete_g.grid(column=1, row=7, sticky=tk.W + tk.E, pady=10)

    # Gruppe Erstellen
    create_g_label_roles_window = tk.Label(input_frame_add_role_popup, text="Gruppe Erstellen",
                                           font=("Arial", size_add_role_popup), background="white")
    create_g_label_roles_window.grid(column=2, row=1, sticky=tk.W + tk.E, pady=10)

    parent.create_g = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.create_g.grid(column=3, row=1, sticky=tk.W + tk.E)

    # Gruppe Bearbeiten
    edit_g_label_roles_window = tk.Label(input_frame_add_role_popup, text="Gruppe Bearbeiten",
                                         font=("Arial", size_add_role_popup), background="white")
    edit_g_label_roles_window.grid(column=2, row=2, sticky=tk.W + tk.E)

    parent.edit_g = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.edit_g.grid(column=3, row=2, sticky=tk.W + tk.E)

    # Rollen Erstellen
    create_r_label_roles_window = tk.Label(input_frame_add_role_popup, text="Rollen Erstellen",
                                           font=("Arial", size_add_role_popup), background="white")
    create_r_label_roles_window.grid(column=2, row=3, sticky=tk.W + tk.E)

    parent.create_r = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.create_r.grid(column=3, row=3, sticky=tk.W + tk.E)

    # Rollen Bearbeiten
    edit_r_label_roles_window = tk.Label(input_frame_add_role_popup, text="Rollen Bearbeiten",
                                         font=("Arial", size_add_role_popup), background="white")
    edit_r_label_roles_window.grid(column=2, row=4, sticky=tk.W + tk.E)

    parent.edit_r = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.edit_r.grid(column=3, row=4, sticky=tk.W + tk.E)

    # Rollen Loeschen
    delete_r_label_roles_window = tk.Label(input_frame_add_role_popup, text="Rolle Löschen",
                                           font=("Arial", size_add_role_popup), background="white")
    delete_r_label_roles_window.grid(column=2, row=5, sticky=tk.W + tk.E)

    parent.delete_r = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.delete_r.grid(column=3, row=5, sticky=tk.W + tk.E)

    # Benutzer Loeschen
    delete_u_label_roles_window = tk.Label(input_frame_add_role_popup, text="User Löschen",
                                           font=("Arial", size_add_role_popup), background="white")
    delete_u_label_roles_window.grid(column=2, row=6, sticky=tk.W + tk.E)

    parent.delete_u = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.delete_u.grid(column=3, row=6, sticky=tk.W + tk.E)

    # Benutzer Bearbeiten
    edit_u_label_roles_window = tk.Label(input_frame_add_role_popup, text="User Bearbeiten",
                                           font=("Arial", size_add_role_popup), background="white")
    edit_u_label_roles_window.grid(column=2, row=7, sticky=tk.W + tk.E)

    parent.edit_u = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.edit_u.grid(column=3, row=7, sticky=tk.W + tk.E)

    # Benuzter Erstellen
    create_u_label_roles_window = tk.Label(input_frame_add_role_popup, text="User Erstellen",
                                           font=("Arial", size_add_role_popup), background="white")
    create_u_label_roles_window.grid(column=2, row=8, sticky=tk.W + tk.E)

    parent.create_u = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    parent.create_u.grid(column=3, row=8, sticky=tk.W + tk.E)

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
        if parent.role_name_entry.get() is not None and parent.role_name_entry.get() != "":
            role_name = parent.role_name_entry.get()
            view = "True" if parent.view.get() == 1 else "False"
            delete_rl = "True" if parent.delete_rl.get() == 1 else "False"
            feature = "True" if parent.feature.get() == 1 else "False"
            delete = "True" if parent.delete.get() == 1 else "False"
            edit = "True" if parent.edit.get() == 1 else "False"
            create = "True" if parent.create.get() == 1 else "False"
            delete_g = "True" if parent.delete_g.get() == 1 else "False"
            create_g = "True" if parent.create_g.get() == 1 else "False"
            edit_g = "True" if parent.edit_g.get() == 1 else "False"
            create_r = "True" if parent.create_r.get() == 1 else "False"
            edit_r = "True" if parent.edit_r.get() == 1 else "False"
            delete_r = "True" if parent.delete_r.get() == 1 else "False"
            delete_u = "True" if parent.delete_u.get() == 1 else "False"
            edit_u = "True" if parent.edit_u.get() == 1 else "False"
            create_u = "True" if parent.create_u.get() == 1 else "False"
            rechte = {
                "ROLLE_LOESCHBAR": delete_rl,
                "ADMIN_FEATURE": feature,
                "ENTRY_ANSEHEN": view,
                "ENTRY_LOESCHEN": delete,
                "ENTRY_BEARBEITEN": edit,
                "ENTRY_ERSTELLEN": create,
                "GRUPPEN_LOESCHEN": delete_g,
                "GRUPPEN_ERSTELLEN": create_g,
                "GRUPPEN_BEARBEITEN": edit_g,
                "ROLLEN_ERSTELLEN": create_r,
                "ROLLEN_BEARBEITEN": edit_r,
                "ROLLEN_LOESCHEN": delete_r,
                "USER_LOESCHEN": delete_u,
                "USER_BEARBEITEN": edit_u,
                "USER_ERSTELLEN": create_u
            }
            db.create_rolle(role_name, **rechte)
            from .adminRoleWindow import adminRoleWindow
            adminRoleWindow.update_treeview_with_data()
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
    parent.add_btn_add_item_popup = tk.PhotoImage(file=resource_path("includes/assets/HinzuBig_blue.png"))
    parent.exit_btn_add_item_popup = tk.PhotoImage(file=resource_path("includes/assets/AbbrechenButton.png"))

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

    # Fehleranzeige
    error_label = tk.Label(button_frame_add_item_popup, text="", background="white",fg="darkred",font=("Arial", 14))
    error_label.grid(row=0, column=0,columnspan=2, padx=0, pady=20)
