import tkinter as tk
from tkinter import messagebox

from main import ddINV
from includes.sec_data_info import sqlite3api as sqlapi
from .customMessageBoxDelete import *
from ._styles import *

logger:Logger = Logger('RolesDetailsWindow')


def show_roles_details(selected_roles, tree, controller):
    """
    Zeigt die Details des ausgewählten Raums an. Die Methode liest die Daten aus
    der ausgewählten Zeile eines Treeviews, speichert die ID des Raums in einem
    Cache und aktualisiert die Daten des Detailframes. Anschließend wird der Frame
    zum Anzeigen der Details angezeigt.

    :param str selected_roles: Das ausgewählte Raumelement im Treeview.
    :param tree: Der Treeview, aus dem die Daten abgerufen werden.
    :param controller: Der Controller, der das Frame-Management übernimmt.
    :return: Es wird kein Wert zurückgegeben.
    """
    # Daten aus der ausgewählten Zeile
    data = tree.item(selected_roles, "values")
    logger.debug(f"Data of the selected item: {data}") # Debug
    cache.selected_ID = data[0]
    controller.show_frame(RolesDetailsWindow)  # Zeige die Details-Seite

    # Frame aktualisieren und anzeigen
    details = controller.frames[RolesDetailsWindow]
    details.update_data(data)  # Methode in DetailsWindow aufrufen


