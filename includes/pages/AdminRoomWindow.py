import tkinter as tk
from tkinter import ttk

import includes.sec_data_info.sqlite3api as sqlapi
import cache
from ._styles import *
from ._sort_tree import sort_column
import customtkinter as ctk


# Hauptseite (zweites Fenster)
class AdminRoomWindow(tk.Frame):
    """
    Beschreibt die Klasse und ihre Funktionalität.

    Die Klasse `AdminRoomWindow` repräsentiert das Fenster für die Raumverwaltung in einer
    Tkinter basierten GUI-Anwendung. Sie stellt die visuelle und funktionale Basis für
    das Verwalten von Räumen bereit, einschließlich Navigation, Suche, Hinzufügen neuer
    Räume sowie die Integration eines Tabellenbaums mit Rauminformationen.

    :ivar srhHead: Enthält das SRH-Logo, das im Header-Bereich als Bild angezeigt wird.
    :type srhHead: PhotoImage
    :ivar log_out_btn: Bild für die Logout-Schaltfläche im Header-Bereich.
    :type log_out_btn: PhotoImage
    :ivar add_btn: Bild für die Schaltfläche zum Hinzufügen eines neuen Raums.
    :type add_btn: PhotoImage
    :ivar searchBtn: Bild für die Schaltfläche, um die Suche zu starten.
    :type searchBtn: PhotoImage
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")

        def go_back_admin_window():
            """
           Enthält Navigation zur Hauptseite.
            """
            from .MainPage import MainPage
            controller.show_frame(MainPage)

        def show_settings_window_admin_window():
            print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: show settings window admin window") # Debug
            from .settingsWindow import pop_up_settings
            pop_up_settings(self, controller)

        def search(event=None):                           # funktionalität hinzufügen
            search_entrys = []
            for entry in sqlapi.fetch_all_rooms():
                for value in entry:
                    if room_search_entry.get().lower() in str(entry[value]).lower():
                        if entry not in search_entrys:
                            search_entrys.append(entry)
            self.update_treeview_with_data(data=search_entrys)

        def add_room():
            from .addRoomPopup import add_room_popup
            add_room_popup(self)

        def on_entry_click(event):
            if room_search_entry.get() == 'Suche':
                room_search_entry.delete(0, "end")  # Lösche den Platzhalter-Text
                room_search_entry.configure(text_color='black')  # Setze Textfarbe auf schwarz

        def on_focus_out(event):
            if room_search_entry.get() == '':
                room_search_entry.insert(0, 'Suche')  # Platzhalter zurücksetzen
                room_search_entry.configure(text_color='grey')  # Textfarbe auf grau ändern

        def on_key_press(event):
            typed_key = event.char  # The character of the typed key

        def change_to_user():
            from .AdminUserWindow import AdminUserWindow
            controller.show_frame(AdminUserWindow)
            AdminUserWindow.update_treeview_with_data()

        def change_to_roles():
            from .AdminRoleWindow import AdminRoleWindow
            controller.show_frame(AdminRoleWindow)
            AdminRoleWindow.update_treeview_with_data()

        global tree

        # Konfiguriere das Grid-Layout für das AdminRoomWindow
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Erstelle einen Header-Bereich
        header_frame = tk.Frame(self,
                                background=srh_blue)
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
                                foreground="white")
        header_label.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N + tk.W)

        # Erstellen eines Schriftzuges im Header
        text_header_label = tk.Label(header_frame,
                                     background=srh_blue,
                                     text="Raum-Übersicht",
                                     font=('Arial', 30),
                                     foreground="white")
        text_header_label.grid(row=0, column=1, padx=0, pady=50, sticky="")

        # Konvertiere das Bild für Tkinter
        self.log_out_btn = tk.PhotoImage(file=resource_path("./includes/assets/ArrowLeft.png"))

        # Füge einen Button mit dem Bild hinzu
        log_out_button = tk.Button(header_frame,
                                   image=self.log_out_btn,
                                   command=go_back_admin_window,
                                   cursor="hand2",
                                   bd=border,
                                   relief=tk.FLAT,
                                   bg=srh_blue,
                                   activebackground=srh_blue)
        log_out_button.grid(row=0, column=3, sticky=tk.E, padx=20)

        self.admin_room_window_avatar = cache.user_avatar

        # Füge einen Button mit dem Bild hinzu
        options_button_admin_room_window = tk.Button(header_frame,
                                                     image=self.admin_room_window_avatar,
                                                     command=show_settings_window_admin_window,
                                                     bd=0,
                                                     cursor="hand2",
                                                     relief=tk.FLAT,
                                                     bg=srh_blue,
                                                     activebackground=srh_blue)
        options_button_admin_room_window.grid(row=0, column=2, sticky=tk.E, padx=20)

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
                                 hover_color=nav_bar_hover_color)
        user_nav.grid(padx=40, pady=15, row=0, column=0, sticky=tk.W + tk.E)

        room_nav = ctk.CTkButton(navi,
                                 text="Räume",
                                 border_width=border,
                                 corner_radius=corner,
                                 cursor="hand2",
                                 fg_color="#C5C5C5",
                                 text_color="black",
                                 font=("Arial", 20),
                                 hover_color=nav_bar_hover_color)
        room_nav.grid(padx=40, pady=5, row=0, column=1, sticky=tk.W + tk.E)

        role_nav = ctk.CTkButton(navi,
                                 text="Rollen",
                                 border_width=border,
                                 corner_radius=corner,
                                 cursor="hand2",
                                 fg_color="#C5C5C5",
                                 text_color="black",
                                 command=change_to_roles,
                                 font=("Arial", 20),
                                 hover_color=nav_bar_hover_color)
        role_nav.grid(padx=40, pady=5, row=0, column=2, sticky=tk.W + tk.E)

        # Erstellen des MiddleFrame
        middle_frame = tk.Frame(self,
                                bg="white")
        middle_frame.grid(row=2, padx=10, pady=10, column=0, sticky="nesw")

        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(1, weight=1)

        # Verschiebe den SearchFrame nach oben, indem du seine Zeile anpasst
        search_frame = tk.Frame(middle_frame, bg="white")
        search_frame.grid(pady=5, padx=5, row=0, column=0, sticky=tk.W + tk.E + tk.N)

        search_frame.grid_columnconfigure(0, weight=0)
        search_frame.grid_columnconfigure(1, weight=1)
        search_frame.grid_columnconfigure(2, weight=0)

        self.add_btn = tk.PhotoImage(file=resource_path("./includes/assets/HinzuSmall_blue.png"))
        global room_add_button
        room_add_button = tk.Button(search_frame,
                                    image=self.add_btn,
                                    bd=border,
                                    relief=tk.FLAT,
                                    bg="white",
                                    cursor="hand2",
                                    activebackground="white",
                                    command=add_room)
        room_add_button.grid(padx=10, pady=5, row=0, column=2, sticky="w")

        self.searchBtn = tk.PhotoImage(file=resource_path("./includes/assets/search_button_blue.png"))
        search_button = tk.Button(search_frame,
                                 image=self.searchBtn,
                                 bd=border,
                                 relief=tk.FLAT,
                                 cursor="hand2",
                                 bg="white",
                                 activebackground="white",
                                 command=search)
        search_button.grid(padx=5, pady=5, row=0, column=0)

        # Entry-Feld mit Platzhalter-Text
        room_search_entry = ctk.CTkEntry(search_frame,
                                         fg_color=srh_grey,
                                         text_color="black",
                                         font=("Arial", 27),
                                         corner_radius=corner,
                                         border_width=border)
        room_search_entry.insert(0, 'Suche')  # Setze den Platzhalter-Text

        # Events für Klick und Fokusverlust hinzufügen
        room_search_entry.bind('<FocusIn>', on_entry_click)
        room_search_entry.bind('<FocusOut>', on_focus_out)
        room_search_entry.bind('<Return>', search)
        room_search_entry.bind("<Key>", on_key_press)
        room_search_entry.grid(column=1, row=0, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)

        # Ändere die Position des TreeFrames auf row=3
        room_tree_frame = tk.Frame(middle_frame,
                                   background="white")
        room_tree_frame.grid(row=1, column=0, padx=0, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # Spaltenkonfiguration für das TreeFrame
        room_tree_frame.grid_rowconfigure(1, weight=1)
        room_tree_frame.grid_columnconfigure(0, weight=1)  # Spalte für die Tabelle
        room_tree_frame.grid_columnconfigure(1, weight=0)  # Spalte für die Scrollbar (fixiert)

        global room_tree
        room_tree = ttk.Treeview(room_tree_frame,
                                 columns=("c1", "c2"),
                                 cursor="hand2",
                                 show="headings")

        # Scrollbar erstellen
        room_tree_scroll = ctk.CTkScrollbar(
            room_tree_frame,
            orientation="vertical",
            command=room_tree.yview,
            fg_color="white",
            width=20,                                                # <--- +++++side scrollbar visibility+++++ #
            corner_radius=scroll_corner,
            button_color = srh_grey,
            button_hover_color="#2980b9"
        )

        room_tree_scroll.grid(row=1, column=1, sticky=tk.N + tk.S)  # Scrollbar genau neben der Tabelle

        # Treeview mit Scrollbar verbinden
        room_tree.configure(yscrollcommand=room_tree_scroll.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        room_tree.tag_configure("oddrow", background="#f7f7f7")
        room_tree.tag_configure("evenrow", background="white")

        room_columns = [
            ("# 1", "Raum", 200),
            ("# 2", "Ort", 300),
        ]

        for col_id, col_name, col_width in room_columns:
            room_tree.column(col_id, anchor=tk.CENTER, width=col_width)
            room_tree.heading(col_id, text=col_name, command=lambda c=col_id: sort_column(room_tree, c, False))

        room_tree.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        room_tree.tkraise()
        self.update_treeview_with_data()

        # Funktion für das Ereignis-Binding
        def on_room_selected(event):
            try:
                selected_room = room_tree.focus()
                print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: Ausgewählter Raum: {selected_room}")  # Debug
                if selected_room:
                    from .RoomDetailsWindow import RoomDetailsWindow, show_room_details
                    show_room_details(selected_room, room_tree, controller)
            except Exception as e:
                print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: Fehler bei der Auswahl: {e}")

        # Binde die Ereignisfunktion an die Treeview
        room_tree.bind("<Double-1>", on_room_selected)

    def update_treeview_with_data(self = None, data=None):
        """
        Aktualisiert ein TreeView-Widget mit den Daten aus der Datenbank. Holt alle verfügbaren
        Raum-Daten aus der Datenquelle und fügt sie zeilenweise in das TreeView-Widget ein. Dabei
        wird abwechselnd ein Tag für ungerade und gerade Zeilen gesetzt, um eine visuelle
        Unterscheidung zu ermöglichen.

        :raises: Keine Fehler werden explizit geworfen.
        """
        room_tree.delete(*room_tree.get_children())
        i = 0
        if data is None:
            data = sqlapi.fetch_all_rooms()

        for entry in data:
            # Bestimme das Tag für die aktuelle Zeile
            tag = "evenrow" if i % 2 == 0 else "oddrow"

            # Daten mit dem Tag in das Treeview einfügen
            room_tree.insert(
                "",
                "end",
                text=f"{entry['Raum']}",
                values=(
                    entry['Raum'],
                    entry['Ort'],
                ),
                tags=(tag,)
            )
            i += 1
        if cache.user_group_data['GRUPPEN_ERSTELLEN'] == "False":
            room_add_button.grid_forget()
        else:
            room_add_button.grid(padx=10, pady=5, row=0, column=2, sticky="w")