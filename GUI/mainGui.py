import tkinter as tk
from tkinter import ttk
from tkinter import *

#https://chatgpt.com/share/6746f2eb-67ac-8003-95be-480c6f1bd897

# Importiere Klassen direkt aus dem Modul pages
from pages import logInWindow,\
				   mainPage,\
				   settingsWindow, \
				   detailsWindow, \
				   adminWindow, \
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
		self.state("zoomed")

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
		self.resizable(False, False)  # Ermögliche Größenanpassung des Fensters
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
		for F in (logInWindow, mainPage, detailsWindow):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")  # Platziere die Frames im Grid
	# Verändert die Seite beim Start
		self.show_frame(logInWindow)

	# Funktion, um ein Frame (Seite) anzuzeigen
	def show_frame(self, cont):
		print(f"show_frame wird für {cont.__name__} aufgerufen")  # Debug
		frame = self.frames[cont]
		frame.tkraise()

		if hasattr(frame, 'on_load') and callable(frame.on_load):
			print(f"on_load wird für {cont.__name__} aufgerufen")  # Debug
			frame.on_load()


# Hauptanwendung starten
app = ddINV()
app.mainloop()