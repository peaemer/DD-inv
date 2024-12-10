import math
from importlib.resources import read_text

from Datenbank import sqlite3api as db
import json
from typing import List,Dict
import tkinter as tk

obj = json.loads("""[{"text":"test","weight":2,"decline_history":"0","peek_wheight":"10"},{"text":"bla","weight":5}]""")

initial_history:str = """[{"text":"","weight":0}]"""
history_object:any = ''
loaded_history:List[Dict[str,str]] = json.loads(initial_history)
json_object = json.loads(initial_history)

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

search_var:tk.StringVar = tk.StringVar()
searchbar = tk.Entry(root, textvariable= search_var,width=100,font=("Arial",14))
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

def pending_search(username:str=fallback_username)->None:
    search_term = searchbar.get()
    print(f"""[SearchBar]:running pending search with searchbar text: "{search_term}" """)
    user_data:str = db.read_benutzer_suchverlauf('Alex')
    print(f"""[SearchBar]: read history as string, data="{user_data}" """)
    history_object_ = json.loads(user_data)
    print('[SearchBar]: converted string to object, object='+str(history_object_))

def update_dropdown(new_items:List[str])->None:
    print(f"show dropdown")
    dropdown.place(x=100,y=135)
    dropdown.delete(0, tk.END)
    for item in new_items:
        dropdown.insert(tk.END, item)
        
def hide_dropdown(event):
    dropdown.place_forget()

# Function to handle selection from the dropdown
def on_dropdown_select(event:tk.Event)->None:
    selected_values = [dropdown.get(i) for i in dropdown.curselection()]
    selected_item:str = selected_values[0]
    print(f"Selected item: {selected_item} from dropdown")
    searchbar.delete(0, tk.END)
    searchbar.insert(0, selected_item)
    searchbar.focus()

def start_search(event:tk.Event)->None:
    search_term = search_var.get()
    print(f"""[SearchBar]:starting search""")
    global search_is_running, loaded_history
    loaded_history = json.loads(db.read_benutzer_suchverlauf('Alex'))
    print(f"""[SearchBar]: loaded: "{loaded_history}" """)
    search_is_running = True
    update_search(None)

def update_search(*args):
    search_term = search_var.get()
    print(f"""[SearchBar]:running pending search with searchbar text:"{search_term}" """)
    new_options:List[str] = []
    sorted_history:list[dict[str, str]] = sorted(loaded_history,key=lambda x:x['weight'])
    i:int = 0
    for entry in sorted_history:
        if str(search_term) in entry['text']:
            new_options.append(entry['text'])
            i = i+1
        if(i>=6):
            break
    update_dropdown(new_options)

def finish_search(search_term:str)->None:
    #search_term:str = str(search_var.get())
    print(f"""[SearchBar]:finishing search with searchbar text: "{search_term}" """)
    term_existed:bool = False
    weight:int = 100
    sorted_history:list[dict[str, str]] = sorted(loaded_history,key=lambda x:x['weight'])
    for entry in sorted_history:
        print(f"""[SearchBar]:processing:"{entry['text']}" """)
        weight = int(entry['weight'])
        if entry['text'] == search_term:
            if weight*2 <= 100:
                weight *= 2
            else:
                weight = 100
            entry['weight'] = str(math.floor(weight))
            term_existed = True
        else:
            weight = math.floor(weight*0.7)
            if weight-1 >= 0:
                weight -= 1
            else:
                weight = 0
        print(f"weight is now:{entry['weight']} ")
        if weight == 0:
            print(f"removing:{entry}")
            sorted_history.remove(entry)
        else:
            entry['weight'] = str(weight)
    if not term_existed:
        while len(sorted_history) >= 30:
            sorted_history.pop()
        print(f"""[SearchBar]:loaded history was before: "{sorted_history}" """)
#        temp:json_object = json.loads("{\"weight\":\"100\",\"text\":\""+search_term+"\"}")
        temp = {"weight":"100","text":search_term}
        sorted_history.append(temp)
        print(f"""[SearchBar]:adding: "{temp}" """)
        print(f"""[SearchBar]:loaded history is now: "{sorted_history}" """)
    print(sorted_history)
    db.update_benutzer('Alex', neue_suchverlauf=json.dumps(sorted_history))
    searchbar.delete(0, tk.END)
    print(f"""[SearchBar]: wrote: "{json.dumps(sorted_history)}" """)




# Bind the focus events to show or hide the dropdown
searchbar.bind("<FocusIn>", start_search)
searchbar.bind("<FocusOut>", hide_dropdown)
search_button.bind("<Button-1>", lambda event:finish_search(dropdown_var.get()))
dropdown.bind("<<ListboxSelect>>", on_dropdown_select)
search_var.trace_add("write", update_search)
select_item_button.bind("<Button-2>", lambda event:finish_search(event.widget.curselection()[0]))

root.mainloop()