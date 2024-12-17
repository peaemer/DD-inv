import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
from includes.sec_data_info import sqlite3api as sqlapi
from includes.sec_data_info import UserSecurity as sec
import cache
import random, string
import customtkinter as ctk


LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"


def show_roles_details(selected_roles, tree, controller):
    """
    Zeigt die Details des ausgewählten Raums an. Die Methode liest die Daten aus
    der ausgewählten Zeile eines Treeviews, speichert die ID des Raums in einem
    Cache und aktualisiert die Daten des Detailframes. Anschließend wird der Frame
    zum Anzeigen der Details angezeigt.

    :param selected_room: Das ausgewählte Raumelement im Treeview.
    :param tree: Der Treeview, aus dem die Daten abgerufen werden.
    :param controller: Der Controller, der das Frame-Management übernimmt.
    :return: Es wird kein Wert zurückgegeben.
    """
    # Daten aus der ausgewählten Zeile
    data = tree.item(selected_roles, "values")
    print(f"DEBUG: Data of the selected item: {data}") # Debug
    cache.selected_ID = data[0]
    controller.show_frame(rolesDetailsWindow)  # Zeige die Details-Seite
    # Frame aktualisieren und anzeigen
    details = controller.frames[rolesDetailsWindow]
    details.update_data(data)  # Methode in detailsWindow aufrufen



