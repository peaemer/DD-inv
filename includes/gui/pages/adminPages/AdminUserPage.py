"""
    .
"""
from typing_extensions import override
from includes.sec_data_info import sqlite3api
from includes.util.Logging import Logger
from .AdminPage import AdminPage
from ...popups import AddUserPopup

logger:Logger = Logger('AdminUserPage')

class AdminUserPage(AdminPage):
    @override
    def on_cell_click(self, cell_text:str) -> None:
        pass

    def __init__(self, parent, controller):
        super().__init__(
            parent,
            controller,
            header_text='Nutzer-Übersicht',
            window_name='dd inv',
            add_button_callback=lambda :AddUserPopup.AddUserPopup(self.winfo_toplevel()),
            get_data_callback=sqlite3api.read_all_benutzer,
            select_item_callback=None,
            tree_structure={'Name': 100, 'Passwort': 200, 'E-Mail': 300, 'Rolle': 100}
        )
        self.apply_layout()