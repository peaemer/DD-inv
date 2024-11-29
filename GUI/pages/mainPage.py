import tkinter as tk
from tkinter import ttk
from tkinter import *
import Datenbank.sqlite3api as sqlapi
import cache
from GUI.SearchBar import SearchBar

LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"


# Hauptseite (zweites Fenster)
class mainPage(tk.Frame):
    #if (cache.user_group == "admin"):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")

        def showSettingsWindow():
            from .settingsWindow import popUpSettings
            popUpSettings(self)

        def showAdminWindow():
            from .adminWindow import adminWindow
            controller.show_frame(adminWindow)

        # Speichere die Funktion als Attribut, um später darauf zuzugreifen
        self.showAdminWindow = showAdminWindow

        def logOut():
            from .logInWindow import logInWindow
            cache.user_group = None  # Benutzergruppe zurücksetzen
            print("--------------------------------")
            print(f"Cache-Werte nach logOut: Gruppe={cache.user_group}, Benutzer={cache.user_name}")
            controller.show_frame(logInWindow)

        def search(event=None):                           # funktionalität hinzufügen
            SearchBar.completed_search(searchEntry.get())
            search_entrys = []
            for entry in sqlapi.fetch_hardware():
                for value in entry:
                    if searchEntry.get().lower() in str(entry[value]).lower():
                        if entry not in search_entrys:
                            search_entrys.append(entry)
            self.update_treeview_with_data(data=search_entrys)

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
        self.headerFrame = tk.Frame(self, height=10, background="#DF4807")
        self.headerFrame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

        # Konfiguriere die Spalten für den Header
        self.headerFrame.grid_columnconfigure(0, weight=1)
        self.headerFrame.grid_rowconfigure(0, weight=1)

        self.srhHead = tk.PhotoImage(file="assets/srh.png")

        # Füge ein zentriertes Label hinzu
        headerLabel = tk.Label(self.headerFrame, image=self.srhHead, background="#DF4807", foreground="white")
        headerLabel.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N + tk.W)

        # Konvertiere das Bild für Tkinter
        self.logOutBtn = tk.PhotoImage(file="assets/ausloggen.png")

        # Füge einen Button mit dem Bild hinzu
        logOutButton = tk.Button(self.headerFrame, image=self.logOutBtn, command=logOut, bd=0, relief=tk.FLAT, bg="#DF4807",
                                 activebackground="#DF4807")
        logOutButton.grid(row=0, column=3, sticky=tk.E, padx=20)

        # Konvertiere das Bild für Tkinter
        self.optBtn = tk.PhotoImage(file="assets/option.png")

        # Füge einen Button mit dem Bild hinzu
        optionsButton = tk.Button(self.headerFrame,
                                  image=self.optBtn,
                                  command=showSettingsWindow,
                                  bd=0,
                                  relief=tk.FLAT,
                                  bg="#DF4807",
                                  activebackground="#DF4807")
        optionsButton.grid(row=0, column=2, sticky=tk.E, padx=20)

        self.adminBtn = tk.PhotoImage(file="assets/Key.png")




        greyFrame = tk.Frame(self, height=10, background="#F4EFEF")
        greyFrame.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N)

        # Füge den LogIn-Label zur Frame hinzu
        logInLabel = tk.Label(greyFrame,
                              text="Inventur-Übersicht",
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
        searchFrame.grid(pady=50, padx=185, row=1, column=0, sticky=tk.W + tk.E + tk.N)

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
        searchButton.grid(padx=5, pady=5, row=0, column=0)

        # Entry-Feld mit Platzhalter-Text
        searchEntry = tk.Entry(searchFrame, bg=srhGrey, font=("Arial", 20), bd=0, fg='grey')
        searchEntry.insert(0, 'Suche')  # Setze den Platzhalter-Text

        # Events für Klick und Fokusverlust hinzufügen
        searchEntry.bind('<FocusIn>', onEntryClick)
        searchEntry.bind('<FocusOut>', onFocusOut)
        searchEntry.bind('<Return>', search)
        searchEntry.grid(column=1, row=0, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)



        treeStyle = ttk.Style()
        treeStyle.theme_use("default") #alt, classic,xpnative,winnative, default
        treeStyle.configure("Treeview.Heading",rowheight=50, font=("Arial", 20))
        treeStyle.configure("Treeview", rowheight=40, font=("Arial", 14))



        # Ändere die Position des TreeFrames auf row=3
        treeFrame = tk.Frame(self, background="white")
        treeFrame.grid(row=1, column=0, padx=0)

        self.addBtn = tk.PhotoImage(file="assets/Erstellen.png")
        addButton = tk.Button(treeFrame,image=self.addBtn, bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=addItem)
        addButton.grid(padx=10, pady=5, row=0, column=0, sticky="e")

        tree = ttk.Treeview(treeFrame, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show="headings", height=15)

        scroll = tk.Scrollbar(
            treeFrame,
            orient="vertical",
            command=tree.yview,
            bg="black",
            activebackground="darkblue",
            troughcolor="grey",
            highlightcolor="black",
            width=15,
            borderwidth=1
        )
        scroll.grid(row=1, column=1, sticky="ns")
        tree.configure(yscrollcommand=scroll.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        tree.tag_configure("oddrow", background="#f7f7f7")
        tree.tag_configure("evenrow", background="white")

        ### listbox for directories
        tree.column("# 1", anchor=CENTER, width=60)
        tree.heading("# 1", text="ID", )
        tree.column("# 2", anchor=CENTER, width=155)
        tree.heading("# 2", text="Service Tag")
        tree.column("# 3", anchor=CENTER, width=250)
        tree.heading("# 3", text="Typ")
        tree.column("# 4", anchor=CENTER, width=100)
        tree.heading("# 4", text="Raum")
        tree.column("# 5", anchor=CENTER, width=250)
        tree.heading("# 5", text="Name")
        tree.column("# 6", anchor=CENTER, width=300)
        tree.heading("# 6", text="Beschädigung")
        tree.column("# 7", anchor=CENTER, width=250)
        tree.heading("# 7", text="Ausgeliehen von")
        tree.grid(row=1, column=0)
        tree.tkraise()

        def insert_data(self):
            i = 0
            for entry in sqlapi.fetch_hardware():
                # Bestimme das Tag für die aktuelle Zeile
                tag = "evenrow" if i % 2 == 0 else "oddrow"

                # Daten mit dem Tag in das Treeview einfügen
                tree.insert(
                    "",
                    "end",
                    text=f"{entry['Service_Tag']}",
                    values=(
                        i,
                        entry['Service_Tag'],
                        entry['Geraetetype'],
                        entry['Raum'],
                        entry['Modell'],
                        entry['Beschaedigung'],
                        entry['Ausgeliehen_von']
                    ),
                    tags=(tag,)
                )
                i += 1
        insert_data(self)

        # Funktion für das Ereignis-Binding
        def onItemSelected(event):
            try:
                selectedItem = tree.focus()
                print(f"Ausgewähltes Item: {selectedItem}")  # Debug
                if selectedItem:
                    from .detailsWindow import detailsWindow, showDetails
                    showDetails(selectedItem, tree, controller)
            except Exception as e:
                print(f"Fehler bei der Auswahl: {e}")

        # Binde die Ereignisfunktion an die Treeview
        tree.bind("<Double-1>", onItemSelected)

    def update_treeview_with_data(self = None, data=None):
        # Clear the current treeview contents
        tree.delete(*tree.get_children())

        # If no data is provided, fetch the data from sqlapi
        if data is None:
            data = sqlapi.fetch_hardware()

        for entry in data:
            tag = "evenrow" if entry['ID'] % 2 == 0 else "oddrow"
            tree.insert(
                "",
                "end",
                values=(entry['ID'], entry['Service_Tag'], entry['Geraetetype'], entry['Raum'],
                        entry['Modell'], entry['Beschaedigung'], entry['Ausgeliehen_von']),
                tags=(tag,)
            )

    def on_load(self):
        """Diese Methode wird aufgerufen, nachdem die Seite vollständig geladen ist."""
        print(f"{self.__class__.__name__} geladen")

        # Überprüfe die Benutzergruppe
        print(f"Überprüfe Benutzergruppe: {cache.user_group}")  # Debug-Print für die Benutzergruppe
        if cache.user_group == "Admin":
            print("Als Admin eingeloggt.")

            # Überprüfe, ob der Admin-Button bereits existiert
            if not hasattr(self, "adminButton"):
                print(
                    "Admin-Button existiert noch nicht. Erstelle den Admin-Button.")  # Debug-Print für das Erstellen des Buttons
                # Erstelle den Admin-Button, wenn er noch nicht existiert
                self.adminButton = tk.Button(
                    self.headerFrame,
                    image=self.adminBtn,
                    command=self.showAdminWindow,  # Funktion für Admin-Button
                    bd=0,
                    relief=tk.FLAT,
                    bg="#DF4807",
                    activebackground="#DF4807"
                )
                self.adminButton.grid(row=0, column=1, sticky=tk.E, padx=20)
                print("Admin-Button wurde erfolgreich erstellt und platziert.")  # Bestätigung der Erstellung
            else:
                self.adminButton.grid(row=0, column=1, sticky=tk.E, padx=20)
                print(
                    "Admin-Button existiert bereits. Keine Erstellung notwendig.")  # Wenn der Button bereits existiert
        else:
            print("Nicht als Admin eingeloggt.")  # Benutzer ist kein Admin
            # Entferne den Admin-Button, falls er existiert
            if hasattr(self, "adminButton"):
                print("Admin-Button existiert, entferne ihn.")  # Debug-Print für das Entfernen des Buttons
                self.adminButton.grid_remove()
            else:
                print("Kein Admin-Button zum Entfernen gefunden.")  # Wenn kein Button vorhanden ist

        self.update_treeview_with_data()