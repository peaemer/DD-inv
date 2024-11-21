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

    parent.srhHead2 = tk.PhotoImage(file="assets/srh.png")

    # Füge ein zentriertes Label hinzu
    headerLabel = tk.Label(headerFrame, image=parent.srhHead2, background="#DF4807", foreground="white")
    headerLabel.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N + tk.W)

    # chekbox zum anhacken / abhacken
    chek_button = ttk.Checkbutton(parent,
                                  text="Click me for more actions")
    chek_button.pack()

    # auswaehlen was bei verschiedenen optionen passieren soll
    selected_option = tk.StringVar()

    # def der optionen
    def print_current_option():
        print(selected_option.get())

    check = ttk.Checkbutton(parent,
                            text="Nothing happens in the upper checkbox",
                            variable=selected_option,
                            command=print_current_option,
                            onvalue="no action avabiale",
                            offvalue="i gott u xD")
    check.pack()

    # Hintergrund-Label
    parent.bg_label = tk.Label(parent)
    parent.bg_label.place(relwidth=1,
                          relheight=1)

    # Button zum Bildauswählen
    parent.select_button = tk.Button(parent,
                                     text="Wähle ein besseres Bild aus, als diesen Hintergrund zu verwenden...",
                                     command=parent.choseAPicture)
    parent.select_button.pack(pady=20)

    def set_background(parent, file_path):
        # Bild laden und skalieren
        image = Image.open(file_path)
        resize_image = image.resize((parent.winfo_width(), parent.winfo_height()), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(resize_image)
        parent.bg_label.config(image=bg_image)
        parent.bg_label.image = bg_image

    def choseAPicture(parent):
        # Datei-Dialog öffnen
        file_path = filedialog.askopenfilename(title="Wähle ein Bild aus...",
                                               filetypes=[("Bilddateien",
                                                           "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp")])
        if file_path:
            parent.set_background(file_path)
        else:
            print("Error: Could´t load or get image")
