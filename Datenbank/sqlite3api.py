import sqlite3
import os
from Security.UserSecurity import hashPassword

# Pfad zur Datenbankdatei
path: str = r'L:\Austausch\Azubi\dd-inv\db\DD-invBeispielDatenbank.sqlite3'

def init_connection():
    """
    Hilfsfunktion zur Herstellung einer Verbindung mit der SQLite-Datenbank.
    - Überprüft, ob die Datenbankdatei existiert.
    - row_factory wird auf sqlite3.Row gesetzt, um die Ergebnisse als Dictionaries zurückzugeben.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Datenbankdatei nicht gefunden: {path}")
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    return con


#####################################
# B E N U T Z E R - E N D P U N K T #
#####################################

def create_benutzer(nutzername, passwort, email):
    """
    Fügt einen neuen Benutzer zur Tabelle `Benutzer` hinzu.
    Passwort_hashed_value wird genutzt um Plain_Passwörter in ein Hash wert zu ändern
    {e.args} werden genutzt um genauere Fehlermeldungen zurück zu bekommen
    :param Nutzername:z.B. LukasFa
    :param passwort:z.B. #Lukas1234 (Wird ihn ein Hashwert umgewandelt)
    :param Email:z.B. Lukas.Fabisch@fabisch.com
    """
    try:
        passwort_hashed_value = hashPassword(passwort)
        with init_connection() as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Benutzer (Nutzername, Passwort, Email, Rolle) VALUES (?, ?, ?, 'Guest')",
                (nutzername, passwort_hashed_value, email)
            )
            con.commit()
        return "Benutzer wurde hinzugefügt."
    except sqlite3.Error as e:
        return f"Fehler beim Hinzufügen des Benutzers: {e.args[0]}"

def read_all_benutzer():
    """
    Ruft alle Benutzer aus der Tabelle `Benutzer` ab.
    Fetchall um jeden einzelnen Eintrag zu bekommen
    RuntimeError ist dafür da um fehler bei der Dictionary vorzubeugen
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Benutzer")
            rows = cur.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        raise RuntimeError(f"Fehler beim Abrufen der Benutzer: {e.args[0]}")

def read_benutzer(nutzername):
    """
    Ruft die Daten eines spezifischen Benutzers ab.
    :param Nutzername
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Benutzer WHERE Nutzername = ?", (nutzername,))
            row = cur.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        raise RuntimeError(f"Fehler beim Abrufen des Benutzers: {e.args[0]}")

def update_benutzer(nutzername, neues_passwort=None, neues_email=None, neue_rolle=None):
    """
    Aktualisiert die Daten eines Benutzers (Passwort, Email, Rolle).
    :param Nutzername
    :param neues_passwort:(falls kein neues, leer lassen und neues Komma setzten)
    :param neues_email:(falls kein neues, leer lassen und neues Komma setzten)
    :param neue_rolle:(falls kein neues, leer lassen und neues Komma setzten)
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            update_fields = []
            parameters = []

            if neues_passwort:
                update_fields.append("Passwort = ?")
                parameters.append(hashPassword(neues_passwort))
            if neues_email:
                update_fields.append("Email = ?")
                parameters.append(neues_email)
            if neue_rolle:
                update_fields.append("Rolle = ?")
                parameters.append(neue_rolle)

            if not update_fields:
                return "Keine Aktualisierungsdaten vorhanden."

            sql_query = f"UPDATE Benutzer SET {', '.join(update_fields)} WHERE Nutzername = ?"
            parameters.append(nutzername)
            cur.execute(sql_query, parameters)
            con.commit()
        return "Benutzer erfolgreich aktualisiert."
    except sqlite3.Error as e:
        return f"Fehler beim Aktualisieren des Benutzers: {e.args[0]}"

def delete_benutzer(nutzername):
    """
    Löscht einen Benutzer aus der Tabelle `Benutzer`.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Benutzer WHERE Nutzername = ?", (nutzername,))
            con.commit()
        return "Benutzer erfolgreich gelöscht."
    except sqlite3.Error as e:
        return f"Fehler beim Löschen des Benutzers: {e.args[0]}"


#####################################
# H A R D W A R E - E N D P U N K T #
#####################################

def create_hardware(Service_Tag, Geraetetyp, Modell, Beschaedigung, Ausgeliehen_von, Raum):
    """
    Erstellt einen neuen Eintrag in der Tabelle `Hardware`.
    :param Service_Tag
    :param Geraetetyp
    :param Modell
    :param Beschaedigung
    :param Ausgeliehen_von
    :param Standort
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Hardware (Service_Tag, Geraetetyp, Modell, Beschaedigung, Ausgeliehen_von, Standort) VALUES (?, ?, ?, ?, ?, ?)",
                (Service_Tag, Geraetetyp, Modell, Beschaedigung, Ausgeliehen_von, Raum)
            )
            con.commit()
        return "Hardware-Eintrag wurde erstellt."
    except sqlite3.Error as e:
        return f"Fehler beim Erstellen des Hardware-Eintrags: {e.args[0]}"

