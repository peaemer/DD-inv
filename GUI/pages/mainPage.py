import json
import tkinter as tk
from tkinter import ttk
from tkinter import *
from CTkListbox import *
import customtkinter as ctk
from  GUI.SearchBar import SearchBar
import Datenbank.sqlite3api as sqlapi
import GUI.SearchBar.SearchBar as sb
import cache

# Importieren der extra Schriftart
from ._SRHFont import load_font, SRHHeadline


LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
load_font(SRHHeadline)
srhGrey = "#d9d9d9"


# Hauptseite (zweites Fenster)
class mainPage(tk.Frame):
    """
    Die Klasse mainPage repräsentiert die Benutzeroberfläche der Hauptseite der Anwendung.

    Die Hauptseite dient als zentrale Übersicht für die Inventur. Sie enthält mehrere
    wichtige Funktionen wie die Möglichkeit, nach Elementen zu suchen, neue Elemente hinzuzufügen,
    sich auszuloggen, und verschiedene Optionen und Einstellungen anzuzeigen. Die Benutzeroberfläche
    besteht aus mehreren geordneten Abschnitten wie dem Header, einer Seitenleiste und einem
    mittleren Bereich zur Anzeige der Inhalte. Dabei wird ein Grid-Layout verwendet, um die Widgets
    entsprechend ihrer Funktionalität und Position anzuordnen.

    :ivar header_frame: Frame-Widget, das den Header-Bereich der Hauptseite darstellt.
    :type header_frame: tk.Frame
    :ivar srh_head: Bildobjekt, das zur Anzeige eines Logos im Header verwendet wird.
    :type srh_head: tk.PhotoImage
    :ivar log_out_btn: Bildobjekt für den Log-Out-Button.
    :type log_out_btn: tk.PhotoImage
    :ivar opt_btn: Bildobjekt für den Button, um die Einstellungen zu öffnen.
    :type opt_btn: tk.PhotoImage
    :ivar admin_btn: Bildobjekt für den Button, um den Admin-Bereich zu öffnen.
    :type admin_btn: tk.PhotoImage
    :ivar add_btn: Bildobjekt für den Button, um ein neues Element hinzuzufügen.
    :type add_btn: tk.PhotoImage
    :ivar search_btn: Bildobjekt für den Such-Button.
    :type search_btn: tk.PhotoImage
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="white")

        def show_settings_window():
            """
            Repräsentiert die Hauptseite der Anwendung, die als Frame innerhalb einer
            tkinter-Anwendung konzipiert ist. Diese Klasse dient als Hauptcontainer für
            Inhalte und verwaltet die Navigation zu anderen Fenstern oder Frames.

            :cvar parent: Der übergeordnete tkinter-Widget, in dem die Hauptseite angezeigt wird.
            :cvar controller: Der Controller, der die Navigation zwischen den Seiten steuert.
            """
            from .settingsWindow import pop_up_settings
            pop_up_settings(self, controller)

        def show_admin_window():
            """
            Diese Klasse repräsentiert die Hauptrahmenseite der Anwendung und erbt von
            `tk.Frame`. Sie dient als Grundlage für die GUI-Komponente und ermöglicht
            die Navigation zwischen verschiedenen Seiten oder Fenstern durch den
            Controller.

            Der Hauptfokus dieser Klasse ist die Integration der Administrations-
            Fensteransicht durch die Methode `show_admin_window`.
            """
            from .adminUserWindow import adminUserWindow
            controller.show_frame(adminUserWindow)

        # Speichere die Funktion als Attribut, um später darauf zuzugreifen
        self.show_admin_window = show_admin_window

        def log_out():
            """
            Eine Klasse, die das Hauptseiten-Frame darstellt und verwendet wird, um
            den Benutzer zwischen verschiedenen Ansichten zu navigieren. Diese Klasse
            enthält die Hauptlogik für den Vorgang beim Ausloggen.

            :ivar parent: Die Elternkomponente, auf der dieses Frame basiert.
            :ivar controller: Der Controller, der die Navigation zwischen verschiedenen Frames verwaltet.
            """
            from .logInWindow import logInWindow
            cache.user_group = None  # Benutzergruppe zurücksetzen
            controller.show_frame(logInWindow)

        def search(event=None):                           # funktionalität hinzufügen
            """
            Eine Klasse, die ein Hauptseiten-Frame darstellt, das in einer
            Tkinter-GUI verwendet wird. Diese Klasse dient als Basis für
            die Anzeige von Inhalten und Interaktionen der Anwendung.

            :param parent: Das übergeordnete Widget, in das dieses Frame
                           integriert wird.
            :param controller: Der Hauptcontroller für die Steuerung der
                               Ansicht in der Anwendung.
            """
            search_entrys = []
            for entry in sqlapi.fetch_hardware():
                for value in entry:
                    if search_entry.get().lower() in str(entry[value]).lower():
                        if entry not in search_entrys:
                            search_entrys.append(entry)
            self.update_treeview_with_data(data=search_entrys)
            sb.finish_search(cache.loaded_history,search_entry,dropdown,search_entry_var.get(),cache.user_name)

        def add_item():
            """
            Eine Klasse, die die Hauptseite einer Anwendung darstellt und eine entsprechende grafische Benutzeroberfläche
            bereitstellt. Die Klasse erbt von `tk.Frame` und wird innerhalb eines tkinter-Anwendungsrahmens verwendet.

            Die Klasse enthält eine Methode zur Initialisierung des Layouts und eine Hilfsmethode, um ein Popup-Fenster
            zum Hinzufügen eines Eintrags anzuzeigen.

            Attributes:
                parent: Das übergeordnete tkinter-Widget, innerhalb dessen der Rahmen liegt.
                controller: Eine Controller-Instanz, die die Navigation oder Steuerung zwischen
                            verschiedenen Anwendungsseiten ermöglicht.

            Methoden:
                add_item:
                    Ruft eine Funktion auf, um ein Dialog-Popup für das Hinzufügen eines Eintrags
                    zu erstellen.

            :param parent: Das Eltern-Widget für den tkinter-Rahmen.
            :type parent: tk.Widget
            :param controller: Der Controller für die Navigation und Steuerung.
            :type controller: object
            """
            from .addItemPopup import add_item_popup
            add_item_popup(self)

        def on_entry_click():
            """
            Eine Klasse, die die Hauptseite in einer Tkinter-basierten GUI-Anwendung repräsentiert. Sie erbt von
            `tk.Frame` und implementiert Interaktionen wie das Entfernen eines Platzhalters in einem
            Suchfeld, wenn dieses fokussiert wird.

            :param parent: Das übergeordnete Widget, das als Container für dieses Frame dient.
            :type parent: tk.Widget
            :param controller: Der Controller, der die Navigation zwischen verschiedenen Seiten innerhalb der Anwendung verwaltet.
            :type controller: Any

            :method on_entry_click(event): Ereignis-Handler für das Klicken in das Suchfeld. Entfernt den Platzhaltertext und
                                           setzt die Textfarbe auf schwarz, wenn der Platzhaltertext vorhanden ist.
            :param event: Ein Tkinter-Ereignisobjekt, das das durch den Benutzer ausgelöste Ereignis beschreibt.
            :type event: tk.Event

            """
            print("""[MainPage]:on_entry_click""")
            if search_entry.get() == 'Suche':
                search_entry.delete(0, "end")  # Lösche den Platzhalter-Text
                search_entry.config(fg='black')  # Setze Textfarbe auf schwarz
            sb.start_search(cache.loaded_history,search_entry,dropdown,search_entry_var.get(),cache.user_name)

        def on_key_press(var1:str, var2:str, var3:str):
            """
            Eine Klasse, die ein Frame-Objekt für die Hauptseite einer Tkinter-Anwendung darstellt.

            Zusammenfassung:
            Diese Klasse bietet eine grundlegende Struktur für die Hauptseite innerhalb
            einer grafischen Benutzeroberfläche, die mit Tkinter erstellt wird. Ein
            zentrales Ereignis-Handling für Tastatureingaben (z.B. on_key_press-Methode)
            wird implementiert, um Benutzereingaben zu verarbeiten.

            :parameter parent: Das übergeordnete Tkinter-Widget, dem dieses Frame hinzugefügt wird.
            :parameter controller: Ein Controller-Objekt, das zur Steuerung der Anwendungslogik verwendet wird.
            """
            print(f"""[MainPage]: executing on_key_press with searchbar text "{search_entry_var.get()}" """)
            #typed_key = event.char  # The character of the typed key
            print(search_entry_var.get())

        def on_focus_out():
            """
            Die Klasse `mainPage` stellt eine Benutzeroberfläche dar, die von der
            Tkinter Frame-Klasse abgeleitet ist. Sie dient als Hauptseite einer GUI-Anwendung
            und ermöglicht verschiedene Interaktionen.

            Es wird ein Fokus-Event überwacht und bei einem Fokusverlust eine Überprüfung
            des Suchfeldes durchgeführt, um gegebenenfalls Platzhaltertext und die passende
            Textfarbe zu setzen.

            :param parent: Das übergeordnete Tkinter-Widget, das den Rahmen enthält.
            :type parent: tk.Widget
            :param controller: Ein Kontrollobjekt für die Verwaltung der Navigation und
                anderer Interaktionen zwischen Subkomponenten der GUI.
            :type controller: Objekt
            """

            if search_entry_var.get() == '':
                search_entry.insert(0, 'Suche')  # Platzhalter zurücksetzen
                search_entry.config(fg='grey')  # Textfarbe auf grau ändern


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
            """
            Diese Klasse mainPage stellt ein GUI-Frame dar, das in einer tkinter-Anwendung
            verwendet wird. Es dient als Rahmen für Widgets und enthält Methoden, um auf
            Ereignisse zu reagieren, wie zum Beispiel Änderungen der Fenstergröße.

            :param parent: Der übergeordnete Widget-Container, zu dem dieses Frame gehört.
            :type parent: tk.Widget
            :param controller: Ein Objekt, das als Controller für Navigation oder
                               Steuerungslogik dient.
            :type controller: Objekt

            :method show_size: Eine Methode zur Handhabung von Ereignissen, bei denen die
                               Größe des Fensters geändert wird. Sie gibt die neuen
                               Breiten- und Höhenwerte des Ereignisses aus.
            :param event: Das Ereignisobjekt, das von tkinter übergeben wird und
                          Informationen über das Größenänderungsereignis enthält.
            :type event: tk.Event
            """
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

        dropdown_var: tk.StringVar = tk.StringVar()
        dropdown: CTkListbox = CTkListbox(search_frame, font=("Arial", 20), bg_color="white", border_color=srhGrey, corner_radius=10)
        #dropdown.grid(column=1, row=1, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)

        search_entry_var: tk.StringVar = tk.StringVar()
        search_entry = tk.Entry(search_frame, font=("Arial", 20), bg=srhGrey, bd=0, fg='grey', textvariable=search_entry_var)
        search_entry.grid(column=1, row=0, columnspan=1, sticky=tk.W + tk.E, padx=5, pady=5)

        # Entry-Feld mit Platzhalter-Text
        search_entry = ctk.CTkEntry(search_frame, fg_color=srhGrey,text_color="black", font=("Arial", 27), corner_radius=20, border_width=0,textvariable=search_entry_var)
        cache.loaded_history = json.loads(sqlapi.read_benutzer_suchverlauf(cache.user_name) if sqlapi.read_benutzer(cache.user_name) else """[{}]""")
        print(str(search_entry._textvariable)+" test")
        search_entry.insert(0, 'Suche')  # Setze den Platzhalter-Text

        # Events für Klick und Fokusverlust hinzufügen
        search_entry.bind('<FocusIn>', lambda _: on_entry_click())
        search_entry.bind('<FocusOut>', lambda _: on_focus_out())
        search_entry.bind('<Return>', search)
        search_entry.bind("<Key>", on_key_press)
        search_entry.bind("<Button-1>", search)
        search_entry_var.trace_add("write", on_key_press)
        dropdown.bind("<<ListboxSelect>>", lambda  _: sb.on_dropdown_select(search_entry, dropdown))


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
            """
            Eine Klasse, die eine Hauptseite mit GUI-Elementen repräsentiert. Diese Klasse erbt von
            `tk.Frame` und wird typischerweise in einer tkinter-Anwendung verwendet.

            :Attributes:
                parent (tk.Widget): Der übergeordnete Widget, in dem der Rahmen eingebettet wird.
                controller (tk.Tk oder Subklasse): Der Hauptcontroller der tkinter-Anwendung,
                    der für die Navigation und das Management der Frames verantwortlich ist.
            """
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
            """
            Hauptseite eines GUI-Frameworks basierend auf tkinter.

            Diese Klasse stellt die Hauptseite dar, die eine Benutzeroberfläche für die
            Navigation und Anzeige spezifischer Detailinformationen bereitstellt.
            """
            try:
                selected_item = tree.focus()
                if selected_item:
                    from .detailsWindow import detailsWindow, show_details
                    show_details(selected_item, tree, controller)
            except Exception as e:
                print(f"Fehler bei der Auswahl: {e}")

        def on_side_tree_select(event):
            """
            Hauptseite für die Anwendung. Diese Klasse erstellt die Hauptansicht für das
            Programm und erlaubt Benutzern, durch die Auswahl eines Elements aus dem
            Baum (side_tree) entsprechende Daten in der Hauptansicht (treeview) anzuzeigen.

            :Attributes:
                parent: Die Elterninstanz oder der übergeordnete Container, in dem diese
                    Seite eingebettet ist.
                controller: Der zentrale Steuerungsmechanismus, der zwischen den
                    verschiedenen Seiten der Anwendung vermittelt.

            :Methode:
                on_side_tree_select(event):
                    Wird ausgelöst, wenn ein Element im side_tree ausgewählt wird. Diese
                    Methodik ermöglicht:
                    - Das Anzeigen aller Daten, wenn "Alle Räume" ausgewählt wird.
                    - Das Filtern und Anzeigen von Daten basierend auf dem Raum.
                    - Weitere spezifische Filterlogiken, wenn das übergeordnete über den
                      Elternknoten bestimmt wird.

            :Rückgabewerte:
                Keine der Methoden in dieser Klasse gibt Werte zurück.

            :Parameter:
                :param event: Das Ereignisobjekt, das durch die Auswahl eines Elements
                    ausgelöst wird.

            :Erhobene Ausnahmen:
                Keine direkte Fehlerbehandlung wird in der aktuellen Funktionslogik
                implementiert.

            Einschränkungen:
            Die Funktionalität setzt voraus, dass die Methode fetch_all_rooms() und
            fetch_hardware() im Modul 'sqlapi' korrekt implementiert sind und die
            erforderlichen Daten liefern.
            """
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
        """
        Aktualisiert die Treeview mit den bereitgestellten Daten oder den aus der SQL-API
        abgerufenen Hardwaredaten. Vorhandene Einträge in der Treeview werden geleert und
        ersetzt. Zeilen erhalten je nach ihrer Reihenfolge unterschiedliche Tags
        für alternative Farbmarkierungen.

        :param data: Die zu aktualisierenden Daten, standardmäßig None. Wenn keine Daten
            bereitgestellt werden, werden diese aus der SQL-API abgerufen.
        :type data: Optional[List[Dict[str, Any]]]
        :return: Es wird nichts zurückgegeben.
        """
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
        """
        Überprüft beim Laden die Benutzergruppe des aktuellen Nutzers und entscheidet, ob
        ein Admin-Button erstellt, angezeigt oder entfernt werden soll. Der Admin-Button wird
        nur für Nutzer der Gruppe "Admin" sichtbar und ermöglicht den Zugriff auf zusätzliche
        Administrationsfunktionen. Danach wird die Anzeige des Treeviews aktualisiert.

        :param self: Das aktuelle Objekt, das Zugriff auf die Eigenschaften und Methoden
            der Klasse hat.

        Attribute
        ---------
        admin_button : tk.Button
            Eine Referenz auf den Admin-Button, falls dieser erstellt wurde.

        admin_btn : Bild
            Das Bild, das im Admin-Button angezeigt wird.

        header_frame : Frame
            Der Frame, in dem der Admin-Button positioniert wird.

        user_group : str
            Die Benutzergruppe des aktuellen Nutzers, die aus dem `cache` geladen wird.

        Returns
        -------
        None
            Diese Methode gibt keinen Wert zurück.
        """

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