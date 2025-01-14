import tkinter as tk
from tkinter import ttk
from tkinter import *
from includes.sec_data_info import sqlite3api as db
import cache
from ._styles import *
import customtkinter as ctk
from ..CTkScrollableDropdown import *


def show_details(selectedItem, tree, controller):
    """
    Zeigt die Details eines ausgewählten Elements in einer Benutzeroberfläche an. Diese Funktion ruft die Daten
    des ausgewählten Elements aus einer Baumstruktur ab, speichert die ID des Elements im Cache und zeigt die
    Details-Seite mit den aktualisierten Informationen an.

    :param selectedItem: Das aktuell ausgewählte Baum-Element.
    :param tree: Die Baumstruktur, welche die zugehörigen Daten enthält.
    :param controller: Der Controller, der für die Navigation und Verwaltung der Frames zuständig ist.
    :return: Gibt keinen Wert zurück.
    """
    # Daten aus der ausgewählten Zeile
    data = tree.item(selectedItem, "values")
    print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: Data of the selected item: {data}")  # Debug
    cache.selected_ID = data[0]

    controller.show_frame(detailsWindow)  # Zeige die Details-Seite

    # Frame aktualisieren und anzeigen
    details = controller.frames[detailsWindow]
    details.update_data(data)  # Methode in detailsWindow aufrufen



