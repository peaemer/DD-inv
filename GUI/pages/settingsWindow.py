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
    popup.geometry("960x540")
    popup.transient(parent)  # Popup bleibt im Vordergrund des Hauptfensters
    popup.grab_set()  # Blockiere Interaktionen mit dem Hauptfenster
    popup.attributes('-topmost', True)  # Erzwinge den Fokus auf das Popup

    # Bildschirmbreite und -hoehe ermitteln
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Fensterbreite und -hoehe definieren
    window_width = 960  # Halb von 1920
    window_height = 540  # Halb von 1080

    # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Setze die Fenstergroeße und Position
    popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    popup.resizable(True, True)
    popup.iconbitmap("assets/srhIcon.ico")

    # Konfiguriere das Grid-Layout fuer die Einstellungen
    popup.grid_rowconfigure(0, weight=0)
    popup.grid_rowconfigure(1, weight=1)
    popup.grid_rowconfigure(2, weight=0)
    popup.grid_rowconfigure(3, weight=0)
    popup.grid_columnconfigure(0, weight=1)

    # Erstelle einen Header-Bereich
    headerFrameSettings = tk.Frame(popup, height=0)
    headerFrameSettings.grid(row=0,
                             column=0,
                             sticky=tk.W + tk.E + tk.N)

    # Konfiguriere die Spalten für den Header
    headerFrameSettings.grid_columnconfigure(0, weight=1)
    headerFrameSettings.grid_rowconfigure(0, weight=1)

    popup.optionsHead = tk.PhotoImage(file="assets/option.png")

    # Füge ein zentriertes Label hinzu
    headerLabel = tk.Label(headerFrameSettings,
                           image=popup.optionsHead,
                           foreground="white")
    headerLabel.grid(row=1,
                     column=0,
                     padx=10,
                     pady=10,
                     sticky=tk.N + tk.W)

    sideSettings = tk.Frame(popup,
                            height=5,
                            background="#F4EFEF")
    sideSettings.grid(row=2,
                      column=0,
                      sticky=tk.W + tk.E + tk.N)

    # Konfiguriere die sideSettings für zentrierte Ausrichtung
    sideSettings.grid_columnconfigure(0, weight=1)

    sideSettingsView = tk.Frame(popup)
    sideSettingsView.grid(row=1,
                          column=0,
                          sticky=tk.W + tk.E + tk.N)

    # schrifzug "System" setzen
    overviewStngSystem = tk.Label(sideSettingsView,
                                 text="System",
                                 bd=0,
                                 relief=tk.FLAT,
                                 font=("Arial", 15))
    overviewStngSystem.grid(padx=1,
                           pady=5,
                           row=1,
                           column=0,
                           sticky=tk.W + tk.E)

    # schrifzug "Hintergrund" setzen
    overviewStngsBackground = tk.Label(sideSettingsView,
                                       text="Hintergrund",
                                       bd=0,
                                       relief=tk.FLAT,
                                       font=("Arial", 15))
    overviewStngsBackground.grid(padx=1,
                                 pady=6,
                                 row=1,
                                 column=0,
                                 sticky=tk.W + tk.E)


    # ablegen der nachfolgenden optionen (daher def. sich die Gruppe)
    storage_variable = tk.StringVar()

    # verschiedene optionen zum auswaehlen (eine option gleichzeitig)
    option_zero = ttk.Radiobutton(popup,
                                 text="Deafault",
                                 variable=storage_variable,
                                 value="White")

    option_one = ttk.Radiobutton(popup,
                                 text="Grün",
                                 variable=storage_variable,
                                 value="Grün")

    option_two = ttk.Radiobutton(popup,
                                 text="Blau",
                                 variable=storage_variable,
                                 value="Blau")

    option_three = ttk.Radiobutton(popup,
                                   text="Gelb",
                                   variable=storage_variable,
                                   value="Gelb")

    option_for = ttk.Radiobutton(popup,
                                   text="Schwarz",
                                   variable=storage_variable,
                                   value="Schwarz")

    option_zero.grid()
    option_one.grid()
    option_two.grid()
    option_three.grid()
    option_for.grid()

    def set_background(popup, file_path):
        # Bild laden und skalieren
        image = Image.open(file_path)
        resize_image = image.resize((popup.winfo_width(), popup.winfo_height()), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(resize_image)
        popup.bg_label.config(image=bg_image)
        popup.bg_label.image = bg_image
        set_background.grid(popup,
                            row=2)

    def chose_A_Picture(popup):
        # Datei-Dialog öffnen
        file_path = filedialog.askopenfilename(title="Wähle ein Bild aus...",
                                               filetypes=[("Bilddateien",
                                                           "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp")])
        if file_path:
            popup.set_background(file_path)
        else:
            print("Error: Could´t load or get image")
    chose_A_Picture.grid(popup,
                         row=2)