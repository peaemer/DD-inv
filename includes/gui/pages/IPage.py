"""
    .
"""
import tkinter
from abc import ABC, abstractmethod
from tkinter import ttk
from typing import Callable, Any

import customtkinter
from customtkinter import CTkEntry

import cache
from includes.util import Paths
from includes.util.Logging import Logger
from includes.windows.Searchbar import SearchbarLogic
from includes.windows.Searchbar.Searchbar import Searchbar
from includes.gui.styles import *
from includes.windows.ctk_listbox import CTkListbox

logger:Logger = Logger('IPage')

class IPage(tkinter.Frame, ABC):
    """
        This is the base class for all window frames. It sets up the general arrangement of the frames of the Window.
        The frames are the header frame at the top of the window, the two sidebar frames and the main frame in the
        middle of the window. Classes that inherit from IWindow can access these frames only through the setup methods.
        The frames are created inside the constructor of IWindow.
    """

    def __init__(self, parent:tkinter.Widget, controller:Any,window_name:str='', header_text:str='', admin_mode:bool=False):
        """
            :param tkinter.Toplevel|tkinter.Frame parent:
            :param bool admin_mode:

        """
        super().__init__(parent, background='white',name=window_name)
        self.controller = controller
        self.parent = parent
        self.header_text = header_text
        self.admin_mode = admin_mode

        self.__header_frame:tkinter.Frame = tkinter.Frame(self, background=srh_orange if admin_mode else srh_blue)
        self.__header_buttons_frame_right:tkinter.Frame = tkinter.Frame(self.__header_frame, background=srh_orange if admin_mode else srh_blue)
        self.__header_buttons_frame_left:tkinter.Frame = tkinter.Frame(self.__header_frame, background=srh_orange if admin_mode else srh_blue)

        self.__navigation_bar_frame:tkinter.Frame = tkinter.Frame(self, background=srh_grey)
        self.__searchbar_frame:tkinter.Frame = tkinter.Frame(self, background='white')
        self.__dropdown_overlay_frame:tkinter.Frame = tkinter.Frame(self, background='white')

        self.__center_frame:tkinter.Frame = tkinter.Frame(self, background='white')
        self.__left_bar_frame:tkinter.Frame = tkinter.Frame(self, background='white')
        self.__right_bar_frame:tkinter.Frame = tkinter.Frame(self, background='white')

        self.navigation_buttons: list[customtkinter.CTkButton] = []

        self.search_button_image:tkinter.PhotoImage|None = None
        self.add_item_button_image:tkinter.PhotoImage|None = None

        self.add_item_button:tkinter.Button|None = None
        self.search_button:tkinter.Button|None = None

        self.search_entry_oval:CTkEntry|None = None
        self.search_entry:Searchbar|None = None
        self.dropdown:CTkListbox|None = None

        self.__searchbar_enabled: bool = False
        self.__navigation_bar_enabled: bool = False
        self.__treeview_enabled: bool = False

        self.__overlay_left_sidebar:bool = self.setup_side_bar_left(self.__left_bar_frame)
        self.__overlay_right_sidebar:bool = self.setup_side_bar_right(self.__right_bar_frame)
        self.__hide_left_sidebar:bool = False
        self.__hide_right_sidebar:bool = False

        self.__get_treeview_data_callback:Callable[[],list[dict[str,str]]]|None = None
        self.__on_cell_click_callback: Callable[[dict[str,str|list[str]]],None] | None = None

        self.__treeview_structure:dict[str,int]|None = None

        self.after(0, self.setup_header_bar, self.__header_frame)
        self.after(0, self.setup_main_frame, self.__center_frame)

        self.apply_layout()

    def __sort_column(self, col, reverse:bool=False):
        """
        Sortiert die Einträge einer Spalte in einer `ttk.Treeview`-Tabelle.

        Diese Funktion sortiert die Inhalte der angegebenen Spalte entweder numerisch oder alphanumerisch,
        abhängig vom Datentyp der Spaltenwerte. Zusätzlich wird die Reihenfolge der Einträge im Treeview
        aktualisiert, und die Tags für "oddrow" (ungerade Zeilen) und "evenrow" (gerade Zeilen) werden
        entsprechend neu gesetzt. Der Header der Spalte wird so konfiguriert, dass ein Klick auf den Header
        die Sortierrichtung umkehrt.

        Args:
            col (str): Der Name der zu sortierenden Spalte.
            reverse (bool, optional): Gibt an, ob die Sortierung in umgekehrter Reihenfolge erfolgen soll.
                Standardmäßig False für aufsteigende Sortierung.

        Raises:
            ValueError: Falls beim Überprüfen von numerischen Werten ein unerwarteter Typ auftritt.

        Notes:
            - Die Funktion überprüft, ob alle Werte in der Spalte numerisch sind (sofern nicht leer)
              und wählt basierend darauf die geeignete Sortierlogik (numerisch oder alphanumerisch).
            - Nach der Sortierung werden die Tags für "oddrow" und "evenrow" neu gesetzt, um ein visuelles
              Unterscheiden der Zeilen zu ermöglichen.
            - Die Funktion modifiziert den Header der Spalte, sodass beim nächsten Klick die Sortierrichtung
              umgekehrt wird.
        """
        if self.treeview is None:
            return
        # Daten aus der Treeview abrufen
        data = [(self.treeview.set(item, col), item) for item in self.treeview.get_children('')]

        # Prüfen, ob die Spalte hauptsächlich numerische Daten enthält
        def is_numeric(value):
            """."""
            try:
                float(value)
                return True
            except ValueError:
                return False

        # Entscheiden, ob die Spalte als Zahl oder Text sortiert werden soll
        if all(is_numeric(row[0]) for row in data if row[0] != ''):
            key_func = lambda x: float(x[0])
        else:
            key_func = lambda x: str(x[0])

        # Daten sortieren
        data.sort(key=key_func, reverse=reverse)

        # Reihenfolge in der Treeview aktualisieren
        for index, (_, item) in enumerate(data):
            self.treeview.move(item, "", index)

        # Tags für odd/even-Reihen neu setzen
        for index, item in enumerate(self.treeview.get_children('')):
            tag = "oddrow" if index % 2 == 0 else "evenrow"
            self.treeview.item(item, tags=(tag,))

        # Header aktualisieren, um Sortierrichtung zu wechseln
        self.treeview.heading(col, command=lambda c=col: self.__sort_column(c, not reverse))

    @abstractmethod
    def setup_main_frame(self, frame:tkinter.Frame) -> None:
        """
            All Subclasses o fIWindow must override this method.
            Code that adds content to the main frame should be called in this method.
        """

    @abstractmethod
    def setup_header_bar(self, frame:tkinter.Frame) -> None:
        """
            All Subclasses o fIWindow must override this method.
            Code that adds content to the header frame should be called in this method.
        """

    @abstractmethod
    def setup_side_bar_left(self, frame:tkinter.Frame) -> bool:
        """
            All Subclasses o fIWindow must override this method.
            Code that adds content to the frame of the left sidebar should be called in this method.
            If the method returns True, the left sidebar will go from the bottom up to the top of the window, by
            narrowing the header frame.
            If the method returns False, the left sidebar will start from the bottom of the window and end at the bottom of the
            header frame. The header frame will extend to the left of the window.
        """

    @abstractmethod
    def setup_side_bar_right(self, frame:tkinter.Frame) -> bool:
        """
            All Subclasses o fIWindow must override this method.
            Code that adds content to the frame of the right sidebar should be called in this method.
            If the method returns True, the right sidebar will go from the bottom up to the top of the window, by
            narrowing the header frame.
            If the method returns False, the right sidebar will start from the bottom of the window and end at the bottom of the
            header frame. The header frame will extend to the right of the window.
        """

    def update_treeview(self, data:list[dict[str,str]]= None) -> None:
        """
            .
        """
        if not self.__treeview_enabled:
            logger.error('no treeview enabled')
            return
        else:
            logger.debug('update treeview')
            self.treeview.delete(*self.treeview.get_children())

            i:int=0
            for row in data if data else self.__get_treeview_data_callback():
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                l:list[str] = []
                for enumerated in enumerate(row.keys()):
                    l.append(row[enumerated[1]])
                self.treeview.insert(
                    "",
                    "end",
                    tags=(tag,),
                    values=tuple(l)
                )
                i += 1
            logger.debug('finished update treeview')

    def set_treeview_columns(self):
        """
            .
        """
        if self.treeview['columns']:
            self.treeview['columns'] = tuple([f"c{i}" for i in range(0,len(self.__treeview_structure))])
        i:int=1
        print(self.__treeview_structure)
        for column_name in enumerate(self.__treeview_structure.keys()):
            self.treeview.column(f'# {i}', anchor=tkinter.CENTER, width=self.__treeview_structure[column_name[1]])
            self.treeview.heading(f'# {i}', text=column_name[1], command=lambda c=f'# {i}': self.__sort_column(c, True))
            i+=1

    def enable_treeview(
            self,
            get_data_callback:Callable[[],list[dict[str,str]]],
            on_cell_click_callback:Callable[[dict[str,str]],None],
            tree_structure:dict[str,int]
    ):
        """
            .
        """
        self.__treeview_enabled = True
        self.__treeview_structure = tree_structure

        self.treeview:ttk.Treeview = ttk.Treeview(
            self.__center_frame,
            columns=tuple([f"c{i}" for i in range(0,len(tree_structure if tree_structure else self.__treeview_structure))]),
            show="headings"
        )

        self.tree_scrollbar = customtkinter.CTkScrollbar(
            self.__center_frame,
            orientation="vertical",
            command=self.treeview.yview,
            fg_color="white",
            width=20,  # <--- +++++side scrollbar visibility+++++ #
            corner_radius=scroll_corner,
            button_color=srh_grey,
            button_hover_color=srh_blue
        )
        self.horizontal_tree_scrollbar = customtkinter.CTkScrollbar(
            self.__center_frame,
            orientation="horizontal",
            command=self.treeview.xview,
            fg_color="white",
            height=20,  # <--- +++++side scrollbar visibility+++++ #
            corner_radius=scroll_corner,
            button_color=srh_grey,
            button_hover_color=srh_blue
        )

        self.set_treeview_columns()

        if callable(get_data_callback):
            self.__get_treeview_data_callback = get_data_callback
        else:
            def callback():
                """a callback that returns an empty data dictionary"""
                return {}
            self.__get_treeview_data_callback = callback

        if callable(on_cell_click_callback):
            self.__on_cell_click_callback = on_cell_click_callback
        else:
            pass

        def callback():
            """a callback that returns an empty data dictionary"""
            print(self.treeview.item(self.treeview.focus()))
        self.__on_cell_click_callback = callback

        #self.treeview.bind("<Double-1>", lambda _:self.__on_click_callback(self.treeview.item(self.treeview.focus())))
        self.treeview.bind("<Double-1>", lambda _:self.__on_cell_click_callback())

        self.__center_frame.grid_rowconfigure(0, weight=1)
        self.__center_frame.grid_rowconfigure(1, weight=0)
        self.__center_frame.grid_columnconfigure(0, weight=1)
        self.__center_frame.grid_columnconfigure(1, weight=0)

        self.treeview.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.tree_scrollbar.grid(row=0, rowspan=2, column=1, sticky='NS')
        self.horizontal_tree_scrollbar.grid(row=1, column=0, sticky='WE')

        self.treeview.tkraise()
        self.apply_layout()
        self.update_treeview()

    def enable_navigation_bar(self, buttons:list[tuple[str, Callable]]):
        """
            .
        """
        if self.__navigation_bar_enabled:
            raise RuntimeError('enable_navigation_bar was called twice')
        self.__navigation_bar_enabled = True
        for button_text, button_callback in buttons:
            self.navigation_buttons.append(
                customtkinter.CTkButton(
                    self.__navigation_bar_frame,
                    text=button_text,
                    border_width=border,
                    command=button_callback,
                    cursor="hand2",
                    corner_radius=corner,
                    fg_color='#a9a9a9',
                    text_color="black",
                    font=("Arial", 20),
                    hover_color=nav_bar_hover_color
                )
            )
            self.__navigation_bar_frame.grid_columnconfigure(len(self.navigation_buttons) - 1, weight=1)
            self.navigation_buttons[-1].grid(row=0, padx=40, pady=15, column=len(self.navigation_buttons) - 1,sticky='WE')
        self.apply_layout()

    def select_on_search(self, search_term:str):
        """
            .
        """
        search_entries = []
        for entry in self.__get_treeview_data_callback():
            for value in entry:
                if search_term in str(entry[value]).lower():
                    if entry not in search_entries:
                        search_entries.append(entry)
        self.update_treeview(data=search_entries)

    def enable_searchbar(self, add_item_callback:Callable) -> None:
        """
            creates a frame on top of the center frame.
            it contains a search button, the actual searchbar and a button for adding items.


        """
        if self.__searchbar_enabled:
            raise RuntimeError('enable_navigation_bar was called twice')
        self.__searchbar_enabled = True

        self.search_button_image = tkinter.PhotoImage(file=Paths.assets_path('SearchButton.png'))

        self.search_button = tkinter.Button(
            self.__searchbar_frame,
            image=self.search_button_image,
            bd=0, relief=tkinter.FLAT,
            bg="white",cursor="hand2",
            activebackground="white",
            command=lambda:self.search_entry.finish_search(cache.user_name)
        )

        self.add_item_button_image = tkinter.PhotoImage(file=Paths.assets_path("Erstellen.png"))

        self.add_item_button = tkinter.Button(
            self.__searchbar_frame,
            image=self.add_item_button_image,
            bd=0, relief=tkinter.FLAT,
            bg="white",cursor="hand2",
            activebackground="white",
            command=add_item_callback
        )

        #erstelle den hinufügen-button im auf dem search frame
        self.dropdown: CTkListbox = CTkListbox(
            self.__dropdown_overlay_frame,
            font=("Arial", 20),
            text_color='black',
            bg_color="white",
            border_color=srh_grey,
            corner_radius=10,
            scrollbar_fg_color="white",
            scrollbar_button_color='white',
            scrollbar_button_hover_color='white'
        )

        self.search_entry_oval:CTkEntry = CTkEntry(
            self.__searchbar_frame,
            text_color="black",
            fg_color=srh_grey,
            bg_color="white",
            font=("Arial", 26),
            corner_radius=20,
            border_width=0,
            height=25
        )

        self.search_entry:Searchbar = Searchbar(
            self,
            self.__searchbar_frame,
            self.dropdown,
            cache.user_name
        )

        self.__searchbar_frame.grid_columnconfigure(0, weight=0)
        self.__searchbar_frame.grid_columnconfigure(1, weight=1)
        self.__searchbar_frame.grid_columnconfigure(2, weight=0)

        # setze die grid Layouts der buttons und der Suchleiste im search-frame
        self.search_button.grid(padx=5, pady=5, row=0, column=0)
        self.add_item_button.grid(padx=5, pady=5, row=0, column=2)
        self.search_entry.grid(column=1, row=0, columnspan=1, sticky='WE', padx=26, pady=20)
        self.search_entry_oval.grid(column=1, row=0, columnspan=1, sticky='WE', padx=5, pady=5)
        self.dropdown.grid(padx=0, pady=5, row=0, column=0)

        self.search_entry_oval.bind('<FocusIn>', lambda  _: self.search_entry.focus())
        self.search_entry.add_on_focus_in_event(lambda  _: self.__dropdown_overlay_frame.tkraise(self.__center_frame))
        self.search_entry.add_on_focus_out_event(lambda _: self.__center_frame.tkraise(self.__dropdown_overlay_frame))
        self.search_entry.add_on_finish_search_event(lambda _: self.select_on_search(self.search_entry.get(0.0,'end-1c')))
        self.dropdown.bind("<<ListboxSelect>>", lambda var: SearchbarLogic.on_dropdown_select(self.search_entry, self.dropdown, cache.user_name))
        self.dropdown.bind("<<ListboxSelect>>", lambda var: self.__center_frame.tkraise(self.__dropdown_overlay_frame))

        self.search_entry.insert('end', 'Suche', tags='normal')
        self.__center_frame.tkraise(self.__dropdown_overlay_frame)
        self.apply_layout()

    def toggle_left_sidebar(self):
        """."""
        self.__hide_left_sidebar = not self.__hide_left_sidebar
        self.apply_layout()

    def toggle_right_sidebar(self):
        """."""
        self.__hide_right_sidebar = not self.__hide_right_sidebar
        self.apply_layout()

    def apply_layout(self):
        """
            arrange the default items depending on which ones are ment to be shown
        """
        logger.debug('apply layout')
        self.__header_frame.grid(
            row=0,
            columnspan=3,
            column=0,
            sticky='NSWE'
        )
        self.__left_bar_frame.grid(
            column=0,
            rowspan=1 + (1 if self.__overlay_left_sidebar else 0) + (1 if self.__searchbar_enabled else 0) + (1 if self.__overlay_left_sidebar and self.__searchbar_enabled else 0) + (1 if self.__overlay_left_sidebar and self.__navigation_bar_enabled else 0),
            row=(0 if self.__overlay_left_sidebar else 1) + (1 if self.__navigation_bar_enabled and not self.__overlay_left_sidebar else 0),
            sticky='NSWE'
        )

        self.__right_bar_frame.grid(
            column=2,
            rowspan=1 + (1 if self.__overlay_right_sidebar else 0) + (1 if self.__searchbar_enabled else 0) + (1 if self.__overlay_right_sidebar and self.__searchbar_enabled else 0) + (1 if self.__overlay_right_sidebar and self.__navigation_bar_enabled else 0),
            row=(0 if self.__overlay_right_sidebar else 1) + (1 if self.__navigation_bar_enabled and not self.__overlay_right_sidebar else 0),
            sticky='NSWE'
        )

        if self.__navigation_bar_enabled:
            self.__navigation_bar_frame.grid(
                row=1,
                column=1 if self.__overlay_left_sidebar else 0,
                columnspan=3 - (1 if self.__overlay_left_sidebar else 0) - (1 if self.__overlay_right_sidebar else 0),
                sticky='NSWE'
            )

        if self.__searchbar_enabled:
            self.__searchbar_frame.grid(
                row=2 if self.__navigation_bar_enabled else 1,
                column=1,
                padx=20,
                sticky='NSWE'
            )
            self.__dropdown_overlay_frame.grid(
                row=1 + (1 if self.__searchbar_enabled else 0) + (1 if self.__navigation_bar_enabled else 0),
                column=1,
                padx=(90, 180),
                pady = 0,
                sticky='NWE'
            )

        self.__center_frame.grid(
            row=1 + (1 if self.__searchbar_enabled else 0) + (1 if self.__navigation_bar_enabled else 0),
            column=1,
            padx=10,
            pady=(0,10),
            sticky='NSWE'
        )

        self.grid_columnconfigure(0, weight=0 if self.__hide_left_sidebar else 1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_columnconfigure(2, weight=0 if self.__hide_left_sidebar else 1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0 if self.__navigation_bar_enabled or self.__searchbar_enabled else 4)
        self.grid_rowconfigure(2, weight=4 if self.__navigation_bar_enabled ^ self.__searchbar_enabled else 0)
        self.grid_rowconfigure(3, weight=4 if self.__navigation_bar_enabled and self.__searchbar_enabled else 0)

        self.__center_frame.tkraise(self.__dropdown_overlay_frame)

    def on_load(self):
        """
            Subclasses o fIWindow can optionally override this method.
            It is called everytime a page is shown again by the current DdInv instance
        """
        if self.__treeview_enabled:
            self.set_treeview_columns()
            self.update_treeview()
        self.apply_layout()