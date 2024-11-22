import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk


# Schriftarten / Farbschema
LARGEFONT = ("Arial", 30)
SETTINGSFONT = ("Arial", 30)
srhGrey = "#d9d9d9"


def popUpSettings(parent):
    popup = tk.Toplevel(parent)
    popup.title("Einstellungen")  # Titel des Fensters
    popup.geometry("960x540")  # Standardgroeße des Fensters
    popup.configure(background="white")  # Hintergrundfarbe festlegen
    popup.transient(parent)  # Popup bleibt im Vordergrund des Hauptfensters
    popup.grab_set()  # Blockiere Interaktionen mit dem Hauptfenster
    popup.attributes('-topmost', True)  # Erzwinge den Fokus auf das Popup

    # Bildschirmbreite und -hoehe ermitteln
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Fensterbreite und -hoehe definieren
    window_width = 960  # Halb von 1920; Fensterbreite
    window_height = 540  # Halb von 1080; Fensterhoehe

    # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Setze die Fenstergroeße und Position
    popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    popup.resizable(True, True)  # Fenstergroeße kann veraendert werden
    popup.iconbitmap("assets/srhIcon.ico")  # Icon fuer das Fenster

    # Konfiguriere das Grid-Layout fuer die Einstellungen
    popup.grid_rowconfigure(0, weight=0)  # fixiert Zeilenhoehe
    popup.grid_rowconfigure(1, weight=1)  # Dynamsche hoehe für Inhalte
    popup.grid_rowconfigure(2, weight=0)
    popup.grid_rowconfigure(3, weight=0)
    popup.grid_columnconfigure(0, weight=1)  # Spalte nimmt gesamte breite

    # Erstelle einen Header-Bereich (oben im Fenster)
    headerFrameSettings = tk.Frame(popup, height=0)
    headerFrameSettings.grid(row=0,
                             column=0,
                             sticky=tk.W + tk.E + tk.N)  # Header ersteckt sich Horizontal

    # Konfiguriere die Spalten für den Header
    headerFrameSettings.grid_columnconfigure(0, weight=1)  # Zentrierte Inhalte
    headerFrameSettings.grid_rowconfigure(0, weight=1)  # Dynamische Inhalte

    # Header-Logo laden und anzeigen
    popup.optionsHead = tk.PhotoImage(file="assets/option.png")
    headerLabel = tk.Label(headerFrameSettings,
                           image=popup.optionsHead,
                           foreground="white")
    headerLabel.grid(row=1,
                     column=0,
                     padx=10,
                     pady=10,
                     sticky=tk.N + tk.W)

    # Seitenleiste (linker Bereich)
    sideSettings = tk.Frame(popup,
                            height=5,
                            background="#F4EFEF")
    sideSettings.grid(row=2,
                      column=0,
                      sticky=tk.W + tk.E + tk.N)  # Vollbreite

    # sidesettings für die Ausrichtung der Seiteleiste
    sideSettings.grid_columnconfigure(0, weight=1)

    # Bereich für Einstellungen
    sideSettingsView = tk.Frame(popup)
    sideSettingsView.grid(row=1,
                          column=0,
                          sticky=tk.W + tk.E + tk.N)

    # schrifzug "System" setzen (Label einfügen)
    overviewStngSystem = tk.Label(sideSettingsView,
                                  text="System",
                                  bd=0,
                                  relief=tk.FLAT,
                                  font=("Arial", 15))
    overviewStngSystem.grid(padx=1,
                            pady=5,
                            row=0,
                            column=0,
                            sticky=tk.W + tk.S)

    # schrifzug "Hintergrund" setzen (Label einfügen)
    overviewStngsBackground = tk.Label(sideSettingsView,
                                       text="Hintergrund",
                                       bd=0,
                                       relief=tk.FLAT,
                                       font=("Arial", 15))
    overviewStngsBackground.grid(padx=1,
                                 pady=6,
                                 row=1,
                                 column=0,
                                 sticky=tk.W + tk.S)

    # schrifzug "Benachrichtigungen" setzen (Label einfügen)
    overviewStngsMessage = tk.Label(sideSettingsView,
                                    text="Benachrichtigungen",
                                    bd=0,
                                    relief=tk.FLAT,
                                    font=("Arial", 15))
    overviewStngsMessage.grid(padx=1,
                              pady=6,
                              row=2,
                              column=0,
                              sticky=tk.W + tk.S)

    # schrifzug "Konten" setzen (Label einfügen)
    overviewStngsProfile = tk.Label(sideSettingsView,
                                    text="Konten",
                                    bd=0,
                                    relief=tk.FLAT,
                                    font=("Arial", 15))
    overviewStngsProfile.grid(padx=1,
                              pady=6,
                              row=3,
                              column=0,
                              sticky=tk.W + tk.S)

    # schrifzug "Sprache" setzen (Label einfügen)
    overviewStngsLangue = tk.Label(sideSettingsView,
                                   text="Sprache",
                                   bd=0,
                                   relief=tk.FLAT,
                                   font=("Arial", 15))
    overviewStngsLangue.grid(padx=1,
                             pady=6,
                             row=4,
                             column=0,
                             sticky=tk.W + tk.S)

    # Radiobuttons zur auswahl von Farben (Themes)
    storage_variable = tk.StringVar()  # speichern der Auswahl

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

    # Radiobuttons platzieren
    option_zero.grid()
    option_one.grid()
    option_two.grid()
    option_three.grid()
    option_for.grid()

    # Funktion: Hintergrund aendern
    def set_background(popup, file_path):
        # Bild laden und Popup-Groeße skalieren
        image = Image.open(file_path)
        resize_image = image.resize((popup.winfo_width(), popup.winfo_height()), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(resize_image)
        popup.bg_label.config(image=bg_image)  # Hintergrund ändern
        popup.bg_label.image = bg_image
        set_background.grid(popup,
                            row=2)

    # Funktion: Bild auswaehlen
    def chose_A_Picture(popup):
        # Datei-Dialog oeffnen fuer Bildauswahl
        file_path = filedialog.askopenfilename(title="Wähle ein Bild aus...",
                                               filetypes=[("Bilddateien",
                                                           "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp")])
        if file_path:
            popup.set_background(file_path)  # Hintergrund setzen
        else:
            print("Error: Could´t load or get image")
    chose_A_Picture.grid(popup,
                         row=2)
