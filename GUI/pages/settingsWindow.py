import base64
import tkinter as tk
import webbrowser
from io import BytesIO
from tkinter import ttk
from tkinter import filedialog
import requests
from PIL import Image, ImageTk
import Datenbank.sqlite3api as db
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
    popup.geometry("550x700")  # groeße des Fensters
    popup.configure(background="white")  # Hintergrundfarbe
    popup.transient(parent)  # Setzt Hauptfenster in Hintergrund
    popup.grab_set()  # Fokus auf Popup
    popup.attributes('-topmost', 0)  # Fenster immer im Vordergrund der Anwendung selbst

    # Bildschirmbreite und hoehe ermitteln (fenster mittig auf Bildschirm setzten)
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    window_width, window_height = 550, 700
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    popup.resizable(True, True)  # Fenstergroeße anpassbar
    popup.iconbitmap("assets/srhIcon.ico")  # Fenster-Icon

    # Grid-Layout für Popup konfigurieren (danymische groeße)
    popup.grid_rowconfigure(0, weight=0)  # Bereich fuer Kategorien
    popup.grid_rowconfigure(1, weight=1)  # Hauptbereich
    popup.grid_columnconfigure(0, weight=0)  # Seitenleiste
    popup.grid_columnconfigure(1, weight=1)  # Hauptinhalt

    # Erstelle Header-Bereich (oben im Fenster)
    header_frame_settings = tk.Frame(popup)
    header_frame_settings.grid(row=0,
                               column=0,
                               columnspan=2,
                               sticky="nesw")  # Header erstreckt sich Horizontal,

    # Konfiguriere die Spalten für den Header
    header_frame_settings.grid_columnconfigure(1, weight=1)
    header_frame_settings.grid_rowconfigure(1, weight=1)

    # Header-Logo laden und anzeigen
    popup.optionsHead = tk.PhotoImage(file="assets/Tool.png")
    header_label = tk.Label(header_frame_settings,
                            image=popup.optionsHead,
                            foreground="white")
    header_label.grid(row=1,
                      column=0,
                      padx=320,
                      pady=10,
                      sticky="nesw")

    # Seitenleiste
    side_settings = tk.Frame(popup, width=200, bg=srhOrange)
    side_settings.grid(row=0, column=0, rowspan=2, sticky="nesw")
    side_settings.grid_columnconfigure(0, weight=1)

    # SRH Logo in der Seitenleiste
    popup.srh_logo = tk.PhotoImage(file="assets/srh.png")
    srh_logo_label = tk.Label(side_settings, image=popup.srh_logo, bg=srhOrange)
    srh_logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="n")


    ###################################
    # # L A Y O U T : P R O F I L E # #
    ###################################


    # Dynamischer Frame mit Einstellungsmöglichkeiten
    frame_profile = tk.Frame(popup, bg="white")
    frame_profile.grid(row=1, column=1, rowspan=2, sticky="nesw")
    #frame_profile.grid_forget()

    # Überschrift Dein Profil
    profile_btn_label = tk.Label(frame_profile,
                                 text="Dein Profil",
                                 font=SETTINGSFONT,
                                 bg="white")
    profile_btn_label.grid(row=0, column=0, pady=10, sticky="nw")

    def load_image_from_url(url):
        """
        Lädt ein Bild von einer angegebenen URL herunter und gibt das Bildobjekt zurück.

        Das Bild wird von der angegebenen URL abgerufen, erforderliche Daten werden im
        Speicher verarbeitet, und das Bild wird mithilfe von `Pillow` geöffnet und
        zurückgegeben.

        :param url: Die URL, von der das Bild heruntergeladen werden soll.
        :type url: str
        :return: Ein Bildobjekt, das die heruntergeladene Bilddatei repräsentiert.
        :rtype: PIL.Image.Image
        :raises requests.HTTPError: Wird ausgelöst, wenn die HTTP-Anfrage fehlschlägt, z.B. bei 404 oder 500.
        """
        response = requests.get(url)
        response.raise_for_status()  # Überprüft, ob die Anfrage erfolgreich war
        img_data = BytesIO(response.content)  # Bilddaten in einen BytesIO-Stream laden
        return Image.open(img_data)

    def load_image_from_base64(base64_string):
        """
        Decodiert einen Base64-kodierten Bild-String und lädt das Bild-Objekt.

        Diese Funktion nimmt einen Base64-kodierten Bild-String, dekodiert ihn und
        erzeugt ein Bild-Objekt, das weiterverwendet werden kann.

        :param base64_string: Der Base64-kodierte Bild-String.
        :type base64_string: str
        :return: Ein Bild-Objekt, das aus dem dekodierten Bild-String erstellt wurde.
        :rtype: Image
        """
        img_data = base64.b64decode(base64_string)
        img = Image.open(BytesIO(img_data))
        return img

    # Bild des Benutzers laden
    if cache.user_avatar.startswith("http"):
        # Bild von der URL laden und anzeigen
        try:
            img = load_image_from_url(cache.user_avatar)

            # Bild skalieren (z. B. auf 128x128 Pixel)
            img = img.resize((128, 128))

            parent.img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(frame_profile, image=parent.img_tk)
            label.grid()
        except Exception as e:
            label = tk.Label(frame_profile, text=f"Fehler beim Laden von URL: {e}")
            label.grid()
    else:
        # Bild aus Base64-String laden und anzeigen
        try:
            img = load_image_from_base64(cache.user_avatar)

            # Bild skalieren (z. B. auf 128x128 Pixel)
            img = img.resize((128, 128))

            parent.img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(frame_profile, image=parent.img_tk)
            label.grid()
        except Exception as e:
            label = tk.Label(frame_profile, text=f"Fehler beim Laden von Base64: {e}")
            label.grid()

    # Schriftzug Eingeloggt als
    profile_btn_label = tk.Label(frame_profile,
                                 text="Eingeloggt als\n"+cache.user_name,
                                 font=BTNFONT,
                                 bg="white")
    profile_btn_label.grid(row=2, column=0, pady=10, sticky="nw")

    frame_role = tk.Frame(frame_profile, padx=10, pady=30, bg="white", highlightcolor="blue")
    frame_role.grid(row=3, column=0, rowspan=1, sticky="nw")
    iR = 0

    # Schriftzug Rechte in der Gruppe
    profile_btn_label = tk.Label(frame_role,
                                 text="Rechte in der Gruppe",
                                 font=BTNFONT,
                                 bg="white")
    profile_btn_label.grid(row=0, column=0, pady=0, sticky="nw")

    for role in db.read_all_rollen():
        role2_btn_label = tk.Label(frame_role,
                                   text=role["Rolle"],
                                   font=BTNFONT,
                                   bg="white",
                                   fg="gray")
        if cache.user_group == role["Rolle"]:
            role2_btn_label.configure(fg="black")
        role2_btn_label.grid(row=iR+1, column=0, pady=0, sticky="nw")
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
        btn_image_logout = tk.PhotoImage(file="assets/BenutzerAbmeldenSettings.png")
        return btn_image_logout

    # Laden des Bildes auf den Bts
    parent.btn_image_logout = load_button_images_profile()

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
                                  command=lambda:log_out(controller),
                                  text="Benutzer Abmelden",
                                  font=BTNFONT,
                                  bg="white",
                                  cursor="hand2",
                                  image=parent.btn_image_logout,
                                  borderwidth=0)
    profile_btn_label.grid(row=5, column=0, pady=10, sticky="nw")


    #################################
    # # L A Y O U T : S Y S T E M # #
    #################################


    # Dynamischer Frame mit Einstellungsmöglichkeiten
    frame_system = tk.Frame(popup, bg="white")
    frame_system.grid(row=1, column=1, rowspan=2, sticky="nesw")
    frame_system.grid_remove()

    # Überschrift System erstellen
    radiobutton_label = tk.Label(frame_system,
                                 text="System",
                                 font=SETTINGSFONT,
                                 bg="white")
    radiobutton_label.grid(row=0, column=0, pady=10, sticky="new")

    # Überschrift Auflösung ändern
    button_bg_label = tk.Label(frame_system,
                               text="Auflösung ändern",
                               font=BTNFONT,
                               bg="white")
    button_bg_label.grid(row=6, column=0, pady=10, sticky="nw")

    def set_default_background():
        """
        Zeigt ein Pop-up-Fenster für die Einstellungen einer Anwendung an.

        Diese Funktion steuert das Display eines Einstellungspop-ups innerhalb der Anwendung.
        Sie konfiguriert visuelle Eigenschaften und verwaltet dynamische Elemente basierend
        auf den übergebenen Argumenten.

        :param parent: Hauptfenster oder Widget, das das Pop-up-Fenster enthält
        :type parent: Widget
        :param controller: Steuerungsobjekt zur Verwaltung des Pop-ups
        :type controller: object
        :return: Es wird kein Wert zurückgegeben.
        :rtype: None
        """
        parent.configure(bg="white")
        popup.configure(bg="white")
        if hasattr(parent, "bg_label"):
            parent.bg_label.destroy()

    btn_set_bg = ttk.Button(frame_system,
                            text="Hintergrund zurücksetzen",
                            style="Custom.TButton",
                            command=set_default_background)
    btn_set_bg.grid(column=0, pady=10)

    # Style anpassen
    style = ttk.Style()
    style.configure("Custom.TButton", background="white", font=BTNFONT)
    style.configure("Custom.TRadiobutton", background="white", font=BTNFONT)


    ################################
    # # L A Y O U T : S T Y L E # #
    ################################


    # Dynamischer Frame mit Einstellungsmöglichkeiten
    frame_style = tk.Frame(popup, bg="white")
    frame_style.grid(row=1, column=1, rowspan=2, sticky="nesw")
    frame_style.grid_forget()

    frame_style.columnconfigure(0, weight=1)

    # Überschrift für Style
    radiobutton_label = tk.Label(frame_style,
                                 text="Style",
                                 font=SETTINGSFONT,
                                 bg="white")
    radiobutton_label.grid(row=0, column=0, pady=1, sticky="new")

    # Überschrift für Radiobutton-Kategorie
    radiobutton_label = tk.Label(frame_style,
                                 text="Setze einen vordefinierten Style",
                                 font=BTNFONT,
                                 bg="white")
    radiobutton_label.grid(row=1, column=0, pady=1, sticky="nw")

    # Radiobuttons zur Auswahl von Farben (Themes)
    storage_variable = tk.StringVar(value="White")

    parent.option_zero = tk.PhotoImage(file="assets/DefaultBtnSettings.png")
    parent.option_one = tk.PhotoImage(file="assets/GreenBtnSettings.png")
    parent.option_two = tk.PhotoImage(file="assets/BlueBtnSettings.png")
    parent.option_three = tk.PhotoImage(file="assets/YellowBtnSettings.png")
    parent.option_for = tk.PhotoImage(file="assets/BlackBtnSettings.png")

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
        btn_image_select = tk.PhotoImage(file="assets/BesseresAussehenWählen.png")
        btn_image_reset = tk.PhotoImage(file="assets/HintergrundZurücksetzen.png")
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
    frame_ueber.grid_forget()

    # Ueberschrift erstellen Über das DD-Inv Tool
    ueber_label = tk.Label(frame_ueber,
                           text="Über das DD-Inv Tool",
                           font=SETTINGSFONT,
                           bg="white")
    ueber_label.grid(row=0, column=0, pady=1, sticky="new")

    # Unterüberschrift erstellen Credits
    Credits_label = tk.Label(frame_ueber,
                             text="Credits",
                             font=BTNFONT,
                             bg="white")
    Credits_label.grid(row=1, column=0, pady=10, sticky="new")

    # Jack Button
    def open_Jack(url):
        webbrowser.open(url)

    jack_image = tk.PhotoImage(file="")
    btn_links_label = ttk.Label(frame_ueber, text="Peaemer (Jack)", cursor="hand2")
    btn_links_label.grid(row=2, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=jack_image)
    btn_links_label.bind("<Button-1>", lambda e: open_Jack("https://github.com/peaemer/"))

    # Alex Button
    def open_Alex(url):
        webbrowser.open(url)

    alex_image = tk.PhotoImage(file="")
    btn_links_label = ttk.Label(frame_ueber, text="Alex5X5 (Alex)", cursor="hand2")
    btn_links_label.grid(row=3, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=alex_image)
    btn_links_label.bind("<Button-1>", lambda e: open_Alex("https://github.com/Alex5X5"))

    # Fabian Button
    def open_Fabian(url):
        webbrowser.open(url)

    fabian_image = tk.PhotoImage(file="")
    btn_links_label = ttk.Label(frame_ueber, text="GitSchwan (Fabian)", cursor="hand2")
    btn_links_label.grid(row=4, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=fabian_image)
    btn_links_label.bind("<Button-1>", lambda e: open_Fabian("https://github.com/GitSchwan"))

    # Anakin Button
    def open_Anakin(url):
        webbrowser.open(url)

    anakin_image = tk.PhotoImage(file="")
    btn_links_label = ttk.Label(frame_ueber, text="Chauto (Anakin)", cursor="hand2")
    btn_links_label.grid(row=5, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=anakin_image)
    btn_links_label.bind("<Button-1>", lambda e: open_Anakin("https://github.com/Chautoo"))

    # Rene Button
    def open_Rene(url):
        webbrowser.open(url)

    rene_image = tk.PhotoImage(file="")
    btn_links_label = ttk.Label(frame_ueber, text="FemRene (Rene)", cursor="hand2")
    btn_links_label.grid(row=6, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=rene_image)
    btn_links_label.bind("<Button-1>", lambda e: open_Rene("https://github.com/FemRene"))

    # Tam Button
    def open_Tam(url):
        webbrowser.open(url)

    tam_image = tk.PhotoImage(file="")
    btn_links_label = ttk.Label(frame_ueber, text="Tam")
    btn_links_label.grid(row=7, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=tam_image)
    btn_links_label.bind("<Button-1>", lambda e: open_Tam(""))

    # Unterueberschrift erstellen Anwendung erstellt mit folgenden Tools
    build_label = tk.Label(frame_ueber,
                           text="Anwendung erstellt mit folgenden Tools",
                           font=BTNFONT,
                           bg="white")
    build_label.grid(row=8, column=0, pady=10, sticky="new")

    # SQL3 Button
    def open_SQL3(url):
        webbrowser.open(url)

    sql3_image = tk.PhotoImage(file="assets/SQL3Settings.png")
    btn_links_label = ttk.Label(frame_ueber, text="SQLite", cursor="hand2")
    btn_links_label.grid(row=9, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=sql3_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_SQL3("https://www.sqlite.org/"))

    # Figma Button
    def open_Figma(url):
        webbrowser.open(url)

    figma_image = tk.PhotoImage(file="assets/FigmaSettings.png")
    btn_links_label = ttk.Label(frame_ueber, text="Figma", cursor="hand2")
    btn_links_label.grid(row=10, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=figma_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_Figma("https://www.figma.com/"))

    # PyCharm Button
    def open_PyCharm(url):
        webbrowser.open(url)

    py_charm_image = tk.PhotoImage(file="assets/PyCharmSettings.png")
    btn_links_label = ttk.Label(frame_ueber, text="PyCharm", cursor="hand2")
    btn_links_label.grid(row=11, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=py_charm_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_PyCharm("https://www.jetbrains.com/de-de/pycharm/"))

    # Python Button
    def open_Python(url):
        webbrowser.open(url)

    python_image = tk.PhotoImage(file="assets/PythonSettings.png")
    btn_links_label = ttk.Label(frame_ueber, text="Python", cursor="hand2")
    btn_links_label.grid(row=12, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=python_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_Python("https://www.python.org/"))

    # WindowsXP Button
    def open_WindowsXP(url):
        webbrowser.open(url)

    windows_xp_image = tk.PhotoImage(file="assets/WindowsXPSettings.png")
    btn_links_label = ttk.Label(frame_ueber, text="WindowsXP", cursor="hand2")
    btn_links_label.grid(row=13, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=windows_xp_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_WindowsXP("https://gist.github.com/rolfn/1a05523cfed7214f4ad27f0a4ae56b07"))

    # Unterueberschrift Du möchtest das Projekt Unterstützen?
    build_label = tk.Label(frame_ueber,
                           text="Du möchtest das Projekt unterstützen?",
                           font=BTNFONT,
                           bg="white")
    build_label.grid(row=14, column=0, pady=10, sticky="new")

    # Ko-Fi Button
    def open_KoFi(url):
        webbrowser.open(url)

    ko_fi_image = tk.PhotoImage(file="assets/KoFiSettings.png")
    btn_links_label = ttk.Label(frame_ueber, text="Ko-Fi (Spende)", cursor="hand2")
    btn_links_label.grid(row=15, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=ko_fi_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_KoFi("https://ko-fi.com/dd_inv"))

    # Feedback Button
    def open_Feedback(url):
        webbrowser.open(url)

    feedback_image = tk.PhotoImage(file="assets/FeedbackSettings.png")
    btn_links_label = ttk.Label(frame_ueber, text="Feedback (E-Mail)", cursor="hand2")
    btn_links_label.grid(row=16, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=feedback_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_Feedback("mailto:Jack-Mike.Saering@srhk.de"))

    # Unterueberschrift Info
    build_label = tk.Label(frame_ueber,
                           text="Info",
                           font=BTNFONT,
                           bg="white")
    build_label.grid(row=17, column=0, pady=10, sticky="new")

    # VersionBuild Button
    def open_VersionBuild(url):
        webbrowser.open(url)

    logo_image = tk.PhotoImage(file="assets/DD-Inv_Logo.png")
    btn_links_label = ttk.Label(frame_ueber, text="VersionBuild   V. 0.0.311 (Alpha)", cursor="hand2")
    btn_links_label.grid(row=18, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=logo_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_VersionBuild("https://github.com/peaemer/DD-inv/commit/3cf34836049538c57b3cac282a740703e0312ba7"))

    # Github Button
    def open_Github(url):
        webbrowser.open(url)

    git_hub_image = tk.PhotoImage(file="assets/GitHubSettings.png")
    btn_links_label = ttk.Label(frame_ueber, text="Visit our Github", cursor="hand2")
    btn_links_label.grid(row=19, column=0, pady=2, sticky="new")
    btn_links_label.configure(width=30, anchor='center', image=git_hub_image, compound="left")
    btn_links_label.bind("<Button-1>", lambda e: open_Github("https://github.com/peaemer/DD-inv"))


    ###############################
    # # F R A M E : S W I T C H # #
    ###############################


    # Kategorien in der Seitenleiste
    categories = ["Profil",
                  "System",
                  "Style",
                  "Über DD-Inv"]

    category_labels_settings = []
    # Dynamische Frames erstellen
    frame_profile = tk.Frame(popup, padx=10, pady=30, bg="white")
    frame_system = tk.Frame(popup, padx=10, pady=30, bg="white")
    frame_style = tk.Frame(popup, padx=10, pady=30, bg="white")
    frame_ueber = tk.Frame(popup, padx=10, pady=30, bg="white")

    # Zuordnung der Frames zu den Kategorien
    frames = {"Profil": frame_profile,
              "System": frame_system,
              "Style": frame_style,
              "Über DD-Inv": frame_ueber}

    current_frame = frames["System"]  # Halte den aktuell sichtbaren Frame
    current_frame.grid(row=1, column=1, rowspan=2, sticky="nw")

    # Funktion zum Anzeigen des Frames
    def show_frame_settings(category):
        """
        Öffnet das Einstellungs-Popup-Fenster und bindet es mit dem übergebenen
        Elternelement und der Steuerkomponente. Diese Funktion dient zur
        Konfigurationsaktualisierung, die in einer grafischen Benutzeroberfläche
        integriert ist.

        :param parent: Das Elternelement des Einstellungs-Popups
        :type parent: Objekt
        :param controller: Steuereinheit zur Verwaltung des Einstellungszustands
        :type controller: Objekt
        :return: Gibt keinen Rückgabewert zurück
        :rtype: None
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
        Ruft bestimmte Einstellungen auf und hebt ausgewählte Kategorien visuell hervor,
        indem Label- und Frame-Eigenschaften konfiguriert werden. Wird verwendet, um Benutzern ein interaktives
        Navigationssystem innerhalb der Konfigurationsoberfläche zu bieten.

        :param label_settings: Das Label-Widget, das hervorgehoben werden soll.
        :type label_settings: Tkinter.Label
        :param category_settings: Die Kategorie oder der Frame, der mit dem angeklickten Label verbunden
            ist und angezeigt werden soll.
        :type category_settings: Tkinter.Frame

        :return: Gibt keinen Rückgabewert zurück.
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

    # Alle Frames initial verstecken
    for frame in frames.values():
        frame.grid_remove()

    # Debug Info
    print("Einstellungen vollständig geladen")