#import math
#from importlib.resources import read_text

from Datenbank import sqlite3api as db
import json
from typing import List,Dict
import tkinter as tk

history_object:any = ''
loaded_history:List[Dict[str,str]] = json.loads('[]')

search_is_running = False
fallback_username = 'Alex'

root = tk.Tk()
root.geometry("800x600")
root.title("Searchbar with Custom Dropdown")

dropdown_items:List[str] = []
dropdown_var:tk.StringVar = tk.StringVar()
dropdown:tk.Listbox = tk.Listbox(root, width=int(100), selectmode=tk.SINGLE, font=("Arial",14), listvariable=dropdown_var)
dropdown.place_forget()

search_button = tk.Button(root, text="Search")
search_button.place(x=100,y=100)
search_button.configure(width=6,height=1)

searchbar_var:tk.StringVar = tk.StringVar()
searchbar = tk.Entry(root, textvariable= searchbar_var, width=100, font=("Arial", 14))
searchbar.place(x=160,y=100)

select_item_button = tk.Button(root, text="Select Item")

def fetch_limited_hardware(term:str, username:str=fallback_username)->list[str,dict[str,str]]:
    data:list[str,dict[str,str]]
    for item_key, database_entry in db.fetch_hardware():
        print(f"{item_key}: {database_entry}")
        for value in database_entry:
            if term.lower() in str(database_entry[value]).lower():
                if database_entry not in data:
                    data.append(database_entry)
    return data

#def pending_search(username:str=fallback_username)->None:
#    search_term = searchbar.get()
#    print(f"""[SearchBar]:running pending search with searchbar text: "{search_term}" """)
#    user_data:str = db.read_benutzer_suchverlauf('Alex')
#    print(f"""[SearchBar]: read history as string, data="{user_data}" """)
#    history_object_ = json.loads(user_data)
#    print('[SearchBar]: converted string to object, object='+str(history_object_))

#def hide_dropdown(event):
#    dropdown.place_forget()

def __limit_scl(factor1:float, factor2:float, limit:float)->float: return limit if factor1*factor2 > limit else factor1 * factor2
def __limit_div(dividend:float, divisor:float, limit:float)->float: return limit if dividend / divisor < limit else dividend / divisor
def __limit_add(summand1:float, summand2:float, limit:float)->float: return limit if summand1+summand2 > limit else summand1 + summand2
def __limit_sub(minuend:float, subtrahend:float, limit:float)->float: return limit if minuend-subtrahend < limit else minuend - subtrahend

def __scale_history_weights(search_term:str, history:list[dict[str, str]])->bool:
    """
        recalculates the weight and spree values of each search term of the user's history depending on their occurrences
        The more often a term was searched for, the higher is its weight. The weight decreases evenly everytime it wasn't searched.
        The spree is how many times in a row a term was searched for. The spree only decreases partially, even if the term isn't being searched again right away.

        Parameters:
        :param str search_term: the term the user is currently searching for
        :param list[dict[str, str]] history: the history of the user's search terms read from the database4
        Return:
        :return bool: whether the search term already existed in the users history
    """
    if len(history) == 0:
        return False

    term_existed:bool = False
    for entry in history:
        print(f"""[SearchBar]:processing "{entry['text']}" """)
        weight:float = float(entry['weight']) if entry['weight'] else 0
        spree:float = float(entry['spree']) if entry['spree'] else 0
        text:str = str(entry['text']) if entry['text'] else ''

        if text == search_term:
            #double and round the weight value of the term
            weight = __limit_scl(weight, 2, 100)
            weight = round(weight, 2)
            #add 1 to the spree value of the term
            entry['spree'] = str(__limit_add(spree, 1, 10))
            term_existed = True
        else:
            #multiply the weight by 0.7
            #subltrtact 1 from the weight value so id doesn't get just  closer to 0 indefinitely
            weight = round(__limit_div(weight,1.5,0), 2)
            __limit_sub(weight, 1, 0)
            entry['spree'] = str(__limit_sub(spree,0.5,0))
        print(f"""[SearchBar]:weight of entry is now:{weight}""")

        if spree == 0 and weight== 0:
            #remove the term from the history as it seems to be useless
            print(f"""[SearchBar]:removing "{entry}" """)
            history.remove(entry)
        else:
            entry['weight'] = str(weight)
    return term_existed

