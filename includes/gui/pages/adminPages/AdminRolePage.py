"""
    .
"""
from typing_extensions import override
from includes.sec_data_info import sqlite3api
from includes.util.Logging import Logger
from .AdminPage import AdminPage
from ...popups import AddRolePopup

logger:Logger = Logger('AdminRolePage')

class AdminRolePage(AdminPage):

    @override
    def on_cell_click(self, cell_text:str) -> None:
        pass

    def __init__(self, parent, controller):
        super().__init__(
            parent,
            controller,
            header_text='Nutzer-Übersicht',
            window_name='dd inv',
            add_button_callback=lambda :AddRolePopup.AddRolePopup(self.winfo_toplevel()),
            get_data_callback=sqlite3api.read_all_rollen,
            select_item_callback=None,
            tree_structure={
                'Rolle': 250, 'Rolle Löschbar': 200, 'Admin Feature': 150, 'Ansehen': 150, 'Löschen': 90,
                'Bearbeiten': 100, 'Erstellen': 100, 'Gruppe Löschen': 160, 'Gruppe Erstellen': 160,
                'Gruppe Bearbeiten': 190, 'Rollen Erstellen': 170, 'Rollen Bearbeiten': 170,
                'Rollen Löschen': 160, 'User Löschen': 160, 'User Bearbeiten': 190, 'User Erstellen': 160
            }
        )
        self.apply_layout()