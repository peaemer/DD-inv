"""
    .
"""
import json
from typing import override

import tkinter as tk
import customtkinter as ctk

import cache
from includes.gui.popups.IPopUp import IPopUp
from includes.gui.styles import *
from includes.CTkScrollableDropdown import CTkScrollableDropdownFrame
from includes.util import Paths
from includes.util.Logging import Logger
from includes.sec_data_info import sqlite3api as db

logger: Logger = Logger('AddItemPopup2')

class AddItemPopup(IPopUp):
    
    """

        :var list[tkinter.Button] buttons:

        :var tkinter.Frame content_frame:
    """

    def submit_entry(self):
        """
            .
        """
        logger.debug(f'sentry:{self.service_tag_entry}')
        tag:str = self.service_tag_entry.get() if self.service_tag_entry and self.service_tag_entry.get() else ''
        type:str = self.type_entry.get() if self.type_entry else ''
        room:str = self.room_combobox.get() if self.room_combobox and self.room_combobox.get() else ''
        name:str = self.name_entry.get() if self.name_entry and self.name_entry.get() else ''
        damage:str = self.damage_entry.get() if self.damage_entry and self.damage_entry.get() else ''
        metadata:str = json.dumps(list[dict[str,str]]([{"erstellt von":cache.user_name}]))
        if type == '' or room == 'Raum auswählen' or name == '':
            self.error_label.configure(text="Bitte fülle alle Felder aus (Typ, Raum, Name)")
        else:
            logger.debug(db.create_hardware(tag,type,name,damage,"",room, metadata))
            from ..pages.MainPage import MainPage
            MainPage.update_treeview_with_data(data=None)
            MainPage.update_sidetree_with_data()
            self.destroy()

    @override
    def add_content(self, content_frame: tk.Frame):
        content_frame.grid_rowconfigure(0, weight=0)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_rowconfigure(2, weight=0)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_columnconfigure(2, weight=1)
        
        # Label und Eingabefeld hinzufügen
        self.service_tag_label = tk.Label(
            content_frame,
            text="Service Tag",
            background="white",
            font=("Arial", size_add_item_popup)
        )
        self.service_tag_label.grid(row=1, column=0, padx=0, pady=20, sticky=tk.E)

        self.service_tag_entry = ctk.CTkEntry(
            content_frame,
            border_width=0,
            text_color="black",
            fg_color=srh_grey,
            font=("Arial", size_add_item_popup),
            corner_radius=corner
        )
        self.service_tag_entry.grid(row=1, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

        # Typ
        self.type_label = tk.Label(
            content_frame,
            text="Typ",
            background="white",
            font=("Arial", size_add_item_popup)
        )
        self.type_label.grid(row=2, column=0, padx=0, pady=20, sticky=tk.E)

        self.type_entry = ctk.CTkEntry(
            content_frame,
            border_width=0,
            text_color="black",
            fg_color=srh_grey,
            font=("Arial", size_add_item_popup),
            corner_radius=corner
        )
        self.type_entry.grid(row=2, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

        # Raum (Dropdown-Menü)
        self.room_label = tk.Label(
            content_frame,
            text="Raum", background="white",
            font=("Arial", size_add_item_popup)
        )
        self.room_label.grid(row=3, column=0, padx=0, pady=20, sticky=tk.E)

        # Combobox statt Entry
        room_values = []
        for room in db.fetch_all_rooms():
            room_values.append(room['Raum'])

        self.room_combobox = ctk.CTkComboBox(
            content_frame,
            values=room_values,
            font=("Arial", size_add_item_popup),
            fg_color=srh_grey,
            text_color="black",
            button_color=srh_grey,
            corner_radius=corner,
            border_width=0,
            state="readonly"
        )
        self.room_combobox.grid(row=3, column=1, padx=20, pady=20, sticky="ew")

        CTkScrollableDropdownFrame(
            self.room_combobox,
            values=room_values,
            button_color=srh_grey,  # BUGGY
            frame_corner_radius=corner,
            fg_color=srh_grey,
            text_color="black",
            frame_border_width=comboborder,
            frame_border_color=srh_grey_hover,
            justify="left"
        )

        # Name
        self.name_label = tk.Label(
            content_frame,
             text="Name",
             background="white",
             font=("Arial", size_add_item_popup)
         )
        self.name_label.grid(row=4, column=0, padx=0, pady=20, sticky=tk.E)

        self.name_entry = ctk.CTkEntry(
            content_frame,
            border_width=0,
            text_color="black",
            fg_color=srh_grey,
            font=("Arial", size_add_item_popup),
            corner_radius=corner
        )
        self.name_entry.grid(row=4, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

        # Beschädigung
        self.damage_label = tk.Label(
            content_frame,
            text="Beschädigung",
            background="white",
            font=("Arial", size_add_item_popup)
        )
        self.damage_label.grid(row=5, column=0, padx=0, pady=20, sticky=tk.E)

        self.damage_entry = ctk.CTkEntry(
            content_frame,
            border_width=0,
            text_color="black",
            fg_color=srh_grey,
            font=("Arial", size_add_item_popup),
            corner_radius=corner
        )
        self.damage_entry.grid(row=5, column=1, padx=20, pady=20, sticky=tk.E + tk.W)

        self.error_label = tk.Label(content_frame,
            text="",
            background="white",
            fg="darkred",
            font=("Arial", 14)
        )
        self.error_label.grid(row=6, column=0, columnspan=2, padx=0, pady=20, sticky=tk.E)
        print(self.__dict__)

    def __init__(self, parent: tk.Toplevel, admin_mode: bool = False):
        """
            :param tkinter.Toplevel parent:
            :param bool admin_mode:

        """
        super().__init__(
            parent,
            'Erstellen',
            background='white',
            header_text='Erstellen',
            admin_mode=admin_mode,
            size=(650, 650),
            buttons=[
                (tk.PhotoImage(file=Paths.assets_path("AbbrechenButton.png")), self.destroy),
                (tk.PhotoImage(file=Paths.assets_path("ErstellenButton.png")), self.submit_entry)
            ]
        )