class detailsWindow(tk.Frame):
    """
    Repräsentiert ein Detailfenster innerhalb einer Tkinter-Applikation.

    Das Detailfenster bietet Funktionen zur Anzeige von Details eines Objekts, Eingabefeldern
    für verschiedene Eigenschaften und eine Baumansicht für datengestützte Tabellendarstellungen.
    Es ermöglicht die Navigation zu anderen Ansichten und konfiguriert eine intuitive Benutzerschnittstelle.

    :ivar controller: Der Controller der Anwendung, der für die Navigation zwischen Fenstern verwendet wird.
    :ivar go_back_btn_details_window: Bildressource für den Zurück-Button.
    :ivar opt_btn_details_window: Bildressource für den Optionen-Button.
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
            """
            Repräsentiert ein Fenster mit detaillierter Ansicht innerhalb der GUI-Anwendung. Die Klasse erbt von
            `tk.Frame` und stellt eine Benutzeroberfläche zur Verfügung, die in der Lage ist, verschiedene
            Unterseiten oder Frames zu laden und anzuzeigen. Dieses spezielle Fenster dient beispielsweise zur
            Anzeige von Details und ermöglicht die Navigation zurück zur Hauptseite der Anwendung.

            :Attributes:
              parent:
                Ein Widget, das das Eltern-Element dieses Frames darstellt. Das Eltern-Element bestimmt die
                hierarchische Struktur und Position des Frames innerhalb des GUI-Layouts.
              controller:
                Ein Controller-Objekt, das die Verwaltung der Frame-Navigation und des Anwendungszustands
                übernimmt. Hiermit können neue Seiten angezeigt werden.
            """
            from .mainPage import mainPage
            controller.show_frame(mainPage)

        def show_settings_window_details_window():
            """
            Eine Klasse, die ein Detailfenster innerhalb einer Tkinter-Anwendung repräsentiert. Diese
            Klasse erbt von ``tk.Frame`` und bietet Methoden, um bestimmte Ereignisse oder
            Aktionen auszuführen, wie das Öffnen eines Einstellungsfensters innerhalb des
            Detailfensters.

            Attributes
            ----------
            parent : Any
                Das übergeordnete Widget oder Objekt, zu dem dieses Frame gehört.
            controller : Any
                Der Controller, der zur Verwaltung dieses Fensters verwendet wird.

            Methods
            -------
            show_settings_window_details_window()
                Öffnet das Einstellungs-Pop-Up-Fenster im Detailfenster.
            """
            print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: Show settings window details window")
            from .settingsWindow import pop_up_settings
            pop_up_settings(self, controller)

        from ._avatarManager import resource_path
        self.go_back_btn_details_window = tk.PhotoImage(file=resource_path("./includes/assets/ArrowLeft.png"))

        # Erstelle einen Header-Bereich
        header_frame_details_window = tk.Frame(self, height=10, background="#DF4807")
        header_frame_details_window.grid(row=0, column=0,columnspan=2, sticky=tk.W + tk.E + tk.N)

        # Überschrift mittig zentrieren
        header_frame_details_window.grid_columnconfigure(0, weight=1)  # Platz links
        header_frame_details_window.grid_columnconfigure(1, weight=3)  # Überschrift zentriert (größerer Gewichtungsfaktor)
        header_frame_details_window.grid_columnconfigure(2, weight=1)  # Option-Button


        # Zentriere das Label in Spalte 1
        header_label_details_window = tk.Label(
            header_frame_details_window,
            text="Details",
            background="#DF4807",
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

        size_details_window = 28

        # Ändere die Position des TreeFrames
        tree_frame_details_window = tk.Frame(container_frame, background="red", width=200, height=400)
        tree_frame_details_window.grid(row=0, column=0, padx=40, sticky="")

        global tree_details_window
        tree_details_window = ttk.Treeview(tree_frame_details_window, column=("c1", "c2"), show="headings", height=30)

        scroll_details_window = tk.Scrollbar(
            tree_frame_details_window,
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

        ### listbox for directories
        tree_details_window.column("# 1", anchor=CENTER, width=180)
        tree_details_window.heading("# 1", text="Nutzername", )
        tree_details_window.column("# 2", anchor=CENTER, width=180)
        tree_details_window.heading("# 2", text="Ausgeliehen am")
        tree_details_window.grid(row=1, column=0)
        tree_details_window.tkraise()

        # Input-Frame
        input_frame_details_window = tk.Frame(container_frame, background="white")
        input_frame_details_window.grid(row=0, column=1, pady=20, sticky="nsew")

        input_frame_details_window.grid_columnconfigure(0, weight=1)  # Zentriere das Input-Frame
        input_frame_details_window.grid_columnconfigure(1, weight=1)
        input_frame_details_window.grid_columnconfigure(2, weight=1)

        # Service Tag
        service_tag_label_details_window = tk.Label(input_frame_details_window, text="Service Tag",
                                                    font=("Arial", size_details_window), background="white")
        service_tag_label_details_window.grid(column=0, row=0, sticky=tk.W + tk.E, padx=20, pady=10)

        self.service_tag_entry_details_window = ctk.CTkEntry(input_frame_details_window,
                                                             font=("Arial", size_details_window),
                                                             corner_radius=corner,fg_color=srhGrey,text_color="black",border_width=border)
        self.service_tag_entry_details_window.grid(column=1, row=0, sticky=tk.W + tk.E, padx=20, pady=10)

        # Typ
        type_label_details_window = tk.Label(input_frame_details_window, text="Typ",
                                             font=("Arial", size_details_window), background="white")
        type_label_details_window.grid(column=0, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        self.type_entry_details_window = ctk.CTkEntry(input_frame_details_window, font=("Arial", size_details_window),
                                                             corner_radius=corner,fg_color=srhGrey,text_color="black",border_width=border)
        self.type_entry_details_window.grid(column=1, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        # Raum (Dropdown-Menü)
        room_label_details_window = tk.Label(input_frame_details_window, text="Raum", background="white",
                                             font=("Arial", size_details_window))
        room_label_details_window.grid(row=2, column=0, padx=0, pady=20, sticky=tk.W + tk.E)

        # CTkComboBox statt ttk.Combobox
        room_values = []
        for room in db.fetch_all_rooms():
            room_values.append(room['Raum'])

        self.room_combobox_details_window = ctk.CTkComboBox(input_frame_details_window,
                                                            font=("Arial", size_details_window),
                                                             corner_radius=corner,button_color=srhGrey ,fg_color=srhGrey,
                                                            text_color="black",border_width=border,
                                                            state="readonly")

        self.room_combobox_details_window.grid(row=2, column=1, padx=20, pady=20, sticky=tk.W + tk.E)
        CTkScrollableDropdown(self.room_combobox_details_window, values=room_values,button_color=srhGrey,
                              frame_corner_radius=corner, autocomplete=True, fg_color=srhGrey,
                              text_color="black", frame_border_width=comboborder, frame_border_color=srhGreyHover,
                              alpha=1, justify="left",hover_color=srhGreyHover)

        self.room_combobox_details_window.set("Raum auswählen")  # Platzhalter

        # Name
        name_label_details_window = tk.Label(input_frame_details_window, text="Name",
                                             font=("Arial", size_details_window), background="white")
        name_label_details_window.grid(column=0, row=3, sticky=tk.W + tk.E, padx=20, pady=10)

        self.name_entry_details_window = ctk.CTkEntry(input_frame_details_window, font=("Arial", size_details_window),
                                                             corner_radius=corner,fg_color=srhGrey,text_color="black",border_width=border)
        self.name_entry_details_window.grid(column=1, row=3, sticky=tk.W + tk.E, padx=20, pady=10)

        # Beschädigung
        damaged_label_details_window = tk.Label(input_frame_details_window, text="Beschädigung",
                                                font=("Arial", size_details_window), background="white")
        damaged_label_details_window.grid(column=0, row=4, sticky=tk.W + tk.E, padx=20, pady=10)

        self.damaged_entry_details_window = ctk.CTkEntry(input_frame_details_window,
                                                         font=("Arial", size_details_window),
                                                             corner_radius=corner,fg_color=srhGrey,text_color="black",border_width=border)
        self.damaged_entry_details_window.grid(column=1, row=4, sticky=tk.W + tk.E, padx=20, pady=10)

        # Funktion zum Eintrag hinzufügen
        def refresh_entry():
            """
            Eine Klasse, die ein Fenster für Details erstellt und die Möglichkeit bietet, bestimmte
            Einträge zu aktualisieren. Diese Klasse ist von `tk.Frame` abgeleitet und dient als UI-Komponente
            innerhalb einer größeren Anwendung.

            :Attributes:
                type_entry_details_window (tk.Entry): Eingabefeld zur Erfassung des Gerätetyps.
                room_entry_details_window (tk.Entry): Eingabefeld für den Speicherort des Geräts.
                name_entry_details_window (tk.Entry): Eingabefeld für den Modellnamen des Geräts.
                damaged_entry_details_window (tk.Entry): Eingabefeld zur Erfassung des Gerätezustands.
                parent (tk.Widget): Eltern-Widget, zu dem diese Instanz gehört.
                controller: Steuerungsinstanz, die u.a. Navigation zwischen Fenstern ermöglicht.
            """
            #update
            type = self.type_entry_details_window.get() if self.type_entry_details_window.get() != "" else "None"
            room = self.room_combobox_details_window.get() if self.room_combobox_details_window.get() != "" else "None"
            name = self.name_entry_details_window.get() if self.name_entry_details_window.get() != "" else "None"
            if not self.damaged_entry_details_window.get() or self.damaged_entry_details_window.get() == "":
                damage = "None"
            else:
                damage = self.damaged_entry_details_window.get()
            print(damage)
            print(db.update_hardware_by_ID(cache.selected_ID, neue_beschaedigung=damage, neue_Standort=room, neue_Modell=name, neue_Geraetetyp=type))
            from .mainPage import mainPage
            mainPage.update_sidetree_with_data()
            controller.show_frame(mainPage)

        def lend(data):
            """
            Eine Klasse, die die Details-Ansicht als Tkinter-Frame darstellt.

            Diese Klasse ist für die Darstellung und Verwaltung einer spezifischen
            Detailansicht innerhalb einer GUI-Anwendung verantwortlich. Sie erbt von
            Tkinter's ``Frame`` und integriert zusätzliche Methoden zur Behandlung
            spezifischer UI-Aktionen.

            :param parent: Der übergeordnete Tkinter-Container, in den dieser Frame
                           eingebunden wird.
            :type parent: tk.Widget
            :param controller: Ein Controller-Objekt, das die Steuerlogik enthält und
                               den Zustand der Anwendung verwaltet.
            :type controller: beliebiger Typ
            """
            print("Übergebene Daten:", data)
            from .lendPopup import lend_popup
            lend_popup(self, data, controller)

        def return_item(data):
            """
            Eine Klasse, die die Details-Ansicht als Tkinter-Frame darstellt.

            Diese Klasse ist für die Darstellung und Verwaltung einer spezifischen
            Detailansicht innerhalb einer GUI-Anwendung verantwortlich. Sie erbt von
            Tkinter's ``Frame`` und integriert zusätzliche Methoden zur Behandlung
            spezifischer UI-Aktionen.

            :param parent: Der übergeordnete Tkinter-Container, in den dieser Frame
                           eingebunden wird.
            :type parent: tk.Widget
            :param controller: Ein Controller-Objekt, das die Steuerlogik enthält und
                               den Zustand der Anwendung verwaltet.
            :type controller: beliebiger Typ
            """
            db.update_hardware_by_ID(cache.selected_ID, neue_Ausgeliehen_von=" ")
            from .mainPage import mainPage
            mainPage.update_treeview_with_data()
            controller.show_frame(mainPage)

        def delete_entry():
            """
            Eine Klasse, die ein Detailfenster als Unterklasse von `tk.Frame` darstellt. Es
            bietet die Möglichkeit, bestimmte Hardware-Datensätze aus einer Datenbank zu
            löschen und die Anzeige in der Hauptseite zu aktualisieren.

            Attribute
            ---------
            parent
                Der übergeordnete Tkinter-Container für die Frame-Erstellung.
            controller
                Eine Instanz, die für die Navigation zwischen den Frames verantwortlich ist.

            Methoden
            -------
            delete_entry
                Löscht den aktuell ausgewählten Hardware-Eintrag aus der Datenbank und
                aktualisiert die Anzeige in der Hauptseite.

            """
            db.delete_hardware_by_id(cache.selected_ID)
            from .mainPage import mainPage
            mainPage.update_treeview_with_data()
            mainPage.update_sidetree_with_data()
            controller.show_frame(mainPage)

        from ._avatarManager import resource_path
        self.edit_btn = tk.PhotoImage(file=resource_path("./includes/assets/Aktualisieren.png"))
        self.lend_btn = tk.PhotoImage(file=resource_path("./includes/assets/Ausleihen.png"))
        self.delete_btn = tk.PhotoImage(file=resource_path("./includes/assets/Loeschen.png"))
        self.return_btn = tk.PhotoImage(file=resource_path("./includes/assets/Zurueckgeben.png"))

        # Buttons in ein separates Frame
        global button_frame_add_item_popup, lend_button, ret_button, delete_button, edit_button
        button_frame_add_item_popup = tk.Frame(self, background="white")
        button_frame_add_item_popup.grid(row=2, column=0, pady=20)

        lend_button = tk.Button(button_frame_add_item_popup, image=self.lend_btn,
                                bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                                command=lambda: lend({"name": self.name_entry_details_window.get()}))

        ret_button = tk.Button(button_frame_add_item_popup, image=self.return_btn,
                                bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                                command=lambda: return_item({"name": self.name_entry_details_window.get()}))


        def customMessageBoxCall():
            from customMessageBoxDelete import customMessageBoxDelete
            customMessageBoxDelete(parent,
                                           title="Aktion Bestätigen",
                                           message="Willst du diesen Eintrag unwiederruflich löschen?",
                                           delete_callback=delete_entry)


        delete_button = tk.Button(button_frame_add_item_popup, image=self.delete_btn,
                                 bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                                 command=customMessageBoxCall)
        #delete_button.pack(side=tk.LEFT, padx=20)  # Neben Exit-Button platzieren


        edit_button = tk.Button(button_frame_add_item_popup, image=self.edit_btn,
                               bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                               command=refresh_entry)
        #edit_button.pack(side=tk.LEFT, padx=20)  # Links platzieren

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
        :return: Es wird kein Wert zurückgegeben.
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

        if db.fetch_hardware_by_id(cache.selected_ID)['Ausgeliehen_von'] == "" or db.fetch_hardware_by_id(cache.selected_ID)['Ausgeliehen_von'] == " ":
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
