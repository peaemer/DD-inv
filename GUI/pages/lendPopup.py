import tkinter as tk
from tkcalendar import Calendar, DateEntry

LARGEFONT = ("Arial", 20)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"



def lendPopup(parent, data):
    # Neues Fenster (Popup)
    popup = tk.Toplevel()
    popup.title("Ausleihen")
    popup.geometry("600x500")
    popup.transient(parent)
    popup.configure(background="white")
    popup.grab_set()  # Macht das Popup modal
    popup.attributes("-topmost", True)

    # Bildschirmbreite und -höhe ermitteln
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()

    # Fensterbreite und -höhe definieren
    window_width = 650
    window_height = 650

    # Berechne die Position, um das Fenster in der Mitte des Bildschirms zu platzieren
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    popup.resizable(False, False)

    # Icon setzen (optional)
    try:
        popup.iconbitmap("assets/srhIcon.ico")
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")

    # Funktion, um die Eingaben zu verarbeiten
    def confirmLend():
        item = nameEntry.get().strip()
        borrower = entry.get().strip()
        #lend_date = calEntry.get().strip()
        print(f"Item: {item}, Borrower: {borrower}, Date:")
        #lendupdate
        popup.destroy()  # Schließt das Popup nach Bestätigung


    # Grid-Layout konfigurieren
    popup.grid_rowconfigure(0, weight=0)  # Titelzeile
    popup.grid_rowconfigure(1, weight=0)  # Formularzeilen
    popup.grid_rowconfigure(2, weight=0)  # Formularzeilen
    popup.grid_rowconfigure(3, weight=0)  # Formularzeilen
    popup.grid_rowconfigure(4, weight=1)  # Buttonzeile
    popup.grid_columnconfigure(1, weight=1)  # Spalte 1 flexibel


    # Titelbereich
    titleLabel = tk.Label(
        popup, text="Ausleihen", font=("Arial", 35), bg="#DF4807", fg="white"
    )
    titleLabel.grid(row=0, column=0, columnspan=2, ipady=10, sticky="new")


    itemVar = tk.StringVar()
    itemVar.set("Itemplatzhalter") #funktion zum eifügen des Namens

    userVar = tk.StringVar()
    userVar.set("Affe") #funktion zum eifügen des Namens



    # Formularbereich

    nameLabel = tk.Label(popup, text="Name", font=LARGEFONT, bg="white", anchor="w")
    nameLabel.grid(row=1, column=0, padx=20, pady=10, sticky="w")

    nameEntry = tk.Entry(popup, font=LARGEFONT, bg=srhGrey, relief=tk.FLAT)
    nameEntry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

    borrowerlabel = tk.Label(popup, text="Ausleiher", font=LARGEFONT, bg="white", anchor="w")
    borrowerlabel.grid(row=2, column=0, padx=20, pady=10, sticky="w")

    entry = tk.Entry(popup, font=LARGEFONT, bg=srhGrey, relief=tk.FLAT, textvariable=userVar)
    entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

    label = tk.Label(popup, text="Ausleihdatum", font=LARGEFONT, bg="white", anchor="w")
    label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

    calEntry = DateEntry(popup, width= 16,locale="de_DE" , background="grey", foreground="white", bd=2)
    calEntry.grid(row=3, column=1, padx=20, pady=10, sticky="w")

    calEntry2 = DateEntry(popup, width=16,locale="de_DE" , background="grey", foreground="white", bd=2)
    calEntry2.grid(row=3, column=1, padx=20, pady=10, sticky="w")

    popup.grid_columnconfigure(1, weight=1)  # Spalte 1 flexibel

    userVar = tk.StringVar()
    userVar.set("Itemplatzhalter") #funktion zum eifügen des Namens

    nameEntry.insert(0, data["name"])

    # Buttonbereich
    buttonFrame = tk.Frame(popup, bg="white")
    buttonFrame.grid(row=4, column=0, columnspan=2, pady=20)

    confirmBtn = tk.Button(
        buttonFrame, text="Bestätigen", font=LARGEFONT, bg="#DF4807", fg="white",
        relief=tk.FLAT, command=confirmLend
    )
    confirmBtn.grid(row=0, column=0, padx=10)

    cancelBtn = tk.Button(
        buttonFrame, text="Abbrechen", font=LARGEFONT, bg=srhGrey, relief=tk.FLAT,
        command=popup.destroy
    )
    cancelBtn.grid(row=0, column=1, padx=10)
