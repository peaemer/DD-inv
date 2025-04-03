from typing_extensions import override
from includes.sec_data_info import sqlite3api
from includes.util.Logging import Logger
from .AdminPage import AdminPage
from ...popups import AddRoomPopup

logger:Logger = Logger('AdminUserPage')

class AdminRoomPage(AdminPage):

    @override
    def on_cell_click(self, cell_text:str) -> None:
        pass

    def __init__(self, parent, controller):
        super().__init__(
            parent,
            controller,
            header_text='Nutzer-Übersicht',
            window_name='dd inv',
            add_button_callback=lambda :AddRoomPopup.AddRoomPopup(self.winfo_toplevel()),
            get_data_callback=sqlite3api.fetch_all_rooms,
            select_item_callback=None,
            tree_structure={'Raum':200, 'Ort': 300}
        )
        self.apply_layout()