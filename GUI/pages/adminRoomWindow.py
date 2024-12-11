import tkinter as tk
from tkinter import ttk
from tkinter import *
import Datenbank.sqlite3api as sqlapi
import cache
import customtkinter as ctk
from ._SRHFont import load_font, SRHHeadline

LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"


# Hauptseite (zweites Fenster)
class adminRoomWindow(tk.Frame):
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

        def add_room():
            from .addRoomPopup import add_room_popup
            add_room_popup(self)

        def on_entry_click(event):
            if room_search_entry.get() == 'Suche':
                room_search_entry.delete(0, "end")  # Lösche den Platzhalter-Text
                room_search_entry.config(fg='black')  # Setze Textfarbe auf schwarz

        def on_focus_out(event):
            if room_search_entry.get() == '':
                room_search_entry.insert(0, 'Suche')  # Platzhalter zurücksetzen
                room_search_entry.config(fg='grey')  # Textfarbe auf grau ändern

        def on_key_press(event):
            typed_key = event.char  # The character of the typed key


        def change_to_user():
            from .adminUserWindow import adminUserWindow
            controller.show_frame(adminUserWindow)

        def change_to_roles():
            from .adminRoomWindow import adminRoomWindow
            controller.show_frame(adminRoomWindow)


        global tree

        # Konfiguriere das Grid-Layout für das adminRoomWindow
        self.grid_columnconfigure(0, weight=1)

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
        text_header_label = tk.Label(header_frame, background="#DF4807", text="Raum-Übersicht", font=(SRHHeadline, 30), foreground="white")
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


        #########
        #NAV:BAR#
        #########

        navi = tk.Frame(self, background=srhGrey)
        navi.grid(row=1, column=0, sticky="nesw")

        navi.grid_columnconfigure(0, weight=1)
        navi.grid_columnconfigure(1, weight=1)
        navi.grid_columnconfigure(2, weight=1)

        user_nav = ctk.CTkButton(navi, text="Nutzer", border_width=0, command=change_to_user, corner_radius=20, fg_color="#C5C5C5",
                                 text_color="black", font=("Arial", 20), hover_color="darkgray")
        user_nav.grid(padx=40, pady=15, row=0, column=0, sticky=tk.W + tk.E)

        room_nav = ctk.CTkButton(navi, text="Räume", border_width=0, corner_radius=20, fg_color="#C5C5C5",
                                 text_color="black", font=("Arial", 20), hover_color="darkgray")
        room_nav.grid(padx=40, pady=5, row=0, column=1, sticky=tk.W + tk.E)

        role_nav = ctk.CTkButton(navi, text="Rollen", border_width=0, corner_radius=20, fg_color="#C5C5C5",
                                 text_color="black", command=change_to_roles, font=("Arial", 20),
                                 hover_color="darkgray")
        role_nav.grid(padx=40, pady=5, row=0, column=2, sticky=tk.W + tk.E)


        # Erstellen des MiddleFrame
        middle_frame = tk.Frame(self, bg="white")
        middle_frame.grid(row=2, padx=10, pady=10, column=0, sticky="nesw")

        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(1, weight=1)

        # Verschiebe den SearchFrame nach oben, indem du seine Zeile anpasst
        search_frame = tk.Frame(middle_frame, bg="white")
        search_frame.grid(pady=5, padx=5, row=0, column=0, sticky=tk.W + tk.E + tk.N)

        search_frame.grid_columnconfigure(0, weight=0)
        search_frame.grid_columnconfigure(1, weight=1)
        search_frame.grid_columnconfigure(2, weight=0)


        self.add_btn = tk.PhotoImage(file="assets/HinzuSmall.png")
        room_add_button = tk.Button(search_frame, image=self.add_btn, bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=add_room)
        room_add_button.grid(padx=10, pady=5, row=0, column=2, sticky="w")

        self.searchBtn = tk.PhotoImage(file="assets/SearchButton.png")
        search_button = tk.Button(search_frame,
                                 image=self.searchBtn,
                                 bd=0,
                                 relief=tk.FLAT,
                                 bg="white",
                                 activebackground="white",
                                 command=search)
        search_button.grid(padx=5, pady=5, row=0, column=0)

        # Entry-Feld mit Platzhalter-Text
        room_search_entry = tk.Entry(search_frame, bg=srhGrey, font=("Arial", 20), bd=0, fg='grey')
        room_search_entry.insert(0, 'Suche')  # Setze den Platzhalter-Text

        # Events für Klick und Fokusverlust hinzufügen
        room_search_entry.bind('<FocusIn>', on_entry_click)
        room_search_entry.bind('<FocusOut>', on_focus_out)
        room_search_entry.bind('<Return>', search)
        room_search_entry.bind("<Key>", on_key_press)
        room_search_entry.grid(column=1, row=0, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)


        # Ändere die Position des TreeFrames auf row=3
        room_tree_frame = tk.Frame(middle_frame, background="white")
        room_tree_frame.grid(row=1, column=0, padx=0, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # Spaltenkonfiguration für das TreeFrame
        room_tree_frame.grid_rowconfigure(1, weight=1)
        room_tree_frame.grid_columnconfigure(0, weight=1)  # Spalte für die Tabelle
        room_tree_frame.grid_columnconfigure(1, weight=0)  # Spalte für die Scrollbar (fixiert)


        global room_tree
        room_tree = ttk.Treeview(room_tree_frame, column=("c1", "c2"), show="headings")

        room_scroll = tk.Scrollbar(
            room_tree_frame,
            orient="vertical",
            command=room_tree.yview,
            bg="black",
            activebackground="darkblue",
            troughcolor="grey",
            highlightcolor="black",
            width=15,
            borderwidth=1
        )

        room_scroll.grid(row=1, column=1, sticky="ns")
        room_tree.configure(yscrollcommand=room_scroll.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        room_tree.tag_configure("oddrow", background="#f7f7f7")
        room_tree.tag_configure("evenrow", background="white")

        ### listbox for directories
        room_tree.column("# 1", anchor=CENTER, width=200)
        room_tree.heading("# 1", text="Raum", )
        room_tree.column("# 2", anchor=CENTER, width=300)
        room_tree.heading("# 2", text="Ort")
        room_tree.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        room_tree.tkraise()

        def insert_data(self):
            i = 0
            for entry in sqlapi.fetch_all_rooms():
                # Bestimme das Tag für die aktuelle Zeile
                tag = "evenrow" if i % 2 == 0 else "oddrow"

                # Daten mit dem Tag in das Treeview einfügen
                room_tree.insert(
                    "",
                    "end",
                    text=f"{str(entry['Raum'])}",
                    values=(
                        entry['Raum'],
                        entry['Ort']
                    ),
                    tags=(tag,)
                )
                i += 1
        insert_data(self)

        # Funktion für das Ereignis-Binding
        def on_room_selected(event):
            try:
                selected_room = room_tree.focus()
                print(f"Ausgewählter Raum: {selected_room}")  # Debug
                if selected_room:
                    from .roomDetailsWindow import roomDetailsWindow, show_room_details
                    show_room_details(selected_room, room_tree, controller)
            except Exception as e:
                print(f"Fehler bei der Auswahl: {e}")

        # Binde die Ereignisfunktion an die Treeview
        room_tree.bind("<Double-1>", on_room_selected)

    def update_treeview_with_data(self):
        room_tree.delete(*room_tree.get_children())
        i = 0
        for entry in sqlapi.fetch_all_rooms():
            # Bestimme das Tag für die aktuelle Zeile
            tag = "evenrow" if i % 2 == 0 else "oddrow"

            # Daten mit dem Tag in das Treeview einfügen
            room_tree.insert(
                "",
                "end",
                text=f"{entry['Raum']}",
                values=(
                    i,
                    entry['Raum'],
                    entry['Ort'],
                ),
                tags=(tag,)
            )
            i += 1