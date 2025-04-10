import tkinter
from tkinter import ttk
from typing import Any, Callable
from abc import ABC, abstractmethod

import customtkinter
import cache
from includes.CTkScrollableDropdown import CTkScrollableDropdownFrame
from includes.util import Paths
from includes.windows import MainPage
from main import DDInv
from ...popups.customMessageBoxDelete import *

from includes.logic.sort_tree import sort_column
from includes.gui.styles import *
from includes.util.Logging import Logger
import includes.sec_data_info.sqlite3api as db

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


class DetailsWindow(tk.Frame, ABC):
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
        """."""
        tk.Frame.__init__(self, parent)

        self.controller:DDInv = controller
        self.configure(background="white")

        self.__tree_frame:tkinter.Frame = tkinter.Frame(self)
        self.__action_frame:tkinter.Frame = tkinter.Frame(self)

        self.action_items:dict[str, tkinter.Button|tkinter.Label|customtkinter.CTkEntry] = {}



        self.__tree_frame.grid(row=0, column=0, sticky="nsew")
        self.__tree_frame.grid(row=0, column=1, sticky="nsew")

        def go_back_details_window():
            from ..MainPage import MainPage
            update_label.configure(text="")
            controller.show_frame(MainPage)

        def show_settings_window_details_window():
            """
            show_settings_window_details_window()
                Öffnet das Einstellungs-Pop-Up-Fenster im Detailfenster.
            """
            logger.debug("Show settings window details window")
            from ...popupFrames.PopupFrameSupport import PopupFrameSupport
            #pop_up_settings(self, controller)

        self.go_back_btn_details_window = tk.PhotoImage(file=Paths.assets_path("./includes/assets/ArrowLeft.png"))

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

        self.service_tag_entry_details_window = customtkinter.CTkEntry(input_frame_details_window,
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

        self.type_entry_details_window = customtkinter.CTkEntry(input_frame_details_window,
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

        self.room_combobox_details_window = customtkinter.CTkComboBox(input_frame_details_window,
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

        self.name_entry_details_window = customtkinter.CTkEntry(input_frame_details_window,
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

        self.damaged_entry_details_window = customtkinter.CTkEntry(input_frame_details_window,
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

            self.controller.get_page_instance(MainPage).update_sidetree_with_data()
            update_label.configure(text=answer)

        def lend(data):
            logger.debug(f"Übergebene Daten: {data}")
            from includes.windows.lendPopup import lend_popup
            lend_popup(self, data, controller)

        def return_item(data):
            db.update_hardware_by_id(cache.selected_ID, neue_ausgeliehen_von="")
            from includes.gui.pages.MainPage import MainPage
            self.controller.get_page_instance(MainPage).update_sidetree_with_data()
            controller.show_frame(MainPage)

        def delete_entry():
            db.delete_hardware_by_id(cache.selected_ID)
            from includes.gui.pages.MainPage import MainPage
            self.controller.get_page_instance(MainPage).update_sidetree_with_data()
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

    @abstractmethod
    def setup_action_frame(self, frame:tkinter.Frame):
        """
            .
        """
        pass

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


import tkinter
import customtkinter
from abc import ABC, abstractmethod

class DetailsWindow(tkinter.Frame, ABC):
    """
        This is the base class for all window frames. It sets up the general arrangement of the frames of the Window.
        The frames are the header frame at the top of the window, the two sidebar frames and the main frame in the
        middle of the window. Classes that inherit from IWindow can access these frames only through the setup methods.
        The frames are created inside the constructor of IWindow.
    """

    self.go_back_btn_details_window = tk.PhotoImage(file=resource_path("./includes/assets/ArrowLeft.png"))

    # Erstelle einen Header-Bereich
    header_frame_details_window = tk.Frame(self,
                                           height=10,
                                           background="#00699a"
                                           )
    header_frame_details_window.grid(row=0, column=0, columnspan=2, sticky=tk.W + tk.E + tk.N)

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

    # Nutzername
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

    # Passwort
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

    # Email
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

    # Rolle
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
                               button_color=srh_grey,  # BUGGY
                               frame_corner_radius=corner,
                               fg_color=srh_grey,
                               text_color="black",
                               frame_border_width=comboborder,
                               frame_border_color=srh_grey_hover,
                               justify="left"
                               )

    def __setup_action_buttons(self):
        pass

    def __setup_sidebar(self):
        pass

    def enable_treeview(
            self,
            get_data_callback:Callable[[],list[dict[str,str]]],
            on_cell_click_callback:Callable[[dict[str,str]],None],
            tree_structure:dict[str,int]
    ):
        """
            .
        """
        self.__treeview_enabled = True
        self.__treeview_structure = tree_structure

        self.treeview:ttk.Treeview = ttk.Treeview(
            self.__center_frame,
            columns=tuple([f"c{i}" for i in range(0,len(tree_structure if tree_structure else self.__treeview_structure))]),
            show="headings"
        )

        self.tree_scrollbar = customtkinter.CTkScrollbar(
            self.__center_frame,
            orientation="vertical",
            command=self.treeview.yview,
            fg_color="white",
            width=20,  # <--- +++++side scrollbar visibility+++++ #
            corner_radius=scroll_corner,
            button_color=srh_grey,
            button_hover_color=srh_blue
        )
        self.horizontal_tree_scrollbar = customtkinter.CTkScrollbar(
            self.__center_frame,
            orientation="horizontal",
            command=self.treeview.xview,
            fg_color="white",
            height=20,  # <--- +++++side scrollbar visibility+++++ #
            corner_radius=scroll_corner,
            button_color=srh_grey,
            button_hover_color=srh_blue
        )

        self.set_treeview_columns()

        if callable(get_data_callback):
            self.__get_treeview_data_callback = get_data_callback
        else:
            def callback():
                """a callback that returns an empty data dictionary"""
                return {}
            self.__get_treeview_data_callback = callback

        if callable(on_cell_click_callback):
            self.__on_cell_click_callback = on_cell_click_callback
        else:
            def callback():
                """a callback that returns an empty data dictionary"""
                print(self.treeview.item(self.treeview.focus()))
            self.__on_cell_click_callback = callback

        #self.treeview.bind("<Double-1>", lambda _:self.__on_click_callback(self.treeview.item(self.treeview.focus())))
        self.treeview.bind("<Double-1>", lambda _:self.__on_cell_click_callback(dict[str,str](self.treeview.item(self.treeview.focus()))['values']))

        self.__center_frame.grid_rowconfigure(0, weight=1)
        self.__center_frame.grid_rowconfigure(1, weight=0)
        self.__center_frame.grid_columnconfigure(0, weight=1)
        self.__center_frame.grid_columnconfigure(1, weight=0)

        self.treeview.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.tree_scrollbar.grid(row=0, rowspan=2, column=1, sticky='NS')
        self.horizontal_tree_scrollbar.grid(row=1, column=0, sticky='WE')

        self.treeview.tkraise()
        self.apply_layout()
        self.update_treeview()


    def apply_layout(self):
        """
            arrange the default items depending on which ones are ment to be shown
        """
        logger.debug('apply layout')
        self.__header_frame.grid(
            row=0,
            columnspan=3,
            column=0,
            sticky='NSWE'
        )
        self.__left_bar_frame.grid(
            column=0,
            rowspan=1 + (1 if self.__overlay_left_sidebar else 0) + (1 if self.__searchbar_enabled else 0) + (1 if self.__overlay_left_sidebar and self.__searchbar_enabled else 0) + (1 if self.__overlay_left_sidebar and self.__navigation_bar_enabled else 0),
            row=(0 if self.__overlay_left_sidebar else 1) + (1 if self.__navigation_bar_enabled and not self.__overlay_left_sidebar else 0),
            sticky='NSWE'
        )

        self.__right_bar_frame.grid(
            column=2,
            rowspan=1 + (1 if self.__overlay_right_sidebar else 0) + (1 if self.__searchbar_enabled else 0) + (1 if self.__overlay_right_sidebar and self.__searchbar_enabled else 0) + (1 if self.__overlay_right_sidebar and self.__navigation_bar_enabled else 0),
            row=(0 if self.__overlay_right_sidebar else 1) + (1 if self.__navigation_bar_enabled and not self.__overlay_right_sidebar else 0),
            sticky='NSWE'
        )

        if self.__navigation_bar_enabled:
            self.__navigation_bar_frame.grid(
                row=1,
                column=1 if self.__overlay_left_sidebar else 0,
                columnspan=3 - (1 if self.__overlay_left_sidebar else 0) - (1 if self.__overlay_right_sidebar else 0),
                sticky='NSWE'
            )

        if self.__searchbar_enabled:
            self.__searchbar_frame.grid(
                row=2 if self.__navigation_bar_enabled else 1,
                column=1,
                padx=20,
                sticky='NSWE'
            )
            self.__dropdown_overlay_frame.grid(
                row=1 + (1 if self.__searchbar_enabled else 0) + (1 if self.__navigation_bar_enabled else 0),
                column=1,
                padx=(90, 180),
                pady = 0,
                sticky='NWE'
            )

        self.__center_frame.grid(
            row=1 + (1 if self.__searchbar_enabled else 0) + (1 if self.__navigation_bar_enabled else 0),
            column=1,
            padx=10,
            pady=(0,10),
            sticky='NSWE'
        )

        self.grid_columnconfigure(0, weight=0 if self.__hide_left_sidebar else 1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_columnconfigure(2, weight=0 if self.__hide_left_sidebar else 1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0 if self.__navigation_bar_enabled or self.__searchbar_enabled else 4)
        self.grid_rowconfigure(2, weight=4 if self.__navigation_bar_enabled ^ self.__searchbar_enabled else 0)
        self.grid_rowconfigure(3, weight=4 if self.__navigation_bar_enabled and self.__searchbar_enabled else 0)

        self.__center_frame.tkraise(self.__dropdown_overlay_frame)


    def __init__(
            self,
            parent:tkinter.Widget,
            controller:Any,
            window_name:str='',
            header_text:str='',
            admin_mode:bool=False
    ):
        """
            :param tkinter.Toplevel|tkinter.Frame parent:
            :param bool admin_mode:

        """
        super().__init__(parent, background='white',name=window_name)
        self.controller = controller
        self.parent = parent
        self.admin_mode = admin_mode
        self.admin_mode = True

        self.__tree_frame:tkinter.Frame = tkinter.Frame(self, background='blue' if admin_mode else srh_blue)
        self.__info_frame:tkinter.Frame = tkinter.Frame(self, background='green' if admin_mode else srh_blue)
        self.__action_buttons_frame:tkinter.Frame = tkinter.Frame(self, background='yellow' if admin_mode else srh_blue)
        self.__header_frame:tkinter.Frame = tkinter.Frame(self, background=srh_orange if admin_mode else srh_blue)


        self.navigation_buttons: list[customtkinter.CTkButton] = []

        self.search_button_image:tkinter.PhotoImage|None = None
        self.add_item_button_image:tkinter.PhotoImage|None = None

        self.add_item_button:tkinter.Button|None = None
        self.search_button:tkinter.Button|None = None
        self.__searchbar_enabled: bool = False
        self.__navigation_bar_enabled: bool = False
        self.__treeview_enabled: bool = False

        self.__overlay_left_sidebar:bool = self.setup_side_bar_left(self.__left_bar_frame)
        self.__overlay_right_sidebar:bool = self.setup_side_bar_right(self.__right_bar_frame)
        self.__hide_left_sidebar:bool = False
        self.__hide_right_sidebar:bool = False

        self.__get_treeview_data_callback:Callable[[],list[dict[str,str]]]|None = None
        self.__on_cell_click_callback: Callable[[dict[str,str|list[str]]],None] | None = None

        self.__treeview_structure:dict[str,int]|None = None

        self.after(0, self.setup_header_bar, self.__header_frame)
        self.after(0, self.setup_main_frame, self.__center_frame)

        self.apply_layout()

    def __sort_column(self, col, reverse:bool=False):
        """
        Sortiert die Einträge einer Spalte in einer `ttk.Treeview`-Tabelle.

        Diese Funktion sortiert die Inhalte der angegebenen Spalte entweder numerisch oder alphanumerisch,
        abhängig vom Datentyp der Spaltenwerte. Zusätzlich wird die Reihenfolge der Einträge im Treeview
        aktualisiert, und die Tags für "oddrow" (ungerade Zeilen) und "evenrow" (gerade Zeilen) werden
        entsprechend neu gesetzt. Der Header der Spalte wird so konfiguriert, dass ein Klick auf den Header
        die Sortierrichtung umkehrt.

        Args:
            col (str): Der Name der zu sortierenden Spalte.
            reverse (bool, optional): Gibt an, ob die Sortierung in umgekehrter Reihenfolge erfolgen soll.
                Standardmäßig False für aufsteigende Sortierung.

        Raises:
            ValueError: Falls beim Überprüfen von numerischen Werten ein unerwarteter Typ auftritt.

        Notes:
            - Die Funktion überprüft, ob alle Werte in der Spalte numerisch sind (sofern nicht leer)
              und wählt basierend darauf die geeignete Sortierlogik (numerisch oder alphanumerisch).
            - Nach der Sortierung werden die Tags für "oddrow" und "evenrow" neu gesetzt, um ein visuelles
              Unterscheiden der Zeilen zu ermöglichen.
            - Die Funktion modifiziert den Header der Spalte, sodass beim nächsten Klick die Sortierrichtung
              umgekehrt wird.
        """
        if self.treeview is None:
            return
        # Daten aus der Treeview abrufen
        data = [(self.treeview.set(item, col), item) for item in self.treeview.get_children('')]

        # Prüfen, ob die Spalte hauptsächlich numerische Daten enthält
        def is_numeric(value):
            """."""
            try:
                float(value)
                return True
            except ValueError:
                return False

        # Entscheiden, ob die Spalte als Zahl oder Text sortiert werden soll
        if all(is_numeric(row[0]) for row in data if row[0] != ''):
            key_func = lambda x: float(x[0])
        else:
            key_func = lambda x: str(x[0])

        # Daten sortieren
        data.sort(key=key_func, reverse=reverse)

        # Reihenfolge in der Treeview aktualisieren
        for index, (_, item) in enumerate(data):
            self.treeview.move(item, "", index)

        # Tags für odd/even-Reihen neu setzen
        for index, item in enumerate(self.treeview.get_children('')):
            tag = "oddrow" if index % 2 == 0 else "evenrow"
            self.treeview.item(item, tags=(tag,))

        # Header aktualisieren, um Sortierrichtung zu wechseln
        self.treeview.heading(col, command=lambda c=col: self.__sort_column(c, not reverse))

    @abstractmethod
    def setup_main_frame(self, frame:tkinter.Frame) -> None:
        """
            All Subclasses o fIWindow must override this method.
            Code that adds content to the main frame should be called in this method.
        """

    @abstractmethod
    def setup_header_bar(self, frame:tkinter.Frame) -> None:
        """
            All Subclasses o fIWindow must override this method.
            Code that adds content to the header frame should be called in this method.
        """

    @abstractmethod
    def setup_side_bar_left(self, frame:tkinter.Frame) -> bool:
        """
            All Subclasses o fIWindow must override this method.
            Code that adds content to the frame of the left sidebar should be called in this method.
            If the method returns True, the left sidebar will go from the bottom up to the top of the window, by
            narrowing the header frame.
            If the method returns False, the left sidebar will start from the bottom of the window and end at the bottom of the
            header frame. The header frame will extend to the left of the window.
        """

    @abstractmethod
    def setup_side_bar_right(self, frame:tkinter.Frame) -> bool:
        """
            All Subclasses o fIWindow must override this method.
            Code that adds content to the frame of the right sidebar should be called in this method.
            If the method returns True, the right sidebar will go from the bottom up to the top of the window, by
            narrowing the header frame.
            If the method returns False, the right sidebar will start from the bottom of the window and end at the bottom of the
            header frame. The header frame will extend to the right of the window.
        """

    def update_treeview(self, data:list[dict[str,str]]= None, filter_string:str = None) -> None:
        """
            .
        """
        if not self.__treeview_enabled:
            logger.error('no treeview enabled')
            return
        else:
            logger.debug('update treeview')
            self.treeview.delete(*self.treeview.get_children())

            i:int=0
            for row in data if data else self.__get_treeview_data_callback():
                if filter_string is not None and not any(filter_string not in value for value in row):
                    continue
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                l:list[str] = []
                for enumerated in enumerate(row.keys()):
                    l.append(row[enumerated[1]])
                self.treeview.insert(
                    "",
                    "end",
                    tags=(tag,),
                    values=tuple(l)
                )
                i += 1
            logger.debug('finished update treeview')

    def set_treeview_columns(self):
        """
            .
        """
        if self.treeview['columns']:
            self.treeview['columns'] = tuple([f"c{i}" for i in range(0,len(self.__treeview_structure))])
        i:int=1
        print(self.__treeview_structure)
        for column_name in enumerate(self.__treeview_structure.keys()):
            self.treeview.column(f'# {i}', anchor=tkinter.CENTER, width=self.__treeview_structure[column_name[1]])
            self.treeview.heading(f'# {i}', text=column_name[1], command=lambda c=f'# {i}': self.__sort_column(c, True))
            i+=1

    def enable_treeview(
            self,
            get_data_callback:Callable[[],list[dict[str,str]]],
            on_cell_click_callback:Callable[[dict[str,str]],None],
            tree_structure:dict[str,int]
    ):
        """
            .
        """
        self.__treeview_enabled = True
        self.__treeview_structure = tree_structure

        self.treeview:ttk.Treeview = ttk.Treeview(
            self.__center_frame,
            columns=tuple([f"c{i}" for i in range(0,len(tree_structure if tree_structure else self.__treeview_structure))]),
            show="headings"
        )

        self.tree_scrollbar = customtkinter.CTkScrollbar(
            self.__center_frame,
            orientation="vertical",
            command=self.treeview.yview,
            fg_color="white",
            width=20,  # <--- +++++side scrollbar visibility+++++ #
            corner_radius=scroll_corner,
            button_color=srh_grey,
            button_hover_color=srh_blue
        )
        self.horizontal_tree_scrollbar = customtkinter.CTkScrollbar(
            self.__center_frame,
            orientation="horizontal",
            command=self.treeview.xview,
            fg_color="white",
            height=20,  # <--- +++++side scrollbar visibility+++++ #
            corner_radius=scroll_corner,
            button_color=srh_grey,
            button_hover_color=srh_blue
        )

        self.set_treeview_columns()

        if callable(get_data_callback):
            self.__get_treeview_data_callback = get_data_callback
        else:
            def callback():
                """a callback that returns an empty data dictionary"""
                return {}
            self.__get_treeview_data_callback = callback

        if callable(on_cell_click_callback):
            self.__on_cell_click_callback = on_cell_click_callback
        else:
            def callback():
                """a callback that returns an empty data dictionary"""
                print(self.treeview.item(self.treeview.focus()))
            self.__on_cell_click_callback = callback

        #self.treeview.bind("<Double-1>", lambda _:self.__on_click_callback(self.treeview.item(self.treeview.focus())))
        self.treeview.bind("<Double-1>", lambda _:self.__on_cell_click_callback(dict[str,str](self.treeview.item(self.treeview.focus()))['values']))

        self.__center_frame.grid_rowconfigure(0, weight=1)
        self.__center_frame.grid_rowconfigure(1, weight=0)
        self.__center_frame.grid_columnconfigure(0, weight=1)
        self.__center_frame.grid_columnconfigure(1, weight=0)

        self.treeview.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.tree_scrollbar.grid(row=0, rowspan=2, column=1, sticky='NS')
        self.horizontal_tree_scrollbar.grid(row=1, column=0, sticky='WE')

        self.treeview.tkraise()
        self.apply_layout()
        self.update_treeview()

    def enable_navigation_bar(self, buttons:list[tuple[str, Callable]]):
        """
            .
        """
        if self.__navigation_bar_enabled:
            raise RuntimeError('enable_navigation_bar was called twice')
        self.__navigation_bar_enabled = True
        for button_text, button_callback in buttons:
            self.navigation_buttons.append(
                customtkinter.CTkButton(
                    self.__navigation_bar_frame,
                    text=button_text,
                    border_width=border,
                    command=button_callback,
                    cursor="hand2",
                    corner_radius=corner,
                    fg_color='#a9a9a9',
                    text_color="black",
                    font=("Arial", 20),
                    hover_color=nav_bar_hover_color
                )
            )
            self.__navigation_bar_frame.grid_columnconfigure(len(self.navigation_buttons) - 1, weight=1)
            self.navigation_buttons[-1].grid(row=0, padx=40, pady=15, column=len(self.navigation_buttons) - 1,sticky='WE')
        self.apply_layout()

    def select_on_search(self, search_term:str):
        """
            .
        """
        search_entries = []
        for entry in self.__get_treeview_data_callback():
            for value in entry:
                if search_term in str(entry[value]).lower():
                    if entry not in search_entries:
                        search_entries.append(entry)
        self.update_treeview(data=search_entries)

    def enable_searchbar(self, add_item_callback:Callable) -> None:
        """
            creates a frame on top of the center frame.
            it contains a search button, the actual searchbar and a button for adding items.


        """
        if self.__searchbar_enabled:
            raise RuntimeError('enable_navigation_bar was called twice')
        self.__searchbar_enabled = True

        self.search_button_image = tkinter.PhotoImage(file=Paths.assets_path('SearchButton.png'))

        self.search_button = tkinter.Button(
            self.__searchbar_frame,
            image=self.search_button_image,
            bd=0, relief=tkinter.FLAT,
            bg="white",cursor="hand2",
            activebackground="white",
            command=lambda:self.search_entry.finish_search(cache.user_name)
        )

        self.add_item_button_image = tkinter.PhotoImage(file=Paths.assets_path("Erstellen.png"))

        self.add_item_button = tkinter.Button(
            self.__searchbar_frame,
            image=self.add_item_button_image,
            bd=0, relief=tkinter.FLAT,
            bg="white",cursor="hand2",
            activebackground="white",
            command=add_item_callback
        )

        #erstelle den hinufügen-button im auf dem search frame
        self.dropdown: CTkListbox = CTkListbox(
            self.__dropdown_overlay_frame,
            font=("Arial", 20),
            text_color='black',
            bg_color="white",
            border_color=srh_grey,
            corner_radius=10,
            scrollbar_fg_color="white",
            scrollbar_button_color='white',
            scrollbar_button_hover_color='white'
        )

        self.search_entry_oval:CTkEntry = CTkEntry(
            self.__searchbar_frame,
            text_color="black",
            fg_color=srh_grey,
            bg_color="white",
            font=("Arial", 26),
            corner_radius=20,
            border_width=0,
            height=25
        )

        self.search_entry:Searchbar = Searchbar(
            self,
            self.__searchbar_frame,
            self.dropdown,
            cache.user_name
        )

        self.__searchbar_frame.grid_columnconfigure(0, weight=0)
        self.__searchbar_frame.grid_columnconfigure(1, weight=1)
        self.__searchbar_frame.grid_columnconfigure(2, weight=0)

        # setze die grid Layouts der buttons und der Suchleiste im search-frame
        self.search_button.grid(padx=5, pady=5, row=0, column=0)
        self.add_item_button.grid(padx=5, pady=5, row=0, column=2)
        self.search_entry.grid(column=1, row=0, columnspan=1, sticky='WE', padx=26, pady=20)
        self.search_entry_oval.grid(column=1, row=0, columnspan=1, sticky='WE', padx=5, pady=5)
        self.dropdown.grid(padx=0, pady=5, row=0, column=0)

        self.search_entry_oval.bind('<FocusIn>', lambda  _: self.search_entry.focus())
        self.search_entry.add_on_focus_in_event(lambda  _: self.__dropdown_overlay_frame.tkraise(self.__center_frame))
        self.search_entry.add_on_focus_out_event(lambda _: self.__center_frame.tkraise(self.__dropdown_overlay_frame))
        self.search_entry.add_on_finish_search_event(lambda _: self.update_treeview(filter_string=self.search_entry.get(0.0,'end-1c')))
        self.dropdown.bind("<<ListboxSelect>>", lambda var: SearchbarLogic.on_dropdown_select(self.search_entry, self.dropdown, cache.user_name))
        self.dropdown.bind("<<ListboxSelect>>", lambda var: self.__center_frame.tkraise(self.__dropdown_overlay_frame))

        self.search_entry.insert('end', 'Suche', tags='normal')
        self.__center_frame.tkraise(self.__dropdown_overlay_frame)
        self.apply_layout()

    def toggle_left_sidebar(self):
        """."""
        self.__hide_left_sidebar = not self.__hide_left_sidebar
        self.apply_layout()

    def toggle_right_sidebar(self):
        """."""
        self.__hide_right_sidebar = not self.__hide_right_sidebar
        self.apply_layout()

    def apply_layout(self):
        """
            arrange the default items depending on which ones are ment to be shown
        """
        logger.debug('apply layout')
        self.__header_frame.grid(
            row=0,
            columnspan=3,
            column=0,
            sticky='NSWE'
        )
        self.__left_bar_frame.grid(
            column=0,
            rowspan=1 + (1 if self.__overlay_left_sidebar else 0) + (1 if self.__searchbar_enabled else 0) + (1 if self.__overlay_left_sidebar and self.__searchbar_enabled else 0) + (1 if self.__overlay_left_sidebar and self.__navigation_bar_enabled else 0),
            row=(0 if self.__overlay_left_sidebar else 1) + (1 if self.__navigation_bar_enabled and not self.__overlay_left_sidebar else 0),
            sticky='NSWE'
        )

        self.__right_bar_frame.grid(
            column=2,
            rowspan=1 + (1 if self.__overlay_right_sidebar else 0) + (1 if self.__searchbar_enabled else 0) + (1 if self.__overlay_right_sidebar and self.__searchbar_enabled else 0) + (1 if self.__overlay_right_sidebar and self.__navigation_bar_enabled else 0),
            row=(0 if self.__overlay_right_sidebar else 1) + (1 if self.__navigation_bar_enabled and not self.__overlay_right_sidebar else 0),
            sticky='NSWE'
        )

        if self.__navigation_bar_enabled:
            self.__navigation_bar_frame.grid(
                row=1,
                column=1 if self.__overlay_left_sidebar else 0,
                columnspan=3 - (1 if self.__overlay_left_sidebar else 0) - (1 if self.__overlay_right_sidebar else 0),
                sticky='NSWE'
            )

        if self.__searchbar_enabled:
            self.__searchbar_frame.grid(
                row=2 if self.__navigation_bar_enabled else 1,
                column=1,
                padx=20,
                sticky='NSWE'
            )
            self.__dropdown_overlay_frame.grid(
                row=1 + (1 if self.__searchbar_enabled else 0) + (1 if self.__navigation_bar_enabled else 0),
                column=1,
                padx=(90, 180),
                pady = 0,
                sticky='NWE'
            )

        self.__center_frame.grid(
            row=1 + (1 if self.__searchbar_enabled else 0) + (1 if self.__navigation_bar_enabled else 0),
            column=1,
            padx=10,
            pady=(0,10),
            sticky='NSWE'
        )

        self.grid_columnconfigure(0, weight=0 if self.__hide_left_sidebar else 1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_columnconfigure(2, weight=0 if self.__hide_left_sidebar else 1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0 if self.__navigation_bar_enabled or self.__searchbar_enabled else 4)
        self.grid_rowconfigure(2, weight=4 if self.__navigation_bar_enabled ^ self.__searchbar_enabled else 0)
        self.grid_rowconfigure(3, weight=4 if self.__navigation_bar_enabled and self.__searchbar_enabled else 0)

        self.__center_frame.tkraise(self.__dropdown_overlay_frame)

    def on_load(self):
        """
            Subclasses o fIWindow can optionally override this method.
            It is called everytime a page is shown again by the current DdInv instance
        """
        if self.__treeview_enabled:
            self.set_treeview_columns()
            self.update_treeview()
        self.apply_layout()