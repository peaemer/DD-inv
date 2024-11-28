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

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")

        def goBackAdminWindow():
            from .mainPage import mainPage
            controller.show_frame(mainPage)

        def showSettingsWindow():
            from .settingsWindow import popUpSettings
            popUpSettings(self)

        def search():                           # funktionalität hinzufügen
            print("I am Searching")

        def addItem():
            from .addItemPopup import addItemPopup
            addItemPopup(self)

        def onEntryClick(event):
            if searchEntry.get() == 'Suche':
                searchEntry.delete(0, "end")  # Lösche den Platzhalter-Text
                searchEntry.config(fg='black')  # Setze Textfarbe auf schwarz

        def onFocusOut(event):
            if searchEntry.get() == '':
                searchEntry.insert(0, 'Suche')  # Platzhalter zurücksetzen
                searchEntry.config(fg='grey')  # Textfarbe auf grau ändern

        global tree

        # Konfiguriere das Grid-Layout für die Hauptseite
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Erstelle einen Header-Bereich
        headerFrame = tk.Frame(self, height=10, background="#DF4807")
        headerFrame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

        # Konfiguriere die Spalten für den Header
        headerFrame.grid_columnconfigure(0, weight=1)
        headerFrame.grid_rowconfigure(0, weight=1)

        self.srhHead = tk.PhotoImage(file="assets/srh.png")

        # Füge ein zentriertes Label hinzu
        headerLabel = tk.Label(headerFrame, image=self.srhHead, background="#DF4807", foreground="white")
        headerLabel.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N + tk.W)

        # Konvertiere das Bild für Tkinter
        self.logOutBtn = tk.PhotoImage(file="assets/ArrowLeft.png")

        # Füge einen Button mit dem Bild hinzu
        logOutButton = tk.Button(headerFrame, image=self.logOutBtn, command=goBackAdminWindow, bd=0, relief=tk.FLAT, bg="#DF4807",
                                 activebackground="#DF4807")
        logOutButton.grid(row=0, column=3, sticky=tk.E, padx=20)

        # Konvertiere das Bild für Tkinter
        self.optBtn = tk.PhotoImage(file="assets/option.png")

        # Füge einen Button mit dem Bild hinzu
        optionsButton = tk.Button(headerFrame,
                                  image=self.optBtn,
                                  command=showSettingsWindow,
                                  bd=0,
                                  relief=tk.FLAT,
                                  bg="#DF4807",
                                  activebackground="#DF4807")
        optionsButton.grid(row=0, column=2, sticky=tk.E, padx=20)


        greyFrame = tk.Frame(self, height=10, background="#F4EFEF")
        greyFrame.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N)

        # Füge den LogIn-Label zur Frame hinzu
        logInLabel = tk.Label(greyFrame,
                              text="User-Übersicht",
                              bd=0,
                              relief=tk.FLAT,
                              bg="#F4EFEF",
                              font=("Arial", 20))
        logInLabel.grid(padx=200, pady=5, row=0, column=0, sticky=tk.W)

        # Konfiguriere den greyFrame für zentrierte Ausrichtung
        greyFrame.grid_columnconfigure(0, weight=1)

        greyFrameSide = tk.Frame(self, height=10, background=srhGrey)
        greyFrameSide.grid(row=1, column=0, sticky=tk.W + tk.N + tk.S)

        overviewLabel = tk.Label(greyFrameSide, text="Räume", bd=0, relief=tk.FLAT, bg=srhGrey, font=("Arial", 20))
        overviewLabel.grid(padx=40, pady=5, row=0, column=0, sticky=tk.W + tk.E)

        # Verschiebe den SearchFrame nach oben, indem du seine Zeile anpasst
        searchFrame = tk.Frame(self, bg="white")
        searchFrame.grid(pady=50, padx=200, row=1, column=0, sticky=tk.W + tk.E + tk.N)

        searchFrame.grid_columnconfigure(0, weight=0)
        searchFrame.grid_columnconfigure(1, weight=1)
        searchFrame.grid_columnconfigure(2, weight=0)

        self.searchBtn = tk.PhotoImage(file="assets/SearchButton.png")
        searchButton = tk.Button(searchFrame,
                                 image=self.searchBtn,
                                 bd=0,
                                 relief=tk.FLAT,
                                 bg="white",
                                 activebackground="white",
                                 command=search)
        searchButton.grid(padx=10, pady=5, row=0, column=0)

        # Entry-Feld mit Platzhalter-Text
        searchEntry = tk.Entry(searchFrame, bg=srhGrey, font=("Arial", 20), bd=0, fg='grey')
        searchEntry.insert(0, 'Suche')  # Setze den Platzhalter-Text

        # Events für Klick und Fokusverlust hinzufügen
        searchEntry.bind('<FocusIn>', onEntryClick)
        searchEntry.bind('<FocusOut>', onFocusOut)
        searchEntry.grid(column=1, row=0, columnspan=2, sticky=tk.W + tk.E, padx=5, pady=5)


        # Ändere die Position des TreeFrames auf row=3
        userTreeFrame = tk.Frame(self, background="white")
        userTreeFrame.grid(row=1, column=0, padx=260)

        self.addBtn = tk.PhotoImage(file="assets/Erstellen.png")
        userAddButton = tk.Button(userTreeFrame,image=self.addBtn, bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=addItem)
        userAddButton.grid(padx=10, pady=5, row=0, column=0, sticky="e")

        user_tree = ttk.Treeview(userTreeFrame, column=("c1", "c2", "c3", "c4", "c5"), show="headings", height=30)

        userScroll = tk.Scrollbar(
            userTreeFrame,
            orient="vertical",
            command=user_tree.yview,
            bg="black",
            activebackground="darkblue",
            troughcolor="grey",
            highlightcolor="black",
            width=15,
            borderwidth=1
        )
        userScroll.grid(row=1, column=1, sticky="ns")
        user_tree.configure(yscrollcommand=userScroll.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        user_tree.tag_configure("oddrow", background="#f7f7f7")
        user_tree.tag_configure("evenrow", background="white")

        ### listbox for directories
        user_tree.column("# 1", anchor=CENTER, width=60)
        user_tree.heading("# 1", text="ID", )
        user_tree.column("# 2", anchor=CENTER, width=125)
        user_tree.heading("# 2", text="Nutzername")
        user_tree.column("# 3", anchor=CENTER, width=150)
        user_tree.heading("# 3", text="Passwort")
        user_tree.column("# 4", anchor=CENTER, width=200)
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
        def onItemSelected(event):
            try:
                selectedItem = user_tree.focus()
                print(f"Ausgewähltes Item: {selectedItem}")  # Debug
                if selectedItem:
                    from .detailsWindow import detailsWindow, showDetails
                    showDetails(selectedItem, tree, controller)
            except Exception as e:
                print(f"Fehler bei der Auswahl: {e}")

        # Binde die Ereignisfunktion an die Treeview
        user_tree.bind("<<TreeviewSelect>>", onItemSelected)

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