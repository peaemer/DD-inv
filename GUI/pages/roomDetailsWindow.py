import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import Datenbank.sqlite3api as db
import Security.UserSecurity as sec
import cache
import random, string

LARGEFONT = ("Arial", 35)
LOGINFONT = ("Arial", 40)
srhGrey = "#d9d9d9"


def show_room_details(selected_room, tree, controller):
    # Daten aus der ausgewählten Zeile
    data = tree.item(selected_room, "values")
    print(f"Daten des ausgewählten Items: {data}")
    cache.selected_ID = data[0]

    # Frame aktualisieren und anzeigen
    details = controller.frames[roomDetailsWindow]
    details.update_data(data)  # Methode in detailsWindow aufrufen
    controller.show_frame(roomDetailsWindow)  # Zeige die Details-Seite


class roomDetailsWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="white")

        def go_back_details_window():
            from .adminRoomWindow import adminRoomWindow
            controller.show_frame(adminRoomWindow)

        def show_settings_window_details_window():
            print("Show settings window details window")
            from .settingsWindow import pop_up_settings
            pop_up_settings(self)

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
            text="Raum Details",
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
        container_frame.grid_columnconfigure(0, weight=1)

        size_details_window = 30

        # Input-Frame
        input_frame_details_window = tk.Frame(container_frame, background="white")
        input_frame_details_window.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

        input_frame_details_window.grid_columnconfigure(0, weight=1)  # Zentriere das Input-Frame
        input_frame_details_window.grid_columnconfigure(1, weight=1)

        # Raum
        room_num = tk.Label(input_frame_details_window, text="Raum",
                            font=("Arial", size_details_window), background="white")
        room_num.grid(column=0, row=0, sticky=tk.EW, padx=20, pady=10)

        self.room_num_entry = tk.Entry(input_frame_details_window, font=("Arial", size_details_window),
                                       background=srhGrey, relief=tk.SOLID)
        self.room_num_entry.grid(column=1, row=0, sticky=tk.EW, padx=20, pady=10)

        # Ort
        place_label_details_window = tk.Label(input_frame_details_window, text="Ort",
                                              font=("Arial", size_details_window), background="white")
        place_label_details_window.grid(column=0, row=2, sticky=tk.EW, padx=20, pady=10)

        self.place_entry = tk.Entry(input_frame_details_window, font=("Arial", size_details_window),
                                    background=srhGrey, relief=tk.SOLID)
        self.place_entry.grid(column=1, row=2, sticky=tk.EW, padx=20, pady=10)


        # Funktion zum Eintrag hinzufügen
        def refresh_entry():
            #update
            db.update_benutzer(self.name.get(), neues_email=self.email.get(), neue_rolle=self.role_combobox.get())
            from .adminUserWindow import adminUserWindow
            adminUserWindow.update_treeview_with_data()
            controller.show_frame(adminUserWindow)

        def delete_entry():
            db.delete_benutzer(self.name.get())
            from .adminUserWindow import adminUserWindow
            adminUserWindow.update_treeview_with_data()
            controller.show_frame(adminUserWindow)

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
        self.room_num_entry.delete(0, tk.END)
        self.room_num_entry.insert(0, data[0])

        self.place_entry.delete(0, tk.END)
        self.place_entry.insert(0, data[1])