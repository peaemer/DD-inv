import tkinter as tk
from tkinter import filedialog
import customtkinter  # Library kann mit "pip install customtkinter" geladen werden
import customtkinter as ttk

LARGEFONT = ("Arial", 30)
SETTINGSFONT = ("Arial", 30)
srhGrey = "#d9d9d9"

#class SettingsWindow(ttk.CTkFrame):
#    def __init__(parent, parent, controller):
#        tk.Frame.__init__(parent, parent)
#        parent.configure(background="white")

        # Hintergrund-Label
#        parent.bg_label = tk.Label(parent)
#        parent.bg_label.place(relwidth=1, relheight=1)

        # Button zum Bildauswählen
#        parent.select_button = tk.Button(parent, text="Wähle ein besseres Bild aus, als diesen Hintergrund zu verwenden...",
#                                       command=parent.choseAPicture)
#        parent.select_button.pack(pady=20)



def popUpSettings(parent):
    popup = tk.Toplevel(parent)
    popup.title("Einstellungen")
    popup.geometry("800x600")
    popup.transient(parent)  # Popup bleibt im Vordergrund des Hauptfensters
    popup.grab_set()  # Blockiere Interaktionen mit dem Hauptfenster
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

    # Konfiguriere das Grid-Layout für die Hauptseite
    popup.grid_rowconfigure(0, weight=0)
    popup.grid_rowconfigure(1, weight=1)
    popup.grid_rowconfigure(2, weight=0)
    popup.grid_rowconfigure(3, weight=0)
    popup.grid_columnconfigure(0, weight=1)

    # Erstelle einen Header-Bereich
    headerFrame = tk.Frame(popup, height=10, background="#DF4807")
    headerFrame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N)

    # Konfiguriere die Spalten für den Header
    headerFrame.grid_columnconfigure(0, weight=1)
    headerFrame.grid_rowconfigure(0, weight=1)

    parent.srhHead2 = tk.PhotoImage(file="assets/srh.png")

    # Füge ein zentriertes Label hinzu
    headerLabel = tk.Label(headerFrame, image=parent.srhHead2, background="#DF4807", foreground="white")
    headerLabel.grid(row=0, column=0, padx=20, pady=20, sticky=tk.N + tk.W)

    def btnDarkmode(parent):
        # Button Darkmode erstellen
        btn_switch = tk.StringVar(value="on")

        def change_theme():
            pass  # Darkmode-Logik hier hinzufügen

        # Erstellen und definieren des Switches
        darkmode_switch = customtkinter.CTkSwitch(text="Light-/Darkmode",
                                                  command=change_theme,
                                                  variable=btn_switch,
                                                  onvalue="on",
                                                  offvalue="off")
        darkmode_switch.pack()

    def set_background(parent, file_path):
        # Bild laden und skalieren
        image = Image.open(file_path)
        resize_image = image.resize((parent.winfo_width(), parent.winfo_height()), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(resize_image)
        parent.bg_label.config(image=bg_image)
        parent.bg_label.image = bg_image

    def choseAPicture(parent):
        # Datei-Dialog öffnen
        file_path = filedialog.askopenfilename(title="Wähle ein Bild aus...",
                                               filetypes=[("Bilddateien", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp")])
        if file_path:
            parent.set_background(file_path)
        else:
            print("Error: Could´t load or get image")
