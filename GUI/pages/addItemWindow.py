import tkinter as tk
from .mainPage import mainPage

def addItemPopUp:
    # Toplevel-Fenster erstellen
    popup = tk.Toplevel(self)
    popup.title("Neuer Eintrag")
    popup.geometry("300x200")

    label = tk.Label(popup, text="Füge einen neuen Eintrag hinzu:")
    label.pack(pady=10)

    entry = tk.Entry(popup)
    entry.pack(pady=5)

    def submit_entry():
        item_name = entry.get()
        # Hier kannst du den Code zum Hinzufügen des Eintrags zur Datenbank einfügen
        print(f"Neuer Eintrag hinzugefügt: {item_name}")
        popup.destroy()  # Fenster schließen

    submit_button = tk.Button(popup, text="Hinzufügen", command=submit_entry)
    submit_button.pack(pady=20)