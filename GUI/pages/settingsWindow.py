import tkinter as tk
import webbrowser
from tkinter import ttk
from tkinter import *
from tkinter import filedialog


# Schriftarten / Farbschema
LARGEFONT = ("Arial", 30)
SETTINGSFONT = ("Arial", 18, 'bold')
BTNFONT = ("Arial", 15)
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

    category_labelsSettings = []
    # Dynamische Frames erstellen
    FrameSystem = tk.Frame(popup, padx=10, pady=30, bg="white")
    FrameStyle = tk.Frame(popup, padx=10, pady=30, bg="white")
    FrameProfile = tk.Frame(popup, padx=10, pady=30, bg="white")
    FrameUeber = tk.Frame(popup, padx=10, pady=30, bg="white")

    # Zuordnung der Frames zu den Kategorien
    frames = {
        "System": FrameSystem,
        "Style": FrameStyle,
        "Profil": FrameProfile,
        "Über DD-Inv": FrameUeber
    }

    current_frame = frames["Über DD-Inv"]  # Halte den aktuell sichtbaren Frame

    # Funktion zum Anzeigen des Frames
    def showFrame_Settings(category):
        print(f"Aktuell sichtbarer Frame vor Verstecken: {frames}")
        nonlocal current_frame  # Zugriff auf die äußere Variable
        print(current_frame)
        if current_frame:  # Falls bereits ein Frame angezeigt wird
            current_frame.grid_forget()  # Verstecke den aktuellen Frame
            print("if current_frame")
        new_frame = frames.get(category)
        if new_frame:  # Wenn der neue Frame existiert
            new_frame.grid(row=1, column=1, rowspan=2, sticky="nw")
            current_frame = new_frame
            print(f"Neuer aktueller Frame: {current_frame}")

    # Funktion für Klick auf Kategorie
    def onCategoryClick_Settings(labelSettings, categorySettings):
        # Setze alle Labels zurück
        for cat in category_labelsSettings:
            cat.config(fg="white")
            print("if on_category_click")
        # Hervorhebung des angeklickten Labels
        labelSettings.config(fg="Black")
        # Zeige den zugehörigen Frame
        showFrame_Settings(categorySettings)

    # Kategorien in der Seitenleiste erstellen
    category_labelsSettings = []  # Liste für die Label-Referenzen
    for idx, category in enumerate(categories):
        label = tk.Label(
            sideSettings,
            text=category,
            bd=0,
            relief=tk.FLAT,
            font=SETTINGSFONT,
            fg="white",
            bg=srhOrange,
        )
        label.grid(padx=10, pady=8, row=idx + 1, column=0, sticky="w")
        label.bind(
            "<Button-1>",
            lambda event, lbl=label, cat=category: onCategoryClick_Settings(lbl, cat)
        )
        category_labelsSettings.append(label)

    # Alle Frames initial verstecken
    for frame in frames.values():
        frame.grid_forget()

    # Debug Info
    print("Einstellungen vollständig geladen")


    #################################
    # # L A Y O U T : S Y S T E M # #
    #################################


    # Dynamischer Frame mit Einstellungsmöglichkeiten
    FrameSystem = tk.Frame(popup, padx=100, pady=30, bg="white")
    FrameSystem.grid(row=1, column=1, rowspan=2, sticky="nw")
    FrameSystem.grid_forget()

    # Überschrift System erstellen
    radiobutton_label = tk.Label(
        FrameSystem, text="System", font=SETTINGSFONT, bg="white"
    )
    radiobutton_label.grid(row=0, column=0, pady=10, sticky="nw")

    # Überschrift Auflösung ändern
    button_bg_label = tk.Label(
        FrameSystem, text="Auflösung ändern", font=BTNFONT, bg="white"
    )
    button_bg_label.grid(row=6, column=0, pady=10, sticky="nw")

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
    btn_set_bg.grid(column=0, pady=10)

    # Style anpassen
    style = ttk.Style()
    style.configure("Custom.TButton", background="white", font=BTNFONT)
    style.configure("Custom.TRadiobutton", background="white", font=BTNFONT)


    ################################
    # # L A Y O U T : S T Y L E # #
    ################################


    # Dynamischer Frame mit Einstellungsmöglichkeiten
    FrameStyle = tk.Frame(popup, padx=100, pady=10, bg="white")
    FrameStyle.grid(row=1, column=1, rowspan=2, sticky="nw")
    FrameStyle.grid_forget()

    # Überschrift für Style
    radiobutton_label = tk.Label(
        FrameStyle, text="Style", font=SETTINGSFONT, bg="white"
    )
    radiobutton_label.grid(row=0, column=0, pady=1, sticky="nw")

    # Überschrift für Radiobutton-Kategorie
    radiobutton_label = tk.Label(
        FrameStyle, text="Setze einen vordefinierten Style", font=BTNFONT, bg="white"
    )
    radiobutton_label.grid(row=1, column=0, pady=1, sticky="nw")

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
        FrameStyle, text="Wähle aus einem Eigenem Bild", font=BTNFONT, bg="white"
    )
    button_bg_label.grid(row=7, column=0, pady=1, sticky="nw")

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
        ).grid(row=idx + 2, column=0, pady=5)

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
    btn_chose_picture.grid(row=len(radio_buttons) + 3, column=0, pady=10)

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
    btn_set_bg.grid(row=len(radio_buttons) + 4, column=0, pady=10)

    # Style anpassen
    style = ttk.Style()
    style.configure("Custom.TButton", background="white", font=BTNFONT)
    style.configure("Custom.TRadiobutton", background="white", font=BTNFONT)


    ###################################
    # # L A Y O U T : P R O F I L E # #
    ###################################


    # Dynamischer Frame mit Einstellungsmöglichkeiten
    FrameProfile = tk.Frame(popup, padx=100, pady=30, bg="white")
    FrameProfile.grid(row=1, column=1, rowspan=2, sticky="nw")
    FrameProfile.grid_forget()

    # Überschrift Passe dein Profil an
    ProfileBtn_label = tk.Label(
        FrameProfile, text="Passe dein Profil an", font=SETTINGSFONT, bg="white"
    )
    ProfileBtn_label.grid(row=1, column=0, pady=10, sticky="nw")

    #FrameProfile.imglogin = tk.PhotoImage(
    #    file=root_path + "")
    #FrameProfile.imgmainpage = tk.PhotoImage(
    #    file=root_path + "")
    #FrameProfile.imgProfileTest = tk.PhotoImage(file=root_path + "")

    # Seiteninhalt
    profilbild = tk.Button(FrameProfile, bd=0, bg='white')
    username = tk.Label(FrameProfile, text="Username", bd=0, bg='white', fg='#6F6C6C', font=("Poppins", 15))
    FrameProfile.username = tk.Label(FrameProfile, text=" ", bd=0, bg='white', fg='black', font=("Poppins", 18))

    vorname = tk.Label(FrameProfile, text="Vorname", bd=0, bg='white', fg='#6F6C6C', font=("Poppins", 15))
    FrameProfile.vorname = tk.Label(FrameProfile, text=" ", bd=0, bg='white', fg='black', font=("Poppins", 18))

    nachname = tk.Label(FrameProfile, text="Nachname", bd=0, bg='white', fg='#6F6C6C', font=("Poppins", 15))
    FrameProfile.nachname = tk.Label(FrameProfile, text=" ", bd=0, bg='white', fg='black', font=("Poppins", 18))

    gruppen = tk.Label(FrameProfile, text="Gruppen", bd=0, bg='white', fg='#6F6C6C', font=("Poppins", 15))
    FrameProfile.usergrupp = tk.Label(FrameProfile, text="xx, xx", bd=0, bg='white', fg='black', font=("Poppins", 18))

    email = tk.Label(FrameProfile, text="Email", bd=0, bg='white', fg='#6F6C6C', font=("Poppins", 15))
    FrameProfile.useremail = tk.Label(FrameProfile, text="xxx@srhk.de", bd=0, bg='white', fg='black', font=("Poppins", 18))

    rechte = tk.Label(FrameProfile, text="Rechte", bd=0, bg='white', fg='#6F6C6C', font=("Poppins", 15))
    rechte_frame = tk.Frame(FrameProfile, bg='#D9D9D9')
    adminrechte = tk.Label(FrameProfile, text="Admin", bd=0, bg='white', fg='black', font=("Poppins", 18))
    ausbilderrechte = tk.Label(FrameProfile, text="Ausbilder", bd=0, bg='white', fg='#6F6C6C',
                               font=("Poppins", 18))
    userrechte = tk.Label(FrameProfile, text="Schüler", bd=0, bg='white', fg='#6F6C6C', font=("Poppins", 18))

    profilbild.grid(padx=0, pady=0)

    #username.grid(padx=499, pady=10)
    #parent.username.grid(padx=502, pady=40)

    #vorname.grid(padx=499, pady=90)
    #parent.vorname.grid(padx=502, pady=120)

    #nachname.place(padx=499, pady=170)
    #parent.nachname.grid(x=502, y=200)

    #gruppen.grid(padx=499, pady=250)
    #parent.usergrupp.grid(padx=502, pady=280)

    #email.grid(padx=0, pady=500)
    #parent.useremail.grid(padx=3, pady=525)

    #rechte.grid(padx=0, pady=570)
    #rechte_frame.grid(padx=3, pady=605, width=1, height=80)
    #adminrechte.grid(padx=13, pady=590)
    #ausbilderrechte.grid(padx=13, pady=630)
    #userrechte.grid(padx=13, pady=670)

    #FrameProfile.grid(padx=0.21, pady=0.15, relwidth=1, relheight=0.85)


    ###############################
    # # L A Y O U T : U E B E R # #
    ###############################


    # Dynamischer Frame mit Einstellungsmöglichkeiten
    FrameUeber = tk.Frame(popup, padx=10, pady=1, bg="white")
    FrameUeber.grid(row=1, column=1, rowspan=2, sticky="new")
    #FrameUeber.grid_forget()

    # Überschrift erstellen Über das DD-Inv Tool
    Ueber_label = tk.Label(
        FrameUeber, text="Über das DD-Inv Tool", font=SETTINGSFONT, bg="white"
    )
    Ueber_label.grid(row=0, column=0, pady=1, sticky="new")

    # Unterüberschrift erstellen Credits
    Credits_label = tk.Label(
        FrameUeber, text="Credits", font=BTNFONT, bg="white"
    )
    Credits_label.grid(row=1, column=0, pady=10, sticky="new")

    # Jack Button
    def open_Jack(url):
        webbrowser.open(url)

    JackImage = PhotoImage(file="")
    BtnLinks_label = ttk.Label(FrameUeber, text="Peaemer (Jack)", cursor="hand2")
    BtnLinks_label.grid(row=2, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=JackImage)
    BtnLinks_label.bind("<Button-1>", lambda e: open_Jack("https://github.com/peaemer/"))

    # Alex Button
    def open_Alex(url):
        webbrowser.open(url)

    AlexImage = PhotoImage(file="")
    BtnLinks_label = ttk.Label(FrameUeber, text="Alex5X5 (Alex)", cursor="hand2")
    BtnLinks_label.grid(row=3, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=AlexImage)
    BtnLinks_label.bind("<Button-1>", lambda e: open_Alex("https://github.com/Alex5X5"))

    # Fabian Button
    def open_Fabian(url):
        webbrowser.open(url)

    FabianImage = PhotoImage(file="")
    BtnLinks_label = ttk.Label(FrameUeber, text="GitSchwan (Fabian)", cursor="hand2")
    BtnLinks_label.grid(row=4, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=FabianImage)
    BtnLinks_label.bind("<Button-1>", lambda e: open_Fabian("https://github.com/GitSchwan"))

    # Anakin Button
    def open_Anakin(url):
        webbrowser.open(url)

    AnakinImage = PhotoImage(file="")
    BtnLinks_label = ttk.Label(FrameUeber, text="Chauto (Anakin)", cursor="hand2")
    BtnLinks_label.grid(row=5, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=AnakinImage)
    BtnLinks_label.bind("<Button-1>", lambda e: open_Anakin("https://github.com/Chautoo"))

    # Rene Button
    def open_Rene(url):
        webbrowser.open(url)

    ReneImage = PhotoImage(file="")
    BtnLinks_label = ttk.Label(FrameUeber, text="FemRene (Rene)", cursor="hand2")
    BtnLinks_label.grid(row=6, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=ReneImage)
    BtnLinks_label.bind("<Button-1>", lambda e: open_Rene("https://github.com/FemRene"))

    # Tam Button
    def open_Tam(url):
        webbrowser.open(url)

    TamImage = PhotoImage(file="")
    BtnLinks_label = ttk.Label(FrameUeber, text="Tam")
    BtnLinks_label.grid(row=7, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=TamImage)
    BtnLinks_label.bind("<Button-1>", lambda e: open_Tam(""))

    # Unterüberschrift erstellen Anwendung erstellt mit folgenden Tools
    Build_label = tk.Label(
        FrameUeber, text="Anwendung erstellt mit folgenden Tools", font=BTNFONT, bg="white"
    )
    Build_label.grid(row=8, column=0, pady=10, sticky="new")

    # SQL3 Button
    def open_SQL3(url):
        webbrowser.open(url)

    SQL3Image = PhotoImage(file="assets/SQL3Settings.png")
    BtnLinks_label = ttk.Label(FrameUeber, text="SQLite", cursor="hand2")
    BtnLinks_label.grid(row=9, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=SQL3Image, compound="left")
    BtnLinks_label.bind("<Button-1>", lambda e: open_SQL3("https://www.sqlite.org/"))

    # Figma Button
    def open_Figma(url):
        webbrowser.open(url)

    FigmaImage = PhotoImage(file="assets/FigmaSettings.png")
    BtnLinks_label = ttk.Label(FrameUeber, text="Figma", cursor="hand2")
    BtnLinks_label.grid(row=10, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=FigmaImage, compound="left")
    BtnLinks_label.bind("<Button-1>", lambda e: open_Figma("https://www.figma.com/"))

    # PyCharm Button
    def open_PyCharm(url):
        webbrowser.open(url)

    PyCharmImage = PhotoImage(file="assets/PyCharmSettings.png")
    BtnLinks_label = ttk.Label(FrameUeber, text="PyCharm", cursor="hand2")
    BtnLinks_label.grid(row=11, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=PyCharmImage, compound="left")
    BtnLinks_label.bind("<Button-1>", lambda e: open_PyCharm("https://www.jetbrains.com/de-de/pycharm/"))

    # Python Button
    def open_Python(url):
        webbrowser.open(url)

    PythonImage = PhotoImage(file="assets/PythonSettings.png")
    BtnLinks_label = ttk.Label(FrameUeber, text="Python", cursor="hand2")
    BtnLinks_label.grid(row=12, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=PythonImage, compound="left")
    BtnLinks_label.bind("<Button-1>", lambda e: open_Python("https://www.python.org/"))

    # WindowsXP Button
    def open_WindowsXP(url):
        webbrowser.open(url)

    WindowsXPImage = PhotoImage(file="assets/WindowsXPSettings.png")
    BtnLinks_label = ttk.Label(FrameUeber, text="WindowsXP", cursor="hand2")
    BtnLinks_label.grid(row=13, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=WindowsXPImage, compound="left")
    BtnLinks_label.bind("<Button-1>", lambda e: open_WindowsXP("https://gist.github.com/rolfn/1a05523cfed7214f4ad27f0a4ae56b07"))

    # Unterüberschrift Du möchtest das Projekt Unterstützen?
    Build_label = tk.Label(
        FrameUeber, text="Du möchtest das Projekt unterstützen?", font=BTNFONT, bg="white"
    )
    Build_label.grid(row=14, column=0, pady=10, sticky="new")

    # Ko-Fi Button
    def open_KoFi(url):
        webbrowser.open(url)

    KoFiImage = PhotoImage(file="assets/KoFiSettings.png")
    BtnLinks_label = ttk.Label(FrameUeber, text="Ko-Fi (Spende)", cursor="hand2")
    BtnLinks_label.grid(row=15, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=KoFiImage, compound="left")
    BtnLinks_label.bind("<Button-1>", lambda e: open_KoFi("https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white"))

    # Feedback Button
    def open_Feedback(url):
        webbrowser.open(url)

    FeedbackImage = PhotoImage(file="assets/FeedbackSettings.png")
    BtnLinks_label = ttk.Label(FrameUeber, text="Feedback (E-Mail)", cursor="hand2")
    BtnLinks_label.grid(row=16, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=FeedbackImage, compound="left")
    BtnLinks_label.bind("<Button-1>", lambda e: open_Feedback("mailto:Jack-Mike.Saering@srhk.de"))

    # Unterüberschrift Info
    Build_label = tk.Label(
        FrameUeber, text="Info", font=BTNFONT, bg="white"
    )
    Build_label.grid(row=17, column=0, pady=10, sticky="new")

    # VersionBuild Button
    def open_VersionBuild(url):
        webbrowser.open(url)

    LogoImage = PhotoImage(file="assets/DD-Inv_Logo.png")
    BtnLinks_label = ttk.Label(FrameUeber, text="VersionBuild   V. 0.0232 (Alpha)", cursor="hand2")
    BtnLinks_label.grid(row=18, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=LogoImage, compound="left")
    BtnLinks_label.bind("<Button-1>", lambda e: open_VersionBuild("https://github.com/peaemer/DD-inv/commit/f010504196f5d8c601abcf00c799beb76470b839"))

    # Github Button
    def open_Github(url):
        webbrowser.open(url)

    GitHubImage = PhotoImage(file="assets/GitHubSettings.png")
    BtnLinks_label = ttk.Label(FrameUeber, text="Visit our Github", cursor="hand2")
    BtnLinks_label.grid(row=19, column=0, pady=2, sticky="new")
    BtnLinks_label.configure(width=30, anchor='center', image=GitHubImage, compound="left")
    BtnLinks_label.bind("<Button-1>", lambda e: open_Github("https://github.com/peaemer/DD-inv"))
