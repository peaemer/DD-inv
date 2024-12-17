from time import sleep

from CTkListbox import CTkListbox
import customtkinter as CTk

from Datenbank import sqlite3api as db
import json
from typing import List,Dict
import tkinter as tk

history_object:any = ''

search_is_running = False
fallback_username = 'Alex'

cancel_dropdown_updates:int = 0
cancel_key_press_updates:int = 0


def fetch_limited_hardware(term:str, username:str=fallback_username)->list[str,dict[str,str]]:
    data:list[str,dict[str,str]] = json.loads('')
    for item_key, database_entry in db.fetch_hardware():
        print(f"{item_key}: {database_entry}")
        for value in database_entry:
            if term.lower() in str(database_entry[value]).lower():
                if database_entry not in data:
                    data.append(database_entry)
    return data

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
        print(f"""[SearchBar]:processing "{entry['text']}" """)
        weight:float = float(entry['weight']) if entry['weight'] else 0
        repeated_uses:float = float(entry['repeated_uses']) if entry['repeated_uses'] else 0
        text:str = str(entry['text']) if entry['text'] else ''

        if text == search_term:
            #double and round the weight value of the term
            weight = __limit_scl(weight, 2, 100)
            weight = round(weight, 2)
            #add 1 to the repeated_uses value of the term
            entry['repeated_uses'] = str(__limit_add(repeated_uses, 1, 10))
            term_existed = True
        else:
            #multiply the weight by 0.7
            #subltrtact 1 from the weight value so id doesn't get just  closer to 0 indefinitely
            weight = round(__limit_div(weight,1.5,0), 2)
            weight = __limit_sub(weight, 1, 0)
            entry['repeated_uses'] = str(__limit_sub(repeated_uses,0.5,0))
        print(f"""[SearchBar]:weight of entry is now:{weight}""")

        if weight== 0:
            #remove the term from the history as it seems to be useless
            print(f"""[SearchBar]:removing "{entry}" """)
            loaded_history.remove(entry)
        else:
            entry['weight'] = str(weight)
    return term_existed

def __update_dropdown(new_items:List[str], dropdown:CTkListbox)->None:
    print(f"[SearchBar][__update_dropdown]:update dropdown")
    global cancel_dropdown_updates
    if cancel_dropdown_updates > 0:
        cancel_dropdown_updates-=1
        print(f"""[SearchBar][__update_dropdown]:canceling dropdown""")
        return
    print(f"""[SearchBar][__update_dropdown]:setting grid of dropdown""")
    try:
        dropdown.grid(column=1, row=1, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)
    except Exception as e:
        print('ERROR')
    print(f"""[SearchBar][__update_dropdown]:successfully set grid of dropdown""")
    if dropdown:
        while dropdown.size() > 0:
            dropdown.delete(0, 0)
            #dropdown.delete(0,dropdown.size()-1)
            print(f"""[SearchBar][__update_dropdown]:removed all items from dropdown""")
        print(f"""[SearchBar][__update_dropdown]:adding new items to dropdown""")
        if not new_items:
            print(f"""[SearchBar][__update_dropdown]:new items are null""")
            print(f"""[SearchBar][__update_dropdown]:aborting dropdown update""")
            return
        try:
            for item in new_items:
                print(f"""[SearchBar][__update_dropdown]:added "{item}" to dropdown menu""")
                dropdown.insert(dropdown.size(), item)
        except Exception as e:
            print(f"""[EXCEPTION][SearchBar][__update_dropdown]:failed to add item to dropdown menu because of {e}""")
            return
    else:
        print(f"""[SearchBar][__update_dropdown]:dropdown was null""")
        return
    print(f"""[SearchBar][__update_dropdown]:finished dropdown update""")
    print(dropdown.buttons)

def __match_entries(loaded_history:List[dict[str, str]], search_term:str) -> List[str]:
    i:int = 0
    result:List[str] = []
    for entry in loaded_history:
        if str(search_term) in entry['text']:
            result.append(entry['text'])
            print(f"""[SearchBar][update searchbar]:adding "{entry}" to new dropdown options""")
            i = i+1
        if i>=6:
            break
    return result

