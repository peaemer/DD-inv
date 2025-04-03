from typing import override

import tkinter
import customtkinter

from includes.sec_data_info import sqlite3api as sqlapi
from .IPopUp import IPopUp
from includes.gui.styles import *
from includes.util import Paths


class AddRoomPopup(IPopUp):
    """
        Creates a popup where a new room can be created. Contains an entry for the name
        of the new room and one for the location description.
        When pressing the submit button, a new entry in the rooms table will be created with the
        properties of the new role.
    """

    def submit_entry(self):
        """
            .
        """
        if not self.loction_entry.get() or self.loction_entry.get() in ['', ' '] or not self.name_entry.get() or self.name_entry.get() in ['', ' ']:
            self.error_label.configure(text="Bitte fülle alle Felder aus.")
        else:
            sqlapi.create_room(self.name_entry.get(), self.loction_entry.get())
            from ..pages.adminPages.AdminRoomPage import AdminRoomWindow
            AdminRoomWindow.update_treeview_with_data()
            from ..pages.MainPage import MainPage
            MainPage.update_sidetree_with_data()
            self.destroy()

    @override
    def add_content(self, content_frame: tkinter.Frame):
        """
            .
        """
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_columnconfigure(2, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)

        self.location_label:tkinter.Label = tkinter.Label(
            content_frame,
            text="Raum Bezeichnung",
            background="white",
            font=("Arial", size_add_room_popup)
        )
        self.name_label:tkinter.Label = tkinter.Label(
            content_frame,
            text="Ort",
            background="white",
            font=("Arial", size_add_room_popup)
        )

        self.loction_entry:customtkinter.CTkEntry = customtkinter.CTkEntry(
            content_frame,
            fg_color="#d9d9d9",
            text_color="black",
            border_width=border,
            font=("Arial", 18),
            corner_radius=corner
        )
        self.name_entry:customtkinter.CTkEntry = customtkinter.CTkEntry(
            content_frame,
            fg_color="#d9d9d9",
            text_color="black",
            border_width=border,
            font=("Arial", size_add_room_popup),
            corner_radius=corner
        )

        self.error_label:tkinter.Label = tkinter.Label(content_frame)

        self.name_label.grid(row=0, column=0, padx=10, pady=20, sticky=tkinter.E)
        self.location_label.grid(row=1, column=0, padx=10, pady=20, sticky=tkinter.E)

        self.name_entry.grid(row=0, column=1, padx=20, pady=20, sticky='WE')
        self.loction_entry.grid(row=1, column=1, padx=20, pady=20, sticky='WE')

        self.error_label.grid(row=2, column=0, padx=10, pady=20, sticky=tkinter.E)

    def __init__(self, parent: tkinter.Toplevel):
        """
            Fügt ein Popup-Fenster hinzu, das verwendet wird, um Daten für einen neuen Raum
            einzugeben, einschließlich Raumbezeichnung und Ort. Das Fenster bietet zusätzlich
            Optionen zur Bestätigung oder zum Abbrechen der Eingabe.

            :param parent: Das übergeordnete Fenster, auf dem das Popup-Fenster dargestellt wird.
            :type parent: tkinter.Tk oder tkinter.Frame

            :return: Entweder wird das Popup geschlossen ohne Aktion, oder die Eingaben werden
                     verarbeitet und einem extern definierten Datenbanksystem hinzugefügt.
            :rtype: None
        """
        super().__init__(
            parent,
            'Raum Hinzufügen',
            header_text='Raum Hinzufügen',
            admin_mode=True,
            size=(650, 650),
            buttons=[
                (tkinter.PhotoImage(file=Paths.assets_path("AbbrechenButton.png")), self.destroy),
                (tkinter.PhotoImage(file=Paths.assets_path("HinzuBig_blue.png")), self.submit_entry)
            ],
            header_button=(tkinter.PhotoImage(file=Paths.assets_path("ArrowLeft.png")), self.destroy),
        )