import tkinter as tk
from tkinter import ttk
from tkinter import *



LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"


# Hauptseite (zweites Fenster)
class mainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Konfiguriere das Grid-Layout für die Hauptseite
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Erstelle einen Header-Bereich
        headerFrame = tk.Frame(self, height=10, background="#DF4807")
        headerFrame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

        # Konfiguriere die Spalten für den Header
        headerFrame.grid_columnconfigure(0, weight=1)
        headerFrame.grid_columnconfigure(1, weight=0)
        headerFrame.grid_columnconfigure(2, weight=1)
        headerFrame.grid_columnconfigure(3, weight=0)
        headerFrame.grid_rowconfigure(0, weight=1)

        self.srhHead = tk.PhotoImage(file="assets/srhHeader.png")

        # Füge ein zentriertes Label hinzu
        headerLabel = tk.Label(headerFrame, image=self.srhHead, background="#DF4807", foreground="white")
        headerLabel.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N + tk.W)

        # Funktion für den Logout-Button
        def logOut():
            from .logInWindow import logInWindow
            controller.show_frame(logInWindow)  # funktionalität hinzufügen

        # Konvertiere das Bild für Tkinter
        self.logOutBtn = tk.PhotoImage(file="assets/ausloggen.png")

        # Füge einen Button mit dem Bild hinzu
        logOutButton = tk.Button(headerFrame, image=self.logOutBtn, command=logOut, bd=0, relief=tk.FLAT, bg="#DF4807",
                                 activebackground="#DF4807")
        logOutButton.grid(row=0, column=3, sticky=tk.E, padx=20)

        treeFrame = tk.Frame(self, background='white')
        treeFrame.grid(row=1, column=0)

        tree = ttk.Treeview(treeFrame, column=("c1", "c2", "c3", "c4", "c5"), show="headings", height=5)

        scroll = ttk.Scrollbar(treeFrame, orient="vertical", command=tree.yview)
        scroll.grid(row=0, column=1)
        tree.configure(yscrollcommand=scroll.set)

        ### listbox for directories
        tree.column("# 1", anchor=CENTER, width=50)
        tree.heading("# 1", text="ID")
        tree.column("# 2", anchor=CENTER, width=235)
        tree.heading("# 2", text="Service Tag")
        tree.column("# 3", anchor=CENTER, width=235)
        tree.heading("# 3", text="Typ")
        tree.column("# 4", anchor=CENTER, width=235)
        tree.heading("# 4", text="Raum")
        tree.column("# 5", anchor=CENTER, width=235)
        tree.heading("# 5", text="Name")
        tree.grid(row=0, column=0)

        # Hier muss die Datenbank hinzugefügt werden
        dataValue = open("dataList", "r")
        dataValue = []
        for i in dataValue:
            lineList = i.split()
            dataValue.append(lineList)

        for i in dataValue:
            tree.insert(" ", "end", values=(i))



