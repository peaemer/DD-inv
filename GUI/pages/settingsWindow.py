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
def pop_up_settings(parent):
    """
    Creates a new settings window as a pop-up.

    This function sets up a new pop-up window with specific configurations
    such as size, position, icon, and grid layout. It also manages the
    placement of header, sidebar, and dynamic content frames within the pop-up
    window. The function prepares different frames for each category and
    initializes the interface with a specific frame visible to the user.

    :param parent: The parent window to which this pop-up is associated.
    :type parent: tkinter.Tk
    :return: None
    """
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
    header_frame_settings = tk.Frame(popup, height=0)
    header_frame_settings.grid(row=0,
                               column=1,
                               sticky=tk.W + tk.E + tk.N)  # Header erstreckt sich Horizontal,

    # Konfiguriere die Spalten für den Header
    header_frame_settings.grid_columnconfigure(0, weight=1)
    header_frame_settings.grid_rowconfigure(0, weight=1)

    # Header-Logo laden und anzeigen
    popup.optionsHead = tk.PhotoImage(file="assets/Tool.png")
    header_label = tk.Label(header_frame_settings,
                            image=popup.optionsHead,
                            foreground="white")
    header_label.grid(row=1,
                      column=0,
                      padx=10,
                      pady=10,
                      sticky=tk.N + tk.W + tk.E)

    # Seitenleiste
    side_settings = tk.Frame(popup, width=200, bg=srhOrange)
    side_settings.grid(row=0, column=0, rowspan=2, sticky="nesw")
    side_settings.grid_columnconfigure(0, weight=1)

    # SRH Logo in der Seitenleiste
    popup.srh_logo = tk.PhotoImage(file="assets/srh.png")
    srh_logo_label = tk.Label(side_settings, image=popup.srh_logo, bg=srhOrange)
    srh_logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="n")


    #################################
    # # L A Y O U T : S Y S T E M # #
    #################################


    # Dynamischer Frame mit Einstellungsmöglichkeiten
    frame_system = tk.Frame(popup, padx=100, pady=30, bg="white")
    frame_system.grid(row=1, column=1, rowspan=2, sticky="nw")
    #frame_system.grid_remove()

    # Überschrift System erstellen
    radiobutton_label = tk.Label(
        frame_system, text="System", font=SETTINGSFONT, bg="white"
    )
    radiobutton_label.grid(row=0, column=0, pady=10, sticky="nw")

    # Überschrift Auflösung ändern
    button_bg_label = tk.Label(
        frame_system, text="Auflösung ändern", font=BTNFONT, bg="white"
    )
    button_bg_label.grid(row=6, column=0, pady=10, sticky="nw")

    def set_default_background():
        parent.configure(bg="white")
        popup.configure(bg="white")
        if hasattr(parent, "bg_label"):
            parent.bg_label.destroy()

    btn_set_bg = ttk.Button(
        frame_system,
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
    frame_style = tk.Frame(popup, padx=100, pady=10, bg="white")
    frame_style.grid(row=1, column=1, rowspan=2, sticky="nw")
    #frame_style.grid_forget()

    # Überschrift für Style
    radiobutton_label = tk.Label(
        frame_style, text="Style", font=SETTINGSFONT, bg="white"
    )
    radiobutton_label.grid(row=0, column=0, pady=1, sticky="nw")

    # Überschrift für Radiobutton-Kategorie
    radiobutton_label = tk.Label(
        frame_style, text="Setze einen vordefinierten Style", font=BTNFONT, bg="white"
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
        frame_style, text="Wähle aus einem Eigenem Bild", font=BTNFONT, bg="white"
    )
    button_bg_label.grid(row=7, column=0, pady=1, sticky="nw")

    def change_app_background(color):
        parent.configure(bg=color)
        popup.configure(bg=color)

    for idx, (text, image, value) in enumerate(radio_buttons):
        ttk.Radiobutton(
            frame_style,
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
        frame_style,
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
        frame_style,
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
    frame_profile = tk.Frame(popup, padx=100, pady=30, bg="white")
    #frame_profile.grid(row=1, column=1, rowspan=2, sticky="nw")
    #frame_profile.grid_forget()

    # Überschrift Passe dein Profil an
    ProfileBtn_label = tk.Label(
        frame_profile, text="Passe dein Profil an", font=SETTINGSFONT, bg="white"
    )
    ProfileBtn_label.grid(row=1, column=0, pady=10, sticky="nw")

    #frame_profile.imglogin = tk.PhotoImage(
    #    file=root_path + "")
    #frame_profile.imgmainpage = tk.PhotoImage(
    #    file=root_path + "")
    #frame_profile.imgProfileTest = tk.PhotoImage(file=root_path + "")

    # Seiteninhalt
    profilbild = tk.Button(frame_profile, bd=0, bg='white')
    username = tk.Label(frame_profile, text="Username", bd=0, bg='white', fg='#6F6C6C', font=("Poppins", 15))
    frame_profile.username = tk.Label(frame_profile, text=" ", bd=0, bg='white', fg='black', font=("Poppins", 18))

    vorname = tk.Label(frame_profile, text="Vorname", bd=0, bg='white', fg='#6F6C6C', font=("Poppins", 15))
    frame_profile.vorname = tk.Label(frame_profile, text=" ", bd=0, bg='white', fg='black', font=("Poppins", 18))

    nachname = tk.Label(frame_profile, text="Nachname", bd=0, bg='white', fg='#6F6C6C', font=("Poppins", 15))
    frame_profile.nachname = tk.Label(frame_profile, text=" ", bd=0, bg='white', fg='black', font=("Poppins", 18))

    gruppen = tk.Label(frame_profile, text="Gruppen", bd=0, bg='white', fg='#6F6C6C', font=("Poppins", 15))
    frame_profile.usergrupp = tk.Label(frame_profile, text="xx, xx", bd=0, bg='white', fg='black', font=("Poppins", 18))

    email = tk.Label(frame_profile, text="Email", bd=0, bg='white', fg='#6F6C6C', font=("Poppins", 15))
    frame_profile.useremail = tk.Label(frame_profile, text="xxx@srhk.de", bd=0, bg='white', fg='black', font=("Poppins", 18))

    rechte = tk.Label(frame_profile, text="Rechte", bd=0, bg='white', fg='#6F6C6C', font=("Poppins", 15))
    rechte_frame = tk.Frame(frame_profile, bg='#D9D9D9')
    adminrechte = tk.Label(frame_profile, text="Admin", bd=0, bg='white', fg='black', font=("Poppins", 18))
    ausbilderrechte = tk.Label(frame_profile, text="Ausbilder", bd=0, bg='white', fg='#6F6C6C',
                               font=("Poppins", 18))
    userrechte = tk.Label(frame_profile, text="Schüler", bd=0, bg='white', fg='#6F6C6C', font=("Poppins", 18))

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

    #frame_profile.grid(padx=0.21, pady=0.15, relwidth=1, relheight=0.85)


    ###############################
    # # L A Y O U T : U E B E R # #
    ###############################


    # Dynamischer Frame mit Einstellungsmöglichkeiten
    frame_ueber = tk.Frame(popup, padx=10, pady=1, bg="white")
    frame_ueber.grid(row=1, column=1, rowspan=2, sticky="new")
    #frame_ueber.grid_forget()

    # Überschrift erstellen Über das DD-Inv Tool
    Ueber_label = tk.Label(
        frame_ueber, text="Über das DD-Inv Tool", font=SETTINGSFONT, bg="white"
    )
    Ueber_label.grid(row=0, column=0, pady=1, sticky="new")

    # Unterüberschrift erstellen Credits
    Credits_label = tk.Label(
        frame_ueber, text="Credits", font=BTNFONT, bg="white"
    )
    Credits_label.grid(row=1, column=0, pady=10, sticky="new")

    # Jack Button
    def open_Jack(url):
        webbrowser.open(url)

    jack_image = PhotoImage(file="")
    btn_links_label = ttk.Label(frame_ueber, text="Peaemer (Jack)", cursor="hand2")
    btn_links_label.grid(row=2, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=jack_image)
    btn_links_label.bind("<Button-1>", lambda e: open_Jack("https://github.com/peaemer/"))

    # Alex Button
    def open_Alex(url):
        webbrowser.open(url)

    alex_image = PhotoImage(file="")
    btn_links_label = ttk.Label(frame_ueber, text="Alex5X5 (Alex)", cursor="hand2")
    btn_links_label.grid(row=3, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=alex_image)
    btn_links_label.bind("<Button-1>", lambda e: open_Alex("https://github.com/Alex5X5"))

    # Fabian Button
    def open_Fabian(url):
        webbrowser.open(url)

    fabian_image = PhotoImage(file="")
    btn_links_label = ttk.Label(frame_ueber, text="GitSchwan (Fabian)", cursor="hand2")
    btn_links_label.grid(row=4, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=fabian_image)
    btn_links_label.bind("<Button-1>", lambda e: open_Fabian("https://github.com/GitSchwan"))

    # Anakin Button
    def open_Anakin(url):
        webbrowser.open(url)

    anakin_image = PhotoImage(file="")
    btn_links_label = ttk.Label(frame_ueber, text="Chauto (Anakin)", cursor="hand2")
    btn_links_label.grid(row=5, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=anakin_image)
    btn_links_label.bind("<Button-1>", lambda e: open_Anakin("https://github.com/Chautoo"))

    # Rene Button
    def open_Rene(url):
        webbrowser.open(url)

    rene_image = PhotoImage(file="")
    btn_links_label = ttk.Label(frame_ueber, text="FemRene (Rene)", cursor="hand2")
    btn_links_label.grid(row=6, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=rene_image)
    btn_links_label.bind("<Button-1>", lambda e: open_Rene("https://github.com/FemRene"))

    # Tam Button
    def open_Tam(url):
        webbrowser.open(url)

    tam_image = PhotoImage(file="")
    btn_links_label = ttk.Label(frame_ueber, text="Tam")
    btn_links_label.grid(row=7, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=tam_image)
    btn_links_label.bind("<Button-1>", lambda e: open_Tam(""))

    # Unterüberschrift erstellen Anwendung erstellt mit folgenden Tools
    build_label = tk.Label(
        frame_ueber, text="Anwendung erstellt mit folgenden Tools", font=BTNFONT, bg="white"
    )
    build_label.grid(row=8, column=0, pady=10, sticky="new")

    # SQL3 Button
    def open_SQL3(url):
        webbrowser.open(url)

    sql3_image = PhotoImage(file="assets/SQL3Settings.png")
    btn_links_label = ttk.Label(frame_ueber, text="SQLite", cursor="hand2")
    btn_links_label.grid(row=9, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=sql3_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_SQL3("https://www.sqlite.org/"))

    # Figma Button
    def open_Figma(url):
        webbrowser.open(url)

    figma_image = PhotoImage(file="assets/FigmaSettings.png")
    btn_links_label = ttk.Label(frame_ueber, text="Figma", cursor="hand2")
    btn_links_label.grid(row=10, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=figma_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_Figma("https://www.figma.com/"))

    # PyCharm Button
    def open_PyCharm(url):
        webbrowser.open(url)

    py_charm_image = PhotoImage(file="assets/PyCharmSettings.png")
    btn_links_label = ttk.Label(frame_ueber, text="PyCharm", cursor="hand2")
    btn_links_label.grid(row=11, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=py_charm_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_PyCharm("https://www.jetbrains.com/de-de/pycharm/"))

    # Python Button
    def open_Python(url):
        webbrowser.open(url)

    python_image = PhotoImage(file="assets/PythonSettings.png")
    btn_links_label = ttk.Label(frame_ueber, text="Python", cursor="hand2")
    btn_links_label.grid(row=12, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=python_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_Python("https://www.python.org/"))

    # WindowsXP Button
    def open_WindowsXP(url):
        webbrowser.open(url)

    windows_xp_image = PhotoImage(file="assets/WindowsXPSettings.png")
    btn_links_label = ttk.Label(frame_ueber, text="WindowsXP", cursor="hand2")
    btn_links_label.grid(row=13, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=windows_xp_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_WindowsXP("https://gist.github.com/rolfn/1a05523cfed7214f4ad27f0a4ae56b07"))

    # Unterüberschrift Du möchtest das Projekt Unterstützen?
    build_label = tk.Label(
        frame_ueber, text="Du möchtest das Projekt unterstützen?", font=BTNFONT, bg="white"
    )
    build_label.grid(row=14, column=0, pady=10, sticky="new")

    # Ko-Fi Button
    def open_KoFi(url):
        webbrowser.open(url)

    ko_fi_image = PhotoImage(file="assets/KoFiSettings.png")
    btn_links_label = ttk.Label(frame_ueber, text="Ko-Fi (Spende)", cursor="hand2")
    btn_links_label.grid(row=15, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=ko_fi_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_KoFi("https://ko-fi.com/dd_inv"))

    # Feedback Button
    def open_Feedback(url):
        webbrowser.open(url)

    feedback_image = PhotoImage(file="assets/FeedbackSettings.png")
    btn_links_label = ttk.Label(frame_ueber, text="Feedback (E-Mail)", cursor="hand2")
    btn_links_label.grid(row=16, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=feedback_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_Feedback("mailto:Jack-Mike.Saering@srhk.de"))

    # Unterüberschrift Info
    build_label = tk.Label(
        frame_ueber, text="Info", font=BTNFONT, bg="white"
    )
    build_label.grid(row=17, column=0, pady=10, sticky="new")

    # VersionBuild Button
    def open_VersionBuild(url):
        webbrowser.open(url)

    logo_image = PhotoImage(file="assets/DD-Inv_Logo.png")
    btn_links_label = ttk.Label(frame_ueber, text="VersionBuild   V. 0.0.291 (Alpha)", cursor="hand2")
    btn_links_label.grid(row=18, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=logo_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_VersionBuild("https://github.com/peaemer/DD-inv/commit/2253443a1349e58db31ef8592bf77d3a7afda198"))

    # Github Button
    def open_Github(url):
        webbrowser.open(url)

    git_hub_image = PhotoImage(file="assets/GitHubSettings.png")
    btn_links_label = ttk.Label(frame_ueber, text="Visit our Github", cursor="hand2")
    btn_links_label.grid(row=19, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=git_hub_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_Github("https://github.com/peaemer/DD-inv"))


    ###############################
    # # F R A M E : S W I T C H # #
    ###############################


    # Kategorien in der Seitenleiste
    categories = ["System",
                  "Style",
                  "Profil",
                  "Über DD-Inv"]

    category_labels_settings = []
    # Dynamische Frames erstellen
    frame_system = tk.Frame(popup, padx=10, pady=30, bg="white")
    frame_style = tk.Frame(popup, padx=10, pady=30, bg="white")
    frame_profile = tk.Frame(popup, padx=10, pady=30, bg="white")
    frame_ueber = tk.Frame(popup, padx=10, pady=30, bg="white")

    # Zuordnung der Frames zu den Kategorien
    frames = {
        "System": frame_system,
        "Style": frame_style,
        "Profil": frame_profile,
        "Über DD-Inv": frame_ueber
    }

    current_frame = frames["System"]  # Halte den aktuell sichtbaren Frame
    current_frame.grid(row=1, column=1, rowspan=2, sticky="nw")

    # Funktion zum Anzeigen des Frames
    def show_frame_settings(category):
        """
        Updates the visible frame in a user interface based on the provided category.

        This function manages the display of frames by hiding the currently visible
        frame and revealing the new frame associated with the given category. It
        ensures that only one frame is visible at a time, corresponding to the user's
        selection.

        :param category: The category used to determine which frame to display. A
                         corresponding frame must exist within the frames collection.
        :return: None
        """
        print(f"Aktuell sichtbarer Frame vor Verstecken: {frames}")
        nonlocal current_frame  # Zugriff auf die äußere Variable
        print(current_frame)
        if current_frame:  # Falls bereits ein Frame angezeigt wird
            current_frame.grid_remove()  # Verstecke den aktuellen Frame
            print("if current_frame")
        new_frame = frames.get(category)
        if new_frame:  # Wenn der neue Frame existiert
            new_frame.grid(row=1, column=1, rowspan=2, sticky="nw")
            current_frame = new_frame
            print(f"Neuer aktueller Frame: {current_frame}")

    # Funktion für Klick auf Kategorie
    def on_category_click_settings(label_settings, category_settings):
        """
        Manages the label and category settings when a category is clicked.

        This function is responsible for updating the visual appearance of
        category labels and displaying the associated frame when a category
        is selected. It resets all other category labels to a default state
        and highlights the selected category for user clarity.

        :param label_settings: The label widget associated with the selected
                              category. It requires configuration to highlight
                              the selected label.
        :param category_settings: The settings or information related to the
                                 selected category. This data is used to
                                 determine which frame to display.
        :return: None
        """
        # Setze alle Labels zurück
        for cat in category_labels_settings:
            cat.config(fg="white")
            print("if on_category_click")
        # Hervorhebung des angeklickten Labels
        label_settings.config(fg="Black")
        # Zeige den zugehörigen Frame
        show_frame_settings(category_settings)

    # Kategorien in der Seitenleiste erstellen
    category_labels_settings = []  # Liste für die Label-Referenzen
    for idx, category in enumerate(categories):
        label = tk.Label(
            side_settings,
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
            lambda event, lbl=label, cat=category: on_category_click_settings(lbl, cat)
        )
        category_labels_settings.append(label)

    # Alle Frames initial verstecken
    for frame in frames.values():
        frame.grid_remove()

    # Debug Info
    print("Einstellungen vollständig geladen")