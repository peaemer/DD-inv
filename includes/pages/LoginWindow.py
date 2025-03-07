import tkinter as tk
import webbrowser
from tkinter import *
from tkinter import ttk
import customtkinter as ctk

from .customMessageBoxDelete import *
from ._avatarManager import check_internet_connection, loadImage
from includes.sec_data_info import sqlite3api as db


class LoginWindow(tk.Frame):
    """
    Eine Klasse, die ein Login-Fenster für die Anwendung darstellt.

    Dieses Fenster dient als Benutzeroberfläche für den Login in die Anwendung. Es enthält
    unter anderem Eingabefelder für die Eingabe des Benutzernamens und des Passworts, sowie
    einen Button zur Authentifizierung. Die Klasse übernimmt die Darstellung und die
    grundlegende Verarbeitung von Benutzerdaten zur Anmeldung.

    :ivar srh_head: Enthält das Bild für den Header des Fensters.
    :type srh_head: tk.PhotoImage
    :ivar log_out_btn: Enthält das Bild für den Button zur Anmeldung.
    :type log_out_btn: tk.PhotoImage

    ExampleClass::f: example method
    """
    def __init__(self, parent, controller):
        check_internet_connection()
        tk.Frame.__init__(self, parent)
        self.configure(background="white")

        def log_in():
            """
            Eine Klasse, die ein Login-Fenster als GUI-Komponente bereitstellt. Die Klasse
            erweitert `tk.Frame` und bietet eine Funktionalität für die Benutzeranmeldung,
            einschließlich der Überprüfung der Anmeldeinformationen und der Weiterleitung
            zu einer Hauptseite bei erfolgreicher Authentifizierung. Die Benutzerdaten werden
            im Cache gespeichert, um die Benutzerrolle und andere Aspekte festzulegen.

            Attributes
            ----------
            parent : tk.Tk
                Der übergeordnete Rahmen, in dem der Login-Rahmen eingebunden wird.
            controller : tk.Tk
                Der Controller, der zur Steuerung des Frames und des Seitenwechsels verwendet wird.

            Methods
            -------
            log_in()
                Führt die Authentifizierung der Benutzerdaten durch und leitet den Benutzer
                bei erfolgreicher Anmeldung auf die Hauptseite weiter.
            """
            password = password_entry.get().strip()
            user = username_entry.get().strip()

            # Reset cache für Benutzerinformationen
            cache.user_group = None
            cache.user_name = None

            # Importiere Sicherheits- und Datenbankmodule
            from includes.sec_data_info import UserSecurity as security

            if security.verify_user(user, password):  # Benutzer authentifizieren
                # Benutzerinformationen aus der Datenbank abrufen
                benutzer_info = db.read_benutzer(user)
                cache.user = benutzer_info
                cache.user_group = benutzer_info.get('Rolle', '')  # Rolle des Benutzers speichern
                cache.user_name = user  # Benutzernamen im Cache speichern
                cache.user_group_data = next((rolle for rolle in db.read_all_rollen() if rolle['Rolle'] == cache.user_group), None)
                cache.user_avatar = loadImage(parent=parent, image=db.get_avatar_info(user), defult_image=cache.user_default_avatar, width=48, height=48) if cache.internet else loadImage(parent=parent, image=cache.user_default_avatar, width=48, height=48)
                cache.user_avatarx128 = loadImage(parent=parent, image=db.get_avatar_info(user), defult_image=cache.user_default_avatar, width=128, height=128) if cache.internet else loadImage(parent=parent, image=cache.user_default_avatar, width=128, height=128)

                password_entry.delete(0, 'end')
                username_entry.delete(0, 'end')
                # Zeige die MainPage an
                from .MainPage import MainPage
                cache.controller = controller
                controller.show_frame(MainPage)

            else:
                # Zeige Fehlermeldung bei falschem Login
                customMessageBoxDelete(self,
                    title="Nutzername oder Passwort falsch",
                    message="Nutzername und Passwort stimmen nicht überein.\n Bitte versuchen Sie es erneut."
                )

        def on_enter(event):
            """
            Eine Klasse, die ein Anmeldefenster in einer GUI-Applikation darstellt. Sie erbt von
            tk.Frame und bietet Funktionen zur Benutzerinteraktion und Anmeldung.

            :param parent: Eltern-Widget, in dem sich diese Frame-Komponente befindet.
                Erwartet ein tkinter Widget.
            :param controller: Eine Controller-Instanz, die zur Navigation und Steuerung
                anderer GUI-Komponenten verwendet wird. Sollte sicherstellen, dass sie über
                die entsprechenden Methoden verfügt.

            """
            log_in()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # Header
        header_frame = tk.Frame(self,
            height=10,
            background=srh_orange
        )
        header_frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

        from ._avatarManager import resource_path
        self.srh_head = tk.PhotoImage(file=resource_path("./includes/assets/srhHeader.png"))
        srh_header = tk.Label(header_frame,
            image=self.srh_head,
            bd=0,
            bg=srh_orange
        )
        srh_header.grid(padx=10, pady=10, row=0, column=0, sticky=tk.W + tk.N + tk.E)

        grey_frame = tk.Frame(self,
            height=10,
            background=srh_grey
        )
        grey_frame.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N)

        # Text im GreyFrame
        grey_label = tk.Label(grey_frame,
            text="Willkommen bei DD-Inv",
            font=LARGEFONT,
            bg=srh_grey,
            fg="black",
            anchor="center"
        )
        grey_label.pack(expand=True, fill="both")  # Text zentrieren und Frame ausfüllen

        # Konfiguriere die Spalten- und Zeilenverhältnisse so, dass sie sich dynamisch verteilen
        self.grid_columnconfigure(0, weight=1)  # Spalte 0 kann sich ausdehnen
        self.grid_rowconfigure(1, weight=0)  # Zeile 1 (wo das greyCanvas liegt) kann sich ausdehnen

        # Login-Formular mit abgerundeten Eingabefeldern
        form_frame = tk.Frame(self, bg="white")
        form_frame.grid(row=2, column=0, sticky="nsew", pady=60)

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(2, weight=1)
        form_frame.grid_columnconfigure(3, weight=1)
        form_frame.grid_columnconfigure(4, weight=1)
        form_frame.grid_columnconfigure(5, weight=1)
        form_frame.grid_columnconfigure(6, weight=1)

        # Username
        tk.Label(form_frame,
            text="Benutzername",
            font=LARGEFONT,
            bg="white"
        ).grid(column=3, row=0, pady=10)

        username_entry = ctk.CTkEntry(form_frame,
            font=LOGINFONT,
            corner_radius=corner,
            fg_color=srh_grey,
            border_width=border,
            text_color="black",
            justify="center"
        )
        username_entry.grid(column=3, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        # Passwort
        tk.Label(form_frame,
            text="Passwort",
            font=LARGEFONT,
            bg="white"
        ).grid(column=3, row=2, pady=10)

        password_entry = ctk.CTkEntry(form_frame,
            font=LOGINFONT,
            corner_radius=corner,
            fg_color=srh_grey,
            border_width=border,
            text_color="black",
            show="•",
            justify="center"
        )
        password_entry.grid(column=3, row=3, sticky=tk.W + tk.E, padx=20, pady=10)

        # Login-Button
        self.log_out_btn = tk.PhotoImage(file=resource_path("./includes/assets/Anmelden.png"))
        login_button = tk.Button(form_frame,
            image=self.log_out_btn,
            bg="white",
            cursor="hand2",
            command=log_in,
            bd=0,
            relief=tk.FLAT,
            activebackground="white",
        )

        login_button.grid(column=3, row=4, pady=50, sticky="ew")

        # Bind die Enter-Taste
        username_entry.bind("<Return>", on_enter)
        password_entry.bind("<Return>", on_enter)

        # Bottom
        bottom_frame = tk.Frame(self, height=10, background="white")
        bottom_frame.grid(row=3, column=0, sticky=tk.W + tk.E + tk.S)

        def open_VersionBuild(url):
            webbrowser.open(url)

        parent.logo_image = PhotoImage(file=resource_path("./includes/assets/DD-Inv_Logo.png"))
        btn_links_label = ttk.Label(bottom_frame, background="white", text="VersionBuild   V. 1.2 STABLE", cursor="hand1", font=("Arial", 12))
        btn_links_label.grid(row=18, column=0, pady=2, sticky="new")
        btn_links_label.configure(width=30, anchor='center', image=parent.logo_image, compound="left")
        btn_links_label.bind("<Button-1>", lambda e: open_VersionBuild("https://github.com/peaemer/DD-inv/releases/latest"))