def update_search(loaded_history:list[dict[str, str]], dropdown:CTkListbox, search_term:str, username:str)->None:
    """
        called when the user types an additional character into the search bar

        :param list[dict[str,str]] loaded_history: the history of the user's search terms
        :param CTkListbox dropdown: the dropdown where the suggested search terms are displayed
        :param str search_term: the current search term
    """
    global search_is_running, cancel_key_press_updates
    if not search_is_running:
        return
    if cancel_key_press_updates >0:
        print(
        f"""[SearchBar][update searchbar]:canceling 1 out of {cancel_key_press_updates} to be canceled """)
        cancel_key_press_updates -= 1
        return
    print(f"""[SearchBar][update searchbar]:running update search for user "{username}" with searchbar text "{search_term}" and loaded history "{loaded_history}" """)
    sorted_history:list[dict[str, str]] = sorted(loaded_history,key=lambda x:x['weight'])
    print(f"""[SearchBar][update searchbar]:loaded history is "{loaded_history}" """)
    print(f"""[SearchBar][update searchbar]:sorted history is "{sorted_history}" """)
    new_options:List[str] = []
    i:int = 0
    for entry in loaded_history:
        if str(search_term) in entry['text']:
            new_options.append(entry['text'])
            print(f"""[SearchBar][update searchbar]:adding "{entry}" to new dropdown options""")
            i = i+1
        if i>=6:
            break
    print(f"""[SearchBar][update searchbar]:updating dropdown with options "{new_options}" """)
    #if len(new_options)>0:
    __update_dropdown(__match_entries(loaded_history, search_term), dropdown)



def finish_search(loaded_history:list[dict[str,str]], searchbar:CTk.CTkEntry, dropdown:CTkListbox, root:CTk.CTkFrame, search_term:str, username:str)->None:
    """
        Called once user stops typing into the search bar.
        Recalculates the weight and repeated_uses of each term.
        In case the term wasn't searched for already, adds it to the users search history and if needed strips away some of the users search history's entries.

        Parameters:
        :param list[dict[str,str]] loaded_history: the history of the user's search terms
        :param tk.Entry searchbar: the search bar
        :param CTkListbox dropdown: the dropdown where the suggested search terms are displayed
        :param str search_term: the current search term
        :param str username: the current user's username
    """
    global search_is_running
    if not search_is_running:
        return

    print(f"""[SearchBar]:finishing search for user {username} with searchbar text "{search_term}" """)
    if not search_term == "":
        sorted_history:list[dict[str, str]] = sorted(loaded_history,key=lambda x:x['weight'])
        if not __scale_history_weights(sorted_history, search_term):
            while len(sorted_history) >= 30:
                sorted_history.pop()
            print(f"""[SearchBar]:sorted history was before "{sorted_history}" """)
            if all(history_entry.get("text") != search_term for history_entry in sorted_history):
                new_entry = {'weight':'100','repeated_uses':'1','text':search_term}
                sorted_history.append(new_entry)
                print(f"""[SearchBar]:adding: "{new_entry}" to search history as it doesn't exist""")
            print(f"""[SearchBar]:sorted history is now "{sorted_history}" """)
        print(f"""[SearchBar]: writing to database "{json.dumps(sorted_history)}" """)
        db.update_benutzer(username, neue_suchverlauf=json.dumps(sorted_history))
        loaded_history.clear()
        for entry in sorted_history:
            loaded_history.append(entry)
        reloaded_history: str = db.read_benutzer_suchverlauf(username)
        #temp_history = json.loads(reloaded_history if reloaded_history else '[]')
        print(f"""[SearchBar]: reloaded loaded_history is now "{reloaded_history}" for user "{username}" """)
    searchbar.delete(0, tk.END)
    dropdown.grid_forget()
    root.focus()
    search_is_running = False