class RolesDetailsWindow(tk.Frame):
    """
    Die Klasse RoomDetailsWindow dient zur Darstellung und Bearbeitung von Raumdetails in einer GUI.

    Die Klasse ist eine Unterklasse von ``tk.Frame`` und wird zur Anzeige und Bearbeitung von Raumdaten
    in einer GUI verwendet. Sie bietet Interaktionen zum Zurückkehren zu einer Admin-Seite, zum Anzeigen
    eines Einstellungs-Popups sowie zum Aktualisieren oder Löschen von Raumeinträgen.

    :ivar controller: Der Controller, der für die Steuerung der GUI-Seiten zuständig ist.
    :type controller: tk.Tk
    :ivar go_back_btn_roles_window: Bild für den „Zurück“-Button.
    :type go_back_btn_roles_window: tk.PhotoImage
    :ivar edit_btn: Bild für den „Aktualisieren“-Button.
    :type edit_btn: tk.PhotoImage
    :ivar lend_btn: Bild für den „Ausleihen“-Button.
    :type lend_btn: tk. PhotoImage
    :ivar delete_btn: Bild für den „Löschen“-Button.
    :type delete_btn: tk.PhotoImage
    """
    def __init__(self, parent, controller: ddINV):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="white")

        def go_back_roles_window():
            from .AdminRoleWindow import AdminRoleWindow
            controller.show_frame(AdminRoleWindow)

        from ._avatarManager import resource_path
        self.go_back_btn_roles_window = tk.PhotoImage(file=resource_path("./includes/assets/ArrowLeft.png"))

        # Erstelle einen Header-Bereich
        header_frame_roles_window = tk.Frame(self,
            height=10,
            background="#00699a"
        )
        header_frame_roles_window.grid(row=0, column=0,columnspan=2, sticky=tk.W + tk.E + tk.N)

        # Überschrift mittig zentrieren
        header_frame_roles_window.grid_columnconfigure(0, weight=1)  # Platz links
        header_frame_roles_window.grid_columnconfigure(1, weight=3)  # Überschrift zentriert (größerer Gewichtungsfaktor)
        header_frame_roles_window.grid_columnconfigure(2, weight=1)  # Option-Button

        # Zentriere das Label in Spalte 1
        header_label_roles_window = tk.Label(header_frame_roles_window,
            text="Rollen Details",
            background="#00699a",
            foreground="white",
            font=("Arial", 60)
        )
        header_label_roles_window.grid(row=0, column=1, pady=40, sticky=tk.W + tk.E)

        # Buttons in Spalten 2 und 3 platzieren
        go_back_button_roles_window = tk.Button(header_frame_roles_window,
            image=self.go_back_btn_roles_window,
            command=go_back_roles_window,
            bd=0,
            relief=tk.FLAT,
            bg="#00699a",
            activebackground="#00699a"
        )
        go_back_button_roles_window.grid(row=0, column=0, sticky=tk.W, padx=20)

        # Container für Input- und Tree-Frame
        container_frame = tk.Frame(self, background="white")
        container_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Konfiguration der Container-Spalten
        container_frame.grid_columnconfigure(0, weight=1)

        # Input-Frame
        input_frame_roles_window = tk.Frame(container_frame, background="white")
        input_frame_roles_window.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

        input_frame_roles_window.grid_columnconfigure(0, weight=1)  # Zentriere das Input-Frame
        input_frame_roles_window.grid_columnconfigure(1, weight=1)
        input_frame_roles_window.grid_columnconfigure(2, weight=1)
        input_frame_roles_window.grid_columnconfigure(3, weight=1)
        input_frame_roles_window.grid_columnconfigure(4, weight=1)
        input_frame_roles_window.grid_columnconfigure(5, weight=1)
        input_frame_roles_window.grid_columnconfigure(6, weight=1)
        input_frame_roles_window.grid_columnconfigure(7, weight=1)
        input_frame_roles_window.grid_columnconfigure(8, weight=1)

        # Rollen Name
        self.role_name = tk.Label(input_frame_roles_window,
            text="",
            font=("Arial", 24),
            background="white"
        )
        self.role_name.grid(column=0, columnspan=9, row=0, sticky=tk.W + tk.E, pady=5)

        # Ansehen
        view_label_roles_window = tk.Label(input_frame_roles_window,
            text="Ansehen",
            font=("Arial", size_roles_window),
            background="white"
        )
        view_label_roles_window.grid(column=3, row=1, sticky=tk.W + tk.E, pady=5)

        self.view = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.view.grid(column=4, row=1, sticky=tk.W + tk.E, pady=5)

        # Rolle Loeschbar
        delete_rl_label_roles_window = tk.Label(input_frame_roles_window,
            text="Rolle Löschbar",
            font=("Arial", size_roles_window),
            background="white"
        )
        delete_rl_label_roles_window.grid(column=3, row=2, sticky=tk.W + tk.E, pady=5)

        self.delete_rl = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.delete_rl.grid(column=4, row=2, sticky=tk.W + tk.E, pady=5)

        # Admin Feature
        feature_label_roles_window = tk.Label(input_frame_roles_window,
            text="Admin Feature",
            font=("Arial", size_roles_window),
            background="white"
        )
        feature_label_roles_window.grid(column=3, row=3, sticky=tk.W + tk.E, pady=5)

        self.feature = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.feature.grid(column=4, row=3, sticky=tk.W + tk.E, pady=5)

        # Loeschen
        delete_label_roles_window = tk.Label(input_frame_roles_window,
            text="Löschen",
            font=("Arial", size_roles_window),
            background="white"
        )
        delete_label_roles_window.grid(column=3, row=4, sticky=tk.W + tk.E, pady=5)

        self.delete = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.delete.grid(column=4, row=4, sticky=tk.W + tk.E, pady=5)

        # Bearbeiten
        edit_label_roles_window = tk.Label(input_frame_roles_window,
            text="Bearbeiten",
            font=("Arial", size_roles_window),
            background="white"
        )
        edit_label_roles_window.grid(column=3, row=5, sticky=tk.W + tk.E, pady=5)

        self.edit = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.edit.grid(column=4, row=5, sticky=tk.W + tk.E, pady=5)

        # Erstellen
        create_label_roles_window = tk.Label(input_frame_roles_window,
            text="Erstellen",
            font=("Arial", size_roles_window),
            background="white"
        )
        create_label_roles_window.grid(column=3, row=6, sticky=tk.W + tk.E, pady=5)

        self.create = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.create.grid(column=4, row=6, sticky=tk.W + tk.E, pady=5)

        # Gruppe Loeschen
        delete_g_label_roles_window = tk.Label(input_frame_roles_window,
            text="Gruppe Löschen" ,
            font=("Arial", size_roles_window),
            background="white"
        )
        delete_g_label_roles_window.grid(column=3, row=7, sticky=tk.W + tk.E, pady=5)

        self.delete_g = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.delete_g.grid(column=4, row=7, sticky=tk.W + tk.E, pady=5)

        # Gruppe Erstellen
        create_g_label_roles_window = tk.Label(input_frame_roles_window,
            text="Gruppe Erstellen",
            font=("Arial", size_roles_window),
            background="white"
        )
        create_g_label_roles_window.grid(column=5, row=1, sticky=tk.W + tk.E, pady=5)

        self.create_g = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.create_g.grid(column=6, row=1, sticky=tk.W + tk.E, pady=5)

        # Gruppe Bearbeiten
        edit_g_label_roles_window = tk.Label(input_frame_roles_window,
            text="Gruppe Bearbeiten",
            font=("Arial", size_roles_window),
            background="white"
        )
        edit_g_label_roles_window.grid(column=5, row=2, sticky=tk.W + tk.E, pady=5)

        self.edit_g = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.edit_g.grid(column=6, row=2, sticky=tk.W + tk.E, pady=5)

        # Rollen Erstellen
        create_r_label_roles_window = tk.Label(input_frame_roles_window,
            text="Rollen Erstellen",
            font=("Arial", size_roles_window),
            background="white"
        )
        create_r_label_roles_window.grid(column=5, row=3, sticky=tk.W + tk.E, pady=10)

        self.create_r = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.create_r.grid(column=6, row=3, sticky=tk.W + tk.E, pady=5)

        # Rollen Bearbeiten
        edit_r_label_roles_window = tk.Label(input_frame_roles_window,
            text="Rollen Bearbeiten",
            font=("Arial", size_roles_window),
            background="white"
        )
        edit_r_label_roles_window.grid(column=5, row=4, sticky=tk.W + tk.E, pady=5)

        self.edit_r = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.edit_r.grid(column=6, row=4, sticky=tk.W + tk.E, pady=5)

        # Rollen Loeschen
        delete_r_label_roles_window = tk.Label(input_frame_roles_window,
            text="Rolle Löschen",
            font=("Arial", size_roles_window),
            background="white"
        )
        delete_r_label_roles_window.grid(column=5, row=5, sticky=tk.W + tk.E, pady=5)

        self.delete_r = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.delete_r.grid(column=6, row=5, sticky=tk.W + tk.E, pady=5)

        # User Loeschen
        delete_u_label_roles_window = tk.Label(input_frame_roles_window,
            text="User Löschen",
            font=("Arial", size_roles_window),
            background="white"
        )
        delete_u_label_roles_window.grid(column=5, row=6, sticky=tk.W + tk.E, pady=5)

        self.delete_u = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.delete_u.grid(column=6, row=6, sticky=tk.W + tk.E, pady=5)

        # User Bearbeiten
        edit_u_label_roles_window = tk.Label(input_frame_roles_window,
            text="User Bearbeiten",
            font=("Arial", size_roles_window),
            background="white"
        )
        edit_u_label_roles_window.grid(column=5, row=7, sticky=tk.W + tk.E, pady=5)

        self.edit_u = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.edit_u.grid(column=6, row=7, sticky=tk.W + tk.E, pady=5)

        # User Erstellen
        create_u_label_roles_window = tk.Label(input_frame_roles_window,
            text="User Erstellen",
            font=("Arial", size_roles_window),
            background="white"
        )
        create_u_label_roles_window.grid(column=5, row=8, sticky=tk.W + tk.E, pady=5)

        self.create_u = ctk.CTkCheckBox(input_frame_roles_window, text_color="white")
        self.create_u.grid(column=6, row=8, sticky=tk.W + tk.E, pady=5)

        # Funktion zum Eintrag hinzufügen
        def refresh_entry():
            view = "True" if self.view.get() == 1 else "False"
            delete_rl = "True" if self.delete_rl.get() == 1 else "False"
            feature = "True" if self.feature.get() == 1 else "False"
            delete = "True" if self.delete.get() == 1 else "False"
            edit = "True" if self.edit.get() == 1 else "False"
            create = "True" if self.create.get() == 1 else "False"
            delete_g = "True" if self.delete_g.get() == 1 else "False"
            create_g = "True" if self.create_g.get() == 1 else "False"
            edit_g = "True" if self.edit_g.get() == 1 else "False"
            create_r = "True" if self.create_r.get() == 1 else "False"
            edit_r = "True" if self.edit_r.get() == 1 else "False"
            delete_r = "True" if self.delete_r.get() == 1 else "False"
            delete_u = "True" if self.delete_u.get() == 1 else "False"
            edit_u = "True" if self.edit_u.get() == 1 else "False"
            create_u = "True" if self.create_u.get() == 1 else "False"
            rechte = {
                "ROLLE_LOESCHBAR": delete_rl,
                "ADMIN_FEATURE": feature,
                "ENTRY_ANSEHEN": view,
                "ENTRY_LOESCHEN": delete,
                "ENTRY_BEARBEITEN": edit,
                "ENTRY_ERSTELLEN": create,
                "GRUPPEN_LOESCHEN": delete_g,
                "GRUPPEN_ERSTELLEN": create_g,
                "GRUPPEN_BEARBEITEN": edit_g,
                "ROLLEN_ERSTELLEN": create_r,
                "ROLLEN_BEARBEITEN": edit_r,
                "ROLLEN_LOESCHEN": delete_r,
                "USER_LOESCHEN": delete_u,
                "USER_BEARBEITEN": edit_u,
                "USER_ERSTELLEN": create_u
            }
            logger.debug(sqlapi.update_role(self.role_name.cget("text"), **rechte))
            from .AdminRoleWindow import AdminRoleWindow
            AdminRoleWindow.update_treeview_with_data()
            controller.show_frame(AdminRoleWindow)

        def delete_entry():
            """
            delete_entry():
                Löscht Benutzereinträge aus der Datenbank und erneuert die entsprechende
                Anzeige im AdminUserWindow-Frame.
            """
            state = True
            for user in sqlapi.read_all_benutzer():
                if user['Rolle'] == self.role_name.cget("text"):
                    state = False
            if state:
                sqlapi.delete_rolle(self.role_name.cget("text"))
            else:
                messagebox.showerror("Abgebrochen", "Es befinden sich noch Nutzer in den Gruppen")
            from .AdminRoleWindow import AdminRoleWindow
            AdminRoleWindow.update_treeview_with_data()
            controller.show_frame(AdminRoleWindow)

        def customMessageBoxCall():
            if customMessageBoxDelete(self,
                title="Aktion Bestätigen",
                message="Willst du diese Rolle unwiderruflich löschen?",
                buttonText="Rolle Löschen",
                blue=True
            ):
                delete_entry()

        self.edit_btn = tk.PhotoImage(file=resource_path("./includes/assets/AktualisierenBig_blue.png"))
        self.lend_btn = tk.PhotoImage(file=resource_path("./includes/assets/Ausleihen.png"))
        self.delete_btn = tk.PhotoImage(file=resource_path("./includes/assets/Loeschen.png"))

        # Buttons in ein separates Frame
        button_frame_update_role = tk.Frame(self, background="white")
        button_frame_update_role.grid(row=2, column=0, pady=20)

        global delete_button, edit_button
        delete_button = tk.Button(button_frame_update_role,
            image=self.delete_btn,
            bd=0,
            relief=tk.FLAT,
            bg="white",
            cursor="hand2",
            activebackground="white",
            command=customMessageBoxCall
        )

        edit_button = tk.Button(button_frame_update_role,
            image=self.edit_btn,
            bd=0,
            relief=tk.FLAT,
            bg="white",
            cursor="hand2",
            activebackground="white",
            command=refresh_entry
        )

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(0, weight=1)

    def update_data(self, data):
        """
        Aktualisiert die Daten in den Entry-Feldern mit den bereitgestellten Informationen.
        Existierende Einträge in den Feldern werden gelöscht und durch die neuen Daten ersetzt.

        :param data: Eine Liste, die die neuen Daten für die Entry-Felder enthält.
                    Das erste Listenelement entspricht dem neuen Wert für `room_num_entry`.
                    Das zweite Listenelement entspricht dem neuen Wert für `place_entry`.

        """
        # Daten in die Entry-Felder einfügen
        self.role_name.configure(text=data[0])
        self.delete_rl.select() if data[1] == "✔" else self.delete_rl.deselect()
        if data[1] == "✔" and cache.user_group_data['ROLLEN_LOESCHEN'] == "True":
            delete_button.pack(side=tk.LEFT, padx=20)
        else:
            delete_button.pack_forget()
        self.feature.select() if data[2] == "✔" else self.feature.deselect()
        self.view.select() if data[3] == "✔" else self.view.deselect()
        self.delete.select() if data[4] == "✔" else self.delete.deselect()
        self.edit.select() if data[5] == "✔" else self.edit.deselect()
        self.create.select() if data[6] == "✔" else self.create.deselect()
        self.delete_g.select() if data[7] == "✔" else self.delete_g.deselect()
        self.create_g.select() if data[8] == "✔" else self.create_g.deselect()
        self.edit_g.select() if data[9] == "✔" else self.edit_g.deselect()
        self.create_r.select() if data[10] == "✔" else self.create_r.deselect()
        self.edit_r.select() if data[11] == "✔" else self.edit_r.deselect()
        if cache.user_group_data['ROLLEN_BEARBEITEN'] == "True":
            edit_button.pack(side=tk.LEFT, padx=20)
        else:
            edit_button.pack_forget()
        self.delete_r.select() if data[12] == "✔" else self.delete_r.deselect()
        self.delete_u.select() if data[13] == "✔" else self.delete_u.deselect()
        self.edit_u.select() if data[14] == "✔" else self.edit_u.deselect()
        self.create_u.select() if data[15] == "✔" else self.create_u.deselect()
