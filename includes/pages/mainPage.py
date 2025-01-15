import tkinter as tk
from shutil import which
from tkinter import ttk
from tkinter import *

from customtkinter import CTkEntry

from includes.sec_data_info import sqlite3api as sqlapi
from .Searchbar import SearchbarLogic as sb
from .Searchbar.Searchbar2 import Searchbar2
from .Searchbar.Logging import Logger
import cache
from ._styles import *
import customtkinter as ctk
from customtkinter.windows.widgets.ctk_textbox import CTkTextbox
import json
from .ctk_listbox import *



# Hauptseite (zweites Fenster)
class mainPage(tk.Frame):
    """
    Die Klasse mainPage repräsentiert die Benutzeroberfläche der Hauptseite der Anwendung.

    Die Hauptseite dient als zentrale Übersicht für die Inventur. Sie enthält mehrere
    wichtige Funktionen wie die Möglichkeit, nach Elementen zu suchen, neue Elemente hinzuzufügen,
    sich auszuloggen, und verschiedene Optionen und Einstellungen anzuzeigen. Die Benutzeroberfläche
    besteht aus mehreren geordneten Abschnitten wie dem Header, einer Seitenleiste und einem
    mittleren Bereich zur Anzeige der Inhalte. Dabei wird ein Grid-Layout verwendet, um die Widgets
    entsprechend ihrer Funktionalität und Position anzuordnen.

    :ivar header_frame: Frame-Widget, das den Header-Bereich der Hauptseite darstellt.
    :type header_frame: tk.Frame
    :ivar srh_head: Bildobjekt, das zur Anzeige eines Logos im Header verwendet wird.
    :type srh_head: tk.PhotoImage
    :ivar log_out_btn: Bildobjekt für den Log-Out-Button.
    :type log_out_btn: tk.PhotoImage
    :ivar opt_btn: Bildobjekt für den Button, um die Einstellungen zu öffnen.
    :type opt_btn: tk.PhotoImage
    :ivar admin_btn: Bildobjekt für den Button, um den Admin-Bereich zu öffnen.
    :type admin_btn: tk.PhotoImage
    :ivar add_btn: Bildobjekt für den Button, um ein neues Element hinzuzufügen.
    :type add_btn: tk.PhotoImage
    :ivar search_btn: Bildobjekt für den Such-Button.
    :type search_btn: tk.PhotoImage
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")

        def show_settings_window():
            """
            Repräsentiert die Hauptseite der Anwendung, die als Frame innerhalb einer
            tkinter-Anwendung konzipiert ist. Diese Klasse dient als Hauptcontainer für
            Inhalte und verwaltet die Navigation zu anderen Fenstern oder Frames.

            :cvar parent: Der übergeordnete tkinter-Widget, in dem die Hauptseite angezeigt wird.
            :cvar controller: Der Controller, der die Navigation zwischen den Seiten steuert.
            """
            from .settingsWindow import pop_up_settings
            pop_up_settings(self, controller)

        def show_admin_window():
            """
            Diese Klasse repräsentiert die Hauptrahmenseite der Anwendung und erbt von
            `tk.Frame`. Sie dient als Grundlage für die GUI-Komponente und ermöglicht
            die Navigation zwischen verschiedenen Seiten oder Fenstern durch den
            Controller.

            Der Hauptfokus dieser Klasse ist die Integration der Administrations-
            Fensteransicht durch die Methode `show_admin_window`.
            """
            from .adminUserWindow import adminUserWindow
            controller.show_frame(adminUserWindow)
            adminUserWindow.update_treeview_with_data()

        # Speichere die Funktion als Attribut, um später darauf zuzugreifen
        self.show_admin_window = show_admin_window

        def log_out():
            """
            Eine Klasse, die das Hauptseiten-Frame darstellt und verwendet wird, um
            den Benutzer zwischen verschiedenen Ansichten zu navigieren. Diese Klasse
            enthält die Hauptlogik für den Vorgang beim Ausloggen.

            :ivar parent: Die Elternkomponente, auf der dieses Frame basiert.
            :ivar controller: Der Controller, der die Navigation zwischen verschiedenen Frames verwaltet.
            """
            from .logInWindow import logInWindow
            cache.user_group = ""  # Benutzergruppe zurücksetzen
            cache.user_name = ""
            controller.show_frame(logInWindow)

        def search(search_term:str) -> None:
            """

            """
            search_entries = []
            for entry in sqlapi.fetch_hardware():
                for value in entry:
                    if search_term.lower() in str(entry[value]).lower():
                        if entry not in search_entries:
                            search_entries.append(entry)
            self.update_treeview_with_data(data=search_entries)
            tree_frame.tkraise(dropdown_overlay_frame)

        def add_item():
            """
            Eine Klasse, die die Hauptseite einer Anwendung darstellt und eine entsprechende grafische Benutzeroberfläche
            bereitstellt. Die Klasse erbt von `tk.Frame` und wird innerhalb eines tkinter-Anwendungsrahmens verwendet.

            Die Klasse enthält eine Methode zur Initialisierung des Layouts und eine Hilfsmethode, um ein Popup-Fenster
            zum Hinzufügen eines Eintrags anzuzeigen.

            Attributes:
                parent: Das übergeordnete tkinter-Widget, innerhalb dessen der Rahmen liegt.
                controller: Eine Controller-Instanz, die die Navigation oder Steuerung zwischen
                            verschiedenen Anwendungsseiten ermöglicht.

            Methoden:
                add_item:
                    Ruft eine Funktion auf, um ein Dialog-Popup für das Hinzufügen eines Eintrags
                    zu erstellen.

            :param parent: Das Eltern-Widget für den tkinter-Rahmen.
            :type parent: tk.Widget
            :param controller: Der Controller für die Navigation und Steuerung.
            :type controller: object
            """
            from .addItemPopup import add_item_popup
            add_item_popup(self)
            print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: add_item executed")  # Debug

        global tree

        # Konfiguriere das Grid-Layout für die Hauptseite
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Erstelle einen Header-Bereich
        self.header_frame = tk.Frame(self, background="#DF4807")
        self.header_frame.grid(row=0, column=0,columnspan=2, sticky=tk.W + tk.E)

        # Konfiguriere die Spalten für den Header
        self.header_frame.grid_columnconfigure(0, weight=1)  # Platz links
        self.header_frame.grid_columnconfigure(1, weight=2)  # Zentrale Spalte
        self.header_frame.grid_columnconfigure(2, weight=1)  # Platz rechts
        self.header_frame.grid_rowconfigure(0, weight=1)
        from ._avatarManager import resource_path
        self.srh_head = tk.PhotoImage(file=resource_path("./includes/assets/srh.png"))

        # Füge ein zentriertes Label hinzu
        header_label = tk.Label(self.header_frame, image=self.srh_head, background="#DF4807", foreground="white")
        header_label.grid(row=0, column=0, padx=20, pady=20, sticky=tk.W)

        # Erstellen eines Schriftzuges im Header
        text_header_label = tk.Label(self.header_frame, background="#DF4807", text="Inventur-Übersicht", font=('Arial', 30), foreground="white")
        text_header_label.grid(row=0, column=1, padx=0, pady=50, sticky="")

        # Konvertiere das Bild für Tkinter
        self.log_out_btn = tk.PhotoImage(file=resource_path("./includes/assets/ausloggen.png"))

        # Füge einen Button mit dem Bild hinzu
        log_out_button = tk.Button(self.header_frame,
                                   image=self.log_out_btn,
                                   command=log_out,
                                   bd=0,
                                   relief=tk.FLAT,
                                   bg="#DF4807",
                                   activebackground="#DF4807")
        log_out_button.grid(row=0, column=4, sticky=tk.E, padx=20)

        # Konvertiere das Bild für Tkinter
        self.main_page_avatar = cache.user_avatar

        # Füge einen Button mit dem Bild hinzu
        global main_page_options_button
        main_page_options_button = tk.Button(self.header_frame,
                                   image=self.main_page_avatar,
                                   command=show_settings_window,
                                   bd=0,
                                   relief=tk.FLAT,
                                   bg="#DF4807",
                                   activebackground="#DF4807")
        main_page_options_button.grid(row=0, column=3, sticky=tk.E, padx=20)

        # Platzieren des Adminbuttons
        from ._avatarManager import resource_path
        self.admin_btn = tk.PhotoImage(file=resource_path("./includes/assets/Key.png"))

        # Erstellen des Grayframes für linke Seite
        grey_frame_side = tk.Frame(self, background=srhGrey)
        grey_frame_side.grid(row=1, column=0, sticky="nsw")
        grey_frame_side.grid_rowconfigure(0, weight=1)
        grey_frame_side.grid_columnconfigure(0, weight=1)

        tree_style_side_tree = ttk.Style()
        tree_style_side_tree.theme_use("default")
        tree_style_side_tree.configure("Treeview_side",
                                       background=srhGrey,
                                       font=("Arial", 20),
                                       rowheight=40,  # Zeilenhöhe für größere Abstände
                                       selectbackground="blue",  # Markierungshintergrund
                                       selectforeground="white")  # Markierungstextfarbe
        tree_style_side_tree.layout("Treeview_side", [('Treeview.treearea', {'sticky': 'nswe'})])

        # Treeview erstellen
        global side_tree
        side_tree = ttk.Treeview(grey_frame_side, show="tree", style="Treeview_side")


        # Scrollbar erstellen
        side_tree_scroll = ctk.CTkScrollbar(
            grey_frame_side,
            orientation="vertical",
            command=side_tree.yview,
            fg_color="white",
            width=0,                                                # <--- +++++side scrollbar visibility+++++ #
            corner_radius=10,
            button_color = srhGrey,
            button_hover_color="#2980b9"
        )
        side_tree_scroll.grid(row=0, column=1, sticky=tk.N + tk.S)  # Scrollbar genau neben der Tabelle

        # Treeview mit Scrollbar verbinden
        side_tree.configure(yscrollcommand=side_tree_scroll.set)

        self.update_sidetree_with_data()
        side_tree.grid(row=0, column=0, sticky=tk.W + tk.N + tk.S)

        # Erstellen des MiddleFrame
        middle_frame = tk.Frame(self, bg="white")
        middle_frame.grid(row=1, padx=10, pady=10, column=1, sticky="nesw")

        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(1, weight=1)



        # Dbug Info Anzeige der Fenstergroesse
        def show_size(event):
            """
            Diese Klasse mainPage stellt ein GUI-Frame dar, das in einer tkinter-Anwendung
            verwendet wird. Es dient als Rahmen für Widgets und enthält Methoden, um auf
            Ereignisse zu reagieren, wie zum Beispiel Änderungen der Fenstergröße.

            :param parent: Der übergeordnete Widget-Container, zu dem dieses Frame gehört.
            :type parent: tk.Widget
            :param controller: Ein Objekt, das als Controller für Navigation oder
                               Steuerungslogik dient.
            :type controller: Objekt

            :method show_size: Eine Methode zur Handhabung von Ereignissen, bei denen die
                               Größe des Fensters geändert wird. Sie gibt die neuen
                               Breiten- und Höhenwerte des Ereignisses aus.
            :param event: Das Ereignisobjekt, das von tkinter übergeben wird und
                          Informationen über das Größenänderungsereignis enthält.
            :type event: tk.Event
            """
            print(f"New size - Width: {event.x} Height: {event.y}") #Debug
        #print(f"{debug_ANSI_style+"DEBUG"+ANSI_style_END}:", show_size) # Debug

        dropdown_overlay_frame: tk.Frame = tk.Frame(middle_frame, background="white")
        search_frame: tk.Frame= tk.Frame(middle_frame, bg="white")

        #erstelle den hinufügen-button im auf dem search frame
        self.add_btn = tk.PhotoImage(file=resource_path("./includes/assets/Erstellen.png"))
        self.add_button = tk.Button(search_frame, image=self.add_btn, bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=add_item)
        self.search_btn = tk.PhotoImage(file=resource_path("./includes/assets/SearchButton.png"))
        search_button = tk.Button(search_frame, image=self.search_btn, bd=0, relief=tk.FLAT, bg="white", activebackground="white",command=lambda:search_entry.finish_search(cache.user_name))

        #erstelle den hinufügen-button im auf dem search frame
        dropdown: CTkListbox = CTkListbox(dropdown_overlay_frame, font=("Arial", 20), text_color='black', bg_color="white",border_color=srhGrey, corner_radius=10, scrollbar_fg_color="white", scrollbar_button_color='white', scrollbar_button_hover_color='white')
        search_entry_oval:CTkEntry = CTkEntry(search_frame, text_color="black", fg_color=srhGrey, bg_color="white", font=("Arial", 26), corner_radius=20, border_width=0, height=25)
        search_entry:Searchbar2 = Searchbar2(self, search_frame, dropdown, cache.user_name)

        #setze die grid layouts für den frame der Suchleiste und den frame des such-dropdowns
        dropdown_overlay_frame.grid(row=1, column=0, padx=(77, 166), pady=0, sticky=tk.N + tk.W + tk.E)
        dropdown_overlay_frame.grid_rowconfigure(0, weight=1)
        dropdown_overlay_frame.grid_columnconfigure(0, weight=1)

        search_frame.grid(pady=5, padx=5, row=0, column=0, sticky=tk.W + tk.E + tk.N)
        search_frame.grid_columnconfigure(0, weight=0)
        search_frame.grid_columnconfigure(1, weight=1)
        search_frame.grid_columnconfigure(2, weight=0)

        # setze die grid Layaouts der buttons und der Suchleiste im search-frame
        search_button.grid(padx=5, pady=5, row=0, column=0)
        self.add_button.grid(padx=10, pady=1, row=0, column=2, sticky="w")
        search_entry.grid(column=1, row=0, columnspan=1, sticky=tk.W + tk.E, padx=22, pady=10)
        search_entry_oval.grid(column=1, row=0, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)
        dropdown.grid(padx=0, pady=5, row=0, column=0, sticky=tk.W + tk.E + tk.N)

        #binde Funktionen an die events der Suchleiste
        search_entry_oval.bind('<FocusIn>', lambda  _: search_entry.focus())
        search_entry.add_on_focus_in_event(lambda  _: dropdown_overlay_frame.tkraise(tree_frame))
        search_entry.add_on_focus_out_event(lambda _: tree_frame.tkraise(dropdown_overlay_frame))
        search_entry.add_on_finish_search_event(lambda _: search(search_entry.get(0.0,'end-1c')))
        dropdown.bind("<<ListboxSelect>>", lambda var: sb.on_dropdown_select(search_entry, dropdown, cache.user_name))
        dropdown.bind("<<ListboxSelect>>", lambda var: tree_frame.tkraise(dropdown_overlay_frame))

        cache.loaded_history = json.loads(
            sqlapi.read_benutzer_suchverlauf(cache.user_name) if sqlapi.read_benutzer(cache.user_name) == "" else """[{}]""")
        search_entry.insert(0.0, 'Suche')  # Setze den Platzhalter-Text

        # style der Tabelle
        tree_style = ttk.Style()
        tree_style.theme_use("default") #alt, classic,xpnative,winnative, default
        tree_style.configure("Treeview.Heading",rowheight=50, font=("Arial", 16))
        tree_style.configure("Treeview", rowheight=40, font=("Arial", 14))

        # Frame für die Tabelle und Scrollbar
        tree_frame = tk.Frame(middle_frame, background="white")
        tree_frame.grid(row=1, column=0, padx=0, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # Spaltenkonfiguration für das TreeFrame
        tree_frame.grid_rowconfigure(1, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)  # Spalte für die Tabelle
        tree_frame.grid_columnconfigure(1, weight=0)  # Spalte für die Scrollbar (fixiert)

        # Treeview erstellen
        tree = ttk.Treeview(tree_frame, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"),style="Treeview", show="headings")

        # Scrollbar erstellen
        scroll = ctk.CTkScrollbar(
            tree_frame,
            orientation="vertical",
            command=tree.yview,
            fg_color="white",
            width=20,
            corner_radius=10,
            button_color = srhGrey,
            button_hover_color="#2980b9"
        )
        scroll.grid(row=1, column=1, sticky=tk.N + tk.S)  # Scrollbar genau neben der Tabelle

        # Treeview mit Scrollbar verbinden
        tree.configure(yscrollcommand=scroll.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        tree.tag_configure("oddrow", background="#f7f7f7")
        tree.tag_configure("evenrow", background="white")

        # listbox for directories
        tree.column("# 1", anchor=CENTER, width=40)
        tree.heading("# 1", text="ID")
        tree.column("# 2", anchor=CENTER, width=130)
        tree.heading("# 2", text="Service Tag")
        tree.column("# 3", anchor=CENTER, width=230)
        tree.heading("# 3", text="Typ")
        tree.column("# 4", anchor=CENTER, width=120)
        tree.heading("# 4", text="Raum")
        tree.column("# 5", anchor=CENTER, width=250)
        tree.heading("# 5", text="Name")
        tree.column("# 6", anchor=CENTER, width=300)
        tree.heading("# 6", text="Beschädigung")
        tree.column("# 7", anchor=CENTER, width=240)
        tree.heading("# 7", text="Ausgeliehen von")
        tree.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)  # Tabelle vollständig anpassen
        tree.tkraise()
        self.update_treeview_with_data()

        # Funktion für das Ereignis-Binding
        def on_item_selected(event):
            """
            Hauptseite eines GUI-Frameworks basierend auf tkinter.

            Diese Klasse stellt die Hauptseite dar, die eine Benutzeroberfläche für die
            Navigation und Anzeige spezifischer Detailinformationen bereitstellt.
            """

            try:
                selected_item = tree.focus()
                print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: Selected Item: {selected_item}")
                if selected_item:
                    from .detailsWindow import detailsWindow, show_details
                    show_details(selected_item, tree, controller)
            except Exception as e:
                print(f"Error during selection: {e}") #Debug


        def on_side_tree_select(event):
            """
            Hauptseite für die Anwendung. Diese Klasse erstellt die Hauptansicht für das
            Programm und erlaubt Benutzern, durch die Auswahl eines Elements aus dem
            Baum (side_tree) entsprechende Daten in der Hauptansicht (treeview) anzuzeigen.

            :Attributes:
                parent: Die Elterninstanz oder der übergeordnete Container, in dem diese
                    Seite eingebettet ist.
                controller: Der zentrale Steuerungsmechanismus, der zwischen den
                    verschiedenen Seiten der Anwendung vermittelt.

            :Methode:
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
                print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: ", selected_text)
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
                    parent_name = side_tree.item(side_tree.parent(side_tree.selection()[0]),'text') if side_tree.selection() else None
                    filtered_data = []
                    for hw in sqlapi.fetch_hardware():
                        if hw.get("Raum") and hw.get("Raum").startswith(parent_name) and hw.get("Geraetetype") and hw.get("Geraetetype").startswith(selected_text):
                            filtered_data.append(hw)
                    self.update_treeview_with_data(data=filtered_data)

        side_tree.bind("<<TreeviewSelect>>", on_side_tree_select)

        # Binde die Ereignisfunktion an die Treeview
        tree.bind("<Double-1>", on_item_selected)

    def update_sidetree_with_data(self = None, rooms = None):
        print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: update_sidetree_with_data aufgerufen.") # Debug
        side_tree.delete(*side_tree.get_children())
        side_tree.insert("", tk.END, text="Alle Räume")
        if rooms is None:
            rooms = sqlapi.fetch_all_rooms()
        for room in rooms:
            cats = []
            tree_parent = side_tree.insert("", tk.END, text=room['Raum'])
            for hw in sqlapi.fetch_hardware():
                if hw['Raum'] and hw['Raum'].startswith(room['Raum']):
                    if not hw['Geraetetype'] in cats:
                        cats.append(hw['Geraetetype'])
                        side_tree.insert(tree_parent, tk.END, text=hw['Geraetetype'])

    def update_profile_picture(self=None):
        main_page_avatar = cache.user_avatar
        main_page_options_button.configure(image=main_page_avatar)

    # Aktualisieren der Data in der Tabelle
    def update_treeview_with_data(self = None, data=None):
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
            i+=1
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

    def on_load(self):
        """
        Überprüft beim Laden die Benutzergruppe des aktuellen Nutzers und entscheidet, ob
        ein Admin-Button erstellt, angezeigt oder entfernt werden soll. Der Admin-Button wird
        nur für Nutzer der Gruppe "Admin" sichtbar und ermöglicht den Zugriff auf zusätzliche
        Administrationsfunktionen. Danach wird die Anzeige des Treeviews aktualisiert.

        :param self: Das aktuelle Objekt, das Zugriff auf die Eigenschaften und Methoden
            der Klasse hat.

        Attribute
        ---------
        admin_button : tk.Button
            Eine Referenz auf den Admin-Button, falls dieser erstellt wurde.

        admin_btn : Bild
            Das Bild, das im Admin-Button angezeigt wird.

        header_frame : Frame
            Der Frame, in dem der Admin-Button positioniert wird.

        user_group : str
            Die Benutzergruppe des aktuellen Nutzers, die aus dem `cache` geladen wird.

        Returns
        -------
        None
            Diese Methode gibt keinen Wert zurück.
        """

        # Überprüfe die Benutzergruppe
        if cache.user_group_data['ENTRY_ERSTELLEN'] == "True":
            self.add_button.grid(padx=10, pady=1, row=0, column=2, sticky="w")
        else:
            self.add_button.grid_forget()
        if cache.user_group_data['ADMIN_FEATURE'] == "True":
            print("DEBUG: Admin")
            # Überprüfe, ob der Admin-Button bereits existiert
            if not hasattr(self, "admin_button"):
                # Erstelle den Admin-Button, wenn er noch nicht existiert
                self.admin_button = tk.Button(
                    self.header_frame,
                    image=self.admin_btn,
                    command=self.show_admin_window,  # Funktion für Admin-Button
                    bd=0,
                    relief=tk.FLAT,
                    bg="#DF4807",
                    activebackground="#DF4807"
                )
                self.admin_button.grid(row=0, column=2, sticky=tk.E, padx=20)
            else:
                self.admin_button.grid(row=0, column=2, sticky=tk.E, padx=20)
        else:
            # Entferne den Admin-Button, falls er existiert
            if hasattr(self, "admin_button"):
                print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: Removed Admin window") #Debug
                self.admin_button.grid_remove()

        self.update_treeview_with_data()