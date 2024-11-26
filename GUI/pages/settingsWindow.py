import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


# Schriftarten / Farbschema
LARGEFONT = ("Arial", 30)
SETTINGSFONT = ("Arial", 15)
srhGrey = "#d9d9d9"
srhOrange = "#DF4807"

def popUpSettings(parent):
    popup = tk.Toplevel(parent)
    popup.title("Einstellungen")  # Titel des Fensters
    popup.geometry("960x540")  # Standardgröße des Fensters
    popup.configure(background="white")  # Hintergrundfarbe festlegen
    popup.transient(parent)  # Popup bleibt im Vordergrund des Hauptfensters
    popup.grab_set()  # Blockiere Interaktionen mit dem Hauptfenster
    popup.attributes('-topmost', True)  # Erzwinge den Fokus auf das Popup

    # Bildschirmbreite und -höhe ermitteln
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Fensterbreite und -höhe definieren
    window_width = 960  # Halb von 1920; Fensterbreite
    window_height = 540  # Halb von 1080; Fensterhöhe

    # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Setze die Fenstergöße und Position
    popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    popup.resizable(True, True)  # Fenstergöße kann verändert werden
    popup.iconbitmap("assets/srhIcon.ico")  # Icon für das Fenster

    # Konfiguriere das Grid-Layout für die Einstellungen
    popup.grid_rowconfigure(0, weight=0)  # fixiert Zeilenhöhe
    popup.grid_rowconfigure(1, weight=1)  # Dynamische Höhe für Inhalte
    popup.grid_rowconfigure(2, weight=0)
    popup.grid_rowconfigure(3, weight=0)
    popup.grid_columnconfigure(0, weight=1)  # Spalte nimmt gesamte Breite

    # Erstelle einen Header-Bereich (oben im Fenster)
    headerFrameSettings = tk.Frame(popup, height=0)
    headerFrameSettings.grid(row=1,
                             column=0,
                             sticky=tk.W + tk.E + tk.N)  # Header erstreckt sich Horizontal

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
                     sticky=tk.N + tk.W + tk.E)

    # Seitenleiste (linker Bereich)
    # srh Logo in der oberen linken Seite einfügen
    popup.srhLogo = tk.PhotoImage(file="assets/srh.png")
    sideSettings = tk.Frame(popup,
                            height=5,
                            bg="#DF4807")
    sideSettings.grid(row=0,
                      column=0,
                      rowspan=1,
                      padx=10,
                      sticky=tk.N + tk.W + tk.S)  # Seitenleiste auf der linken Seite

    # Seitenleiste für die Ausrichtung der Kategorien
    sideSettings.grid_columnconfigure(0, weight=1)

    # Kategorien in der Seitenleiste
    categories = [
        (popup.srhLogo, None),
        ("", None),
        ("System", None),
        ("Hintergrund", None),
        ("Profil(e)", None),
        ("Über", None)
    ]

    def on_category_click(label):
        # Setze alle Labels zurück
        for cat in category_labels:
            cat.config(fg="white")
        # Hervorhebung des angeklickten Labels
        label.config(fg=srhGrey)

    category_labels = []
    for idx, (text, _) in enumerate(categories):
        label = tk.Label(sideSettings,
                         text=text,
                         bd=0,
                         relief=tk.FLAT,
                         font=SETTINGSFONT,
                         fg="white",
                         bg="#DF4807")
        label.grid(padx=10, pady=8, row=idx, column=0, sticky=tk.W + tk.S)
        label.bind("<Button-1>", lambda event, lbl=label: on_category_click(lbl))
        category_labels.append(label)

    # Dynamischer Frame mit einstellungsmöglichkeiten
    middleFrame = tk.Frame(popup, padx=145, pady=100, bg="white")
    middleFrame.grid(row=1, sticky=tk.S + tk.E)

    # Radiobuttons zur Auswahl von Farben (Themes)
    storage_variable = tk.StringVar()  # Speichern der Auswahl

    # Verschiedene Optionen zum Auswählen (eine Option gleichzeitig)
    parent.option_zero = tk.PhotoImage(file="assets/DefaultBtnSettings.png")
    option_zero = ttk.Radiobutton(middleFrame,
                                  image=parent.option_zero,
                                  text="Default",
                                  variable=storage_variable,
                                  value="White")

    parent.option_one = tk.PhotoImage(file="assets/GreenBtnSettings.png")
    option_one = ttk.Radiobutton(middleFrame,
                                 image=parent.option_one,
                                 text="Grün",
                                 variable=storage_variable,
                                 value="Grün")

    parent.option_two = tk.PhotoImage(file="assets/BlueBtnSettings.png")
    option_two = ttk.Radiobutton(middleFrame,
                                 image=parent.option_two,
                                 text="Blau",
                                 variable=storage_variable,
                                 value="Blau")

    parent.option_three = tk.PhotoImage(file="assets/YellowBtnSettings.png")
    option_three = ttk.Radiobutton(middleFrame,
                                   image=parent.option_three,
                                   text="Gelb",
                                   variable=storage_variable,
                                   value="Gelb")

    parent.option_for = tk.PhotoImage(file="assets/BlackBtnSettings.png")
    option_for = ttk.Radiobutton(middleFrame,
                                 image=parent.option_for,
                                 text="Schwarz",
                                 variable=storage_variable,
                                 value="Schwarz")

    # Radiobuttons separat anordnen (in Frame)
    radio_frame = tk.Frame(middleFrame, background="#F4EFEF")
    radio_frame.grid(row=0,
                     column=0,
                     sticky=tk.E + tk.S,
                     pady=5)

    # Radiobuttons platzieren (jeder in einer eigenen Zeile innerhalb von `radio_frame`)
    option_zero.grid(row=4, column=0, padx=5, sticky=tk.E)
    option_one.grid(row=5, column=0, padx=5, sticky=tk.E)
    option_two.grid(row=6, column=0, padx=5, sticky=tk.E)
    option_three.grid(row=7, column=0, padx=5, sticky=tk.E)
    option_for.grid(row=8, column=0, padx=5, sticky=tk.E)

    # Funktion: Hintergrund ändern
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

    # Funktion: Bild auswählen
    def chose_A_Picture():
        # Öffne Dateidialog zum Auswählen eines Bildes
        parent.file_path = filedialog.askopenfilename(title="Wähle ein Bild aus... (Windows-Explorer)",  # Titel des Dialogfensters
                                                      filetypes=[("Bilddateien", "*.png;*.gif")])  # Zulässige Dateitypen
        if parent.file_path:
            # Wenn Datei ausgewählt wurde, setze Hintergrund
            set_background(parent.file_path)

    # Frame für die Funktion erstellen
    functionFrame = tk.Frame(middleFrame, bg="white")
    functionFrame.grid(row=2,  # Positioniere Frame in der dritten Zeile im Layout
                       column=1,  # Frame erstreckt sich über die zweite Spalte
                       sticky=tk.N + tk.W + tk.E + tk.S,  # Zentriert / dehnt sich aus bei Änderungen
                       pady=20)  # Vertikaler Abstand zwischen Frame und anderen Elementen

    # Konfiguriere Layout innerhalb des Frames
    functionFrame.grid_rowconfigure(0, weight=1)  # Erlaubt flexible Größe
    functionFrame.grid_columnconfigure(0, weight=1)

    # Button zum Bild auswählen
    parent.btn_chose_picature = tk.PhotoImage(file="assets/BesseresAussehenWählen.png")
    btn_chose_picature = ttk.Button(functionFrame,
                                    image=parent.btn_chose_picature,
                                    text="Besseres Aussehen auswählen....",  # Text auf dem Button
                                    command=chose_A_Picture)  # Funktion die ausgeführt wird

    # Button: Hintergrund setzen
    parent.btn_set_bg = tk.PhotoImage(file="assets/HintergrundAnwenden.png")
    btn_set_bg = ttk.Button(functionFrame,
                            image=parent.btn_set_bg,
                            text="Hintergrund anwenden",  # Text auf dem Button
                            command=lambda: set_background("Downloads/images.png"))

    # Funktionale Hauptbereiche (in fünf Zeilen unterteilt)
    headerFrameSettings.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N)
    sideSettings.grid(row=1, column=0, rowspan=2, sticky=tk.N + tk.W + tk.S)  # Seitenleiste
    btn_set_bg.grid(row=1, column=0, sticky=tk.E)
    btn_chose_picature.grid(row=2, column=0, sticky=tk.E)
    radio_frame.grid(row=3, column=0, sticky=tk.E)
