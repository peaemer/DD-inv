import tkinter as tk

import cache
from GUI.pages import adminUserWindow
#https://chatgpt.com/share/6746f2eb-67ac-8003-95be-480c6f1bd897

# Importiere Klassen direkt aus dem Modul pages
from pages import logInWindow,\
				  mainPage,\
				  userDetailsWindow,\
				  detailsWindow,\
				  adminRoomWindow,\
				  adminUserWindow,\
			      _DPIAwareness


# Hauptklasse für das Tkinter-Fenster
class ddINV(tk.Tk):
	"""
	The ddINV class represents the main application window for an inventory tool.

	This class is responsible for initializing and configuring the main window
	of the inventory tool application. It sets up the application window with
	a specified title, size, and position on the screen. Additionally, it manages
	the frames (or pages) within the window, allowing for navigation between
	different sections of the application.

	:ivar frames: A dictionary that stores the different frames/pages within the
	              application, keyed by frame class.
	:type frames: dict
	"""
	# Initialisierungsfunktion für das Hauptfenster
	def __init__(self, *args, **kwargs):
		# Initialisiere die Tkinter-Basis-Klasse
		tk.Tk.__init__(self, *args, **kwargs)

		# Setze den Fenstertitel
		self.title("Inventartool")
		self.configure(background="white")
		self.state("zoomed")

		# Setze die Fenstergröße und Position
		width, height = self.winfo_screenwidth(), self.winfo_screenheight()
		self.geometry('%dx%d+0+0' % (width, height))
		self.tk.call('tk', 'scaling', 1.2)  # Vergroessert / verkleinert den Inhalt innerhalb des Fensters
		self.resizable(True, True)  # Ermögliche Größenanpassung des Fensters
		self.iconbitmap("assets/srhIcon.ico")  # Setze das Fenster-Icon

		# Setze das Fenster in den Vordergrund
		self.attributes('-topmost', 0)

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
		for F in (logInWindow, mainPage,detailsWindow , userDetailsWindow, adminRoomWindow, adminUserWindow):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")  # Platziere die Frames im Grid
	# Verändert die Seite beim Start
		cache.user_name = 'Alex'
		self.show_frame(mainPage)


	# Funktion, um ein Frame (Seite) anzuzeigen
	def show_frame(self, cont):
		print(f"show_frame wird für {cont.__name__} aufgerufen")  # Debug
		frame = self.frames[cont]
		if isinstance(frame, tk.Frame):
			frame.tkraise()

			if hasattr(frame, 'on_load') and callable(frame.on_load):
				print(f"on_load wird für {cont.__name__} aufgerufen")  # Debug
				frame.on_load()


if __name__ == "__main__":
    app = ddINV()
    app.mainloop()