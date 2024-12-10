import tkinter as tk
from tkinter import ttk, messagebox
import Datenbank.sqlite3api as db
import string, random


def add_user_popup(parent):
    add_popup = tk.Toplevel(parent)
    add_popup.title("User Hinzufügen")
    add_popup.transient(parent)
    add_popup.grab_set()
    add_popup.attributes('-topmost', True)
    add_popup.configure(background="white")

    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    window_width = 650
    window_height = 650

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    add_popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    add_popup.resizable(False, False)

    try:
        add_popup.iconbitmap("assets/srhIcon.ico")
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")

    # Header
    header_frame_add_item_popup = tk.Frame(add_popup, background="#DF4807")
    header_frame_add_item_popup.grid(row=0, column=0, sticky=tk.NSEW)
    header_frame_add_item_popup.grid_columnconfigure(0, weight=1)

    header_label_add_item_popup = tk.Label(
        header_frame_add_item_popup, background="#DF4807",
        text="Hinzufügen", foreground="white", font=("Arial", 40)
    )
    header_label_add_item_popup.grid(row=0, column=0, sticky=tk.NSEW)

    # Input Frame
    input_frame_add_user_popup = tk.Frame(add_popup, background="white")
    input_frame_add_user_popup.grid(row=1, column=0, pady=20, sticky=tk.NSEW)
    input_frame_add_user_popup.grid_columnconfigure(0, weight=1)
    input_frame_add_user_popup.grid_columnconfigure(1, weight=1)

    size_add_user_popup = 16

    # Username
    username_label_add_user_popup = tk.Label(
        input_frame_add_user_popup, text="Username", background="white",
        font=("Arial", size_add_user_popup)
    )
    username_label_add_user_popup.grid(row=0, column=0, padx=10, pady=20, sticky=tk.E)

    username_entry_add_user_popup = tk.Entry(
        input_frame_add_user_popup, background="#d9d9d9",
        font=("Arial", size_add_user_popup), bd=0
    )
    username_entry_add_user_popup.grid(row=0, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Email
    email_add_user_popup = tk.Label(
        input_frame_add_user_popup, text="E-Mail", background="white",
        font=("Arial", size_add_user_popup)
    )
    email_add_user_popup.grid(row=1, column=0, padx=10, pady=20, sticky=tk.E)

    email_entry_add_user_popup = tk.Entry(
        input_frame_add_user_popup, background="#d9d9d9",
        font=("Arial", size_add_user_popup), bd=0
    )
    email_entry_add_user_popup.grid(row=1, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Rolle
    roll_label_add_user_popup = tk.Label(
        input_frame_add_user_popup, text="Rolle", background="white",
        font=("Arial", size_add_user_popup)
    )
    roll_label_add_user_popup.grid(row=2, column=0, padx=10, pady=20, sticky=tk.E)

    role_values = []
    for room in db.read_all_rollen():
        role_values.append(room['Rolle'])
    role_combobox_add_user_popup = ttk.Combobox(
        input_frame_add_user_popup, values=role_values,
        font=("Arial", size_add_user_popup)
    )
    role_combobox_add_user_popup.grid(row=2, column=1, padx=20, pady=20, sticky=tk.W + tk.E)
    role_combobox_add_user_popup.set("Rolle auswählen")


    error_label = tk.Label(input_frame_add_user_popup, text="", background="white",fg="darkred",font=("Arial", 14))
    error_label.grid(row=3, column=0,columnspan=2, padx=0, pady=20, sticky=tk.E)

    # Buttons
    def submit_entry():
        pw = str(''.join(random.choices(string.ascii_letters, k=7)))
        if not username_entry_add_user_popup.get() or username_entry_add_user_popup.get() == "" or not role_combobox_add_user_popup.get() or role_combobox_add_user_popup.get() == "Rolle auswählen":
            error_label.configure(text="Please enter all required fields (Username)")
        else:
            db.create_benutzer(username_entry_add_user_popup.get(), pw, email_entry_add_user_popup.get())
            messagebox.showinfo(title="Added User", message="Nutzername: "+username_entry_add_user_popup.get()+"\nNew password: " + pw)
            from .adminUserWindow import adminUserWindow
            adminUserWindow.update_treeview_with_data()
            add_popup.destroy()

    def exit_entry():
        add_popup.destroy()

    parent.add_btn_add_item_popup = tk.PhotoImage(file="assets/Hinzu.png")
    parent.exit_btn_add_item_popup = tk.PhotoImage(file="assets/AbbrechenButton.png")

    button_frame_add_item_popup = tk.Frame(add_popup, background="white")
    button_frame_add_item_popup.grid(row=2, column=0, pady=20, sticky=tk.NSEW)
    button_frame_add_item_popup.grid_columnconfigure(0, weight=1)
    button_frame_add_item_popup.grid_columnconfigure(1, weight=1)

    exit_button_add_item_popup = tk.Button(
        button_frame_add_item_popup, image=parent.exit_btn_add_item_popup,
        bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=exit_entry
    )
    exit_button_add_item_popup.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)

    submit_button_add_item_popup = tk.Button(
        button_frame_add_item_popup, image=parent.add_btn_add_item_popup,
        bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=submit_entry
    )
    submit_button_add_item_popup.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

    # Grid Configuration
    add_popup.grid_rowconfigure(0, weight=1)  # Header
    add_popup.grid_rowconfigure(1, weight=2)  # Input-Bereich
    add_popup.grid_rowconfigure(2, weight=1)  # Buttons
    add_popup.grid_columnconfigure(0, weight=1)  # Zentriere alle Inhalte
