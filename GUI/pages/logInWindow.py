import tkinter as tk
from tkinter import ttk
from tkinter import *



LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 35)
srhGrey = "#d9d9d9"

# Login-Fenster (erste Seite)
class logInWindow(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		defaultbg = self.cget('bg')


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
		loginFrame = tk.Frame(self)
		loginFrame.grid(row=1, column=0, sticky=tk.N + tk.S, pady=100)

		# Füge die Eingabefelder für Username und Passwort hinzu
		username_label = ttk.Label(loginFrame, text="Benutzername", font=LOGINFONT)
		username_label.grid(column=0, row=1, sticky=tk.W + tk.E, padx=130, pady=5)

		username_entry = tk.Entry(loginFrame, font=LOGINFONT)
		username_entry.grid(column=0, row=2, sticky=tk.W + tk.E, padx=5, pady=5)

		password_label = ttk.Label(loginFrame, text="Passwort", font=LOGINFONT)
		password_label.grid(column=0, row=3, sticky=tk.W + tk.E, padx=190, pady=5)

		password_entry = tk.Entry(loginFrame, show="*", font=LOGINFONT)
		password_entry.grid(column=0, row=4, sticky=tk.W + tk.E, padx=5, pady=5)

		self.logOutBtn = tk.PhotoImage(file="assets/Anmelden.png")

		# Login-Button, der zur Hauptseite führt
		login_button = tk.Button(loginFrame, image=self.logOutBtn,bg=defaultbg, command=logIn, font=LOGINFONT,  bd=0, relief=tk.FLAT, activebackground=defaultbg)
		login_button.grid(column=0, row=5, sticky=tk.W + tk.E, padx=5, pady=30)
