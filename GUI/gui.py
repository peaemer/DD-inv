import tkinter as tk
from tkinter import ttk
from tkinter import *

# Definiere die Schriftarten
LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
srhGrey = "d9d9d9"

# Hauptklasse für das Tkinter-Fenster
class ddINV(tk.Tk):
	
	# Initialisierungsfunktion für das Hauptfenster
	def __init__(self, *args, **kwargs):
		# Initialisiere die Tkinter-Basis-Klasse
		tk.Tk.__init__(self, *args, **kwargs)

		# Setze den Fenstertitel
		self.title("DD-inv")

		# Fensterbreite und -höhe definieren
		window_width = 1920
		window_height = 1080

		# Bildschirmbreite und -höhe ermitteln
		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()

		# Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
		center_x = int(screen_width / 2 - window_width / 2)
		center_y = int(screen_height / 2 - window_height / 2)

		# Setze die Fenstergröße und Position
		self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
		self.resizable(True, True)  # Ermögliche Größenanpassung des Fensters
		self.iconbitmap("assets/srhIcon.ico")  # Setze das Fenster-Icon

		# Setze das Fenster in den Vordergrund
		self.attributes('-topmost', 1)

		# Konfiguriere das Grid-Layout für das Hauptfenster
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)

		# Erstelle einen Container für die Seiten
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)

		# Konfiguriere das Grid im Container
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		# Initialisiere ein Dictionary, um die Frames (Seiten) zu speichern
		self.frames = {}

		# Erstelle die Seiten (Frames) und speichere sie im Dictionary
		for F in (logInWindow, mainPage):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")  # Platziere die Frames im Grid

		# Zeige das Login-Fenster an
		self.show_frame(logInWindow)

	# Funktion, um ein Frame (Seite) anzuzeigen
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()  # Bringt das angegebene Frame in den Vordergrund

# Login-Fenster (erste Seite)
class logInWindow(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		# Funktion für den Login-Button (Platzhalter)
		def logIn():
			print("AAAAAAAAAAAAAAA")
			if benutzername == Benutzername:
				return login()

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

		# Login-Button, der zur Hauptseite führt
		login_button = tk.Button(loginFrame, text="Anmelden",bg="#DF4807",foreground="white" , command=lambda: controller.show_frame(mainPage), font=LOGINFONT)
		login_button.grid(column=0, row=5, sticky=tk.W + tk.E, padx=5, pady=20)

# Hauptseite (zweites Fenster)
class mainPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		# Konfiguriere das Grid-Layout für die Hauptseite
		self.grid_rowconfigure(0, weight=0)
		self.grid_rowconfigure(1, weight=1)
		self.grid_rowconfigure(2, weight=1)
		self.grid_columnconfigure(0, weight=1)

		# Erstelle einen Header-Bereich
		headerFrame = tk.Frame(self, height=10, background="#DF4807")
		headerFrame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

		# Konfiguriere die Spalten für den Header
		headerFrame.grid_columnconfigure(0, weight=1)
		headerFrame.grid_columnconfigure(1, weight=0)
		headerFrame.grid_columnconfigure(2, weight=1)
		headerFrame.grid_columnconfigure(3, weight=0)
		headerFrame.grid_rowconfigure(0, weight=1)

		self.srhHead = tk.PhotoImage(file="assets/srhHeader.png")

		# Füge ein zentriertes Label hinzu
		headerLabel = tk.Label(headerFrame, image=self.srhHead, background="#DF4807", foreground="white")
		headerLabel.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N + tk.W)

		# Funktion für den Logout-Button
		def logOut():
			controller.show_frame(logInWindow)    #funktionalität hinzufügen

		# Konvertiere das Bild für Tkinter
		self.logOutBtn = tk.PhotoImage(file="assets/ausloggen.png")

		# Füge einen Button mit dem Bild hinzu
		logOutButton = tk.Button(headerFrame, image=self.logOutBtn, command=logOut, bd=0, relief=tk.FLAT, bg="#DF4807", activebackground="#DF4807")
		logOutButton.grid(row=0, column=3, sticky=tk.E, padx=20)
		
		treeFrame = tk.Frame(self, background='white')
		treeFrame.grid(row=1, column=0)

		tree = ttk.Treeview(treeFrame, column=("c1","c2","c3","c4","c5"), show="headings", height=5)

		scroll = ttk.Scrollbar(treeFrame, orient="vertical", command=tree.yview)
		scroll.grid(row=0, column=1)
		tree.configure(yscrollcommand=scroll.set)

				### listbox for directories
		tree.column("# 1", anchor=CENTER, width=50)
		tree.heading("# 1", text="ID")
		tree.column("# 2", anchor=CENTER, width=235)
		tree.heading("# 2", text="Süßi Tag")
		tree.column("# 3", anchor=CENTER, width=235)
		tree.heading("# 3", text="Typ")
		tree.column("# 4", anchor=CENTER, width=235)
		tree.heading("# 4", text="Raum")
		tree.column("# 5", anchor=CENTER, width=235)
		tree.heading("# 5", text="Name")
		tree.grid(row=0, column=0)

		dataValue = open("dataList", "r")
		dataValue = []
		for i in dataValue:
			lineList = i.split()
			dataValue.append(lineList)
		
		for i in dataValue:
			tree.insert(" ", "end", values=(i))

		


# Hauptanwendung starten
app = ddINV()
app.mainloop()