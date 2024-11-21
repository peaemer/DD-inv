import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter  # Library kann mit "pip install customtkinter" geladen werden
import customtkinter as ttk

LARGEFONT = ("Arial", 30)
SETTINGSFONT = ("Arial", 30)
srhGrey = "#d9d9d9"

class SettingsWindow(ttk.CTkFrame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")

        # Hintergrund-Label
        self.bg_label = tk.Label(self)
        self.bg_label.place(relwidth=1, relheight=1)

        # Button zum Bildauswählen
        self.select_button = tk.Button(self, text="Wähle ein besseres Bild aus, als diesen Hintergrund zu verwenden...",
                                       command=self.choseAPicture)
        self.select_button.pack(pady=20)

    def popUpSettings(self):
        popup = tk.Toplevel(self)
        popup.title("Einstellungen")
        popup.geometry("800x600")

        # Konfiguriere das Grid-Layout für die Hauptseite
        popup.grid_rowconfigure(0, weight=0)
        popup.grid_rowconfigure(1, weight=1)
        popup.grid_rowconfigure(2, weight=0)
        popup.grid_rowconfigure(3, weight=0)
        popup.grid_columnconfigure(0, weight=1)

        # Erstelle einen Header-Bereich
        headerFrame = tk.Frame(popup, height=10, background="#DF4807")
        headerFrame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

        # Konfiguriere die Spalten für den Header
        headerFrame.grid_columnconfigure(0, weight=1)
        headerFrame.grid_rowconfigure(0, weight=1)

        self.srhHead = tk.PhotoImage(file="assets/srh.png")

        # Füge ein zentriertes Label hinzu
        headerLabel = tk.Label(headerFrame, image=self.srhHead, background="#DF4807", foreground="white")
        headerLabel.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N + tk.W)

    def btnDarkmode(self):
        # Button Darkmode erstellen
        btn_switch = tk.StringVar(value="on")

        def change_theme():
            pass  # Darkmode-Logik hier hinzufügen

        # Erstellen und definieren des Switches
        darkmode_switch = customtkinter.CTkSwitch(text="Light-/Darkmode",
                                                  command=change_theme,
                                                  variable=btn_switch,
                                                  onvalue="on",
                                                  offvalue="off")
        darkmode_switch.pack()

    def set_background(self, file_path):
        # Bild laden und skalieren
        image = Image.open(file_path)
        resize_image = image.resize((self.winfo_width(), self.winfo_height()), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(resize_image)
        self.bg_label.config(image=bg_image)
        self.bg_label.image = bg_image

    def chose_A_Picture(self):
        # Datei-Dialog öffnen
        file_path = filedialog.askopenfilename(title="Wähle ein Bild aus...",
                                               filetypes=[("Bilddateien", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp")])
        if file_path:
            self.set_background(file_path)
        else:
            print("Error: Could´t load or get image")
