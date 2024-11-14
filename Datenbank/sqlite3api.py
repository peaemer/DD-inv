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
        # Mit ".execute" rufen wir die zuvor verknüpfte Datenbank auf eine darauffolgenden Befehl auzuführen
        # Der Befehl erfolgt mit Doppelter Klammer, in die erste Klammer kommt der SQL befehl und die zweite,
        # Die nötigen Parameter
        con.commit()
        # Mit dem .Commit befehl werden die Änderungen an die DB übertragen
        msg = "Benutzer wurde hinzugefügt"
        return msg
    except sqlite3.Error as e:
        # Error exception wird in jeder Funktion aufgerufen
        # Ausgabe der Funktion kann bei bedarf als "print" eingestellt werden
        msgError = "Fehler beim Hinzufügen des Benutzers"
        return msgError, e


# Damit werden alle Benutzer ausgegeben
def read_all_benutzer():
    #Alle Funktionen wurden in "Try" gesetzt um Fehler bei der Ausführung des Prgramms zu verhinder
    try:
        cur.execute("SELECT * FROM Benutzer")
        #
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

        # Sortiern der Fehler der DB in eine "Liste" inclusive der beigefügten Parameter
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

# Hiermit kann neue Hardware erstellt werden

def create_hardware(Service_Tag, Geraetename, Modell, Beschaedigung, Ausgeliehen_von, Standort):
    try:
        con.execute("INSERT INTO Hardware(Service_Tag, Geraetename, Modell, Beschaedigung, Ausgeliehen_von, Standort) VALUES(? ,? ,? ,? ,? ,?)",
                    (Service_Tag, Geraetename, Modell, Beschaedigung, Ausgeliehen_von, Standort))
        con.commit()
        print("Hardware eintrag wurde erstellt")
    except sqlite3.Error as e:
        print("Fehler beim erstellen des Hardware eintrags", e)

# Funktionen zum Abrufen der gesamten Datenbank "Hardware"
def fetch_hardware():
    try:
        con.execute("SELECT * FROM Hardware")
        rows = cur.fetchall()
        return [dict(rows)for rows in rows]
    except sqlite3.Error as e:
        print("Fehler beim Abrufen der Hardware einträge", e)
        return []

# Funktion zum Abrufen von einzelnen Service-Tags
def fetch_hardware_by_id(Service_Tag):
    try:
        con.execute("SELECT * FROM Hardware WHERE Service_Tag = ?", (Service_Tag,))
        rows = cur.fetchall()
        return dict(rows) if rows else None
    except sqlite3.Error as e:
        print("Fehler beim Abrufen des Service-Tags, bitte überprüfen sie die Schreibweise")


# Funktion zum Updaten von Hardware Einträgen
def update_Hardware_by_service_tag(Service_Tag, neue_Ausgeliehen_von=None, neue_beschaedigung=None, neue_Standort=None):
    try:
        update_fields = []
        parameters = []

        # Stellt sicher das nur die eingegeben Sachen aktualisiert wird
        if neue_Ausgeliehen_von:
            update_fields.append("Ausgeliehen_von = ?")
            parameters.append()
        if neue_Standort:
            update_fields.append("Standort = ?")
            parameters.append(neue_Standort)
        if neue_beschaedigung:
            update_fields.append('Beschaedigung = ?')
            parameters.append(neue_beschaedigung)

        # Falls keine Daten für die Aktualisierung übergeben werden
        if not update_fields:
            msg = "Keine Aktualisierungensdaten vorhanden"
            return msg

        # SQL Abfrage wird aus den vorhandenen Variablen erstellt
        sql_quary =  f"UPDATE HARDWARE SET {', '.join(update_fields)} WHERE Service_Tag = ?"
        parameters.append(Service_Tag)
        cur.execute(sql_quary, parameters)
        con.commit()
        msg = "Benutzer erfolgreich erstellt"
        return msg
    except sqlite3.Error as e:
        msg = "Fehler beim Aktualisieren des Benutzers:"
        return msg, e

# Funktion zum Entfernen von Hardware-Einträgen
def delete_Hardware_by_service_tag(Service_Tag):
    try:
        con.execute(("DELETE FROM HARDWARE WHERE Service_Tag = ?"), (Service_Tag,))
        con.commit()
        print("Hardware-Eintrag wurde erfolgreich entfernt")
    except sqlite3.Error as e:
        msg = "Fehler beim entfernen des Hardware eintrags"
        return  msg, e

con.close()