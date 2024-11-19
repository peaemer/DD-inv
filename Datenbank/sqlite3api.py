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

def create_hardware(Service_Tag, Geraetetyp, Modell, Beschaedigung, Ausgeliehen_von, Standort):
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO Hardware (Service_Tag, Geraetetyp, Modell, Beschaedigung, Ausgeliehen_von, Standort) VALUES (?, ?, ?, ?, ?, ?)",
            (Service_Tag, Geraetetyp, Modell, Beschaedigung, Ausgeliehen_von, Standort)
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

###########################################################
# N U T Z E R R O L L E N - R E C H T E - E N D P U N K T #
###########################################################

def create_Rolle(ANSEHEN,
                 ROLLE_LOESCHBAR,
                 ADMIN_FEATURE,
                 LOESCHEN,
                 BEARBEITEN,
                 ERSTELLEN,
                 GRUPPEN_LOESCHEN,
                 GRUPPEN_ERSTELLEN,
                 GRUPPEN_BEARBEITEN,
                 ROLLEN_ERSTELLEN,
                 ROLLEN_BEARBEITEN,
                 ROLLEN_LOESCHEN):
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO NutzerrollenRechte (ANSEHEN,ROLLE_LOESCHBAR,ADMIN_FEATURE,LOESCHEN,BEARBEITEN,ERSTELLEN,GRUPPEN_LOESCHEN,GRUPPEN_ERSTELLEN,GRUPPEN_BEARBEITEN,ROLLEN_ERSTELLEN,ROLLEN_BEARBEITEN,ROLLEN_LOESCHEN) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,)",
                    (ANSEHEN,ROLLE_LOESCHBAR,ADMIN_FEATURE,LOESCHEN,BEARBEITEN,ERSTELLEN,GRUPPEN_LOESCHEN,GRUPPEN_ERSTELLEN,GRUPPEN_BEARBEITEN,ROLLEN_ERSTELLEN,ROLLEN_BEARBEITEN,ROLLEN_LOESCHEN)
                    )
        con.close()
        return "Nutzerrolle wurder erfolgreich erstellt."
    except sqlite3 as e:
        return "Es ist eine fehler beim erstellen der Rolle aufgetreten", str(e)
    finally:
        con.close()

def read_all_Rollen():
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM NutzerollenRechte")
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        return [], "Fehler beim Abrufen der Rollen:", str(e)
    finally:
        con.close()

def read_Rolle(nutzername):
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

def update_rolle(Rolle,
                 neue_ROLLE_LOESCHBAR=None,
                 neue_ADMIN_FEATURE=None,
                 neue_LOESCHEN=None,
                 neue_BEARBEITEN=None,
                 neue_ERSTELLEN=None,
                 neue_GRUPPEN_LOESCHEN=None,
                 neue_GRUPPEN_ERSTELLEN=None,
                 neue_GRUPPEN_BEARBEITEN=None,
                 neue_ROLLEN_ERSTELLEN=None,
                 neue_ROLLEN_BEARBEITEN=None,
                 neue_ROLLEN_LOESCHEN=None):
    try:
        con = init_connection()
        cur = con.cursor()
        update_fields = []
        parameters = []

        if neue_ROLLE_LOESCHBAR:
            update_fields.append("ROLLE_LOESCHBAR = ?")
            parameters.append(neue_ROLLE_LOESCHBAR)
        if neue_ADMIN_FEATURE:
            update_fields.append("ADMIN_FEATURE = ?")
            parameters.append(neue_ADMIN_FEATURE)
        if neue_LOESCHEN:
            update_fields.append("LOESCHEN = ?")
            parameters.append(neue_LOESCHEN)
        if neue_BEARBEITEN:
            update_fields.append("BEARBEITEN = ?")
            parameters.append(neue_BEARBEITEN)
        if neue_ERSTELLEN:
            update_fields.append("ERSTELLEN = ?")
            parameters.append(neue_ERSTELLEN)
        if neue_GRUPPEN_LOESCHEN:
            update_fields.append("GRUPPEN_LOESCHEN = ?")
            parameters.append(neue_GRUPPEN_LOESCHEN)
        if neue_GRUPPEN_ERSTELLEN:
            update_fields.append("GRUPPEN_ERSTELLEN = ?")
            parameters.append(neue_GRUPPEN_ERSTELLEN)
        if neue_GRUPPEN_BEARBEITEN:
            update_fields.append("GRUPPEN_BEARBEITEN = ?")
            parameters.append(neue_GRUPPEN_BEARBEITEN)
        if neue_ROLLEN_ERSTELLEN:
            update_fields.append("ROLLEN_ERSTELLEN = ?")
            parameters.append(neue_ROLLEN_ERSTELLEN)
        if neue_ROLLEN_BEARBEITEN:
            update_fields.append("ROLLEN_BEARBEITEN = ?")
            parameters.append(neue_ROLLEN_BEARBEITEN)
        if neue_ROLLEN_LOESCHEN:
            update_fields.append("ROLLEN_LOESCHEN = ?")
            parameters.append(neue_ROLLEN_LOESCHEN)

        if not update_fields:
            return "Keine Aktualisierungsdaten vorhanden."

        sql_query = f"UPDATE NutzerrollenRechte SET {', '.join(update_fields)} WHERE Rolle = ?"
        parameters.append(Rolle)
        cur.execute(sql_query, parameters)
        con.commit()
        return "Rolle erfolgreich aktualisiert."

    except sqlite3.Error as e:
        return "Fehler beim Aktualisieren des Benutzers:", str(e)
    finally:
        con.close()

def delete_Rolle(Rolle):
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM NutzerrollenRechte WHERE Rolle = ?", (Rolle,))
        con.commit()
        return "Rolle wurde erfolgreich entfernt."
    except sqlite3.Error as e:
        return "Fehler beim Entfernen der Rolle:", str(e)
    finally:
        con.close()
