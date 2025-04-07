import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

import cache
from includes.util import Paths
from includes.windows import customMessageBoxDelete
from includes.CTkScrollableDropdown import *

from includes.windows.customMessageBoxDelete import *
from includes.windows._sort_tree import sort_column
import includes.sec_data_info.sqlite3api as db
from includes.gui.styles import size_details_window, corner, border, srh_grey, comboborder, srh_grey_hover
from includes.CTkScrollableDropdown import CTkScrollableDropdownFrame

logger:Logger = Logger('DetailsWindow')


def show_details(selected_item, tree: ttk.Treeview, controller):
    """
    Zeigt die Details eines ausgewählten Elements in einer Benutzeroberfläche an. Diese Funktion ruft die Daten
    des ausgewählten Elements aus einer Baumstruktur ab, speichert die ID des Elements im Cache und zeigt die
    Details-Seite mit den aktualisierten Informationen an.

    :param selected_item: Das aktuell ausgewählte Baum-Element.
    :param tree: Die Baumstruktur, welche die zugehörigen Daten enthält.
    :param controller: Der Controller, der für die Navigation und Verwaltung der Frames zuständig ist.
    :return: Gibt keinen Wert zurück.
    """
    # Daten aus der ausgewählten Zeile
    data = tree.item(selected_item, "values")
    logger.debug(f"Data of the selected item: {data}")  # Debug
    cache.selected_ID = data[0]

    controller.show_frame(DetailsWindow)  # Zeige die Details-Seite

    # Frame aktualisieren und anzeigen
    details = controller.frames[DetailsWindow]
    details.update_data(data)  # Methode in DetailsWindow aufrufen


