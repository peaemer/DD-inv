import sys
import tkinter as tk
from tkinter import ttk
import cache

LARGEFONT = ("Arial", 25)
LOGINFONT = ("Arial", 15)  # Angepasste Font-Größe für Eingabe
srhGrey = "#d9d9d9"
srhOrange = "#DF4807"

class logInWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")

        def logIn():
            password = passwordEntry.get().strip()
            user = usernameEntry.get().strip()
            import Security.UserSecurity as security
            if security.verifyUser(user, password):
                cache.user_group = "admin"
                cache.user_name = user
                from .mainPage import mainPage
                controller.show_frame(mainPage)
            else:
                sys.exit()

        def on_enter(event):
            logIn()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        headerFrame = tk.Frame(self, height=10, background=srhOrange)
        headerFrame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

        self.srhHead = tk.PhotoImage(file="assets/srhHeader.png")
        srhHeader = tk.Label(headerFrame, image=self.srhHead, bd=0, bg=srhOrange)
        srhHeader.grid(padx=10, pady=10, row=0, column=0, sticky=tk.W + tk.N + tk.E)

        # GreyFrame
        greyCanvas = tk.Canvas(self, bg="white", highlightthickness=0)
        greyCanvas.grid(row=1, column=0, sticky="nsew")  # Verwende "nsew" für vollständige Dehnung

        # Konfiguriere die Spalten- und Zeilenverhältnisse so, dass sie sich dynamisch verteilen
        self.grid_columnconfigure(0, weight=1)  # Spalte 0 kann sich ausdehnen
        self.grid_rowconfigure(1, weight=1)  # Zeile 1 (wo das greyCanvas liegt) kann sich ausdehnen

        # Login-Formular mit abgerundeten Eingabefeldern
        formFrame = tk.Frame(self, bg="white")
        formFrame.place(relx=0.5, rely=0.5, anchor="center")

        # Funktion zur Erstellung abgerundeter Ecken
        def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
            """Erstellt ein Rechteck mit abgerundeten Ecken."""
            points = [
                x1 + radius, y1,
                x1 + radius, y1,
                x2 - radius, y1,
                x2 - radius, y1,
                x2, y1,
                x2, y1 + radius,
                x2, y2 - radius,
                x2, y2 - radius,
                x2, y2,
                x2 - radius, y2,
                x2 - radius, y2,
                x1 + radius, y2,
                x1 + radius, y2,
                x1, y2,
                x1, y2 - radius,
                x1, y1 + radius,
                x1, y1 + radius,
                x1, y1,
            ]
            return canvas.create_polygon(points, smooth=True, **kwargs)

        # Abgerundeter Hintergrund mit der neuen Funktion
        create_rounded_rectangle(greyCanvas, 20, 20, 490, 90, radius=30, fill=srhGrey, outline="")
        greyCanvas.create_text(
            250, 55, text="Willkommen bei DD-Inv", font=LARGEFONT, fill="black"
        )

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
            formFrame, text="Benutzername", font=LARGEFONT, bg="white"
        ).grid(column=0, row=0, pady=10)
        usernameCanvas = tk.Canvas(formFrame, width=350, height=50, bg="white", highlightthickness=0)
        usernameCanvas.grid(column=0, row=1, pady=10)
        usernameVar = tk.StringVar()
        usernameEntry = create_rounded_entry(usernameCanvas, formFrame, usernameVar)

        # Passwort
        tk.Label(
            formFrame, text="Passwort", font=LARGEFONT, bg="white"
        ).grid(column=0, row=2, pady=10)
        passwordCanvas = tk.Canvas(formFrame, width=350, height=50, bg="white", highlightthickness=0)
        passwordCanvas.grid(column=0, row=3, pady=10)
        passwordVar = tk.StringVar()
        passwordEntry = create_rounded_entry(passwordCanvas, formFrame, passwordVar)
        passwordEntry.config(show="*")

        # Login-Button
        self.logOutBtn = tk.PhotoImage(file="assets/Anmelden.png")
        loginButton = tk.Button(
            formFrame,
            image=self.logOutBtn,
            bg="white",
            command=logIn,
            bd=0,
            relief=tk.FLAT,
            activebackground="white",
        )
        loginButton.grid(column=0, row=4, pady=20, sticky="ew")

        # Bind die Enter-Taste
        usernameEntry.bind("<Return>", on_enter)
        passwordEntry.bind("<Return>", on_enter)
