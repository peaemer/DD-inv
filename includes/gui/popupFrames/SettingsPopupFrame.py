"""
    .
"""
import copy
import tkinter
from enum import Enum
from typing import override, Callable

import customtkinter

from includes.logic import ImageLoader, SettingsBindings
from includes.windows import _avatarManager
from main import DDInv
from includes.util import Paths
from includes.gui.styles import *
from includes.util.Logging import Logger
from includes.gui.pages.IPage import IPage


logger:Logger = Logger('Settings Popup Frame')

class WindowState(Enum):
    """
        a placeholder for the current window type
    """
    PROFILE = 0
    SYSTEM = 1
    CREDITS = 2

class SettingsPopupFrame(IPage):
    """
        .
    """

    def __init__(self, parent:tkinter.Frame, controller:DDInv, admin_mode:bool):
        """
            .
        """
        super().__init__(parent, controller, admin_mode=admin_mode)
        self.__parent = parent
        self.__window_state = WindowState.PROFILE
        self.category_icons:dict[WindowState, tuple[tkinter.PhotoImage, str]] = {
            WindowState.PROFILE: (tkinter.PhotoImage(file=Paths.assets_path("ProfileSettingsIcon.png")), 'Dein Profil'),
            WindowState.SYSTEM: (tkinter.PhotoImage(file=Paths.assets_path("SystemSettingsIcon.png")), 'System'),
            WindowState.CREDITS: (tkinter.PhotoImage(file=Paths.assets_path("Tool.png")), 'Über DD-Inv')
        }
        self.hader_bar_icon:tkinter.PhotoImage = self.category_icons[self.__window_state][0]
        self.hader_bar_icon_label: tkinter.Label | None = None
        self.hader_bar_text_label: tkinter.Label | None = None

        self.credit_links_buttons:list[dict[str, str | customtkinter.CTkButton | tkinter.PhotoImage | tkinter.Label | None]] = [
            {'name':'Peaemer (Jack)', 'url':'https://github.com/peaemer', 'icon_url':'https://avatars.githubusercontent.com/u/148626202?v=4'},
            {'name':'Alex5X5 (Alex)', 'url':'https://github.com/Alex5X5', 'icon_url':'https://avatars.githubusercontent.com/u/75848461?v=4'},
            {'name':'GitSchwan (Fabian)', 'url':'https://github.com/GitSchwan', 'icon_url':'https://avatars.githubusercontent.com/u/173039634?v=4'},
            {'name':'Chauto (Anakin)', 'url':'https://github.com/Chautoo', 'icon_url': 'https://avatars.githubusercontent.com/u/89986856?v=4'},
            {'name':'FemRene (Rene)', 'url':'https://github.com/FemRene', 'icon_url': 'https://avatars.githubusercontent.com/u/110292225?v=4'},
      #      {'name':'Tam', 'url':'', 'icon_url':''}
        ]
        self.after(1000,self.switch_to_credits)
        #self.switch_to_credits()


    # def zum aendern des Icons im Header bassierend auf der angezeiten Seite
    # def update_header_icon(self):
    #     """."""
    #     try:
    #         """Aktualisiert das Header-Icon basierend auf der ausgewählten Kategorie."""
    #         # Wähle das passende Icon basierend auf der Kategorie
    #         # new_icon = category_icons.get(categories)
    #         for cat in category_icons:
    #             if cat == categorie:
    #                 new_icon = category_icons.get(cat)
    #                 header_label.configure(image=new_icon)
    #                 header_label.image = new_icon  # Verhindert, dass das Bild von der Garbage Collection gelöscht wird.
    #
    #     except Exception as e:
    #         logger.error(f"Error when loading or changing the icon in the heading area. {button['image']}: {e}")

    @override
    def on_load(self) -> None:
        pass

    @override
    def setup_header_bar(self, frame: tkinter.Frame) -> None:
        frame.grid_rowconfigure(0, weight=4)
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=0)
        frame.grid_rowconfigure(4, weight=4)

        self.hader_bar_icon_label = tkinter.Label(
            frame,
            image=self.category_icons[self.__window_state][0],
            foreground="white",
            background=srh_grey
        )

        self.header_bar_text_label = tkinter.Label(
            frame,
            text=self.category_icons[self.__window_state][1],
            foreground="white",
            background=srh_grey
        )

        self.hader_bar_icon_label.grid(row=0, column=1, sticky='E')

        # for i in range(len(self.credit_links_buttons)):
        #    # self.credit_links_buttons[i] = (tkinter.Button(), tkinter.PhotoImage(file=self.credit_links_buttons[i][3]))
        #    self.credit_links_buttons[i]['icon'] = ImageLoader.load_image(self.credit_links_buttons[i]['icon'])
        #    self.credit_links_buttons[i]['label']



    def switch_to_system(self):
        pass

    def switch_to_profile(self):
        pass


    def switch_to_credits(self):
        for i in range(0,3,1):
            #self.credit_links_buttons[i]['button'].grid(row=i + 1, column=1, rowspan=2, columnspan=2, sticky="nsew")
            self.credit_links_buttons[i]['icon_label'].grid(row=i*2, column=2, rowspan=1, columnspan=2, sticky="nsew")
            self.credit_links_buttons[i]['name_label'].grid(row=i*2+1, column=1, rowspan=1, columnspan=4, sticky="nsew")
        for i in range(3,5):
            #self.credit_links_buttons[i]['button'].grid(row=i + 1, column=1, rowspan=2, columnspan=2, sticky="nsew")
            self.credit_links_buttons[i]['icon_label'].grid(row=i*2-6, column=7, rowspan=1, columnspan=2, sticky="nsew")
            self.credit_links_buttons[i]['name_label'].grid(row=i*2-5, column=6, rowspan=1, columnspan=4, sticky="nsew")

        pass
        #
        # for i in range(0,5):
        #     self.credit_links_buttons[i]['button'].grid(row=i + 1, column=4, rowspan=2, columnspan=2, sticky="nsew")
        #     self.credit_links_buttons[i]['label'].grid(row=i + 3, column=4, rowspan=1, columnspan=2, sticky="nsew")
        #
        # for i in range(0,2):
        #     self.credit_links_buttons[i]['button'].grid(row=i + 1, column=7, rowspan=2, columnspan=2, sticky="nsew")
        #     self.credit_links_buttons[i]['label'].grid(row=i + 3, column=7, rowspan=1, columnspan=2, sticky="nsew")
        #
        # # Erstellen der Buttons mit einer Schleife für die Credits
        # for i in range(0,5):
        #     self.credit_links_buttons[i]['button'].grid(row=i + 1, column=1, columnspan=1, sticky="nsew")
        #
        # for i in range(0,5):
        #     try:
        #         if not self.credit_links_buttons[i]['image']:
        #             self.credit_links_buttons[i]['image icon']=ImageLoader.load_image(self.credit_links_buttons[i]['image'])
        #         if not self.credit_links_buttons[i]['button']:
        #             self.credit_links_buttons[i]['button']=customtkinter.CTkButton()
        #
    #            else:
    #                # Optional: Ein Standardbild verwenden, wenn kein Bild angegeben ist
    #                button_image = tkinter.PhotoImage(file=resource_path("includes/assets/GitHubSettings.png"))
    #             parent.images_credits.append(button_image)  # Das Bild in der Liste speichern
    #             btn_label = tkinter.Label(frame_ueber,
    #                                  text=button['name'],
    #                                  cursor="hand2",
    #                                  image=button_image,
    #                                  compound="top",
    #                                  font=SETTINGS_ABOUT_FONT,
    #                                  background="white"
    #                                  )
    #             btn_label.grid(row=index, column=0, pady=1, sticky="nsew")
    #             btn_label.bind("<Button-1>", lambda e, url=button["url"]: open_url(url))
    #         except Exception as e:
    #             logger.error('Error while loading images for Credits.')
    #
    #
    #     def open_url(url):
    #         if url:
    #             webbrowser.open_new_tab(url)
    #         else:
    #             logger.error("Error loading the URL.")
    #
    #     # Eine Liste, um alle Bilder zu speichern, damit sie im Speicher bleiben
    #     parent.images_credits = []
    #
    #
    #     for index, button in enumerate(buttons_data_credits, start=2):
    #
    #     # Unterueberschrift Tools
    #     build_label = tkinter.Label(frame_ueber,
    #                            text="Tools",
    #                            font=SETTINGS_FONT,
    #                            bg="white"
    #                            )
    #     build_label.grid(row=1, column=1, pady=5, sticky="nesw")
    #
    #     # Liste mit den Namenm, URL, Bild fuer genutzte Tools
    #     buttons_data_tools = [
    #         {'name': "SQL3',  'url':  'https://www.sqlite.org/",
    #          "image": resource_path("includes/assets/SQL3Settings.png")},
    #         {'name': "Figma',  'url':  'https://www.figma.com/",
    #          "image": resource_path("includes/assets/FigmaSettings.png")},
    #         {'name': "PyCharm',  'url':  'https://www.jetbrains.com/de-de/pycharm/",
    #          "image": resource_path("includes/assets/PyCharmSettings.png")},
    #         {'name': "Python',  'url':  'https://www.python.org/",
    #          "image": resource_path("includes/assets/PythonSettings.png")},
    #         {'name': "WindowsXP',  'url':  'https://gist.github.com/rolfn/1a05523cfed7214f4ad27f0a4ae56b07",
    #          "image": resource_path("includes/assets/WindowsXPSettings.png")}
    #     ]
    #
    #     parent.images_tools = []
    #
    #     for index, button in enumerate(buttons_data_tools, start=2):
    #         try:
    #             button_image = tkinter.PhotoImage(file=button["image"])
    #             parent.images_tools.append(button_image)  # Das Bild in der Liste speichern
    #             btn_label = tkinter.Label(frame_ueber,
    #                                  text=button['name'],
    #                                  cursor="hand2",
    #                                  image=button_image,
    #                                  font=SETTINGS_ABOUT_FONT,
    #                                  compound="top",
    #                                  background="white"
    #                                  )
    #             btn_label.grid(row=index, column=1, pady=1, sticky="nesw")
    #             btn_label.bind("<Button-1>", lambda e, url=button["url"]: open_url(url))
    #         except Exception as e:
    #             logger.error(f"Error while trying to load the {button['image']}: {e}")
    #
    #     # Unterueberschrift Unterstzütze Uns
    #     build_label = tkinter.Label(frame_ueber,
    #                            text="Unterstütze Uns",
    #                            font=SETTINGS_FONT,
    #                            bg="white"
    #                            )
    #     build_label.grid(row=1, column=2, pady=5, sticky="nesw")
    #
    #     # Liste mit den Namenm, URL, Bild fuer Projekt Unterstuetzen
    #     buttons_data_support = [
    #         {'name': "Ko-Fi',  'url':  'https://ko-fi.com/dd_inv",
    #          "image": resource_path("includes/assets/KoFiSettings.png")},
    #         {'name': "Feedback',  'url':  'mailto:Jack-Mike.Saering@srhk.de",
    #          "image": resource_path("includes/assets/FeedbackSettings.png")}
    #     ]
    #
    #     parent.images_support = []
    #
    #     # Erstellen der Buttons mit einer Schleife
    #     for index, button in enumerate(buttons_data_support, start=2):
    #         try:
    #             button_image = tkinter.PhotoImage(file=button["image"])
    #             parent.images_support.append(button_image)  # Das Bild in der Liste speichern
    #             btn_label = tkinter.Label(frame_ueber,
    #                                  text=button['name'],
    #                                  cursor="hand2",
    #                                  image=button_image,
    #                                  font=SETTINGS_ABOUT_FONT,
    #                                  compound="top",
    #                                  background="white"
    #                                  )
    #             btn_label.grid(row=index, column=2, pady=1, sticky="nesw")
    #             btn_label.bind("<Button-1>",
    #                            lambda e,
    #                                   url=button["url"]: open_url(url)
    #                            )
    #         except Exception as e:
    #             logger.error(f"Error while trying to load the {button['image']}: {e}")
    #
    #     # Unterueberschrift Info
    #     build_label = tkinter.Label(frame_ueber,
    #                            text="Info",
    #                            font=SETTINGS_FONT,
    #                            bg="white"
    #                            )
    #     build_label.grid(row=4, column=2, sticky="nesw")
    #
    #     # Liste mit den Namenm, URL, Bild fuer Info
    #     buttons_data_info = [
    #         {'name': "VersionBuild   V. 1.2 STABLE',  'url':  'https://github.com/peaemer/DD-inv/releases/latest",
    #          "image": resource_path("includes/assets/DD-Inv_Logo.png")},
    #         {'name': "GitHub',  'url':  'https://github.com/peaemer/DD-inv",
    #          "image": resource_path("includes/assets/GitHubSettings.png")}
    #     ]
    #
    #     parent.images_info = []
    #
    #     # Erstellen der Buttons mit einer Schleife
    #     for index, button in enumerate(buttons_data_info, start=5):
    #         try:
    #             button_image = tkinter.PhotoImage(file=button["image"])
    #             parent.images_support.append(button_image)  # Das Bild in der Liste speichern
    #             btn_label = tkinter.Label(frame_ueber,
    #                                  text=button['name'],
    #                                  cursor="hand2",
    #                                  image=button_image,
    #                                  font=SETTINGS_ABOUT_FONT,
    #                                  compound="top",
    #                                  background="white"
    #                                  )
    #             btn_label.grid(row=index, column=2, pady=1, sticky="nesw")
    #             btn_label.bind("<Button-1>",
    #                            lambda e,
    #                                   url=button["url"]: open_url(url)
    #                            )
    #         except Exception as e:
    #             logger.error(f"Error loading the image. {button['image']}: {e}")
    #
    #     # LOGGER PRINT
    #     logger.debug(f"Complete loading of the 'About-Us' settings page. {['image']}")
    #
    #     ###########################
    #     # F R A M E : S W I T C H #
    #     ###########################
    #
    #     # Kategorien in der Seitenleiste
    #     categories = [
    #         "Profil",
    #         "System",
    #         "Über-DD-Inv"
    #     ]
    #
    #     category_labels_settings = []
    #
    #     # Zuordnung der Frames zu den Kategorien
    #     frames = {
    #         "Profil": frame_profile,
    #         "System": frame_system,
    #         "Über-DD-Inv": frame_ueber
    #     }
    #
    #     current_frame = frames["Profil"]  # Halte den aktuell sichtbaren Frame
    #     current_frame.grid(row=1, column=1, rowspan=1, columnspan=1, sticky="nsew")
    #     current_frame.columnconfigure(0, weight=1)
    #     current_frame.columnconfigure(1, weight=1)
    #
    #
    @override
    def setup_side_bar_right(self, frame: tkinter.Frame) -> bool:
        return False

    @override
    def setup_side_bar_left(self, frame: tkinter.Frame) -> bool:
        return True

    @override
    def setup_main_frame(self, frame:tkinter.Frame) -> None:

        frame.grid_rowconfigure(0, weight=0)  # Bereich fuer Kategorien
        frame.grid_rowconfigure(1, weight=1)  # Hauptbereich
        frame.grid_columnconfigure(0, weight=0)  # Seitenleiste
        frame.grid_columnconfigure(1, weight=1)  # Hauptinhalt

        for i in range(0,17): frame.grid_rowconfigure(i, weight=1)
        for i in range(0,13): frame.grid_columnconfigure(i, weight=1)

        for data in self.credit_links_buttons:
            data.update(
                {
                    'name_label': tkinter.Label(
                        frame,
                        text=data['name'],
                        font=SETTINGS_BTN_FONT,
                        bg="white"
                    )
                }
            )
            data.update(
                {
                    'icon_label':tkinter.Label(
                        frame,
                        font=SETTINGS_BTN_FONT,
                        bg='green'
                    )
                }
            )
            data.update(
                {
                    'icon': _avatarManager.loadImage(
                        parent=data['icon_label'],
                        image=data['icon_url'],
                        defult_image=Paths.assets_path('GitHubSettings.png'),
                        width=48,
                        height=48
                    )
                }
            )
            logger.debug(f'label:{data['icon_label']}')
            logger.debug(f'icon_url:{data['icon_url']}')
            logger.debug(f'icon:{data['icon']}')
            data['icon_label'].configure(image=data['icon'])
            # data['icon_label'].__setattr__('url',data['url'])
            data['icon_label'].bind("<Button-1>",lambda _, url_ = data['url']: SettingsBindings.open_url(url_))
            logger.debug(f"""binding  button url {data['icon_label'].url}""")

        for i in range(0,len(self.credit_links_buttons)):

            logger.debug('creating button')
            #self.credit_links_buttons[i]['icon']=ImageLoader.load_image(self.credit_links_buttons[i]['icon_url'])
            self.credit_links_buttons[i].update(
                {
                    'name_label': tkinter.Label(
                        frame,
                        text=self.credit_links_buttons[i]['name'],
                        font=SETTINGS_BTN_FONT,
                        bg="white"
                    )
                }
            )
            self.credit_links_buttons[i].update(
                {
                    'icon_label':tkinter.Label(
                        frame,
                        font=SETTINGS_BTN_FONT,
                        bg='green'
                    )
                }
            )
            self.credit_links_buttons[i].update(
                {
                    'icon': _avatarManager.loadImage(
                        parent=self.credit_links_buttons[i]['icon_label'],
                        image=self.credit_links_buttons[i]['icon_url'],
                        defult_image=Paths.assets_path('GitHubSettings.png'),
                        width=48,
                        height=48
                    )
                }
            )
            logger.debug(f'label:{self.credit_links_buttons[i]['icon_label']}')
            logger.debug(f'icon_url:{self.credit_links_buttons[i]['icon_url']}')
            logger.debug(f'icon:{self.credit_links_buttons[i]['icon']}')
            self.credit_links_buttons[i]['icon_label'].configure(image=self.credit_links_buttons[i]['icon'])
            self.credit_links_buttons[i]['icon_label'].__setattr__('url',copy.copy(self.credit_links_buttons[i]['url']))
            self.credit_links_buttons[i]['icon_label'].bind("<Button-1>",lambda _: SettingsBindings.open_url(self.credit_links_buttons[i]['icon_label'].url))
            logger.debug(f"""binding  button url {self.credit_links_buttons[i]['icon_label'].url}""")
        logger.debug(f'credit content:{self.credit_links_buttons}')
        logger.debug(f"Complete loading of the 'Main' settings page. {['image']}")
    #
    #     ###################################
    #     # # L A Y O U T : P R O F I L E # #
    #     ###################################
    #
    #     # Überschrift Dein Profil
    #     profile_btn_label = tkinter.Label(frame,
    #                                  text="Dein Profil",
    #                                  font=SETTINGS_FONT,
    #                                  bg="white"
    #                                  )
    #     profile_btn_label.grid(row=0, column=0, pady=0, columnspan=3, sticky="new")
    #
    #     # Profilbild zum Laden importieren
    #     parent.avatar = cache.user_avatarx128
    #     parent.settings_img_label = tkinter.Label(frame,
    #                                          image=parent.avatar,
    #                                          background="white"
    #                                          )
    #     parent.settings_img_label.grid(row=1, column=0, pady=5, rowspan=2, columnspan=1, sticky="nesw")
    #
    #     # Schriftzug Eingeloggt als
    #     profile_btn_label = tkinter.Label(frame,
    #                                  text="Eingeloggt als\n" + cache.user_name,
    #                                  font=SETTINGS_BTN_FONT,
    #                                  bg="white"
    #                                  )
    #     profile_btn_label.grid(row=3, column=0, padx=20, pady=5, rowspan=1, sticky="nesw")
    #
    #     # Schriftzug Rechte in der Gruppe
    #     profile_btn_label = tkinter.Label(frame,
    #                                  text="Rechte des Users\n" + cache.user_group,
    #                                  font=SETTINGS_BTN_FONT,
    #                                  bg="white"
    #                                  )
    #     profile_btn_label.grid(row=4, column=0, padx=20, pady=5, sticky="nesw")
    #
    #     # Schriftzug E-Mail-Adresse
    #     profile_btn_label = tkinter.Label(frame,
    #                                  text="E-Mail-Adressse\n" + load_user_email(cache.user_name),
    #                                  font=SETTINGS_BTN_FONT,
    #                                  bg="white"
    #                                  )
    #     profile_btn_label.grid(row=5, column=0, padx=20, pady=5, sticky="nesw")
    #
    #     # Eingabe für die Profilbild-URL
    #     profile_image_url_label = tkinter.Label(frame,
    #                                        text="Profilbild-URL / Base64 eingeben",
    #                                        font=SETTINGS_BTN_FONT,
    #                                        bg="white",
    #                                        anchor="w"
    #                                        )
    #     profile_image_url_label.grid(row=1, column=1, sticky="n")
    #
    #     profile_image_url = ctkinter.CTkEntry(frame,
    #                                      border_width=border,
    #                                      corner_radius=corner,
    #                                      text_color="black",
    #                                      fg_color=srh_grey,
    #                                      font=SETTINGS_FONT,
    #                                      width=250
    #                                      )
    #     profile_image_url.grid(row=2, column=1, columnspan=1, pady=5, sticky="n")
    #
    #     # Importieren der Funktion URL
    #     from ._avatarManager import loadImage
    #
    #     # Laden des Bildes für Profile Btn
    #     parent.btn_image_set_profile_picture_settings = tkinter.PhotoImage(
    #         file=Paths.assets_path("SetProfileSettings.png"))
    #
    #     # Label für Fehlermeldungen
    #     info_label_profile = tkinter.Label(frame,
    #                                   text="",
    #                                   background="white",
    #                                   font=error_red
    #                                   )
    #     info_label_profile.grid(row=2, pady=10, column=1, sticky="sew")
    #
    #     def setAvatar():
    #         try:
    #             cache.user_avatarx128 = loadImage(parent=parent, image=profile_image_url.get(), width=128, height=128)
    #             parent.avatar_new = cache.user_avatarx128
    #             cache.user_avatar = loadImage(parent=parent, image=profile_image_url.get(), width=48, height=48)
    #             parent.avatar = cache.user_avatar
    #             db.upsert_avatar(cache.user_name, profile_image_url.get())
    #             parent.settings_img_label.configure(image=parent.avatar_new)
    #             from .MainPage import MainPage
    #             MainPage.update_profile_picture()
    #
    #         except Exception as e:
    #             logger.error(f"Error while applying the profile picture. {button['image']}: {e}")
    #             info_label_profile.config(text="Bitte eine valide URL oder Base64 eingeben.")
    #             info_label_profile.config(text="Eingabe ungültig.")
    #
    #     # Button zum Aktualisieren des Profilbilds
    #     update_image_button = tkinter.Button(frame,
    #                                     text="Profilbild setzen",
    #                                     image=parent.btn_image_set_profile_picture_settings,
    #                                     bg="white",
    #                                     activebackground="white",
    #                                     borderwidth=0,
    #                                     cursor="hand2",
    #                                     command=lambda: setAvatar()
    #                                     )
    #     update_image_button.grid(row=3, column=1, sticky="nesw")
    #
    #     # def zum Abmelden des Benutzers
    #     global cotr
    #     contr: controller = controller
    #
    #     def log_out_settings(controller: controller):
    #         """
    #         Zeigt die Einstellungs-Popup-Funktionalität an und erlaubt es dem Benutzer, sich auszuloggen.
    #
    #         :param parent: Das Eltern-Widget, das als Basis für das Popup-Fenster dient.
    #         :type parent: widget
    #         :param controller: Der Controller, der für die Navigation und Zustandsverwaltung der Anwendung
    #                            verantwortlich ist.
    #         :type controller: Controller-Klasse
    #         """
    #         try:
    #             from .LoginWindow_ import LoginWindow__
    #             cache.user_group = None  # Benutzergruppe zurücksetzen
    #             contr.show_frame(LoginWindow__)
    #             popup.destroy()
    #
    #         except Exception as e:
    #             print(f"{debug_ANSI_style}DEBUG{ANSI_style_END}: Error during logout by the user. {e}")
    #
    #     # Laden des Bildes auf dem Passwort Btn
    #     parent.btn_image_password = tkinter.PhotoImage(file=Paths.assets_path("ResetPasswordSettings.png"))
    #
    #     # Schriftzug Passwort ändern
    #     cache.controller = controller
    #     profile_btn_label = tkinter.Button(frame,
    #                                   command=lambda: customMessageBoxResetPasswrd(parent=parent,
    #                                                                                title="Passwort ändern",
    #                                                                                message="Passwort ändern",
    #                                                                                calb=lambda: log_out_settings(
    #                                                                                    controller)),
    #                                   text="Passwort ändern",
    #                                   font=SETTINGS_BTN_FONT,
    #                                   bg="white",
    #                                   activebackground="white",
    #                                   cursor="hand2",
    #                                   image=parent.btn_image_password,
    #                                   borderwidth=0
    #                                   )
    #     profile_btn_label.grid(row=4, column=1, pady=35, sticky="nesw")
    #
    #     # PNG-Bild für Btn
    #     def load_button_images_profile():
    #         """
    #         Lädt und gibt das Bild einer Schaltfläche für die Abmeldung des Benutzers zurück.
    #
    #         Dieses Bild kann in einer GUI verwendet werden, um eine konsistente Darstellung
    #         der Benutzeroberfläche zu gewährleisten.
    #
    #         :return: Das Bild der Schaltfläche als `tkinter.PhotoImage` Objekt.
    #         :rtype: tkinter.PhotoImage
    #         """
    #         btn_image_logout = tkinter.PhotoImage(file=Paths.assets_path("BenutzerAbmeldenSettings.png"))
    #         return btn_image_logout
    #
    #     # Laden des Bildes auf den Abmelden Btn
    #     parent.btn_image_logout = load_button_images_profile()
    #
    #     # Schriftzug Benutzer Abmelden
    #     profile_btn_label = tkinter.Button(frame,
    #                                   command=lambda: log_out_settings(controller),
    #                                   text="Benutzer Abmelden",
    #                                   font=SETTINGS_BTN_FONT,
    #                                   bg="white",
    #                                   activebackground="white",
    #                                   cursor="hand2",
    #                                   image=parent.btn_image_logout,
    #                                   borderwidth=0
    #                                   )
    #     profile_btn_label.grid(row=5, column=1, sticky="nesw")
    #
    #     # LOGGER PRINT
    #     logger.debug(f"Complete loading of the 'Profile' settings page. {['image']}")
    #
    #     #################################
    #     # # L A Y O U T : S Y S T E M # #
    #     #################################
    #
    #     # Dynamischer Frame mit Einstellungsmöglichkeiten
    #     frame_system = tkinter.Frame(popup, bg="white")
    #     frame_system.grid(row=1, column=1, rowspan=1, sticky="nsew")
    #     frame_system.grid_columnconfigure(0, weight=1)
    #     frame_system.grid_columnconfigure(1, weight=1)
    #     frame_system.grid_rowconfigure(0, weight=1)
    #     for i in range(1, 11):
    #         frame_system.grid_rowconfigure(i, weight=0)
    #
    #     # Überschrift System erstellen
    #     radiobutton_label = tkinter.Label(frame_system,
    #                                  text="System",
    #                                  font=SETTINGS_FONT,
    #                                  bg="white"
    #                                  )
    #     radiobutton_label.grid(row=0, column=0, pady=0, columnspan=3, sticky="new")
    #
    #     # Überschrift Auflösung ändern
    #     button_bg_label = tkinter.Label(frame_system,
    #                                text="Auflösung anpassen",
    #                                font=SETTINGS_BTN_FONT,
    #                                bg="white"
    #                                )
    #     button_bg_label.grid(row=1, column=0, pady=10, sticky="new")
    #
    #     def fenster_groesse_aendern(parent):
    #         breite = breite_entry.get()
    #         hoehe = hoehe_entry.get()
    #         if breite.isdigit() and hoehe.isdigit():  # Überprüfen, ob die Eingaben Zahlen sind
    #             config: Configuration = config_manager.generate_configuration('Fenster Aufloesung')
    #             config.write_parameter('hoehe', hoehe)
    #             config.write_parameter('breite', breite)
    #             info_label_system.config(text="Einstellung wird gespeichert und App geschlossen...")
    #             parent.after(3000, close_app)  # Verzögerung von 3 Sekunden und dann Neustart
    #         else:
    #             info_label_system.config(text="Bitte gültige Zahlen eingeben.")
    #
    #     # Eingabefelder fuer Breite
    #     breite_label = tkinter.Label(frame_system,
    #                             text="Breite",
    #                             background="white",
    #                             font=SETTINGS_BTN_FONT
    #                             )
    #     breite_label.grid(row=2, column=0, pady=3)
    #
    #     breite_entry = ctkinter.CTkEntry(frame_system,
    #                                 corner_radius=20,
    #                                 fg_color=srh_grey,
    #                                 text_color="black",
    #                                 font=SETTINGS_BTN_FONT,
    #                                 placeholder_text="z.B. 1920",
    #                                 border_width=0
    #                                 )
    #     breite_entry.grid(row=3, column=0, pady=3)
    #
    #     # Eingabefeld fuer Hoehe
    #     hoehe_label = tkinter.Label(frame_system,
    #                            text="Höhe",
    #                            background="white",
    #                            font=SETTINGS_BTN_FONT
    #                            )
    #     hoehe_label.grid(row=4, column=0, pady=3)
    #
    #     hoehe_entry = ctkinter.CTkEntry(frame_system,
    #                                corner_radius=20,
    #                                fg_color=srh_grey,
    #                                text_color="black",
    #                                font=SETTINGS_BTN_FONT,
    #                                placeholder_text="z.B. 1080",
    #                                border_width=0
    #                                )
    #     hoehe_entry.grid(row=5, column=0, pady=7)
    #
    #     # Button zur Bestätigung
    #     parent.set_res_btn = tkinter.PhotoImage(file=Paths.assets_path("SetResSettings.png"))
    #     aendern_button = tkinter.Button(frame_system,
    #                                image=parent.set_res_btn,
    #                                borderwidth=0,
    #                                cursor="hand2",
    #                                activebackground="white",
    #                                background="white",
    #                                command=lambda: fenster_groesse_aendern(parent)
    #                                )
    #     aendern_button.grid(row=6, pady=5, column=0)
    #
    #     # DBUG-Modus als Einstellung für Admins
    #     def DBUG_for_Admin(parent):
    #         if cache.user_group_data['ADMIN_FEATURE'] == "True":
    #             # Schriftzug DEBUG-Modus aktivieren / deaktivieren
    #             zoom_label = tkinter.Label(frame_system,
    #                                   text="DEBUG-Modus aktivieren / deaktivieren",
    #                                   background="white",
    #                                   font=SETTINGS_BTN_FONT
    #                                   )
    #             zoom_label.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")
    #
    #             # Checkbox DEBUG NORMAL
    #             debug_normal_label = tkinter.Label(frame_system,
    #                                           text="DEBUG-Normal",
    #                                           background="white",
    #                                           font=SETTINGS_BTN_FONT
    #                                           )
    #             debug_normal_label.grid(row=8, column=0, columnspan=2, pady=10, sticky="new")
    #
    #             def on_debug_normal_click():
    #                 current_value = parent.debug_normal_value.get()
    #                 DEBUG_MODE_NORMAL = current_value
    #                 config: Configuration = config_manager.generate_configuration('Admin Debug Mode')
    #                 config.write_parameter('Debug Mode Normal', str(current_value))
    #                 info_label_system.config(text="Einstellung wird gespeichert und App geschlossen...")
    #                 logger.debug("DEBUG_NORMAL is now activated.")
    #                 parent.after(3000, close_app)
    #
    #             parent.debug_normal_value = ctkinter.BooleanVar(value=False)
    #
    #             def load_debug_mode_normal():
    #                 config: Configuration = config_manager.generate_configuration('Admin Debug Mode')
    #                 try:
    #                     saved_value = config.read_parameter('Debug Mode Normal', generate_if_missing=True,
    #                                                         gen_initial_value='False')
    #                     return saved_value.lower() == "true"
    #                 except KeyError:
    #                     return False
    #
    #             parent.debug_normal = ctkinter.CTkCheckBox(frame_system,
    #                                                   text_color="white",
    #                                                   command=lambda: on_debug_normal_click(),
    #                                                   variable=parent.debug_normal_value,
    #                                                   )
    #             parent.debug_normal.grid(column=1, row=8, columnspan=2)
    #
    #             normal_saved_value = load_debug_mode_normal()  # Funktion zum Laden des gespeicherten Wertes
    #             parent.debug_normal_value.set(normal_saved_value)  # Gespeicherten Wert anwenden
    #
    #             # Checkbox DEBUG ALL
    #             debug_all_label = tkinter.Label(frame_system,
    #                                        text="DEBUG-Alle",
    #                                        background="white",
    #                                        font=SETTINGS_BTN_FONT
    #                                        )
    #             debug_all_label.grid(row=9, column=0, columnspan=2, pady=10, sticky="new")
    #
    #             def on_debug_all_click():
    #                 current_value = parent.debug_all_value.get()
    #                 DEBUG_MODE_ALL = current_value
    #                 config: Configuration = config_manager.generate_configuration('Admin Debug Mode')
    #                 config.write_parameter('Debug Mode All', str(current_value))
    #                 info_label_system.config(text="Einstellung wird gespeichert und App geschlossen...")
    #                 logger.debug("DEBUG_ALL is now activated.")
    #                 parent.after(3000, close_app)
    #
    #             def load_debug_mode_all():
    #                 config: Configuration = config_manager.generate_configuration('Admin Debug Mode')
    #                 try:
    #                     saved_value = config.read_parameter('Debug Mode All', generate_if_missing=True,
    #                                                         gen_initial_value='False')
    #                     return saved_value.lower() == "true"
    #                 except KeyError:
    #                     return False
    #
    #             parent.debug_all_value = ctkinter.BooleanVar(value=False)
    #
    #             parent.debug_all = ctkinter.CTkCheckBox(frame_system,
    #                                                text_color="white",
    #                                                command=lambda: on_debug_all_click(),
    #                                                variable=parent.debug_all_value,
    #                                                )
    #             parent.debug_all.grid(column=1, columnspan=2, row=9)
    #
    #             all_saved_value = load_debug_mode_all()  # Funktion zum Laden des gespeicherten Wertes
    #             parent.debug_all_value.set(all_saved_value)  # Gespeicherten Wert anwenden
    #         else:
    #             logger.debug("DEBUG settings only available for administrator.")
    #
    #     DBUG_for_Admin(frame_system)
    #
    #     # Label für die Zoomstufe
    #     zoom_label = tkinter.Label(frame_system,
    #                           text="Anpassen der Zoomstufe",
    #                           background="white",
    #                           font=SETTINGS_BTN_FONT
    #                           )
    #     zoom_label.grid(row=2, column=1, pady=10, sticky="new")
    #
    #     # Funktion zur Aktualisierung der Zoomstufe
    #     def update_zoom(value):
    #         logger.debug(f"Zoom level updated: {value}")
    #
    #     def get_zoom_parameter():
    #         config: Configuration = config_manager.generate_configuration('Zoom indicator')
    #         try:
    #             saved_value = config.read_parameter('Zoom indicator', generate_if_missing=True, gen_initial_value='1')
    #             logger.debug(saved_value)
    #             return float(saved_value)
    #         except KeyError:
    #             return 1.0
    #         except TypeError as e:
    #             logger.error(f"{e}")
    #             return 1.0
    #
    #     zoom_control = ctkinter.CTkSlider(frame_system,
    #                                  from_=int(0.5),  # Minimaler Zoomfaktor
    #                                  to=int(3.0),  # Maximaler Zoomfaktor
    #                                  number_of_steps=20,  # Anzahl der Schritte (optional)
    #                                  command=lambda value: update_zoom(round(value, 1))  # Rundung auf 1 Nachkommastelle
    #                                  )
    #     zoom_control.grid(row=3, column=1, pady=10, sticky="ew")
    #     zoom_control.set(get_zoom_parameter())  # Standard-Zoomfaktor
    #
    #     confirm_button = ctkinter.CTkButton(frame_system,
    #                                    text="Speichern und Beenden",
    #                                    border_width=border,
    #                                    corner_radius=corner,
    #                                    fg_color=srh_orange,
    #                                    command=lambda: save_zoom(zoom_control.get())
    #                                    )
    #     confirm_button.grid(row=4, column=1, pady=10, sticky="")
    #
    #     def save_zoom(value):
    #         if zoom_control:
    #             config: Configuration = config_manager.generate_configuration('Zoom indicator')
    #             config.write_parameter('Zoom indicator', value)
    #             info_label_system.config(text="Einstellung wird gespeichert und App geschlossen...")
    #             parent.after(2000, close_app)
    #         else:
    #             logger.debug("It is not possible to adjust the zoom level.")
    #
    #     # Label für Fehlermeldungen
    #     info_label_system = tkinter.Label(frame_system,
    #                                  text="",
    #                                  background="white",
    #                                  font=error_red
    #                                  )
    #     info_label_system.grid(row=10, pady=10, column=0, columnspan=3, sticky="sew")
    #
    #     # LOGGER PRINT
    #     logger.debug(f"Complete loading of the 'System' settings page. {['image']}")
    #
    #     ###############################
    #     # # L A Y O U T : U E B E R # #
    #     ###############################
    #
    #     # Dynamischer Frame mit Einstellungsmöglichkeiten
    #     frame_ueber = tkinter.Frame(popup, bg="white")
    #     frame_ueber.grid(row=1, column=1, sticky="nsew")
    #     frame_ueber.grid_columnconfigure(0, weight=1)
    #     frame_ueber.grid_columnconfigure(1, weight=1)
    #     frame_ueber.grid_columnconfigure(2, weight=1)
    #     frame_ueber.grid_rowconfigure(0, weight=1)
    #
    #     # Ueberschrift erstellen Über das DD-Inv Tool
    #     ueber_label = tkinter.Label(frame_ueber,
    #                            text="Über das DD-Inv Tool",
    #                            font=SETTINGS_FONT,
    #                            bg="white"
    #                            )
    #     ueber_label.grid(row=0, column=0, columnspan=3, sticky="new")
    #
    #     # Unterüberschrift erstellen Credits
    #     credits_label = tkinter.Label(frame_ueber,
    #                              text="Credits",
    #                              font=SETTINGS_FONT,
    #                              bg="white"
    #                              )
    #     credits_label.grid(row=1, column=0, pady=5, sticky="nsew")
    #
    #     # Liste mit den Namen, URL, Bild fuer Credits
    #     # Funktion zum Anzeigen des Frames
    #     def show_frame_settings(category):
    #         logger.debug(f"Currently visible frame before hiding: {frames}")
    #         nonlocal current_frame  # Zugriff auf die äußere Variable
    #         logger.debug(f"current_frame:{current_frame}")
    #         if current_frame:  # Falls bereits ein Frame angezeigt wird
    #             current_frame.grid_remove()  # Verstecke den aktuellen Frame
    #             logger.debug(f"frame:{current_frame}")
    #         new_frame = frames.get(category)
    #         logger.debug(f"new_frame after creation:{new_frame}")
    #         if new_frame:  # Wenn der neue Frame existiert
    #             new_frame.grid(row=1, column=1, rowspan=1, sticky="nsew")
    #             new_frame.columnconfigure(0, weight=1)
    #             new_frame.rowconfigure(0, weight=0)
    #             current_frame = new_frame
    #             logger.debug(f"New current_frame: {current_frame}")
    #
    #     # Funktion für Klick auf Kategorie
    #     def on_category_click_settings(label_settings, category_settings):
    #         update_header_icon(category_settings)
    #         # Setze alle Labels zurück
    #         for cat in category_labels_settings:
    #             cat.config(fg="white")
    #             logger.debug("if on_category_click")
    #         # Hervorhebung des angeklickten Labels
    #         label_settings.config(fg="Black")
    #         # Zeige den zugehörigen Frame
    #         show_frame_settings(category_settings)
    #
    #     # Kategorien in der Seitenleiste erstellen
    #     category_labels_settings = []  # Liste für die Label-Referenzen
    #     for idx, category in enumerate(categories):
    #         label = tkinter.Label(side_settings,
    #                          text=category,
    #                          bd=0,
    #                          relief=tkinter.FLAT,
    #                          font=SETTINGS_BTN_FONT,
    #                          fg="white",
    #                          bg=srh_orange
    #                          )
    #         label.grid(padx=10, pady=8, row=idx + 1, column=0, sticky="w")
    #
    #         label.bind("<Button-1>",
    #                    lambda event,
    #                           lbl=label,
    #                           cat=category:
    #                    on_category_click_settings(lbl, cat)
    #                    )
    #         category_labels_settings.append(label)
    #
    #     # Verstecke alle Frames außer dem initialen Profil-Frame
    #     for key, frame in frames.items():
    #         if key != "Profil":  # Verstecke nur die anderen Frames
    #             frame.grid_remove()
    #
    #     # LOGGER PRINT
    #     logger.debug(f"Fully load the switch to switch between the settings pages. {['image']}")
    #
