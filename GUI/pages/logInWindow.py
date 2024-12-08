import sys
import tkinter as tk
import webbrowser
from tkinter import *
from tkinter import ttk, messagebox
import cache
import Datenbank.sqlite3api as db

LARGEFONT = ("Arial", 25)
LOGINFONT = ("Arial", 15)  # Angepasste Font-Größe für Eingabe
srhGrey = "#d9d9d9"
srhOrange = "#DF4807"

class logInWindow(tk.Frame):
    """
    Represents a login window frame for the application, designed to interface with
    a `controller` to facilitate user authentication and navigation. This class
    manages user input for authentication, updates cache with user details, and
    controls the display transition based on authentication success. It includes
    UI elements like rounded entry fields and buttons, constructed using the
    Tkinter library.

    :ivar srh_head: Image for the header logo located at 'assets/srhHeader.png'.
    :type srh_head: tk.PhotoImage
    :ivar log_out_btn: Image for the login button located at 'assets/Anmelden.png'.
    :type log_out_btn: tk.PhotoImage
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")

        def log_in():
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
            log_in()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        header_frame = tk.Frame(self, height=10, background=srhOrange)
        header_frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

        self.srh_head = tk.PhotoImage(file="assets/srhHeader.png")
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
        self.grid_rowconfigure(1, weight=1)  # Zeile 1 (wo das greyCanvas liegt) kann sich ausdehnen

        # Login-Formular mit abgerundeten Eingabefeldern
        form_frame = tk.Frame(self, bg="white")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        def create_rounded_entry(canvas, parent, text_var, width=350, height=50):
            """Hilfsfunktion, um ein Eingabefeld mit abgerundeten Ecken zu erstellen."""
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
        btn_links_label = ttk.Label(bottom_frame, background="white", text="VersionBuild   V. 0.0.291 (Alpha)", cursor="hand2", font=("Arial", 12))
        btn_links_label.grid(row=18, column=0, pady=2, sticky="new")
        btn_links_label.configure(width=30, anchor='center', image=logo_image, compound="left")
        btn_links_label.bind("<Button-1>", lambda e: open_VersionBuild("https://github.com/peaemer/DD-inv/commit/2253443a1349e58db31ef8592bf77d3a7afda198"))
