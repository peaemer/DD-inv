import tkinter as tk
from tkinter import ttk
from tkinter import *

# Importiere Klassen direkt aus dem Modul pages
from pages import logInWindow,\
				   mainPage,\
				   settingsWindow, \
			       _DPIAwareness

# Hauptklasse für das Tkinter-Fenster
class ddINV(tk.Tk):

	# Initialisierungsfunktion für das Hauptfenster
	def __init__(self, *args, **kwargs):
		# Initialisiere die Tkinter-Basis-Klasse
		tk.Tk.__init__(self, *args, **kwargs)

		# Setze den Fenstertitel
		self.title("Inventartool")
		self.configure(background="white")

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
		self.show_frame(mainPage)

	# Funktion, um ein Frame (Seite) anzuzeigen
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()  # Bringt das angegebene Frame in den Vordergrund



# Hauptanwendung starten
app = ddINV()
app.mainloop()