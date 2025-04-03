from tkinter import ttk, messagebox
from ..CTkScrollableDropdown import *

from ._avatarManager import resource_path
from .customMessageBoxDelete import *
from includes.util.Logging import Logger
from ..sec_data_info import UserSecurity
from ._sort_tree import sort_column
from .styles import *
import includes.sec_data_info.sqlite3api as db


def show_user_details(selected_user, tree, controller):
    # Daten aus der ausgewählten Zeile
    data = tree.item(selected_user, "values")
    Logger('UserDetailsWindow').debug(f"Data of the selected user: {data}")
    cache.selected_ID = data[1]
    controller.show_frame(UserDetailsWindow)  # Zeige die Details-Seite
    # Frame aktualisieren und anzeigen
    details = controller.frames[UserDetailsWindow]
    details.update_data(data)  # Methode in DetailsWindow aufrufen


class UserDetailsWindow(tk.Frame):
    """
    Repräsentiert ein Fenster für Benutzerdetails innerhalb einer Tkinter-Anwendung.

    Diese Klasse ist für die Anzeige und Bearbeitung der Benutzerdetails verantwortlich. Sie
    bietet die Möglichkeit, Benutzerinformationen einzusehen, Passwörter zurückzusetzen sowie
    Rollen und E-Mails zu ändern. Außerdem verfügt das Fenster über Funktionalitäten wie das
    Navigieren zu anderen Fenstern oder das Hinzufügen, Aktualisieren und Löschen von Benutzerdaten.

    :ivar controller: Eine Referenz auf den Controller, der die Fensterverwaltung regelt.
    :type controller: Any
    :ivar go_back_btn_details_window: Bildressource für den Zurück-Button.
    :type go_back_btn_details_window: tkinter.PhotoImage
    :ivar name: Eingabefeld für den Benutzernamen.
    :type name: tkinter.Entry
    :ivar reset_password: Button zum Zurücksetzen des Benutzerpassworts.
    :type reset_password: tkinter.Button
    :ivar email: Eingabefeld für die E-Mail-Adresse des Benutzers.
    :type email: tkinter.Entry
    :ivar role_combobox: Dropdown-Feld für die Auswahl der Benutzerrolle.
    :type role_combobox: tkinter.ttk.Combobox
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="white")

        def go_back_details_window():
            from .AdminUserWindow import AdminUserWindow
            controller.show_frame(AdminUserWindow)

        def show_settings_window_details_window():
            print("Show settings window details window")
            from .settingsWindow import pop_up_settings
            pop_up_settings(self, controller)

        def reset_pass():
            pw = UserSecurity.set_password(self.name.get(), None, None, randomize_password=True)
            if pw:
                messagebox.showinfo(title="Reseted User Password", message="New password: " + pw)
                from .AdminUserWindow import AdminUserWindow
                AdminUserWindow.update_treeview_with_data()
                controller.show_frame(AdminUserWindow)

        def customMessageBoxCall():
            if customMessageBoxDelete(self,
                    title="Aktion Bestätigen",
                    message="Willst du diesen Benutzer unwiderruflich löschen?",
                    buttonText="Benutzer Löschen",
                    blue=True):
                delete_entry()

        self.go_back_btn_details_window = tk.PhotoImage(file=resource_path("./includes/assets/ArrowLeft.png"))

        # Erstelle einen Header-Bereich
        header_frame_details_window = tk.Frame(self,
            height=10,
            background="#00699a"
        )
        header_frame_details_window.grid(row=0, column=0,columnspan=2, sticky=tk.W + tk.E + tk.N)

        # Überschrift mittig zentrieren
        header_frame_details_window.grid_columnconfigure(0, weight=1)  # Platz links
        header_frame_details_window.grid_columnconfigure(1, weight=3)  # Überschrift zentriert
        header_frame_details_window.grid_columnconfigure(2, weight=1)  # Option-Button

        # Zentriere das Label in Spalte 1
        header_label_details_window = tk.Label(
            header_frame_details_window,
            text="Nutzer Details",
            background="#00699a",
            foreground="white",
            font=("Arial", 60)
        )
        header_label_details_window.grid(row=0, column=1, pady=40, sticky=tk.W + tk.E)

        # Buttons in Spalten 2 und 3 platzieren
        go_back_button_details_window = tk.Button(
            header_frame_details_window,
            image=self.go_back_btn_details_window,
            command=go_back_details_window,
            bd=0,
            relief=tk.FLAT,
            bg="#00699a",
            activebackground="#00699a"
        )
        go_back_button_details_window.grid(row=0, column=0, sticky=tk.W, padx=20)

        # Container für Input- und Tree-Frame
        container_frame = tk.Frame(self, background="white")
        container_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Konfiguration der Container-Spalten
        container_frame.grid_columnconfigure(0, weight=1)  # Baumansicht
        container_frame.grid_columnconfigure(1, weight=1)  # Eingabefelder

        # Ändere die Position des TreeFrames
        tree_frame_details_window = tk.Frame(container_frame,
            background="white",
            width=200,
            height=400
        )
        tree_frame_details_window.grid(row=0, column=0, padx=40, sticky="")

        self.tree_details_window = ttk.Treeview(tree_frame_details_window,
            columns=("c1", "c2", "c3"),
            show="headings",
            height=30
        )

        scroll_details_window = tk.Scrollbar(tree_frame_details_window,
            orient="vertical",
            command=self.tree_details_window.yview,
            bg="black",
            activebackground="darkblue",
            troughcolor="grey",
            highlightcolor="black",
            width=15,
            borderwidth=1
        )
        scroll_details_window.grid(row=1, column=1, sticky="ns")
        self.tree_details_window.configure(yscrollcommand=scroll_details_window.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        self.tree_details_window.tag_configure("oddrow", background="#f7f7f7")
        self.tree_details_window.tag_configure("evenrow", background="white")

        user_details_window_columns = [
            ("# 1", "Name", 180),
            ("# 2", "ServiceTag/ID", 200),
            ("# 3", "Ausgeliehen am", 220),
        ]

        for col_id, col_name, col_width in user_details_window_columns:
            self.tree_details_window.column(col_id,
                anchor=tk.CENTER,
                width=col_width
            )
            self.tree_details_window.heading(col_id,
                text=col_name,
                command=lambda c=col_id: sort_column(self.tree_details_window,
                    c,
                    False)
            )

        self.tree_details_window.grid(row=1, column=0)
        self.tree_details_window.tkraise()

        # Input-Frame
        input_frame_details_window = tk.Frame(container_frame,
            background="white"
        )
        input_frame_details_window.grid(row=0, column=1, pady=20, sticky="nsew")

        input_frame_details_window.grid_columnconfigure(0, weight=1)  # Zentriere das Input-Frame
        input_frame_details_window.grid_columnconfigure(1, weight=1)
        input_frame_details_window.grid_columnconfigure(2, weight=1)

        #Nutzername
        name = tk.Label(input_frame_details_window,
            text="Nutzername",
            font=("Arial", size_details_window),
            background="white"
        )
        name.grid(column=0, row=0, sticky=tk.W + tk.E, padx=20, pady=10)

        self.name = ctk.CTkEntry(input_frame_details_window,
            font=("Arial", size_details_window),
            fg_color=srh_grey,
            border_width=border,
            corner_radius=corner,
            text_color="black"
        )
        self.name.grid(column=1, row=0, sticky=tk.W + tk.E, padx=20, pady=10)

        #Passwort
        password_label_details_window = tk.Label(input_frame_details_window,
            text="Passwort",
            font=("Arial", size_details_window),
            background="white"
        )
        password_label_details_window.grid(column=0, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        self.reset_password = ctk.CTkButton(input_frame_details_window,
            font=("Arial", size_details_window),
            text="Passwort zurücksetzen",
            command=reset_pass,
            fg_color=srh_grey,
            border_width=border,
            corner_radius=corner,
            text_color="black",
        )
        self.reset_password.grid(column=1, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        #Email
        email_label_details_window = tk.Label(input_frame_details_window,
            text="E-Mail",
            font=("Arial", size_details_window),
            background="white"
        )
        email_label_details_window.grid(column=0, row=2, sticky=tk.W + tk.E, padx=20, pady=10)

        self.email = ctk.CTkEntry(input_frame_details_window,
            font=("Arial", size_details_window),
            fg_color=srh_grey,
            border_width=border,
            corner_radius=corner,
            text_color="black"
        )
        self.email.grid(column=1, row=2, sticky=tk.W + tk.E, padx=20, pady=10)

        #Rolle
        role_label_details_window = tk.Label(input_frame_details_window,
            text="Rolle",
            font=("Arial", size_details_window),
            background="white"
        )
        role_label_details_window.grid(column=0, row=3, sticky=tk.W + tk.E, padx=20, pady=10)

        role_values = []
        for room in db.read_all_rollen():
            role_values.append(room['Rolle'])
        self.role_combobox = ctk.CTkComboBox(input_frame_details_window,
            values=role_values,
            font=("Arial", size_details_window),
            state="readonly",
            fg_color=srh_grey,
            border_width=border,
            button_color=srh_grey,
            corner_radius=corner,
            text_color="black"
        )

        self.role_combobox.grid(row=3, column=1, padx=20, pady=20, sticky=tk.W + tk.E)
        CTkScrollableDropdownFrame(self.role_combobox,
            values=role_values,
            button_color=srh_grey,  #BUGGY
            frame_corner_radius=corner,
            fg_color=srh_grey,
            text_color="black",
            frame_border_width=comboborder,
            frame_border_color=srh_grey_hover,
            justify="left"
        )

        # Funktion zum Eintrag hinzufügen
        def refresh_entry():
            #update
            print(db.update_benutzer(self.name.get(), neues_email=self.email.get(), neue_rolle=self.role_combobox.get()))
            from .AdminUserWindow import AdminUserWindow
            AdminUserWindow.update_treeview_with_data()
            controller.show_frame(AdminUserWindow)

        def delete_entry():
            """
            delete_entry()
                Löscht Benutzereinträge aus der Datenbank und aktualisiert die
                Benutzeransicht.
            """
            db.delete_benutzer(self.name.get())
            from .AdminUserWindow import AdminUserWindow
            AdminUserWindow.update_treeview_with_data()
            controller.show_frame(AdminUserWindow)

        self.edit_btn = tk.PhotoImage(file=resource_path("./includes/assets/AktualisierenBig_blue.png"))
        self.lend_btn = tk.PhotoImage(file=resource_path("./includes/assets/Ausleihen.png"))
        self.delete_btn = tk.PhotoImage(file=resource_path("./includes/assets/Loeschen.png"))

        # Buttons in ein separates Frame
        button_frame_add_item_popup = tk.Frame(self, background="white")
        button_frame_add_item_popup.grid(row=2, column=0, pady=20)

        global delete_button, edit_button

        delete_button = tk.Button(button_frame_add_item_popup,
            image=self.delete_btn,
            bd=0, relief=tk.FLAT, bg="white", activebackground="white",cursor="hand2",
            command= customMessageBoxCall
        )
        delete_button.pack(side=tk.LEFT, padx=20)  # Neben Exit-Button platzieren

        edit_button = tk.Button(button_frame_add_item_popup,
            image=self.edit_btn,
            bd=0, relief=tk.FLAT, bg="white",
            activebackground="white",cursor="hand2",
            command=refresh_entry
        )
        edit_button.pack(side=tk.LEFT, padx=20)  # Links platzieren

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(0, weight=1)

    def update_data(self, data):
        """
        Fügt Daten in die entsprechenden Entry-Felder und die Combobox ein.

        :param data: Eine Liste mit Werten, wobei jedes Element spezifischen Daten zugeordnet ist. Der zweite Wert
                     (`data[1]`) repräsentiert den Namen, der vierte Wert (`data[3]`) die E-Mail und der fünfte Wert
                     (`data[4]`) die Rolle, die in das Combobox-Feld gesetzt wird.
        :type data: list
        :return: None
        """
        # Daten in die Entry-Felder einfügen
        self.name.delete(0, tk.END)
        self.name.insert(0, data[1])

        self.tree_details_window.delete(*self.tree_details_window.get_children())
        i = 0
        for entry in db.fetch_ausleih_historie():
            if entry['Nutzername'] == data[1]:
                hw = db.fetch_hardware_by_id(entry['Hardware_ID'])
                if hw:
                    i += 1
                    tag = "evenrow" if i % 2 == 0 else "oddrow"
                    self.tree_details_window.insert(
                        "",
                        "end",
                        values=(hw['Modell'], hw['Service_Tag'], entry['Ausgeliehen_am']),
                        tags=(tag,)
                    )

        self.email.delete(0, tk.END)
        self.email.insert(0, data[3])

        self.role_combobox.set(data[4])  # Platzhalter

        if cache.user_group_data['USER_LOESCHEN'] == "True":
            delete_button.pack(side=tk.LEFT, padx=20)
        else:
            delete_button.pack_forget()
        if cache.user_group_data['USER_BEARBEITEN'] == "True":
            edit_button.pack(side=tk.LEFT, padx=20)
        else:
            edit_button.pack_forget()