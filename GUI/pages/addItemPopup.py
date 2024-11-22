import tkinter as tk

def addItemPopup(parent):
    # Toplevel-Fenster erstellen
    addPopup = tk.Toplevel(parent)
    addPopup.title("Neuer Eintrag")
    addPopup.transient(parent)  # Popup bleibt im Vordergrund des Hauptfensters
    addPopup.grab_set()         # Blockiere Interaktionen mit dem Hauptfenster
    addPopup.attributes('-topmost', True)  # Erzwinge den Fokus auf das Popup
    addPopup.configure(background="white")

    # Bildschirmbreite und -höhe ermitteln
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Fensterbreite und -höhe definieren
    window_width = 600
    window_height = 600

    # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    addPopup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    addPopup.resizable(False, False)

    # Icon setzen (optional)
    try:
        addPopup.iconbitmap("assets/srhIcon.ico")
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")

    # Erstelle einen Header-Bereich
    headerFrameAddItemPopup = tk.Frame(addPopup, height=10, background="#DF4807")
    headerFrameAddItemPopup.grid(row=0, column=0, columnspan=2, sticky=tk.W + tk.E + tk.N)

    # Spaltenkonfiguration für Zentrierung im Frame
    headerFrameAddItemPopup.grid_columnconfigure(0, weight=1)

    # Füge ein zentriertes Label hinzu
    headerLabelAddItemPopup = tk.Label(headerFrameAddItemPopup, background="#DF4807",
                                       text="Erstellen", foreground="white", font=("Arial", 40))
    headerLabelAddItemPopup.grid(row=0, column=0, sticky=tk.NSEW)

    # Input-Frame
    inputFrameAddItemPopup = tk.Frame(addPopup, background="white")
    inputFrameAddItemPopup.grid(row=1, column=0, pady=20)

    inputFrameAddItemPopup.grid_columnconfigure(0, weight=1)  # Zentriere das Input-Frame
    inputFrameAddItemPopup.grid_columnconfigure(1, weight=1)

    # Label und Eingabefeld hinzufügen
    serviceTagLabel = tk.Label(inputFrameAddItemPopup, text="Service Tag", background="white")
    serviceTagLabel.grid(row=0, column=0, padx=10, sticky=tk.E)

    serviceTagEntry = tk.Entry(inputFrameAddItemPopup, background="#d9d9d9")
    serviceTagEntry.grid(row=0, column=1, padx=10, sticky=tk.W)

    typeLabel = tk.Label(inputFrameAddItemPopup, text="Typ", background="white")
    typeLabel.grid(row=1, column=0, padx=10, sticky=tk.E)

    typeEntry = tk.Entry(inputFrameAddItemPopup, background="#d9d9d9")
    typeEntry.grid(row=1, column=1, padx=10, sticky=tk.W)

    roomLabel = tk.Label(inputFrameAddItemPopup, text="Raum", background="white")
    roomLabel.grid(row=2, column=0, padx=10, sticky=tk.E)

    roomEntry = tk.Entry(inputFrameAddItemPopup, background="#d9d9d9")
    roomEntry.grid(row=2, column=1, padx=10, sticky=tk.W)

    nameLabel = tk.Label(inputFrameAddItemPopup, text="Name", background="white")
    nameLabel.grid(row=3, column=0, padx=10, sticky=tk.E)

    nameEntry = tk.Entry(inputFrameAddItemPopup, background="#d9d9d9")
    nameEntry.grid(row=3, column=1, padx=10, sticky=tk.W)

    # Funktion zum Eintrag hinzufügen
    def submit_entry():
        print("Eintrag hinzugefügt.")
        addPopup.destroy()  # Popup schließen

    submitButton = tk.Button(addPopup, text="Hinzufügen", command=submit_entry)
    submitButton.grid(row=2, column=0, pady=20)

    addPopup.grid_rowconfigure(0, weight=0)
    addPopup.grid_rowconfigure(1, weight=1)
    addPopup.grid_rowconfigure(2, weight=0)
    addPopup.grid_columnconfigure(0, weight=1)
