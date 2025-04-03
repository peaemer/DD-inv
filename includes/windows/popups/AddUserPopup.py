import string
from random import Random
from typing import override

import tkinter as tk
import customtkinter as ctk

from includes.windows.customMessageBoxDelete import customMessageBoxDelete
from includes.windows.IPopUp import IPopUp
from includes.windows.styles import srh_grey, corner, comboborder, srh_grey_hover, size_add_user_popup, border
from includes.CTkScrollableDropdown import CTkScrollableDropdownFrame
from includes.util import Paths
from includes.util.Logging import Logger
from includes.sec_data_info import sqlite3api as db

logger: Logger = Logger('AddItemPopup2')


class AddUserPopup(IPopUp):
    """

        :var list[tkinter.Button] buttons:

        :var tkinter.Frame content_frame:
    """

    def submit_entry(self):
        """
            .
        """
        pw = str(''.join(Random().choices(string.ascii_letters, k=7)))

        if not self.username_entry.get() or self.username_entry.get() == "" or not self.role_combobox.get() or self.role_combobox.get() == "Rolle auswählen":
            self.error_label.configure(text="Bitte fülle alle Felder aus (Nutzername)")
        else:
            db.create_benutzer(self.username_entry.get(), pw, self.email_entry.get())
            customMessageBoxDelete(
                self,
                title="Benutzer Erstellt",
                message="Nutzername: " + self.username_entry.get() + "\nNew password: " + pw,
                blue=True
            )
            from ..AdminUserWindow import AdminUserWindow
            AdminUserWindow.update_treeview_with_data()
            self.destroy()

    @override
    def add_content(self, content_frame: tk.Frame):

        content_frame.grid_rowconfigure(0, weight=1)  # Header
        content_frame.grid_rowconfigure(1, weight=1)  # Input-Bereich
        content_frame.grid_rowconfigure(2, weight=1)  # Buttons
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_columnconfigure(2, weight=1)

        self.username_label = tk.Label(
            content_frame,
            text="Username",
            background="white",
            font=("Arial", size_add_user_popup),
            pady=10
        )
        self.username_entry = ctk.CTkEntry(
            content_frame,
            fg_color="#d9d9d9",
            text_color="black",
            border_width=border,
            corner_radius=corner,
            font=("Arial", size_add_user_popup)
        )
        self.email_label = tk.Label(
            content_frame,
            text="E-Mail",
            background="white",
            font=("Arial", size_add_user_popup)
        )
        self.email_entry = ctk.CTkEntry(
            content_frame,
            fg_color="#d9d9d9",
            text_color="black",
            border_width=border,
            corner_radius=corner,
            font=("Arial", size_add_user_popup)
        )
        self.role_label = tk.Label(
            content_frame,
            text="Rolle",
            background="white",
            font=("Arial", size_add_user_popup)
        )
        self.error_label = tk.Label(content_frame,
            text="",
            background="white",
            fg="darkred", font=("Arial", 14)
        )

        self.username_label.grid(row=1, column=0, padx=10, pady=30, sticky=tk.E)
        self.username_entry.grid(row=1, column=1, padx=20, pady=30, sticky=tk.W + tk.E)
        self.email_label.grid(row=2, column=0, padx=10, pady=30, sticky=tk.E)
        self.email_entry.grid(row=2, column=1, padx=20, pady=30, sticky=tk.W + tk.E)
        self.role_label.grid(row=3, column=0, padx=10, pady=30, sticky=tk.E)
        self.error_label.grid(row=4, column=0, columnspan=3, padx=0, pady=30)

        role_values = []
        for room in db.read_all_rollen():
            role_values.append(room['Rolle'])
        self.role_combobox = ctk.CTkComboBox(
            content_frame,
            font=("Arial", size_add_user_popup),
            text_color="black",
            corner_radius=corner,
            button_color=srh_grey,
            fg_color=srh_grey,
            border_width=border,
            state="readonly"
        )

        self.role_combobox.grid(row=3, column=1, padx=10, pady=15, sticky=tk.W + tk.E)

        CTkScrollableDropdownFrame(
            self.role_combobox,
            values=role_values,
            button_color=srh_grey,  # BUGGY
            frame_corner_radius=corner,
            fg_color=srh_grey,
            text_color="black",
            frame_border_width=comboborder,
            frame_border_color=srh_grey_hover,
            justify="left"
        )

        self.role_combobox.set("Rolle auswählen")


    def __init__(self, parent: tk.Toplevel):
        """

            :param tkinter.Toplevel parent:

        """
        super().__init__(
            parent,
            'Benutzer Hinzufügen',
            header_text='Benutzer Hinzufügen',
            admin_mode=True,
            size=(650, 650),
            buttons=[
                (tk.PhotoImage(file=Paths.assets_path("AbbrechenButton.png")), self.destroy),
                (tk.PhotoImage(file=Paths.assets_path("HinzuBig_blue.png")), self.submit_entry)
            ],
            header_button=(tk.PhotoImage(file=Paths.assets_path("ArrowLeft.png")), self.destroy),
        )