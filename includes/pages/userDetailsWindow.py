import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
from includes.sec_data_info import sqlite3api as db
from includes.sec_data_info import UserSecurity as sec
import cache
import random, string

LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"


def show_user_details(selected_user, tree, controller):
    # Daten aus der ausgewählten Zeile
    data = tree.item(selected_user, "values")
    print(f"Daten des ausgewählten Items: {data}")
    cache.selected_ID = data[0]
    controller.show_frame(userDetailsWindow)  # Zeige die Details-Seite
    # Frame aktualisieren und anzeigen
    details = controller.frames[userDetailsWindow]
    details.update_data(data)  # Methode in detailsWindow aufrufen



class userDetailsWindow(tk.Frame):
    """
    Repräsentiert ein Fenster für Benutzerdetails innerhalb einer Tkinter-Anwendung.

    Diese Klasse ist für die Anzeige und Bearbeitung der Benutzerdetails verantwortlich. Sie
    bietet die Möglichkeit, Benutzerinformationen einzusehen, Passwörter zurückzusetzen sowie
    Rollen und E-Mails zu ändern. Außerdem verfügt das Fenster über Funktionalitäten wie das
    Navigieren zu anderen Fenstern oder das Hinzufügen, Aktualisieren und Löschen von Benutzerdaten.

    :ivar controller: Eine Referenz auf den Controller, der die Fensterverwaltung regelt.
    :type controller: Any
    :ivar go_back_btn_details_window: Bildressource für den Zurück-Button.
    :type go_back_btn_details_window: tkinter.PhotoImage
    :ivar opt_btn_details_window: Bildressource für den Optionen-Button.
    :type opt_btn_details_window: tkinter.PhotoImage
    :ivar name: Eingabefeld für den Benutzernamen.
    :type name: tkinter.Entry
    :ivar reset_password: Button zum Zurücksetzen des Benutzerpassworts.
    :type reset_password: tkinter.Button
    :ivar email: Eingabefeld für die E-Mail-Adresse des Benutzers.
    :type email: tkinter.Entry
    :ivar role_combobox: Dropdown-Feld für die Auswahl der Benutzerrolle.
    :type role_combobox: tkinter.ttk.Combobox
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="white")

        def go_back_details_window():
            """
            Repräsentiert ein Fenster innerhalb einer tkinter-Anwendung, das
            spezifisch für Benutzerdetails gestaltet ist. Dieses Fenster ist ein
            Unterrahmen (`tk.Frame`) und wird von einem übergeordneten tkinter-
            Controller genutzt, um eine Navigation zwischen verschiedenen Fenstern
            zu ermöglichen.

            Attributes:
                parent (tk.Widget): Der übergeordnete tkinter-Widget, der dieses Frame enthält.
                controller: Der Controller, der das Fenster-Management und die
                            Navigation zwischen den Frames steuert.

            Methods:
                go_back_details_window: Navigiert zurück zum Fenster der Benutzerverwaltung.

            :param parent: Der übergeordnete tkinter-Widget, der dieses Frame enthält.
            :param controller: Der Controller, der für die Navigation zwischen Frames
                               verwendet wird.
            """
            from .adminUserWindow import adminUserWindow
            controller.show_frame(adminUserWindow)

        def show_settings_window_details_window():
            """
            Eine Klasse, die ein Tkinter-Frame zur Darstellung eines Benutzerdetails-Fensters
            repräsentiert. Diese Klasse enthält eine Methode, die ein Einstellungsfenster
            zeigt.

            :ivar parent: Das übergeordnete Tkinter-Widget, zu dem dieses Frame gehört.
            :ivar controller: Ein Controller, der verwendet wird, um die Navigation oder
                Steuerung zwischen verschiedenen Frames im Tkinter-Fenster zu ermöglichen.
            """
            print("Show settings window details window")
            from .settingsWindow import pop_up_settings
            pop_up_settings(self, controller)


        def reset_pass():
            """
            Eine Benutzeroberfläche zur Anzeige und Verwaltung der Details eines Benutzers.
            Diese Klasse dient als übergeordneter Rahmen für spezifische Benutzerfunktionen,
            einschließlich der Möglichkeit, das Passwort eines Benutzers zurückzusetzen. Sie
            bietet Schnittstellen für die Kommunikation mit anderen Fenstern.

            :ivar name: Name des aktuellen Benutzers, dessen Details angezeigt werden.
            :type name: tkinter.StringVar
            :ivar controller: Referenz auf den Hauptcontroller der Anwendung, der das
                Rahmenrouting steuert.
            :type controller: Any
            """
            pw = str(''.join(random.choices(string.ascii_letters, k=7)))
            db.update_benutzer(self.name.get(), neues_passwort=pw)
            messagebox.showinfo(title="Reseted User Password", message="New password: " + pw)
            from .adminUserWindow import adminUserWindow
            adminUserWindow.update_treeview_with_data()
            controller.show_frame(adminUserWindow)

        self.go_back_btn_details_window = tk.PhotoImage(file="includes/assets/ArrowLeft.png")

        # Erstelle einen Header-Bereich
        header_frame_details_window = tk.Frame(self, height=10, background="#00699a")
        header_frame_details_window.grid(row=0, column=0,columnspan=2, sticky=tk.W + tk.E + tk.N)

        # Überschrift mittig zentrieren
        header_frame_details_window.grid_columnconfigure(0, weight=1)  # Platz links
        header_frame_details_window.grid_columnconfigure(1, weight=3)  # Überschrift zentriert (größerer Gewichtungsfaktor)
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

        from ._avatarManager import loadImage
        self.avatar = loadImage(parent=parent)

        options_button_details_window = tk.Button(
            header_frame_details_window,
            image=self.avatar,
            command=show_settings_window_details_window,
            bd=0,
            relief=tk.FLAT,
            bg="#00699a",
            activebackground="#00699a"
        )
        options_button_details_window.grid(row=0, column=2, sticky=tk.E, padx=20)


        # Container für Input- und Tree-Frame
        container_frame = tk.Frame(self, background="white")
        container_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Konfiguration der Container-Spalten
        container_frame.grid_columnconfigure(0, weight=1)  # Baumansicht
        container_frame.grid_columnconfigure(1, weight=1)  # Eingabefelder



        size_details_window = 30



        # Ändere die Position des TreeFrames
        tree_frame_details_window = tk.Frame(container_frame, background="red", width=200, height=400)
        tree_frame_details_window.grid(row=0, column=0, padx=40, sticky="")

        tree_details_window = ttk.Treeview(tree_frame_details_window, column=("c1", "c2", "c3"), show="headings", height=30)

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
        tree_details_window.heading("# 1", text="Name", )
        tree_details_window.column("# 2", anchor=CENTER, width=200)
        tree_details_window.heading("# 2", text="ServiceTag/ID")
        tree_details_window.column("# 3", anchor=CENTER, width=220)
        tree_details_window.heading("# 3", text="Ausgeliehen am")
        tree_details_window.grid(row=1, column=0)
        tree_details_window.tkraise()

        # Input-Frame
        input_frame_details_window = tk.Frame(container_frame, background="white")
        input_frame_details_window.grid(row=0, column=1, pady=20, sticky="nsew")

        input_frame_details_window.grid_columnconfigure(0, weight=1)  # Zentriere das Input-Frame
        input_frame_details_window.grid_columnconfigure(1, weight=1)

        #Nutzername
        name = tk.Label(input_frame_details_window, text="Nutzername",
                                                font=("Arial", size_details_window), background="white")
        name.grid(column=0, row=0, sticky=tk.W + tk.E, padx=20, pady=10)

        self.name = tk.Entry(input_frame_details_window, font=("Arial", size_details_window),
                             background=srhGrey, relief=tk.SOLID)
        self.name.grid(column=1, row=0, sticky=tk.W + tk.E, padx=20, pady=10)

        #Passwort
        password_label_details_window = tk.Label(input_frame_details_window, text="Passwort",
                                          font=("Arial", size_details_window), background="white")
        password_label_details_window.grid(column=0, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        self.reset_password = tk.Button(input_frame_details_window, font=("Arial", 24),text="Passwort zurücksetzen" ,command=reset_pass,
                                                  background=srhGrey, relief=tk.SOLID)
        self.reset_password.grid(column=1, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        #Email
        email_label_details_window = tk.Label(input_frame_details_window, text="E-Mail",
                                          font=("Arial", size_details_window), background="white")
        email_label_details_window.grid(column=0, row=2, sticky=tk.W + tk.E, padx=20, pady=10)

        self.email = tk.Entry(input_frame_details_window, font=("Arial", size_details_window),
                              background=srhGrey, relief=tk.SOLID)
        self.email.grid(column=1, row=2, sticky=tk.W + tk.E, padx=20, pady=10)

        #Rolle
        role_label_details_window = tk.Label(input_frame_details_window, text="Rolle",
                                          font=("Arial", size_details_window), background="white")
        role_label_details_window.grid(column=0, row=3, sticky=tk.W + tk.E, padx=20, pady=10)

        role_values = []
        for room in db.read_all_rollen():
            role_values.append(room['Rolle'])
        self.role_combobox = ttk.Combobox(input_frame_details_window, values=role_values,
                                          font=("Arial", size_details_window))
        self.role_combobox.grid(row=3, column=1, padx=20, pady=20, sticky=tk.W + tk.E)


        # Funktion zum Eintrag hinzufügen
        def refresh_entry():
            """
            Eine Klasse, die ein Benutzerdetails-Fenster darstellt, das in einer tkinter-Anwendung verwendet wird.
            Diese Klasse erbt von ``tk.Frame`` und implementiert die Logik zur Aktualisierung eines Benutzers in der
            Datenbank und zur Navigation zu einem anderen Fenster.

            Attribute:
            ----------
            parent : tk.Widget
                Das übergeordnete Widget, zu dem dieses Frame gehört.
            controller : Any
                Ein Controller, der zur Verwaltung der Fensterwechsel in der Anwendung verwendet wird.
            name : tk.StringVar
                Eine Variable, die den Namen des Benutzers hält und mit dem Eingabefeld verbunden ist.
            email : tk.StringVar
                Eine Variable, die die E-Mail-Adresse des Benutzers hält und mit dem Eingabefeld verbunden ist.
            role_combobox : ttk.Combobox
                Ein Combobox-Widget, das die Rolle des Benutzers anzeigt und geändert werden kann.
            """
            #update
            db.update_benutzer(self.name.get(), neues_email=self.email.get(), neue_rolle=self.role_combobox.get())
            from .adminUserWindow import adminUserWindow
            adminUserWindow.update_treeview_with_data()
            controller.show_frame(adminUserWindow)

        def delete_entry():
            """
            Eine Klasse, die ein Fenster zur Darstellung und Bearbeitung von Benutzerdetails
            in einer GUI-Anwendung repräsentiert. Die Klasse erbt von `tk.Frame`.

            Attributes
            ----------
            parent : tk.Widget
                Der übergeordnete Rahmen oder das übergeordnete Widget für dieses Frame.
            controller : Any
                Eine Steuerungsinstanz, die für den Wechsel von Fenstern in der Anwendung
                verantwortlich ist.

            Methods
            -------
            delete_entry()
                Löscht Benutzereinträge aus der Datenbank und aktualisiert die
                Benutzeransicht.
            """
            db.delete_benutzer(self.name.get())
            from .adminUserWindow import adminUserWindow
            adminUserWindow.update_treeview_with_data()
            controller.show_frame(adminUserWindow)

        self.edit_btn = tk.PhotoImage(file="includes/assets/AktualisierenBig_blue.png")
        self.lend_btn = tk.PhotoImage(file="includes/assets/Ausleihen.png")
        self.delete_btn = tk.PhotoImage(file="includes/assets/Loeschen.png")

        # Buttons in ein separates Frame
        button_frame_add_item_popup = tk.Frame(self, background="white")
        button_frame_add_item_popup.grid(row=2, column=0, pady=20)

        delete_button = tk.Button(button_frame_add_item_popup, image=self.delete_btn,
                                 bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                                 command= delete_entry)
        delete_button.pack(side=tk.LEFT, padx=20)  # Neben Exit-Button platzieren


        edit_button = tk.Button(button_frame_add_item_popup, image=self.edit_btn,
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
        Fügt Daten in die entsprechenden Entry-Felder und die Combobox ein.

        :param data: Eine Liste mit Werten, wobei jedes Element spezifischen Daten zugeordnet ist. Der zweite Wert
                     (`data[1]`) repräsentiert den Namen, der vierte Wert (`data[3]`) die E-Mail und der fünfte Wert
                     (`data[4]`) die Rolle, die in das Combobox-Feld gesetzt wird.
        :type data: list
        :return: None
        """
        # Daten in die Entry-Felder einfügen
        self.name.delete(0, tk.END)
        self.name.insert(0, data[1])

        self.email.delete(0, tk.END)
        self.email.insert(0, data[3])

        self.role_combobox.set(data[4])  # Platzhalter