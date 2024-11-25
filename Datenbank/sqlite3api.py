import sqlite3
import os
from Security.UserSecurity import hashPassword

# Pfad zur Datenbankdatei
path: str = os.path.join(os.path.dirname(__file__), 'DD-invBeispielDatenbank.sqlite3')

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
    """
    try:
        passwort_hashed_value = hashPassword(passwort)
        with init_connection() as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Benutzer (Nutzername, Passwort, Email, Rolle) VALUES (?, ?, ?, 'Guest')",
                (nutzername, passwort_hashed_value, email)
            )
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
        return "Benutzer erfolgreich gelöscht."
    except sqlite3.Error as e:
        return f"Fehler beim Löschen des Benutzers: {e.args[0]}"


#####################################
# H A R D W A R E - E N D P U N K T #
#####################################

def create_hardware(Service_Tag, Geraetetyp, Modell, Beschaedigung, Ausgeliehen_von, Standort):
    """
    Erstellt einen neuen Eintrag in der Tabelle `Hardware`.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Hardware (Service_Tag, Geraetetyp, Modell, Beschaedigung, Ausgeliehen_von, Standort) VALUES (?, ?, ?, ?, ?, ?)",
                (Service_Tag, Geraetetyp, Modell, Beschaedigung, Ausgeliehen_von, Standort)
            )
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
        return "Hardware erfolgreich aktualisiert."
    except sqlite3.Error as e:
        return f"Fehler beim Aktualisieren der Hardware: {e.args[0]}"

def delete_hardware_by_service_tag(Service_Tag):
    """
    Löscht einen Hardware-Eintrag aus der Tabelle `Hardware`.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Hardware WHERE Service_Tag = ?", (Service_Tag,))
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
        return "Rolle wurde erfolgreich entfernt."
    except sqlite3.Error as e:
        return f"Fehler beim Entfernen der Rolle: {e.args[0]}"
