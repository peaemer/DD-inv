from CTkListbox import CTkListbox

import cache
from Datenbank import sqlite3api as db
import json
from typing import List,Dict
import tkinter as tk

history_object:any = ''

search_is_running = False
fallback_username = 'Alex'
""""
root = tk.Tk()
root.geometry("800x600")
root.title("Searchbar with Custom Dropdown")
"""

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
    print(f"[SearchBar]:update dropdown")

    dropdown.grid(column=1, row=1, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)
    #dropdown.place(x=100,y=130)
    dropdown.delete(0, tk.END)
    for item in new_items:
        dropdown.insert(tk.END, item)
    #dropdown.tkraise()

def on_dropdown_select(searchbar:tk.Entry, dropdown:CTkListbox)->None:
    """
        called when a dropdown entry is clicked

        :param tk.event searchbar: the searchbar
        :param CTkListbox dropdown: the dropdown where the suggested search terms are displayed
    """
    global search_is_running
    if not search_is_running:
        return
    #print(dropdown.get(dropdown.curselection()))
    #all_selected_items:list[str] = [dropdown.get(i) for i in dropdown.curselection()]
    #print(f"""[SearchBar]:all selected items are "{all_selected_items}" """)
    #if len(all_selected_items) == 0:
    #    return
    #selected_item:str = all_selected_items[0]
    print(f"""[SearchBar]:selected item "{dropdown.get(dropdown.curselection())}" from dropdown""")
    searchbar.delete(0, tk.END)
    searchbar.insert(0, dropdown.get(dropdown.curselection()))
    searchbar.focus()

def update_search(loaded_history:list[dict[str, str]], dropdown:CTkListbox, search_term:str, username:str)->None:
    """
        called when the user types an additional character into the search bar

        :param list[dict[str,str]] loaded_history: the history of the user's search terms
        :param CTkListbox dropdown: the dropdown where the suggested search terms are displayed
        :param str search_term: the current search term
    """
    global search_is_running
    if not search_is_running:
        return
    print(f"""[SearchBar]:running update search for user "{username}" with searchbar text "{search_term}" and loaded history "{loaded_history}" """)
    sorted_history:list[dict[str, str]] = sorted(loaded_history,key=lambda x:x['weight'])
    print(f"""[SearchBar]:loaded history is "{loaded_history}" """)
    print(f"""[SearchBar]:sorted history is "{sorted_history}" """)
    new_options:List[str] = []
    i:int = 0
    for entry in sorted_history:
        if str(search_term) in entry['text']:
            new_options.append(entry['text'])
            i = i+1
        if i>=6:
            break
    __update_dropdown(new_options, dropdown)



def finish_search(loaded_history:list[dict[str,str]], searchbar:tk.Entry, dropdown:CTkListbox, search_term:str, username:str)->None:
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
            temp = {'weight':'100','repeated_uses':'1','text':search_term}
            sorted_history.append(temp)
            print(f"""[SearchBar]:adding: "{temp}" """)
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
    search_is_running = False

def start_search(loaded_history:List[Dict[str,str]], searchbar:tk.Entry, dropdown:CTkListbox, search_term:str, username:str):
    """
        called when the user starts typing into the search bar

        Parameters:
        :param list[dict[str,str]] loaded_history: the history of the user's search terms
        :param tk.Entry searchbar: the search bar
        :param CTkListbox dropdown: the dropdown where the suggested search terms are displayed
        :param str search_term: the current search term
        :param str username: the current user's username
    """
    global search_is_running
#    search_term = searchbar_var.get()
    print(f"""[SearchBar]:starting search for user "{username}" with searchbar text "{search_term}" """)
    history_string:str = db.read_benutzer_suchverlauf(username)
    temp_history = json.loads(history_string if history_string else '[]')
    print(f"""[SearchBar]:loaded "{temp_history}" for {username}""")
    loaded_history.clear()
    for entry in temp_history:
        loaded_history.append(entry)
    search_is_running = True
    searchbar.delete(0, tk.END)
    update_search(loaded_history, dropdown, search_term, username)

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
class searchBar(tk.Entry):

    dropdown: CTkListbox
    __dropdown_var:tk.StringVar
    __text_var:tk.StringVar

    def __init__(self, parent):
        self.__text_var = tk.StringVar()
        tk.Entry.__init__(self, parent, font=("Arial", 20), bg='white', bd=0, fg='grey', textvariable=self.__text_var)
        self.__dropdown_var = tk.StringVar()
        self.dropdown = CTkListbox(parent, font=("Arial", 20), bg="white", listvariable=self.__dropdown_var)
        self.dropdown.grid(column=1, row=1, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)
        self.grid(column=1, row=0, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)

        # Entry-Feld mit Platzhalter-Text
        self.insert(0, 'Suche')  # Setze den Platzhalter-Text
        """
        # Events für Klick und Fokusverlust hinzufügen
        """
        lh:list[dict[str,str]] = json.loads('[{}]')
        self.bind('<FocusIn>', start_search(lh, self, self.dropdown, self.__dropdown_var.get(), cache.user_name))
        self.__text_var.trace_add("write", lambda var1, var2, var3: update_search(cache.loaded_history, self.dropdown, self.__text_var.get(),cache.user_name))
        """"
        self.bind('<FocusOut>', on_focus_out)
        self.bind('<Return>', search)
        self.bind("<Key>", on_key_press)
        self.bind("<<ListboxSelect>>", lambda _: on_dropdown_select(dropdown))
        """

    def start_search(self):
        start_search(cache.loaded_history, self,  self.dropdown, self.__text_var.get(), cache.user_name)

    def finish_search(self):
        finish_search(cache.loaded_history, self, self.dropdown, self.__text_var.get(),cache.user_name)

    def update_search(self):
        update_search(cache.loaded_history, self.dropdown, self.__text_var.get(),)