class DetailsWindow(tk.Frame):
    """
    Repräsentiert ein Detailfenster innerhalb einer Tkinter-Applikation.

    Das Detailfenster bietet Funktionen zur Anzeige von Details eines Objekts, Eingabefeldern
    für verschiedene Eigenschaften und eine Baumansicht für datengestützte Tabellendarstellungen.
    Es ermöglicht die Navigation zu anderen Ansichten und konfiguriert eine intuitive Benutzerschnittstelle.

    :ivar controller: Der Controller der Anwendung, der für die Navigation zwischen Fenstern verwendet wird.
    :ivar go_back_btn_details_window: Bildressource für den Zurück-Button.
    :ivar service_tag_entry_details_window: Eingabefeld für den Service Tag.
    :ivar type_entry_details_window: Eingabefeld für den Typ des Objekts.
    :ivar room_combobox_details_window: Eingabefeld für die Rauminformation.
    :ivar name_entry_details_window: Eingabefeld für den Namen.
    :ivar damaged_entry_details_window: Eingabefeld für Informationen über Schäden.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="white")

        def go_back_details_window():
            from .MainPage import MainPage
            update_label.configure(text="")
            controller.show_frame(MainPage)

        def show_settings_window_details_window():
            """
            show_settings_window_details_window()
                Öffnet das Einstellungs-Pop-Up-Fenster im Detailfenster.
            """
            logger.debug("Show settings window details window")
            from SettingsPage import pop_up_settings
            pop_up_settings(self, controller)

        self.go_back_btn_details_window = tk.PhotoImage(file=Paths.assets_path("ArrowLeft.png"))

        initial_entry: dict[str, str] = db.fetch_hardware_by_id(cache.selected_ID)

        # Erstelle einen Header-Bereich
        header_frame_details_window = tk.Frame(self,
            height=10,
            background="#DF4807"
        )
        header_frame_details_window.grid(row=0, column=0,columnspan=2, sticky=tk.W + tk.E + tk.N)

        # Überschrift mittig zentrieren
        header_frame_details_window.grid_columnconfigure(0, weight=1)  # Platz links
        header_frame_details_window.grid_columnconfigure(1, weight=3)  # Überschrift zentriert
        header_frame_details_window.grid_columnconfigure(2, weight=1)  # Option-Button

        # Zentriere das Label in Spalte 1
        header_label_details_window = tk.Label(header_frame_details_window,
            text="Details",
            background="#DF4807",
            foreground="white",
            font=("Arial", 60)
        )
        header_label_details_window.grid(row=0, column=1, pady=40, sticky=tk.W + tk.E)

        # Buttons in Spalten 2 und 3 platzieren
        go_back_button_details_window = tk.Button(header_frame_details_window,
            image=self.go_back_btn_details_window,
            command=go_back_details_window,
            bd=0,
            relief=tk.FLAT,
            bg="#DF4807",
            activebackground="#DF4807"
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

        global tree_details_window
        tree_details_window = ttk.Treeview(tree_frame_details_window,
            columns=("c1", "c2"),
            show="headings",
            height=30
        )

        scroll_details_window = tk.Scrollbar(tree_frame_details_window,
            orient="vertical",
            command=tree_details_window.yview,
            bg="black",
            activebackground="darkblue",
            troughcolor="grey",
            highlightcolor="black",
            width=15,
            borderwidth=1
        )
        scroll_details_window.grid(row=1, column=1, sticky="ns")
        tree_details_window.configure(yscrollcommand=scroll_details_window.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        tree_details_window.tag_configure("oddrow", background="#f7f7f7")
        tree_details_window.tag_configure("evenrow", background="white")

        # Spaltenüberschriften und Konfiguration
        details_window_columns = [
            ("# 1", "ID", 200),
            ("# 2", "Name", 200),
        ]

        for col_id, col_name, col_width in details_window_columns:
            tree_details_window.column(col_id,
                anchor=tk.CENTER,
                width=col_width
            )
            tree_details_window.heading(col_id,
                text=col_name,
                command=lambda c=col_id: sort_column(tree_details_window, c, False)
            )

        tree_details_window.tkraise()
        tree_details_window.grid(row=1, column=0)

        # Input-Frame
        input_frame_details_window = tk.Frame(container_frame, background="white")
        input_frame_details_window.grid(row=0, column=1, pady=20, sticky="nsew")

        input_frame_details_window.grid_columnconfigure(0, weight=1)  # Zentriere das Input-Frame
        input_frame_details_window.grid_columnconfigure(1, weight=1)
        input_frame_details_window.grid_columnconfigure(2, weight=1)

        # Service Tag
        service_tag_label_details_window = tk.Label(input_frame_details_window,
            text="Service Tag",
            font=("Arial", size_details_window),
            background="white"
        )
        service_tag_label_details_window.grid(column=0, row=0, sticky=tk.W + tk.E, padx=20, pady=10)

        self.service_tag_entry_details_window = ctk.CTkEntry(input_frame_details_window,
            font=("Arial", size_details_window),
            corner_radius=corner,
            fg_color=srh_grey,
            text_color="black",
            border_width=border,
        )
        self.service_tag_entry_details_window.delete(0, tk.END)
        self.service_tag_entry_details_window.insert(0, initial_entry['Service_Tag'])
        self.service_tag_entry_details_window.grid(column=1, row=0, sticky=tk.W + tk.E, padx=20, pady=10)

        # Typ
        type_label_details_window = tk.Label(input_frame_details_window,
            text="Typ",
            font=("Arial", size_details_window),
            background="white"
        )
        type_label_details_window.grid(column=0, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        self.type_entry_details_window = ctk.CTkEntry(input_frame_details_window,
            font=("Arial", size_details_window),
            corner_radius=corner,
            fg_color=srh_grey,
            text_color="black",
            border_width=border
        )
        self.type_entry_details_window.delete(0, tk.END)
        self.type_entry_details_window.insert(0, initial_entry['Geraetetype'])
        self.type_entry_details_window.grid(column=1, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        # Raum (Dropdown-Menü)
        room_label_details_window = tk.Label(input_frame_details_window,
            text="Raum",
            background="white",
            font=("Arial", size_details_window)
        )
        room_label_details_window.grid(row=2, column=0, padx=0, pady=20, sticky=tk.W + tk.E)

        # CTkComboBox statt ttk.Combobox
        room_values = []
        for room in db.fetch_all_rooms():
            room_values.append(room['Raum'])

        self.room_combobox_details_window = ctk.CTkComboBox(input_frame_details_window,
            font=("Arial", size_details_window),
            corner_radius=corner,
            button_color=srh_grey,
            fg_color=srh_grey,
            text_color="black",
            border_width=border,
            state="readonly"
        )
        self.room_combobox_details_window.set(initial_entry['Raum'])
        self.room_combobox_details_window.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

        CTkScrollableDropdownFrame(self.room_combobox_details_window,
            values=room_values,
            button_color=srh_grey,  #BUGGY
            frame_corner_radius=corner,
            autocomplete=True,
            fg_color=srh_grey,
            text_color="black",
            frame_border_width=comboborder,
            frame_border_color=srh_grey_hover,
            justify="left"
        )

        self.room_combobox_details_window.set("Raum auswählen")  # Platzhalter

        # Name
        name_label_details_window = tk.Label(input_frame_details_window,
            text="Name",
            font=("Arial", size_details_window),
            background="white"
        )
        name_label_details_window.grid(column=0, row=3, sticky=tk.W + tk.E, padx=20, pady=10)

        self.name_entry_details_window = ctk.CTkEntry(input_frame_details_window,
            font=("Arial", size_details_window),
            corner_radius=corner,
            fg_color=srh_grey,
            text_color="black",
            border_width=border
        )
        self.name_entry_details_window.delete(0, tk.END)
        self.name_entry_details_window.insert(0, initial_entry['Modell'])
        self.name_entry_details_window.grid(column=1, row=3, sticky=tk.W + tk.E, padx=20, pady=10)

        # Beschädigung
        damaged_label_details_window = tk.Label(input_frame_details_window,
            text="Beschädigung",
            font=("Arial", size_details_window),
            background="white"
        )
        damaged_label_details_window.grid(column=0, row=4, sticky=tk.W + tk.E, padx=20, pady=10)

        self.damaged_entry_details_window = ctk.CTkEntry(input_frame_details_window,
            font=("Arial", size_details_window),
            corner_radius=corner,
            fg_color=srh_grey,
            text_color="black",
            border_width=border
        )
        self.damaged_entry_details_window.delete(0, tk.END)
        self.damaged_entry_details_window.insert(0,initial_entry['Beschaedigung'])
        self.damaged_entry_details_window.grid(column=1, row=4, sticky=tk.W + tk.E, padx=20, pady=10)

        update_label = tk.Label(input_frame_details_window,
            text="",
            background="white",
            cursor="hand2",
            fg="darkred",
            font=("Arial", 22)
        )
        update_label.grid(row=5, column=0, columnspan=2, padx=0, pady=20, sticky="ew")

        # Funktion zum Eintrag hinzufügen
        def refresh_entry():
            """
                reads new data out of all the entries if the content of an entry
                doesn't match the data onside the database, the new data is written to the database
            """
            #update


            type:str = self.type_entry_details_window.get() if self.type_entry_details_window.get() not in [None, '', ' ', initial_entry['Geraetetype']] else initial_entry['Geraetetype']
            room:str = self.room_combobox_details_window.get() if self.room_combobox_details_window.get() not in [None, '', ' ', initial_entry['Raum']] else initial_entry['Raum']
            name:str = self.name_entry_details_window.get() if self.name_entry_details_window.get() not in [None, '', ' ', initial_entry['Modell']] else initial_entry['Modell']
            service_tag:str = self.service_tag_entry_details_window.get() if self.service_tag_entry_details_window.get() != initial_entry['Service_Tag'] else initial_entry['Service_Tag']
            damage:str = self.damaged_entry_details_window.get() if self.damaged_entry_details_window.get() != initial_entry['Beschaedigung'] else initial_entry['Beschaedigung']

            #logger.debug(f"damage:{damage}")
            answer = db.update_hardware_by_id(
                cache.selected_ID,
                neue_beschaedigung=damage,
                neuer_standort=room,
                neuer_service_tag=service_tag,
                neues_modell=name,
                neuer_geraetetyp=type)

            logger.debug(f"""db.update_hardware_by_id:{answer}""")

            from .MainPage import MainPage
            MainPage.update_sidetree_with_data()
            update_label.configure(text=answer)

        def lend(data):
            logger.debug(f"Übergebene Daten: {data}")
            from includes.windows.lendPopup import lend_popup
            lend_popup(self, data, controller)

        def return_item(data):
            db.update_hardware_by_id(cache.selected_ID, neue_ausgeliehen_von="")
            from .MainPage import MainPage
            MainPage.update_treeview_with_data()
            controller.show_frame(MainPage)

        def delete_entry():
            db.delete_hardware_by_id(cache.selected_ID)
            from .MainPage import MainPage
            db.delete_hardware_by_id(cache.selected_ID)
            MainPage.update_treeview_with_data()
            MainPage.update_sidetree_with_data()
            update_label.configure(text="")
            controller.show_frame(MainPage)

        self.edit_btn = tk.PhotoImage(file=Paths.assets_path("Aktualisieren.png"))
        self.lend_btn = tk.PhotoImage(file=Paths.assets_path("Ausleihen.png"))
        self.delete_btn = tk.PhotoImage(file=Paths.assets_path("Loeschen.png"))
        self.return_btn = tk.PhotoImage(file=Paths.assets_path("Zurueckgeben.png"))

        # Buttons in ein separates Frame
        global button_frame_add_item_popup, lend_button, ret_button, delete_button, edit_button
        button_frame_add_item_popup = tk.Frame(self, background="white")
        button_frame_add_item_popup.grid(row=2, column=0, pady=20)

        lend_button = tk.Button(button_frame_add_item_popup,
            image=self.lend_btn,
            bd=0,
            relief=tk.FLAT,
            bg="white",
            activebackground="white",
            cursor="hand2",
            command=lambda: lend({"name": self.name_entry_details_window.get()}))

        ret_button = tk.Button(button_frame_add_item_popup,
            image=self.return_btn,
            bd=0,
            relief=tk.FLAT,
            bg="white",
            activebackground="white",
            cursor="hand2",
            command=lambda: return_item({"name": self.name_entry_details_window.get()}))

        def customMessageBoxCall():
            if customMessageBoxDelete(self,
                title="Aktion Bestätigen",
                message="Willst du diesen Eintrag unwiderruflich löschen?",
                buttonText="Eintrag Löschen"):
                delete_entry()

        delete_button = tk.Button(button_frame_add_item_popup,
            image=self.delete_btn,
            cursor="hand2",
            bd=0,
            relief=tk.FLAT,
            bg="white",
            activebackground="white",
            command=customMessageBoxCall)

        edit_button = tk.Button(button_frame_add_item_popup,
            image=self.edit_btn,
            cursor="hand2",
            bd=0,
            relief=tk.FLAT,
            bg="white",
            activebackground="white",
            command=refresh_entry
        )

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(0, weight=1)


    def update_data(self, data):
        """
        Aktualisiert die Daten in den Eingabefeldern des Fensters mit den übergebenen
        Daten aus der Liste. Vorhandene Eingaben in den Feldern werden gelöscht und
        ersetzt.

        :param data: Eine Liste mit Werten, die in die Eingabefelder eingefügt werden.
                     Die Liste muss folgende Indizes enthalten:
                     - Index 1: Wert für das Service-Tag-Eingabefeld
                     - Index 2: Wert für das Typ-Eingabefeld
                     - Index 3: Wert für das Raum-Eingabefeld
                     - Index 4: Wert für das Namens-Eingabefeld
                     - Index 5: Wert für das Beschädigungs-Eingabefeld
        :return: es wird kein Wert zurückgegeben.
        """
        global i
        i = 0
        tree_details_window.delete(*tree_details_window.get_children())
        if db.fetch_ausleih_historie():
            for entry in db.fetch_ausleih_historie():
                if entry["Hardware_ID"] == cache.selected_ID:
                    i += 1
                    tag = "evenrow" if i % 2 == 0 else "oddrow"
                    tree_details_window.insert(
                        "",
                        "end",
                        values=(entry['Ausgeliehen_am'], entry['Nutzername']),
                        tags=(tag,)
                    )

        if cache.user_group_data['ENTRY_LOESCHEN'] == "False":
            delete_button.pack_forget()
        else:
            delete_button.pack(side=tk.LEFT, padx=20)  # Neben Exit-Button platzieren
        if cache.user_group_data['ENTRY_BEARBEITEN'] == "False":
            edit_button.pack_forget()
        else:
            edit_button.pack(side=tk.LEFT, padx=20)  # Links platzieren

        if (db.fetch_hardware_by_id(cache.selected_ID)['Ausgeliehen_von'] == ""
                or db.fetch_hardware_by_id(cache.selected_ID)['Ausgeliehen_von'] == " "):
            lend_button.pack_forget()
            ret_button.pack_forget()
            lend_button.pack(side=tk.LEFT, padx=20)  # Neben Exit-Button platzieren
        else:
            lend_button.pack_forget()
            ret_button.pack_forget()
            ret_button.pack(side=tk.LEFT, padx=20)  # Neben Exit-Button platzieren

        # Daten in die Entry-Felder einfügen
        self.service_tag_entry_details_window.delete(0, tk.END)
        self.service_tag_entry_details_window.insert(0, data[1])

        self.type_entry_details_window.delete(0, tk.END)
        self.type_entry_details_window.insert(0, data[2])

        self.room_combobox_details_window.set(data[3])

        self.name_entry_details_window.delete(0, tk.END)
        self.name_entry_details_window.insert(0, data[4])

        self.damaged_entry_details_window.delete(0, tk.END)
        self.damaged_entry_details_window.insert(0, data[5])
