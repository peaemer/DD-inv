import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


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

    # sidesettings für die Ausrichtung der Seitenleiste
    sideSettings.grid_columnconfigure(0, weight=1)

    # Bereich für Einstellungen der sidesettings
    sideSettingsView = tk.Frame(popup)
    sideSettingsView.grid(row=1,
                          column=0,
                          sticky=tk.W + tk.E + tk.N)

    # schriftzug "System" setzen (Label einfügen)
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

    # schriftzug "Benachrichtigungen" setzen (Label einfügen)
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

    # schriftzug "Konten" setzen (Label einfügen)
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

    # schriftzug "Sprache" setzen (Label einfügen)
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
    def set_background(file_path):
        if file_path:
            # Bild laden und für Tkinter konvertieren
            bg_image = tk.PhotoImage(file=file_path)

            # Aktualisiere das Hintergrundbild im Popup
            parent.bg_label.config(image=bg_image)
            parent.bg_label.image = bg_image  # Referenz halten, damit das Bild nicht vom Speicher gelöscht wird
        else:
            # Fehlerfall, falls kein Bild geladen werden konnte
            print("Error: Could´t load or get image")

    # Funktion: Bild auswaehlen
    def chose_A_Picture():
        # oeffne Dateidialog zum auswaehlen eines Bildes
        parent.file_path = filedialog.askopenfilename(title="Wähle ein Bild aus... (Windows-Explorer)",  # Titel des Dialogfensters
                                                      filetypes=[("Bilddateien", "*.png;*.gif")])  # Zulaessige Dateitypen
        if parent.file_path:
            # Wenn datei ausgewaehlt wurde, setze Hintergrund
            set_background(parent.file_path)

    # Frame für die Funktion erstellen
    functionFrame = tk.Frame(popup, background="#F4EFEF")  #Hintergrundfarbe
    functionFrame.grid(row=2,  # Positioniere Frame in der dritten Zeile im Layout
                       column=0,  # Frame erstreckt über erste Spalte (zentral)
                       sticky=tk.N + tk.W + tk.E + tk.S,  # Zentriert / dehnt sich aus bei Aenderungen
                       pady=20)  # Vertikaler abstand zwischen Frame und anderen Elementen

    # Konfiguriere Layout inerhalb des Frames
    functionFrame.grid_rowconfigure(0, weight=1)  # Erlaubt flexible groeße
    functionFrame.grid_columnconfigure(0, weight=1)

    # Butten zum Bild auswaehlen
    btn_chose_picature = ttk.Button(functionFrame,
                                    text="Besseres Aussehen auswählen....",  # Text auf dem Button
                                    command=chose_A_Picture)  # Funktion die ausgefuehrt wird
    btn_chose_picature.grid(row=0,  # Position des Buttons (erste Zeile im Frame)
                            column=0,  # Postion des Buttons (erste Spalte im Frame)
                            padx=10,  # Abstand um den Button herum
                            pady=10)  # Abstand um den Button herum

    # Button: Hintergrund setzen
    btn_set_bg = ttk.Button(functionFrame,
                            text="Hintergrund anwenden",  # Text auf dem Button
                            command=lambda: set_background("Downloads/images.png"))
    btn_set_bg.grid(row=1,  # Position des Buttons (zweite Zeile im Frame)
                    column=0,  # Position des Buttons (erste Spalte im Frame)
                    padx=10,  # Abstand um den Button herum
                    pady=10)  # Abstand um den Button herum
