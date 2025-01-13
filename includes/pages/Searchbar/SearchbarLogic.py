import math
from collections.abc import Callable
from copy import copy

from includes.pages.ctk_listbox import CTkListbox
from includes.sec_data_info import sqlite3api as db
import customtkinter as ctk

import json
from typing import Final
import tkinter as tk

DEBUG_MODE: Final[bool] = True
DEBUG_MAYHEM: Final[bool] = True
MAX_REPEATED_USES: Final[int] = 5
fallback_username: Final[str] = '1234'

search_is_running = False
cancel_dropdown_updates: int = 0
cancel_key_press_updates: int = 0
last_searchbar_text_length: int = 0

loaded_history: list[dict[str, str]] = []
do_on_finish: list[Callable] = []


def __debug(message: str):
    global DEBUG_MODE
    if DEBUG_MODE: print(message)

def __debug_e(message: str):
    global DEBUG_MAYHEM
    if DEBUG_MAYHEM: print(message)


def __limit_scl(factor1: float, factor2: float,
                limit: float) -> float: return limit if factor1 * factor2 > limit else factor1 * factor2


def __limit_div(dividend: float, divisor: float,
                limit: float) -> float: return limit if dividend / divisor < limit else dividend / divisor


def __limit_add(summand1: float, summand2: float,
                limit: float) -> float: return limit if summand1 + summand2 > limit else summand1 + summand2


def __limit_sub(minuend: float, subtrahend: float,
                limit: float) -> float: return limit if minuend - subtrahend < limit else minuend - subtrahend


def __match_entries(search_term: str) -> list[dict[str, str]]:
    global loaded_history
    i: int = 0
    result: list[dict[str, str]] = []
    for entry in loaded_history:
        if entry['text'].startswith(search_term):
            result.append(entry)
            __debug_e(f"""[SearchbarLogic][__match_entries]:"{entry}" contains "{search_term} """)
            i = i + 1
            if i >= 3:
                break
    return result


def __update_dropdown(dropdown: CTkListbox, search_term: str) -> None:
    """
        shows the dropdown and sets its options to the three entries with the highes weight in the search history that start with the current searchbar text

        :param CTkListbox dropdown: the dropdown where the suggested search terms are displayed
        :param str search_term: the search term
    """
    global cancel_dropdown_updates, loaded_history
    if cancel_dropdown_updates > 0:
        cancel_dropdown_updates -= 1
        __debug(f"[SearchbarLogic][__update_dropdown]:canceling dropdown update")
        return
    __debug_e(f"[SearchbarLogic][__update_dropdown]:updating dropdown")
    __debug_e(f"""[SearchbarLogic][__update_dropdown]:setting grid of dropdown""")
    try:
        dropdown.grid(padx=5, pady=5, row=0, column=0, sticky=tk.W + tk.E)
    except Exception as e:
        __debug(f"""[EXCEPTION][SearchbarLogic][__update_dropdown]:failed to set grid of dropdown menu because of {e}""")
    __debug_e(f"""[SearchbarLogic][__update_dropdown]:successfully set grid of dropdown""")
    new_items: list[dict[str, str]] = []
    for new_item in sorted(loaded_history, key=lambda x: float(x['weight']), reverse=True):
        if new_item['text'].startswith(search_term.lower()):
            new_items.append(new_item)
    if dropdown:
        while dropdown.size() > 0:
            dropdown.delete(0, 0)
        __debug_e(f"""[SearchbarLogic][__update_dropdown]:removed all items from dropdown""")
        __debug_e(f"""[SearchbarLogic][__update_dropdown]:adding new items to dropdown from list "{new_items}" """)
        if not new_items:
            __debug(f"""[SearchbarLogic][__update_dropdown]:new items are null""")
            __debug(f"""[SearchbarLogic][__update_dropdown]:aborting dropdown update""")
            return
        try:
            i: int = 0
            for item in new_items:
                dropdown.insert(dropdown.size(), item['text'])
                __debug_e(f"""[SearchbarLogic][__update_dropdown]:added "{item['text']}" to dropdown menu""")
                i = i + 1
                if i >= 3:
                    break
        except Exception as e:
            __debug(
                f"""[EXCEPTION][SearchbarLogic][__update_dropdown]:failed to add item to dropdown menu because of {e}""")
            return
    else:
        __debug(f"""[SearchbarLogic][__update_dropdown]:dropdown was null""")
        __debug(f"""[SearchbarLogic][__update_dropdown]:aborting dropdown update""")
        return
    __debug(f"""[SearchbarLogic][__update_dropdown]:finished dropdown update""")


