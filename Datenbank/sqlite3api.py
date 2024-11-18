import sqlite3

def init_connection():
    # Hilfsfunktion für Verbindungen
    con = sqlite3.connect('DD-invBeispielDatenbank.sqlite3')
    con.row_factory = sqlite3.Row  # Rückgabe von Zeilen als Dictionary
    return con


#####################################
# B E N U T Z E R - E N D P U N K T #
#####################################

def create_benutzer(nutzername, passwort, email):
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO Benutzer (Nutzername, Passwort, Email, Rolle) VALUES (?, ?, ?, 'Guest')",
            (nutzername, passwort, email)
        )
        con.commit()
        return "Benutzer wurde hinzugefügt."
    except sqlite3.Error as e:
        return "Fehler beim Hinzufügen des Benutzers:", str(e)
    finally:
        con.close()

def read_all_benutzer():
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM Benutzer")
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        return [], "Fehler beim Abrufen der Benutzer:", str(e)
    finally:
        con.close()

def read_benutzer(nutzername):
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM Benutzer WHERE Nutzername = ?", (nutzername,))
        row = cur.fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        return None, "Fehler beim Abrufen des Benutzers:", str(e)
    finally:
        con.close()

def update_benutzer(nutzername, neues_passwort=None, neues_email=None, neue_rolle=None):
    try:
        con = init_connection()
        cur = con.cursor()
        update_fields = []
        parameters = []

        if neues_passwort:
            update_fields.append("Passwort = ?")
            parameters.append(neues_passwort)
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
        return "Fehler beim Aktualisieren des Benutzers:", str(e)
    finally:
        con.close()

def delete_benutzer(nutzername):
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM Benutzer WHERE Nutzername = ?", (nutzername,))
        con.commit()
        return "Benutzer erfolgreich gelöscht."
    except sqlite3.Error as e:
        return "Fehler beim Löschen des Benutzers:", str(e)
    finally:
        con.close()


#####################################
# H A R D W A R E - E N D P U N K T #
#####################################

def create_hardware(Service_Tag, Geraetename, Modell, Beschaedigung, Ausgeliehen_von, Standort):
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO Hardware (Service_Tag, Geraetename, Modell, Beschaedigung, Ausgeliehen_von, Standort) VALUES (?, ?, ?, ?, ?, ?)",
            (Service_Tag, Geraetename, Modell, Beschaedigung, Ausgeliehen_von, Standort)
        )
        con.commit()
        return "Hardware-Eintrag wurde erstellt."
    except sqlite3.Error as e:
        return "Fehler beim Erstellen des Hardware-Eintrags:", str(e)
    finally:
        con.close()

def fetch_hardware():
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM Hardware")
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        return [], "Fehler beim Abrufen der Hardware-Einträge:", str(e)
    finally:
        con.close()

def fetch_hardware_by_id(Service_Tag):
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM Hardware WHERE Service_Tag = ?", (Service_Tag,))
        row = cur.fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        return None, "Fehler beim Abrufen des Service-Tags:", str(e)
    finally:
        con.close()

def update_Hardware_by_service_tag(Service_Tag, neue_Ausgeliehen_von=None, neue_beschaedigung=None, neue_Standort=None):
    try:
        con = init_connection()
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
        return "Fehler beim Aktualisieren der Hardware:", str(e)
    finally:
        con.close()

def delete_Hardware_by_service_tag(Service_Tag):
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM Hardware WHERE Service_Tag = ?", (Service_Tag,))
        con.commit()
        return "Hardware-Eintrag wurde erfolgreich entfernt."
    except sqlite3.Error as e:
        return "Fehler beim Entfernen des Hardware-Eintrags:", str(e)
    finally:
        con.close()
