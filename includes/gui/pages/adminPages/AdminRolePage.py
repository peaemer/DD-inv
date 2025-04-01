import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

from includes.sec_data_info import sqlite3api as sqlapi
import cache
from ..._styles import *
from includes.util.Logging import Logger
from includes.windows._sort_tree import sort_column
from includes.util import Paths
from .AdminRoomPage import AdminRoomPage

logger:Logger = Logger('AdminRoleWindow')


# Hauptseite (zweites Fenster)
class AdminRoleWindow(tk.Frame):
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
            from ...pages.MainPage import MainPage
            controller.show_frame(MainPage)

        def show_settings_window_admin_window():
            logger.debug("show settings window admin window")
            from ...pages.SettingsPage import pop_up_settings
            pop_up_settings(self, controller)

        def search(event=None):                           # funktionalität hinzufügen
            search_entrys = []
            for entry in sqlapi.read_all_rollen():
                for value in entry:
                    if role_search_entry.get().lower() in str(entry[value]).lower():
                        if entry not in search_entrys:
                            search_entrys.append(entry)
            self.update_treeview_with_data(data=search_entrys)

        def on_entry_click(event):
            logger.debug("on_entry_click executed")
            if role_search_entry.get() == 'Suche':
                role_search_entry.delete(0, "end")  # Lösche den Platzhalter-Text
                role_search_entry.configure(text_color='black')  # Setze Textfarbe auf schwarz
                logger.debug("Cleared Entry for use")

        def on_focus_out(event):
            logger.debug("on_focus_out executed")  # Debug
            if role_search_entry.get() == '':
                role_search_entry.insert(0, 'Suche')  # Platzhalter zurücksetzen
                role_search_entry.configure(text_color='grey')  # Textfarbe auf grau ändern
                logger.debug("Reset Entry") #Debug

        def on_key_press(event):
            typed_key = event.char  # The character of the typed key
            logger.debug(f"Key pressed:{typed_key}")

        def change_to_room():
            from .AdminRoomPage import AdminRoomPage
            controller.show_frame(AdminRoomPage)
            AdminRoomPage.update_treeview_with_data()
            logger.debug("change_to_role executed")  # Debug

        def change_to_user():
            from .AdminUserPage import AdminUserPage
            controller.show_frame(AdminUserPage)
            AdminUserPage.update_treeview_with_data()
            logger.debug("change_to_user executed")  # Debug

        def add_role():
            from ...popups.AddRolePopup import AddRolePopup
            AddRolePopup(self.winfo_toplevel())
            logger.debug("Add role executed") #Debug

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
        from includes.windows._avatarManager import resource_path
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
            text="Rollen-Übersicht",
            font=('Arial', 30),
            foreground="white"
        )
        text_header_label.grid(row=0, column=1, padx=0, pady=50, sticky="")

        # Konvertiere das Bild für Tkinter
        from includes.windows._avatarManager import resource_path
        self.log_out_btn = tk.PhotoImage(file=resource_path("./includes/assets/ArrowLeft.png"))

        # Füge einen Button mit dem Bild hinzu
        log_out_button = tk.Button(header_frame,
            image=self.log_out_btn,
            command=go_back_admin_window,
            bd=border,
            cursor="hand2",
            relief=tk.FLAT,
            bg=srh_blue,
            activebackground=srh_blue
        )
        log_out_button.grid(row=0, column=3, sticky=tk.E, padx=20)

        self.admin_role_window_avatar = cache.user_avatar

        # Füge einen Button mit dem Bild hinzu
        options_button_admin_role_window = tk.Button(header_frame,
            image=self.admin_role_window_avatar,
            command=show_settings_window_admin_window,
            bd=border,
            cursor="hand2",
            relief=tk.FLAT,
            bg=srh_blue,
            activebackground=srh_blue
        )
        options_button_admin_role_window.grid(row=0, column=2, sticky=tk.E, padx=20)

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
            command=change_to_user,
            cursor="hand2",
            corner_radius=corner,
            fg_color="#C5C5C5",
            text_color="black",
            font=("Arial", 20),
            hover_color=nav_bar_hover_color
        )
        user_nav.grid(padx=40, pady=15, row=0, column=0, sticky=tk.W + tk.E)

        room_nav = ctk.CTkButton(navi,
            text="Räume",
            border_width=border,
            corner_radius=corner,
            cursor="hand2" ,
            fg_color="#C5C5C5",
            text_color="black",
            command=change_to_room,
            font=("Arial", 20),
            hover_color=nav_bar_hover_color
        )
        room_nav.grid(padx=40, pady=5, row=0, column=1, sticky=tk.W + tk.E)

        role_nav = ctk.CTkButton(navi,
            text="Rollen",
            border_width=border,
            corner_radius=corner,
            cursor="hand2",
            fg_color="#C5C5C5",
            text_color="black",
            font=("Arial", 20),
            hover_color=nav_bar_hover_color
        )
        role_nav.grid(padx=40, pady=5, row=0, column=2, sticky=tk.W + tk.E)

        middle_frame = tk.Frame(self, background="white")
        middle_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(1, weight=1)

        # Verschiebe den SearchFrame nach oben, indem du seine Zeile anpasst
        search_frame = tk.Frame(middle_frame, bg="white")
        search_frame.grid(pady=5, padx=5, row=0, column=0, sticky=tk.W + tk.E + tk.N)

        search_frame.grid_columnconfigure(0, weight=0)
        search_frame.grid_columnconfigure(1, weight=1)
        search_frame.grid_columnconfigure(2, weight=0)

        global group_add_button
        self.add_btn = tk.PhotoImage(file=Paths.assets_path("Hinzusmall_blue.png"))

        group_add_button = tk.Button(search_frame,
            image=self.add_btn,
            bd=border,
            cursor="hand2",
            relief=tk.FLAT,
            bg="white",
            activebackground="white",
            command=add_role
        )
        group_add_button.grid(padx=10, pady=1, row=0, column=2, sticky="w")

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
        role_search_entry = ctk.CTkEntry(search_frame,
            fg_color=srh_grey,
            text_color="black",
            font=("Arial", 27),
            corner_radius=corner,
            border_width=border
        )
        role_search_entry.insert(0, 'Suche')  # Setze den Platzhalter-Text

        # Events für Klick und Fokusverlust hinzufügen
        role_search_entry.bind('<FocusIn>', on_entry_click)
        role_search_entry.bind('<FocusOut>', on_focus_out)
        role_search_entry.bind('<Return>', search)
        role_search_entry.bind("<Key>", on_key_press)
        role_search_entry.grid(column=1, row=0, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)

        role_tree_frame = tk.Frame(middle_frame, background="white")
        role_tree_frame.grid(row=1, column=0, padx=0, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # Spaltenkonfiguration für das TreeFrame
        role_tree_frame.grid_rowconfigure(1, weight=1)
        role_tree_frame.grid_columnconfigure(0, weight=1)  # Spalte für die Tabelle
        role_tree_frame.grid_columnconfigure(1, weight=0)  # Spalte für die Scrollbar (fixiert)

        global role_tree
        role_tree = ttk.Treeview(role_tree_frame,
                                 columns=("c1", "c2", "c3", "c4", "c5","c6", "c7", "c8",
                                          "c9", "c10","c11", "c12", "c13", "c14","c15","c16"),
                                 show="headings")

        # Scrollbar erstellen
        role_tree_scroll = ctk.CTkScrollbar(role_tree_frame,
            orientation="vertical",
            command=role_tree.yview,
            fg_color="white",
            width=20,                                                # <--- +++++side scrollbar visibility+++++ #
            corner_radius=scroll_corner,
            button_color = srh_grey,
            button_hover_color=srh_blue
        )
        role_tree_scroll.grid(row=1, column=1, sticky=tk.N + tk.S)  # Scrollbar genau neben der Tabelle

        # Treeview mit Scrollbar verbinden
        role_tree.configure(yscrollcommand=role_tree_scroll.set)

        # Scrollbar erstellen
        h_role_tree_scroll = ctk.CTkScrollbar(role_tree_frame,
            orientation="horizontal",
            command=role_tree.xview,
            fg_color="white",
            width=20,                                                # <--- +++++side scrollbar visibility+++++ #
            corner_radius=scroll_corner,
            button_color = srh_grey,
            button_hover_color=srh_blue
        )
        h_role_tree_scroll.grid(row=2, column=0, sticky=tk.W + tk.E)  # Scrollbar genau neben der Tabelle

        # Treeview mit Scrollbar verbinden
        role_tree.configure(xscrollcommand=h_role_tree_scroll.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        role_tree.tag_configure("oddrow", background="#f7f7f7")
        role_tree.tag_configure("evenrow", background="white")

        # Spaltennamen und Breiten als Liste
        role_columns = [
            ("# 1","Rolle", 250),
            ("# 2","Rolle Löschbar", 150),
            ("# 3","Admin Feature", 150),
            ("# 4","Ansehen", 90),
            ("# 5","Löschen", 100),
            ("# 6","Bearbeiten", 110),
            ("# 7","Erstellen", 100),
            ("# 8","Gruppe Löschen", 160),
            ("# 9","Gruppe Erstellen", 160),
            ("# 10","Gruppe Bearbeiten", 190),
            ("# 11","Rollen Erstellen", 170),
            ("# 12","Rollen Bearbeiten", 170),
            ("# 13","Rollen Löschen", 160),
            ("# 14","User Löschen", 160),
            ("# 15","User Bearbeiten", 190),
            ("# 16","User Erstellen", 160)
        ]

        for col_id, col_name, col_width in role_columns:
            role_tree.column(col_id, anchor=tk.CENTER, width=col_width)
            role_tree.heading(col_id, text=col_name, command=lambda c=col_id: sort_column(role_tree, c, True))

        # Treeview positionieren
        role_tree.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        role_tree.tkraise()
        self.update_treeview_with_data()

        # Funktion für das Ereignis-Binding
        def on_item_selected(event):
            """
            Diese Methode erbt von ``tk.Frame`` und
            dient als Grundaufbau für Benutzerinteraktionen, wie beispielsweise
            die Auswahl von Benutzerdetails im Interface.
            """
            try:
                selected_user = role_tree.focus()
                logger.debug(f"Selected user: {selected_user}") # Debug
                if selected_user:
                    from ..RolesDetailsPage import RolesDetailsWindow, show_roles_details
                    show_roles_details(selected_user, role_tree, controller)
            except Exception as e:
                logger.error(f"Error during selection: {e}") # Debug

        # Binde die Ereignisfunktion an die Treeview
        role_tree.bind("<Double-1>", on_item_selected)

    def update_treeview_with_data(self = None, data=None):
        """
        Aktualisiert die Treeview-Komponente mit Daten aus einer SQL-Datenbank. Diese Methode
        löscht zunächst alle vorhandenen Einträge im Treeview und fügt dann neue Daten aus der
        Datenbank ein. Jede Zeile erhält ein Tag, das zu einer alternierenden Darstellung von
        geraden und ungeraden Zeilen verwendet werden kann.
        """
        role_tree.delete(*role_tree.get_children())
        i = 0
        if data is None:
            data = sqlapi.read_all_rollen()

        for entry in data:
            # Bestimme das Tag für die aktuelle Zeile
            tag = "evenrow" if i % 2 == 0 else "oddrow"

            # Daten mit dem Tag in das Treeview einfügen
            role_tree.insert(
                "",
                "end",
                text=f"{entry['Rolle']}",
                values=(
                    entry['Rolle'],
                    "✔" if entry['ROLLE_LOESCHBAR'] == 'True' else "❌",
                    "✔" if entry['ADMIN_FEATURE'] == 'True' else "❌",
                    "✔" if entry['ENTRY_ANSEHEN'] == 'True' else "❌",
                    "✔" if entry['ENTRY_LOESCHEN'] == 'True' else "❌",
                    "✔" if entry['ENTRY_BEARBEITEN'] == 'True' else "❌",
                    "✔" if entry['ENTRY_ERSTELLEN'] == 'True' else "❌",
                    "✔" if entry['GRUPPEN_LOESCHEN'] == 'True' else "❌",
                    "✔" if entry['GRUPPEN_ERSTELLEN'] == 'True' else "❌",
                    "✔" if entry['GRUPPEN_BEARBEITEN'] == 'True' else "❌",
                    "✔" if entry['ROLLEN_ERSTELLEN'] == 'True' else "❌",
                    "✔" if entry['ROLLEN_BEARBEITEN'] == 'True' else "❌",
                    "✔" if entry['ROLLEN_LOESCHEN'] == 'True' else "❌",
                    "✔" if entry['USER_LOESCHEN'] == 'True' else "❌",
                    "✔" if entry['USER_BEARBEITEN'] == 'True' else "❌",
                    "✔" if entry['USER_ERSTELLEN'] == 'True' else "❌",
                ),
                tags=(tag,)
            )
            i += 1
        logger.debug("AdminRoleWindow treeview updated") #Debug
        if cache.user_group_data['ROLLEN_ERSTELLEN'] == "False":
            group_add_button.grid_forget()
        else:
            group_add_button.grid(padx=10, pady=1, row=0, column=2, sticky="w")
