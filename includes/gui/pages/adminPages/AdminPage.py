from abc import ABC, abstractmethod

from typing_extensions import Callable, override
import tkinter
import cache

from includes.gui.pages import MainPage
from ..IPage import IPage
from includes.gui.styles import *
from includes.util import Paths
from includes.util.Logging import Logger

logger:Logger = Logger('AdminPage')


# Hauptseite (zweites Fenster)
class AdminPage(IPage, ABC):

    from main import DdInv
    def __init__(
        self,
        parent:tkinter.Widget|tkinter.Toplevel,
        controller:DdInv,
        add_button_callback:Callable,
        get_data_callback:Callable|None,
        select_item_callback:Callable|None,
        tree_structure:dict[str,int],
        window_name:str='',
        header_text:str='',
    ):
        """
            .
        """
        super().__init__(parent, controller, window_name=window_name, header_text=header_text, admin_mode=True)
        self.header_text = header_text
        self.admin_user_window_avatar = cache.user_avatar
        self.tree_structure = tree_structure

        from .AdminUserPage import AdminUserPage
        from .AdminRoomPage import AdminRoomPage
        from .AdminRolePage import AdminRolePage

        self.enable_navigation_bar(
            [
                ('Nutzer', lambda:self.controller.show_frame(AdminUserPage)),
                ('Räume',lambda:self.controller.show_frame(AdminRoomPage)),
                ('Rollen', lambda:self.controller.show_frame(AdminRolePage)),
            ]
        )

        def on_finish_search(search_term:str) -> None:
            pass

        self.enable_searchbar(on_finish_search, add_button_callback)
        self.toggle_right_sidebar()
        self.toggle_left_sidebar()
        self.apply_layout()
        self.enable_treeview(get_data_callback, select_item_callback, tree_structure)
        self.update_treeview()

    @override
    def setup_header_bar(self, frame: tkinter.Frame) -> None:
        """
            .
        """
        self.srh_image = tkinter.PhotoImage(file=Paths.assets_path("srh.png"))
        self.exit_admin_mode_button_image = tkinter.PhotoImage(file=Paths.assets_path("ArrowLeft.png"))
        self.options_button_image:tkinter.PhotoImage = cache.user_avatar
        self.admin_button_image = tkinter.PhotoImage(file=Paths.assets_path("Key.png"))

        from includes.windows.settingsWindow import pop_up_settings
        self.options_button = tkinter.Button(
            frame,
            image=self.options_button_image,
            command=lambda: pop_up_settings(self, self.controller),
            bd=0,
            relief=tkinter.FLAT,
            cursor="hand2",
            bg=srh_blue,
            activebackground="#DF4807"
        )

        self.srh_image_label = tkinter.Label(
            frame,
            image=self.srh_image,
            background=srh_blue,
            foreground="white"
        )
        self.header_text_label = tkinter.Label(
            frame,
            background=srh_blue,
            text=self.header_text,
            font=('Arial', 30),
            foreground="white"
        )

        self.exit_admin_mode_button = tkinter.Button(
            frame,
            image=self.exit_admin_mode_button_image,
            command=lambda: self.controller.show_frame(MainPage.MainPage),
            bd=0,
            cursor="hand2",
            relief=tkinter.FLAT,
            bg=srh_blue,
            activebackground="#DF4807"
        )
        frame.config(bg=srh_blue)

        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=0)
        frame.grid_columnconfigure(3, weight=1)
        frame.grid_columnconfigure(4, weight=0)
        frame.grid_columnconfigure(5, weight=0)
        frame.grid_rowconfigure(0, weight=3)
        frame.grid_rowconfigure(1, weight=1)

#        self.navigation_frame.grid(row=1, column=0, columnspan=5, sticky="NSWE")

        self.srh_image_label.grid(row=0, column=0, padx=20, pady=20, sticky='W')
        self.header_text_label.grid(row=0, column=2, padx=0, pady=50, sticky='')
        self.options_button.grid(row=0, column=4, sticky='E', padx=20)
        self.exit_admin_mode_button.grid(row=0, column=5, sticky='E', padx=20)

    @override
    def on_load(self):
        super().on_load()

    @override
    def setup_main_frame(self, frame:tkinter.Frame) -> None:
        pass

    @override
    def setup_side_bar_left(self, frame:tkinter.Frame) -> bool:
        return False

    @override
    def setup_side_bar_right(self, frame:tkinter.Frame) -> bool:
        return False

    @abstractmethod
    def on_cell_click(self, cell_text:str) -> None:
        """
            .
        """
        pass