import tkinter as tk
from tkinter import ttk
from tkinter import *

# Schriftarten und Farbkodierungen für den Text und das GUI-Design definieren
LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"  # grauer Hintergrund für bestimmte Frames und Widgets

# Hauptseite (zweites Fenster)
class mainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")  # Hintergrundfarbe der Hauptseite auf weiß setzen

        # Funktion, um zur Login-Seite zurückzukehren
        def logOut():
            from .logInWindow import logInWindow
            controller.show_frame(logInWindow)  # zur Login-Seite wechseln

        # Funktion zur Suche (wird später mit Funktionalität ausgestattet)
        def search():
            print("I am Searching")

        # Funktion zur Filterung (wird später mit Funktionalität ausgestattet)
        def filtr():
            print("Do be filtering")

        # Funktion zum Entfernen des Platzhaltertexts im Suchfeld
        def onEntryClick(event):
            if searchEntry.get() == 'Suche':
                searchEntry.delete(0, "end")  # lösche Platzhaltertext
                searchEntry.config(fg='black')  # Textfarbe schwarz für eingegebene Inhalte

        # Funktion zum Hinzufügen des Platzhaltertexts bei Fokusverlust
        def onFocusOut(event):
            if searchEntry.get() == '':
                searchEntry.insert(0, 'Suche')  # Platzhalter wieder einfügen
                searchEntry.config(fg='grey')  # Textfarbe zurück auf grau setzen

        # Konfiguriere das Grid-Layout für die Hauptseite
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Header-Bereich erstellen
        headerFrame = tk.Frame(self, height=10, background="#DF4807")  # Header-Farbe definiert
        headerFrame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

        # Konfiguriere die Spalten und Zeilen im Header für gleichmäßige Ausrichtung
        headerFrame.grid_columnconfigure(0, weight=1)
        headerFrame.grid_rowconfigure(0, weight=1)

        # Lade und füge das Logo-Bild im Header hinzu
        self.srhHead = tk.PhotoImage(file="assets/srh.png")
        headerLabel = tk.Label(headerFrame, image=self.srhHead, background="#DF4807", foreground="white")
        headerLabel.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N + tk.W)

        # Lade das Logout-Bild und erstelle einen Button damit
        self.logOutBtn = tk.PhotoImage(file="assets/ausloggen.png")
        logOutButton = tk.Button(headerFrame, image=self.logOutBtn, command=logOut, bd=0, relief=tk.FLAT, bg="#DF4807",
                                 activebackground="#DF4807")
        logOutButton.grid(row=0, column=3, sticky=tk.E, padx=20)

        # Lade das Options-Bild und erstelle einen Button für Optionen
        self.optBtn = tk.PhotoImage(file="assets/option.png")
        optionsButton = tk.Button(headerFrame, image=self.optBtn, command=logOut, bd=0, relief=tk.FLAT, bg="#DF4807",
                                 activebackground="#DF4807")
        optionsButton.grid(row=0, column=2, sticky=tk.E, padx=20)

        # Sekundärer Header-Bereich für den Haupttitel
        greyFrame = tk.Frame(self, height=10, background="#F4EFEF")
        greyFrame.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N)

        # Haupttitel für die Inventurübersicht
        logInLabel = tk.Label(greyFrame, text="Inventurübersicht", bd=0, relief=tk.FLAT, bg="#F4EFEF", font=("Arial", 20))
        logInLabel.grid(padx=200, pady=5, row=0, column=0, sticky=tk.W)
        greyFrame.grid_columnconfigure(0, weight=1)

        # Linker Bereich zur Kategorisierung
        greyFrameSide = tk.Frame(self, height=10, background=srhGrey)
        greyFrameSide.grid(row=1, column=0, sticky=tk.W + tk.N + tk.S)

        # Label für die Kategorisierung als "Räume"
        overviewLabel = tk.Label(greyFrameSide, text="Räume", bd=0, relief=tk.FLAT, bg=srhGrey, font=("Arial", 20))
        overviewLabel.grid(padx=40, pady=5, row=0, column=0, sticky=tk.W + tk.E)

        # Such- und Filterbereich
        searchFrame = tk.Frame(self, bg="white")
        searchFrame.grid(pady=50, padx=200, row=1, column=0, sticky=tk.W + tk.E + tk.N)

        # Such-Button Bild und Funktion hinzufügen
        self.searchBtn = tk.PhotoImage(file="assets/SearchButton.png")
        searchButton = tk.Button(searchFrame, image=self.searchBtn, bd=0, relief=tk.FLAT, bg="white",
                                 activebackground="white", command=search)
        searchButton.grid(padx=10, pady=5, row=0, column=0)

        # Entry-Feld mit Platzhaltertext für Suche
        searchEntry = tk.Entry(searchFrame, bg=srhGrey, font=("Arial", 20), bd=0, fg='grey')
        searchEntry.insert(0, 'Suche')  # Platzhaltertext hinzufügen
        searchEntry.bind('<FocusIn>', onEntryClick)
        searchEntry.bind('<FocusOut>', onFocusOut)
        searchEntry.grid(column=1, row=0, columnspan=2, sticky=tk.W + tk.E, padx=5, pady=5)

        # Filter-Button Bild und Funktion hinzufügen
        self.filterBtn = tk.PhotoImage(file="assets/Filter.png")
        filterButton = tk.Button(searchFrame, image=self.filterBtn, bd=0, relief=tk.FLAT, bg="white",
                                 activebackground="white", command=filtr)
        filterButton.grid(row=0, column=3, padx=10)

        # Button zum Erstellen neuer Einträge
        self.addBtn = tk.PhotoImage(file="assets/ErstellenButton.png")
        addButton = tk.Button(self, image=self.addBtn, bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                              command=search)
        addButton.grid(padx=10, pady=5, row=2, column=0)

        # Bereich für die Anzeige der Datenbank-Einträge
        treeFrame = tk.Frame(self, background="white")
        treeFrame.grid(row=1, column=0, padx=260)

        # Erstellen des Treeview-Widgets zur Anzeige der Einträge in Spalten
        tree = ttk.Treeview(treeFrame, column=("c1", "c2", "c3", "c4", "c5"), show="headings", height=30)
        scroll = tk.Scrollbar(treeFrame, orient="vertical", command=tree.yview, bg="black",
                              activebackground="darkblue", troughcolor="grey", highlightcolor="black",
                              width=12, borderwidth=1)
        scroll.grid(row=1, column=1, sticky="ns")  # Scrollbar in den Baumansichtsrahmen einfügen
        tree.configure(yscrollcommand=scroll.set)

        # Spalten und Überschriften für die Datenanzeige im TreeView
        tree.column("# 1", anchor=CENTER, width=90)
        tree.heading("# 1", text="ID")
        tree.column("# 2", anchor=CENTER, width=310)
        tree.heading("# 2", text="Service Tag")
        tree.column("# 3", anchor=CENTER, width=310)
        tree.heading("# 3", text="Typ")
        tree.column("# 4", anchor=CENTER, width=310)
        tree.heading("# 4", text="Raum")
        tree.column("# 5", anchor=CENTER, width=310)
        tree.heading("# 5", text="Name")
        tree.grid(row=1, column=0)
        tree.tkraise()  # sicherstellen, dass TreeView über anderen Elementen liegt

        # Platzhalter für Datenbank-Einträge
        for i in range(50):
            tree.insert("", "end", text=f"Item {i}", values=(f"Wert {i}", f"Wert {i + 10}"))