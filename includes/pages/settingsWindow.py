import tkinter as tk
import webbrowser
from tkinter import ttk
from tkinter import filedialog
import customtkinter as ctk
from includes.sec_data_info import sqlite3api as db
import cache

# Schriftarten / Farbschema
LARGEFONT = ("Arial", 30)
SETTINGSFONT = ("Arial", 18, 'bold')
BTNFONT = ("Arial", 15)
srhGrey = "#d9d9d9"
srhOrange = "#DF4807"


#########################
# H A U P T L A Y O U T #
#########################

# Funktion erstellt Popupfenster "Einstellungen"
def pop_up_settings(parent, controller):
    """
    Erstellt ein neues Einstellungsfenster als Pop-up mit verschiedenen
    Funktionen zur Anpassung und Anzeige von Benutzerdaten in einer GUI-Anwendung.

    Das Pop-up-Fenster bietet eine graphische Benutzeroberfläche, die folgende
    Aspekte umfasst:
    - Einstellungsoptionen, die in einem dynamisch anpassbaren Layout präsentiert
      werden.
    - Benutzerinformationen, einschließlich Profilbilder und Rollen in der Gruppe.
    - Anzeige von Bildern, die entweder von URLs oder Base64-codierten Strings
      geladen werden können.
    - Anpassbare Seitenelemente und Farbschemata, um den Stil der Anwendung
      konsistent zu halten.

    Das Fenster wird zentriert auf dem Bildschirm angezeigt und kann in seinen
    Abmessungen angepasst werden. Es beinhaltet Header-, Seitenleisten- und
    Profilbereiche sowie weitere konfigurierbare Abschnitte.

    :param parent: Das Hauptfenster, von welchem das Pop-up angezeigt wird.
    :type parent: tk.Tk
    :param controller: Ein übergeordnetes Steuerungsobjekt der Anwendung, das
        eventuell benötigt wird, um auf globale Informationen und Methoden der
        Anwendung zuzugreifen.
    :type controller: object
    :return: Gibt das konfigurierte Einstellungs-Pop-up Fenster als `tk.Toplevel`
        Objekt zurück.
    :rtype: tk.Toplevel
    """
    # erstellt ein neues Fenster
    popup = tk.Toplevel(parent)
    popup.title("Einstellungen")
    popup.geometry("750x550")  # groeße des Fensters
    popup.configure(background="white")  # Hintergrundfarbe
    popup.transient(parent)  # Setzt Hauptfenster in Hintergrund
    popup.grab_set()  # Fokus auf Popup
    popup.attributes('-topmost', 0)  # Fenster immer im Vordergrund der Anwendung selbst

    # Bildschirmbreite und hoehe ermitteln (fenster mittig auf Bildschirm setzten)
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    window_width, window_height = 750, 550
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    popup.resizable(True, True)  # Fenstergroeße anpassbar
    from ._avatarManager import resource_path
    popup.iconbitmap(resource_path("./includes/assets/srhIcon.ico"))  # Fenster-Icon

    # Grid-Layout für Popup konfigurieren (danymische groeße)
    popup.grid_rowconfigure(0, weight=0)  # Bereich fuer Kategorien
    popup.grid_rowconfigure(1, weight=1)  # Hauptbereich
    popup.grid_columnconfigure(0, weight=0)  # Seitenleiste
    popup.grid_columnconfigure(1, weight=1)  # Hauptinhalt

    def update_header_icon(categorie):
        """Aktualisiert das Header-Icon basierend auf der ausgewählten Kategorie."""
        # Wähle das passende Icon basierend auf der Kategorie
        # new_icon = category_icons.get(categories)
        for cat in category_icons:
            if cat == categorie:
                new_icon = category_icons.get(cat)
                header_label.configure(image=new_icon)
                header_label.image = new_icon  # Verhindert, dass das Bild von der Garbage Collection gelöscht wird.

    # Header-Bereich erstellen
    header_frame_settings = tk.Frame(popup)
    header_frame_settings.grid(row=0, column=0, columnspan=2, sticky="nesw")

    # Konfiguration für Header
    header_frame_settings.grid_columnconfigure(1, weight=1)
    header_frame_settings.grid_rowconfigure(1, weight=1)

    # Icons laden
    default_icon = tk.PhotoImage(file=resource_path("./includes/assets/ProfileSettingsIcon.png"))
    category_icons: dict = {"Profil": tk.PhotoImage(file=resource_path("./includes/assets/ProfileSettingsIcon.png")),
                            "System": tk.PhotoImage(file=resource_path("./includes/assets/SystemSettingsIcon.png")),
                            "Style": tk.PhotoImage(file=resource_path("./includes/assets/StyleIconSettings.png")),
                            "Über DD-Inv": tk.PhotoImage(file=resource_path("./includes/assets/Tool.png"))}

    # Standard-Header-Icon
    popup.optionsHead = default_icon
    header_label = tk.Label(header_frame_settings, image=popup.optionsHead, foreground="white")
    header_label.grid(row=1, column=0, padx=420, pady=10, sticky="nesw")
    # Seitenleiste
    side_settings = tk.Frame(popup, width=200, bg=srhOrange)
    side_settings.grid(row=0, column=0, rowspan=2, sticky="nesw")
    side_settings.grid_columnconfigure(0, weight=1)

    # SRH Logo in der Seitenleiste
    from ._avatarManager import resource_path
    popup.srh_logo = tk.PhotoImage(file=resource_path("./includes/assets/srh.png"))
    srh_logo_label = tk.Label(side_settings, image=popup.srh_logo, bg=srhOrange)
    srh_logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="n")

    ###################################
    # # L A Y O U T : P R O F I L E # #
    ###################################

    # Dynamischer Frame mit Einstellungsmöglichkeiten
    frame_profile = tk.Frame(popup, bg="white")
    frame_profile.grid(row=1, column=1, rowspan=2, columnspan=2, sticky="nesw")

    # Überschrift Dein Profil
    profile_btn_label = tk.Label(frame_profile,
                                 text="Dein Profil",
                                 font=SETTINGSFONT,
                                 bg="white")
    profile_btn_label.grid(row=0, column=0, pady=10, columnspan=2, sticky="new")

    # Frame für das Profilbild
    frame_within_picture = tk.Frame(frame_profile, padx=5, bg="white", highlightcolor="blue")
    frame_within_picture.grid(row=1, column=0, rowspan=1, sticky="nw")

    # Profilbild zum Laden importieren
    from ._avatarManager import loadImage
    parent.avatar = loadImage(parent=parent, width=128, height=128)
    label = tk.Label(frame_within_picture, image=parent.avatar)
    label.grid(row=0)

    # Schriftzug Eingeloggt als
    profile_btn_label = tk.Label(frame_profile,
                                 text="Eingeloggt als\n" + cache.user_name,
                                 font=BTNFONT,
                                 bg="white")
    profile_btn_label.grid(row=3, column=0, pady=10, rowspan=2, sticky="nw")

    frame_role = tk.Frame(frame_profile, padx=5, pady=30, bg="white", highlightcolor="blue")
    frame_role.grid(row=4, column=0, rowspan=1, sticky="nw")
    iR = 0

    # Schriftzug Rechte in der Gruppe
    profile_btn_label = tk.Label(frame_role,
                                 text="Rechte in der Gruppe",
                                 font=BTNFONT,
                                 bg="white")
    profile_btn_label.grid(row=0, column=0, sticky="nw")

    for role in db.read_all_rollen():
        role2_btn_label = tk.Label(frame_role,
                                   text=role["Rolle"],
                                   font=BTNFONT,
                                   bg="white",
                                   fg="gray")
        if cache.user_group == role["Rolle"]:
            role2_btn_label.configure(fg="black")
        role2_btn_label.grid(row=iR + 1, column=0, pady=0, sticky="nw")
        iR += 1

    # PNG-Bild für Btn
    def load_button_images_profile():
        """
        Lädt und gibt das Bild einer Schaltfläche für die Abmeldung des Benutzers zurück.

        Dieses Bild kann in einer GUI verwendet werden, um eine konsistente Darstellung
        der Benutzeroberfläche zu gewährleisten.

        :return: Das Bild der Schaltfläche als `tk.PhotoImage` Objekt.
        :rtype: tk.PhotoImage
        """
        btn_image_logout = tk.PhotoImage(file=resource_path("./includes/assets/BenutzerAbmeldenSettings.png"))
        return btn_image_logout

    # Laden des Bildes auf den Abmelden Btn
    parent.btn_image_logout = load_button_images_profile()

    # Eingabe für die Profilbild-URL
    profile_image_url_label = tk.Label(frame_profile,
                                       text="Profilbild-URL eingeben",
                                       font=BTNFONT,
                                       bg="white")
    profile_image_url_label.grid(row=1, column=1, pady=10, sticky="ne")

    profile_image_url = ctk.CTkEntry(frame_profile, border_width=0, corner_radius=20, text_color="black",
                                     fg_color=srhGrey)
    profile_image_url.grid(row=1, column=1, pady=40, sticky="ne")

    # Importieren der Funktion URL
    from ._avatarManager import load_image_from_url

    # Laden des Bildes für Profile Btn
    parent.btn_image_set_profile_picture_settings = tk.PhotoImage(file="./includes/assets/SetProfileSettings.png")

    # Button zum Aktualisieren des Profilbilds
    update_image_button = tk.Button(frame_profile,
                                    text="Profilbild setzen",
                                    image=parent.btn_image_set_profile_picture_settings,
                                    bg="white",
                                    borderwidth=0,
                                    cursor="hand2",
                                    command=load_image_from_url)
    update_image_button.grid(row=3, column=1, pady=10, sticky="ne")

    # def zum Abmelden des Benutzers
    def log_out(controller):
        """
        Zeigt die Einstellungs-Popup-Funktionalität an und erlaubt es dem Benutzer, sich auszuloggen.

        :param parent: Das Eltern-Widget, das als Basis für das Popup-Fenster dient.
        :type parent: widget
        :param controller: Der Controller, der für die Navigation und Zustandsverwaltung der Anwendung
                           verantwortlich ist.
        :type controller: Controller-Klasse
        """
        from .logInWindow import logInWindow
        cache.user_group = None  # Benutzergruppe zurücksetzen
        controller.show_frame(logInWindow)
        popup.destroy()

    # Schriftzug Benutzer Abmelden
    profile_btn_label = tk.Button(frame_profile,
                                  command=lambda: log_out(controller),
                                  text="Benutzer Abmelden",
                                  font=BTNFONT,
                                  bg="white",
                                  cursor="hand2",
                                  image=parent.btn_image_logout,
                                  borderwidth=0)
    profile_btn_label.grid(row=4, column=1, pady=10, sticky="ne")

    #################################
    # # L A Y O U T : S Y S T E M # #
    #################################

    # Dynamischer Frame mit Einstellungsmöglichkeiten
    frame_system = tk.Frame(popup, bg="white")
    frame_system.grid(row=1, column=1, rowspan=2, sticky="nesw")

    # Überschrift System erstellen
    radiobutton_label = tk.Label(frame_system,
                                 text="System",
                                 font=SETTINGSFONT,
                                 bg="white")
    radiobutton_label.grid(row=0, column=0, pady=10, columnspan=2, sticky="new")

    # Überschrift Auflösung ändern
    button_bg_label = tk.Label(frame_system,
                               text="Auflösung ändern",
                               font=BTNFONT,
                               bg="white")
    button_bg_label.grid(row=1, column=0, pady=10, sticky="nw")

    def fenster_groesse_aendern(parent):
        breite = breite_entry.get()
        hoehe = hoehe_entry.get()
        if breite.isdigit() and hoehe.isdigit():  # Überprüfen, ob die Eingaben Zahlen sind
            parent.geometry(f"{breite}x{hoehe}")
        else:
            info_label.config(text="Bitte gültige Zahlen eingeben.")

    # Eingabefelder für Breite und Höhe
    breite_label = tk.Label(frame_system, text="Breite:", background="white", font=BTNFONT)
    breite_label.grid(row=2, column=0)
    breite_entry = ctk.CTkEntry(frame_system, corner_radius=20, fg_color=srhGrey, border_width=0)
    breite_entry.grid(row=3)

    hoehe_label = tk.Label(frame_system, text="Höhe:", background="white", font=BTNFONT)
    hoehe_label.grid(row=4, column=0)
    hoehe_entry = ctk.CTkEntry(frame_system, corner_radius=20, fg_color=srhGrey, border_width=0)
    hoehe_entry.grid(row=5)

    # Button zur Bestätigung
    aendern_button = tk.Button(frame_system, text="Auflösung ändern", command=fenster_groesse_aendern)
    aendern_button.grid(row=6)

    # Info-Label für Rückmeldungen
    info_label = tk.Label(frame_system, text="")
    info_label.grid(row=7)

    ################################
    # # L A Y O U T : S T Y L E # #
    ################################

    # Dynamischer Frame mit Einstellungsmöglichkeiten
    frame_style = tk.Frame(popup, bg="white")
    frame_style.grid(row=1, column=1, rowspan=2, sticky="nesw")

    frame_style.columnconfigure(0, weight=1)

    # Überschrift für Style
    radiobutton_label = tk.Label(frame_style,
                                 text="Style",
                                 font=SETTINGSFONT,
                                 bg="white")
    radiobutton_label.grid(row=0, column=0, pady=1, columnspan=2, sticky="new")

    # Überschrift für Radiobutton-Kategorie
    radiobutton_label = tk.Label(frame_style,
                                 text="Setze einen vordefinierten Style",
                                 font=BTNFONT,
                                 bg="white")
    radiobutton_label.grid(row=1, column=0, pady=1, sticky="nw")

    # Radiobuttons zur Auswahl von Farben (Themes)
    storage_variable = tk.StringVar(value="White")

    parent.option_zero = tk.PhotoImage(file=resource_path("./includes/assets/DefaultBtnSettings.png"))
    parent.option_one = tk.PhotoImage(file=resource_path("./includes/assets/GreenBtnSettings.png"))
    parent.option_two = tk.PhotoImage(file=resource_path("./includes/assets/BlueBtnSettings.png"))
    parent.option_three = tk.PhotoImage(file=resource_path("./includes/assets/YellowBtnSettings.png"))
    parent.option_for = tk.PhotoImage(file=resource_path("./includes/assets/BlackBtnSettings.png"))

    radio_buttons = [("Standard", parent.option_zero, "White"),
                     ("Grün", parent.option_one, "dark Green"),
                     ("Blau", parent.option_two, "light Blue"),
                     ("Gelb", parent.option_three, "Yellow"),
                     ("Schwarz", parent.option_for, "Black")]

    # Überschrift für Backgroundbutton-Kategorie
    button_bg_label = tk.Label(frame_style,
                               text="Wähle aus einem Eigenem Bild",
                               font=BTNFONT,
                               bg="white")
    button_bg_label.grid(row=7, column=0, pady=1, sticky="nw")

    # def fuer btn change app background
    def change_app_background(color):
        """
        Funktion, um den App-Hintergrundfarben zu ändern.

        Diese Funktion nimmt eine Farbe als Eingabe und aktualisiert sowohl den
        Hintergrund einer bestimmten Eltern-Komponente als auch den eines Popup-Fensters
        mit der angegebenen Farbe. Sie wird verwendet, um das Erscheinungsbild der
        Benutzeroberfläche dynamisch anzupassen.

        :param color: Die neue Hintergrundfarbe als Zeichenkette.
        :type color: str
        :return: Diese Funktion hat keinen Rückgabewert.
        """
        parent.configure(bg=color)
        popup.configure(bg=color)

    for idx, (text, image, value) in enumerate(radio_buttons):
        ttk.Radiobutton(frame_style,
                        image=image,
                        text=text,
                        variable=storage_variable,
                        value=value,
                        style="Custom.TRadiobutton",
                        command=lambda color=value: change_app_background(color)).grid(row=idx + 2,
                                                                                       column=0,
                                                                                       pady=5,
                                                                                       sticky="w")

    # PNG-Bilder für Buttons laden
    def load_button_images_style():
        """
        Lädt die Bilder für die Schaltflächen im Button-Stil.

        Diese Funktion lädt und gibt zwei `tk.PhotoImage`-Objekte für die Darstellung von
        Schaltflächenbildern zurück. Die Bilder werden aus angegebenen Dateien geladen und
        können anschließend in der Benutzeroberfläche verwendet werden.

        :raises FileNotFoundError: Wenn die angegebenen Bilddateien nicht gefunden werden.

        :return: Ein Tupel von `tk.PhotoImage`-Objekten, das die Bilder für die
                 Schaltflächen enthält.
        :rtype: Tuple[tk.PhotoImage, tk.PhotoImage]
        """
        btn_image_select = tk.PhotoImage(file=resource_path("./includes/assets/BesseresAussehenWählen.png"))
        btn_image_reset = tk.PhotoImage(file=resource_path("./includes/assets/HintergrundZurücksetzen.png"))
        return btn_image_select, btn_image_reset

    # Laden der Bilder auf den Bts
    parent.btn_image_select, parent.btn_image_reset = load_button_images_style()

    # Hintergrundbild-Auswahl
    def apply_selected_image_style():
        """
        Zeigt ein Popup-Fenster für die Einstellungen an und ermöglicht es den Benutzern, ein Hintergrundbild
        auszuwählen. Diese Funktion öffnet ein Dateidialogfeld, um ein Bild auszuwählen, und wendet das ausgewählte
        Bild als Hintergrund auf das übergebene Eltern-Widget an.

        :param parent: Das übergeordnete Widget bzw. der Container, auf den das ausgewählte Bild angewendet werden soll.
        :type parent: tk.Widget
        :param controller: Der Controller, der für die Steuerung des Popup-Fensters verantwortlich ist.
        :type controller: object
        :return: Es wird kein Wert zurückgegeben.
        """
        file_path = filedialog.askopenfilename(title="Wähle ein Bild aus...",
                                               filetypes=[("Bilddateien", "*.png;*.jpg;*.jpeg")])

        if file_path:
            bg_image = tk.PhotoImage(file=file_path)
            parent.bg_label = tk.Label(parent, image=bg_image)
            parent.bg_label.image = bg_image
            parent.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

    btn_chose_picture = ttk.Button(frame_style,
                                   text="Besseres Aussehen auswählen...",
                                   style="Custom.TButton",
                                   image=parent.btn_image_select,
                                   command=apply_selected_image_style)
    btn_chose_picture.grid(row=len(radio_buttons) + 3, column=0, pady=10, sticky="w")

    # Hintergrund setzen
    def set_default_background():
        """
        Konfiguriert die Pop-up-Einstellungen für eine spezifische Oberfläche.
        Das Hauptziel der Funktion ist es, das Erscheinungsbild des Pop-ups gemäß
        angegebener Parameter zu definieren.

        :param parent: Die übergeordnete Oberfläche, auf der das Pop-up angewendet wird.
        :type parent: Widget
        :param controller: Kontrollinstanz, die die Logik des Pop-ups steuert.
        :type controller: Object
        :return: Keine Rückgabe.
        :rtype: None
        """
        parent.configure(bg="white")
        popup.configure(bg="white")
        if hasattr(parent, "bg_label"):
            parent.bg_label.destroy()

    btn_set_bg = ttk.Button(frame_style,
                            text="Hintergrund zurücksetzen",
                            style="Custom.TButton",
                            image=parent.btn_image_reset,
                            command=set_default_background)
    btn_set_bg.grid(row=len(radio_buttons) + 4, column=0, pady=10, sticky="w")

    # Style anpassen
    style = ttk.Style()
    style.configure("Custom.TButton", background="white", font=BTNFONT, borderwidth=0)
    style.configure("Custom.TRadiobutton", background="white", font=BTNFONT)

    ###############################
    # # L A Y O U T : U E B E R # #
    ###############################

    # Dynamischer Frame mit Einstellungsmöglichkeiten
    frame_ueber = tk.Frame(popup, bg="white")
    frame_ueber.grid(row=1, column=1, rowspan=2, sticky="new")

    # Ueberschrift erstellen Über das DD-Inv Tool
    ueber_label = tk.Label(frame_ueber,
                           text="Über das DD-Inv Tool",
                           font=SETTINGSFONT,
                           bg="white")
    ueber_label.grid(row=0, column=0, pady=1, columnspan=2, sticky="new")

    # Unterüberschrift erstellen Credits
    Credits_label = tk.Label(frame_ueber,
                             text="Credits",
                             font=BTNFONT,
                             bg="white")
    Credits_label.grid(row=1, column=0, pady=10, sticky="new")

    # Liste mit den Namenm, URL, Bild fuer Credits
    buttons_data_credits = [{"name": "Peaemer (Jack)", "url": "https://github.com/peaemer/", "image": ""},
                            {"name": "Alex5X5 (Alex)", "url": "https://github.com/Alex5X5", "image": ""},
                            {"name": "GitSchwan (Fabian)", "url": "https://github.com/GitSchwan", "image": ""},
                            {"name": "Chauto (Anakin)", "url": "https://github.com/Chautoo", "image": ""},
                            {"name": "FemRene (Rene)", "url": "https://github.com/FemRene", "image": ""},
                            {"name": "Tam", "url": "", "image": ""}]

    # Funktion zum oeffnen der URL
    def open_url(url):
        if url:
            webbrowser.open(url)

    # Erstellen der Buttons mit einer Schleife
    for index, button in enumerate(buttons_data_credits, start=2):
        image = tk.PhotoImage(file=button["image"])  # Bild laden
        btn_label = ttk.Label(frame_ueber,
                              text=button["name"],
                              cursor="hand2")
        btn_label.grid(row=index, column=0, pady=2, sticky="new")
        btn_label.configure(width=30, anchor='center', image=image, compound="left", background="white")
        btn_label.bind("<Button-1>", lambda e, url=button["url"]: open_url(url))

    # Unterueberschrift erstellen Anwendung erstellt mit folgenden Tools
    build_label = tk.Label(frame_ueber,
                           text="Anwendung erstellt mit folgenden Tools",
                           font=BTNFONT,
                           bg="white")
    build_label.grid(row=8, column=0, pady=10, sticky="new")

    # Liste mit den Namenm, URL, Bild fuer genutzte Tools
    buttons_data_tools = [
        {"name": "SQL3", "url": "https://www.sqlite.org/", "image": resource_path("includes/assets/SQL3Settings.png")},
        {"name": "Figma", "url": "https://www.figma.com/", "image": resource_path("includes/assets/FigmaSettings.png")},
        {"name": "PyCharm", "url": "https://www.jetbrains.com/de-de/pycharm/",
         "image": resource_path("includes/assets/PyCharmSettings.png")},
        {"name": "Python", "url": "https://www.python.org/",
         "image": resource_path("includes/assets/PythonSettings.png")},
        {"name": "WindowsXP", "url": "https://gist.github.com/rolfn/1a05523cfed7214f4ad27f0a4ae56b07",
         "image": resource_path("includes/assets/WindowsXPSettings.png")}]

    # Funktion zum oeffnen der URL
    def open_url(url):
        if url:
            webbrowser.open(url)

    # Erstellen der Buttons mit einer Schleife
    for index, button in enumerate(buttons_data_tools, start=10):
        image = tk.PhotoImage(file=button["image"])  # Bild laden
        btn_label = ttk.Label(frame_ueber,
                              text=button["name"],
                              cursor="hand2")
        btn_label.grid(row=index, column=0, pady=2, sticky="new")
        btn_label.configure(width=30, anchor='center', image=image, compound="left", background="white")
        btn_label.bind("<Button-1>", lambda e, url=button["url"]: open_url(url))

    # Unterueberschrift Du möchtest das Projekt Unterstützen?
    build_label = tk.Label(frame_ueber,
                           text="Du möchtest das Projekt unterstützen?",
                           font=BTNFONT,
                           bg="white")
    build_label.grid(row=16, column=0, pady=10, sticky="new")

    # Liste mit den Namenm, URL, Bild fuer Projekt Unterstuetzen
    buttons_data_support = [{"name": "Ko-Fi", "url": "https://ko-fi.com/dd_inv",
                             "image": resource_path("includes/assets/KoFiSettings.png")},
                            {"name": "Feedback", "url": "mailto:Jack-Mike.Saering@srhk.de",
                             "image": resource_path("includes/assets/FeedbackSettings.png")}]

    # Funktion zum oeffnen der URL
    def open_url(url):
        if url:
            webbrowser.open(url)

    # Erstellen der Buttons mit einer Schleife
    for index, button in enumerate(buttons_data_support, start=17):
        image = tk.PhotoImage(file=button["image"])  # Bild laden
        btn_label = ttk.Label(frame_ueber,
                              text=button["name"],
                              cursor="hand2")
        btn_label.grid(row=index, column=0, pady=2, sticky="new")
        btn_label.configure(width=30, anchor='center', image=image, compound="left", background="white")
        btn_label.bind("<Button-1>", lambda e, url=button["url"]: open_url(url))

    # Unterueberschrift Info
    build_label = tk.Label(frame_ueber,
                           text="Info",
                           font=BTNFONT,
                           bg="white")
    build_label.grid(row=19, column=0, pady=10, sticky="new")

    # Liste mit den Namenm, URL, Bild fuer Info
    buttons_data_info = [
        {"name": "VersionBuild   V. 0.1 BETA", "url": "https://github.com/peaemer/DD-inv/releases/latest",
         "image": resource_path("includes/assets/DD-Inv_Logo.png")},
        {"name": "GitHub", "url": "https://github.com/peaemer/DD-inv",
         "image": resource_path("includes/assets/GitHubSettings.png")}]

    # Funktion zum oeffnen der URL
    def open_url(url):
        if url:
            webbrowser.open(url)

    # Erstellen der Buttons mit einer Schleife
    for index, button in enumerate(buttons_data_info, start=20):
        image = tk.PhotoImage(file=button["image"])  # Bild laden
        btn_label = ttk.Label(frame_ueber,
                              text=button["name"],
                              cursor="hand2")
        btn_label.grid(row=index, column=0, pady=2, sticky="new")
        btn_label.configure(width=30, anchor='center', image=image, compound="left", background="white")
        btn_label.bind("<Button-1>", lambda e, url=button["url"]: open_url(url))

    ###############################
    # # F R A M E : S W I T C H # #
    ###############################

    # Kategorien in der Seitenleiste
    categories = ["Profil",
                  "System",
                  "Style",
                  "Über DD-Inv"]

    category_labels_settings = []

    # Zuordnung der Frames zu den Kategorien
    frames = {"Profil": frame_profile,
              "System": frame_system,
              "Style": frame_style,
              "Über DD-Inv": frame_ueber}

    current_frame = frames["Profil"]  # Halte den aktuell sichtbaren Frame
    current_frame.grid(row=1, column=1, rowspan=2, sticky="nw")

    # Funktion zum Anzeigen des Frames
    def show_frame_settings(category):
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
        update_header_icon(category_settings)
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
        label = tk.Label(side_settings,
                         text=category,
                         bd=0,
                         relief=tk.FLAT,
                         font=SETTINGSFONT,
                         fg="white",
                         bg=srhOrange)
        label.grid(padx=10, pady=8, row=idx + 1, column=0, sticky="w")

        label.bind("<Button-1>",
                   lambda event,
                          lbl=label,
                          cat=category:
                   on_category_click_settings(lbl, cat))
        category_labels_settings.append(label)

    # Verstecke alle Frames außer dem initialen Profil-Frame
    for key, frame in frames.items():
        if key != "Profil":  # Verstecke nur die anderen Frames
            frame.grid_remove()
