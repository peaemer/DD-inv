import sqlite3

def init_connection():
    # Hilfsfunktion für Verbindungen
    con = sqlite3.connect('DD-invBeispielDatenbank.sqlite3')
    con.row_factory = sqlite3.Row  # Rückgabe von Zeilen als Dictionary
    return con

def update_benutzer(nutzername, neues_passwort=None, neues_email=None, neue_rolle=None):
    try:
        con = init_connection()
        cur = con.cursor()
        update_fields = []
        parameters = []

        if neues_passwort:
            update_fields.append("Passwort_Hash = ?")
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

update_benutzer("Alex", neues_passwort='test')