def fetch_hardware():
    """
    Ruft alle Hardware-Einträge aus der Tabelle `Hardware` ab.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Hardware")
            rows = cur.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        raise RuntimeError(f"Fehler beim Abrufen der Hardware: {e.args[0]}")

def fetch_hardware_by_id(Service_Tag):
    """
    Ruft die Daten einer spezifischen Hardware anhand ihres `Service_Tag` ab.
    :param Service_Tag:z.B. ABC123
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Hardware WHERE Service_Tag = ?", (Service_Tag,))
            row = cur.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        raise RuntimeError(f"Fehler beim Abrufen der Hardware: {e.args[0]}")

def update_hardware_by_service_tag(Service_Tag, neue_Ausgeliehen_von=None, neue_beschaedigung=None, neue_Standort=None):
    """
    Aktualisiert bestimmte Felder einer Hardware basierend auf dem `Service_Tag`.
    :param Nutzername
    :param neue_Ausgeliehen_von:falls kein neues, leer lassen und neues Komma setzten
    :param neue_beschaedigung:(falls kein neues, leer lassen und neues Komma setzten)
    :param neue_Standort:(falls kein neues, leer lassen und neues Komma setzten)
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            update_fields = []
            parameters = []

            if neue_Ausgeliehen_von:
                update_fields.append("Ausgeliehen_von = ?")
                parameters.append(neue_Ausgeliehen_von)
            if neue_beschaedigung:
                update_fields.append("Beschaedigung = ?")
                parameters.append(neue_beschaedigung)
            if neue_Standort:
                update_fields.append("Standort = ?")
                parameters.append(neue_Standort)

            if not update_fields:
                return "Keine Aktualisierungsdaten vorhanden."

            sql_query = f"UPDATE Hardware SET {', '.join(update_fields)} WHERE Service_Tag = ?"
            parameters.append(Service_Tag)
            cur.execute(sql_query, parameters)
            con.commit()
        return "Hardware erfolgreich aktualisiert."
    except sqlite3.Error as e:
        return f"Fehler beim Aktualisieren der Hardware: {e.args[0]}"

def delete_hardware_by_service_tag(Service_Tag):
    """
    Löscht einen Hardware-Eintrag aus der Tabelle `Hardware`.
    :param Service_Tag:z.B. ABC123
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Hardware WHERE Service_Tag = ?", (Service_Tag,))
            con.commit()
        return "Hardware-Eintrag wurde erfolgreich entfernt."
    except sqlite3.Error as e:
        return f"Fehler beim Entfernen des Hardware-Eintrags: {e.args[0]}"


###########################################################
# N U T Z E R R O L L E N - R E C H T E - E N D P U N K T #
###########################################################

def create_rolle(Rolle, **rechte):
    """
    Fügt eine neue Nutzerrolle mit spezifischen Rechten in die Tabelle `NutzerrollenRechte` ein.
    Rollenrechte müssen damit nur noch angehangen werden

    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            columns = ', '.join(rechte.keys())
            placeholders = ', '.join(['?'] * len(rechte))
            values = list(rechte.values())
            cur.execute(f"INSERT INTO NutzerrollenRechte (Rolle, {columns}) VALUES (?, {placeholders})", [Rolle] + values)
            con.commit()
        return "Nutzerrolle wurde erfolgreich erstellt."
    except sqlite3.Error as e:
        return f"Fehler beim Erstellen der Rolle: {e.args[0]}"

def read_all_rollen():
    """
    Ruft alle Rollen aus der Tabelle `NutzerrollenRechte` ab.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM NutzerrollenRechte")
            rows = cur.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        raise RuntimeError(f"Fehler beim Abrufen der Rollen: {e.args[0]}")

