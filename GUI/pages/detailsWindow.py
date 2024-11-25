import tkinter as tk
from tkinter import ttk
from tkinter import *
import Datenbank.sqlite3api as sqlapi


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
        headerFrameDetailsWindow.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

        # Konfiguriere die Spalten für den Header
        headerFrameDetailsWindow.grid_columnconfigure(0, weight=1)  # Platz links
        headerFrameDetailsWindow.grid_columnconfigure(1, weight=10)  # Überschrift
        headerFrameDetailsWindow.grid_columnconfigure(2, weight=0)  # Option-Button
        headerFrameDetailsWindow.grid_columnconfigure(3, weight=0)  # Zurück-Button

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
        goBackButtonDetailsWindow.grid(row=0, column=3, sticky=tk.E, padx=20)

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

        # Input-Frame
        inputFrameDetailsWindow = tk.Frame(self, background="white")
        inputFrameDetailsWindow.grid(row=1, column=0, pady=20)

        inputFrameDetailsWindow.grid_columnconfigure(0, weight=1)  # Zentriere das Input-Frame
        inputFrameDetailsWindow.grid_columnconfigure(1, weight=1)



        sizeDetailsWindow = 30

        # Label und "Anzeige"-Felder
        serviceTagLabelDetailsWindow = tk.Label(inputFrameDetailsWindow, text="Service Tag",
                                                 font=("Arial", sizeDetailsWindow), background="white")
        serviceTagLabelDetailsWindow.grid(column=0, row=0, sticky=tk.W + tk.E, padx=20, pady=10)

        self.serviceTagEntryDetailsWindow = tk.Label(inputFrameDetailsWindow, text="",
                                                      font=("Arial", sizeDetailsWindow), background=srhGrey, bd=0,
                                                      relief=tk.SOLID, anchor="w")
        self.serviceTagEntryDetailsWindow.grid(column=1, row=0, sticky=tk.W + tk.E, padx=20, pady=10)

        typeLabelDetailsWindow = tk.Label(inputFrameDetailsWindow, text="Typ", font=("Arial", sizeDetailsWindow),
                                           background="white")
        typeLabelDetailsWindow.grid(column=0, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        self.typeEntryDetailsWindow = tk.Label(inputFrameDetailsWindow, text="", font=("Arial", sizeDetailsWindow),
                                                background=srhGrey,bd=0, relief=tk.SOLID, anchor="w")
        self.typeEntryDetailsWindow.grid(column=1, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        roomLabelDetailsWindow = tk.Label(inputFrameDetailsWindow, text="Raum", font=("Arial", sizeDetailsWindow),
                                           background="white")
        roomLabelDetailsWindow.grid(column=0, row=2, sticky=tk.W + tk.E, padx=20, pady=10)

        self.roomEntryDetailsWindow = tk.Label(inputFrameDetailsWindow, text="", font=("Arial", sizeDetailsWindow),
                                                background=srhGrey,bd=0, relief=tk.SOLID, anchor="w")
        self.roomEntryDetailsWindow.grid(column=1, row=2, sticky=tk.W + tk.E, padx=20, pady=10)

        nameLabelDetailsWindow = tk.Label(inputFrameDetailsWindow, text="Name", font=("Arial", sizeDetailsWindow),
                                           background="white")
        nameLabelDetailsWindow.grid(column=0, row=3, sticky=tk.W + tk.E, padx=20, pady=10)

        self.nameEntryDetailsWindow = tk.Label(inputFrameDetailsWindow, text="", font=("Arial", sizeDetailsWindow),
                                                background=srhGrey,bd=0, relief=tk.SOLID, anchor="w")
        self.nameEntryDetailsWindow.grid(column=1, row=3, sticky=tk.W + tk.E, padx=20, pady=10)

        damagedLabelDetailsWindow = tk.Label(inputFrameDetailsWindow, text="Beschädigung",
                                              font=("Arial", sizeDetailsWindow), background="white")
        damagedLabelDetailsWindow.grid(column=0, row=4, sticky=tk.W + tk.E, padx=20, pady=10)

        self.damagedEntryDetailsWindow = tk.Label(inputFrameDetailsWindow, text="", font=("Arial", sizeDetailsWindow),
                                                    background=srhGrey,bd=0, relief=tk.SOLID, anchor="w")
        self.damagedEntryDetailsWindow.grid(column=1, row=4, sticky=tk.W + tk.E, padx=20, pady=10)

        # Funktion zum Eintrag hinzufügen
        def editEntry():
            print("Eintrag hinzugefügt.")
            goBackDetailsWindow()

        def lend():
            print("Vorgang abgebrochen")
            goBackDetailsWindow()

        parent.editBtn = tk.PhotoImage(file="assets/Bearbeiten.png")
        parent.lendBtn = tk.PhotoImage(file="assets/Ausleihen.png")

        # Buttons in ein separates Frame
        buttonFrameAddItemPopup = tk.Frame(self, background="white")
        buttonFrameAddItemPopup.grid(row=2, column=0, pady=20)

        lendButton = tk.Button(buttonFrameAddItemPopup, image=parent.lendBtn,
                                             bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                                             command=editEntry)
        lendButton.pack(side=tk.LEFT, padx=20)  # Neben Exit-Button platzieren

        editButton = tk.Button(buttonFrameAddItemPopup, image=parent.editBtn,
                                           bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                                           command=lend)
        editButton.pack(side=tk.LEFT, padx=20)  # Links platzieren

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_data(self, data):
        # Aktualisiere die Labels basierend auf den übergebenen Daten
        self.serviceTagEntryDetailsWindow.config(text=data[1])
        self.typeEntryDetailsWindow.config(text=data[2])
        self.roomEntryDetailsWindow.config(text=data[3])
        self.nameEntryDetailsWindow.config(text=data[4])
        self.damagedEntryDetailsWindow.config(text=data[5])