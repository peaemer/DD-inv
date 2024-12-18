from .ctk_listbox import CTkListbox #muss über 'pip install CTkListbox' installiert werden
import customtkinter as ctk

from ..sec_data_info import sqlite3api as db
import json
from typing import List,Dict, Final
import tkinter as tk

DEBUG_MODE:Final[bool] = False
MAX_REPEATED_USES:Final[int] = 10

search_is_running = False
fallback_username = 'Alex'

cancel_dropdown_updates:int = 0
cancel_key_press_updates:int = 0

def __limit_scl(factor1:float, factor2:float, limit:float)->float: return limit if factor1*factor2 > limit else factor1 * factor2
def __limit_div(dividend:float, divisor:float, limit:float)->float: return limit if dividend / divisor < limit else dividend / divisor
def __limit_add(summand1:float, summand2:float, limit:float)->float: return limit if summand1+summand2 > limit else summand1 + summand2
def __limit_sub(minuend:float, subtrahend:float, limit:float)->float: return limit if minuend-subtrahend < limit else minuend - subtrahend

def __scale_history_weights(loaded_history:list[dict[str, str]], search_term:str)->bool:
    """
        recalculates the weight and repeated_uses values of each search term of the user's history depending on their occurrences
        The more often a term was searched for, the higher is its weight. The weight decreases evenly everytime it wasn't searched.
        The repeated_uses is how many times in a row a term was searched for. The repeated_uses only decreases partially, even if the term isn't being searched again right away.

        Parameters:
        :param str search_term: the term the user is currently searching for
        :param list[dict[str, str]] loaded_history: the history of the user's search terms read from the database4
        Return:
        :return bool: whether the search term already existed in the users history
    """
    if len(loaded_history) == 0:
        return False
    term_existed:bool = False
    for entry in loaded_history:
        if DEBUG_MODE:print(f"""[SearchBar]:processing "{entry['text']}" """)
        weight:float = float(entry['weight']) if entry['weight'] else 0
        repeated_uses:float = float(entry['repeated_uses']) if entry['repeated_uses'] else 0
        text:str = str(entry['text']) if entry['text'] else ''

        if text == search_term:
            #double and round the weight value of the term
            weight = __limit_scl(weight, 2, 100)
            weight = round(weight, 2)
            #add 1 to the repeated_uses value of the term
            entry['repeated_uses'] = str(__limit_add(repeated_uses, 1, MAX_REPEATED_USES))
            if DEBUG_MODE:print(f"""[SearchBar][__scale__history_weights]:term already existed in Database and was updated to be {entry}""")
            term_existed = True
        else:
            #divide weight by a number between 1 and 1,5 so its weight isn't reduced if it gor searched repeatedly
            weight = round(__limit_div(weight,1.5-(0.5*(repeated_uses/MAX_REPEATED_USES)),0), 2)
            #subltrtact 1 from the weight value so id doesn't get just  closer to 0 indefinitely
            weight = __limit_sub(weight, 1, 0)
            entry['repeated_uses'] = str(__limit_sub(repeated_uses,MAX_REPEATED_USES/20,0))
            if DEBUG_MODE:print(f"""[SearchBar][__scale__history_weights]:term already existed in Database and was updated to be {entry}""")

        if weight == 0:
            #remove the term from the history as it seems to be useless
            loaded_history.remove(entry)
        else:
            entry['weight'] = str(weight)
    return term_existed

