import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


# Schriftarten / Farbschema
LARGEFONT = ("Arial", 30)
SETTINGSFONT = ("Arial", 15)
srhGrey = "#d9d9d9"
srhOrange = "#DF4807"


##############################
# # H A U P T L A Y O U T # #
##############################

# Funktion erstellt Popupfenster "Einstellungen"
def popUpSettings(parent):
    # erstellt ein neues Fenster
    popup = tk.Toplevel(parent)
    popup.title("Einstellungen")
    popup.geometry("960x540")  # groeße des Fensters
    popup.configure(background="white")  # Hintergrundfarbe
    popup.transient(parent)  # Setzt Hauptfenster in Hintergrund
    popup.grab_set()  # Fokus auf Popup
    popup.attributes('-topmost', True)  # Fenster immer im Vordergrund

    # Bildschirmbreite und hoehe ermitteln (fenster mittig auf Bildschirm setzten)
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    window_width, window_height = 960, 540
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    popup.resizable(True, True)  # Fenstergroeße anpassbar
    popup.iconbitmap("assets/srhIcon.ico")  # Fenster-Icon

    # Grid-Layout für Popup konfigurieren (danymische groeße)
    popup.grid_rowconfigure(0, weight=1)  # Bereich fuer Kategorien
    popup.grid_rowconfigure(1, weight=10)  # Hauptbereich
    popup.grid_columnconfigure(0, weight=0)  # Seitenleiste
    popup.grid_columnconfigure(1, weight=1)  # Hauptinhalt

    # Erstelle Header-Bereich (oben im Fenster)
    headerFrameSettings = tk.Frame(popup, height=0)
    headerFrameSettings.grid(row=0,
                             column=1,
                             sticky=tk.W + tk.E + tk.N)  # Header erstreckt sich Horizontal,

    # Konfiguriere die Spalten für den Header
    headerFrameSettings.grid_columnconfigure(0, weight=1)
    headerFrameSettings.grid_rowconfigure(0, weight=1)

    # Header-Logo laden und anzeigen
    popup.optionsHead = tk.PhotoImage(file="assets/Tool.png")
    headerLabel = tk.Label(headerFrameSettings,
                           image=popup.optionsHead,
                           foreground="white")
    headerLabel.grid(row=1,
                     column=0,
                     padx=10,
                     pady=10,
                     sticky=tk.N + tk.W + tk.E)

    # Seitenleiste
    sideSettings = tk.Frame(popup, width=200, bg=srhOrange)
    sideSettings.grid(row=0, column=0, rowspan=2, sticky="nesw")
    sideSettings.grid_columnconfigure(0, weight=1)

    # SRH Logo in der Seitenleiste
    popup.srhLogo = tk.PhotoImage(file="assets/srh.png")
    srhLogoLabel = tk.Label(sideSettings, image=popup.srhLogo, bg=srhOrange)
    srhLogoLabel.grid(row=0, column=0, padx=10, pady=10, sticky="n")

    # Kategorien in der Seitenleiste
    categories = ["System",
                  "Style",
                  "Profil",
                  "Über DD-Inv"]

    def on_category_click(label):
        # Setze alle Labels zurück
        for cat in category_labels:
            cat.config(fg="white")
        # Hervorhebung des angeklickten Labels
        label.config(fg="Black")

    category_labels = []
    for idx, text in enumerate(categories):
        label = tk.Label(
            sideSettings,
            text=text,
            bd=0,
            relief=tk.FLAT,
            font=SETTINGSFONT,
            fg="white",
            bg=srhOrange,
        )
        label.grid(padx=10, pady=8, row=idx + 1, column=0, sticky="w")
        label.bind("<Button-1>", lambda event, lbl=label: on_category_click(lbl))
        category_labels.append(label)

    def on_category_click(label):
        for cat in category_labels:
            cat.config(fg="white")
        label.config(fg="Black")

    category_labels = []
    # Dynamische Frames erstellen
    FrameSystem = tk.Frame(popup, padx=10, pady=30, bg="white")
    FrameStyle = tk.Frame(popup, padx=10, pady=30, bg="white")
    FrameProfile = tk.Frame(popup, padx=10, pady=30, bg="white")
    FrameUeber = tk.Frame(popup, padx=10, pady=30, bg="white")

    # Zuordnung der Frames zu den Kategorien
    frames = {"System": FrameSystem,
              "Style": FrameStyle,
              "Profil": FrameProfile,
              "Über DD-Inv": FrameUeber}

    current_frame = None

    def show_frame(categories):
        new_frame = frames.get(categories)
        global current_frame
        if new_frame:
            new_frame.grid(row=1, column=1, rowspan=2, sticky="nw")
            current_frame = new_frame
        else:
            current_frame.grid_forget()

    # Kategorie-Event-Bindung
    for idx, text in enumerate(categories):
        label = tk.Label(
            sideSettings,
            text=text,
            bd=0,
            relief=tk.FLAT,
            font=SETTINGSFONT,
            fg="white",
            bg=srhOrange,
        )
        label.grid(padx=10, pady=8, row=idx + 1, column=0, sticky="w")
        label.bind("<Button-1>", lambda event, lbl=text: (on_category_click(label), show_frame(lbl)))
        category_labels.append(label)

    # Standard-Frame anzeigen
    show_frame("System")
    show_frame("Style")
    show_frame("Profile")
    show_frame("Ueber")

    #################################
    # # L A Y O U T : S Y S T E M # #
    #################################


    # Dynamischer Frame mit Einstellungsmöglichkeiten
    FrameSystem = tk.Frame(popup, padx=100, pady=30, bg="white")
    FrameSystem.grid(row=1, column=1, rowspan=2, sticky="nw")

    # Überschrift für Radiobutton-Kategorie
    radiobutton_label = tk.Label(
        FrameSystem, text="Über das DD-Inv Tool", font=SETTINGSFONT, bg="white"
    )
    radiobutton_label.grid(row=0, column=0, pady=10, sticky="nw")

    # Radiobuttons zur Auswahl von Farben (Themes)
    storage_variable = tk.StringVar(value="White")

    parent.option_zero = tk.PhotoImage(file="assets/DefaultBtnSettings.png")
    parent.option_one = tk.PhotoImage(file="assets/GreenBtnSettings.png")
    parent.option_two = tk.PhotoImage(file="assets/BlueBtnSettings.png")
    parent.option_three = tk.PhotoImage(file="assets/YellowBtnSettings.png")
    parent.option_for = tk.PhotoImage(file="assets/BlackBtnSettings.png")

    radio_buttons = [
        ("Standard", parent.option_zero, "White"),
        ("Grün", parent.option_one, "Green"),
        ("Blau", parent.option_two, "Blue"),
        ("Gelb", parent.option_three, "Yellow"),
        ("Schwarz", parent.option_for, "Black"),
    ]

    # Überschrift für Backgroundbutton-Kategorie
    button_bg_label = tk.Label(
        FrameSystem, text="Feedback", font=SETTINGSFONT, bg="white"
    )
    button_bg_label.grid(row=6, column=0, pady=10, sticky="nw")

    def change_app_background(color):
        parent.configure(bg=color)
        popup.configure(bg=color)

    for idx, (text, image, value) in enumerate(radio_buttons):
        ttk.Radiobutton(
            FrameSystem,
            image=image,
            text=text,
            variable=storage_variable,
            value=value,
            style="Custom.TRadiobutton",
            command=lambda color=value: change_app_background(color),
        ).grid(row=idx + 1, column=0, pady=5)

    # Hintergrundbild-Auswahl
    def apply_selected_image():
        file_path = filedialog.askopenfilename(
            title="Wähle ein Bild aus...",
            filetypes=[("Bilddateien", "*.png;*.jpg;*.jpeg")])

        if file_path:
            bg_image = tk.PhotoImage(file=file_path)
            parent.bg_label = tk.Label(parent, image=bg_image)
            parent.bg_label.image = bg_image
            parent.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

    btn_chose_picture = ttk.Button(
        FrameSystem,
        text="Besseres Aussehen auswählen...",
        style="Custom.TButton",
        command=apply_selected_image,
    )
    btn_chose_picture.grid(row=len(radio_buttons) + 2, column=0, pady=10)

    def set_default_background():
        parent.configure(bg="white")
        popup.configure(bg="white")
        if hasattr(parent, "bg_label"):
            parent.bg_label.destroy()

    btn_set_bg = ttk.Button(
        FrameSystem,
        text="Hintergrund zurücksetzen",
        style="Custom.TButton",
        command=set_default_background,
    )
    btn_set_bg.grid(row=len(radio_buttons) + 3, column=0, pady=10)

    # Style anpassen
    style = ttk.Style()
    style.configure("Custom.TButton", background="white", font=SETTINGSFONT)
    style.configure("Custom.TRadiobutton", background="white", font=SETTINGSFONT)


    ################################
    # # L A Y O U T : S T I E L # #
    ################################


    # Dynamischer Frame mit Einstellungsmöglichkeiten
    FrameStyle = tk.Frame(popup, padx=100, pady=30, bg="white")
    FrameStyle.grid(row=1, column=1, rowspan=2, sticky="nw")

    #erstellen der Funktion anzeigen je nach gedrückter Kategorie


    # Überschrift für Radiobutton-Kategorie
    radiobutton_label = tk.Label(
        FrameStyle, text="Setze einen vordefinierten Style", font=SETTINGSFONT, bg="white"
    )
    radiobutton_label.grid(row=0, column=0, pady=10, sticky="nw")

    # Radiobuttons zur Auswahl von Farben (Themes)
    storage_variable = tk.StringVar(value="White")

    parent.option_zero = tk.PhotoImage(file="assets/DefaultBtnSettings.png")
    parent.option_one = tk.PhotoImage(file="assets/GreenBtnSettings.png")
    parent.option_two = tk.PhotoImage(file="assets/BlueBtnSettings.png")
    parent.option_three = tk.PhotoImage(file="assets/YellowBtnSettings.png")
    parent.option_for = tk.PhotoImage(file="assets/BlackBtnSettings.png")

    radio_buttons = [
        ("Standard", parent.option_zero, "White"),
        ("Grün", parent.option_one, "Green"),
        ("Blau", parent.option_two, "Blue"),
        ("Gelb", parent.option_three, "Yellow"),
        ("Schwarz", parent.option_for, "Black"),
    ]

    # Überschrift für Backgroundbutton-Kategorie
    button_bg_label = tk.Label(
        FrameStyle, text="Wähle aus einem Eigenem Bild", font=SETTINGSFONT, bg="white"
    )
    button_bg_label.grid(row=6, column=0, pady=10, sticky="nw")

    def change_app_background(color):
        parent.configure(bg=color)
        popup.configure(bg=color)

    for idx, (text, image, value) in enumerate(radio_buttons):
        ttk.Radiobutton(
            FrameStyle,
            image=image,
            text=text,
            variable=storage_variable,
            value=value,
            style="Custom.TRadiobutton",
            command=lambda color=value: change_app_background(color),
        ).grid(row=idx + 1, column=0, pady=5)

    # Hintergrundbild-Auswahl
    def apply_selected_image():
        file_path = filedialog.askopenfilename(
            title="Wähle ein Bild aus...",
            filetypes=[("Bilddateien", "*.png;*.jpg;*.jpeg")])

        if file_path:
            bg_image = tk.PhotoImage(file=file_path)
            parent.bg_label = tk.Label(parent, image=bg_image)
            parent.bg_label.image = bg_image
            parent.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

    btn_chose_picture = ttk.Button(
        FrameStyle,
        text="Besseres Aussehen auswählen...",
        style="Custom.TButton",
        command=apply_selected_image,
    )
    btn_chose_picture.grid(row=len(radio_buttons) + 2, column=0, pady=10)

    def set_default_background():
        parent.configure(bg="white")
        popup.configure(bg="white")
        if hasattr(parent, "bg_label"):
            parent.bg_label.destroy()

    btn_set_bg = ttk.Button(
        FrameStyle,
        text="Hintergrund zurücksetzen",
        style="Custom.TButton",
        command=set_default_background,
    )
    btn_set_bg.grid(row=len(radio_buttons) + 3, column=0, pady=10)

    # Style anpassen
    style = ttk.Style()
    style.configure("Custom.TButton", background="white", font=SETTINGSFONT)
    style.configure("Custom.TRadiobutton", background="white", font=SETTINGSFONT)


    ###################################
    # # L A Y O U T : P R O F I L E # #
    ###################################


    # Dynamischer Frame mit Einstellungsmöglichkeiten
    FrameProfile = tk.Frame(popup, padx=100, pady=30, bg="white")
    FrameProfile.grid(row=1, column=1, rowspan=2, sticky="nw")

    # Überschrift für Radiobutton-Kategorie
    radiobutton_label = tk.Label(
        FrameProfile, text="Passe dein Profil an", font=SETTINGSFONT, bg="white"
    )
    radiobutton_label.grid(row=0, column=0, pady=10, sticky="nw")

    def set_default_background():
        parent.configure(bg="white")
        popup.configure(bg="white")
        if hasattr(parent, "bg_label"):
            parent.bg_label.destroy()

    btn_set_bg = ttk.Button(
        FrameProfile,
        text="Hintergrund zurücksetzen",
        style="Custom.TButton",
        command=set_default_background,
    )
    btn_set_bg.grid(row=len(radio_buttons) + 3, column=0, pady=10)

    # Style anpassen
    style = ttk.Style()
    style.configure("Custom.TButton", background="white", font=SETTINGSFONT)
    style.configure("Custom.TRadiobutton", background="white", font=SETTINGSFONT)


    ###############################
    # # L A Y O U T : U E B E R # #
    ###############################


    # Dynamischer Frame mit Einstellungsmöglichkeiten
    FrameUeber = tk.Frame(popup, padx=100, pady=30, bg="white")
    FrameUeber.grid(row=1, column=1, rowspan=2, sticky="nw")

    # Überschrift für Radiobutton-Kategorie
    radiobutton_label = tk.Label(
        FrameUeber, text="Über das DD-Inv Tool", font=SETTINGSFONT, bg="white"
    )
    radiobutton_label.grid(row=0, column=0, pady=10, sticky="nw")

    def set_default_background():
        parent.configure(bg="white")
        popup.configure(bg="white")
        if hasattr(parent, "bg_label"):
            parent.bg_label.destroy()

    btn_set_bg = ttk.Button(
        FrameUeber,
        text="Hintergrund zurücksetzen",
        style="Custom.TButton",
        command=set_default_background,
    )
    btn_set_bg.grid(row=len(radio_buttons) + 3, column=0, pady=10)

    # Style anpassen
    style = ttk.Style()
    style.configure("Custom.TButton", background="white", font=SETTINGSFONT)
    style.configure("Custom.TRadiobutton", background="white", font=SETTINGSFONT)
