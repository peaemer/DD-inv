import tkinter
from typing import override

import tkinter as tk

import customtkinter
import customtkinter as ctk

from includes.windows.IPopUp import IPopUp
from includes.windows.styles import corner, border, size_add_role_popup
from includes.util import Paths
from includes.util.Logging import Logger
from includes.sec_data_info import sqlite3api as db

logger: Logger = Logger('AddItemPopup2')


class AddRolePopup(IPopUp):
    """
        Creates a popup where a new role can be created. Contains an entry for the name
        of the new role, and a list of optional rights, that users with that role will have.
        When pressing the Submit button, a new entry in the roles table will be created with the
        properties of the new role.
    """

    def submit_entry(self):
        """
            .
        """
        if self.name_entry.get() is not None and self.name_entry.get() != "":
            def read_option_value(option_name:str) -> str:
                return "True" if self.options[option_name][1].get() == 1 else "False"

            role_name = self.name_entry.get()
            rechte = {
                "ROLLE_LOESCHBAR": read_option_value("Rolle Löschbar"),
                "ADMIN_FEATURE": read_option_value("Admin Feature"),
                "ENTRY_ANSEHEN": read_option_value("Eintrag Ansehen"),
                "ENTRY_LOESCHEN": read_option_value("Eintrag Löschen"),
                "ENTRY_BEARBEITEN": read_option_value("Eintrag Bearbeiten"),
                "ENTRY_ERSTELLEN": read_option_value("Rolle Löschbar"),
                "GRUPPEN_LOESCHEN": read_option_value("Gruppen Löschen"),
                "GRUPPEN_ERSTELLEN": read_option_value("Gruppen Erstellen"),
                "GRUPPEN_BEARBEITEN": read_option_value("Gruppen Bearbeiten"),
                "ROLLEN_ERSTELLEN": read_option_value("Rollen Erstellen"),
                "ROLLEN_BEARBEITEN": read_option_value("Rollen Bearbeiten"),
                "ROLLEN_LOESCHEN": read_option_value("Rollen Löschen"),
                "USER_LOESCHEN": read_option_value("Benutzer Löschen"),
                "USER_BEARBEITEN": read_option_value("Benutzer Bearbeiten"),
                "USER_ERSTELLEN": read_option_value("Benutzer Erstellen")
            }
            db.create_rolle(role_name, **rechte)
            from .AdminRoleWindow import AdminRoleWindow
            AdminRoleWindow.update_treeview_with_data()
            self.destroy()

    # noinspection DuplicatedCode
    @override
    def add_content(self, content_frame: tk.Frame):
        row:int = 1
        column:int = 0
        content_frame.grid_columnconfigure(column, weight=1)
        content_frame.grid_columnconfigure(column+1, weight=1)
        for name in ['Benutzer Erstellen', 'Benutzer Bearbeiten', 'Benutzer Löschen', 'Eintrag Ansehen', 'Eintrag Bearbeiten', 'Eintrag Löschen', 'Rolle Löschbar', 'Admin Feature']:
            content_frame.grid_rowconfigure(row, weight=1)
            self.options[name] = (
                tk.Label(content_frame, text=name, background="white", font=("Arial", size_add_role_popup),pady=10),
                ctk.CTkCheckBox(content_frame, text_color="white")
            )
            self.options[name][0].grid(row=row, column=column, sticky='W', padx = 20)
            self.options[name][1].grid(row=row, column=column+1)
            row+=1
        row = 1
        column = 2
        content_frame.grid_columnconfigure(column, weight=1)
        content_frame.grid_columnconfigure(column+1, weight=1)
        for name in ['Gruppen Erstellen', 'Gruppen Bearbeiten', 'Gruppen Löschen', 'Rollen Erstellen', 'Rollen Bearbeiten', 'Rollen Löschen']:
            content_frame.grid_rowconfigure(row, weight=1)
            self.options[name] = (
                tk.Label(content_frame, text=name, background="white", font=("Arial", size_add_role_popup),pady=10),
                ctk.CTkCheckBox(content_frame, text_color="white")
            )
            self.options[name][0].grid(row=row, column=column, sticky='W', padx = 20)
            self.options[name][1].grid(row=row, column=column+1)
            row+=1

        self.name_label = tk.Label(
            content_frame,
            text='Rollenname',
            background='white',
            font=("Arial", size_add_role_popup),
            pady=10
        )

        self.name_entry = customtkinter.CTkEntry(
            content_frame,
            fg_color="#d9d9d9",
            text_color="black",
            border_width=border,
            font=("Arial", 18),
            corner_radius=corner
        )

        self.name_label.grid(row=0, column=0, sticky='E',padx=20)
        self.name_entry.grid(row=0, column=1, columnspan = 2, sticky='WE')

    def __init__(self, parent: tk.Toplevel):
        """
            :param tkinter.Toplevel parent:

        """
        super().__init__(
            parent,
            'Rolle Hinzufügen',
            header_text='Rolle Hinzufügen',
            admin_mode=True,
            size=(650, 650),
            buttons=[
                (tk.PhotoImage(file=Paths.assets_path("AbbrechenButton.png")), self.destroy),
                (tk.PhotoImage(file=Paths.assets_path("HinzuBig_blue.png")), self.submit_entry)
            ],
            header_button=(tk.PhotoImage(file=Paths.assets_path("ArrowLeft.png")), self.destroy),
        )

        self.options:dict[str,tuple[tkinter.Label,customtkinter.CTkCheckBox]] = {}