def __scale_history_weights(search_term: str) -> bool:
    """
        recalculates the 'weight' and 'repeated_uses' values of each search term of the user's history depending on their occurrences.
        The more often a term was searched for, the higher is its weight.
        The weight is decreased by applying the function f(x)= 100/(2x/a+1)-19x/40a where x is the number
        of iterations, a is a random number greater than 0 and the result is the weight.
        The repeated_uses is how many times in a row a term was searched for. The repeated_uses only decreases partially, even if the term isn't being searched again right away.

        Parameters:
        :param str search_term: the term the user is currently searching for

        Return:
        :return bool: whether the search term already existed in the users history
    """
    global loaded_history

    def weight_function(y: float, a: float) -> float:
        """
                the function for decreasing the weight in its recursive form

                :param float y: the y value of the function at x-1
                :param float a: a parameter that determines that the x-axis intersection is at ~ 10*a
        """
        return (
                (3800 * a) / (a * math.sqrt(6400 * math.pow(y, 2) - 3040 * y + 608361) - 80 * a * y + 19 * (a + 4)) -
                (a * math.sqrt(6400 * math.pow(y, 2) - 3040 * y + 608361) - 80 * a * y - 19 * (a - 4)) / (160 * a)
        )

    if len(loaded_history) == 0:
        return False
    term_existed: bool = False
    for entry in loaded_history:
        weight: float = float(entry['weight']) if entry['weight'] else 0
        repeated_uses: float = float(entry['repeated_uses']) if entry['repeated_uses'] else 0
        text: str = entry['text'] if entry['text'] else ''
        __debug_e(f"""[SearchbarLogic]:processing "{text}" """)

        if text == search_term:
            weight = 100
            entry['repeated_uses'] = str(__limit_add(repeated_uses, 1, MAX_REPEATED_USES))
            entry['weight'] = str(weight)
            __debug(
                f"""[SearchbarLogic][__scale__history_weights]:term already existed in Database and was updated to be {entry}""")
            term_existed = True
        else:
            weight = weight_function(weight, 2 + repeated_uses)
            entry['repeated_uses'] = str(__limit_sub(repeated_uses, MAX_REPEATED_USES / 20, 0))
            if weight <= 0:
                __debug_e(f"""[SearchbarLogic][__scale__history_weights]: weight of "{entry['text']}" is "{weight}" """)
                loaded_history.remove(entry)
                __debug_e(
                    f"""[SearchbarLogic][__scale__history_weights]:removing entry "{entry['text']}", loaded history is "{loaded_history}" """)
            else:
                entry['weight'] = str(weight)
                __debug_e(f"""[SearchbarLogic][__scale__history_weights]: weight of "{entry['text']}" is "{weight}" """)
    __debug(
        f"""[SearchbarLogic][__scale__history_weights]:after removing unused search entries laded history is now "{loaded_history}" """)
    return term_existed


def get_most_suggested_term(search_term: str) -> str:
    for suggestion in sorted(loaded_history, key=lambda x: float(x['weight']), reverse=True):
        if suggestion['text'].startswith(search_term.lower()):
            __debug(
                f"""[SearchbarLogic][get_most_suggested_term]:suggestion for current term "{search_term}" is "{suggestion}" """)
            return copy(suggestion['text'])
    return ''


def update_search(dropdown: CTkListbox, search_term: str, username: str) -> None:
    """
        called when the searchbar text changed like the user typing an additional character into the search bar .

        :param CTkListbox dropdown: the dropdown where the suggested search terms are displayed
        :param str search_term: the current search term
        :param str username: the current user's username
    """
    global search_is_running, cancel_key_press_updates
    if not search_is_running:
        return
    if cancel_key_press_updates > 0:
        __debug(f"""[SearchbarLogic][update searchbar]:canceling 1 out of {cancel_key_press_updates} to be canceled """)
        cancel_key_press_updates -= 1
        return
    __debug(f"""[SearchbarLogic][update searchbar]:running update search for user "{username}" with searchbar text "{search_term}" and loaded history "{loaded_history}" """)
    __debug(f"""[SearchbarLogic][update_search]:chose "{__match_entries(search_term.lower())}" as new options for dropdown""")
    __update_dropdown(dropdown, search_term)