def start_search(loaded_history:List[Dict[str,str]], searchbar:CTk.CTkEntry, dropdown:CTkListbox, search_term:str, username:str):

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
        return
    search_is_running = True
    print(f"""[SearchBar]:starting search for user "{username}" with searchbar text "{search_term}" """)
    #db.update_benutzer('Alex',neue_suchverlauf='[]')
    history_string:str = db.read_benutzer_suchverlauf(username)
    temp_history = json.loads(history_string if history_string else '[]')
    print(f"""[SearchBar]:loaded "{temp_history}" for {username}""")
    loaded_history.clear()
    for entry in temp_history:
        loaded_history.append(entry)
    searchbar.delete(0, tk.END)
    new_items: list[str] = []
    for entry in loaded_history:
        new_items.append(entry['text'])
    __update_dropdown(new_items, dropdown)
    #update_search(loaded_history, dropdown, search_term, username)


def on_dropdown_select(loaded_history:list[dict[str,str]], searchbar:CTk.CTkEntry, dropdown:CTkListbox, parent:CTk.CTkFrame, username:str)->None:
    """
        called when a dropdown entry is clicked

        :param tk.event searchbar: the searchbar
        :param CTkListbox dropdown: the dropdown where the suggested search terms are displayed
    """
    global search_is_running, cancel_key_press_updates
    if not search_is_running:
        return
    selected_button_text = dropdown.get(dropdown.curselection())
    print(f"""[SearchBar]:selected item "{selected_button_text}" from dropdown""")
    searchbar.delete(0, tk.END)
    cancel_key_press_updates += 1
    try:
        searchbar.insert(0, selected_button_text)
    except Exception as e:
        print(f"""[EXCEPTION][SearchBar][__update_dropdown]:failed to add text to searchbar menu because of {e}""")
    return
    new_items:list[str] = []
    for entry in loaded_history:
        new_items.append(entry['text'])
    try:
        #parent.focus()
        __update_dropdown(new_items, dropdown)
    except Exception as e:
        print('error!')
    print(dropdown.__class__)
    print(f"[SearchBar][OnDropdownSelect]:finished on dropdown select")

def on_searchbar_lost_focus(searchbar:CTk.CTkEntry,search_bar_variable:tk.StringVar, dropdown:CTkListbox)->None:
    """
    global  search_is_running
    dropdown.grid_forget()
    if search_bar_variable.get() == '':
        searchbar.insert(0, 'Suche')  # Platzhalter zurücksetzen
        searchbar.configure(fg_color='grey')  # Textfarbe auf grau ändern
        searchbar.configure(bg_color='white')
    search_is_running = False
    """
"""
history:List[Dict[str,str]] = json.loads('[{}]')

dropdown_items:List[str] = []
dropdown_var_:tk.StringVar = tk.StringVar()
dropdown_:CTkListbox = CTkListbox(root, width=int(100), selectmode=tk.SINGLE, font=("Arial",14), listvariable=dropdown_var_)
dropdown_.place_forget()

search_button_var_ = tk.StringVar()
search_button_ = tk.Button(root, text="Search", )
search_button_.place(x=100,y=100)
search_button_.configure(width=6,height=1)

searchbar_var_:tk.StringVar = tk.StringVar()
searchbar_ = tk.Entry(root, textvariable= searchbar_var_, width=100, font=("Arial", 14))
searchbar_.place(x=160,y=100)

select_item_button = tk.Button(root, text="Select Item")

searchbar_.bind("<FocusIn>", lambda event: start_search(history, searchbar_, dropdown_,  searchbar_var_.get(), 'Alex'))
searchbar_.bind("<FocusOut>", lambda event: dropdown_.place_forget())
searchbar_var_.trace_add("write", lambda var1,var2,var3: update_search(history, dropdown_, searchbar_var_.get()))
search_button_.bind("<Button-1>", lambda event: finish_search(history, searchbar_, dropdown_, searchbar_var_.get(), 'Alex'))
dropdown_.bind("<<ListboxSelect>>", lambda event: on_dropdown_select(searchbar_,dropdown_))
select_item_button.bind("<Button-2>", lambda event: finish_search(history, searchbar_, dropdown_, event.widget.curselection()[0], 'Alex'))

#root.mainloop()
"""