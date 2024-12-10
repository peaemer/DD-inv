import tkinter as tk
from tkinter import ttk
from tkinter import *
import Datenbank.sqlite3api as sqlapi
import cache

LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"
from ._SRHFont import load_font, SRHHeadline

# Hauptseite (zweites Fenster)
class adminUserWindow(tk.Frame):
    """
    The adminWindow class provides a graphical interface for managing user information and
    performing administrative tasks within a Tkinter application. It allows navigation between
    different pages, settings access, searching functionalities, and the ability to add new items.

    This class is constructed as a frame that can be integrated into a Tkinter application,
    rendering multiple components such as buttons, labels, entry widgets with placeholders,
    and a Treeview for displaying user data. It facilitates user interactions through a
    Grid layout and integrates different pop-up windows for operations like settings and
    adding items.

    :ivar srhHead: Stores the PhotoImage for the header logo.
    :type srhHead: tk.PhotoImage
    :ivar log_out_btn: Stores the PhotoImage for the logout button.
    :type log_out_btn: tk.PhotoImage
    :ivar opt_btn: Stores the PhotoImage for the options button.
    :type opt_btn: tk.PhotoImage
    :ivar searchBtn: Stores the PhotoImage for the search button.
    :type searchBtn: tk.PhotoImage
    :ivar add_btn: Stores the PhotoImage for the add item button.
    :type add_btn: tk.PhotoImage
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")

        def go_back_admin_window():
            from .mainPage import mainPage
            controller.show_frame(mainPage)

        def show_settings_window_admin_window():
            print("show settings window admin window")
            from .settingsWindow import pop_up_settings
            pop_up_settings(self)

        def search():                           # funktionalität hinzufügen
            print("I am Searching")

        def add_user_item():
            from .addUserPopup import add_user_popup
            add_user_popup(self)

        def on_entry_click(event):
            if user_search_entry.get() == 'Suche':
                user_search_entry.delete(0, "end")  # Lösche den Platzhalter-Text
                user_search_entry.config(fg='black')  # Setze Textfarbe auf schwarz

        def on_focus_out(event):
            if user_search_entry.get() == '':
                user_search_entry.insert(0, 'Suche')  # Platzhalter zurücksetzen
                user_search_entry.config(fg='grey')  # Textfarbe auf grau ändern

        def on_key_press(event):
            typed_key = event.char  # The character of the typed key

        def change_to_room():
            from .adminRoomWindow import adminRoomWindow
            controller.show_frame(adminRoomWindow)

        def add_user():
            from .addUserPopup import add_user_popup
            add_user_popup(self)

        global tree

        # Konfiguriere das Grid-Layout für das adminUserWindow
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Erstelle einen Header-Bereich
        header_frame = tk.Frame(self, background="#DF4807")
        header_frame.grid(row=0, column=0,columnspan=2, sticky=tk.W + tk.E)

        # Konfiguriere die Spalten für den Header
        header_frame.grid_columnconfigure(0, weight=1)  # Platz links
        header_frame.grid_columnconfigure(1, weight=2)  # Zentrale Spalte
        header_frame.grid_columnconfigure(2, weight=1)  # Platz rechts
        header_frame.grid_rowconfigure(0, weight=1)

        self.srhHead = tk.PhotoImage(file="assets/srh.png")

        # Füge ein zentriertes Label hinzu
        header_label = tk.Label(header_frame, image=self.srhHead, background="#DF4807", foreground="white")
        header_label.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N + tk.W)

        # Erstellen eines Schriftzuges im Header
        text_header_label = tk.Label(header_frame, background="#DF4807", text="Nutzer-Übersicht", font=(SRHHeadline, 30), foreground="white")
        text_header_label.grid(row=0, column=1, padx=0, pady=50, sticky="")


        # Konvertiere das Bild für Tkinter
        self.log_out_btn = tk.PhotoImage(file="assets/ArrowLeft.png")

        # Füge einen Button mit dem Bild hinzu
        log_out_button = tk.Button(header_frame, image=self.log_out_btn, command=go_back_admin_window, bd=0, relief=tk.FLAT, bg="#DF4807",
                                 activebackground="#DF4807")
        log_out_button.grid(row=0, column=3, sticky=tk.E, padx=20)

        # Konvertiere das Bild für Tkinter
        self.opt_btn = tk.PhotoImage(file="assets/option.png")

        # Füge einen Button mit dem Bild hinzu
        options_button = tk.Button(header_frame,
                                   image=self.opt_btn,
                                   command=show_settings_window_admin_window,
                                   bd=0,
                                   relief=tk.FLAT,
                                   bg="#DF4807",
                                   activebackground="#DF4807")
        options_button.grid(row=0, column=2, sticky=tk.E, padx=20)

        # Erstellen des Grayframes für linke Seite
        grey_frame_side = tk.Frame(self, background=srhGrey)
        grey_frame_side.grid(row=1, column=0, rowspan=2, sticky="nsw")


        #wip
        grey_frame_side.grid_columnconfigure(0, weight=1)

        user_button = tk.Button(grey_frame_side, text="Nutzer", bd=0, relief=tk.FLAT , bg=srhGrey, font=("Arial", 20))
        user_button.grid(padx=40, pady=5, row=0, column=0, sticky=tk.W + tk.E)

        room_button = tk.Button(grey_frame_side, text="Räume", bd=0, relief=tk.FLAT, bg=srhGrey,command=change_to_room, font=("Arial", 20))
        room_button.grid(padx=40, pady=5, row=1, column=0, sticky=tk.W + tk.E)


        middle_frame = tk.Frame(self, background="white")
        middle_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(1, weight=1)

        # Verschiebe den SearchFrame nach oben, indem du seine Zeile anpasst
        search_frame = tk.Frame(middle_frame, bg="white")
        search_frame.grid(pady=5, padx=5, row=0, column=0, sticky=tk.W + tk.E + tk.N)

        search_frame.grid_columnconfigure(0, weight=0)
        search_frame.grid_columnconfigure(1, weight=1)
        search_frame.grid_columnconfigure(2, weight=0)

        self.add_btn = tk.PhotoImage(file="assets/Hinzusmall.png")
        user_add_button = tk.Button(search_frame, image=self.add_btn, bd=0, relief=tk.FLAT, bg="white",
                                    activebackground="white", command=add_user)
        user_add_button.grid(padx=10, pady=1, row=0, column=2, sticky="w")

        self.searchBtn = tk.PhotoImage(file="assets/SearchButton.png")
        search_button = tk.Button(search_frame,
                                 image=self.searchBtn,
                                 bd=0,
                                 relief=tk.FLAT,
                                 bg="white",
                                 activebackground="white",
                                 command=search)
        search_button.grid(padx=10, pady=5, row=0, column=0)

        # Entry-Feld mit Platzhalter-Text
        user_search_entry = tk.Entry(search_frame, bg=srhGrey, font=("Arial", 20), bd=0, fg='grey')
        user_search_entry.insert(0, 'Suche')  # Setze den Platzhalter-Text

        # Events für Klick und Fokusverlust hinzufügen
        user_search_entry.bind('<FocusIn>', on_entry_click)
        user_search_entry.bind('<FocusOut>', on_focus_out)
        user_search_entry.bind('<Return>', search)
        user_search_entry.bind("<Key>", on_key_press)
        user_search_entry.grid(column=1, row=0, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)

        user_tree_frame = tk.Frame(middle_frame, background="white")
        user_tree_frame.grid(row=1, column=0, padx=0, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # Spaltenkonfiguration für das TreeFrame
        user_tree_frame.grid_rowconfigure(1, weight=1)
        user_tree_frame.grid_columnconfigure(0, weight=1)  # Spalte für die Tabelle
        user_tree_frame.grid_columnconfigure(1, weight=0)  # Spalte für die Scrollbar (fixiert)

        global user_tree
        user_tree = ttk.Treeview(user_tree_frame, column=("c1", "c2", "c3", "c4", "c5"), show="headings")

        user_scroll = tk.Scrollbar(
            user_tree_frame,
            orient="vertical",
            command=user_tree.yview,
            bg="black",
            activebackground="darkblue",
            troughcolor="grey",
            highlightcolor="black",
            width=15,
            borderwidth=1
        )
        user_scroll.grid(row=1, column=1, sticky="ns")

        # Treeview mit Scrollbar verbinden
        user_tree.configure(yscrollcommand=user_scroll.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        user_tree.tag_configure("oddrow", background="#f7f7f7")
        user_tree.tag_configure("evenrow", background="white")

        ### listbox for directories
        user_tree.column("# 1", anchor=CENTER, width=60)
        user_tree.heading("# 1", text="ID", )
        user_tree.column("# 2", anchor=CENTER, width=200)
        user_tree.heading("# 2", text="Nutzername")
        user_tree.column("# 3", anchor=CENTER, width=200)
        user_tree.heading("# 3", text="Passwort")
        user_tree.column("# 4", anchor=CENTER, width=300)
        user_tree.heading("# 4", text="E-Mail")
        user_tree.column("# 5", anchor=CENTER, width=100)
        user_tree.heading("# 5", text="Rolle")
        user_tree.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        user_tree.tkraise()

        def insert_data(self):
            i = 0
            for entry in sqlapi.read_all_benutzer():
                # Bestimme das Tag für die aktuelle Zeile
                tag = "evenrow" if i % 2 == 0 else "oddrow"

                # Daten mit dem Tag in das Treeview einfügen
                user_tree.insert(
                    "",
                    "end",
                    text=f"{entry['Nutzername']}",
                    values=(
                        i,
                        entry['Nutzername'],
                        entry['Passwort'],
                        entry['Email'],
                        entry['Rolle'],
                    ),
                    tags=(tag,)
                )
                i += 1
        insert_data(self)

        # Funktion für das Ereignis-Binding
        def on_item_selected(event):
            try:
                selected_user = user_tree.focus()
                print(f"Ausgewählter User: {selected_user}")  # Debug
                if selected_user:
                    from .userDetailsWindow import userDetailsWindow, show_user_details
                    show_user_details(selected_user, user_tree, controller)
            except Exception as e:
                print(f"Fehler bei der Auswahl: {e}")

        # Binde die Ereignisfunktion an die Treeview
        user_tree.bind("<Double-1>", on_item_selected)

    def update_treeview_with_data(self=None):
        user_tree.delete(*user_tree.get_children())
        i = 0
        for entry in sqlapi.read_all_benutzer():
            # Bestimme das Tag für die aktuelle Zeile
            tag = "evenrow" if i % 2 == 0 else "oddrow"

            # Daten mit dem Tag in das Treeview einfügen
            user_tree.insert(
                "",
                "end",
                text=f"{entry['Nutzername']}",
                values=(
                    i,
                    entry['Nutzername'],
                    entry['Passwort'],
                    entry['Email'],
                    entry['Rolle'],
                ),
                tags=(tag,)
            )
            i += 1