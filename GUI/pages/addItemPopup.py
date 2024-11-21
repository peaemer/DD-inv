import tkinter as tk

def addItemPopup(parent):

    # Toplevel-Fenster erstellen
    popup = tk.Toplevel(parent)
    popup.title("Neuer Eintrag")
    popup.transient(parent)  # Popup bleibt im Vordergrund des Hauptfensters
    popup.grab_set()         # Blockiere Interaktionen mit dem Hauptfenster
    popup.attributes('-topmost', True)  # Erzwinge den Fokus auf das Popup

    # Bildschirmbreite und -höhe ermitteln
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Fensterbreite und -höhe definieren
    window_width = 960  # Halb von 1920
    window_height = 540  # Halb von 1080

    # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # Setze die Fenstergröße und Position
    popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    popup.resizable(False, False)

    # Icon setzen (optional)
    try:
        popup.iconbitmap("assets/srhIcon.ico")
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")

    # Label und Eingabefeld hinzufügen
    label = tk.Label(popup, text="Füge einen neuen Eintrag hinzu:")
    label.pack(pady=10)

    entry = tk.Entry(popup)
    entry.pack(pady=5)

    # Funktion zum Eintrag hinzufügen
    def submit_entry():
        item_name = entry.get()
        print(f"Neuer Eintrag hinzugefügt: {item_name}")
        popup.destroy()  # Popup schließen

    submit_button = tk.Button(popup, text="Hinzufügen", command=submit_entry)
    submit_button.pack(pady=20)