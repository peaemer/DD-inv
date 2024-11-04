import sqlite3

# Datenbank initialisieren
con = sqlite3.connect('DD-invBeispielDatenbank.sqlite3')
# Quarry als Curser erstellen
cur = con.cursor()


# Erstellen eine neuen Nutzers -Der Standard für Rolle ist Guest
# Wird nicht in der Datenbank angezeigt aber beim erstellen mit beachtet
def create_benutzer(nutzername, passwort, email):
    try:
        cur.execute("INSERT INTO Benutzer (Nutzername, Passwort, Email, Rolle) VALUES (?, ?, ?, Guest)",
                    (nutzername, passwort,email))
        con.commit()
        msg = "Benutzer wurde hinzugefügt"
        return msg
    except sqlite3.Error as e:
        msgError = "Fehler beim Hinzufügen des Benutzers"
        return msgError, e


# Damit werden alle Benutzer ausgegeben
def read_all_benutzer():
    try:
        cur.execute("SELECT * FROM Benutzer")
        rows = cur.fetchall()
        return [dict(row) for row in rows] # Ändert das Format zur Dictionary
    except sqlite3.Error as e:
        msgError = "Fehler beim Abrufen der Benutzer"
        return [], msgError, e


# Damit können bestimme Nutzer ausgegeben werden
def read_benutzer(nutzername):
    try:
        cur.execute("SELECT * FROM Benutzer WHERE Nutzername = ?", (nutzername,))
        row = cur.fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        msgError = "Fehler beim Abrufen des Benutzers:"
        return None, msgError, e


# Funktionen zum Aktualisieren eines Benutzers
def update_benutzer(nutzername, neues_passwort=None, neues_email=None, neue_rolle=None):
    try:
        update_fields = []
        parameters = []

        # Stellt sicher das nur die eingegeben Sachen aktualisiert wird
        if neues_passwort:
            update_fields.append("Passwort = ?")
            parameters.append(neues_passwort)
        if neues_email:
            update_fields.append("Email = ?")
            parameters.append(neues_email)
        if neue_rolle:
            update_fields.append('Rolle = ?')
            parameters.append(neue_rolle)

        # Falls keine Daten für die Aktualisierung übergeben werden
        if not update_fields:
            msg = "Keine Aktualisierungensdaten vorhanden"
            return msg


        # SQL Abfrage wird aus den vorhandenen Variablen erstellt
        sql_quary =  f"UPDATE BENUTZER SET {', '.join(update_fields)} WHERE Nutzername = ?"
        parameters.append(nutzername)
        cur.execute(sql_quary, parameters)
        con.commit()
        msg = "Benutzer erfolgreich erstellt"
        return msg
    except sqlite3.Error as e:
        msg = "Fehler beim Aktualisieren des Benutzers:"
        return msg, e


# Funktion zum Löschen eines Benutzers
def delete_benutzer(nutzername):
    try:
        cur.execute("DELETE FROM Benutzer WHERE Nutzername = ?", (nutzername,))
        con.commit()
        print("Benutzer erfolgreich gelöscht.")
    except sqlite3.Error as e:
        print("Fehler beim Löschen des Benutzers:", e)


# Endpunkt für Hardware #

#Hiermit kann neue Hardware erstellt werden

def create_hardware(Service_Tag, Geraetename, Modell, Beschaedigung, Ausgeliehen_von, Standort):
    try:
        con.execute("INSERT INTO Hardware(Service_Tag, Geraetename, Modell, Beschaedigung, Ausgeliehen_von, Standort) VALUES(? ,? ,? ,? ,? ,?)",
                    (Service_Tag, Geraetename, Modell, Beschaedigung, Ausgeliehen_von, Standort))
        con.commit()
        print("Hardware eintrag wurde erstellt")
    except sqlite3.Error as e:
        print("Fehler beim erstellen des Hardware eintrags", e)

def fetch_hardware


con.close()