def __update_dropdown(new_items:List[str], dropdown:tk.Listbox)->None:
    print(f"[SearchBar]:update dropdown")
    dropdown.place(x=100,y=130)
    dropdown.delete(0, tk.END)
    for item in new_items:
        dropdown.insert(tk.END, item)
    dropdown.tkraise()

def on_dropdown_select(dropdown:tk.Listbox)->None:
    """
        called when dropdown selection is clicked

        Parameters
        ----------
        :param tk.Listbox dropdown: the dropdown where th past search terms are displayed
    """
    selected_values = [dropdown.get(i) for i in dropdown.curselection()]
    selected_item:str = selected_values[0]
    print(f"""[SearchBar]:Selected item:"{selected_item}" from dropdown""")
    searchbar.delete(0, tk.END)
    searchbar.insert(0, selected_item)
    searchbar.focus()

def update_search(dropdown:tk.Listbox, searchbar_var:tk.StringVar)->None:
    """
        called when the user types an additional character into the search bar

        Parameters:
        :param tk.Listbox dropdown: dropdown to be updated later
        :param tk.StringVar searchbar_var: a string variable to get the newly typed character from
    """
    search_term = searchbar_var.get()
    print(f"""[SearchBar]:running pending search with searchbar text "{search_term}" """)
    new_options:List[str] = []
    sorted_history:list[dict[str, str]] = sorted(loaded_history,key=lambda x:x['weight'])
    i:int = 0
    for entry in sorted_history:
        if str(search_term) in entry['text']:
            new_options.append(entry['text'])
            i = i+1
        if i>=6:
            break
    __update_dropdown(new_options, dropdown)

def start_search(dropdown:tk.Listbox, searchbar_var:tk.StringVar, username:str = fallback_username)->None:
    """
        called when the user stops typing into the search bar

        Parameters:

    """
    global search_is_running, loaded_history
    search_term = searchbar_var.get()
    print(f"""[SearchBar]:starting search""")
    loaded_history = json.loads(db.read_benutzer_suchverlauf(username))
    print(f"""[SearchBar]:loaded "{loaded_history}" """)
    search_is_running = True
    update_search(dropdown, searchbar_var)


def finish_search(searchbar_:tk.Entry, search_term:str, username:str = fallback_username)->None:
    """
        Called once user stops typing into the search bar.
        Recalculates the weight and spree of each term.
        In case the term wasn't searched for already, adds it to the users search history and if needed strips away some of the users search history's entries.

        Parameters:
        :param str search_term: the final string to search for
        :param str username: the username of the user who is currently searching
        :param Tk.Entry searchbar_: the searchbar entry where the user was typing in
    """
    global search_is_running, loaded_history
    print(f"""[SearchBar]:finishing search with searchbar text "{search_term}" """)
    sorted_history:list[dict[str, str]] = sorted(loaded_history,key=lambda x:x['weight'])
    if not __scale_history_weights(search_term, sorted_history):
        while len(sorted_history) >= 30:
            sorted_history.pop()
        print(f"""[SearchBar]:loaded history was before "{sorted_history}" """)
        temp = {'weight':'100','spree':'1','text':search_term}
        sorted_history.append(temp)
        print(f"""[SearchBar]:adding: "{temp}" """)
        print(f"""[SearchBar]:loaded history is now "{sorted_history}" """)
    print(sorted_history)
    db.update_benutzer(username, neue_suchverlauf=json.dumps(sorted_history))
    searchbar_.delete(0, tk.END)
    print(f"""[SearchBar]: writing to database "{json.dumps(sorted_history)}" """)
    loaded_history = json.loads(db.read_benutzer_suchverlauf(username))
    print(f"""[SearchBar]: reloaded loaded_history is now "{loaded_history}" """)


# Bind the focus events to the test gui
searchbar.bind("<FocusIn>", lambda event: start_search(dropdown, searchbar_var, 'Alex'))
searchbar.bind("<FocusOut>", lambda event: dropdown.place_forget())
searchbar_var.trace_add("write", lambda var1_, var2_, var3_: update_search(dropdown, searchbar_var))
search_button.bind("<Button-1>", lambda event: finish_search(searchbar, searchbar_var.get(), 'Alex'))
dropdown.bind("<<ListboxSelect>>", lambda  event: on_dropdown_select(dropdown))
select_item_button.bind("<Button-2>", lambda event: finish_search(searchbar, event.widget.curselection()[0], 'Alex'))



root.mainloop()