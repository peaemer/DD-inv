import tkinter as tk
from tkinter import ttk
from tkinter import *
import Datenbank.sqlite3api as sqlapi
import cache

LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"


# Hauptseite (zweites Fenster)
class adminWindow(tk.Frame):
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

        def add_item():
            from .addItemPopup import add_item_popup
            add_item_popup(self)

        def on_entry_click(event):
            if search_entry.get() == 'Suche':
                search_entry.delete(0, "end")  # Lösche den Platzhalter-Text
                search_entry.config(fg='black')  # Setze Textfarbe auf schwarz

        def on_focus_out(event):
            if search_entry.get() == '':
                search_entry.insert(0, 'Suche')  # Platzhalter zurücksetzen
                search_entry.config(fg='grey')  # Textfarbe auf grau ändern

        global tree

        # Konfiguriere das Grid-Layout für die Hauptseite
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Erstelle einen Header-Bereich
        header_frame = tk.Frame(self, height=10, background="#DF4807")
        header_frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

        # Konfiguriere die Spalten für den Header
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_rowconfigure(0, weight=1)

        self.srhHead = tk.PhotoImage(file="assets/srh.png")

        # Füge ein zentriertes Label hinzu
        header_label = tk.Label(header_frame, image=self.srhHead, background="#DF4807", foreground="white")
        header_label.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N + tk.W)

        # Konvertiere das Bild für Tkinter
        self.log_out_btn = tk.PhotoImage(file="assets/ArrowLeft.png")

        # Füge einen Button mit dem Bild hinzu
        log_out_button = tk.Button(header_frame, image=self.log_out_btn, command=go_back_admin_window(), bd=0, relief=tk.FLAT, bg="#DF4807",
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


        grey_frame = tk.Frame(self, height=10, background="#F4EFEF")
        grey_frame.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N)

        # Füge den LogIn-Label zur Frame hinzu
        log_in_label = tk.Label(grey_frame,
                              text="User-Übersicht",
                              bd=0,
                              relief=tk.FLAT,
                              bg="#F4EFEF",
                              font=("Arial", 20))
        log_in_label.grid(padx=200, pady=5, row=0, column=0, sticky=tk.W)

        # Konfiguriere den grey_frame für zentrierte Ausrichtung
        grey_frame.grid_columnconfigure(0, weight=1)

        grey_frame_side = tk.Frame(self, height=10, background=srhGrey)
        grey_frame_side.grid(row=1, column=0, sticky=tk.W + tk.N + tk.S)

        overview_label = tk.Label(grey_frame_side, text="Räume", bd=0, relief=tk.FLAT, bg=srhGrey, font=("Arial", 20))
        overview_label.grid(padx=40, pady=5, row=0, column=0, sticky=tk.W + tk.E)

        # Verschiebe den SearchFrame nach oben, indem du seine Zeile anpasst
        search_frame = tk.Frame(self, bg="white")
        search_frame.grid(pady=50, padx=200, row=1, column=0, sticky=tk.W + tk.E + tk.N)

        search_frame.grid_columnconfigure(0, weight=0)
        search_frame.grid_columnconfigure(1, weight=1)
        search_frame.grid_columnconfigure(2, weight=0)

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
        search_entry = tk.Entry(search_frame, bg=srhGrey, font=("Arial", 20), bd=0, fg='grey')
        search_entry.insert(0, 'Suche')  # Setze den Platzhalter-Text

        # Events für Klick und Fokusverlust hinzufügen
        search_entry.bind('<FocusIn>', on_entry_click)
        search_entry.bind('<FocusOut>', on_focus_out)
        search_entry.grid(column=1, row=0, columnspan=2, sticky=tk.W + tk.E, padx=5, pady=5)


        # Ändere die Position des TreeFrames auf row=3
        user_tree_frame = tk.Frame(self, background="white")
        user_tree_frame.grid(row=1, column=0, padx=260)

        self.add_btn = tk.PhotoImage(file="assets/Erstellen.png")
        user_add_button = tk.Button(user_tree_frame, image=self.add_btn, bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=add_item)
        user_add_button.grid(padx=10, pady=5, row=0, column=0, sticky="e")

        user_tree = ttk.Treeview(user_tree_frame, column=("c1", "c2", "c3", "c4", "c5"), show="headings", height=15)

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
        user_tree.tkraise()
        user_tree.grid(row=1, column=0, sticky="nsew")
        def insert_data(self):
            i = 0
            for entry in sqlapi.read_all_benutzer():
                print(entry)
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
                selected_item = user_tree.focus()
                print(f"Ausgewähltes Item: {selected_item}")  # Debug
                if selected_item:
                    from .detailsWindow import detailsWindow, show_details
                    show_details(selected_item, tree, controller)
            except Exception as e:
                print(f"Fehler bei der Auswahl: {e}")

        # Binde die Ereignisfunktion an die Treeview
        user_tree.bind("<<TreeviewSelect>>", on_item_selected)

    def update_treeview_with_data(self):
        user_tree.delete(*user_tree.get_children())
        i = 0
        for entry in sqlapi.fetch_hardware():
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            user_tree.insert(
                "",
                "end",
                values=(i, entry['Service_Tag'], entry['Geraetetyp'], entry['Raum'],
                        entry['Modell'], entry['Beschaedigung'], entry['Ausgeliehen_von']),
                tags=(tag,)
            )
            i += 1