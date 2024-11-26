import tkinter as tk
import Datenbank.sqlite3api as db

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
    window_width = 650
    window_height = 650

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

    sizeAddItemPopup = 16

    # Label und Eingabefeld hinzufügen
    serviceTagLabelAddItemPopup = tk.Label(inputFrameAddItemPopup, text="Service Tag", background="white", font=("Arial",sizeAddItemPopup))
    serviceTagLabelAddItemPopup.grid(row=0, column=0, padx=0, pady=20, sticky=tk.E)

    serviceTagEntryAddItemPopup = tk.Entry(inputFrameAddItemPopup, background="#d9d9d9", font=("Arial",sizeAddItemPopup), bd=0)
    serviceTagEntryAddItemPopup.grid(row=0, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    typeLabelAddItemPopup = tk.Label(inputFrameAddItemPopup, text="Typ", background="white", font=("Arial",sizeAddItemPopup))
    typeLabelAddItemPopup.grid(row=1, column=0, padx=0, pady=20, sticky=tk.E)

    typeEntryAddItemPopup = tk.Entry(inputFrameAddItemPopup, background="#d9d9d9", font=("Arial",sizeAddItemPopup), bd=0)
    typeEntryAddItemPopup.grid(row=1, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    roomLabelAddItemPopup = tk.Label(inputFrameAddItemPopup, text="Raum", background="white", font=("Arial",sizeAddItemPopup))
    roomLabelAddItemPopup.grid(row=2, column=0, padx=0, pady=20, sticky=tk.E)

    roomEntryAddItemPopup = tk.Entry(inputFrameAddItemPopup, background="#d9d9d9", font=("Arial",sizeAddItemPopup), bd=0)
    roomEntryAddItemPopup.grid(row=2, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    nameLabelAddItemPopup = tk.Label(inputFrameAddItemPopup, text="Name", background="white", font=("Arial",sizeAddItemPopup))
    nameLabelAddItemPopup.grid(row=3, column=0, padx=0, pady=20, sticky=tk.E)

    nameEntryAddItemPopup = tk.Entry(inputFrameAddItemPopup, background="#d9d9d9", font=("Arial",sizeAddItemPopup), bd=0)
    nameEntryAddItemPopup.grid(row=3, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    damagedLabelAddItemPopup = tk.Label(inputFrameAddItemPopup, text="Beschädigung", background="white", font=("Arial",sizeAddItemPopup))
    damagedLabelAddItemPopup.grid(row=4, column=0, padx=0, pady=20, sticky=tk.E)

    damagedButtonAddItemPopup = tk.Entry(inputFrameAddItemPopup,background="#d9d9d9", font=("Arial",sizeAddItemPopup), bd=0)
    damagedButtonAddItemPopup.grid(row=4, column=1, padx=20, pady=20, sticky=tk.W + tk.E)

    # Funktion zum Eintrag hinzufügen
    def submitEntry():
        # add device
        # tag, typ,raum,name,damage
        tag = serviceTagEntryAddItemPopup if serviceTagEntryAddItemPopup else ""
        type = typeEntryAddItemPopup if typeEntryAddItemPopup else ""
        room = roomEntryAddItemPopup if roomEntryAddItemPopup else ""
        name = nameEntryAddItemPopup if nameEntryAddItemPopup else ""
        damage = damagedButtonAddItemPopup if damagedButtonAddItemPopup else ""
        db.create_hardware(tag,type,name,damage,None,room)
        from .mainPage import mainPage
        print("Eintrag hinzugefügt.")
        addPopup.destroy()

    def exitEntry():
        print("Vorgang abgebrochen")
        addPopup.destroy()

    parent.addBtnAddItemPopup = tk.PhotoImage(file="assets/ErstellenButton.png")
    parent.exitBtnAddItemPopup = tk.PhotoImage(file="assets/AbbrechenButton.png")

    # Buttons in ein separates Frame
    buttonFrameAddItemPopup = tk.Frame(addPopup, background="white")
    buttonFrameAddItemPopup.grid(row=2, column=0, pady=20)

    exitButtonAddItemPopup = tk.Button(buttonFrameAddItemPopup, image=parent.exitBtnAddItemPopup,
                                       bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=exitEntry)
    exitButtonAddItemPopup.pack(side=tk.LEFT, padx=10)  # Links platzieren

    submitButtonAddItemPopup = tk.Button(buttonFrameAddItemPopup, image=parent.addBtnAddItemPopup,
                                         bd=0, relief=tk.FLAT, bg="white", activebackground="white", command=submitEntry)
    submitButtonAddItemPopup.pack(side=tk.LEFT, padx=10)  # Neben Exit-Button platzieren

    addPopup.grid_rowconfigure(0, weight=0)
    addPopup.grid_rowconfigure(1, weight=1)
    addPopup.grid_rowconfigure(2, weight=0)
    addPopup.grid_rowconfigure(3, weight=1)
    addPopup.grid_columnconfigure(0, weight=1)
