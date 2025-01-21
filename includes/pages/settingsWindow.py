import tkinter as tk

import customtkinter as ctk
from tkinter import ttk

from .customMessageBoxResetPasswrd import customMessageBoxResetPasswrd

import webbrowser
from includes.util.Logging import Logger, DEBUG_MODE_NORMAL, DEBUG_MODE_ALL
from includes.sec_data_info import sqlite3api as db
from ._styles import *
import cache

import os
import sys
import json



CONFIG_PATH = "user_config.json"
logger: Logger = Logger('SettingsWindow')


#####################
# S P E I C H E R N #
#####################

# speichern der Einstellungen von windowSettings.py
def save_settings(dictionary: dict):
    """
    Speichert Benutzereinstellungen in einer JSON-Datei.
    """
    jobj = json.dumps(dictionary, indent=4)
    with open("config.json", "w") as outfile:
        outfile.write(jobj)

# setezen der neuen Aufloesung
def load_settings():
    """
    Lädt Benutzereinstellungen aus einer JSON-Datei.
    Gibt Standardwerte zurück, wenn die Datei nicht existiert.
    """
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    return {"resolution": {"width": 1920, "height": 1080}}  # Standardwerte

# neustarten der Anwendung
def close_app():
    """
    Schließt die Anwendung nach der Änderung einer Einstellung.
    """
    python = sys.executable  # Pfad zur Python-Executable
    os.execl(python, python, *sys.argv)

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
    popup.configure(background="white")  # Hintergrundfarbe
    popup.transient(parent)  # Setzt Hauptfenster in Hintergrund
    popup.grab_set()  # Fokus auf Popup
    popup.attributes('-topmost', 0)  # Fenster immer im Vordergrund der Anwendung selbst

    # Bildschirmbreite und hoehe ermitteln (fenster mittig auf Bildschirm setzten)
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    window_width, window_height = 850, 580
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    popup.resizable(False, False)  # Fenstergroeße anpassbar

    #Einfuegen des SRH-Icons
    from ._avatarManager import resource_path
    popup.iconbitmap(resource_path("./includes/assets/srhIcon.ico"))  # Fenster-Icon

    # Grid-Layout für Popup konfigurieren (danymische groeße)
    popup.grid_rowconfigure(0, weight=0)  # Bereich fuer Kategorien
    popup.grid_rowconfigure(1, weight=1)  # Hauptbereich
    popup.grid_columnconfigure(0, weight=0)  # Seitenleiste
    popup.grid_columnconfigure(1, weight=1)  # Hauptinhalt

    #def zum aendern des Icons im Header bassierend auf der angezeiten Seite
    def update_header_icon(categorie):
        try:
            """Aktualisiert das Header-Icon basierend auf der ausgewählten Kategorie."""
            # Wähle das passende Icon basierend auf der Kategorie
            # new_icon = category_icons.get(categories)
            for cat in category_icons:
                if cat == categorie:
                    new_icon = category_icons.get(cat)
                    header_label.configure(image=new_icon)
                    header_label.image = new_icon  # Verhindert, dass das Bild von der Garbage Collection gelöscht wird.

        except Exception as e:
            logger.error(f"Error when loading or changing the icon in the heading area. {button['image']}: {e}")

    # Header-Bereich erstellen
    header_frame_settings = tk.Frame(popup,
                                     background=srhGrey)
    header_frame_settings.grid(row=0, column=1, columnspan=1, sticky="new")

    # Konfiguration für Header
    header_frame_settings.grid_columnconfigure(0, weight=1)
    header_frame_settings.grid_rowconfigure(0, weight=1)

    # Icons laden
    default_icon = tk.PhotoImage(file=resource_path("./includes/assets/ProfileSettingsIcon.png"))
    category_icons: dict = {"Profil": tk.PhotoImage(file=resource_path("./includes/assets/ProfileSettingsIcon.png")),
                            "System": tk.PhotoImage(file=resource_path("./includes/assets/SystemSettingsIcon.png")),
                            "Über DD-Inv": tk.PhotoImage(file=resource_path("./includes/assets/Tool.png"))}

    # Standard-Header-Icon
    popup.optionsHead = default_icon
    header_label = tk.Label(header_frame_settings,
                            image=popup.optionsHead,
                            foreground="white",
                            background=srhGrey)
    header_label.grid(row=1, column=0, padx=0, pady=10, sticky="nsew")

    # Seitenleiste
    side_settings = tk.Frame(popup,
                             width=200,
                             bg=srhOrange)
    side_settings.grid(row=0, column=0, rowspan=2, sticky="nsw")
    side_settings.grid_columnconfigure(0, weight=1)

    # SRH Logo in der Seitenleiste
    from ._avatarManager import resource_path
    popup.srh_logo = tk.PhotoImage(file=resource_path("./includes/assets/srh.png"))
    srh_logo_label = tk.Label(side_settings,
                              image=popup.srh_logo,
                              bg=srhOrange)
    srh_logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="n")

    #LOGGER PRINT
    logger.debug(f"Complete loading of the 'Main' settings page. {['image']}")

    ###################################
    # # L A Y O U T : P R O F I L E # #
    ###################################

    # Dynamischer Frame mit Einstellungsmöglichkeiten
    frame_profile = tk.Frame(popup, bg="white")
    frame_profile.grid(row=1, column=1, sticky="nsew")
    frame_profile.grid_columnconfigure(0, weight=1)
    frame_profile.grid_columnconfigure(1, weight=1)

    # Überschrift Dein Profil
    profile_btn_label = tk.Label(frame_profile,
                                 text="Dein Profil",
                                 font=SETTINGS_FONT,
                                 bg="white")
    profile_btn_label.grid(row=0, column=0, pady=0, columnspan=3, sticky="new")

    # Profilbild zum Laden importieren
    parent.avatar = cache.user_avatarx128
    parent.settings_img_label = tk.Label(frame_profile,
                                         image=parent.avatar,
                                         background="white")
    parent.settings_img_label.grid(row=1, column=0, padx=90, pady=5, rowspan=2, columnspan=1, sticky="nws")

    # Feld für eigene Bio
    own_bio = ctk.CTkEntry(frame_profile,
                           border_width=1,
                           corner_radius=corner,
                           placeholder_text="Bio",
                           text_color="black",
                           fg_color="white",
                           border_color=srhGrey,
                           font=SETTINGS_FONT,
                           width=250)
    own_bio.grid(row=3, column=0, rowspan=2, padx=20, pady=5, sticky="nws")

    # Schriftzug Eingeloggt als
    profile_btn_label = tk.Label(frame_profile,
                                 text="Eingeloggt als\n" + cache.user_name,
                                 font=SETTINGS_BTN_FONT,
                                 bg="white")
    profile_btn_label.grid(row=5, column=0, padx=20, pady=5, rowspan=1, sticky="nws")

    # Schriftzug Rechte in der Gruppe
    profile_btn_label = tk.Label(frame_profile,
                                 text="Rechte des Users\n" + cache.user_group,
                                 font=SETTINGS_BTN_FONT,
                                 bg="white")
    profile_btn_label.grid(row=6, column=0, padx=20, pady=5, sticky="nws")

    def load_user_email(nutzername):
        """
        Lädt die E-Mail-Adresse eines Benutzers aus der Datenbank.

        :param nutzername: Der Benutzername, dessen E-Mail abgerufen werden soll.
        :return: Die E-Mail-Adresse oder ein Fehlerhinweis.
        """
        from includes.sec_data_info.sqlite3api import read_benutzer
        try:
            benutzer_data = read_benutzer(nutzername)
            if benutzer_data and "Email" in benutzer_data:
                return benutzer_data["Email"]
            else:
                return "E-Mail nicht gefunden"
        except Exception as e:
            logger.error(f"Error while trying to load email: {e}")
            return "Error while loading the Email."

    # Schriftzug E-Mail-Adresse
    profile_btn_label = tk.Label(frame_profile,
                                 text="E-Mail-Adressse\n" + load_user_email(cache.user_name),
                                 font=SETTINGS_BTN_FONT,
                                 anchor=tk.W,
                                 bg="white")
    profile_btn_label.grid(row=7, column=0, padx=20, pady=5, sticky="nws")

    # Eingabe für die Profilbild-URL
    profile_image_url_label = tk.Label(frame_profile,
                                       text="Profilbild-URL / Base64 eingeben",
                                       font=SETTINGS_BTN_FONT,
                                       bg="white",
                                       anchor="w")
    profile_image_url_label.grid(row=1, column=1, sticky="n")

    profile_image_url = ctk.CTkEntry(frame_profile,
                                     border_width=border,
                                     corner_radius=corner,
                                     text_color="black",
                                     fg_color=srhGrey,
                                     font=SETTINGS_FONT,
                                     width=250)
    profile_image_url.grid(row=2, column=1, columnspan=1, pady=5, sticky="n")

    # Importieren der Funktion URL
    from ._avatarManager import loadImage

    # Laden des Bildes für Profile Btn
    parent.btn_image_set_profile_picture_settings = tk.PhotoImage(
        file=resource_path("./includes/assets/SetProfileSettings.png"))

    def setAvatar():
        try:
            cache.user_avatarx128 = loadImage(parent=parent, image=profile_image_url.get(), width=128, height=128)
            parent.avatar_new = cache.user_avatarx128
            cache.user_avatar = loadImage(parent=parent, image=profile_image_url.get(), width=48, height=48)
            parent.avatar = cache.user_avatar
            db.upsert_avatar(cache.user_name, profile_image_url.get())
            parent.settings_img_label.configure(image=parent.avatar_new)
            from .mainPage import mainPage
            mainPage.update_profile_picture()

        except Exception as e:
            logger.error(f"Error while applying the profile picture. {button['image']}: {e}")
            info_label.config(text="Bitte eine valide URL oder Base64 eingeben.")
            info_label.config(text="Eingabe ungültig.")

    # Button zum Aktualisieren des Profilbilds
    update_image_button = tk.Button(frame_profile,
                                    text="Profilbild setzen",
                                    image=parent.btn_image_set_profile_picture_settings,
                                    bg="white",
                                    activebackground="white",
                                    borderwidth=0,
                                    cursor="hand2",
                                    command=lambda: setAvatar())
    update_image_button.grid(row=3, column=1, sticky="n")


    # def zum Abmelden des Benutzers
    global cotr
    contr: controller = controller
    def log_out_settings(controller: controller):
        """
        Zeigt die Einstellungs-Popup-Funktionalität an und erlaubt es dem Benutzer, sich auszuloggen.

        :param parent: Das Eltern-Widget, das als Basis für das Popup-Fenster dient.
        :type parent: widget
        :param controller: Der Controller, der für die Navigation und Zustandsverwaltung der Anwendung
                           verantwortlich ist.
        :type controller: Controller-Klasse
        """
        try:
            from .logInWindow import logInWindow
            cache.user_group = None  # Benutzergruppe zurücksetzen
            contr.show_frame(logInWindow)
            popup.destroy()

        except Exception as e:
            print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: Error during logout by the user. {e}")

    # Laden des Bildes auf dem Passwort Btn
    parent.btn_image_password = tk.PhotoImage(file=resource_path("./includes/assets/ResetPasswordSettings.png"))

    # Schriftzug Passwort ändern
    cache.controller = controller
    profile_btn_label = tk.Button(frame_profile,
                                  command=lambda: customMessageBoxResetPasswrd(parent=parent,
                                                                               title="Passwort ändern",
                                                                               message="Bitte ändere das Passwort \n "
                                                                                       "in den nachfolgenden Feldern.",
                                                                               calb= lambda :log_out_settings(controller)),
                                  text="Passwort ändern",
                                  font=SETTINGS_BTN_FONT,
                                  bg="white",
                                  activebackground="white",
                                  cursor="hand2",
                                  image=parent.btn_image_password,
                                  borderwidth=0)
    profile_btn_label.grid(row=5, column=1, pady=10, sticky="ns")

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

    # Schriftzug Benutzer Abmelden
    profile_btn_label = tk.Button(frame_profile,
                                  command=lambda: log_out_settings(controller),
                                  text="Benutzer Abmelden",
                                  font=SETTINGS_BTN_FONT,
                                  bg="white",
                                  activebackground="white",
                                  cursor="hand2",
                                  image=parent.btn_image_logout,
                                  borderwidth=0)
    profile_btn_label.grid(row=6, column=1, pady=10, sticky="ns")

    #LOGGER PRINT
    logger.debug(f"Complete loading of the 'Profile' settings page. {['image']}")

    #################################
    # # L A Y O U T : S Y S T E M # #
    #################################

    # Dynamischer Frame mit Einstellungsmöglichkeiten
    frame_system = tk.Frame(popup, bg="white")
    frame_system.grid(row=1, column=1, rowspan=1, sticky="nsew")
    frame_system.grid_columnconfigure(0, weight=1)
    frame_system.grid_columnconfigure(1, weight=1)
    frame_system.grid_rowconfigure(0, weight=1)
    frame_system.grid_rowconfigure(1, weight=0)
    frame_system.grid_rowconfigure(2, weight=0)
    frame_system.grid_rowconfigure(3, weight=0)
    frame_system.grid_rowconfigure(4, weight=0)
    frame_system.grid_rowconfigure(5, weight=0)
    frame_system.grid_rowconfigure(6, weight=0)
    frame_system.grid_rowconfigure(7, weight=0)
    frame_system.grid_rowconfigure(8, weight=0)
    frame_system.grid_rowconfigure(9, weight=0)
    frame_system.grid_rowconfigure(10, weight=0)

    # Überschrift System erstellen
    radiobutton_label = tk.Label(frame_system,
                                 text="System",
                                 font=SETTINGS_FONT,
                                 bg="white")
    radiobutton_label.grid(row=0, column=0, pady=0, columnspan=1, sticky="new")

    # Überschrift Auflösung ändern
    button_bg_label = tk.Label(frame_system,
                               text="Auflösung anpassen",
                               font=SETTINGS_BTN_FONT,
                               bg="white")
    button_bg_label.grid(row=1, column=0, pady=10, sticky="new")

    def fenster_groesse_aendern(parent):
        breite = breite_entry.get()
        hoehe = hoehe_entry.get()
        if breite.isdigit() and hoehe.isdigit():  # Überprüfen, ob die Eingaben Zahlen sind
            dicti = {"breite": int(breite),
                     "hoehe": int(hoehe)}
            save_settings(dicti)  # Auflösung speichern
            info_label.config(text="Auflösung wird gespeichert und App geschlossen...")
            parent.after(3000, close_app)  # Verzögerung von 3 Sekunden und dann Neustart
        else:
            info_label.config(text="Bitte gültige Zahlen eingeben.")

    # Eingabefelder fuer Breite
    breite_label = tk.Label(frame_system,
                            text="Breite",
                            background="white",
                            font=SETTINGS_BTN_FONT)
    breite_label.grid(row=2, column=0)

    breite_entry = ctk.CTkEntry(frame_system,
                                corner_radius=20,
                                fg_color=srhGrey,
                                text_color="black",
                                font=SETTINGS_BTN_FONT,
                                placeholder_text="z.B. 1920",
                                border_width=0)
    breite_entry.grid(row=3, column=0)

    # Eingabefeld fuer Hoehe
    hoehe_label = tk.Label(frame_system,
                           text="Höhe",
                           background="white",
                           font=SETTINGS_BTN_FONT)
    hoehe_label.grid(row=4, column=0)

    hoehe_entry = ctk.CTkEntry(frame_system,
                               corner_radius=20,
                               fg_color=srhGrey,
                               text_color="black",
                               font=SETTINGS_BTN_FONT,
                               placeholder_text="z.B. 1080",
                               border_width=0)
    hoehe_entry.grid(row=5, column=0)

    # Button zur Bestätigung
    parent.set_res_btn = tk.PhotoImage(file=resource_path("./includes/assets/SetResSettings.png"))
    aendern_button = tk.Button(frame_system,
                               image=parent.set_res_btn,
                               borderwidth=0,
                               cursor="hand2",
                               activebackground="white",
                               background="white",
                               command=lambda: fenster_groesse_aendern(parent))
    aendern_button.grid(row=6, pady=5, column=0)

    # DBUG-Modus als Einstellung für Admins
    def DBUG_for_Admin(parent):
        if cache.user_group_data['ADMIN_FEATURE'] == "True":
            # Schriftzug DEBUG-Modus aktivieren / deaktivieren
            zoom_label = tk.Label(frame_system,
                                  text="DEBUG-Modus aktivieren / deaktivieren",
                                  background="white",
                                  font=SETTINGS_BTN_FONT)
            zoom_label.grid(row=7, column=0, pady=10, sticky="new")

            # Checkbox DEBUG NORMAL
            debug_normal_label = tk.Label(frame_system,
                                          text="DEBUG-Normal",
                                          background="white",
                                          font=SETTINGS_BTN_FONT)
            debug_normal_label.grid(row=8, column=0, pady=10, sticky="new")

            def on_debug_normal_click():
                DEBUG_MODE_NORMAL = False

            parent.debug_normel = ctk.CTkCheckBox(frame_system, text_color="white", command=lambda: on_debug_normal_click)
            parent.debug_normel.grid(column=1, row=8)

            # Checkbox DEBUG ALL
            debug_all_label = tk.Label(frame_system,
                                          text="DEBUG-Alle",
                                          background="white",
                                          font=SETTINGS_BTN_FONT)
            debug_all_label.grid(row=9, column=0, pady=10, sticky="new")

            def on_debug_all_click():
                DEBUG_MODE_ALL = False

            parent.debug_normel = ctk.CTkCheckBox(frame_system, text_color="white", command=lambda: on_debug_all_click)
            parent.debug_normel.grid(column=1, row=9)
        else:
            logger.debug("Einstellungen nur für Administrator Verfügbar.")
    DBUG_for_Admin(frame_system)

    # Label für die Zoomstufe
    zoom_label = tk.Label(frame_system,
                          text="Anpassen der Zoomstufe",
                          background="white",
                          font=SETTINGS_BTN_FONT)
    zoom_label.grid(row=1, column=1, pady=10, sticky="new")

    # Funktion zur Aktualisierung der Zoomstufe
    def update_zoom(value):
        logger.debug(f"Zoom-Stufe aktualisiert: {value}")

    zoom_control = ctk.CTkSlider(frame_system,
                                 from_=int(0.5),  # Minimaler Zoomfaktor
                                 to=int(2.0),  # Maximaler Zoomfaktor
                                 number_of_steps=15,  # Anzahl der Schritte (optional)
                                 command=lambda value: update_zoom(round(value, 1)))  # Rundung auf 1 Nachkommastelle
    zoom_control.grid(row=2, column=1, pady=10, sticky="ew")
    zoom_control.set(1.0)  # Standard-Zoomfaktor

    # Label für Fehlermeldungen
    info_label = tk.Label(frame_system,
                          text="",
                          background="white",
                          font=SETTINGS_BTN_FONT)
    info_label.grid(row=10, pady=10, column=0)

    #LOGGER PRINT
    logger.debug(f"Complete loading of the 'System' settings page. {['image']}")

    ###############################
    # # L A Y O U T : U E B E R # #
    ###############################

    # Dynamischer Frame mit Einstellungsmöglichkeiten
    frame_ueber = tk.Frame(popup, bg="white")
    frame_ueber.grid(row=1, column=1, rowspan=1, sticky="nsew")
    frame_ueber.grid_columnconfigure(0, weight=1)
    frame_ueber.grid_columnconfigure(1, weight=1)
    frame_ueber.grid_columnconfigure(2, weight=1)
    frame_ueber.grid_rowconfigure(0, weight=1)

    # Ueberschrift erstellen Über das DD-Inv Tool
    ueber_label = tk.Label(frame_ueber,
                           text="Über das DD-Inv Tool",
                           font=SETTINGS_FONT,
                           bg="white")
    ueber_label.grid(row=0, column=0, pady=0, columnspan=3, sticky="new")

    # Unterüberschrift erstellen Credits
    credits_label = tk.Label(frame_ueber,
                             text="Credits",
                             font=SETTINGS_BTN_FONT,
                             bg="white")
    credits_label.grid(row=1, column=0, pady=10, sticky="new")

    # Liste mit den Namenm, URL, Bild fuer Credits
    buttons_data_credits = [{"name": "Peaemer (Jack)", "url": "https://github.com/peaemer/",
                             "image": "https://avatars.githubusercontent.com/u/148626202?v=4"},
                            {"name": "Alex5X5 (Alex)", "url": "https://github.com/Alex5X5",
                             "image": "https://avatars.githubusercontent.com/u/75848461?v=4"},
                            {"name": "GitSchwan (Fabian)", "url": "https://github.com/GitSchwan",
                             "image": "https://avatars.githubusercontent.com/u/173039634?v=4"},
                            {"name": "Chauto (Anakin)", "url": "https://github.com/Chautoo",
                             "image": "https://avatars.githubusercontent.com/u/89986856?v=4"},
                            {"name": "FemRene (Rene)", "url": "https://github.com/FemRene",
                             "image": "https://avatars.githubusercontent.com/u/110292225?v=4"},
                            {"name": "Tam", "url": "", "image": ""}]

    def open_url(url):
        if url:
            webbrowser.open_new_tab(url)
        else:
            logger.error("Fehler beim Laden der URL")

    # Eine Liste, um alle Bilder zu speichern, damit sie im Speicher bleiben
    parent.images_credits = []

    # Erstellen der Buttons mit einer Schleife für die Credits
    for index, button in enumerate(buttons_data_credits, start=2):
        try:
            if button["image"]:
                button_image = loadImage(parent=parent, image=button["image"],
                                         defult_image=resource_path("includes/assets/GitHubSettings.png"), width=48,
                                         height=48)
            else:
                # Optional: Ein Standardbild verwenden, wenn kein Bild angegeben ist
                button_image = tk.PhotoImage(file=resource_path("includes/assets/GitHubSettings.png"))
            parent.images_credits.append(button_image)  # Das Bild in der Liste speichern
            btn_label = ttk.Label(frame_ueber,
                                  text=button["name"],
                                  cursor="hand2",
                                  image=button_image,
                                  compound="left",
                                  background="white")
            btn_label.grid(row=index, column=0, pady=2, padx=15, sticky="new")
            btn_label.bind("<Button-1>", lambda e, url=button["url"]: open_url(url))
        except Exception as e:
            logger.error('test')

    # Unterueberschrift Tools
    build_label = tk.Label(frame_ueber,
                           text="Tools",
                           font=SETTINGS_BTN_FONT,
                           bg="white")
    build_label.grid(row=1, column=1, pady=10, sticky="new")

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

    parent.images_tools = []

    for index, button in enumerate(buttons_data_tools, start=2):
        try:
            button_image = tk.PhotoImage(file=button["image"])
            parent.images_tools.append(button_image)  # Das Bild in der Liste speichern
            btn_label = ttk.Label(frame_ueber,
                                  text=button["name"],
                                  cursor="hand2",
                                  image=button_image,
                                  compound="left",
                                  background="white")
            btn_label.grid(row=index, column=1, pady=2, padx=40, sticky="new")
            btn_label.bind("<Button-1>", lambda e, url=button["url"]: open_url(url))
        except Exception as e:
            logger.error(f"Fehler beim Laden des Bildes {button['image']}: {e}")

    # Unterueberschrift Unterstzütze Uns
    build_label = tk.Label(frame_ueber,
                           text="Unterstütze Uns",
                           font=SETTINGS_BTN_FONT,
                           bg="white")
    build_label.grid(row=1, column=2, pady=10, sticky="new")

    # Liste mit den Namenm, URL, Bild fuer Projekt Unterstuetzen
    buttons_data_support = [{"name": "Ko-Fi", "url": "https://ko-fi.com/dd_inv",
                             "image": resource_path("includes/assets/KoFiSettings.png")},
                            {"name": "Feedback", "url": "mailto:Jack-Mike.Saering@srhk.de",
                             "image": resource_path("includes/assets/FeedbackSettings.png")}]

    parent.images_support = []

    # Erstellen der Buttons mit einer Schleife
    for index, button in enumerate(buttons_data_support, start=2):
        try:
            button_image = tk.PhotoImage(file=button["image"])
            parent.images_support.append(button_image)  # Das Bild in der Liste speichern
            btn_label = ttk.Label(frame_ueber,
                                  text=button["name"],
                                  cursor="hand2",
                                  image=button_image,
                                  compound="left",
                                  background="white")
            btn_label.grid(row=index, column=2, pady=2, padx=15, sticky="new")
            btn_label.bind("<Button-1>",
                           lambda e,
                                  url=button["url"]: open_url(url))
        except Exception as e:
            logger.error(f"Fehler beim Laden des Bildes {button['image']}: {e}")

    # Unterueberschrift Info
    build_label = tk.Label(frame_ueber,
                           text="Info",
                           font=SETTINGS_BTN_FONT,
                           bg="white")
    build_label.grid(row=5, column=2, pady=10, sticky="new")

    # Liste mit den Namenm, URL, Bild fuer Info
    buttons_data_info = [
        {"name": "VersionBuild   V. 0.2 BETA", "url": "https://github.com/peaemer/DD-inv/releases/latest",
         "image": resource_path("includes/assets/DD-Inv_Logo.png")},
        {"name": "GitHub", "url": "https://github.com/peaemer/DD-inv",
         "image": resource_path("includes/assets/GitHubSettings.png")}]

    parent.images_info = []

    # Erstellen der Buttons mit einer Schleife
    for index, button in enumerate(buttons_data_info, start=6):
        try:
            button_image = tk.PhotoImage(file=button["image"])
            parent.images_support.append(button_image)  # Das Bild in der Liste speichern
            btn_label = ttk.Label(frame_ueber,
                                  text=button["name"],
                                  cursor="hand2",
                                  image=button_image,
                                  compound="left",
                                  background="white")
            btn_label.grid(row=index, column=2, pady=2, padx=40, sticky="new")
            btn_label.bind("<Button-1>",
                           lambda e,
                                  url=button["url"]: open_url(url))
        except Exception as e:
            logger.error(f"Error loading the image. {button['image']}: {e}")

    # LOGGER PRINT
    logger.debug(f"Complete loading of the 'About-Us' settings page. {['image']}")

    ###############################
    # # F R A M E : S W I T C H # #
    ###############################

    # Kategorien in der Seitenleiste
    categories = ["Profil",
                  "System",
                  "Über DD-Inv"]

    category_labels_settings = []

    # Zuordnung der Frames zu den Kategorien
    frames = {"Profil": frame_profile,
              "System": frame_system,
              "Über DD-Inv": frame_ueber}

    current_frame = frames["Profil"]  # Halte den aktuell sichtbaren Frame
    current_frame.grid(row=1, column=1, rowspan=1, columnspan=1, sticky="nsew")
    current_frame.columnconfigure(0, weight=1)
    current_frame.columnconfigure(1, weight=1)

    # Funktion zum Anzeigen des Frames
    def show_frame_settings(category):
        logger.debug(f"Aktuell sichtbarer Frame vor Verstecken: {frames}")
        nonlocal current_frame  # Zugriff auf die äußere Variable
        logger.debug(f"current_frame:{current_frame}")
        if current_frame:  # Falls bereits ein Frame angezeigt wird
            current_frame.grid_remove()  # Verstecke den aktuellen Frame
            logger.debug(f"frame:{current_frame}")
        new_frame = frames.get(category)
        logger.debug(f"new_frame after creation:{new_frame}")
        if new_frame:  # Wenn der neue Frame existiert
            new_frame.grid(row=1, column=1, rowspan=1, sticky="nsew")
            new_frame.columnconfigure(0, weight=1)
            new_frame.rowconfigure(0, weight=0)
            current_frame = new_frame
            logger.debug(f"New current_frame: {current_frame}")

    # Funktion für Klick auf Kategorie
    def on_category_click_settings(label_settings, category_settings):
        update_header_icon(category_settings)
        # Setze alle Labels zurück
        for cat in category_labels_settings:
            cat.config(fg="white")
            logger.debug("if on_category_click")
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
                         font=SETTINGS_BTN_FONT,
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

    #LOGGER PRINT
    logger.debug(f"Fully load the switch to switch between the settings pages. {['image']}")
