import tkinter as tk
import customtkinter as ctk
import cache
import includes.sec_data_info.sqlite3api as db
from ._styles import *


def delete_entry(contr):
    cache.msgbox.destroy()
    db.delete_hardware_by_id(cache.selected_ID)
    from .mainPage import mainPage
    mainPage.update_treeview_with_data()
    mainPage.update_sidetree_with_data()
    contr.show_frame(mainPage)

def delete_user(contr):
    db.delete_benutzer(cache.selected_ID)
    from .adminUserWindow import adminUserWindow
    adminUserWindow.update_treeview_with_data()
    contr.show_frame(adminUserWindow)

def delete_room(contr):
    from .adminRoomWindow import adminRoomWindow
    adminRoomWindow.update_treeview_with_data()
    from .mainPage import mainPage
    mainPage.update_sidetree_with_data()
    contr.show_frame(adminRoomWindow)

def delete_roles(contr):
    from .adminRoleWindow import adminRoleWindow
    adminRoleWindow.update_treeview_with_data()
    contr.show_frame(adminRoleWindow)

def customMessageBoxDelete(parent, controller, title, message, type):
    msg_box = tk.Toplevel(parent)
    msg_box.title(title)
    msg_box.transient(parent)  # Popup bleibt im Vordergrund des Hauptfensters
    msg_box.grab_set()  # Blockiere Interaktionen mit dem Hauptfenster
    msg_box.attributes('-topmost', 0)
    msg_box.configure(background="white")

    # Bildschirmbreite und -höhe ermitteln
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Fensterbreite und -höhe definieren
    window_width = 450
    window_height = 80

    # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    msg_box.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    msg_box.resizable(False, False)

    try:
        msg_box.iconbitmap("includes/assets/srhIcon.ico")
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")

    cache.msgbox = msg_box

    def selectType():
        match(type):
            case "DELETE_ITEM":
                delete_entry(controller)
            case "DELETE_USER":
                delete_user(controller)
            case "DELETE_ROOM":
                delete_room(controller)
            case "DELETE_ROLE":
                delete_roles(controller)
        msg_box.destroy()

    info_msg = tk.Frame(msg_box, background="white")
    info_msg.grid(row=0,
                  column=0,
                  columnspan=1,
                  sticky="nesw")

    msg = ctk.CTkLabel(info_msg,
                       text=message,
                       text_color="black",
                       font=("Arial", 20),
                       justify="center")
    msg.grid(row=0, column=0, padx=15, pady=5, sticky="nesw", columnspan=2)

    delete = ctk.CTkButton(info_msg,
                           text="Löschen",
                           border_width=0,
                           fg_color=srhOrange,
                           text_color="white",
                           command=selectType)
    delete.grid(row=1, column=0, padx=0, pady=10)

    cancel = ctk.CTkButton(info_msg,
                           text="Abbrechen",
                           border_width=0,
                           fg_color=srhGrey,
                           text_color="black",
                           command=msg_box.destroy)
    cancel.grid(row=1, column=1, padx=0, pady=10)

    info_msg.grid_rowconfigure(0, weight=0)
    info_msg.grid_rowconfigure(1, weight=0)
    info_msg.grid_columnconfigure(0, weight=1)
    info_msg.grid_columnconfigure(1, weight=1)