def __update_dropdown(new_items:List[str], dropdown:CTkListbox)->None:

    global cancel_dropdown_updates
    if cancel_dropdown_updates > 0:
        cancel_dropdown_updates-=1
        if DEBUG_MODE:print(f"[SearchBar][__update_dropdown]:canceling dropdown update")
        return
    if DEBUG_MODE:print(f"[SearchBar][__update_dropdown]:updating dropdown")
    if DEBUG_MODE:print(f"""[SearchBar][__update_dropdown]:setting grid of dropdown""")
    try:
        dropdown.grid(padx=5, pady=5, row=0, column=0, sticky=tk.W + tk.E)
    except Exception as e:
            if DEBUG_MODE:print(f"""[EXCEPTION][SearchBar][__update_dropdown]:failed to set grid of dropdown menu because of {e}""")
    if DEBUG_MODE:print(f"""[SearchBar][__update_dropdown]:successfully set grid of dropdown""")
    if dropdown:
        while dropdown.size() > 0:
            dropdown.delete(0, 0)
            if DEBUG_MODE:print(f"""[SearchBar][__update_dropdown]:removed all items from dropdown""")
        if DEBUG_MODE:print(f"""[SearchBar][__update_dropdown]:adding new items to dropdown""")
        if not new_items:
            if DEBUG_MODE:print(f"""[SearchBar][__update_dropdown]:new items are null""")
            if DEBUG_MODE:print(f"""[SearchBar][__update_dropdown]:aborting dropdown update""")
            return
        try:
            for item in new_items:
                dropdown.insert(dropdown.size(), item)
        except Exception as e:
            if DEBUG_MODE:print(f"""[EXCEPTION][SearchBar][__update_dropdown]:failed to add item to dropdown menu because of {e}""")
            return
    else:
        if DEBUG_MODE:print(f"""[SearchBar][__update_dropdown]:dropdown was null""")
        if DEBUG_MODE:print(f"""[SearchBar][__update_dropdown]:aborting dropdown update""")
        return
    if DEBUG_MODE:print(f"""[SearchBar][__update_dropdown]:finished dropdown update""")

def __match_entries(loaded_history:List[dict[str, str]], search_term:str) -> List[str]:
    i:int = 0
    result:List[str] = []
    for entry in loaded_history:
        if search_term in entry['text']:
            result.append(entry['text'])
            if DEBUG_MODE:print(f"""[SearchBar][update searchbar]:adding "{entry}" to new dropdown options""")
            i = i+1
            if i>=3:
                break
    return result

def update_search(loaded_history:list[dict[str, str]], dropdown:CTkListbox, search_term:str, username:str)->None:
    """
        called when the searchbar text changed like the user typing an additional character into the search bar .

        :param list[dict[str,str]] loaded_history: the history of the user's search terms
        :param CTkListbox dropdown: the dropdown where the suggested search terms are displayed
        :param str search_term: the current search term
        :param str username: the current user's username
    """
    global search_is_running, cancel_key_press_updates
    if not search_is_running:
        return
    if cancel_key_press_updates >0:
        if DEBUG_MODE:print(f"""[SearchBar][update searchbar]:canceling 1 out of {cancel_key_press_updates} to be canceled """)
        cancel_key_press_updates -= 1
        return
    if DEBUG_MODE:print(f"""[SearchBar][update searchbar]:running update search for user "{username}" with searchbar text "{search_term}" and loaded history "{loaded_history}" """)

    sorted_history:list[dict[str, str]] = sorted(loaded_history,key=lambda x:x['weight'])
    if DEBUG_MODE:print(f"""[SearchBar][update searchbar]:sorted history is "{sorted_history}" """)
    new_options:List[str] = []
    i:int = 0
    for entry in sorted_history:
        if str(search_term) in entry['text']:
            new_options.append(entry['text'])
            if DEBUG_MODE:print(f"""[SearchBar][update searchbar]:adding "{entry}" to new dropdown options""")
            i = i+1
        if i>=6:
            break
    if DEBUG_MODE:print(f"""[SearchBar][update_search]:chose "{__match_entries(loaded_history, search_term.lower())}" as new options for dropdown""")
    __update_dropdown(__match_entries(sorted_history, search_term.lower()), dropdown)



