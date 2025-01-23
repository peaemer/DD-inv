from collections.abc import Callable
from copy import copy
from typing import Final
from customtkinter import CTkTextbox
import tkinter as tk

from includes.util.Logging import Logger
from .._styles import srh_grey
from includes.pages.ctk_listbox import CTkListbox
from .SearchbarLogic import start_search, update_search, finish_search, get_most_suggested_term

ALLOWED_CHARACTERS: Final[list[str]] = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '_', ',', '.'
]

STOPS_FAST_MARKING: Final[list[str]] = [
    '_', ' ', ',', '.'
]

logger:Logger = Logger('Searchbar')

class Searchbar2(CTkTextbox):
    root: tk.Frame = None
    parent: tk.Frame = None
    dropdown: CTkListbox = None

    __control_down:bool = False

    __on_focus_in_commands: list[Callable[[str], None]] = []
    __on_focus_out_commands: list[Callable[[str], None]] = []
    __on_update_commands: list[Callable[[str], None]] = []
    __on_finish_commands: list[Callable[[str], None]] = []

    def __get_term(self) -> str:
        return self.get(1.0, 'end-1c')

    def __get_term_length(self) -> int:
        return len(self.__get_term())

    def __get_insert_column(self) -> int:
        return int(self.index('insert').split(".")[1])

    def __get_insert_line(self) -> int:
        return int(self.index('insert').split(".")[0])

    def __get_term_before_cursor(self) -> str:
        return copy(self.get(1.0, f"{self.__get_insert_line()}.{self.__get_insert_column()}"))

    def __get_term_after_cursor(self) -> str:
        return self.get(f'{self.__get_insert_line()}.{self.__get_insert_column()}', 'end-1c')

    def __has_tag(self, index: int, tag: str) -> bool:
        return self.tag_names(f'1.{index}')[0] == tag if self.tag_names(f'1.{index}') else False

    def __clear_autocomplete_text(self, start_index:int = 0, finish_index:int = -1) -> None:
        """
            clears all characters in the searchbar that are behind the start index and are highlighted as hint text.

            :param int start_index: position after which the hit text has to be removed.
            :param int finish_index: position until which the hit text has to be removed.
        """
        logger_:Logger = Logger.from_logger(logger, 'clear_autocomplete_text')
        if finish_index <= -1:
            finish_index = self.__get_term_length()
        if self.__get_term_length() < finish_index:
            logger_.debug(f"""start index {start_index} is greater than total term length {self.__get_term_length()} """)
            return
        while start_index < finish_index:
            if self.__has_tag(start_index, 'hint'):
                logger_.debug_e(f"""deleting text {self.get(f'1.{start_index}')} at pos {start_index}""")
                self.delete(f'1.{start_index}')
            else:
                start_index += 1
        logger_.debug_e(f"""moving cursor to {start_index}""")

    def __set_autocomplete_text(self, full_suggested_term: str) -> None:
        """
            inserts the characters of the new term, that aren't already
            in the current term, behind the cursor and highlights them.

            :param full_suggested_term: the possible completed term for the current search term.
        """
        column = self.__get_insert_column()
        self.__clear_autocomplete_text(column)
        hint_text: str = full_suggested_term.replace(self.__get_term_before_cursor().lower(), '', 1)
        if len(hint_text) > 0:
            logger.debug(f"""setting hit text "{hint_text}" """)
            self.insert('end', hint_text, 'hint')
            logger.debug_e(f"""setting mark at "1.{column}" """)
            self.mark_set("insert", f'1.{column}')

    def __on_newline_typed(self, username: str) -> None:
        """
            called when the user presses enter.
            finishes the current search process.
            calls all events that are bound via the add_on_update_finish_event method.

            :param username: the current user's username.
        """
        logger.debug("last key action was newline")
        for command in self.__on_finish_commands:
            command(self.__get_term())
        finish_search(self, self.dropdown, self.parent, self.__get_term(), username)

    def __on_tab_typed(self, username: str) -> None:
        """
            called when the user presses tab.
            moves the cursor to the most left ands marks all characters as normal

            :param username: the current user's username.
        """
        self.tag_remove('hint', 1.0, f'1.{self.__get_term_length()}')
        self.tag_remove('edit', 1.0, f'1.{self.__get_term_length()}')
        self.tag_add('normal', 1.0, f'1.{self.__get_term_length()}')
        self.mark_set("insert", f'1.{self.__get_term_length()}')
        logger.debug_e(f"""setting mark at "1.{self.__get_term_length()}" """)
        update_search(self.dropdown, self.__get_term(), username)

    def __on_escape_typed(self) -> None:
        """
            called when the user presses escape.
            clears all characters that are marked as hint text
        """
        logger.debug("last key action was escape")
        if not self.__has_tag(self.__get_insert_column() + 1, 'hint'):
            self.__on_focus_out()
        self.__clear_autocomplete_text()

    def __on_character_removed(self, username: str) -> None:
        """
                called every time a character is removed from the searchbar term.
                calls all events that are bound via the add_on_update_search_event method.

                :param str username: the current user's username
        """
        self.__clear_autocomplete_text()
        for command in self.__on_update_commands:
            command(self.__get_term())
        update_search(self.dropdown, self.__get_term(), username)

    def __on_normal_typed(self, username: str) -> None:
        """
                called every time a key is pressed that has no special function.
                calls all events that are bound via the add_on_update_search_event method.

                :param str username: the current user's username
        """
        logger.debug("last key action was a normal key")
        self.__clear_autocomplete_text(self.__get_insert_column())
        for command in self.__on_update_commands:
            command(self.__get_term())
        update_search(self.dropdown, self.__get_term(), username)
        self.__set_autocomplete_text(get_most_suggested_term(self.__get_term()))
        for command in self.__on_update_commands:
            command(self.__get_term())

    def __on_up_down_typed(self, event:tk.Event) -> None:
        """
                called every time up or down arrow was typed.
                moves the selection of the dropdown up or down in case that is possible.there are options to select from.

                :param Tk.event event: the event of the button press
        """
        logger_:Logger = Logger.from_logger(logger, 'on_up_down_typed')

        logger_.debug("last key action was either up or down arrow")
        if event.keysym == 'Up':
            if self.dropdown.selections:
                for i in range(0, len(self.dropdown.buttons)):
                    if self.dropdown.buttons[i] == self.dropdown.selections[0]:
                        logger_.debug(f":found selected button {self.dropdown.buttons[i]} at i:{i}")
                        self.dropdown.selections.clear()
                        self.dropdown.selections.append(self.dropdown.buttons[i-1 if i> 0 else 0])
            else:
                if self.dropdown.buttons:
                    self.dropdown.selections.clear()
                    self.dropdown.selections.append(self.dropdown.buttons[len(self.dropdown.buttons) - 1])

        else:
            if self.dropdown.selections:
                for i in range(0, len(self.dropdown.buttons)):
                    logger_.debug(f":found selected button {self.dropdown.buttons[i]} at i:{i}")
                    if self.dropdown.buttons[i] == self.dropdown.selections[0]:
                        self.dropdown.selections.clear()
                        self.dropdown.selections.append(self.dropdown.buttons[i])
            else:
                if self.dropdown.buttons:
                    self.dropdown.selections.clear()
                    self.dropdown.selections.append(self.dropdown.buttons[0])
        self.dropdown.update()
        #print(self.dropdown.selections)

    def __on_shortcut_typed(self, event:tk.Event) -> None:
        """
                called every time a key is pressed together with a control key
        """

        pass

    def __on_key_press(self, event: tk.Event, username: str) -> str:
        """
                called every time a key is pressed while the searchbar is focused
                depending on the key different events are called that modify the searchbar content.
                if the pressed key has no special function, it is entered at the end of the searchbar's text.

                :param str username: the current user's username
        """
        #print(event.keysym)
        if self.__control_down:
            self.__on_shortcut_typed(event)
            return 'break'
        if event.keysym == 'BackSpace':
            self.delete(f'1.{self.__get_insert_column() - 1}', f'1.{self.__get_insert_column()}')
            self.__on_character_removed(username)
        elif event.keysym == 'Delete':
            self.delete(f'1.{self.__get_insert_column()}', f'1.{self.__get_insert_column() + 1}')
            self.__on_character_removed(username)
        elif event.keysym == 'Left':
            if self.__get_insert_column() > 0:
                self.mark_set("insert", f'1.{self.__get_insert_column() - 1}')
        elif event.keysym == 'Right':
            if self.__get_insert_column() - 1 < self.__get_term_length():
                self.mark_set("insert", f'1.{self.__get_insert_column() + 1}')
        elif event.keysym == 'Up' or event.keysym == 'Down':
            self.__on_up_down_typed(event)
        elif event.keysym == 'Escape':
            self.__on_escape_typed()
        elif event.keysym == 'Return':
            self.__on_newline_typed(username)
        elif event.keysym == 'Control_L' or event.keysym == 'Control_L':
            self.__control_down = True
        else:
            if event.char == '\t':
                self.__on_tab_typed(username)
            elif event.char in ALLOWED_CHARACTERS:
                self.insert('insert', event.char)
                self.__on_normal_typed(username)
        return 'break'

    def __on_key_released(self, event: tk.Event) -> None:
        if event.keysym == 'Control_R' or event.keysym == 'Control_L':
            self.__control_down = False

    def __on_mouse_single_click(self, event: tk.Event, username:str) -> str:
        logger.debug(f"""executing on_mouse_single_click""")
        if not self.focus_get() == self:
            logger.debug_e(f"""focusing searchbar""")
            self.focus()
        self.mark_set("insert", self.index(f"@{event.x},{event.y}"))
        if (
                self.__has_tag(self.__get_insert_column(), 'edit')
                or self.__has_tag(self.__get_insert_column()-1, 'edit')
                or self.__has_tag(self.__get_insert_column(), 'hint')
                or self.__has_tag(self.__get_insert_column()-1, 'hint')
            ):
            self.delete(f'1.{self.__get_insert_column()}', f'end-1c')
            self.__on_tab_typed(username)
        return 'break'

    def __on_mouse_double_click(self) -> str:
        """

        """
        logger.debug(f"""executing on_mouse_double_click""")
        column = self.__get_insert_column()
        start:int=self.__get_insert_column()
        if self.__has_tag(column - 1, 'hint') or self.__has_tag(column +1, 'hint'):
            while start > 0:
                if self.__has_tag(start-1,'edit') or self.get(f'1.{self.__get_insert_column()}') in STOPS_FAST_MARKING:
                    break
                start-=1
        finish:int=self.__get_insert_column()
        while finish < self.__get_term_length():
            if self.__has_tag(finish,'edit') or self.get(f'1.{self.__get_insert_column()}') in STOPS_FAST_MARKING:
                break
            finish+=1

        return 'break'

    def __on_focus_in(self, dropdown: CTkListbox, username: str):
        """
            called when the searchbar gains focus.
            clears the searchbar.
            calls all events that are bound via the add_on_focus_in_event method.
        """
        logger.debug(f"""executing on_focus_in with searchbar text "{self.__get_term()}" """)
        self.delete(1.0, "end")
        start_search(self, dropdown, self.__get_term(), username)
        for command in self.__on_focus_in_commands:
            command(self.__get_term())

    def __on_focus_out(self) -> None:
        """
            called when the searchbar looses focus by another widget gaining focus or the parent frame loosing focus.
            clears the searchbar text and inserts 'Suche' with only 'normal' tag.
            calls all events that are bound via the add_on_focus_out_event method.
        """
        logger.debug(f"""executing on_focus_out with searchbar text "{self.__get_term()}" """)
        self.delete(1.0, 'end-1c')
        self.insert('end', 'Suche', tags='normal')
        self.configure(text_color='black',state='normal')
        self.parent.focus()
        for command in self.__on_focus_out_commands:
            command(self.__get_term())

    def finish_search(self, username: str) -> None:
        """
            called when the user presses newline
            stops the current search process and calls

            :param username: the current user's username

        """
        for command in self.__on_finish_commands:
            command(self.__get_term())
        finish_search(self, self.dropdown, self.parent, self.__get_term(), username)

    def add_on_focus_in_event(self, event: Callable[[str], None]) -> None:
        """
            adds a command to the listo of commands that have to be called as soon as the user clicks on the searchbar or uses keybindings to focus it

            :param Callable[[str],None] event: a command that takes the searchbar's term as a parameter

        """
        self.__on_focus_in_commands.append(event)

    def add_on_focus_out_event(self, event: Callable[[str], None]) -> None:
        """
            adds a command to the listo of commands that have to be called as soon as the user clicks any other tk widget other than the searchbar,
            or if the parent frame goes out of focus.

            :param Callable[[str],None] event: a command that takes the searchbar's term as a parameter

        """
        self.__on_focus_out_commands.append(event)

    def add_on_update_search_event(self, event: Callable[[str], None]) -> None:
        """
            adds a command to the listo of commands that have to be called everytime the searchbar content changes

            :param Callable[[str],None] event: a command that takes the searchbar's term as a parameter

        """
        self.__on_update_commands.append(event)

    def add_on_finish_search_event(self, event: Callable[[str], None]) -> None:
        """
            adds a command to the listo of commands that have to be called as soon as the search is about to be finished

            :param Callable[[str],None] event: a command that takes the searchbar's final term as a parameter

        """
        self.__on_finish_commands.append(event)

    def __init__(self, _root: tk.Frame, _parent: tk.Frame, _dropdown: CTkListbox, username: str):
        CTkTextbox.__init__(self, _parent, text_color="black", fg_color=srh_grey, bg_color="white", font=("Arial", 25),
                            corner_radius=0, border_width=0, height=0, border_spacing=0)
        self.root = _root
        self.parent = _parent
        self.dropdown = _dropdown
        self.tag_config('hint', foreground='blue', background='#c2e1ed')
        self.tag_config('edit', foreground='blue', background='#c2e1ed')
        self.tag_config('normal', foreground='black', background=srh_grey)

        self.bind('<FocusIn>', lambda _: self.__on_focus_in(self.dropdown, username))
        self.bind("<Key>", lambda event: self.__on_key_press(event, username))
        self.bind("<KeyRelease>", lambda event: self.__on_key_released(event))
        self.bind('<FocusOut>', lambda _: self.__on_focus_out())
        self.bind('<Button-1>', lambda event:self.__on_mouse_single_click(event,username))
        self.bind('<Double-Button-1>', lambda event:self.__on_mouse_double_click())
