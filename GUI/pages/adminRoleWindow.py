import tkinter as tk
from tkinter import ttk
from tkinter import *
import Datenbank.sqlite3api as sqlapi
import cache
import customtkinter as ctk  #pip install customtkinter

LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"
srhBlue = "#00699a"
from ._SRHFont import load_font, SRHHeadline

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
            print("show settings window admin window")
            from .settingsWindow import pop_up_settings
            pop_up_settings(self)

        def search():                           # funktionalität hinzufügen
            search_entrys = []
            for entry in sqlapi.read_all_rollen():
                for value in entry:
                    if user_search_entry.get().lower() in str(entry[value]).lower():
                        if entry not in search_entrys:
                            search_entrys.append(entry)
            update_treeview_with_data(data=search_entrys)

        def add_role():
            """
            Diese Klasse repräsentiert das Hauptfenster zur Verwaltung von
            Benutzerkonten innerhalb der Anwendung. Sie erbt von `tk.Frame`
            und dient als Grundlage für die Erstellung der Benutzeroberfläche
            zur Verwaltung der Benutzer.

            Attribute
            ----------
            Keine spezifischen Attribute neben denen, die von `tk.Frame`
            geerbt wurden.

            Notes
            -----
            Die spezifischen Funktionen dieser Klasse, einschließlich der
            Methoden und Verhalten, die auf diese Klasse angewandt werden,
            müssen in den jeweiligen Methodendokumentationen definiert werden.
            """
            from .addUserPopup import add_user_popup
            add_user_popup(self)

        def on_entry_click(event):
            """
            Diese Klasse repräsentiert ein Administrationsfenster für Benutzer in einer
            GUI-Anwendung, die mithilfe des tkinter-Frameworks erstellt wurde. Sie
            ermöglicht Funktionen wie die Suche nach Benutzern und die Verwaltung von
            Benutzerkonten innerhalb der Benutzeroberfläche.

            Die Klasse erbt von ``tk.Frame`` und wird in einem Eltern-Widget integriert.
            """
            if user_search_entry.get() == 'Suche':
                user_search_entry.delete(0, "end")  # Lösche den Platzhalter-Text
                user_search_entry.config(fg='black')  # Setze Textfarbe auf schwarz

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
            if user_search_entry.get() == '':
                user_search_entry.insert(0, 'Suche')  # Platzhalter zurücksetzen
                user_search_entry.config(fg='grey')  # Textfarbe auf grau ändern

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
            from .addUserPopup import add_user_popup
            add_user_popup(self)

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

        self.srhHead = tk.PhotoImage(file="assets/srh.png")

        # Füge ein zentriertes Label hinzu
        header_label = tk.Label(header_frame, image=self.srhHead, background=srhBlue, foreground="white")
        header_label.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N + tk.W)

        # Erstellen eines Schriftzuges im Header
        text_header_label = tk.Label(header_frame, background=srhBlue, text="Rollen-Übersicht", font=(SRHHeadline, 30), foreground="white")
        text_header_label.grid(row=0, column=1, padx=0, pady=50, sticky="")


        # Konvertiere das Bild für Tkinter
        self.log_out_btn = tk.PhotoImage(file="assets/ArrowLeft.png")

        # Füge einen Button mit dem Bild hinzu
        log_out_button = tk.Button(header_frame, image=self.log_out_btn, command=go_back_admin_window, bd=0, relief=tk.FLAT, bg=srhBlue,
                                 activebackground=srhBlue)
        log_out_button.grid(row=0, column=3, sticky=tk.E, padx=20)

        # Konvertiere das Bild für Tkinter
        self.opt_btn = tk.PhotoImage(file="assets/option.png")

        # Füge einen Button mit dem Bild hinzu
        options_button = tk.Button(header_frame,
                                   image=self.opt_btn,
                                   command=show_settings_window_admin_window,
                                   bd=0,
                                   relief=tk.FLAT,
                                   bg=srhBlue,
                                   activebackground=srhBlue)
        options_button.grid(row=0, column=2, sticky=tk.E, padx=20)


        #########
        #NAV:BAR#
        #########

        navi = tk.Frame(self, background=srhGrey)
        navi.grid(row=1, column=0, sticky="nesw")

        navi.grid_columnconfigure(0, weight=1)
        navi.grid_columnconfigure(1, weight=1)
        navi.grid_columnconfigure(2, weight=1)


        user_nav = ctk.CTkButton(navi, text="Nutzer", border_width=0, command=change_to_user, corner_radius=20, fg_color="#C5C5C5",
                                 text_color="black", font=("Arial", 20), hover_color="darkgray")
        user_nav.grid(padx=40, pady=15, row=0, column=0, sticky=tk.W + tk.E)

        room_nav = ctk.CTkButton(navi, text="Räume", border_width=0, corner_radius=20 ,fg_color="#C5C5C5",
                                 text_color="black",command=change_to_room, font=("Arial", 20), hover_color="darkgray")
        room_nav.grid(padx=40, pady=5, row=0, column=1, sticky=tk.W + tk.E)

        role_nav = ctk.CTkButton(navi, text="Rollen", border_width=0, corner_radius=20 ,fg_color="#C5C5C5",
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

        self.add_btn = tk.PhotoImage(file="assets/Hinzusmall_blue.png")
        user_add_button = tk.Button(search_frame, image=self.add_btn, bd=0, relief=tk.FLAT, bg="white",
                                    activebackground="white", command=add_role)
        user_add_button.grid(padx=10, pady=1, row=0, column=2, sticky="w")

        self.searchBtn = tk.PhotoImage(file="assets/search_button_blue.png")
        search_button = tk.Button(search_frame,
                                 image=self.searchBtn,
                                 bd=0,
                                 relief=tk.FLAT,
                                 bg="white",
                                 activebackground="white",
                                 command=search)
        search_button.grid(padx=10, pady=5, row=0, column=0)

        # Entry-Feld mit Platzhalter-Text
        user_search_entry = tk.Entry(search_frame, bg=srhGrey, font=("Arial", 20), bd=0, fg='grey')
        user_search_entry.insert(0, 'Suche')  # Setze den Platzhalter-Text

        # Events für Klick und Fokusverlust hinzufügen
        user_search_entry.bind('<FocusIn>', on_entry_click)
        user_search_entry.bind('<FocusOut>', on_focus_out)
        user_search_entry.bind('<Return>', search)
        user_search_entry.bind("<Key>", on_key_press)
        user_search_entry.grid(column=1, row=0, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)

        role_tree_frame = tk.Frame(middle_frame, background="white")
        role_tree_frame.grid(row=1, column=0, padx=0, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # Spaltenkonfiguration für das TreeFrame
        role_tree_frame.grid_rowconfigure(1, weight=1)
        role_tree_frame.grid_columnconfigure(0, weight=1)  # Spalte für die Tabelle
        role_tree_frame.grid_columnconfigure(1, weight=0)  # Spalte für die Scrollbar (fixiert)

        global user_tree
        role_tree = ttk.Treeview(role_tree_frame, column=("c1", "c2", "c3", "c4", "c5","c6", "c7", "c8", "c9", "c10","c11", "c12", "c13"), show="headings")

        role_scroll = tk.Scrollbar(
            role_tree_frame,
            orient="vertical",
            command=role_tree.yview,
            bg="black",
            activebackground="darkblue",
            troughcolor="grey",
            highlightcolor="black",
            width=15,
            borderwidth=1
        )
        role_scroll.grid(row=1, column=1, sticky="ns")

        # Treeview mit Scrollbar verbinden
        role_tree.configure(yscrollcommand=role_scroll.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        role_tree.tag_configure("oddrow", background="#f7f7f7")
        role_tree.tag_configure("evenrow", background="white")

        # Spaltennamen und Breiten als Liste
        columns = [
            ("ID", 30),
            ("Rolle", 150),
            ("Ansehen", 150),
            ("Rolle Löschbar", 150),
            ("Admin Feature", 150),
            ("Löschen", 100),
            ("Bearbeiten", 100),
            ("Erstellen", 100),
            ("Gruppe Löschen", 150),
            ("Gruppe Erstellen", 150),
            ("Gruppe Bearbeiten", 150),
            ("Rollen Erstellen", 150),
            ("Rollen Bearbeiten", 150),
            ("Rollen Löschen", 150)
        ]

        # Treeview-Spalten dynamisch erstellen
        for idx, (col_name, col_width) in enumerate(columns, start=0):
            col_id = f"# {idx}"  # Spalten-ID
            role_tree.column(col_id, anchor=CENTER, width=col_width)
            role_tree.heading(col_id, text=col_name)

        # Treeview positionieren
        role_tree.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        role_tree.tkraise()

        def update_treeview_with_data(data=None):
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

            print(data)
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
                        "✓" if entry['ANSEHEN'] == 'True' else "✕",
                        "✓" if entry['ROLLE_LOESCHBAR'] == 'True' else "✕",
                        "✓" if entry['ADMIN_FEATURE'] == 'True' else "✕",
                        "✓" if entry['LOESCHEN'] == 'True' else "✕",
                        "✓" if entry['BEARBEITEN'] == 'True' else "✕",
                        "✓" if entry['ERSTELLEN'] == 'True' else "✕",
                        "✓" if entry['GRUPPEN_LOESCHEN'] == 'True' else "✕",
                        "✓" if entry['GRUPPEN_ERSTELLEN'] == 'True' else "✕",
                        "✓" if entry['GRUPPEN_BEARBEITEN'] == 'True' else "✕",
                        "✓" if entry['ROLLEN_ERSTELLEN'] == 'True' else "✕",
                        "✓" if entry['ROLLEN_BEARBEITEN'] == 'True' else "✕",
                        "✓" if entry['ROLLEN_LOESCHEN'] == 'True' else "✕",
                    ),
                    tags=(tag,)
                )
                i += 1
        update_treeview_with_data()

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
                print(f"Ausgewählter User: {selected_user}")  # Debug
                if selected_user:
                    from .userDetailsWindow import userDetailsWindow, show_user_details
                    show_user_details(selected_user, user_tree, controller)
            except Exception as e:
                print(f"Fehler bei der Auswahl: {e}")

        # Binde die Ereignisfunktion an die Treeview
        role_tree.bind("<Double-1>", on_item_selected)