class rolesDetailsWindow(tk.Frame):
    """
    Die Klasse roomDetailsWindow dient zur Darstellung und Bearbeitung von Raumdetails in einer GUI.

    Die Klasse ist eine Unterklasse von ``tk.Frame`` und wird zur Anzeige und Bearbeitung von Raumdaten
    in einer GUI verwendet. Sie bietet Interaktionen zum Zurückkehren zu einer Admin-Seite, zum Anzeigen
    eines Einstellungs-Popups sowie zum Aktualisieren oder Löschen von Raumeinträgen.

    :ivar controller: Der Controller, der für die Steuerung der GUI-Seiten zuständig ist.
    :type controller: tk.Tk
    :ivar go_back_btn_roles_window: Bild für den „Zurück“-Button.
    :type go_back_btn_roles_window: tk.PhotoImage
    :ivar opt_btn_roles_window: Bild für den „Optionen“-Button.
    :type opt_btn_roles_window: tk.PhotoImage
    :ivar room_num_entry: Eingabefeld für die Raumnummer.
    :type room_num_entry: tk.Entry
    :ivar place_entry: Eingabefeld für den Ort.
    :type place_entry: tk.Entry
    :ivar edit_btn: Bild für den „Aktualisieren“-Button.
    :type edit_btn: tk.PhotoImage
    :ivar lend_btn: Bild für den „Ausleihen“-Button.
    :type lend_btn: tk.PhotoImage
    :ivar delete_btn: Bild für den „Löschen“-Button.
    :type delete_btn: tk.PhotoImage
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="white")

        def go_back_roles_window():
            """
            Eine Klasse, die ein Fenster darstellt, um Details von Räumen anzuzeigen. Erbt von
            `tk.Frame` und dient als GUI-Komponente, die in einer tkinter-Anwendung eingebettet
            werden kann. Es enthält Funktionalitäten, um zur vorherigen Fensteransicht zurückzukehren.

            :Attributes:
                Keine Attribute, die in der Klassenbeschreibung vorhanden sind.

            :param parent: Das übergeordnete tk-Widget, in das dieser Frame eingebettet wird.
            :type parent: tk.Widget
            :param controller: Ein Objekt, das die Navigation und Verwaltung zwischen verschiedenen
                tkinter-Frames steuert.
            :type controller: object
            """
            from .adminRoleWindow import adminRoleWindow
            controller.show_frame(adminRoleWindow)

        def show_settings_window_roles_window():
            """
            Eine Klasse, die ein Fenster für Rauminformationen darstellt, das als Unterklasse
            von tk.Frame implementiert wurde. Diese Klasse dient als grafisches Fenster,
            das verschiedene Funktionen und Merkmale eines Rauminformationsfensters bereitstellt.

            Attributes
            ----------
            parent : Tkinter Widget
                Das übergeordnete Widget, auf das die aktuelle Instanz aufgesetzt wird.
            controller : Objekt
                Ein Steuerelement für die Verwaltung der Fenster- oder Anwendungslogik.

            """
            print("DEBUG: Show settings window details window")
            from .settingsWindow import pop_up_settings
            pop_up_settings(self, controller)

        from ._avatarManager import resource_path
        self.go_back_btn_roles_window = tk.PhotoImage(file=resource_path("./includes/assets/ArrowLeft.png"))

        # Erstelle einen Header-Bereich
        header_frame_roles_window = tk.Frame(self, height=10, background="#00699a")
        header_frame_roles_window.grid(row=0, column=0,columnspan=2, sticky=tk.W + tk.E + tk.N)

        # Überschrift mittig zentrieren
        header_frame_roles_window.grid_columnconfigure(0, weight=1)  # Platz links
        header_frame_roles_window.grid_columnconfigure(1, weight=3)  # Überschrift zentriert (größerer Gewichtungsfaktor)
        header_frame_roles_window.grid_columnconfigure(2, weight=1)  # Option-Button


        # Zentriere das Label in Spalte 1
        header_label_roles_window = tk.Label(
            header_frame_roles_window,
            text="Rollen Details",
            background="#00699a",
            foreground="white",
            font=("Arial", 60)
        )
        header_label_roles_window.grid(row=0, column=1, pady=40, sticky=tk.W + tk.E)

        # Buttons in Spalten 2 und 3 platzieren
        go_back_button_roles_window = tk.Button(
            header_frame_roles_window,
            image=self.go_back_btn_roles_window,
            command=go_back_roles_window,
            bd=0,
            relief=tk.FLAT,
            bg="#00699a",
            activebackground="#00699a"
        )
        go_back_button_roles_window.grid(row=0, column=0, sticky=tk.W, padx=20)

        from ._avatarManager import loadImage
        self.roles_details_window_avatar = loadImage(parent=parent)

        options_button_roles_window = tk.Button(
            header_frame_roles_window,
            image=self.roles_details_window_avatar,
            command=show_settings_window_roles_window,
            bd=0,
            relief=tk.FLAT,
            bg="#00699a",
            activebackground="#00699a"
        )
        options_button_roles_window.grid(row=0, column=2, sticky=tk.E, padx=20)


        # Container für Input- und Tree-Frame
        container_frame = tk.Frame(self, background="white")
        container_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Konfiguration der Container-Spalten
        container_frame.grid_columnconfigure(0, weight=1)

        size_roles_window = 20

        # Input-Frame
        input_frame_roles_window = tk.Frame(container_frame, background="white")
        input_frame_roles_window.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

        input_frame_roles_window.grid_columnconfigure(0, weight=1)  # Zentriere das Input-Frame
        input_frame_roles_window.grid_columnconfigure(1, weight=0)
        input_frame_roles_window.grid_columnconfigure(2, weight=0)
        input_frame_roles_window.grid_columnconfigure(3, weight=1)

        # Admin
        self.role_name = tk.Label(input_frame_roles_window, text="",
                         font=("Arial", 24), background="white")
        self.role_name.grid(column=1, columnspan=2, row=0, sticky=tk.W + tk.E, padx=0, pady=5)

        # Ansehen
        view_label_roles_window = tk.Label(input_frame_roles_window, text="Ansehen",
                                           font=("Arial", size_roles_window), background="white")
        view_label_roles_window.grid(column=1, row=1, sticky=tk.W + tk.E, padx=100, pady=5)

        self.view = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.view.grid(column=2, row=1, sticky=tk.W + tk.E, padx=100, pady=5)

        # Rolle Loeschbar
        delete_rl_label_roles_window = tk.Label(input_frame_roles_window, text="Rolle Löschbar",
                                                font=("Arial", size_roles_window), background="white")
        delete_rl_label_roles_window.grid(column=1, row=2, sticky=tk.W + tk.E, padx=100, pady=5)

        self.delete_rl = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.delete_rl.grid(column=2, row=2, sticky=tk.W + tk.E, padx=100, pady=5)

        # Admin Feature
        feature_label_roles_window = tk.Label(input_frame_roles_window, text="Admin Feature",
                                              font=("Arial", size_roles_window), background="white")
        feature_label_roles_window.grid(column=1, row=3, sticky=tk.W + tk.E, padx=100, pady=5)

        self.feature = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.feature.grid(column=2, row=3, sticky=tk.W + tk.E, padx=100, pady=5)

        # Loeschen
        delete_label_roles_window = tk.Label(input_frame_roles_window, text="Löschen",
                                             font=("Arial", size_roles_window), background="white")
        delete_label_roles_window.grid(column=1, row=4, sticky=tk.W + tk.E, padx=100, pady=5)

        self.delete = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.delete.grid(column=2, row=4, sticky=tk.W + tk.E, padx=100, pady=5)

        # Bearbeiten
        edit_label_roles_window = tk.Label(input_frame_roles_window, text="Bearbeiten",
                                           font=("Arial", size_roles_window), background="white")
        edit_label_roles_window.grid(column=1, row=5, sticky=tk.W + tk.E, padx=100, pady=5)

        self.edit = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.edit.grid(column=2, row=5, sticky=tk.W + tk.E, padx=100, pady=5)

        # Erstellen
        create_label_roles_window = tk.Label(input_frame_roles_window, text="Erstellen",
                                             font=("Arial", size_roles_window), background="white")
        create_label_roles_window.grid(column=1, row=6, sticky=tk.W + tk.E, padx=100, pady=5)

        self.create = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.create.grid(column=2, row=6, sticky=tk.W + tk.E, padx=100, pady=5)

        # Gruppe Loeschen
        delete_g_label_roles_window = tk.Label(input_frame_roles_window, text="Gruppe Löschen" ,
                                               font=("Arial", size_roles_window), background="white")
        delete_g_label_roles_window.grid(column=1, row=7, sticky=tk.W + tk.E, padx=100, pady=5)

        self.delete_g = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.delete_g.grid(column=2, row=7, sticky=tk.W + tk.E, padx=100, pady=5)

        # Gruppe Erstellen
        create_g_label_roles_window = tk.Label(input_frame_roles_window, text="Gruppe Erstellen",
                                               font=("Arial", size_roles_window), background="white")
        create_g_label_roles_window.grid(column=1, row=8, sticky=tk.W + tk.E, padx=100, pady=5)

        self.create_g = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.create_g.grid(column=2, row=8, sticky=tk.W + tk.E, padx=100, pady=5)

        # Gruppe Bearbeiten
        edit_g_label_roles_window = tk.Label(input_frame_roles_window, text="Gruppe Bearbeiten",
                                             font=("Arial", size_roles_window), background="white")
        edit_g_label_roles_window.grid(column=1, row=9, sticky=tk.W + tk.E, padx=100, pady=5)

        self.edit_g = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.edit_g.grid(column=2, row=9, sticky=tk.W + tk.E, padx=100, pady=5)

        # Rollen Erstellen
        create_r_label_roles_window = tk.Label(input_frame_roles_window, text="Rollen Erstellen",
                                               font=("Arial", size_roles_window), background="white")
        create_r_label_roles_window.grid(column=1, row=10, sticky=tk.W + tk.E, padx=100, pady=10)

        self.create_r = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.create_r.grid(column=2, row=10, sticky=tk.W + tk.E, padx=100, pady=5)

        # Rollen Bearbeiten
        edit_r_label_roles_window = tk.Label(input_frame_roles_window, text="Rollen Bearbeiten",
                                             font=("Arial", size_roles_window), background="white")
        edit_r_label_roles_window.grid(column=1, row=11, sticky=tk.W + tk.E, padx=100, pady=5)

        self.edit_r = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.edit_r.grid(column=2, row=11, sticky=tk.W + tk.E, padx=100, pady=5)

        # Rollen Loeschen
        delete_r_label_roles_window = tk.Label(input_frame_roles_window, text="Rolle Löschen",
                                               font=("Arial", size_roles_window), background="white")
        delete_r_label_roles_window.grid(column=1, row=12, sticky=tk.W + tk.E, padx=100, pady=5)

        self.delete_r = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.delete_r.grid(column=2, row=12, sticky=tk.W + tk.E, padx=100, pady=5)

        # Funktion zum Eintrag hinzufügen
        def refresh_entry():
            """
            Eine Klasse, die ein GUI-Frame-Fenster darstellt und Funktionen zur Darstellung
            und Aktualisierung von Benutzerinformationen bietet. Die Klasse wird in einem
            TKinter-Anwendungsrahmen verwendet und bietet Methoden zum Aktualisieren von
            Benutzerdaten in einer Datenbank und zum Wechseln zwischen Fenstern.

            Attributes:
                name (tk.StringVar): Der Name des Benutzers, dessen Daten aktualisiert
                    werden sollen.
                email (tk.StringVar): Die zu aktualisierende E-Mail-Adresse des Benutzers.
                role_combobox (ttk.Combobox): Die ComboBox, die die Rolle des Benutzers
                    enthält und aktualisiert werden kann.

            """
            #update
            from .adminUserWindow import adminUserWindow
            adminUserWindow.update_treeview_with_data()
            controller.show_frame(adminUserWindow)

        def delete_entry():
            """
            Diese Klasse erstellt ein Fenster, das als Frame fungiert und zur Verwaltung von
            Benutzerdetails in einer Anwendung dient. Die Instanz dieser Klasse kann Teil
            eines größeren Tkinter-basierten GUI-Systems sein. Sie enthält Methoden, um
            Einträge zu entfernen und die Anzeige zu aktualisieren.

            :Attributes:
                parent:
                    Das Eltern-Widget, in welchem dieses Frame eingebettet wird.
                controller:
                    Der übergeordnete Controller, der die Navigation zwischen Frames
                    innerhalb der Anwendung verwaltet.

            :Methods:
                delete_entry():
                    Löscht Benutzereinträge aus der Datenbank und erneuert die entsprechende
                    Anzeige im adminUserWindow-Frame.
            """
            sqlapi.delete_benutzer(self.name.get())
            from .adminUserWindow import adminUserWindow
            adminUserWindow.update_treeview_with_data()
            controller.show_frame(adminUserWindow)

        self.edit_btn = tk.PhotoImage(file=resource_path("./includes/assets/AktualisierenBig_blue.png"))
        self.lend_btn = tk.PhotoImage(file=resource_path("./includes/assets/Ausleihen.png"))
        self.delete_btn = tk.PhotoImage(file=resource_path("./includes/assets/Loeschen.png"))

        # Buttons in ein separates Frame
        button_frame_update_role = tk.Frame(self, background="white")
        button_frame_update_role.grid(row=2, column=0, pady=20)

        delete_button = tk.Button(button_frame_update_role, image=self.delete_btn,
                                 bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                                 command= delete_entry)
        delete_button.pack(side=tk.LEFT, padx=20)  # Neben Exit-Button platzieren


        edit_button = tk.Button(button_frame_update_role, image=self.edit_btn,
                               bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                               command=refresh_entry)
        edit_button.pack(side=tk.LEFT, padx=20)  # Links platzieren

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(0, weight=1)

    def update_data(self, data):
        """
        Aktualisiert die Daten in den Entry-Feldern mit den bereitgestellten Informationen.
        Existierende Einträge in den Feldern werden gelöscht und durch die neuen Daten ersetzt.

        :param data: Eine Liste, die die neuen Daten für die Entry-Felder enthält.
                    Das erste Listenelement entspricht dem neuen Wert für `room_num_entry`.
                    Das zweite Listenelement entspricht dem neuen Wert für `place_entry`.

        """
        # Daten in die Entry-Felder einfügen
        self.role_name.configure(text=data[0])