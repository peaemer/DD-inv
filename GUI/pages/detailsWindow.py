import tkinter as tk
from tkinter import ttk
from tkinter import *
import Datenbank.sqlite3api as db


LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"


def showDetails(selectedItem, tree, controller):
    # Daten aus der ausgewählten Zeile
    data = tree.item(selectedItem, "values")
    print(f"Daten des ausgewählten Items: {data}")

    # Frame aktualisieren und anzeigen
    details = controller.frames[detailsWindow]
    details.update_data(data)  # Methode in detailsWindow aufrufen
    controller.show_frame(detailsWindow)  # Zeige die Details-Seite


class detailsWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="white")

        def goBackDetailsWindow():
            from .mainPage import mainPage
            controller.show_frame(mainPage)

        def showSettingsWindowDetailsWindow():
            from .settingsWindow import popUpSettings
            popUpSettings(self)

        self.goBackBtnDetailsWindow = tk.PhotoImage(file="assets/ArrowLeft.png")
        self.optBtnDetailsWindow = tk.PhotoImage(file="assets/option.png")

        # Erstelle einen Header-Bereich
        headerFrameDetailsWindow = tk.Frame(self, height=10, background="#DF4807")
        headerFrameDetailsWindow.grid(row=0, column=0,columnspan=2, sticky=tk.W + tk.E + tk.N)

        # Überschrift mittig zentrieren
        headerFrameDetailsWindow.grid_columnconfigure(0, weight=1)  # Platz links
        headerFrameDetailsWindow.grid_columnconfigure(1, weight=3)  # Überschrift zentriert (größerer Gewichtungsfaktor)
        headerFrameDetailsWindow.grid_columnconfigure(2, weight=1)  # Option-Button


        # Zentriere das Label in Spalte 1
        headerLabelDetailsWindow = tk.Label(
            headerFrameDetailsWindow,
            text="Details",
            background="#DF4807",
            foreground="white",
            font=("Arial", 60)
        )
        headerLabelDetailsWindow.grid(row=0, column=1, pady=40, sticky=tk.W + tk.E)

        # Buttons in Spalten 2 und 3 platzieren
        goBackButtonDetailsWindow = tk.Button(
            headerFrameDetailsWindow,
            image=self.goBackBtnDetailsWindow,
            command=goBackDetailsWindow,
            bd=0,
            relief=tk.FLAT,
            bg="#DF4807",
            activebackground="#DF4807"
        )
        goBackButtonDetailsWindow.grid(row=0, column=0, sticky=tk.W, padx=20)

        optionsButtonDetailsWindow = tk.Button(
            headerFrameDetailsWindow,
            image=self.optBtnDetailsWindow,
            command=showSettingsWindowDetailsWindow,
            bd=0,
            relief=tk.FLAT,
            bg="#DF4807",
            activebackground="#DF4807"
        )
        optionsButtonDetailsWindow.grid(row=0, column=2, sticky=tk.E, padx=20)


        # Container für Input- und Tree-Frame
        containerFrame = tk.Frame(self, background="white")
        containerFrame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Konfiguration der Container-Spalten
        containerFrame.grid_columnconfigure(0, weight=1)  # Baumansicht
        containerFrame.grid_columnconfigure(1, weight=1)  # Eingabefelder



        sizeDetailsWindow = 30

        treeStyle = ttk.Style()
        treeStyle.theme_use("default")  # alt, classic,xpnative,winnative, default
        treeStyle.configure("Treeview.Heading", font=("Arial", 14))
        treeStyle.configure("Treeview", rowheight=20, font=("Arial", 12))

        # Ändere die Position des TreeFrames auf row=3
        treeFrameDetailsWindow = tk.Frame(containerFrame, background="red", width=200, height=400)
        treeFrameDetailsWindow.grid(row=0, column=0, padx=40, sticky="")

        treeDetailsWindow = ttk.Treeview(treeFrameDetailsWindow, column=("c1", "c2", "c3"), show="headings", height=30)

        scrollDetailsWindow = tk.Scrollbar(
            treeFrameDetailsWindow,
            orient="vertical",
            command=treeDetailsWindow.yview,
            bg="black",
            activebackground="darkblue",
            troughcolor="grey",
            highlightcolor="black",
            width=15,
            borderwidth=1
        )
        scrollDetailsWindow.grid(row=1, column=1, sticky="ns")
        treeDetailsWindow.configure(yscrollcommand=scrollDetailsWindow.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        treeDetailsWindow.tag_configure("oddrow", background="#f7f7f7")
        treeDetailsWindow.tag_configure("evenrow", background="white")

        ### listbox for directories
        treeDetailsWindow.column("# 1", anchor=CENTER, width=180)
        treeDetailsWindow.heading("# 1", text="Ausleiher", )
        treeDetailsWindow.column("# 2", anchor=CENTER, width=180)
        treeDetailsWindow.heading("# 2", text="Ausgeliehen")
        treeDetailsWindow.column("# 3", anchor=CENTER, width=180)
        treeDetailsWindow.heading("# 3", text="Zurückgegeben")
        treeDetailsWindow.grid(row=1, column=0)
        treeDetailsWindow.tkraise()

        # Input-Frame
        inputFrameDetailsWindow = tk.Frame(containerFrame, background="white")
        inputFrameDetailsWindow.grid(row=0, column=1, pady=20, sticky="nsew")

        inputFrameDetailsWindow.grid_columnconfigure(0, weight=1)  # Zentriere das Input-Frame
        inputFrameDetailsWindow.grid_columnconfigure(1, weight=1)

        # Service Tag
        serviceTagLabelDetailsWindow = tk.Label(inputFrameDetailsWindow, text="Service Tag",
                                                font=("Arial", sizeDetailsWindow), background="white")
        serviceTagLabelDetailsWindow.grid(column=0, row=0, sticky=tk.W + tk.E, padx=20, pady=10)

        self.serviceTagEntryDetailsWindow = tk.Entry(inputFrameDetailsWindow, font=("Arial", sizeDetailsWindow),
                                                     background=srhGrey, relief=tk.SOLID)
        self.serviceTagEntryDetailsWindow.grid(column=1, row=0, sticky=tk.W + tk.E, padx=20, pady=10)

        # Typ
        typeLabelDetailsWindow = tk.Label(inputFrameDetailsWindow, text="Typ",
                                          font=("Arial", sizeDetailsWindow), background="white")
        typeLabelDetailsWindow.grid(column=0, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        self.typeEntryDetailsWindow = tk.Entry(inputFrameDetailsWindow, font=("Arial", sizeDetailsWindow),
                                               background=srhGrey, relief=tk.SOLID)
        self.typeEntryDetailsWindow.grid(column=1, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        # Raum
        roomLabelDetailsWindow = tk.Label(inputFrameDetailsWindow, text="Raum",
                                          font=("Arial", sizeDetailsWindow), background="white")
        roomLabelDetailsWindow.grid(column=0, row=2, sticky=tk.W + tk.E, padx=20, pady=10)

        self.roomEntryDetailsWindow = tk.Entry(inputFrameDetailsWindow, font=("Arial", sizeDetailsWindow),
                                               background=srhGrey, relief=tk.SOLID)
        self.roomEntryDetailsWindow.grid(column=1, row=2, sticky=tk.W + tk.E, padx=20, pady=10)

        # Name
        nameLabelDetailsWindow = tk.Label(inputFrameDetailsWindow, text="Name",
                                          font=("Arial", sizeDetailsWindow), background="white")
        nameLabelDetailsWindow.grid(column=0, row=3, sticky=tk.W + tk.E, padx=20, pady=10)

        self.nameEntryDetailsWindow = tk.Entry(inputFrameDetailsWindow, font=("Arial", sizeDetailsWindow),
                                               background=srhGrey, relief=tk.SOLID)
        self.nameEntryDetailsWindow.grid(column=1, row=3, sticky=tk.W + tk.E, padx=20, pady=10)

        # Beschädigung
        damagedLabelDetailsWindow = tk.Label(inputFrameDetailsWindow, text="Beschädigung",
                                             font=("Arial", sizeDetailsWindow), background="white")
        damagedLabelDetailsWindow.grid(column=0, row=4, sticky=tk.W + tk.E, padx=20, pady=10)

        self.damagedEntryDetailsWindow = tk.Entry(inputFrameDetailsWindow, font=("Arial", sizeDetailsWindow),
                                                  background=srhGrey, relief=tk.SOLID)
        self.damagedEntryDetailsWindow.grid(column=1, row=4, sticky=tk.W + tk.E, padx=20, pady=10)

        # Funktion zum Eintrag hinzufügen
        def refreshEntry():
            #update
            print("nix")

        def deleteEntry():
            db.delete_hardware_by_service_tag(self.serviceTagEntryDetailsWindow.get())
            from .mainPage import mainPage
            mainPage.update_treeview_with_data()
            controller.show_frame(mainPage)

        def lend(data):
            print("Übergebene Daten:", data)
            from .lendPopup import lendPopup
            lendPopup(self, data)

        self.editBtn = tk.PhotoImage(file="assets/Aktualisieren.png")
        self.lendBtn = tk.PhotoImage(file="assets/Ausleihen.png")
        self.deleteBtn = tk.PhotoImage(file="assets/Loeschen.png")

        # Buttons in ein separates Frame
        buttonFrameAddItemPopup = tk.Frame(self, background="white")
        buttonFrameAddItemPopup.grid(row=2, column=0, pady=20)

        lendButton = tk.Button(buttonFrameAddItemPopup, image=self.lendBtn,
                                             bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                                             command=lambda: lend({"name": self.nameEntryDetailsWindow.get()}))
        lendButton.pack(side=tk.LEFT, padx=20)  # Neben Exit-Button platzieren


        deleteButton = tk.Button(buttonFrameAddItemPopup, image=self.deleteBtn,
                               bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                               command= deleteEntry)
        deleteButton.pack(side=tk.LEFT, padx=20)  # Neben Exit-Button platzieren


        editButton = tk.Button(buttonFrameAddItemPopup, image=self.editBtn,
                                           bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                                           command=refreshEntry)
        editButton.pack(side=tk.LEFT, padx=20)  # Links platzieren

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(0, weight=1)

    def update_data(self, data):
        # Daten in die Entry-Felder einfügen
        self.serviceTagEntryDetailsWindow.delete(0, tk.END)
        self.serviceTagEntryDetailsWindow.insert(0, data[1])

        self.typeEntryDetailsWindow.delete(0, tk.END)
        self.typeEntryDetailsWindow.insert(0, data[2])

        self.roomEntryDetailsWindow.delete(0, tk.END)
        self.roomEntryDetailsWindow.insert(0, data[3])

        self.nameEntryDetailsWindow.delete(0, tk.END)
        self.nameEntryDetailsWindow.insert(0, data[4])

        self.damagedEntryDetailsWindow.delete(0, tk.END)
        self.damagedEntryDetailsWindow.insert(0, data[5])
