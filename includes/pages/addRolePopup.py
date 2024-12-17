import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
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
    add_popup.resizable(False, False)

    try:
        add_popup.iconbitmap("includes/assets/srhIcon.ico")
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")

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

    # Rolle Auswahl
    role_label_add_role_popup = tk.Label(
        input_frame_add_role_popup, text="Rolle", background="white",
        font=("Arial", size_add_role_popup)
    )
    role_label_add_role_popup.grid(row=0, column=0, padx=10, pady=20, sticky=tk.E)

    role_values = []
    for room in db.read_all_rollen():
        role_values.append(room['Rolle'])
    role_combobox_add_user_popup = ttk.Combobox(
        input_frame_add_role_popup, values=role_values,
        font=("Arial", size_add_role_popup)
    )
    role_combobox_add_user_popup.grid(row=0, column=1, padx=20, pady=20, sticky=tk.W + tk.E)
    role_combobox_add_user_popup.set("Rolle auswählen")

    # Admin
    admin = tk.Label(input_frame_add_role_popup, text="Admin",
                     font=("Arial", size_add_role_popup), background="white")
    admin.grid(column=0, row=1, sticky=tk.W + tk.E, pady=10)

    admin = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    admin.grid(column=1, row=1, sticky=tk.W + tk.E, pady=10)

    # Ansehen
    view_label_roles_window = tk.Label(input_frame_add_role_popup, text="Ansehen",
                                       font=("Arial", size_add_role_popup), background="white")
    view_label_roles_window.grid(column=0, row=2, sticky=tk.W + tk.E, pady=10)

    view = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    view.grid(column=1, row=2, sticky=tk.W + tk.E, pady=10)

    # Rolle Loeschbar
    delete_rl_label_roles_window = tk.Label(input_frame_add_role_popup, text="Rolle Löschbar",
                                            font=("Arial", size_add_role_popup), background="white")
    delete_rl_label_roles_window.grid(column=0, row=3, sticky=tk.W + tk.E, pady=10)

    delete_rl = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    delete_rl.grid(column=1, row=3, sticky=tk.W + tk.E, pady=10)

    # Admin Feature
    feature_label_roles_window = tk.Label(input_frame_add_role_popup, text="Admin Feature",
                                          font=("Arial", size_add_role_popup), background="white")
    feature_label_roles_window.grid(column=0, row=4, sticky=tk.W + tk.E, pady=10)

    feature = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    feature.grid(column=1, row=4, sticky=tk.W + tk.E, pady=10)

    # Loeschen
    delete_label_roles_window = tk.Label(input_frame_add_role_popup, text="Löschen",
                                         font=("Arial", size_add_role_popup), background="white")
    delete_label_roles_window.grid(column=0, row=5, sticky=tk.W + tk.E, pady=10)

    delete = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    delete.grid(column=1, row=5, sticky=tk.W + tk.E, pady=10)

    # Bearbeiten
    edit_label_roles_window = tk.Label(input_frame_add_role_popup, text="Bearbeiten",
                                       font=("Arial", size_add_role_popup), background="white")
    edit_label_roles_window.grid(column=0, row=6, sticky=tk.W + tk.E, pady=10)

    edit = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    edit.grid(column=1, row=6, sticky=tk.W + tk.E, pady=10)

    # Erstellen
    create_label_roles_window = tk.Label(input_frame_add_role_popup, text="Erstellen",
                                         font=("Arial", size_add_role_popup), background="white")
    create_label_roles_window.grid(column=2, row=1, sticky=tk.W + tk.E, pady=10)

    create = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    create.grid(column=3, row=1, sticky=tk.W + tk.E, pady=10)

    # Gruppe Loeschen
    delete_g_label_roles_window = tk.Label(input_frame_add_role_popup, text="Gruppe Löschen",
                                           font=("Arial", size_add_role_popup), background="white")
    delete_g_label_roles_window.grid(column=2, row=2, sticky=tk.W + tk.E, pady=10)

    delete_g = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    delete_g.grid(column=3, row=2, sticky=tk.W + tk.E, pady=10)

    # Gruppe Erstellen
    create_g_label_roles_window = tk.Label(input_frame_add_role_popup, text="Gruppe Erstellen",
                                           font=("Arial", size_add_role_popup), background="white")
    create_g_label_roles_window.grid(column=2, row=3, sticky=tk.W + tk.E, pady=10)

    create_g = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    create_g.grid(column=3, row=3, sticky=tk.W + tk.E, pady=10)

    # Gruppe Bearbeiten
    edit_g_label_roles_window = tk.Label(input_frame_add_role_popup, text="Gruppe Bearbeiten",
                                         font=("Arial", size_add_role_popup), background="white")
    edit_g_label_roles_window.grid(column=2, row=4, sticky=tk.W + tk.E, pady=10)

    edit_g = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    edit_g.grid(column=3, row=4, sticky=tk.W + tk.E, pady=10)

    # Rollen Erstellen
    create_r_label_roles_window = tk.Label(input_frame_add_role_popup, text="Rollen Erstellen",
                                           font=("Arial", size_add_role_popup), background="white")
    create_r_label_roles_window.grid(column=2, row=5, sticky=tk.W + tk.E, padx=20, pady=10)

    create_r = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    create_r.grid(column=3, row=5, sticky=tk.W + tk.E, padx=20, pady=10)

    # Rollen Bearbeiten
    edit_r_label_roles_window = tk.Label(input_frame_add_role_popup, text="Rollen Bearbeiten",
                                         font=("Arial", size_add_role_popup), background="white")
    edit_r_label_roles_window.grid(column=2, row=6, sticky=tk.W + tk.E, padx=20, pady=10)

    edit_r = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    edit_r.grid(column=3, row=6, sticky=tk.W + tk.E, padx=20, pady=10)

    # Rollen Loeschen
    delete_r_label_roles_window = tk.Label(input_frame_add_role_popup, text="Rolle",
                                           font=("Arial", size_add_role_popup), background="white")
    delete_r_label_roles_window.grid(column=2, row=7, sticky=tk.W + tk.E, padx=20, pady=10)

    delete_r = ctk.CTkCheckBox(input_frame_add_role_popup, text_color="white")
    delete_r.grid(column=3, row=7, sticky=tk.W + tk.E, padx=20, pady=10)

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
        if not username_entry_add_role_popup.get() or username_entry_add_role_popup.get() == "" or not role_combobox_add_user_popup.get() or role_combobox_add_user_popup.get() == "Rolle auswählen":
            error_label.configure(text="Bitte fülle alle Felder aus (Nutzername)")
        else:
            db.create_benutzer(username_entry_add_role_popup.get(), pw, email_entry_add_role_popup.get())
            messagebox.showinfo(title="Added User", message="Nutzername: "+username_entry_add_role_popup.get()+"\nNew password: " + pw)
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
