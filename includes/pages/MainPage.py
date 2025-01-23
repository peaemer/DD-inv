import tkinter as tk
from tkinter import ttk
from customtkinter import CTkEntry
import json
import customtkinter as ctk

from ._sort_tree import sort_column
from includes.sec_data_info import sqlite3api as sqlapi
from .Searchbar import SearchbarLogic as sb
from .Searchbar.Searchbar2 import Searchbar2
from includes.util.Logging import Logger
import cache
from ._styles import *
from .ctk_listbox import *
import includes.sec_data_info.sqlite3api as db
from ._avatarManager import resource_path

logger:Logger = Logger('MainPage')


# Hauptseite (zweites Fenster)
class MainPage(ctk.CTkFrame):
    """
    Die Klasse MainPage repräsentiert die Benutzeroberfläche der Hauptseite der Anwendung.
    """
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.configure(fg_color="white")

        def show_settings_window():
            from .settingsWindow import pop_up_settings
            pop_up_settings(self, controller)

        def show_admin_window():
            from .AdminUserWindow import AdminUserWindow
            controller.show_frame(AdminUserWindow)
            AdminUserWindow.update_treeview_with_data()

        self.show_admin_window = show_admin_window

        def log_out():
            from .LogInWindow import LogInWindow
            cache.user_group = ""  # Benutzergruppe zurücksetzen
            cache.user_name = ""
            controller.show_frame(LogInWindow)

        def search(search_term: str) -> None:
            search_entries = []
            for entry in sqlapi.fetch_hardware():
                for value in entry:
                    if search_term.lower() in str(entry[value]).lower():
                        if entry not in search_entries:
                            search_entries.append(entry)
            self.update_treeview_with_data(data=search_entries)
            tree_frame.tkraise(dropdown_overlay_frame)

        def add_item():
            from addItemPopup import add_item_popup
            """
            Ruft eine Funktion auf, um ein Dialog-Popup für das Hinzufügen eines Eintrags
            zu erstellen.
            """
            add_item_popup(self)
            logger.debug("add_item executed")

        global tree

        # Konfiguriere das Grid-Layout für die Hauptseite
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Erstelle einen Header-Bereich
        self.header_frame = ctk.CTkFrame(self, fg_color="#DF4807")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Konfiguriere die Spalten für den Header
        self.header_frame.grid_columnconfigure(0, weight=1)  # Platz links
        self.header_frame.grid_columnconfigure(1, weight=2)  # Zentrale Spalte
        self.header_frame.grid_columnconfigure(2, weight=1)  # Platz rechts


        self.srh_head = tk.PhotoImage(file=resource_path("./includes/assets/srh.png"))

        # Füge ein zentriertes Label hinzu
        header_label = ctk.CTkLabel(self.header_frame,
                                    image=self.srh_head,
                                    fg_color="#DF4807")
        header_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Erstellen eines Schriftzuges im Header
        text_header_label = ctk.CTkLabel(self.header_frame,
                                         fg_color="#DF4807",
                                         text="Inventur-Übersicht",
                                         font=('Arial', 30),
                                         text_color="white")
        text_header_label.grid(row=0, column=1, padx=0, pady=50, sticky="")

        # Log Out Button
        self.log_out_btn = tk.PhotoImage(file=resource_path("./includes/assets/ausloggen.png"))
        log_out_button = ctk.CTkButton(self.header_frame,
                                       image=self.log_out_btn,
                                       command=log_out,
                                       border_width=0,
                                       cursor="hand2",
                                       fg_color="#DF4807",
                                       hover_color="#DF4807")
        log_out_button.grid(row=0, column=4, sticky="e", padx=20)

        # Avatar Button
        self.main_page_avatar = cache.user_avatar
        main_page_options_button = ctk.CTkButton(self.header_frame,
                                                 image=self.main_page_avatar,
                                                 command=show_settings_window,
                                                 border_width=0,
                                                 cursor="hand2",
                                                 fg_color="#DF4807",
                                                 hover_color="#DF4807")
        main_page_options_button.grid(row=0, column=3, sticky="e", padx=20)

        # Admin Button
        self.admin_btn = tk.PhotoImage(file=resource_path("./includes/assets/Key.png"))

        # Erstellen des Grayframes für die linke Seite
        grey_frame_side = ctk.CTkFrame(self, fg_color="gray")
        grey_frame_side.grid(row=1, column=0, sticky="nsw")
        grey_frame_side.grid_rowconfigure(0, weight=1)
        grey_frame_side.grid_columnconfigure(0, weight=1)

        tree_style_side_tree = CTkListbox
        tree_style_side_tree.configure("Treeview_side",
                                       background="gray",
                                       font=("Arial", 20),
                                       rowheight=40,  # Zeilenhöhe für größere Abstände
                                       selectbackground="blue",  # Markierungshintergrund
                                       selectforeground="white")  # Markierungstextfarbe

        global side_tree
        side_tree = ctk.CTkTabview(grey_frame_side, cursor="hand2")

        # Scrollbar erstellen
        side_tree_scroll = ctk.CTkScrollbar(grey_frame_side, orientation="vertical") #command=side_tree.yview)
        side_tree_scroll.grid(row=0, column=1, sticky="ns")

        #side_tree.configure(yscrollcommand=side_tree_scroll.set)

        #self.update_sidetree_with_data()
        side_tree.grid(row=0, column=0, sticky="wns")

        # Erstellen des MiddleFrame
        middle_frame = ctk.CTkFrame(self, fg_color="white")
        middle_frame.grid(row=1, padx=10, pady=10, column=1, sticky="nesw")

        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(1, weight=1)

        dropdown_overlay_frame = ctk.CTkFrame(middle_frame, fg_color="white")
        search_frame = ctk.CTkFrame(middle_frame, fg_color="white")

        # Hinzufügen Button
        self.add_btn = tk.PhotoImage(file=resource_path("./includes/assets/Erstellen.png"))
        self.add_button = ctk.CTkButton(search_frame,
                                        image=self.add_btn,
                                        border_width=0,
                                        fg_color="white",
                                        cursor="hand2",
                                        hover_color="white",
                                        command=add_item)

        self.search_btn = tk.PhotoImage(file=resource_path("./includes/assets/SearchButton.png"))
        search_button = ctk.CTkButton(search_frame,
                                      image=self.search_btn,
                                      border_width=0,
                                      fg_color="white",
                                      cursor="hand2",
                                      hover_color="white",
                                      command=lambda: search_entry.finish_search(cache.user_name))

        # Hinzufügebare Dropdown-Box
        dropdown = ctk.CTkTabview(dropdown_overlay_frame,
                                  text_color='black',
                                  bg_color="white",
                                  border_color="gray",
                                  corner_radius=10)

        # Such-Eingabe
        search_entry_oval = ctk.CTkEntry(search_frame,
                                         text_color="black",
                                         fg_color="gray",
                                         bg_color="white",
                                         corner_radius=20,
                                         border_width=0,
                                         height=25)
        search_entry = Searchbar2(self, search_frame, dropdown, cache.user_name)

        # Setze die grid layouts für den frame der Suchleiste und den frame des Such-Dropdowns
        dropdown_overlay_frame.grid(row=1, column=0, padx=(77, 166), pady=0, sticky=ctk.N + ctk.W + ctk.E)
        dropdown_overlay_frame.grid_rowconfigure(0, weight=1)
        dropdown_overlay_frame.grid_columnconfigure(0, weight=1)

        search_frame.grid(pady=5, padx=5, row=0, column=0, sticky=ctk.W + ctk.E + ctk.N)
        search_frame.grid_columnconfigure(0, weight=0)
        search_frame.grid_columnconfigure(1, weight=1)
        search_frame.grid_columnconfigure(2, weight=0)

        # Setze die grid Layouts der Buttons und der Suchleiste im search-frame
        search_button.grid(padx=5, pady=5, row=0, column=0)
        self.add_button.grid(padx=10, pady=1, row=0, column=2, sticky="w")
        search_entry.grid(column=1, row=0, columnspan=1, sticky=ctk.W + ctk.E, padx=22, pady=10)
        search_entry_oval.grid(column=1, row=0, columnspan=1, sticky=ctk.W + ctk.E, padx=5, pady=5)
        dropdown.grid(padx=0, pady=5, row=0, column=0, sticky=ctk.W + ctk.E + ctk.N)

        # Binde Funktionen an die Events der Suchleiste
        search_entry_oval.bind('<FocusIn>', lambda _: search_entry.focus())
        search_entry.add_on_focus_in_event(lambda _: dropdown_overlay_frame.tkraise(tree_frame))
        search_entry.add_on_focus_out_event(lambda _: tree_frame.tkraise(dropdown_overlay_frame))
        search_entry.add_on_finish_search_event(lambda _: search(search_entry.get(0.0, 'end-1c')))
        dropdown.add_on_select_event(lambda var: sb.on_dropdown_select(search_entry, username=cache.user_name))
        dropdown.bind("<<ListboxSelect>>", lambda var: tree_frame.tkraise(dropdown_overlay_frame))

        cache.loaded_history = json.loads(
            sqlapi.read_benutzer_suchverlauf(cache.user_name)
            if sqlapi.read_benutzer(cache.user_name) == "" else """[{}]""")
        search_entry.insert(0.0, 'Suche')  # Setze den Platzhalter-Text

        # Style der Tabelle
        tree_style = ctk.CTkStyle()  # Verwende CustomTkinter Style
        tree_style.theme_use("default")  # alt, classic, xpnative, winnative, default
        tree_style.configure("Treeview.Heading", rowheight=50, font=("Arial", 16))
        tree_style.configure("Treeview", rowheight=40, font=("Arial", 14))

        # Frame für die Tabelle und Scrollbar
        tree_frame = ctk.CTkFrame(middle_frame, background="white")
        tree_frame.grid(row=1, column=0, padx=0, pady=0, sticky=ctk.N + ctk.S + ctk.E + ctk.W)

        # Spaltenkonfiguration für das TreeFrame
        tree_frame.grid_rowconfigure(1, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)  # Spalte für die Tabelle
        tree_frame.grid_columnconfigure(1, weight=0)  # Spalte für die Scrollbar (fixiert)

        # Treeview erstellen
        tree = ctk.CTkTreeview(tree_frame,
                               columns=("c1", "c2", "c3", "c4", "c5", "c6", "c7"),
                               style="Treeview",
                               cursor="hand2",
                               show="headings")

        # Scrollbar erstellen
        scroll = ctk.CTkScrollbar(
            tree_frame,
            orientation="vertical",
            command=tree.yview,
            fg_color="white",
            width=20,
            corner_radius=10,
            button_color=srh_grey,
            button_hover_color=srh_orange
        )
        scroll.grid(row=1, column=1, sticky=ctk.N + ctk.S)  # Scrollbar genau neben der Tabelle

        # Treeview mit Scrollbar verbinden
        tree.configure(yscrollcommand=scroll.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        tree.tag_configure("oddrow", background="#f7f7f7")
        tree.tag_configure("evenrow", background="white")

        # Spaltenüberschriften und Konfiguration
        columns = [
            ("# 1", "ID", 40),
            ("# 2", "Service Tag", 130),
            ("# 3", "Typ", 230),
            ("# 4", "Raum", 120),
            ("# 5", "Name", 250),
            ("# 6", "Beschädigung", 300),
            ("# 7", "Ausgeliehen von", 240),
        ]
        for col_id, col_name, col_width in columns:
            tree.column(col_id, anchor=ctk.CENTER, width=col_width)
            tree.heading(col_id, text=col_name, command=lambda c=col_id: sort_column(tree, c, True))

        tree.grid(row=1, column=0, sticky=ctk.N + ctk.S + ctk.E + ctk.W)  # Tabelle vollständig anpassen
        tree.tkraise()
        self.update_treeview_with_data()

        # Funktion für das Ereignis-Binding
        def on_item_selected(event):
            try:
                selected_item = tree.focus()
                logger.debug(f"Selected Item: {selected_item}")
                if selected_item:
                    from .DetailsWindow import DetailsWindow, show_details
                    show_details(selected_item, tree, controller)
            except Exception as e:
                logger.debug(f"Error during selection: {e}")  # Debug

        def on_side_tree_select(event):
            """
            on_side_tree_select(event):
                Wird ausgelöst, wenn ein Element im side_tree ausgewählt wird. Diese
                Methodik ermöglicht:
                - Das Anzeigen aller Daten, wenn "Alle Räume" ausgewählt wird.
                - Das Filtern und Anzeigen von Daten basierend auf dem Raum.
                - Weitere spezifische Filterlogiken, wenn das übergeordnete über den
                  Elternknoten bestimmt wird.

            :Rückgabewerte:
                Keine der Methoden in dieser Klasse gibt Werte zurück.

            :Parameter:
                :param event: Das Ereignisobjekt, das durch die Auswahl eines Elements
                    ausgelöst wird.

            :Erhobene Ausnahmen:
                Keine direkte Fehlerbehandlung wird in der aktuellen Funktionslogik
                implementiert.

            Einschränkungen:
            Die Funktionalität setzt voraus, dass die Methode fetch_all_rooms() und
            fetch_hardware() im Modul 'sqlapi' korrekt implementiert sind und die
            erforderlichen Daten liefern.
            """
            # Hole ausgewähltes Element aus dem side_tree
            selected_item = side_tree.selection()
            if selected_item:
                selected_text = side_tree.item(selected_item, 'text')
                logger.debug(selected_text)
                if selected_text == "Alle Räume":
                    # Alle Daten in der Haupttabelle anzeigen
                    self.update_treeview_with_data()
                elif selected_text in [room['Raum'] for room in sqlapi.fetch_all_rooms()]:
                    # Daten nach Raum filtern
                    filtered_data = []
                    for hw in sqlapi.fetch_hardware():
                        if hw.get("Raum") and hw.get("Raum").startswith(selected_text):
                            filtered_data.append(hw)
                    self.update_treeview_with_data(data=filtered_data)
                else:
                    parent_name = side_tree.item(side_tree.parent(side_tree.selection()[0]),
                                                 'text') if side_tree.selection() else None
                    filtered_data = []
                    for hw in sqlapi.fetch_hardware():
                        if hw.get("Raum") and hw.get("Raum").startswith(parent_name) and hw.get(
                                "Geraetetype") and hw.get("Geraetetype").startswith(selected_text):
                            filtered_data.append(hw)
                    self.update_treeview_with_data(data=filtered_data)

        side_tree.bind("<<TreeviewSelect>>", on_side_tree_select)

        # Binde die Ereignisfunktion an die Treeview
        tree.bind("<Double-1>", on_item_selected)

        def update_sidetree_with_data(self=None, rooms=None):
            logger.debug("update_sidetree_with_data aufgerufen.")  # Debug

            # Treeview leeren
            side_tree.delete(*side_tree.get_children())
            side_tree.insert("", ctk.END, text="Alle Räume")

            # Räume abrufen, wenn keine übergeben wurden
            if rooms is None:
                rooms = sqlapi.fetch_all_rooms()

            # Räume sortieren (alphabetisch nach 'Raum')
            rooms = sorted(rooms, key=lambda r: r['Raum'])

            for room in rooms:
                # Kategorienliste für den aktuellen Raum
                cats = []

                # Raum hinzufügen
                tree_parent = side_tree.insert("", ctk.END, text=room['Raum'])

                # Hardware abrufen und nach Raum filtern
                for hw in sqlapi.fetch_hardware():
                    if hw['Raum'] and hw['Raum'].startswith(room['Raum']):
                        # Kategorie hinzufügen, falls nicht vorhanden
                        if hw['Geraetetype'] not in cats:
                            cats.append(hw['Geraetetype'])

                # Kategorien sortieren und hinzufügen
                for category in sorted(cats):
                    side_tree.insert(tree_parent, ctk.END, text=category)

        def update_profile_picture(self=None):
            main_page_avatar = cache.user_avatar
            main_page_options_button.configure(image=main_page_avatar)

        # Aktualisieren der Data in der Tabelle
        def update_treeview_with_data(self=None, data=None):
            """
            Aktualisiert die Treeview mit den bereitgestellten Daten oder den aus der SQL-API
            abgerufenen Hardwaredaten. Vorhandene Einträge in der Treeview werden geleert und
            ersetzt. Zeilen erhalten je nach ihrer Reihenfolge unterschiedliche Tags
            für alternative Farbmarkierungen.

            :param data: Die zu aktualisierenden Daten, standardmäßig None. Wenn keine Daten
                bereitgestellt werden, werden diese aus der SQL-API abgerufen.
            :type data: Optional[List[Dict[str, Any]]]
            :return: Es wird nichts zurückgegeben.
            """
            # Clear the current treeview contents
            global i
            i = 0
            tree.delete(*tree.get_children())

            # If no data is provided, fetch the data from sqlapi
            if data is None:
                data = sqlapi.fetch_hardware()

            for entry in data:
                i += 1
                if entry['Beschaedigung'] == "None":
                    damage = ""
                else:
                    damage = entry['Beschaedigung']
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                tree.insert(
                    "",
                    "end",
                    values=(entry['ID'], entry['Service_Tag'], entry['Geraetetype'], entry['Raum'],
                            entry['Modell'], damage, entry['Ausgeliehen_von']),
                    tags=(tag,)
                )