import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk


LARGEFONT = ("Arial", 30)
SETTINGSFONT = ("Arial", 30)
srhGrey = "#d9d9d9"


def popUpSettings(parent):
    popup = tk.Toplevel(parent)
    popup.title("Einstellungen")
    popup.geometry("800x600")
    popup.transient(parent)  # Popup bleibt im Vordergrund des Hauptfensters
    popup.grab_set()  # Blockiere Interaktionen mit dem Hauptfenster
    popup.attributes('-topmost', True)  # Erzwinge den Fokus auf das Popup

    # Bildschirmbreite und -höhe ermitteln
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Fensterbreite und -höhe definieren
    window_width = 960  # Halb von 1920
    window_height = 540  # Halb von 1080

    # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Setze die Fenstergröße und Position
    popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    popup.resizable(True, True)
    popup.iconbitmap("assets/srhIcon.ico")

    # Konfiguriere das Grid-Layout für die Hauptseite
    popup.grid_rowconfigure(0, weight=0)
    popup.grid_rowconfigure(1, weight=1)
    popup.grid_rowconfigure(2, weight=0)
    popup.grid_rowconfigure(3, weight=0)
    popup.grid_columnconfigure(0, weight=1)

    # Erstelle einen Header-Bereich
    headerFrame = tk.Frame(popup, height=1)
    headerFrame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

    # Konfiguriere die Spalten für den Header
    headerFrame.grid_columnconfigure(0, weight=1)
    headerFrame.grid_rowconfigure(0, weight=1)

    parent.optionsHead = tk.PhotoImage(file="assets/option.png")

    # Füge ein zentriertes Label hinzu
    headerLabel = tk.Label(headerFrame, image=parent.optionsHead, foreground="white")
    headerLabel.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.W)

    # ablegen der optionen (daher def. sich die Gruppe)
    storage_variable = tk.StringVar()

    # verschiedene optionen zum auswaehlen (eine option gleichzeitig)
    option_one = ttk.Radiobutton(parent,
                                 text="Grün",
                                 variable=storage_variable,
                                 value="Grün")

    option_two = ttk.Radiobutton(parent,
                                 text="Blau",
                                 variable=storage_variable,
                                 value="Blau")

    option_three = ttk.Radiobutton(parent,
                                   text="Gelb",
                                   variable=storage_variable,
                                   value="Gelb")

    option_for = ttk.Radiobutton(parent,
                                   text="Schwarz",
                                   variable=storage_variable,
                                   value="Schwarz")

    option_one.grid(row=-2,
                    column=0)
    option_two.grid(row=-2,
                    column=0)
    option_three.grid(row=-2, column=0)
    option_for.grid(row=-2,
                    column=0)

    def set_background(parent, file_path):
        # Bild laden und skalieren
        image = Image.open(file_path)
        resize_image = image.resize((parent.winfo_width(), parent.winfo_height()), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(resize_image)
        parent.bg_label.config(image=bg_image)
        parent.bg_label.image = bg_image

    set_background.grid()

    def choseAPicture(parent):
        # Datei-Dialog öffnen
        file_path = filedialog.askopenfilename(title="Wähle ein Bild aus...",
                                               filetypes=[("Bilddateien",
                                                           "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp")])
        if file_path:
            parent.set_background(file_path)
        else:
            print("Error: Could´t load or get image")

    choseAPicture.grind()