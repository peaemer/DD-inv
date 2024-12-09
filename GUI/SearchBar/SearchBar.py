from importlib.resources import read_text

from Datenbank import sqlite3api as db
import json
from typing import List,Dict
obj = json.loads("""[{"text":"test","weight":2},{"text":"bla","weight":5}]""")

initial_history:str = """[{"text":"","weight":0}]"""
# initial_history:str=''
history_object:any = ''
loaded_history:List[Dict[str,str]] = json.loads(initial_history)
json_object = json.loads(initial_history)

def fetch_limited_hardware(term:str, username:str)->dict[str,dict[str,str]]:
    data:dict[str,dict[str,str]]
    for item_key, database_entry in db.fetch_hardware():
        print(f"{item_key}: {database_entry}")
        for value in database_entry:
            if term.lower() in str(database_entry[value]).lower():
                if database_entry not in data:
                    data.append(database_entry)
    return data

def pending_search(current_term:str, username:str)->None:
    print(f"""[SearchBar]: running pending search with term "{current_term}" """)
    user_data:str = db.read_benutzer_suchverlauf('Alex')
    print(f"""[SearchBar]: read history as string, data="{user_data}" """)
    history_object = json.loads(user_data)
    print('[SearchBar]: converted string to object, object='+str(history_object))



def completed_search(final_term:str)->None:

#    sorted_list = sorted(None, key=lambda x: x['age'])
    pass



#pending_search('as','Alex')



import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Searchbar with Custom Dropdown")


def on_search_change(*args):
    search_content = search_var.get()
    print(f"Search content: {search_content}")

search_var = tk.StringVar()
search_var.trace_add("write", on_search_change)

# Create the search bar (Entry widget)
searchbar = tk.Entry(root, textvariable= search_var, width=30)
searchbar.pack(pady=10)




# Create a list of items for the dropdown
dropdown_items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]

# Create a Listbox to act as a dropdown menu
dropdown = tk.Listbox(root, height=5, selectmode=tk.SINGLE, width=28)
dropdown.place_forget()  # Initially hide the dropdown
username = 'Alex'

# Function to handle search input and dropdown selection
def search_action():
    search_term = searchbar.get()  # Get the text entered in the search bar
    print(f"Searching for: {search_term}")

# Function to show the dropdown below the search bar when it gets focused
def show_dropdown(event):
    print(f"show dropdown")
    # Position the dropdown right below the search bar
    dropdown.place(x=searchbar.winfo_x(), y=searchbar.winfo_y() + searchbar.winfo_height() + 5)
    dropdown.delete(0, tk.END)  # Clear any previous entries
    for item in dropdown_items:  # Insert the dropdown items dynamically
        dropdown.insert(tk.END, item)
    #dropdown.focus_force()

# Function to hide the dropdown when focus is lost
def hide_dropdown(event):
    dropdown.place_forget()

# Function to handle selection from the dropdown
def on_dropdown_select(event):
    # Get the indices of the selected items
    #selected_indices = dropdown.curselection()
    # Get the corresponding values
    selected_values = [dropdown.get(i) for i in dropdown.curselection()]
    #print(f"Selected indices: {selected_indices}")
    #print(f"Selected values: {selected_values}")
    print(f"on dropdown select")
    #searchbar.curs selected_indices[0]
    selected_item:str = selected_values[0]  # Get the selected item
    print(f"Selected item: {selected_item}")
    searchbar.delete(0, tk.END)
    searchbar.insert(0, selected_item)
    searchbar.focus_set()
    #pending_search(selected_item, 'Alex')
    #dropdown.place_forget()  # Optionally hide dropdown after selection


# Bind the focus events to show or hide the dropdown
searchbar.bind("<FocusIn>", show_dropdown)  # Show dropdown when the search bar gets focused
searchbar.bind("<FocusOut>", hide_dropdown)  # Hide dropdown when the search bar loses focus
# Bind the selection event in the listbox to handle dropdown item selection
dropdown.bind("<<ListboxSelect>>", on_dropdown_select)


# Create a button to trigger the search action
search_button = tk.Button(root, text="Search", command=search_action)
search_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()