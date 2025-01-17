import math
from collections.abc import Callable
from copy import copy

from .Logging import Logger

from includes.pages.ctk_listbox import CTkListbox
from includes.sec_data_info import sqlite3api as db
import customtkinter as ctk

import json
from typing import Final
import tkinter as tk

logger:Logger = Logger('SearchbarLogic')

MAX_REPEATED_USES: Final[int] = 5
fallback_username: Final[str] = '1234'

search_is_running = False
cancel_dropdown_updates: int = 0
cancel_key_press_updates: int = 0
last_searchbar_text_length: int = 0

loaded_history: list[dict[str, str]] = []
do_on_finish: list[Callable] = []

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
            logger.debug_e(f""""{entry}" contains "{search_term} """)
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
    logger_:Logger = Logger.from_logger(logger,'update_dropdown')
    if cancel_dropdown_updates > 0:
        cancel_dropdown_updates -= 1
        logger_.debug(f"canceling dropdown update")
        return
    logger_.debug_e(f"updating dropdown")
    logger_.debug_e(f"""setting grid of dropdown""")
    try:
        dropdown.grid(padx=5, pady=5, row=0, column=0, sticky=tk.W + tk.E)
    except Exception as e:
        logger_.debug(f"""[EXCEPTION]failed to set grid of dropdown menu because of {e}""")
    logger_.debug_e(f"""successfully set grid of dropdown""")
    new_items: list[dict[str, str]] = []
    for new_item in sorted(loaded_history, key=lambda x: float(x['weight']), reverse=True):
        if new_item['text'].startswith(search_term.lower()):
            new_items.append(new_item)
    if dropdown:
        while dropdown.size() > 0:
            dropdown.delete(0, 0)
        logger_.debug_e(f"""removed all items from dropdown""")
        logger_.debug_e(f"""adding new items to dropdown from list "{new_items}" """)
        if not new_items:
            logger_.debug(f"""new items are null""")
            logger_.debug(f"""aborting dropdown update""")
            return
        try:
            i: int = 0
            for item in new_items:
                dropdown.insert(dropdown.size(), item['text'])
                logger.debug_e(f"""added "{item['text']}" to dropdown menu""")
                i = i + 1
                if i >= 3:
                    break
        except Exception as e:
            logger_.debug(f"""[EXCEPTION]failed to add item to dropdown menu because of {e}""")
            return
    else:
        logger_.debug(f"""dropdown was null""")
        logger_.debug(f"""aborting dropdown update""")
        return
    logger_.debug(f"""finished dropdown update""")


def __scale_history_weights(search_term: str) -> bool:
    """
        recalculates the 'weight' and 'repeated_uses' values of each search term of the user's history depending on their occurrences.
        The more often a term was searched for, the higher is its weight.
        The weight is decreased by applying the function f(x)= 100/(2x/a+1)-19x/40a where x is the number
        of iterations, a is a random number greater than 0 and the result is the weight.
        The repeated_uses is how many times in a row a term was searched for.
        The repeated_uses only decreases partially, even if the term isn't being searched again right away.

        Parameters:
        :param str search_term: the term the user is currently searching for

        Return:
        :return bool: whether the search term already existed in the users history
    """
    global loaded_history

    logger_:Logger = Logger.from_logger(logger,'scale history weights')

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
        logger_.debug_e(f"""processing "{text}" """)

        if text == search_term:
            weight = 100
            entry['repeated_uses'] = str(__limit_add(repeated_uses, 1, MAX_REPEATED_USES))
            entry['weight'] = str(weight)
            logger_.debug(f"""term already existed in Database and was updated to be {entry}""")
            term_existed = True
        else:
            weight = weight_function(weight, 2 + repeated_uses)
            entry['repeated_uses'] = str(__limit_sub(repeated_uses, MAX_REPEATED_USES / 20, 0))
            if weight <= 0:
                logger_.debug_e(f""" weight of "{entry['text']}" is "{weight}" """)
                loaded_history.remove(entry)
                logger_.debug_e(f"""removing entry "{entry['text']}", loaded history is "{loaded_history}" """)
            else:
                entry['weight'] = str(weight)
                logger_.debug_e(f""" weight of "{entry['text']}" is "{weight}" """)
    logger_.debug(f"""after removing unused search entries laded history is now "{loaded_history}" """)
    return term_existed


def get_most_suggested_term(search_term: str) -> str:
    for suggestion in sorted(loaded_history, key=lambda x: float(x['weight']), reverse=True):
        if suggestion['text'].startswith(search_term.lower()):
            logger.debug(f"""suggestion for current term "{search_term}" is "{suggestion}" """)
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
        logger.debug(f"""canceling 1 out of {cancel_key_press_updates} to be canceled """)
        cancel_key_press_updates -= 1
        return
    logger.debug(f"""running update search for user "{username}" with searchbar text "{search_term}" and loaded history "{loaded_history}" """)
    logger.debug(f"""chose "{__match_entries(search_term.lower())}" as new options for dropdown""")
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
    logger.debug(f"""running finishing search for user {username} with searchbar text "{search_term}" and loaded history "{loaded_history}" """)
    if not search_term == "":
        loaded_history = sorted(loaded_history, key=lambda x: x['weight'], reverse=True)
        if not __scale_history_weights(search_term.lower()):
            while len(loaded_history) >= 30:
                loaded_history.remove(loaded_history[0])
                loaded_history.pop()
            logger.debug(f"""loaded history was before "{loaded_history}" """)
            #if all(history_entry['text'] != search_term for history_entry in temp_history):
            new_entry = {'weight': '100', 'repeated_uses': '1', 'text': search_term.lower()}
            loaded_history.append(new_entry)
            logger.debug(f"""adding "{new_entry}" to search history as it didn't exist in the database""")
            logger.debug(f"""loaded history is now "{loaded_history}" """)
        logger.debug(f"""writing "{json.dumps(loaded_history)}" to database """)
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
    logger.debug_e(f""" search is  "{search_is_running}" running for user "{username}" """)


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
    logger_:Logger = Logger.from_logger(logger,'start_search')
    if search_is_running:
        update_search(dropdown, search_term, username)
    search_is_running = True
    logger_.debug(f"""starting search for user "{username}" with searchbar text "{search_term}" """)
    history_str: str = db.read_benutzer_suchverlauf(username)
    temp_history = json.loads(history_str if history_str else '[]')
    temp_history = sorted(temp_history, key=lambda x: float(x['weight']))
    logger_.debug(f"""loaded "{temp_history}" for "{username}" from database""")
    loaded_history.clear()
    for entry in temp_history:
        loaded_history.append(entry)
        logger_.debug_e(f"""adding "{entry}" to  history "{loaded_history}" """)
    logger_.debug_e(f"""complete read history "{loaded_history}" """)
    searchbar.delete(1.0, 'end-1c')
    __update_dropdown(dropdown, search_term)
    logger_.debug_e(f""" search is running "{search_is_running}" for user "{username}" """)


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
    logger.debug(f"""user "{username}" selected item "{selected_button_text}" from dropdown""")
    searchbar.delete(1.0, 'end-1c')
    cancel_key_press_updates += 1
    try:
        searchbar.insert('end', selected_button_text)
    except Exception as e:
        logger.error(f"""[EXCEPTION]failed to add text to searchbar menu because of {e}""")
    logger.debug(f"finished on dropdown select")
