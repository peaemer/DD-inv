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

    from main import ddINV
    def __init__(
        self,
        parent:tkinter.Widget|tkinter.Toplevel,
        controller:ddINV,
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

        self.enable_searchbar(lambda _: add_button_callback(), add_button_callback)
        self.enable_treeview(get_data_callback, select_item_callback, tree_structure)

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
            activebackground="#DF4807",
            text='bla'
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

#        frame.grid_columnconfigure(0, weight=0)
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

    @override
    def on_load(self) -> None:
        self.update_treeview()

    def update_treeview_with_data(self, data, columns:list[str]=None):
        """
            .
        """
        self.main_treeview.delete(*self.main_treeview.get_children())
        i = 0
        if data is None or columns is None: return

        for entry in data:
            # Bestimme das Tag für die aktuelle Zeile
            tag = "evenrow" if i % 2 == 0 else "oddrow"

            # Daten mit dem Tag in das Treeview einfügen
            self.main_treeview.insert(
                "",
                "end",
                text=f"{entry['Nutzername']}",
                values=(
                    i,
                    entry['Nutzername'],
                    entry['Passwort'],
                    entry['Email'],
                    entry['Rolle'],
                ),
                tags=(tag,)
            )
            i += 1
        logger.debug(f"USER_ERSTELLEN:{cache.user_group_data['USER_ERSTELLEN']}")
        if cache.user_group_data['USER_ERSTELLEN'] == "False":
            self.add_item_button.grid_forget()
        else:
            self.add_item_button.grid(padx=10, pady=1, row=0, column=2, sticky="w")


    @abstractmethod
    def on_cell_click(self, cell_text:str) -> None:
        """
            .
        """
        pass