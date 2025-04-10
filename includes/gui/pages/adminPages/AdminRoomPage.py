"""
    .
"""
from typing_extensions import override
from includes.sec_data_info import sqlite3api
from includes.util.Logging import Logger
from .AdminPage import AdminPage
from ...popups import AddRoomPopup
from includes.gui.pages.detailPages import RoomDetailsWindow


logger:Logger = Logger('AdminUserPage')

class AdminRoomPage(AdminPage):

    def __init__(self, parent, controller):
        super().__init__(
            parent,
            controller,
            header_text='Nutzer-Übersicht',
            window_name='dd inv',
            add_button_callback=lambda :AddRoomPopup.AddRoomPopup(self.winfo_toplevel()),
            get_data_callback=sqlite3api.fetch_all_rooms,
            tree_structure={'Raum':200, 'Ort': 300}
        )
        self.apply_layout()

    @override
    def on_cell_click(self, data) -> None:
        RoomDetailsWindow.show_room_details(data, self.controller)
