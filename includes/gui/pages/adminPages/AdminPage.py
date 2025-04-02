from abc import ABC, abstractmethod

from typing_extensions import override, Callable

from includes.gui.pages import MainPage
from .AdminUserPage import *
from ..IPage import IPage
from includes.gui._styles import *
from includes.windows._sort_tree import sort_column
import customtkinter as ctk  #pip install customtkinter
from includes.util import Paths

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
        super().__init__(parent, controller, window_name=window_name, admin_mode=True)
        self.header_text = header_text
        self.admin_user_window_avatar = cache.user_avatar
        self.tree_structure = tree_structure

        from .AdminUserPage import AdminUserPage
        from .AdminRolePage import AdminRoomPage
        #from .AdminRoomPage import AdminRoomPage

        self.enable_navigation_bar(
                [
                    ('Nutzer', lambda:self.controller.show_frame(AdminUserPage)),
                    ('Räume',lambda:self.controller.show_frame(AdminRoomPage)),
                    ('Rollen', lambda:self.controller.show_frame(AdminRoomPage)),
                ]
        )
        self.enable_searchbar(lambda _: add_button_callback(), add_button_callback)
        self.apply_layout()
        self.enable_treeview(get_data_callback, select_item_callback, tree_structure)
        self.update_treeview()
        return
        self.add_btn = tk.PhotoImage(file=Paths.assets_path("Hinzusmall_blue.png"))
        self.update_treeview_with_data(None)
        self.main_treeview.bind("<Double-1>", select_item_callback)

        # Funktion für das Ereignis-Binding

        # Binde die Ereignisfunktion an die Treeview

    @override
    def setup_header_bar(self, frame: tkinter.Frame) -> None:
        """
            .
        """
        self.srh_image = tk.PhotoImage(file=Paths.assets_path("srh.png"))
        self.exit_admin_mode_button_image = tk.PhotoImage(file=Paths.assets_path("ArrowLeft.png"))
        self.options_button_image = cache.user_avatar
        self.admin_button_image = tk.PhotoImage(file=Paths.assets_path("Key.png"))

        from includes.windows.settingsWindow import pop_up_settings
        self.options_button = tk.Button(
            frame,
            image=self.options_button_image,
            command=lambda: pop_up_settings(self, self.controller),
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            bg="#DF4807",
            activebackground="#DF4807"
        )

        self.srh_image_label = tk.Label(
            frame,
            image=self.srh_image,
            background="#DF4807",
            foreground="white"
        )
        print('header text:'+self.header_text)
        self.header_text_label = tk.Label(
            frame,
            background="#DF4807",
            text=self.header_text,
            font=('Arial', 30),
            foreground="white"
        )

        self.exit_admin_mode_button = tk.Button(
            frame,
            image=self.exit_admin_mode_button_image,
            command=lambda: self.controller.show_frame(MainPage.MainPage),
            bd=0,
            cursor="hand2",
            relief=tk.FLAT,
            bg=srh_blue,
            activebackground="#DF4807"
        )

        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=0)
        frame.grid_columnconfigure(3, weight=1)
        frame.grid_columnconfigure(4, weight=0)
        frame.grid_columnconfigure(5, weight=0)
        frame.grid_rowconfigure(0, weight=3)
        frame.grid_rowconfigure(1, weight=1)

#        self.navigation_frame.grid(row=1, column=0, columnspan=5, sticky="NSWE")

        self.srh_image_label.grid(row=0, column=0, padx=20, pady=20, sticky=tk.W)
        self.header_text_label.grid(row=0, column=2, padx=0, pady=50, sticky="")
        self.options_button.grid(row=0, column=4, sticky=tk.E, padx=20)
        self.exit_admin_mode_button.grid(row=0, column=5, sticky=tk.E, padx=20)

    """
    Erstellt eine Benutzerübersichtsoberfläche für Administratoren.

    Das `AdminUserWindow` ist eine grafische Benutzeroberfläche, die Administratoren eine Übersicht
    über Benutzer bietet, zusammen mit Funktionen wie Suchen, Hinzufügen von Benutzern und
    Navigieren zu anderen Ansichtsfenstern. Diese Klasse erweitert den `tk.Frame` und konfiguriert
    ein umfassendes Layout, einschließlich eines Headers, Navigationsmenüs und eines mittleren
    Bereichs für Benutzerinteraktionen.

    :ivar srhHead: Speichert das Bild für das SRH-Logo, das im Header angezeigt wird.
    :type srhHead: tk.PhotoImage
    :ivar log_out_btn: Speichert das Bild für den Logout-Button.
    :type log_out_btn: tk.PhotoImage
    :ivar add_btn: Speichert das Bild für den "Nutzer hinzufügen"-Button.
    :type add_btn: tk.PhotoImage
    :ivar searchBtn: Speichert das Bild für den Such-Button.
    :type searchBtn: tk.PhotoImage
    """

    def __setup_searchbar(self, frame:tkinter.Frame):
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=0)

        self.add_item_button_icon = tk.PhotoImage(Paths.assets_path("Erstellen.png"))
        self.add_item_button = tk.Button(
            frame,
            image=self.add_item_button_icon,
            bd=0, relief=tk.FLAT,
            bg="white",cursor="hand2",
            activebackground="white",
        )

    def __setup_main_treeview(self,frame:tkinter.Frame, columns:list[str, str, int]):
        self.main_treeview = ttk.Treeview(
            frame,
            columns=("c1", "c2", "c3", "c4", "c5"),
            show="headings",
            cursor="hand2"
        )

        # Treeview mit Scrollbar verbinden
        self.main_treeview.configure(yscrollcommand=self.main_tree_scrollbar.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        self.main_treeview.tag_configure("oddrow", background="#f7f7f7")
        self.main_treeview.tag_configure("evenrow", background="white")

        for col_id, col_name, col_width in [
            ("# 1", "ID", 60),
            ("# 2", "Nutzername", 200),
            ("# 3", "Passwort", 200),
            ("# 4", "E-Mail", 300),
            ("# 5", "Rolle", 100)
        ]:
            self.main_treeview.column(col_id, anchor=tk.CENTER, width=col_width)
            self.main_treeview.heading(col_id, text=col_name, command=lambda c=col_id: sort_column(self.main_treeview, c, False))

        self.main_treeview.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.main_treeview.tkraise()
        self.update_treeview_with_data()

    @override
    def setup_main_frame(self, frame:tkinter.Frame) -> None:
        pass

    @override
    def setup_side_bar_left(self, frame:tkinter.Frame) -> bool:
        return False

    @override
    def setup_side_bar_right(self, frame:tkinter.Frame) -> bool:
        return False

    def on_load(self) -> None:
        pass

    @abstractmethod
    def on_cell_click(self, cell_text:str) -> None:
        """
            .
        """
        pass