import sys
import tkinter as tk
from tkinter import ttk

LARGEFONT = ("Arial", 30)
LOGINFONT = ("Arial", 30)
srhGrey = "#d9d9d9"
srhOrange = "#DF4807"

# Funktion zum Zeichnen eines Rechtecks mit abgerundeten Ecken
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
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1 + radius, y1,
        x1 + radius, y1
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)


# Login-Fenster (erste Seite)
class logInWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(background="white")

        def logIn():
            password = passwordEntry.get().strip()
            user = usernameEntry.get().strip()
            import Security.UserSecurity as security
            if security.verifyUser(user, password):
                from .mainPage import mainPage
                controller.show_frame(mainPage)
            else:
                sys.exit()

        # Funktion, um Login durch Enter-Taste zu bestätigen
        def on_enter(event):
            logIn()

        # Konfiguriere das Grid-Layout für die Login-Seite
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        headerFrame = tk.Frame(self, height=10, background="#DF4807")
        headerFrame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

        self.srhHead = tk.PhotoImage(file="assets/srhHeader.png")
        srhHeader = tk.Label(headerFrame, image=self.srhHead, bd=0, bg="#DF4807")
        srhHeader.grid(padx=20, pady=10, row=0, column=0, sticky=tk.W + tk.N)

        # GreyFrame
        greyCanvas = tk.Canvas(self, bg="white", highlightthickness=0)
        greyCanvas.grid(row=1, column=0, sticky="nsew")
        round_rectangle(greyCanvas, 0, 0, self.winfo_screenwidth() - 20, 70, radius=30, fill=srhGrey)

        greyCanvas.create_text(
            self.winfo_screenwidth() // 2,
            40,
            text="Loggin into DD-Inv",
            font=("Arial", 20),
            fill="black",
        )

        # Login-Formular mit abgerundeten Ecken
        loginCanvas = tk.Canvas(self, width=500, height=400, bg="white", highlightthickness=0)
        loginCanvas.grid(row=1, column=0, pady=70, sticky="nsew")
        round_rectangle(loginCanvas, 0, 0, 500, 400, radius=30, fill="white")

        # Platz für Username und Passwort
        formFrame = tk.Frame(loginCanvas, bg="white")
        formFrame.place(relx=0.5, rely=0.5, anchor="center")

        # Username
        usernameLabel = ttk.Label(formFrame, text="Benutzername", font=LOGINFONT, background="white")
        usernameLabel.grid(column=0, row=0, pady=10, sticky="ew")

        # Eingabefeld Benutzername mit abgerundeten Ecken
        usernameCanvas = tk.Canvas(formFrame, width=350, height=50, bg="white", highlightthickness=0)
        usernameCanvas.grid(column=0, row=1, pady=10)
        round_rectangle(usernameCanvas, 5, 5, 345, 45, radius=20, fill="#f0f0f0")
        usernameEntry = tk.Entry(formFrame, font=LOGINFONT, bg="#f0f0f0", relief=tk.FLAT, justify="center")
        usernameCanvas.create_window(175, 25, window=usernameEntry, width=340, height=30)

        # Passwort
        passwordLabel = ttk.Label(formFrame, text="Passwort", font=LOGINFONT, background="white")
        passwordLabel.grid(column=0, row=2, pady=10, padx=65, sticky="ew")

        # Eingabefeld Passwort mit abgerundeten Ecken
        passwordCanvas = tk.Canvas(formFrame, width=350, height=50, bg="white", highlightthickness=0)
        passwordCanvas.grid(column=0, row=3, pady=10)
        round_rectangle(passwordCanvas, 5, 5, 345, 45, radius=20, fill="#f0f0f0")
        passwordEntry = tk.Entry(formFrame, show="*", font=LOGINFONT, bg="#f0f0f0", relief=tk.FLAT, justify="center")
        passwordCanvas.create_window(175, 25, window=passwordEntry, width=340, height=30)

        # Login-Button
        self.logOutBtn = tk.PhotoImage(file="assets/Anmelden.png")
        loginButton = tk.Button(formFrame, image=self.logOutBtn, bg="white", command=logIn, bd=0, relief=tk.FLAT,
                                activebackground="white")
        loginButton.grid(column=0, row=4, pady=20, sticky="ew")

        # Hinzufügen der Bindungen nach der Erzeugung der Eingabefelder**
        self.usernameEntry = usernameEntry
        self.passwordEntry = passwordEntry

        # Die Enter-Taste binden, um den Login zu bestätigen
        self.usernameEntry.bind("<Return>", on_enter)
        self.passwordEntry.bind("<Return>", on_enter)