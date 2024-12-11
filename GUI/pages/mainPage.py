import tkinter as tk
from tkinter import ttk
from tkinter import *
import Datenbank.sqlite3api as sqlapi
import cache
import customtkinter as ctk

# Importieren der extra Schriftart
from ._SRHFont import load_font, SRHHeadline


LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
load_font(SRHHeadline)
srhGrey = "#d9d9d9"


# Hauptseite (zweites Fenster)
class mainPage(tk.Frame):
    """
    The mainPage class provides the graphical user interface for the main
    application page, utilizing the Tkinter framework. It handles user interactions,
    layout management, and various functionalities such as searching, logging out,
    and navigating to different windows within the application. This class is
    responsible for rendering the main interface that users interact with after
    logging in, including headers, buttons, and data views.

    The class efficiently manages widgets like frames, buttons, and labels, and
    implements key functionalities that enhance user experience, such as placeholders
    in search entries, focus events, and grid layout configurations. It makes extensive
    use of Tkinter's components and styles to deliver an aesthetically organized
    interface. Additionally, this class interacts with different modules within the
    application to transition between various windows and maintain usability and
    navigation flow.

    :ivar header_frame: The header section that includes logos and option buttons.
    :type header_frame: tk.Frame
    :ivar greyFrame: A secondary frame used for additional layout and labels.
    :type greyFrame: tk.Frame
    :ivar headerLabel: A label for header display.
    :type headerLabel: tk.Label
    :ivar log_out_btn: Image for the logout button.
    :type log_out_btn: tk.PhotoImage
    :ivar opt_btn: Image for the settings button.
    :type opt_btn: tk.PhotoImage
    :ivar admin_btn: Image for the admin button.
    :type admin_btn: tk.PhotoImage
    :ivar search_btn: Image for the search button.
    :type search_btn: tk.PhotoImage
    :ivar add_btn: Image for the add item button.
    :type add_btn: tk.PhotoImage
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")

        def show_settings_window():
            from .settingsWindow import pop_up_settings
            pop_up_settings(self)

        def show_admin_window():
            from .adminUserWindow import adminUserWindow
            controller.show_frame(adminUserWindow)

        # Speichere die Funktion als Attribut, um später darauf zuzugreifen
        self.show_admin_window = show_admin_window

        def log_out():
            from .logInWindow import logInWindow
            cache.user_group = None  # Benutzergruppe zurücksetzen
            controller.show_frame(logInWindow)

        def search(event=None):                           # funktionalität hinzufügen
            search_entrys = []
            for entry in sqlapi.fetch_hardware():
                for value in entry:
                    if search_entry.get().lower() in str(entry[value]).lower():
                        if entry not in search_entrys:
                            search_entrys.append(entry)
            self.update_treeview_with_data(data=search_entrys)

        def add_item():
            from .addItemPopup import add_item_popup
            add_item_popup(self)

        def on_entry_click(event):
            if search_entry.get() == 'Suche':
                search_entry.delete(0, "end")  # Lösche den Platzhalter-Text
                search_entry.configure(text_color='black')  # Setze Textfarbe auf schwarz

        def on_key_press(event):
            typed_key = event.char  # The character of the typed key

        def on_focus_out(event):
            if search_entry.get() == '':
                search_entry.insert(0, 'Suche')  # Platzhalter zurücksetzen
                search_entry.configure(text_color='grey')  # Textfarbe auf grau ändern

        global tree

        # Konfiguriere das Grid-Layout für die Hauptseite
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Erstelle einen Header-Bereich
        self.header_frame = tk.Frame(self, background="#DF4807")
        self.header_frame.grid(row=0, column=0,columnspan=2, sticky=tk.W + tk.E)

        # Konfiguriere die Spalten für den Header
        self.header_frame.grid_columnconfigure(0, weight=1)  # Platz links
        self.header_frame.grid_columnconfigure(1, weight=2)  # Zentrale Spalte
        self.header_frame.grid_columnconfigure(2, weight=1)  # Platz rechts
        self.header_frame.grid_rowconfigure(0, weight=1)

        self.srh_head = tk.PhotoImage(file="assets/srh.png")

        # Füge ein zentriertes Label hinzu
        header_label = tk.Label(self.header_frame, image=self.srh_head, background="#DF4807", foreground="white")
        header_label.grid(row=0, column=0, padx=20, pady=20, sticky=tk.W)

        # Erstellen eines Schriftzuges im Header
        text_header_label = tk.Label(self.header_frame, background="#DF4807", text="Inventur-Übersicht", font=(SRHHeadline, 30), foreground="white")
        text_header_label.grid(row=0, column=1, padx=0, pady=50, sticky="")

        # Konvertiere das Bild für Tkinter
        self.log_out_btn = tk.PhotoImage(file="assets/ausloggen.png")

        # Füge einen Button mit dem Bild hinzu
        log_out_button = tk.Button(self.header_frame,
                                   image=self.log_out_btn,
                                   command=log_out,
                                   bd=0,
                                   relief=tk.FLAT,
                                   bg="#DF4807",
                                   activebackground="#DF4807")
        log_out_button.grid(row=0, column=4, sticky=tk.E, padx=20)



        # Konvertiere das Bild für Tkinter
        self.opt_btn = tk.PhotoImage(file="assets/option.png")

        # Füge einen Button mit dem Bild hinzu
        options_button = tk.Button(self.header_frame,
                                   image=self.opt_btn,
                                   command=show_settings_window,
                                   bd=0,
                                   relief=tk.FLAT,
                                   bg="#DF4807",
                                   activebackground="#DF4807")
        options_button.grid(row=0, column=3, sticky=tk.E, padx=20)

        # Platzieren des Adminbuttons
        self.admin_btn = tk.PhotoImage(file="assets/Key.png")

        # Erstellen des Grayframes für linke Seite
        grey_frame_side = tk.Frame(self, background=srhGrey)
        grey_frame_side.grid(row=1, column=0, sticky="nsw")

        tree_style_side_tree = ttk.Style()
        tree_style_side_tree.theme_use("default")
        tree_style_side_tree.configure("Treeview_side",
                                       background=srhGrey,
                                       font=("Arial", 20),
                                       rowheight=40,  # Zeilenhöhe für größere Abstände
                                       selectbackground="blue",  # Markierungshintergrund
                                       selectforeground="white")  # Markierungstextfarbe
        tree_style_side_tree.layout("Treeview_side", [('Treeview.treearea', {'sticky': 'nswe'})])

        # Treeview erstellen
        side_tree = ttk.Treeview(grey_frame_side, show="tree", style="Treeview_side")
        side_tree.grid(row=2, column=0, sticky=tk.W + tk.N + tk.S)

        side_tree.insert("", tk.END, text="Alle Räume")
        for room in sqlapi.fetch_all_rooms():
            cats = []
            tree_parent = side_tree.insert("", tk.END, text=room['Raum'])
            for hw in sqlapi.fetch_hardware():
                if hw['Raum'] and hw['Raum'].startswith(room['Raum']):
                    if not hw['Geraetetype'] in cats:
                        cats.append(hw['Geraetetype'])
                        side_tree.insert(tree_parent, tk.END, text=hw['Geraetetype'])
        side_tree.grid(row=3, column=0, sticky=tk.W + tk.N + tk.S)

        # Erstellen des MiddleFrame
        middle_frame = tk.Frame(self, bg="white")
        middle_frame.grid(row=1, padx=10, pady=10, column=1, sticky="nesw")

        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(1, weight=1)

        # Dbug Info Anzeige der Fenstergroesse
        def show_size(event):
            print(f"Neue Größe - Breite: {event.x} Höhe: {event.y}")
        print(show_size)

        # Verschiebe den SearchFrame nach oben, indem du seine Zeile anpasst
        search_frame = tk.Frame(middle_frame, bg="white")
        search_frame.grid(pady=5, padx=5, row=0, column=0, sticky=tk.W + tk.E + tk.N)

        search_frame.grid_columnconfigure(0, weight=0)
        search_frame.grid_columnconfigure(1, weight=1)
        search_frame.grid_columnconfigure(2, weight=0)

        # Btn Erstellen def mit Image und grid
        self.add_btn = tk.PhotoImage(file="assets/Erstellen.png")
        add_button = tk.Button(search_frame, image=self.add_btn, bd=0, relief=tk.FLAT, bg="white",
                               activebackground="white", command=add_item)
        add_button.grid(padx=10, pady=1, row=0, column=2, sticky="w")

        # Search Btn def und neben dem Entry platzieren
        self.search_btn = tk.PhotoImage(file="assets/SearchButton.png")
        search_button = tk.Button(search_frame,
                                  image=self.search_btn,
                                  bd=0,
                                  relief=tk.FLAT,
                                  bg="white",
                                  activebackground="white",
                                  command=search)
        search_button.grid(padx=5, pady=5, row=0, column=0)

        # Entry-Feld mit Platzhalter-Text
        search_entry = ctk.CTkEntry(search_frame, fg_color=srhGrey,text_color="black", font=("Arial", 27), corner_radius=20, border_width=0)
        search_entry.insert(0, 'Suche')  # Setze den Platzhalter-Text

        # Events für Klick und Fokusverlust hinzufügen
        search_entry.bind('<FocusIn>', on_entry_click)
        search_entry.bind('<FocusOut>', on_focus_out)
        search_entry.bind('<Return>', search)
        search_entry.bind("<Key>", on_key_press)
        search_entry.grid(column=1, row=0, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)




        # style der Tabelle
        tree_style = ttk.Style()
        tree_style.theme_use("default") #alt, classic,xpnative,winnative, default
        tree_style.configure("Treeview.Heading",rowheight=50, font=("Arial", 20))
        tree_style.configure("Treeview", rowheight=40, font=("Arial", 14))

        # Frame für die Tabelle und Scrollbar
        tree_frame = tk.Frame(middle_frame, background="white")
        tree_frame.grid(row=1, column=0, padx=0, pady=0, sticky=tk.N + tk.S + tk.E + tk.W)

        # Spaltenkonfiguration für das TreeFrame
        tree_frame.grid_rowconfigure(1, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)  # Spalte für die Tabelle
        tree_frame.grid_columnconfigure(1, weight=0)  # Spalte für die Scrollbar (fixiert)

        # Treeview erstellen
        tree = ttk.Treeview(tree_frame, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show="headings")

        # Scrollbar erstellen
        scroll = ctk.CTkScrollbar(
            tree_frame,
            orientation="vertical",
            command=tree.yview,
            fg_color="white",
            width=20,
            corner_radius=10,
            button_color = srhGrey,
            button_hover_color="#2980b9"
        )
        scroll.grid(row=1, column=1, sticky=tk.N + tk.S)  # Scrollbar genau neben der Tabelle

        # Treeview mit Scrollbar verbinden
        tree.configure(yscrollcommand=scroll.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        tree.tag_configure("oddrow", background="#f7f7f7")
        tree.tag_configure("evenrow", background="white")

        # listbox for directories
        tree.column("# 1", anchor=CENTER, width=60)
        tree.heading("# 1", text="ID")
        tree.column("# 2", anchor=CENTER, width=175)
        tree.heading("# 2", text="Service Tag")
        tree.column("# 3", anchor=CENTER, width=230)
        tree.heading("# 3", text="Typ")
        tree.column("# 4", anchor=CENTER, width=120)
        tree.heading("# 4", text="Raum")
        tree.column("# 5", anchor=CENTER, width=250)
        tree.heading("# 5", text="Name")
        tree.column("# 6", anchor=CENTER, width=300)
        tree.heading("# 6", text="Beschädigung")
        tree.column("# 7", anchor=CENTER, width=250)
        tree.heading("# 7", text="Ausgeliehen von")
        tree.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)  # Tabelle vollständig anpassen
        tree.tkraise()

        # Funktion zum eintragen von Daten in die Tabelle
        def insert_data(self):
            i = 0
            for entry in sqlapi.fetch_hardware():
                # Bestimme das Tag für die aktuelle Zeile
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                if entry['Beschaedigung'] == "None":
                    damage = ""
                else:
                    damage = entry['Beschaedigung']
                # Daten mit dem Tag in das Treeview einfügen
                tree.insert(
                    "",
                    "end",
                    text=f"{entry['Service_Tag']}",
                    values=(
                        i,
                        entry['Service_Tag'],
                        entry['Geraetetype'],
                        entry['Raum'],
                        entry['Modell'],
                        damage,
                        entry['Ausgeliehen_von']
                    ),
                    tags=(tag,)
                )
                i += 1
        insert_data(self)

        # Funktion für das Ereignis-Binding
        def on_item_selected(event):
            try:
                selected_item = tree.focus()
                if selected_item:
                    from .detailsWindow import detailsWindow, show_details
                    show_details(selected_item, tree, controller)
            except Exception as e:
                print(f"Fehler bei der Auswahl: {e}")

        def on_side_tree_select(event):
            # Hole ausgewähltes Element aus dem side_tree
            selected_item = side_tree.selection()
            if selected_item:
                selected_text = side_tree.item(selected_item, 'text')
                print(selected_text)
                if selected_text == "Alle Räume":
                    # Alle Daten in der Haupttabelle anzeigen
                    self.update_treeview_with_data()
                elif selected_text in [room['Raum'] for room in sqlapi.fetch_all_rooms()]:
                    # Daten nach Raum filtern
                    filtered_data = []
                    for hw in sqlapi.fetch_hardware():
                        if hw.get("Raum") and hw.get("Raum").startswith(selected_text):
                            filtered_data.append(hw)
                    self.update_treeview_with_data(data=filtered_data)
                else:
                    parent_name = side_tree.item(side_tree.parent(side_tree.selection()[0]),'text') if side_tree.selection() else None
                    filtered_data = []
                    for hw in sqlapi.fetch_hardware():
                        if hw.get("Raum") and hw.get("Raum").startswith(parent_name) and hw.get("Geraetetype") and hw.get("Geraetetype").startswith(selected_text):
                            filtered_data.append(hw)
                    self.update_treeview_with_data(data=filtered_data)

        side_tree.bind("<<TreeviewSelect>>", on_side_tree_select)

        # Binde die Ereignisfunktion an die Treeview
        tree.bind("<Double-1>", on_item_selected)

    # Aktualisieren der Data in der Tabelle
    def update_treeview_with_data(self = None, data=None):
        # Clear the current treeview contents
        global i
        i = 0
        tree.delete(*tree.get_children())

        # If no data is provided, fetch the data from sqlapi
        if data is None:
            data = sqlapi.fetch_hardware()

        for entry in data:
            i+=1
            if entry['Beschaedigung'] == "None":
                damage = ""
            else:
                damage = entry['Beschaedigung']
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert(
                "",
                "end",
                values=(entry['ID'], entry['Service_Tag'], entry['Geraetetype'], entry['Raum'],
                        entry['Modell'], damage, entry['Ausgeliehen_von']),
                tags=(tag,)
            )

    def on_load(self):
        """Diese Methode wird aufgerufen, nachdem die Seite vollständig geladen ist."""

        # Überprüfe die Benutzergruppe
        if cache.user_group == "Admin":

            # Überprüfe, ob der Admin-Button bereits existiert
            if not hasattr(self, "adminButton"):
                # Erstelle den Admin-Button, wenn er noch nicht existiert
                self.admin_button = tk.Button(
                    self.header_frame,
                    image=self.admin_btn,
                    command=self.show_admin_window,  # Funktion für Admin-Button
                    bd=0,
                    relief=tk.FLAT,
                    bg="#DF4807",
                    activebackground="#DF4807"
                )
                self.admin_button.grid(row=0, column=2, sticky=tk.E, padx=20)
            else:
                self.admin_button.grid(row=0, column=2, sticky=tk.E, padx=20)
        else:
            # Entferne den Admin-Button, falls er existiert
            if hasattr(self, "adminButton"):
                self.admin_button.grid_remove()

        self.update_treeview_with_data()