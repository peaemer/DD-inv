import tkinter as tk
from tkinter import ttk
from tkinter import *
import Datenbank.sqlite3api as sqlapi


LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"


# Hauptseite (zweites Fenster)
class mainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")


        def showSettingsWindow():
            from .settingsWindow import popUpSettings
            popUpSettings(self)

        def logOut():
            from .logInWindow import logInWindow
            controller.show_frame(logInWindow)  # funktionalität hinzufügen

        def search():                           # funktionalität hinzufügen
            print("I am Searching")


        def filtr():                            # funktionalität hinzufügen
            print("Do be filtering")

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
        self.logOutBtn = tk.PhotoImage(file="assets/ausloggen.png")

        # Füge einen Button mit dem Bild hinzu
        logOutButton = tk.Button(headerFrame, image=self.logOutBtn, command=logOut, bd=0, relief=tk.FLAT, bg="#DF4807",
                                 activebackground="#DF4807")
        logOutButton.grid(row=0, column=3, sticky=tk.E, padx=20)

        # Konvertiere das Bild für Tkinter
        self.optBtn = tk.PhotoImage(file="assets/option.png")

        # Füge einen Button mit dem Bild hinzu
        optionsButton = tk.Button(headerFrame, image=self.optBtn, command=showSettingsWindow, bd=0, relief=tk.FLAT, bg="#DF4807",
                                 activebackground="#DF4807")
        optionsButton.grid(row=0, column=2, sticky=tk.E, padx=20)



        greyFrame = tk.Frame(self, height=10, background="#F4EFEF")
        greyFrame.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N)

        # Füge den LogIn-Label zur Frame hinzu
        logInLabel = tk.Label(greyFrame, text="Inventur-Übersicht", bd=0, relief=tk.FLAT, bg="#F4EFEF", font=("Arial", 20))
        logInLabel.grid(padx=200, pady=5, row=0, column=0, sticky=tk.W)

        # Konfiguriere den greyFrame für zentrierte Ausrichtung
        greyFrame.grid_columnconfigure(0, weight=1)

        greyFrameSide = tk.Frame(self, height=10, background=srhGrey)
        greyFrameSide.grid(row=1, column=0, sticky=tk.W + tk.N + tk.S)

        overviewLabel = tk.Label(greyFrameSide, text="Räume", bd=0, relief=tk.FLAT, bg=srhGrey, font=("Arial", 20))
        overviewLabel.grid(padx=40, pady=5, row=0, column=0, sticky=tk.W + tk.E)

        # Verschiebe den SearchFrame nach oben, indem du seine Zeile anpasst
        searchFrame = tk.Frame(self,bg="white")
        searchFrame.grid(pady=50, padx=200,row=1, column=0, sticky=tk.W + tk.E + tk.N)

        searchFrame.grid_columnconfigure(0, weight=0)
        searchFrame.grid_columnconfigure(1, weight=1)
        searchFrame.grid_columnconfigure(2, weight=0)

        self.searchBtn = tk.PhotoImage(file="assets/SearchButton.png")
        searchButton = tk.Button(searchFrame, image=self.searchBtn, bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=search)
        searchButton.grid(padx=10, pady=5, row=0, column=0)

        # Entry-Feld mit Platzhalter-Text
        searchEntry = tk.Entry(searchFrame, bg=srhGrey, font=("Arial", 20), bd=0, fg='grey')
        searchEntry.insert(0, 'Suche')  # Setze den Platzhalter-Text

        # Events für Klick und Fokusverlust hinzufügen
        searchEntry.bind('<FocusIn>', onEntryClick)
        searchEntry.bind('<FocusOut>', onFocusOut)
        searchEntry.grid(column=1, row=0, columnspan=2, sticky=tk.W + tk.E, padx=5, pady=5)

        self.filterBtn = tk.PhotoImage(file="assets/Filter.png")
        filterButton = tk.Button(searchFrame, image=self.filterBtn, bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=filtr)
        filterButton.grid(row=0, column=3, padx=10)

        # Ändere die Position des TreeFrames auf row=3
        treeFrame = tk.Frame(self, background="white")
        treeFrame.grid(row=1, column=0, padx=260)

        self.addBtn = tk.PhotoImage(file="assets/ErstellenButton.png")
        addButton = tk.Button(treeFrame,image=self.addBtn, bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=addItem)
        addButton.grid(padx=10, pady=5, row=0, column=0, sticky="e")

        tree = ttk.Treeview(treeFrame, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show="headings", height=30)

        scroll = tk.Scrollbar(
            treeFrame,
            orient="vertical",
            command=tree.yview,
            bg="black",
            activebackground="darkblue",
            troughcolor="grey",
            highlightcolor="black",
            width=12,
            borderwidth=1
        )
        scroll.grid(row=1, column=1,sticky="ns")
        tree.configure(yscrollcommand=scroll.set)

        ### listbox for directories
        tree.column("# 1", anchor=CENTER, width=70)
        tree.heading("# 1", text="ID")
        tree.column("# 2", anchor=CENTER, width=250)
        tree.heading("# 2", text="Service Tag")
        tree.column("# 3", anchor=CENTER, width=250)
        tree.heading("# 3", text="Typ")
        tree.column("# 4", anchor=CENTER, width=100)
        tree.heading("# 4", text="Raum")
        tree.column("# 5", anchor=CENTER, width=250)
        tree.heading("# 5", text="Name")
        tree.column("# 6", anchor=CENTER, width=100)
        tree.heading("# 6", text="Beschaedigung")
        tree.column("# 7", anchor=CENTER, width=250)
        tree.heading("# 7", text="Ausgeliehen Von")
        tree.grid(row=1, column=0)
        tree.tkraise()

        i = 0
        for entry in sqlapi.fetch_hardware():
            tree.insert("", "end", text=f"{entry['Service_Tag']}", values=(i, entry['Service_Tag'],entry['Geraetetyp'],entry['Standort'],entry['Modell'],entry['Beschaedigung'],entry['Ausgeliehen_von']))
            i+=1



        #Macht die
        def showDetails(selected_item):
            """Öffnet ein neues Fenster mit den Details des ausgewählten Elements."""
            # Neues Fenster erstellen
            detailsWindow = tk.Toplevel(self)
            detailsWindow.title("Details")
            detailsWindow.geometry("400x400")
            detailsWindow.configure(background="white")  # Hintergrundfarbe festlegen
            detailsWindow.transient(self)  # Popup bleibt im Vordergrund des Hauptfensters
            detailsWindow.attributes('-topmost', True)  # Erzwinge den Fokus auf das Popup

            # Daten aus der ausgewählten Zeile
            data = tree.item(selected_item, "values")
            print(f"Daten des ausgewählten Items: {data}")

            # Zeige die Daten im neuen Fenster
            tk.Label(detailsWindow, text="Details des ausgewählten Elements:", font=("Arial", 16)).pack(pady=10)
            tk.Label(detailsWindow, text=f"ID: {data[0]}").pack(pady=5)
            tk.Label(detailsWindow, text=f"Service Tag: {data[1]}").pack(pady=5)
            tk.Label(detailsWindow, text=f"Typ: {data[2]}").pack(pady=5)
            tk.Label(detailsWindow, text=f"Raum: {data[3]}").pack(pady=5)
            tk.Label(detailsWindow, text=f"Name: {data[4]}").pack(pady=5)
            tk.Label(detailsWindow, text=f"Beschädigung: {data[5]}").pack(pady=5)
            tk.Label(detailsWindow, text=f"Ausgeliehen Von: {data[6]}").pack(pady=5)


        # Funktion für das Ereignis-Binding
        def onItemSelected(event):
            try:
                selectedItem = tree.focus()
                print(f"Ausgewähltes Item: {selectedItem}")  # Debug
                if selectedItem:
                    show_details(selectedItem)
            except Exception as e:
                print(f"Fehler bei der Auswahl: {e}")


        # Binde die Ereignisfunktion an die Treeview
        tree.bind("<<TreeviewSelect>>", onItemSelected)