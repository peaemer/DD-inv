import tkinter as tk
from tkinter import ttk

from GUI.pages import adminUserWindow, roomDetailsWindow
#https://chatgpt.com/share/6746f2eb-67ac-8003-95be-480c6f1bd897

# Importiere Klassen direkt aus dem Modul pages
from pages import logInWindow,\
				  mainPage,\
				  userDetailsWindow,\
				  detailsWindow,\
				  roomDetailsWindow,\
				  adminRoomWindow,\
				  adminUserWindow,\
				  adminRoleWindow,\
			      _DPIAwareness
import customtkinter as ctk


# Hauptklasse für das Tkinter-Fenster
class ddINV(tk.Tk):
	"""
	Zusammenfassung der Klasse ddINV.

	Die Klasse ddINV ist eine erweiterte Tkinter-Anwendung, die ein Hauptfenster zur Verwaltung eines
	Inventarisierungstools bereitstellt. Sie verarbeitet das Layout, die Fensterkonfiguration und
	die Navigation zwischen verschiedenen Seiten (Frames), die in das Hauptfenster geladen werden.
	Sie dient als zentraler Einstiegspunkt für die Benutzeroberfläche des Tools.

	:ivar frames: Ein Dictionary, das die verschiedenen Frames (Seiten) der Anwendung speichert.
	              Die Schlüssel sind die Frame-Klassen, und die Werte sind die Instanzen dieser Klassen.
	:type frames: dict
	"""
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
		self.minsize(1280, 720)
		self.maxsize(1920,1080)
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
		for F in (logInWindow, mainPage,detailsWindow , userDetailsWindow, adminRoomWindow,adminRoleWindow, adminUserWindow, roomDetailsWindow):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")  # Platziere die Frames im Grid
	# Verändert die Seite beim Start
		self.show_frame(logInWindow)


	# Funktion, um ein Frame (Seite) anzuzeigen
	def show_frame(self, cont):
		"""
		Zeigt einen bestimmten Frame an, hebt ihn in der Stapelreihenfolge hervor und ruft optional
		die Methode `on_load` auf, falls sie im Frame definiert ist.

		:param cont: Die Klasse des Frames, der angezeigt werden soll.
		:type cont: Typ der Frame-Klasse
		:return: Keine Rückgabe.
		"""
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