def finish_search(searchbar: ctk.CTkTextbox, dropdown: CTkListbox, root: tk.Frame, search_term: str,
                  username: str) -> None:
    """
        Called once user stops typing into the search bar.
        Recalculates the weight and repeated_uses of the last 30 terms the user searched for.
        In case the term wasn't searched for already, adds the term to the users search history with weight=100 and repeated_uses=1
        if the user has more than 30 terms in his search history, strips away the least likely terms of the users search history.

        Parameters:
        :param tk.Entry searchbar: the search bar where the user is typing in
        :param CTkListbox dropdown: the dropdown where the suggested search terms are displayed
        :param tk.Frame root: the root of th searchbar
        :param str search_term: the current search term
        :param str username: the current user's username
    """
    global search_is_running, cancel_key_press_updates, loaded_history, do_on_finish
    if not search_is_running:
        return
    __debug(
        f"""[SearchbarLogic]:running finishing search for user {username} with searchbar text "{search_term}" and loaded history "{loaded_history}" """)
    if not search_term == "":
        loaded_history = sorted(loaded_history, key=lambda x: x['weight'], reverse=True)
        if not __scale_history_weights(search_term.lower()):
            while len(loaded_history) >= 30:
                loaded_history.remove(loaded_history[0])
                loaded_history.pop()
            __debug(f"""[SearchbarLogic]:loaded history was before "{loaded_history}" """)
            #if all(history_entry['text'] != search_term for history_entry in temp_history):
            new_entry = {'weight': '100', 'repeated_uses': '1', 'text': search_term.lower()}
            loaded_history.append(new_entry)
            if DEBUG_MODE: print(f"""[SearchbarLogic]:adding: "{new_entry}" to search history as it didn't exist in the database""")
            __debug(f"""[SearchbarLogic]:loaded history is now "{loaded_history}" """)
        __debug(f"""[SearchbarLogic]: writing "{json.dumps(loaded_history)}" to database """)
        db.update_benutzer(username, neue_suchverlauf=json.dumps(loaded_history))
    searchbar.delete(0.0, 'end-1c')
    dropdown.grid_forget()
    cancel_key_press_updates = 0
    root.focus()
    new_tree_data: list[dict[str, str]] = []
    for hardware in db.fetch_hardware():
        for parameter in enumerate(hardware):
            if search_term in str(parameter):
                new_tree_data.append(hardware)
    if len(do_on_finish) > 0:
        for do in do_on_finish:
            do()
    search_is_running = False
    __debug_e(f"""[SearchbarLogic]: search is  "{search_is_running}" running for user "{username}" """)


def start_search(searchbar: ctk.CTkTextbox, dropdown: CTkListbox, search_term: str, username: str) -> None:
    """
        called when the user starts typing into the search bar.
        loads the user's search history from the database

        Parameters:
        :param tk.Entry searchbar: the search bar where the user is typing in
        :param CTkListbox dropdown: the dropdown where the suggested search terms are displayed
        :param str search_term: the current search term
        :param str username: the current user's username
    """
    global search_is_running, cancel_key_press_updates, loaded_history
    if search_is_running:
        update_search(dropdown, search_term, username)
    search_is_running = True
    __debug(f"""[SearchbarLogic]:starting search for user "{username}" with searchbar text "{search_term}" """)
    history_str: str = db.read_benutzer_suchverlauf(username)
    temp_history = json.loads(history_str if history_str else '[]')
    temp_history = sorted(temp_history, key=lambda x: float(x['weight']))
    __debug(f"""[SearchbarLogic]:loaded "{temp_history}" for "{username}" from database""")
    loaded_history.clear()
    for entry in temp_history:
        loaded_history.append(entry)
        __debug_e(f"""[SearchbarLogic]:adding "{entry}" to  history "{loaded_history}" """)
    __debug_e(f"""[SearchbarLogic]:complete read history "{loaded_history}" """)
    searchbar.delete(1.0, 'end-1c')
    __update_dropdown(dropdown, search_term)
    __debug_e(f"""[SearchbarLogic]: search is running "{search_is_running}" for user "{username}" """)


def on_dropdown_select(searchbar: ctk.CTkTextbox, dropdown: CTkListbox, username: str) -> None:
    """
        called when a dropdown entry is clicked.
        replaces the entire searchbar text with the text of the entry that was clicked.

        :param searchbar: the search bar where the user is typing in
        :param CTkListbox dropdown: the dropdown where the suggested search terms are displayed
        :param str username: the current user's username
    """
    global search_is_running, cancel_key_press_updates
    if not search_is_running:
        return
    selected_button_text = dropdown.get(dropdown.curselection())
    __debug(f"""[SearchbarLogic]:user "{username}" selected item "{selected_button_text}" from dropdown""")
    searchbar.delete(1.0, 'end-1c')
    cancel_key_press_updates += 1
    try:
        searchbar.insert('end', selected_button_text)
    except Exception as e:
        print(f"""[EXCEPTION][SearchbarLogic][__update_dropdown]:failed to add text to searchbar menu because of {e}""")
    __debug(f"[SearchbarLogic][OnDropdownSelect]:finished on dropdown select")
