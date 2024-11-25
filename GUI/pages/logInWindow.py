import sys
import tkinter as tk
from tkinter import ttk
import Security.UserSecurity as security

LARGEFONTENTRY = ("Arial", 16)
LOGINFONTENTRY = ("Arial", 16)

LARGEFONTLABEL = ("Arial", 30)
LOGINFONTLABEL = ("Arial", 30)
srhGrey = "#d9d9d9"
srhOrange = "#DF4807"


# Funktion zum Erstellen von abgerundeten Rechtecken
def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
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
        x1, y2 - radius,
        x1, y1 + radius,
        x1 + radius, y1,
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)


# Login-Fenster (erste Seite)
class logInWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        defaultbg = self.cget('bg')
        self.configure(background="white")

        # Funktion für Login
        def logIn():
            password = passwordEntry.get().strip()
            user = usernameEntry.get().strip()
            if security.verifyUser(user, password):
                print(security.verifyUser(user, password))
                from .mainPage import mainPage
                controller.show_frame(mainPage)
            else:
                sys.exit()

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

        # Canvas für abgerundetes greyFrame
        greyCanvas = tk.Canvas(self, width=600, height=80, bg="white", highlightthickness=0)
        greyCanvas.grid(row=1, column=0, sticky=tk.N, pady=10)

        round_rectangle(greyCanvas, 10, 10, 590, 70, radius=20, fill=srhGrey)

        # Login-Label innerhalb des abgerundeten greyFrame
        greyCanvas.create_text(300, 40, text="Login into DD-Inv", font=("Arial", 20), fill="#000000")

        # Erstelle das Login-Formular im mittleren Bereich
        loginFrame = tk.Frame(self, bg="white")
        loginFrame.grid(row=1, column=0, sticky=tk.N + tk.S, pady=100)

        # Benutzername
        usernameLabel = ttk.Label(loginFrame, text="Benutzername", font=LOGINFONTLABEL, background="white")
        usernameLabel.grid(column=0, row=1, sticky=tk.W + tk.E, padx=140, pady=5)

        # Abgerundetes Eingabefeld für Benutzername
        usernameCanvas = tk.Canvas(loginFrame, width=400, height=50, bg="white", highlightthickness=0)
        usernameCanvas.grid(column=0, row=2, sticky=tk.W + tk.E, pady=10)
        round_rectangle(usernameCanvas, 5, 5, 595, 45, radius=20, fill="#f0f0f0")

        usernameEntry = tk.Entry(loginFrame, bg="#f0f0f0", font=LOGINFONTENTRY, bd=0, relief=tk.FLAT, justify="center")
        usernameCanvas.create_window(300, 25, window=usernameEntry, width=350, height=30)

        # Passwort
        passwordLabel = ttk.Label(loginFrame, text="Passwort", font=LOGINFONTLABEL, background="white")
        passwordLabel.grid(column=0, row=3, sticky=tk.W + tk.E, padx=190, pady=5)

        # Abgerundetes Eingabefeld für Passwort
        passwordCanvas = tk.Canvas(loginFrame, width=400, height=50, bg="white", highlightthickness=0)
        passwordCanvas.grid(column=0, row=4, sticky=tk.W + tk.E, pady=10)
        round_rectangle(passwordCanvas, 5, 5, 595, 45, radius=20, fill="#f0f0f0")

        passwordEntry = tk.Entry(loginFrame, bg="#f0f0f0", font=LOGINFONTENTRY, bd=0, relief=tk.FLAT, show="*", justify="center")
        passwordCanvas.create_window(300, 25, window=passwordEntry, width=350, height=30)

        self.logOutBtn = tk.PhotoImage(file="assets/Anmelden.png")

        # Login-Button, der zur Hauptseite führt
        loginButton = tk.Button(loginFrame,
                                image=self.logOutBtn,
                                bg="white",
                                command=logIn,
                                font=LOGINFONTENTRY,
                                bd=0,
                                relief=tk.FLAT,
                                activebackground="white")
        loginButton.grid(column=0, row=5, sticky=tk.W + tk.E, padx=5, pady=30)

        # Enter-Taste als Login-Trigger
        def on_enter(event):
            logIn()

        usernameEntry.bind("<Return>", on_enter)
        passwordEntry.bind("<Return>", on_enter)
