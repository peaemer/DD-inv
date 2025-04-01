#import sqlite3
#import json
#import time
import tkinter

from includes.windows import AdminUserWindow
#import traceback

#from setuptools.windows_support import windows_only
#from typing_extensions import override

#from typing_extensions import override

from includes.windows.IWindow import IWindow
from includes.windows.LoginWindow import LoginWindow
from includes.windows.Searchbar.Dropdown import Dropdown

#from typing import Any

#import includes.network.Server
#from includes.windows import add_user_popup, DetailsWindow
#from includes.windows.AddItemPopup import AddItemPopup
#from includes.windows.AddUserPopup import AddUserPopup
#from includes.windows.AddRolePopup import AddRolePopup
#from includes.windows.addRolePopup_ import add_role_popup
#from includes.util import rwlock
#from includes.sec_data_info import sqlite3api
#from includes.windows.addItemPopup import add_item_popup
#from includes.util.Logging import Logger


"""
print(db.add_table('TestTable', [('Spalte1','TEXT'),('Spalte2','TEXT')]))

try:
    with db.init_connection() as con:
        cur = con.cursor()
        # wir brauchen ein Cursor um SQL Befehle an die Datenbank zusenden
        # Values werden als "?" - Platzhalter um fehler beim Übergeben der Values vorzubeugen,
        # Und um eine Variable übergeben zu können
        cur.execute("INSERT INTO TestTable (Spalte1,Spalte2) VALUES (?, ?)",('Bla1',''))
        con.commit()
    print("eintrag hinzugefügt.")
except sqlite3.Error as e:
    # e.args wird benötigt um detailiertere Information über die Fehler dazustellen
    print(f"Fehler beim Hinzufügen des Eintrags: {e.args[0]}")


try:
    with db.init_connection() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM TestTable")
        rows = cur.fetchall()
        # dict ist notwending um die Daten übersichtlicher in einer Tabelle darstellen zu können
        print([dict(row) for row in rows])
except sqlite3.Error as e:
    raise RuntimeError(f"Fehler beim Abrufen der Daten: {e.args[0]}")

#print(db.remove_table('TestTable'))

#db.update_benutzer('Alex',neues_passwort=rf"{hash_password('1234')}")
#print(db.read_benutzer('Alex'))
"""

"""
def exx2():
    exx()

def exx():
    stack:list[str] = traceback.format_stack()
    print(stack)
    stack.reverse()
    i:int = 0
    for line in stack:
        print(i, ' ', line)
        i+=1

exx2()
"""

#logger:Logger = Logger('test')
#data:list[dict[str,Any]] = [{'f':'gdf', 'd': 'fdsaf'},{'g':'öljkn', 'h': 'fasd'}]
#print([dict(entry) for entry in data])

"""
print(
    sqlite3api.extract_entry(
        json.dumps(
            {time.time():'fds',2:'fsd'}
        )
    )[0]
)
print(
    sqlite3api.extract_entry(
        json.dumps(
            {time.time():'fds',2:'fsd'}
        )
    )[1]
)
"""
"""
class TestWindow(IWindow):

    @override
    def setup_main_frame(self) -> None:
        print('running setup_main_frame')

    @override
    def setup_header_bar(self, frame: tkinter.Frame) -> None:
        pass

    @override
    def setup_side_bar_left(self, frame: tkinter.Frame, overlay_header_bar: bool = False) -> bool:
        return True

    @override
    def setup_side_bar_right(self, frame: tkinter.Frame, overlay_header_bar: bool = False) -> bool:
        return True

    @override
    def on_load(self) -> None:
        pass

    def __init__(self, parent):
        print(parent)
        super().__init__(parent)
        self.setup_main_frame()
        print('init!')
        #traceback.print_stack()
        #def test():
        #self.setup_main_frame()
        #test()
"""

def run():
#    AddRolePopup(root)
#    add_role_popup(root)
    #AddUserPopup(root)  # Ensure size is not fullscreen
    #DetailsWindow(root)
#    server:includes.network.Server.Server = includes.network.Server.Server()

    """
    l:list[int] = []
    for i in range(1, 30):
        l.append(i)
    l += [4,4]

    for i in range(0,len(l)):
        print(l[:i]+l[i+1:])
    print(l)
    """
root:tkinter.Tk = tkinter.Tk()  # Tkinter root window
print(root)
root.grid()
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
print(root)
from includes.gui.pages.adminPages.AdminUserPage import AdminUserPage
window = AdminUserPage(root, None)
#Dropdown(window)
#frame.setup_main_frame()
#    frame.setup_main_frame(root)
window.grid(row=0, column=0, sticky=tkinter.NSEW)
print(isinstance(window, IWindow))
root.mainloop()

"""
s = "ABCD"
b = bytearray()
b.extend(map(ord, s))
print(b)
"""

