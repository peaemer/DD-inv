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

        self.labels = []  # Platz für die Labels
        self.title_label = tk.Label(self, text="Details des ausgewählten Elements:", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Erzeuge Platzhalter-Labels
        for i in range(7):
            label = tk.Label(self, text="")  # Leeres Label
            label.pack(pady=5)
            self.labels.append(label)

    def update_data(self, data):
        # Aktualisiere die Label-Texte basierend auf `data`
        label_texts = [
            f"ID: {data[0]}",
            f"Service Tag: {data[1]}",
            f"Typ: {data[2]}",
            f"Raum: {data[3]}",
            f"Name: {data[4]}",
            f"Beschädigung: {data[5]}",
            f"Ausgeliehen Von: {data[6]}"
        ]

        for i, text in enumerate(label_texts):
            self.labels[i].config(text=text)