def finish_search(loaded_history:list[dict[str,str]], searchbar:ctk.CTkEntry, dropdown:CTkListbox, root:tk.Frame, search_term:str, username:str)->None:
    """
        Called once user stops typing into the search bar.
        Recalculates the weight and repeated_uses of each term.
        In case the term wasn't searched for already, adds it to the users search history and if needed strips away some of the users search history's entries.

        Parameters:
        :param list[dict[str,str]] loaded_history: the history of the user's search terms
        :param tk.Entry searchbar: the search bar
        :param CTkListbox dropdown: the dropdown where the suggested search terms are displayed
        :param tk.Frame root: the root of th searchbar
        :param str search_term: the current search term
        :param str username: the current user's username
    """
    global search_is_running
    if not search_is_running:
        return
    if DEBUG_MODE:print(f"""[SearchBar]:running finishing search for user {username} with searchbar text "{search_term}" and loaded history "{loaded_history}" """)
    if not search_term == "":
        sorted_history:list[dict[str, str]] = sorted(loaded_history,key=lambda x:x['weight'])
        if not __scale_history_weights(sorted_history, search_term.lower()):
            while len(sorted_history) >= 30:
                sorted_history.pop()
            if DEBUG_MODE:print(f"""[SearchBar]:sorted history was before "{sorted_history}" """)
            if all(history_entry.get("text") != search_term for history_entry in sorted_history):
                new_entry = {'weight':'100','repeated_uses':'1','text':search_term.lower()}
                sorted_history.append(new_entry)
                if DEBUG_MODE: print(f"""[SearchBar]:adding: "{new_entry}" to search history as it didn't exist in the database""")
            if DEBUG_MODE:print(f"""[SearchBar]:sorted history is now "{sorted_history}" """)
        if DEBUG_MODE:print(f"""[SearchBar]: writing "{json.dumps(sorted_history)}" to database """)
        db.update_benutzer(username, neue_suchverlauf=json.dumps(sorted_history))
        loaded_history.clear()
        for entry in sorted_history:
            loaded_history.append(entry)
        reloaded_history: str = db.read_benutzer_suchverlauf(username)
        if DEBUG_MODE:print(f"""[SearchBar]: reloaded loaded_history is now "{reloaded_history}" for user "{username}" """)
    searchbar.delete(0, tk.END)
    dropdown.grid_forget()
    root.focus()
    search_is_running = False

def start_search(loaded_history:List[Dict[str,str]], searchbar:ctk.CTkEntry, dropdown:CTkListbox, search_term:str, username:str):

    """
        called when the user starts typing into the search bar

        Parameters:
        :param list[dict[str,str]] loaded_history: the history of the user's search terms
        :param tk.Entry searchbar: the search bar
        :param CTkListbox dropdown: the dropdown where the suggested search terms are displayed
        :param str search_term: the current search term
        :param str username: the current user's username
    """
    global search_is_running, cancel_key_press_updates
    if search_is_running:
        update_search(loaded_history,dropdown,search_term, username)
    search_is_running = True
    if DEBUG_MODE:print(f"""[SearchBar]:starting search for user "{username}" with searchbar text "{search_term}" """)
    history_string:str = db.read_benutzer_suchverlauf(username)
    temp_history = json.loads(history_string if history_string else '[]')
    if DEBUG_MODE:print(f"""[SearchBar]:loaded "{temp_history}" for "{username}" from database""")
    loaded_history.clear()
    for entry in temp_history:
        loaded_history.append(entry)
    searchbar.delete(0, tk.END)
    new_items: list[str] = []
    for entry in loaded_history:
        new_items.append(entry['text'])
    __update_dropdown(__match_entries(loaded_history,search_term), dropdown)


def on_dropdown_select(searchbar:ctk.CTkEntry, dropdown:CTkListbox, username:str)->None:
    """
        called when a dropdown entry is clicked

        :param searchbar: the search bar
        :param CTkListbox dropdown: the dropdown
        :param str username: the current user's username
    """
    global search_is_running, cancel_key_press_updates
    if not search_is_running:
        return
    selected_button_text = dropdown.get(dropdown.curselection())
    if DEBUG_MODE:print(f"""[SearchBar]:user "{username}" selected item "{selected_button_text}" from dropdown""")
    searchbar.delete(0, tk.END)
    cancel_key_press_updates += 1
    try:
        searchbar.insert(0, selected_button_text)
    except Exception as e:
        print(f"""[EXCEPTION][SearchBar][__update_dropdown]:failed to add text to searchbar menu because of {e}""")
    if DEBUG_MODE:print(f"[SearchBar][OnDropdownSelect]:finished on dropdown select")