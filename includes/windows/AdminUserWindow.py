import tkinter as tk
from tkinter import ttk
from tkinter import *

from includes.sec_data_info import sqlite3api as sqlapi
import cache
from includes.util.Logging import Logger
from .AddUserPopup import AddUserPopup
from includes.gui.styles import *
import customtkinter as ctk  #pip install customtkinter
from ._sort_tree import sort_column
from ..util import Paths

logger:Logger = Logger('AdminUserWindow')


# Hauptseite (zweites Fenster)
class AdminUserWindow(tk.Frame):
    """
    Erstellt eine Benutzerübersichtsoberfläche für Administratoren.

    Das `AdminUserWindow` ist eine grafische Benutzeroberfläche, die Administratoren eine Übersicht
    über Benutzer bietet, zusammen mit Funktionen wie Suchen, Hinzufügen von Benutzern und
    Navigieren zu anderen Ansichtsfenstern. Diese Klasse erweitert den `tk.Frame` und konfiguriert
    ein umfassendes Layout, einschließlich eines Headers, Navigationsmenüs und eines mittleren
    Bereichs für Benutzerinteraktionen.

    :ivar srhHead: Speichert das Bild für das SRH-Logo, das im Header angezeigt wird.
    :type srhHead: tk.PhotoImage
    :ivar log_out_btn: Speichert das Bild für den Logout-Button.
    :type log_out_btn: tk.PhotoImage
    :ivar add_btn: Speichert das Bild für den "Nutzer hinzufügen"-Button.
    :type add_btn: tk.PhotoImage
    :ivar searchBtn: Speichert das Bild für den Such-Button.
    :type searchBtn: tk.PhotoImage
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")

        def go_back_admin_window():
            """
            go_back_admin_window():
                Navigiert zurück zum Hauptfenster der Anwendung für administrative Benutzer.
            """
            from .MainPage import MainPage
            controller.show_frame(MainPage)

        def show_settings_window_admin_window():
            logger.debug("show settings window admin window")
            from .settingsWindow import pop_up_settings
            pop_up_settings(self, controller)

        def search(event=None):                           # funktionalität hinzufügen
            search_entrys = []
            for entry in sqlapi.read_all_benutzer():
                for value in entry:
                    if user_search_entry.get().lower() in str(entry[value]).lower():
                        if entry not in search_entrys:
                            search_entrys.append(entry)
            self.update_treeview_with_data(data=search_entrys)

        def on_entry_click(event):
            if user_search_entry.get() == 'Suche':
                user_search_entry.delete(0, "end")  # Lösche den Platzhalter-Text
                user_search_entry.configure(text_color='black')  # Setze Textfarbe auf schwarz

        def on_focus_out(event):
            if user_search_entry.get() == '':
                user_search_entry.insert(0, 'Suche')  # Platzhalter zurücksetzen
                user_search_entry.configure(text_color='grey')  # Textfarbe auf grau ändern

        def on_key_press(event):
            typed_key = event.char  # The character of the typed key

        def change_to_room():
            """
            Diese Methode ermöglicht
            es dem Benutzer, die Ansicht zu einer Raum-Administrationsansicht
            zu wechseln.
            """
            from .AdminRoomWindow import AdminRoomWindow
            controller.show_frame(AdminRoomWindow)
            AdminRoomWindow.update_treeview_with_data()

        def change_to_roles():
            from .AdminRoleWindow import AdminRoleWindow
            controller.show_frame(AdminRoleWindow)
            AdminRoleWindow.update_treeview_with_data()

        def add_user():
            AddUserPopup(self.winfo_toplevel())

        global tree

        # Konfiguriere das Grid-Layout für das AdminUserWindow
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Erstelle einen Header-Bereich
        header_frame = tk.Frame(self, background=srh_blue)
        header_frame.grid(row=0, column=0,columnspan=2, sticky=tk.W + tk.E)

        # Konfiguriere die Spalten für den Header
        header_frame.grid_columnconfigure(0, weight=1)  # Platz links
        header_frame.grid_columnconfigure(1, weight=2)  # Zentrale Spalte
        header_frame.grid_columnconfigure(2, weight=1)  # Platz rechts
        header_frame.grid_rowconfigure(0, weight=1)

        from ._avatarManager import resource_path
        self.srhHead = tk.PhotoImage(file=resource_path("./includes/assets/srh.png"))

        # Füge ein zentriertes Label hinzu
        header_label = tk.Label(header_frame,
            image=self.srhHead,
            background=srh_blue,
            foreground="white"
        )
        header_label.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N + tk.W)

        # Erstellen eines Schriftzuges im Header
        text_header_label = tk.Label(header_frame,
            background=srh_blue,
            text="Nutzer-Übersicht",
            font=("Arial", 30),
            foreground="white"
        )
        text_header_label.grid(row=0, column=1, padx=0, pady=50, sticky="")

        # Konvertiere das Bild für Tkinter
        self.log_out_btn = tk.PhotoImage(file=Paths.assets_path("ArrowLeft.png"))

        # Füge einen Button mit dem Bild hinzu
        log_out_button = tk.Button(header_frame,
            image=self.log_out_btn,
            command=go_back_admin_window,
            cursor="hand2",
            bd=border,
            relief=tk.FLAT,
            bg=srh_blue,
            activebackground=srh_blue
        )
        log_out_button.grid(row=0, column=3, sticky=tk.E, padx=20)

        self.admin_user_window_avatar = cache.user_avatar

        # Füge einen Button mit dem Bild hinzu
        options_button_admin_user_window = tk.Button(header_frame,
            image=self.admin_user_window_avatar,
            command=show_settings_window_admin_window,
            bd=border,
            cursor="hand2",
            relief=tk.FLAT,
            bg=srh_blue,
            activebackground=srh_blue
        )
        options_button_admin_user_window.grid(row=0, column=2, sticky=tk.E, padx=20)

        #########
        #NAV:BAR#
        #########

        navi = tk.Frame(self, background=srh_grey)
        navi.grid(row=1, column=0, sticky="nesw")

        navi.grid_columnconfigure(0, weight=1)
        navi.grid_columnconfigure(1, weight=1)
        navi.grid_columnconfigure(2, weight=1)

        user_nav = ctk.CTkButton(navi,
            text="Nutzer",
            border_width=border,
            corner_radius=corner ,
            fg_color="#C5C5C5",
            cursor="hand2",
            text_color="black",
            font=("Arial", 20),
            hover_color=nav_bar_hover_color
        )
        user_nav.grid(padx=40, pady=15, row=0, column=0, sticky=tk.W + tk.E)

        room_nav = ctk.CTkButton(navi,
            text="Räume",
            border_width=border,
            corner_radius=corner ,
            fg_color="#C5C5C5",
            cursor="hand2",
            text_color="black",
            command=change_to_room,
            font=("Arial", 20),
            hover_color=nav_bar_hover_color
        )
        room_nav.grid(padx=40, pady=5, row=0, column=1, sticky=tk.W + tk.E)

        role_nav = ctk.CTkButton(navi,
            text="Rollen",
            border_width=border,
            corner_radius=corner ,
            fg_color="#C5C5C5",
            cursor="hand2",
            text_color="black",
            command=change_to_roles,
            font=("Arial", 20),
            hover_color=nav_bar_hover_color
        )
        role_nav.grid(padx=40, pady=5, row=0, column=2, sticky=tk.W + tk.E)

        middle_frame = tk.Frame(self,
                                background="white")
        middle_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(1, weight=1)

        # Verschiebe den SearchFrame nach oben, indem du seine Zeile anpasst
        search_frame = tk.Frame(middle_frame, bg="white")
        search_frame.grid(pady=5, padx=5, row=0, column=0, sticky=tk.W + tk.E + tk.N)

        search_frame.grid_columnconfigure(0, weight=0)
        search_frame.grid_columnconfigure(1, weight=1)
        search_frame.grid_columnconfigure(2, weight=0)

        global user_add_button
        self.add_btn = tk.PhotoImage(file=resource_path("./includes/assets/Hinzusmall_blue.png"))
        user_add_button = tk.Button(search_frame,
            image=self.add_btn,
            bd=border,
            relief=tk.FLAT,
            cursor="hand2",
            bg="white",
            activebackground="white",
            command=add_user
        )
        user_add_button.grid(padx=10, pady=1, row=0, column=2, sticky="w")

        self.searchBtn = tk.PhotoImage(file=resource_path("./includes/assets/search_button_blue.png"))
        search_button = tk.Button(search_frame,
            image=self.searchBtn,
            bd=border,
            relief=tk.FLAT,
            cursor="hand2",
            bg="white",
            activebackground="white",
            command=search
        )
        search_button.grid(padx=10, pady=5, row=0, column=0)

        # Entry-Feld mit Platzhalter-Text
        user_search_entry = ctk.CTkEntry(search_frame,
            fg_color=srh_grey,
            text_color="black",
            font=("Arial", 27),
            corner_radius=corner,
            border_width=border
        )
        user_search_entry.insert(0, 'Suche')  # Setze den Platzhalter-Text

        # Events für Klick und Fokusverlust hinzufügen
        user_search_entry.bind('<FocusIn>', on_entry_click)
        user_search_entry.bind('<FocusOut>', on_focus_out)
        user_search_entry.bind('<Return>', search)
        user_search_entry.bind("<Key>", on_key_press)
        user_search_entry.grid(column=1, row=0, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)

        self.user_tree_frame = tk.Frame(middle_frame,
            background="white",
            cursor="hand2"
        )
        self.user_tree_frame.grid(row=1, column=0, padx=0, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # Spaltenkonfiguration für das TreeFrame
        self.user_tree_frame.grid_rowconfigure(1, weight=1)
        self.user_tree_frame.grid_columnconfigure(0, weight=1)  # Spalte für die Tabelle
        self.user_tree_frame.grid_columnconfigure(1, weight=0)  # Spalte für die Scrollbar (fixiert)

        self.user_tree = ttk.Treeview(self.user_tree_frame,
            columns=("c1", "c2", "c3", "c4", "c5"),
            show="headings",
            cursor="hand2"
        )

        # Scrollbar erstellen
        self.user_tree_scroll = ctk.CTkScrollbar(self.user_tree_frame,
            orientation="vertical",
            command=self.user_tree.yview,
            fg_color="white",
            width=20,                                                # <--- +++++side scrollbar visibility+++++ #
            corner_radius=scroll_corner,
            button_color = srh_grey,
            button_hover_color="#2980b9"
        )
        self.user_tree_scroll.grid(row=1, column=1, sticky=tk.N + tk.S)  # Scrollbar genau neben der Tabelle

        # Treeview mit Scrollbar verbinden
        self.user_tree.configure(yscrollcommand=self.user_tree_scroll.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        self.user_tree.tag_configure("oddrow", background="#f7f7f7")
        self.user_tree.tag_configure("evenrow", background="white")

        user_columns = [
            ("# 1", "ID", 60),
            ("# 2", "Nutzername", 200),
            ("# 3", "Passwort", 200),
            ("# 4", "E-Mail", 300),
            ("# 5", "Rolle", 100)
        ]
        for col_id, col_name, col_width in user_columns:
            self.user_tree.column(col_id, anchor=tk.CENTER, width=col_width)
            self.user_tree.heading(col_id, text=col_name, command=lambda c=col_id: sort_column(self.user_tree, c, False))

        ### listbox for directories
        self.user_tree.column("# 1", anchor=CENTER, width=60)
        self.user_tree.heading("# 1", text="ID", )
        self.user_tree.column("# 2", anchor=CENTER, width=200)
        self.user_tree.heading("# 2", text="Nutzername")
        self.user_tree.column("# 3", anchor=CENTER, width=200)
        self.user_tree.heading("# 3", text="Passwort")
        self.user_tree.column("# 4", anchor=CENTER, width=300)
        self.user_tree.heading("# 4", text="E-Mail")
        self.user_tree.column("# 5", anchor=CENTER, width=100)
        self.user_tree.heading("# 5", text="Rolle")
        self.user_tree.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.user_tree.tkraise()
        self.update_treeview_with_data()

        # Funktion für das Ereignis-Binding
        def on_item_selected(event):
            """
            Eine GUI-Komponente für die Verwaltung von Benutzerfenstern in
            einer Tkinter-Anwendung.
            Dient als Grundaufbau für Benutzerinteraktionen, wie beispielsweise
            die Auswahl von Benutzerdetails im Interface.
            """
            try:
                selected_user = self.user_tree.focus()
                logger.debug(f"Ausgewählter User: {selected_user}")  # Debug
                if selected_user:
                    from .UserDetailsWindow import UserDetailsWindow, show_user_details
                    show_user_details(selected_user, self.user_tree, controller)
            except Exception as e:
                logger.error(f"Fehler bei der Auswahl: {e}")

        # Binde die Ereignisfunktion an die Treeview
        self.user_tree.bind("<Double-1>", on_item_selected)

    def update_treeview_with_data(self = None, data=None):
        """
        Aktualisiert die Treeview-Komponente mit Daten aus einer SQL-Datenbank. Diese Methode
        löscht zunächst alle vorhandenen Einträge im Treeview und fügt dann neue Daten aus der
        Datenbank ein. Jede Zeile erhält ein Tag, das zu einer alternierenden Darstellung von
        geraden und ungeraden Zeilen verwendet werden kann.

        :return: Gibt keinen Wert zurück.
        """
        if self is None:
            return
        self.user_tree.delete(*self.user_tree.get_children())
        i = 0
        if data is None:
            data = sqlapi.read_all_benutzer()

        for entry in data:
            # Bestimme das Tag für die aktuelle Zeile
            tag = "evenrow" if i % 2 == 0 else "oddrow"

            # Daten mit dem Tag in das Treeview einfügen
            self.user_tree.insert(
                "",
                "end",
                text=f"{entry['Nutzername']}",
                values=(
                    i,
                    entry['Nutzername'],
                    entry['Passwort'],
                    entry['Email'],
                    entry['Rolle'],
                ),
                tags=(tag,)
            )
            i += 1
        logger.debug(f"USER_ERSTELLEN:{cache.user_group_data['USER_ERSTELLEN']}")
        if cache.user_group_data['USER_ERSTELLEN'] == "False":
            user_add_button.grid_forget()
        else:
            user_add_button.grid(padx=10, pady=1, row=0, column=2, sticky="w")
