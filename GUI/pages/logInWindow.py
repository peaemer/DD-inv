import tkinter as tk
<<<<<<< HEAD
from tkinter import ttk
from tkinter import *


=======
from tkinter import ttk, messagebox
import cache
>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13

LARGEFONT = ("Arial", 25)
LOGINFONT = ("Arial", 15)  # Angepasste Font-Größe für Eingabe
srhGrey = "#d9d9d9"
<<<<<<< HEAD

# Login-Fenster (erste Seite)
class logInWindow(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		defaultbg = self.cget('bg')
		self.configure(background="white")

		# Funktion für den Login-Button (Platzhalter)
		def logIn():
			from .mainPage import mainPage
			controller.show_frame(mainPage)

		# Konfiguriere das Grid-Layout für die Login-Seite
		self.grid_rowconfigure(0, weight=0)
		self.grid_rowconfigure(1, weight=1)
		self.grid_rowconfigure(2, weight=1)
		self.grid_columnconfigure(0, weight=1)

		# Erstelle einen Header-Bereich
		headerFrame = tk.Frame(self, height=10, background="#DF4807")
		headerFrame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

		self.srhHead = tk.PhotoImage(file="assets/srhHeader.png")

		# Füge einen Button mit dem Bild hinzu
		srhHeader = tk.Label(headerFrame, image=self.srhHead, bd=0, relief=tk.FLAT, bg="#DF4807", activebackground="#DF4807")
		srhHeader.grid(padx=20, pady=20, row=0, column=0, sticky=tk.W + tk.N)

		greyFrame = tk.Frame(self,height=10, background=srhGrey)
		greyFrame.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N)

		# Füge den LogIn-Label zur Frame hinzu
		logInLabel = tk.Label(greyFrame, text="Log In", bd=0, relief=tk.FLAT, bg=srhGrey, font=("Arial", 20))
		logInLabel.grid(padx=0, pady=5, row=0, column=0, sticky=tk.W + tk.E)

		# Konfiguriere den greyFrame für zentrierte Ausrichtung
		greyFrame.grid_columnconfigure(0, weight=1)

		# Erstelle das Login-Formular im mittleren Bereich
		loginFrame = tk.Frame(self, bg="white")
		loginFrame.grid(row=1, column=0, sticky=tk.N + tk.S, pady=100)

		# Füge die Eingabefelder für Username und Passwort hinzu
		usernameLabel = ttk.Label(loginFrame, text="Benutzername", font=LOGINFONT, background="white")
		usernameLabel.grid(column=0, row=1, sticky=tk.W + tk.E, padx=140, pady=5)

		usernameEntry = tk.Entry(loginFrame, bg=defaultbg, font=LOGINFONT, bd=0)
		usernameEntry.grid(column=0, row=2, sticky=tk.W + tk.E, padx=5, pady=5)

		passwordLabel = ttk.Label(loginFrame, text="Passwort", font=LOGINFONT, background="white")
		passwordLabel.grid(column=0, row=3, sticky=tk.W + tk.E, padx=190, pady=5)

		passwordEntry = tk.Entry(loginFrame, show="*", bg=defaultbg, font=LOGINFONT, bd=0)
		passwordEntry.grid(column=0, row=4, sticky=tk.W + tk.E, padx=5, pady=5)

		self.logOutBtn = tk.PhotoImage(file="assets/Anmelden.png")

		# Login-Button, der zur Hauptseite führt
		loginButton = tk.Button(loginFrame, image=self.logOutBtn,bg="white", command=logIn, font=LOGINFONT,  bd=0, relief=tk.FLAT, activebackground="white")
		loginButton.grid(column=0, row=5, sticky=tk.W + tk.E, padx=5, pady=30)
=======
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
                messagebox.showinfo(title="Fehler", message="Passwort oder Benutzername falsch")
                passwordEntry.delete(0, 'end')

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

        greyFrame = tk.Frame(self, height=10, background=srhGrey)
        greyFrame.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N)

        # Text im GreyFrame
        greyLabel = tk.Label(
            greyFrame,
            text="Willkommen bei DD-Inv",
            font=LARGEFONT,
            bg=srhGrey,
            fg="black",
            anchor="center"
        )
        greyLabel.pack(expand=True, fill="both")  # Text zentrieren und Frame ausfüllen

        # Konfiguriere die Spalten- und Zeilenverhältnisse so, dass sie sich dynamisch verteilen
        self.grid_columnconfigure(0, weight=1)  # Spalte 0 kann sich ausdehnen
        self.grid_rowconfigure(1, weight=1)  # Zeile 1 (wo das greyCanvas liegt) kann sich ausdehnen

        # Login-Formular mit abgerundeten Eingabefeldern
        formFrame = tk.Frame(self, bg="white")
        formFrame.place(relx=0.5, rely=0.5, anchor="center")

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
>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13
