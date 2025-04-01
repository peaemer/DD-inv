import tkinter as tk
from multiprocessing.connection import answer_challenge
import customtkinter as ctk

import cache
from includes.util.Logging import Logger
from ._styles import *

logger: Logger = Logger('SettingsWindow')


def customMessageBoxDelete(parent, title, message, buttonText = None, blue: bool = False) -> bool:
    delete_msg_box = tk.Toplevel(parent)
    delete_msg_box.title(title)
    delete_msg_box.transient(parent)  # Keep popup in front of the main window
    delete_msg_box.grab_set()  # Block interactions with the main window
    delete_msg_box.attributes('-topmost', 0)
    delete_msg_box.configure(background="white")
    delete_msg_box.focus_force()

    # Screen width and height
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Window width and height
    window_width = 460
    window_height = 100

    # Center position
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    delete_msg_box.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    delete_msg_box.resizable(False, False)

    try:
        delete_msg_box.iconbitmap("includes/assets/srhIcon.ico")
    except Exception as e:
        logger.debug(f"Error while loading icon {e}")

    cache.msgbox = delete_msg_box

    # Variable to track user response
    response = tk.BooleanVar(delete_msg_box)
    response.set(False)  # Default to False

    def handle_yes_action():
        response.set(True)  # Confirm action
        delete_msg_box.destroy()

    def handle_no_action():
        response.set(False)  # Confirm action
        delete_msg_box.destroy()

    delete_msg = tk.Frame(delete_msg_box, background="white")
    delete_msg.grid(row=0, column=0, columnspan=1, sticky=tk.NSEW)

    msg = ctk.CTkLabel(delete_msg,
        text=message,
        text_color="black",
        font=("Arial", 20),
        justify="center"
    )
    msg.grid(row=0, column=0, padx=15, pady=5, sticky="nesw", columnspan=2)

    if buttonText is not None:
        delete = ctk.CTkButton(delete_msg,
            text=buttonText,
            border_width=0,
            fg_color=srh_blue if blue else srh_orange,
            hover_color=srh_blue if blue else srh_orange_hover,
            cursor="hand2",
            text_color="white",
            anchor="center",
            command=lambda: handle_yes_action()
        )
        delete.grid(row=1, column=0, padx=0, pady=10)

        cancel = ctk.CTkButton(delete_msg,
            text="Abbrechen",
            border_width=0,
            fg_color=srh_grey,
            cursor="hand2",
            text_color="black",
            anchor="center",
            command=lambda: handle_no_action())
        cancel.grid(row=1, column=1, padx=0, pady=10)
    else:
        cancel = ctk.CTkButton(delete_msg,
            text="OK",
            border_width=0,
            fg_color=srh_grey,
            cursor="hand2",
            text_color="black",
            anchor="center",
            command=lambda: handle_no_action()
        )
        cancel.grid(row=1, column=1, padx=0, pady=10, columnspan=2)

    delete_msg_box.bind("<Return>", lambda event: cancel.invoke())

    delete_msg.grid_rowconfigure(0, weight=0)
    delete_msg.grid_rowconfigure(1, weight=0)
    delete_msg.grid_columnconfigure(0, weight=1)
    delete_msg.grid_columnconfigure(1, weight=0)
    delete_msg.grid_columnconfigure(2, weight=1)
    #delete_msg.grid_columnconfigure(1, weight=1)

    # Wait for user interaction
    delete_msg_box.wait_variable(response)
    return response.get()