def delete_rolle(Rolle):
    """
    Entfernt eine Rolle aus der Tabelle `NutzerrollenRechte`.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM NutzerrollenRechte WHERE Rolle = ?", (Rolle,))
            con.commit()
        return "Rolle wurde erfolgreich entfernt."
    except sqlite3.Error as e:
        return f"Fehler beim Entfernen der Rolle: {e.args[0]}"


#######################################################
# A U S L E I H - H I S T O R I E - E N D P U N K T E #
#######################################################

def create_ausleih_historie(Service_Tag, Nutzername, Ausgeliehen_am):
    """
    Erstellt einen neuen Eintrag in der Tabelle `Ausleih-Historie`.
    - `Service_Tag`: Fremdschlüssel zur Hardware-Tabelle.
    - `Nutzername`: Fremdschlüssel zur Benutzer-Tabelle.
    - Optional können Ausleihdatum und Rückgabedatum angegeben werden.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Ausleih_Historie(Ausgeliehen_am,Service_Tag, Nutzername) VALUES (? ,? ,?)",
                        (Service_Tag,Nutzername,Ausgeliehen_am))
            con.commit()
            return "Historien eintrag wurder erstellt."
    except sqlite3.Error as e:
        return f"Fehler beim erstellen des Eintrags: {e.args[0]}"

def fetch_ausleih_historie():
    """
    Ruft alle Einträge aus der Tabelle `Ausleih-Historie` ab.
    - Gibt eine Liste von Dictionaries mit den Daten zurück.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Ausleih_Historie")
            rows = cur.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        return f"Fehler beim Abrufen der Ausleih_Historie: {e.args[0]}"

def fetch_ausleih_historie_by_id(ID):
    """
    Ruft einen spezifischen Eintrag der Tabelle `Ausleih-Historie` anhand der ID ab.
    - Gibt ein Dictionary mit den Daten zurück oder None, falls der Eintrag nicht existiert.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Ausleih_Historie WHERE ID = ?", (ID,))
            row = cur.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        return None, "Fehler beim Abrufen des Eintrags"

def delete_ausleih_historie(ID):
     """
     Löscht einen Eintrag aus der Tabelle `Ausleih-Historie` anhand der ID.
     """
     try:
         with init_connection() as con:
             cur = con.cursor()
             con.execute("DELETE FROM Ausleih_Historie WHERE ID = ?", (ID, ))
             con.commit()
             return "Eintrag wurde erfolgreich entfernt."
     except sqlite3.Error as e:
         return f"Fehler beim löschen des Eintrags {e.args[0]}"

#########################################
# R O O M _ I N F O - E N D P U N K T E #
#########################################

def create_room(Raum,Ort):
    """
    Wird zum erstellen von neuen Räumen benutzt
    :param Raum (Raumname z.B. E220)
    :param Ort (Ortsname z.B. Haus E 1. Etage)
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Room_Info(Raum, Ort) VALUES(? ,? )", (Raum, Ort))
            con.commit()
            return "Raum wurde erfolgreich erstellt"
    except sqlite3.Error as e:
        return f"Fehler beim erstellen des Raumes {e.args[0]}"

def fetch_all_rooms():
    """
    Mit der Funktion rufen wir alle bis jetzt erstellten Räume in der Datenbank auf
    :return: Gesamte Liste aller Räume in einer Dictionary
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * WHERE Room_Info")
            rows = cur.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        return f"Fehler beim erstellen von {e.args[0]}"

def search_room(Raum):
    """

    :param Raum (Raumname z.B. E220)
    :return: Gibt nur die Informationen über den einzelnen Raum aus
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Room_Info WHERE Raum = ?", (Raum))
            row = cur.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        return f"Fehler beim suchen des Raumes {e.args[0]}"

def update_room(Raum):
    """
    If Statement schaut nach, was genau geändert werden soll, if not zum absichern damit keine sachen auf NUll gesetzt werden
    Query zum updaten von zu updaten
    :param Raum:
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            update_fields = []
            parameters = []

            if neue_Ausgeliehen_von:
                update_fields.append("Raum = ?")
                parameters.append(neue_Ausgeliehen_von)
            if neue_beschaedigung:
                update_fields.append("Ort = ?")
                parameters.append(neue_beschaedigung)


            if not update_fields:
                return "Keine Aktualisierungsdaten vorhanden."

            sql_query = f"UPDATE Room_Info SET {', '.join(update_fields)} WHERE Raum = ?"
            parameters.append(Raum)
            cur.execute(sql_query, parameters)
            con.commit()
        return "Raum erfolgreich aktualisiert."
    except sqlite3.Error as e:
        return f"Fehler beim Aktualisieren des Raumes: {e.args[0]}"

def delete_room(Raum):
    """
    Funktion zum entfernen von Räumen, bitte nur verwenden wenn nötig.
    :param Raum:
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Room_Info WHERE Raum = ?", (Raum))
            con.commit()
            return "Raum wurde gelöscht"
    except sqlite3.Error as e:
        return f"Fehler beim löschen des Raumes: {e.args[0]}"