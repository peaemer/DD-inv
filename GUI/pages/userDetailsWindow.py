import tkinter as tk
from tkinter import ttk
from tkinter import *
import Datenbank.sqlite3api as db
import cache

LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"


def show_user_details(selected_user, tree, controller):
    # Daten aus der ausgewählten Zeile
    data = tree.item(selected_user, "values")
    print(f"Daten des ausgewählten Items: {data}")
    cache.selected_ID = data[0]

    # Frame aktualisieren und anzeigen
    details = controller.frames[userDetailsWindow]
    details.update_data(data)  # Methode in detailsWindow aufrufen
    controller.show_frame(userDetailsWindow)  # Zeige die Details-Seite


class userDetailsWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="white")

        def go_back_details_window():
            from .mainPage import mainPage
            controller.show_frame(mainPage)

        def show_settings_window_details_window():
            print("Show settings window details window")
            from .settingsWindow import pop_up_settings
            pop_up_settings(self)


        def reset_pass():
            print("AAAAAAAA")

        self.go_back_btn_details_window = tk.PhotoImage(file="assets/ArrowLeft.png")
        self.opt_btn_details_window = tk.PhotoImage(file="assets/option.png")

        # Erstelle einen Header-Bereich
        header_frame_details_window = tk.Frame(self, height=10, background="#DF4807")
        header_frame_details_window.grid(row=0, column=0,columnspan=2, sticky=tk.W + tk.E + tk.N)

        # Überschrift mittig zentrieren
        header_frame_details_window.grid_columnconfigure(0, weight=1)  # Platz links
        header_frame_details_window.grid_columnconfigure(1, weight=3)  # Überschrift zentriert (größerer Gewichtungsfaktor)
        header_frame_details_window.grid_columnconfigure(2, weight=1)  # Option-Button


        # Zentriere das Label in Spalte 1
        header_label_details_window = tk.Label(
            header_frame_details_window,
            text="Nutzer Details",
            background="#DF4807",
            foreground="white",
            font=("Arial", 60)
        )
        header_label_details_window.grid(row=0, column=1, pady=40, sticky=tk.W + tk.E)

        # Buttons in Spalten 2 und 3 platzieren
        go_back_button_details_window = tk.Button(
            header_frame_details_window,
            image=self.go_back_btn_details_window,
            command=go_back_details_window,
            bd=0,
            relief=tk.FLAT,
            bg="#DF4807",
            activebackground="#DF4807"
        )
        go_back_button_details_window.grid(row=0, column=0, sticky=tk.W, padx=20)

        options_button_details_window = tk.Button(
            header_frame_details_window,
            image=self.opt_btn_details_window,
            command=show_settings_window_details_window,
            bd=0,
            relief=tk.FLAT,
            bg="#DF4807",
            activebackground="#DF4807"
        )
        options_button_details_window.grid(row=0, column=2, sticky=tk.E, padx=20)


        # Container für Input- und Tree-Frame
        container_frame = tk.Frame(self, background="white")
        container_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Konfiguration der Container-Spalten
        container_frame.grid_columnconfigure(0, weight=1)  # Baumansicht
        container_frame.grid_columnconfigure(1, weight=1)  # Eingabefelder



        size_details_window = 30



        # Ändere die Position des TreeFrames
        tree_frame_details_window = tk.Frame(container_frame, background="red", width=200, height=400)
        tree_frame_details_window.grid(row=0, column=0, padx=40, sticky="")

        tree_details_window = ttk.Treeview(tree_frame_details_window, column=("c1", "c2", "c3"), show="headings", height=30)

        scroll_details_window = tk.Scrollbar(
            tree_frame_details_window,
            orient="vertical",
            command=tree_details_window.yview,
            bg="black",
            activebackground="darkblue",
            troughcolor="grey",
            highlightcolor="black",
            width=15,
            borderwidth=1
        )
        scroll_details_window.grid(row=1, column=1, sticky="ns")
        tree_details_window.configure(yscrollcommand=scroll_details_window.set)

        # Tags für alternierende Zeilenfarben konfigurieren
        tree_details_window.tag_configure("oddrow", background="#f7f7f7")
        tree_details_window.tag_configure("evenrow", background="white")

        ### listbox for directories
        tree_details_window.column("# 1", anchor=CENTER, width=180)
        tree_details_window.heading("# 1", text="Name", )
        tree_details_window.column("# 2", anchor=CENTER, width=200)
        tree_details_window.heading("# 2", text="ServiceTag/ID")
        tree_details_window.column("# 3", anchor=CENTER, width=220)
        tree_details_window.heading("# 3", text="Ausgeliehen am")
        tree_details_window.grid(row=1, column=0)
        tree_details_window.tkraise()

        # Input-Frame
        input_frame_details_window = tk.Frame(container_frame, background="white")
        input_frame_details_window.grid(row=0, column=1, pady=20, sticky="nsew")

        input_frame_details_window.grid_columnconfigure(0, weight=1)  # Zentriere das Input-Frame
        input_frame_details_window.grid_columnconfigure(1, weight=1)

        #Nutzername
        name = tk.Label(input_frame_details_window, text="Nutzername",
                                                font=("Arial", size_details_window), background="white")
        name.grid(column=0, row=0, sticky=tk.W + tk.E, padx=20, pady=10)

        self.name = tk.Entry(input_frame_details_window, font=("Arial", size_details_window),
                             background=srhGrey, relief=tk.SOLID)
        self.name.grid(column=1, row=0, sticky=tk.W + tk.E, padx=20, pady=10)

        #Passwort
        password_label_details_window = tk.Label(input_frame_details_window, text="Passwort",
                                          font=("Arial", size_details_window), background="white")
        password_label_details_window.grid(column=0, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        self.reset_password = tk.Button(input_frame_details_window, font=("Arial", 24),text="Passwort zurücksetzen" ,command=reset_pass,
                                                  background=srhGrey, relief=tk.SOLID)
        self.reset_password.grid(column=1, row=1, sticky=tk.W + tk.E, padx=20, pady=10)

        #EMail
        email_label_details_window = tk.Label(input_frame_details_window, text="E-Mail",
                                          font=("Arial", size_details_window), background="white")
        email_label_details_window.grid(column=0, row=2, sticky=tk.W + tk.E, padx=20, pady=10)

        self.email = tk.Entry(input_frame_details_window, font=("Arial", size_details_window),
                              background=srhGrey, relief=tk.SOLID)
        self.email.grid(column=1, row=2, sticky=tk.W + tk.E, padx=20, pady=10)

        #Rolle
        role_label_details_window = tk.Label(input_frame_details_window, text="Rolle",
                                          font=("Arial", size_details_window), background="white")
        role_label_details_window.grid(column=0, row=3, sticky=tk.W + tk.E, padx=20, pady=10)

        role_values = []
        for room in db.read_all_rollen():
            role_values.append(room['Rolle'])
        self.room_combobox_add_item_popup = ttk.Combobox(input_frame_details_window, values=role_values,
                                                    font=("Arial", size_details_window))
        self.room_combobox_add_item_popup.grid(row=3, column=1, padx=20, pady=20, sticky=tk.W + tk.E)


        # Funktion zum Eintrag hinzufügen
        def refresh_entry():
            #update
            print("nix")

        def delete_entry():
            db.delete_hardware_by_id(cache.selected_ID)
            from .mainPage import mainPage
            mainPage.update_treeview_with_data()
            controller.show_frame(mainPage)

        def lend(data):
            print("Übergebene Daten:", data)
            from .lendPopup import lend_popup
            lend_popup(self, data)

        self.edit_btn = tk.PhotoImage(file="assets/Aktualisieren.png")
        self.lend_btn = tk.PhotoImage(file="assets/Ausleihen.png")
        self.delete_btn = tk.PhotoImage(file="assets/Loeschen.png")

        # Buttons in ein separates Frame
        button_frame_add_item_popup = tk.Frame(self, background="white")
        button_frame_add_item_popup.grid(row=2, column=0, pady=20)

        delete_button = tk.Button(button_frame_add_item_popup, image=self.delete_btn,
                                 bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                                 command= delete_entry)
        delete_button.pack(side=tk.LEFT, padx=20)  # Neben Exit-Button platzieren


        edit_button = tk.Button(button_frame_add_item_popup, image=self.edit_btn,
                               bd=0, relief=tk.FLAT, bg="white", activebackground="white",
                               command=refresh_entry)
        edit_button.pack(side=tk.LEFT, padx=20)  # Links platzieren

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(0, weight=1)

    def update_data(self, data):
        # Daten in die Entry-Felder einfügen
        self.name.delete(0, tk.END)
        self.name.insert(0, data[1])

        self.email.delete(0, tk.END)
        self.email.insert(0, data[3])

        self.room_combobox_add_item_popup.set(data[4])  # Platzhalter