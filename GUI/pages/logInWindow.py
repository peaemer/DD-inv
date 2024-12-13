import json
import sys
import tkinter as tk
import webbrowser
from tkinter import *
from tkinter import ttk, messagebox
import cache
import Datenbank.sqlite3api as db
from GUI.SearchBar import *

LARGEFONT = ("Arial", 25)
LOGINFONT = ("Arial", 15)  # Angepasste Font-Größe für Eingabe
srhGrey = "#d9d9d9"
srhOrange = "#DF4807"

class logInWindow(tk.Frame):
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
    """
    def __init__(self, parent, controller):
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
            cache.user_group = ""
            cache.user_name = ""

            # Importiere Sicherheits- und Datenbankmodule
            import Security.UserSecurity as security

            if security.verifyUser(user, password):  # Benutzer authentifizieren
                # Benutzerinformationen aus der Datenbank abrufen
                benutzer_info = db.read_benutzer(user)
                cache.user_group = benutzer_info.get('Rolle', '')  # Rolle des Benutzers speichern
                cache.user_name = user  # Benutzernamen im Cache speichern
                cache.loaded_history = json.loads(db.read_benutzer_suchverlauf(cache.user_name)) if db.read_benutzer_suchverlauf(cache.user_name) else json.loads("""[{"":""}]""")
                # cache.user_avatar = benutzer_info.get("Avatar", "")  Für Profilbilder in Datenbank

                password_entry.delete(0, 'end')
                username_entry.delete(0, 'end')
                # Zeige die MainPage an
                from .mainPage import mainPage
                controller.show_frame(mainPage)

            else:
                # Zeige Fehlermeldung bei falschem Login
                messagebox.showinfo(title="Fehler", message="Passwort oder Benutzername falsch")
                password_entry.delete(0, 'end')


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
        header_frame = tk.Frame(self, height=10, background=srhOrange)
        header_frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

        self.srh_head = tk.PhotoImage(file="assets/srhHeader.png")
        print(self.srh_head.name)
        print(self.srh_head.get(10,10))
        srh_header = tk.Label(header_frame, image=self.srh_head, bd=0, bg=srhOrange)
        srh_header.grid(padx=10, pady=10, row=0, column=0, sticky=tk.W + tk.N + tk.E)

        grey_frame = tk.Frame(self, height=10, background=srhGrey)
        grey_frame.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N)

        # Text im GreyFrame
        grey_label = tk.Label(
            grey_frame,
            text="Willkommen bei DD-Inv",
            font=LARGEFONT,
            bg=srhGrey,
            fg="black",
            anchor="center"
        )
        grey_label.pack(expand=True, fill="both")  # Text zentrieren und Frame ausfüllen

        # Konfiguriere die Spalten- und Zeilenverhältnisse so, dass sie sich dynamisch verteilen
        self.grid_columnconfigure(0, weight=1)  # Spalte 0 kann sich ausdehnen
        self.grid_rowconfigure(1, weight=0)  # Zeile 1 (wo das greyCanvas liegt) kann sich ausdehnen


        # Login-Formular mit abgerundeten Eingabefeldern
        form_frame = tk.Frame(self, bg="white")
        form_frame.grid(row=2, column=0, sticky="nesw", pady=60)

        form_frame.grid_columnconfigure(0, weight=1)

        def create_rounded_entry(canvas, parent, text_var, width=350, height=50):
            """
            Erstellt ein abgerundetes Eingabefeld innerhalb eines Canvas-Widgets. Die Funktion unterstützt
            die Erstellung eines grafischen, abgerundeten Rahmens und platziert ein `tk.Entry`-Widget,
            welches durch eine gegebene Textvariable gesteuert werden kann. Die Breite, Höhe und
            Gestaltung des Rahmens können angepasst werden.

            :param canvas: Das Canvas-Widget, innerhalb dessen das abgerundete Eingabefeld erstellt wird.
                Typ: tkinter.Canvas
            :param parent: Das übergeordnete Widget, in dem das Eingabefeld platziert wird.
                Typ: tkinter.Widget
            :param text_var: Die Textvariable, die den Inhalt des Eingabefeldes steuert.
                Typ: tkinter.StringVar
            :param width: Die Breite des abgerundeten Eingabefeldes. Standardwert ist 350.
                Typ: int
            :param height: Die Höhe des abgerundeten Eingabefeldes. Standardwert ist 50.
                Typ: int
            :return: Das erstellte Eingabefeld (tk.Entry).
                Typ: tkinter.Entry
            """
            radius = 20  # Radius für die Ecken
            canvas.create_oval(
                0, 0, radius * 2, radius * 2, fill="#f0f0f0", outline="#f0f0f0"
            )
            canvas.create_oval(
                width - radius * 2,
                0,
                width,
                radius * 2,
                fill="#f0f0f0",
                outline="#f0f0f0",
            )
            canvas.create_oval(
                0,
                height - radius * 2,
                radius * 2,
                height,
                fill="#f0f0f0",
                outline="#f0f0f0",
            )
            canvas.create_oval(
                width - radius * 2,
                height - radius * 2,
                width,
                height,
                fill="#f0f0f0",
                outline="#f0f0f0",
            )
            canvas.create_rectangle(
                radius, 0, width - radius, height, fill="#f0f0f0", outline="#f0f0f0"
            )
            canvas.create_rectangle(
                0, radius, width, height - radius, fill="#f0f0f0", outline="#f0f0f0"
            )
            entry = tk.Entry(
                parent,
                textvariable=text_var,
                font=LOGINFONT,
                bg="#f0f0f0",
                relief=tk.FLAT,
                justify="center",
            )
            canvas.create_window(width // 2, height // 2, window=entry, width=width - 10)
            return entry

        # Username
        tk.Label(
            form_frame, text="Benutzername", font=LARGEFONT, bg="white"
        ).grid(column=0, row=0, pady=10)
        username_canvas = tk.Canvas(form_frame, width=350, height=50, bg="white", highlightthickness=0)
        username_canvas.grid(column=0, row=1, pady=10)
        username_var = tk.StringVar()
        username_entry = create_rounded_entry(username_canvas, form_frame, username_var)

        # Passwort
        tk.Label(
            form_frame, text="Passwort", font=LARGEFONT, bg="white"
        ).grid(column=0, row=2, pady=10)
        password_canvas = tk.Canvas(form_frame, width=350, height=50, bg="white", highlightthickness=0)
        password_canvas.grid(column=0, row=3, pady=10)
        password_var = tk.StringVar()
        password_entry = create_rounded_entry(password_canvas, form_frame, password_var)
        password_entry.config(show="*")

        # Login-Button
        self.log_out_btn = tk.PhotoImage(file="assets/Anmelden.png")
        login_button = tk.Button(
            form_frame,
            image=self.log_out_btn,
            bg="white",
            command=log_in,
            bd=0,
            relief=tk.FLAT,
            activebackground="white",
        )
        login_button.grid(column=0, row=4, pady=20, sticky="ew")

        # Bind die Enter-Taste
        username_entry.bind("<Return>", on_enter)
        password_entry.bind("<Return>", on_enter)

        # Bottom
        bottom_frame = tk.Frame(self, height=10, background="white")
        bottom_frame.grid(row=3, column=0, sticky=tk.W + tk.E + tk.S)

        def open_VersionBuild(url):
            webbrowser.open(url)

        logo_image = PhotoImage(file="assets/DD-Inv_Logo.png")
        btn_links_label = ttk.Label(bottom_frame, background="white", text="VersionBuild   V. 0.0.311 (Alpha)", cursor="hand1", font=("Arial", 12))
        btn_links_label.grid(row=18, column=0, pady=2, sticky="new")
        btn_links_label.configure(width=30, anchor='center', image=logo_image, compound="left")
        btn_links_label.bind("<Button-1>", lambda e: open_VersionBuild("https://github.com/peaemer/DD-inv/commit/3cf34836049538c57b3cac282a740703e0312ba7"))
