from ..sec_data_info.UserSecurity import set_password
from .settingsWindow import *
import cache
from ._styles import *

logger:Logger = Logger('customMessageBoxResetPasswrd')


def customMessageBoxResetPasswrd(parent, title, message, calb = None):
    passwrd_msg_box = tk.Toplevel(parent)
    passwrd_msg_box.title(title)
    passwrd_msg_box.transient(parent)  # Popup bleibt im Vordergrund des Hauptfensters
    passwrd_msg_box.grab_set()  # Blockiere Interaktionen mit dem Hauptfenster
    passwrd_msg_box.attributes('-topmost', 0)
    passwrd_msg_box.configure(background="white")

    # Bildschirmbreite und -höhe ermitteln
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Fensterbreite und -höhe definieren
    window_width = 300
    window_height = 330

    # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    passwrd_msg_box.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    passwrd_msg_box.resizable(False, False)

    try:
        passwrd_msg_box.iconbitmap("includes/assets/srhIcon.ico")
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")

    # def zum Umschalten der Passwortsichtbarkeit
    parent.see_pw = False
    def toggle_password(true=True):
        if parent.see_pw:
            msg_passwrd_first.configure(show="•")  # Zeichen durch Punkte verdecken
            msg_passwrd_second.configure(show="•")  # Zeichen durch Punkte verdecken
            toggle_button.configure(text="Passwort anzeigen")
            parent.see_pw = False
        else:
            msg_passwrd_first.configure(show="")  # Zeichen sichtbar machen
            msg_passwrd_second.configure(show="")  # Zeichen sichtbar machen
            toggle_button.configure(text="Passwort verstecken")
            parent.see_pw = true

    # def zum Abmelden des Benutzers
    def log_out_box():
        """
        Zeigt die Einstellungs-Popup-Funktionalität an und erlaubt es dem Benutzer, sich auszuloggen.

        :param parent: Das Eltern-Widget, das als Basis für das Popup-Fenster dient.
        :type parent: widget
        :param controller: Der Controller, der für die Navigation und Zustandsverwaltung der Anwendung
                            verantwortlich ist.
        :type controller: Controller-Klasse
        """
        try:
            if msg_passwrd_first.get() and len(msg_passwrd_first.get()) >= 8:

                set_password(cache.selected_ID, msg_passwrd_first.get(),msg_passwrd_second.get())
                from includes.pages import logInWindow
                cache.user_group = None  # Benutzergruppe zurücksetzen
                cache.user_name = None
                cache.user = None
                passwrd_msg_box.destroy()
                calb()
            else:
                return (info_label.config(text="Das Passwort muss mind. 8 Zeichen lang sein!"),)

        except Exception as e:
            logger.error(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: Error during logout by the user. {e}")

    passwrd_msg = tk.Frame(passwrd_msg_box, background="white")
    passwrd_msg.grid(row=0,
                     column=0,
                     columnspan=1,
                     sticky="nesw")

    msg = ctk.CTkLabel(passwrd_msg,
                       text=message,
                       text_color="black",
                       font=("Arial", 20),
                       justify="center")
    msg.grid(row=0, column=0, padx=15, pady=5, sticky="nesw", columnspan=2)

    #1. Feld für das eintragen des Passwortes
    msg_passwrd_first = ctk.CTkLabel(passwrd_msg,
                                     text="Bitte Passwort eingeben:",
                                     text_color="black",
                                     font=("Arial", 20),
                                     justify="center")
    msg_passwrd_first.grid(row=1, column=0, padx=15, pady=5, sticky="nesw", columnspan=2)

    msg_passwrd_first = ctk.CTkEntry(passwrd_msg,
                                     fg_color=srhGrey,
                                     border_width=0,
                                     text_color="black",
                                     show="•",
                                     corner_radius=corner,
                                     font=("Arial", 20),
                                     justify="center")
    msg_passwrd_first.grid(row=2, column=0, padx=15, pady=5, sticky="nesw", columnspan=2)

    #2. Feld zum wiederholen des Passwortes
    msg_passwrd_second = ctk.CTkLabel(passwrd_msg,
                                      text="Bitte Passwort wiederholen:",
                                      text_color="black",
                                      font=("Arial", 20),
                                      justify="center")
    msg_passwrd_second.grid(row=3, column=0, padx=15, pady=5, sticky="nesw", columnspan=2)

    msg_passwrd_second = ctk.CTkEntry(passwrd_msg,
                                      fg_color=srhGrey,
                                      border_width=0,
                                      corner_radius=corner,
                                      show="•",
                                      text_color="black",
                                      font=("Arial", 20),
                                      justify="center")
    msg_passwrd_second.grid(row=4, column=0, padx=15, pady=5, sticky="nesw", columnspan=2)

    #Btn zum Aufdecken des Passwortes
    toggle_button = ctk.CTkButton(passwrd_msg,
                                  text="Passwort anzeigen",
                                  border_width=0,
                                  fg_color=srhGrey,
                                  text_color="black",
                                  command=toggle_password)
    toggle_button.grid(row=5, column=0, padx=30, pady=10, sticky="ew", columnspan=2)

    # Label für Fehlermeldungen
    info_label = tk.Label(passwrd_msg,
                          text="",
                          background="white",
                          font=("Arial", 10))
    info_label.grid(row=6, pady=5, sticky="ew", columnspan=2)

    #Btn zum Bestätigen
    accpt = ctk.CTkButton(passwrd_msg,
                          text="Bestätigen",
                          border_width=0,
                          fg_color=srhOrange,
                          text_color="white",
                          command=log_out_box)
    accpt.grid(row=7, column=0, padx=0, pady=10)


    #Btn zum Abbrechen
    cancel = ctk.CTkButton(passwrd_msg,
                           text="Abbrechen",
                           border_width=0,
                           fg_color=srhGrey,
                           text_color="black",
                           command=passwrd_msg_box.destroy)
    cancel.grid(row=7, column=1, padx=0, pady=10)

    passwrd_msg.grid_rowconfigure(0, weight=1)
    passwrd_msg.grid_rowconfigure(1, weight=1)
    passwrd_msg.grid_rowconfigure(2, weight=1)
    passwrd_msg.grid_rowconfigure(3, weight=1)
    passwrd_msg.grid_rowconfigure(4, weight=1)
    passwrd_msg.grid_rowconfigure(5, weight=1)
    passwrd_msg.grid_rowconfigure(6, weight=1)
    passwrd_msg.grid_rowconfigure(7, weight=1)
    passwrd_msg.grid_columnconfigure(0, weight=1)
    passwrd_msg.grid_columnconfigure(1, weight=1)
    passwrd_msg.grid_columnconfigure(2, weight=1)
    passwrd_msg.grid_columnconfigure(3, weight=1)
