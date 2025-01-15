import tkinter as tk
from tkinter import ttk
from tkinter import *
from includes.sec_data_info import sqlite3api as sqlapi
import cache
from ._styles import *
from.Searchbar.Logging import Logger
import customtkinter as ctk  #pip install customtkinter

logger:Logger = Logger('AdmonRoleWindow')

# Hauptseite (zweites Fenster)
class adminRoleWindow(tk.Frame):
    """
    Erstellt eine Benutzerübersichtsoberfläche für Administratoren.

    Das `adminUserWindow` ist eine grafische Benutzeroberfläche, die Administratoren eine Übersicht
    über Benutzer bietet, zusammen mit Funktionen wie Suchen, Hinzufügen von Benutzern und
    Navigieren zu anderen Ansichtsfenstern. Diese Klasse erweitert den `tk.Frame` und konfiguriert
    ein umfassendes Layout, einschließlich eines Headers, Navigationsmenüs und eines mittleren
    Bereichs für Benutzerinteraktionen.

    :ivar srhHead: Speichert das Bild für das SRH-Logo, das im Header angezeigt wird.
    :type srhHead: tk.PhotoImage
    :ivar log_out_btn: Speichert das Bild für den Logout-Button.
    :type log_out_btn: tk.PhotoImage
    :ivar opt_btn: Speichert das Bild für den Einstellungs-Button.
    :type opt_btn: tk.PhotoImage
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
            Eine Frame-Klasse, die ein Fenster für administrative Benutzer darstellt. Diese Klasse
            erweitert die tkinter Frame-Klasse und integriert einen Controller zur Navigation
            zwischen verschiedenen Anwendungsfenstern.

            :Attributes:
                parent (tk.Widget): Der übergeordnete Widget-Container, in dem dieser Frame erstellt wird.
                controller (object): Der Controller, der für das Management der Fenster-Navigation
                                     in der Anwendung verantwortlich ist.

            :Methods:
                go_back_admin_window():
                    Navigiert zurück zum Hauptfenster der Anwendung für administrative Benutzer.
            """
            from .mainPage import mainPage
            controller.show_frame(mainPage)

        def show_settings_window_admin_window():
            """
            Diese Klasse `adminUserWindow` ist eine Unterklasse von `tk.Frame` und dient als
            Fensterkomponente für die Verwaltung von Benutzern im Adminbereich. Sie ermöglicht
            die Anzeige bestimmter Fenster und deren Interaktionen.

            :ivar parent: Der übergeordnete Container dieses Frames.
            :ivar controller: Kontrollinstanz für die Verwaltung der Frames.
            """
            logger.debug("show settings window admin window")
            from .settingsWindow import pop_up_settings
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
            """
            Diese Klasse repräsentiert ein Administrationsfenster für Benutzer in einer
            GUI-Anwendung, die mithilfe des tkinter-Frameworks erstellt wurde. Sie
            ermöglicht Funktionen wie die Suche nach Benutzern und die Verwaltung von
            Benutzerkonten innerhalb der Benutzeroberfläche.

            Die Klasse erbt von ``tk.Frame`` und wird in einem Eltern-Widget integriert.
            """
            logger.debug("on_entry_click executed")
            if role_search_entry.get() == 'Suche':
                role_search_entry.delete(0, "end")  # Lösche den Platzhalter-Text
                role_search_entry.configure(text_color='black')  # Setze Textfarbe auf schwarz
                logger.debug("Cleared Entry for use")

        def on_focus_out(event):
            """
            Eine GUI-Klasse, die ein Admin-Panel zur Verfügung stellt, um Benutzerdaten zu verwalten und nach Benutzern
            zu suchen. Die Klasse erbt von `tk.Frame` und verwendet verschiedene UI-Komponenten, um Suchfunktionen und
            Benutzerinteraktionen zu ermöglichen.

            :param parent: Referenz auf das übergeordnete Widget
            :type parent: tk.Widget
            :param controller: Die Steuermechanik, die die Navigation zwischen Frames behandelt
            :type controller: object
            """
            logger.debug("on_focus_out executed")  # Debug
            if role_search_entry.get() == '':
                role_search_entry.insert(0, 'Suche')  # Platzhalter zurücksetzen
                role_search_entry.configure(text_color='grey')  # Textfarbe auf grau ändern
                logger.debug("Reset Entry") #Debug


        def on_key_press(event):

            """
            Eine Klasse, die ein Administrator-Benutzerfenster in einer tkinter-Umgebung definiert.

            Diese Klasse liefert grundlegende Funktionalitäten für ein Administrator-Benutzerfenster,
            indem sie die Eigenschaften und Ereignisse für ihre Darstellung und Bedienung implementiert.

            Attributes
            ----------
            parent :
                Das übergeordnete tkinter-Widget, zu dem dieses Frame hinzugefügt wird.
            controller :
                Die Steuerungskomponente, die verwendet wird, um diverse Fenster und Zustände
                innerhalb der Anwendung zu steuern.

            Methods
            -------
            Keine Methodenbeschreibung in der Klassen-Dokumentation.

            """
            typed_key = event.char  # The character of the typed key
            logger.debug(f"Key pressed:{typed_key}")

        def change_to_room():
            """
            adminUserWindow ist eine Unterklasse von tk.Frame und stellt
            ein Frame zur Verfügung, das spezifisch für die Benutzeroberfläche
            eines Admin-Benutzers entwickelt wurde. Diese Klasse ermöglicht
            es dem Benutzer, die Ansicht zu einer Raum-Administrationsansicht
            zu wechseln.

            :param parent: Das übergeordnete Widget, zu dem dieses Frame gehört
            :type parent: widget
            :param controller: Referenz auf den Controller, der die Navigation zwischen
                               den Frames verwaltet
            :type controller: Controller-Objekt
            """
            from .adminRoomWindow import adminRoomWindow
            controller.show_frame(adminRoomWindow)
            adminRoomWindow.update_treeview_with_data()
            logger.debug("change_to_role executed")  # Debug

        def change_to_user():
            """
            Eine Klasse, die ein Admin-Fenster für Räume darstellt. Diese Klasse ist eine Unterklasse
            von `tk.Frame` und bietet die Benutzeroberfläche zur Verwaltung von Räumen.

            :param parent: Das übergeordnete Widget des Frames.
            :type parent: tk.Widget
            :param controller: Der Controller, welcher die Navigation zwischen den Fenstern steuert.
            :type controller: object
            """
            from .adminUserWindow import adminUserWindow
            controller.show_frame(adminUserWindow)
            adminUserWindow.update_treeview_with_data()
            logger.debug("change_to_user executed")  # Debug

        def add_role():
            """
            Eine Unterklasse von `tk.Frame`, die ein Fenster für die Verwaltung von Admin-Benutzern
            darstellt.

            Diese Klasse enthält Funktionen zur Verwaltung von Benutzern, einschließlich der
            Ergänzung eines neuen Benutzers. Die Klasse sollte in einem tkinter-Projekt verwendet
            werden und erfordert einen `parent` und einen `controller`, die die Benutzeroberflächenelemente
            organisieren und verwalten.

            :param parent: Das übergeordnete tkinter-Objekt für dieses Fenster.
            :type parent: tk.Tk oder tk.Frame
            :param controller: Eine Referenz auf den Controller, der mehrere Fenster verwaltet.
            :type controller: object
            """
            from .addRolePopup import add_role_popup
            add_role_popup(self)
            logger.debug("Add role executed") #Debug

        global tree

        # Konfiguriere das Grid-Layout für das adminUserWindow
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Erstelle einen Header-Bereich
        header_frame = tk.Frame(self, background=srhBlue)
        header_frame.grid(row=0, column=0,columnspan=2, sticky=tk.W + tk.E)

        # Konfiguriere die Spalten für den Header
        header_frame.grid_columnconfigure(0, weight=1)  # Platz links
        header_frame.grid_columnconfigure(1, weight=2)  # Zentrale Spalte
        header_frame.grid_columnconfigure(2, weight=1)  # Platz rechts
        header_frame.grid_rowconfigure(0, weight=1)
        from ._avatarManager import resource_path
        self.srhHead = tk.PhotoImage(file=resource_path("./includes/assets/srh.png"))

        # Füge ein zentriertes Label hinzu
        header_label = tk.Label(header_frame, image=self.srhHead, background=srhBlue, foreground="white")
        header_label.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N + tk.W)

        # Erstellen eines Schriftzuges im Header
        text_header_label = tk.Label(header_frame, background=srhBlue, text="Rollen-Übersicht", font=('Arial', 30), foreground="white")
        text_header_label.grid(row=0, column=1, padx=0, pady=50, sticky="")


        # Konvertiere das Bild für Tkinter
        from ._avatarManager import resource_path
        self.log_out_btn = tk.PhotoImage(file=resource_path("./includes/assets/ArrowLeft.png"))

        # Füge einen Button mit dem Bild hinzu
        log_out_button = tk.Button(header_frame, image=self.log_out_btn, command=go_back_admin_window, bd=border, relief=tk.FLAT, bg=srhBlue,
                                 activebackground=srhBlue)
        log_out_button.grid(row=0, column=3, sticky=tk.E, padx=20)

        self.admin_role_window_avatar = cache.user_avatar

        # Füge einen Button mit dem Bild hinzu
        options_button_admin_role_window = tk.Button(header_frame,
                                   image=self.admin_role_window_avatar,
                                   command=show_settings_window_admin_window,
                                   bd=border,
                                   relief=tk.FLAT,
                                   bg=srhBlue,
                                   activebackground=srhBlue)
        options_button_admin_role_window.grid(row=0, column=2, sticky=tk.E, padx=20)


        #########
        #NAV:BAR#
        #########

        navi = tk.Frame(self, background=srhGrey)
        navi.grid(row=1, column=0, sticky="nesw")

        navi.grid_columnconfigure(0, weight=1)
        navi.grid_columnconfigure(1, weight=1)
        navi.grid_columnconfigure(2, weight=1)


        user_nav = ctk.CTkButton(navi, text="Nutzer", border_width=border, command=change_to_user, corner_radius=corner, fg_color="#C5C5C5",
                                 text_color="black", font=("Arial", 20), hover_color="darkgray")
        user_nav.grid(padx=40, pady=15, row=0, column=0, sticky=tk.W + tk.E)

        room_nav = ctk.CTkButton(navi, text="Räume", border_width=border, corner_radius=corner ,fg_color="#C5C5C5",
                                 text_color="black",command=change_to_room, font=("Arial", 20), hover_color="darkgray")
        room_nav.grid(padx=40, pady=5, row=0, column=1, sticky=tk.W + tk.E)

        role_nav = ctk.CTkButton(navi, text="Rollen", border_width=border, corner_radius=corner ,fg_color="#C5C5C5",
                                 text_color="black", font=("Arial", 20), hover_color="darkgray")
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
        self.add_btn = tk.PhotoImage(file=resource_path("./includes/assets/Hinzusmall_blue.png"))
        group_add_button = tk.Button(search_frame, image=self.add_btn, bd=border, relief=tk.FLAT, bg="white",
                                    activebackground="white", command=add_role)
        group_add_button.grid(padx=10, pady=1, row=0, column=2, sticky="w")

        self.searchBtn = tk.PhotoImage(file=resource_path("./includes/assets/search_button_blue.png"))
        search_button = tk.Button(search_frame,
                                 image=self.searchBtn,
                                 bd=border,
                                 relief=tk.FLAT,
                                 bg="white",
                                 activebackground="white",
                                 command=search)
        search_button.grid(padx=10, pady=5, row=0, column=0)

        # Entry-Feld mit Platzhalter-Text
        role_search_entry = ctk.CTkEntry(search_frame, fg_color=srhGrey, text_color="black", font=("Arial", 27),
                                         corner_radius=corner, border_width=border)
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
        role_tree = ttk.Treeview(role_tree_frame, column=("c1", "c2", "c3", "c4", "c5","c6", "c7", "c8", "c9", "c10","c11", "c12", "c13", "c14","c15","c16"), show="headings")

        # Scrollbar erstellen
        role_tree_scroll = ctk.CTkScrollbar(
            role_tree_frame,
            orientation="vertical",
            command=role_tree.yview,
            fg_color="white",
            width=20,                                                # <--- +++++side scrollbar visibility+++++ #
            corner_radius=scroll_corner,
            button_color = srhGrey,
            button_hover_color="#2980b9"
        )
        role_tree_scroll.grid(row=1, column=1, sticky=tk.N + tk.S)  # Scrollbar genau neben der Tabelle

        # Treeview mit Scrollbar verbinden
        role_tree.configure(yscrollcommand=role_tree_scroll.set)

        # Scrollbar erstellen
        h_role_tree_scroll = ctk.CTkScrollbar(
            role_tree_frame,
            orientation="horizontal",
            command=role_tree.xview,
            fg_color="white",
            width=20,                                                # <--- +++++side scrollbar visibility+++++ #
            corner_radius=scroll_corner,
            button_color = srhGrey,
            button_hover_color="#2980b9"
        )
        h_role_tree_scroll.grid(row=2, column=0, sticky=tk.W + tk.E)  # Scrollbar genau neben der Tabelle


        # Treeview mit Scrollbar verbinden
        role_tree.configure(xscrollcommand=h_role_tree_scroll.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        role_tree.tag_configure("oddrow", background="#f7f7f7")
        role_tree.tag_configure("evenrow", background="white")

        # Spaltennamen und Breiten als Liste
        columns = [
            ("ID", 30),
            ("Rolle", 250),
            ("Rolle Löschbar", 150),
            ("Admin Feature", 150),
            ("Ansehen", 90),
            ("Löschen", 100),
            ("Bearbeiten", 110),
            ("Erstellen", 100),
            ("Gruppe Löschen", 160),
            ("Gruppe Erstellen", 160),
            ("Gruppe Bearbeiten", 190),
            ("Rollen Erstellen", 170),
            ("Rollen Bearbeiten", 170),
            ("Rollen Löschen", 160),
            ("User Löschen", 160),
            ("User Bearbeiten", 190),
            ("User Erstellen", 160)
        ]

        # Treeview-Spalten dynamisch erstellen
        for idx, (col_name, col_width) in enumerate(columns, start=0):
            col_id = f"# {idx}"  # Spalten-ID
            role_tree.column(col_id, anchor=CENTER, width=col_width)
            role_tree.heading(col_id, text=col_name)

        # Treeview positionieren
        role_tree.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        role_tree.tkraise()
        self.update_treeview_with_data()

        # Funktion für das Ereignis-Binding
        def on_item_selected(event):
            """
            Eine GUI-Komponente für die Verwaltung von Benutzerfenstern in
            einer Tkinter-Anwendung. Diese Klasse erbt von ``tk.Frame`` und
            dient als Grundaufbau für Benutzerinteraktionen, wie beispielsweise
            die Auswahl von Benutzerdetails im Interface.

            :param parent: Oberkomponente, in der der Rahmen eingeordnet wird.
            :type parent: tk.Widget

            :param controller: Controller-Objekt, das für die Navigation und
                               Steuerung zwischen verschiedenen Fenstern
                               verantwortlich ist.
            :type controller: object
            """
            try:
                selected_user = role_tree.focus()
                logger.debug(f"Selected user: {selected_user}") # Debug
                if selected_user:
                    from .rolesDetailsWindow import rolesDetailsWindow, show_roles_details
                    show_roles_details(selected_user, role_tree, controller)
            except Exception as e:

                print(f"Error during selection: {e}") # Debug

        # Binde die Ereignisfunktion an die Treeview
        role_tree.bind("<Double-1>", on_item_selected)

    def update_treeview_with_data(self = None, data=None):
        """
        Aktualisiert die Treeview-Komponente mit Daten aus einer SQL-Datenbank. Diese Methode
        löscht zunächst alle vorhandenen Einträge im Treeview und fügt dann neue Daten aus der
        Datenbank ein. Jede Zeile erhält ein Tag, das zu einer alternierenden Darstellung von
        geraden und ungeraden Zeilen verwendet werden kann.

        :return: Gibt keinen Wert zurück.
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
        logger.debug("adminRoleWindow treeview updated") #Debug
        if cache.user_group_data['ROLLEN_ERSTELLEN'] == "False":
            group_add_button.grid_forget()
        else:
            group_add_button.grid(padx=10, pady=1, row=0, column=2, sticky="w")