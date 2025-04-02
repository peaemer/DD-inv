"""
    .
"""

import tkinter
import webbrowser
from tkinter import ttk
from typing import override

import customtkinter

import cache
from includes.windows.customMessageBoxDelete import customMessageBoxDelete
from includes.windows.IWindow import IWindow
from includes.windows._avatarManager import loadImage, check_internet_connection
from includes.windows._styles import LARGEFONT, LOGINFONT, corner, border, srh_grey, srh_orange
from includes.sec_data_info import sqlite3api
from includes.util import Paths
from main import DdInv


# noinspection PyAttributeOutsideInit
class LoginWindow(IWindow):
    """
        .
    """

    def log_in(self):
        """
            .
        """
        password = self.password_entry.get().strip()
        user = self.username_entry.get().strip()

        cache.user_group = None
        cache.user_name = None

        from includes.sec_data_info import UserSecurity

        if UserSecurity.verify_user(user, password):  # Benutzer authentifizieren
            # Benutzerinformationen aus der Datenbank abrufen
            benutzer_info = sqlite3api.read_benutzer(user)
            cache.user = benutzer_info
            cache.user_group = benutzer_info.get('Rolle', '')  # Rolle des Benutzers speichern
            cache.user_name = user  # Benutzernamen im Cache speichern
            cache.user_group_data = next((rolle for rolle in sqlite3api.read_all_rollen() if rolle['Rolle'] == cache.user_group), None)
            cache.user_avatar = loadImage(
                parent=self.parent, image=sqlite3api.get_avatar_info(user),
                defult_image=cache.user_default_avatar, width=48,
                height=48
            ) if cache.internet else loadImage(
                parent=self.parent,
                image=cache.user_default_avatar,
                width=48, height=48
            )
            cache.user_avatarx128 = loadImage(
                parent=self.parent,
                image=sqlite3api.get_avatar_info(user),
                defult_image=cache.user_default_avatar,
                width=128,
                height=128
            ) if cache.internet else loadImage(
                parent=self.parent,
                image=cache.user_default_avatar,
                width=128,
                height=128
            )

            self.password_entry.delete(0, 'end')
            self.username_entry.delete(0, 'end')
            # Zeige die MainPage an
            from .MainPage import MainPage
            cache.controller = self.controller
            self.controller.show_frame(MainPage)

        else:
            # Zeige Fehlermeldung bei falschem Login
            customMessageBoxDelete(
                self,
                title="Nutzername oder Passwort falsch",
                message="Nutzername und Passwort stimmen nicht überein.\n Bitte versuchen Sie es erneut."
            )

    @override
    def setup_main_frame(self, frame:tkinter.Frame) -> None:
        # Username
        tkinter.Label(
            frame,
            text="Benutzername",
            font=LARGEFONT,
            bg="white"
        ).grid(column=1, row=1, pady=10)

        self.username_entry = customtkinter.CTkEntry(
            frame,
            font=LOGINFONT,
            corner_radius=corner,
            fg_color=srh_grey,
            border_width=border,
            text_color="black",
            justify="center"
        )

        # Passwort
        tkinter.Label(
            frame,
            text="Passwort",
            font=LARGEFONT,
            bg="white"
        ).grid(column=1, row=3, pady=10)


        self.password_entry = customtkinter.CTkEntry(
            frame,
            font=LOGINFONT,
            corner_radius=corner,
            fg_color=srh_grey,
            border_width=border,
            text_color="black",
            show="•",
            justify="center"
        )

        self.login_button_image = tkinter.PhotoImage(file=Paths.assets_path("Anmelden.png"))
        self.login_button = tkinter.Button(
            frame,
            image=self.login_button_image,
            bg="white",
            cursor="hand2",
            command=self.log_in,
            bd=0,
            relief=tkinter.FLAT,
            activebackground="white",
        )

        self.link_frame:tkinter.Frame = tkinter.Frame(frame, height=10, background="white")
        self.link_frame.grid(row=6, column=0, columnspan = 3, sticky='SWE')
        self.link_logo_image = tkinter.PhotoImage(file=Paths.assets_path("DD-Inv_Logo.png"))
        self.link_button_label = ttk.Label(self.link_frame, background="white", text="VersionBuild   V. 1.2 STABLE", cursor="hand1", font=("Arial", 12))
        self.link_button_label.grid(row=18, column=0, pady=2, sticky="SW")
        self.link_button_label.configure(width=30, anchor='center', image=self.link_logo_image, compound="left")
        self.link_button_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/peaemer/DD-inv/releases/latest"))

        frame.grid_columnconfigure(0, weight=2)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=2)

        frame.grid_rowconfigure(0, weight=1)
        for i in range(1,6):
            frame.grid_rowconfigure(i, weight=0)
        frame.grid_rowconfigure(6, weight=3)


        self.username_entry.grid(column=1, row=2, padx=0, pady=10, sticky="ew")
        self.password_entry.grid(column=1, row=4, padx=0, pady=10, sticky="ew")

        # Login-Button

        self.login_button.grid(column=1, row=5, padx=0, pady=50)

        # Bind die Enter-Taste
        self.username_entry.bind("<Return>", lambda _:self.log_in())
        self.password_entry.bind("<Return>", lambda _:self.log_in())


    @override
    def setup_header_bar(self, frame:tkinter.Frame) -> None:
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_columnconfigure(0, weight=1)
        self.grey_label = tkinter.Label(
            frame,
            text="Willkommen bei DD-Inv",
            font=LARGEFONT,
            bg=srh_grey,
            fg="black",
            anchor="center"
        )

        self.srh_header_image:tkinter.PhotoImage = tkinter.PhotoImage(file=Paths.assets_path("srhHeader.png"))
        self.srh_header:tkinter.Label = tkinter.Label(
            frame,
            image=self.srh_header_image,
            bd=0,
            bg=srh_orange
        )

        self.srh_header.grid(padx=10, pady=10, row=0, column=0, sticky='NWE')
        self.grey_label.grid(column=0, row=1, columnspan=4, sticky='NWE')  # Text zentrieren und Frame ausfüllen

    @override
    def setup_side_bar_left(self, frame: tkinter.Frame, overlay_header_bar: bool = False) -> bool:
        return False

    @override
    def setup_side_bar_right(self, frame: tkinter.Frame, overlay_header_bar: bool = False) -> bool:
        return False

    @override
    def on_load(self) -> None:
        pass

    def __init__(self, parent:tkinter.Frame, controller:DdInv):
        super().__init__(parent, controller, admin_mode=True)
        check_internet_connection()
        print('init!')
