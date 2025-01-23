import tkinter as tk
import webbrowser
from tkinter import *
from tkinter import ttk
import customtkinter as ctk

from .customMessageBoxDelete import *
from ._avatarManager import check_internet_connection, loadImage
from includes.sec_data_info import sqlite3api as db


class LogInWindow(ctk.CTkFrame):
    def __init__(self, parent, controller):
        check_internet_connection()
        ctk.CTkFrame.__init__(self, parent)
        self.configure(fg_color="white")

        def log_in():
            password = password_entry.get().strip()
            user = username_entry.get().strip()

            # Reset cache for user info
            cache.user_group = None
            cache.user_name = None

            from includes.sec_data_info import UserSecurity as security

            if security.verify_user(user, password):  # User authentication
                benutzer_info = db.read_benutzer(user)
                cache.user = benutzer_info
                cache.user_group = benutzer_info.get('Rolle', '')  # Store user's role
                cache.user_name = user  # Store username in cache
                cache.user_group_data = next((rolle for rolle in db.read_all_rollen() if rolle['Rolle'] == cache.user_group), None)
                cache.user_avatar = loadImage(parent=parent, image=db.get_avatar_info(user), defult_image=cache.user_default_avatar, width=48, height=48) if cache.internet else loadImage(parent=parent, image=cache.user_default_avatar, width=48, height=48)
                cache.user_avatarx128 = loadImage(parent=parent, image=db.get_avatar_info(user), defult_image=cache.user_default_avatar, width=128, height=128) if cache.internet else loadImage(parent=parent, image=cache.user_default_avatar, width=128, height=128)

                password_entry.delete(0, 'end')
                username_entry.delete(0, 'end')
                # Show the MainPage
                from .MainPage import MainPage
                cache.controller = controller
                controller.show_frame(MainPage)

            else:
                # Show error message for incorrect login
                customMessageBoxDelete(self,
                                       title="Nutzername oder Passwort falsch",
                                       message="Nutzername und Passwort stimmen nicht überein.\n Bitte versuchen Sie es erneut.")

        def on_enter(event):
            log_in()

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # Header
        header_frame = ctk.CTkFrame(self, height=10, fg_color=srh_orange)
        header_frame.grid(row=0, column=0, sticky="ew")
        from ._avatarManager import resource_path
        self.srh_head = tk.PhotoImage(file=resource_path("./includes/assets/srhHeader.png"))
        srh_header = ctk.CTkLabel(header_frame, image=self.srh_head, fg_color=srh_orange)
        srh_header.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        grey_frame = ctk.CTkFrame(self, height=10, fg_color=srh_grey)
        grey_frame.grid(row=1, column=0, sticky="ew")

        # Grey frame label
        grey_label = ctk.CTkLabel(grey_frame, text="Willkommen bei DD-Inv", font=LARGEFONT, fg_color=srh_grey)
        grey_label.pack(expand=True, fill="both")

        # Login form
        form_frame = ctk.CTkFrame(self, fg_color="white")
        form_frame.grid(row=2, column=0, sticky="nsew", pady=60)
        form_frame.grid_columnconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)

        # Username entry
        tk.Label(form_frame, text="Benutzername", font=LARGEFONT, bg="white").grid(column=3, row=0, pady=10)
        username_entry = ctk.CTkEntry(form_frame, font=LOGINFONT, corner_radius=corner, fg_color=srh_grey, border_width=border, text_color="black", justify="center")
        username_entry.grid(column=3, row=1, sticky="ew", padx=20, pady=10)

        # Password entry
        tk.Label(form_frame, text="Passwort", font=LARGEFONT, bg="white").grid(column=3, row=2, pady=10)
        password_entry = ctk.CTkEntry(form_frame, font=LOGINFONT, corner_radius=corner, fg_color=srh_grey, border_width=border, text_color="black", show="•", justify="center")
        password_entry.grid(column=3, row=3, sticky="ew", padx=20, pady=10)

        # Login button
        self.log_out_btn = tk.PhotoImage(file=resource_path("./includes/assets/Anmelden.png"))
        login_button = ctk.CTkButton(form_frame, image=self.log_out_btn, fg_color="white", cursor="hand2", command=log_in, border_width=0)
        login_button.grid(column=3, row=4, pady=50, sticky="ew")

        # Bind Enter key
        username_entry.bind("<Return>", on_enter)
        password_entry.bind("<Return>", on_enter)

        # Bottom frame
        bottom_frame = ctk.CTkFrame(self, height=10, fg_color="white")
        bottom_frame.grid(row=3, column=0, sticky="ew")

        def open_VersionBuild(url):
            webbrowser.open(url)

        parent.logo_image = PhotoImage(file=resource_path("./includes/assets/DD-Inv_Logo.png"))
        btn_links_label = ctk.CTkLabel(bottom_frame, text="VersionBuild   V. 0.2 BETA", cursor="hand2", font=("Arial", 12), fg_color="white")
        btn_links_label.grid(row=0, column=0, pady=2, sticky="new")
        btn_links_label.configure(width=30, anchor="center", image=parent.logo_image, compound="left")
        btn_links_label.bind("<Button-1>", lambda e: open_VersionBuild("https://github.com/peaemer/DD-inv/releases/latest"))
