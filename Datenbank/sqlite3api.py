import sqlite3
import os
<<<<<<< HEAD
=======
from Security.UserSecurity import hashPassword

# Pfad zur Datenbankdatei
path: str = r'L:\Austausch\Azubi\dd-inv\db\DD-invBeispielDatenbank.sqlite3'
>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13

path:str = os.path.dirname(__file__)+'\DD-invBeispielDatenbank.sqlite3'
def init_connection():
    """
    Hilfsfunktion zur Herstellung einer Verbindung mit der SQLite-Datenbank.
    - Die Datenbankdatei muss unter dem angegebenen Pfad existieren.
    - row_factory wird auf sqlite3.Row gesetzt, um die Ergebnisse als Dictionaries zurückzugeben.
    """
    con = sqlite3.connect(path)
    # Wichtig ist das hier der Root-Pfad angegeben wird

    con.row_factory = sqlite3.Row  # Rückgabe von Zeilen als Dictionary
    return con

#####################################
# B E N U T Z E R - E N D P U N K T #
#####################################

def create_benutzer(nutzername, passwort, email):
    """
    Fügt einen neuen Benutzer zur Tabelle `Benutzer` hinzu.
<<<<<<< HEAD
    - Nutzername, Passwort und Email müssen übergeben werden.
    - Standardrolle wird auf 'Guest' gesetzt.
    - alles wird in Try gesetzt um bei fehlern ein Crash zu verhindern
=======
    Passwort_hashed_value wird genutzt um Plain_Passwörter in ein Hash wert zu ändern
    {e.args} werden genutzt um genauere Fehlermeldungen zurück zu bekommen
    :param Nutzername:z.B. LukasFa
    :param passwort:z.B. #Lukas1234 (Wird ihn ein Hashwert umgewandelt)
    :param Email:z.B. Lukas.Fabisch@fabisch.com
>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13
    """
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
    """
    Ruft alle Benutzer aus der Tabelle `Benutzer` ab.
    - Gibt eine Liste von Dictionaries zurück, die die Benutzerdaten enthalten.
    """
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

def read_benutzer_rolle(nutzername):
    """
<<<<<<< HEAD
    Ruft die Rolle eines Benutzers ab.
    - Der Nutzername dient als Identifikator.
    - Gibt einen String mit der Rolle des Benutzers zurück.
=======
    Ruft die Daten eines spezifischen Benutzers ab.
    :param Nutzername
>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13
    """
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("SELECT Rolle FROM Benutzer WHERE Nutzername = ?", (nutzername,))
        row = cur.fetchone()
        return dict(row).get('Rolle') if row else None
    except sqlite3.Error as e:
        return None, "Fehler beim Abrufen des Benutzers:", str(e)
    finally:
        con.close()

def update_benutzer(nutzername, neues_passwort=None, neues_email=None, neue_rolle=None):
    """
    Aktualisiert die Daten eines Benutzers (Passwort, Email, Rolle).
<<<<<<< HEAD
    - Nur die übergebenen Parameter werden geändert.
    - Dynamische Erstellung der SQL-Abfrage, basierend auf den übergebenen Parametern.
=======
    :param Nutzername
    :param neues_passwort:(falls kein neues, leer lassen und neues Komma setzten)
    :param neues_email:(falls kein neues, leer lassen und neues Komma setzten)
    :param neue_rolle:(falls kein neues, leer lassen und neues Komma setzten)
>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13
    """
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
    """
    Löscht einen Benutzer aus der Tabelle `Benutzer`.
    - Der Nutzername dient als Identifikator.
    """
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

def create_hardware(Service_Tag, Geraetetyp, Modell, Beschaedigung, Ausgeliehen_von, Raum):
    """
    Erstellt einen neuen Eintrag in der Tabelle `Hardware`.
<<<<<<< HEAD
    - Alle notwendigen Hardwaredetails (z. B. Service_Tag, Gerätetyp) müssen übergeben werden.
    """
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO Hardware (Service_Tag, Geraetetyp, Modell, Beschaedigung, Ausgeliehen_von, Standort) VALUES (?, ?, ?, ?, ?, ?)",
            (Service_Tag, Geraetetyp, Modell, Beschaedigung, Ausgeliehen_von, Standort)
        )
        con.commit()
=======
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
                "INSERT INTO Hardware (Service_Tag, Geraetetyp, Modell, Beschaedigung, Ausgeliehen_von, Raum) VALUES (?, ?, ?, ?, ?, ?)",
                (Service_Tag, Geraetetyp, Modell, Beschaedigung, Ausgeliehen_von, Raum)
            )
            con.commit()
>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13
        return "Hardware-Eintrag wurde erstellt."
    except sqlite3.Error as e:
        return "Fehler beim Erstellen des Hardware-Eintrags:", str(e)
    finally:
        con.close()

def fetch_hardware():
    """
    Ruft alle Hardware-Einträge aus der Tabelle `Hardware` ab.
    - Gibt eine Liste von Dictionaries zurück.
    """
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

def fetch_hardware_by_id(ID):
    """
    Ruft die Daten einer spezifischen Hardware anhand ihres `Service_Tag` ab.
<<<<<<< HEAD
    - Gibt ein Dictionary mit den Daten zurück oder None, falls kein Eintrag existiert.
    """
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM Hardware WHERE Service_Tag = ?", (Service_Tag,))
        row = cur.fetchone()
        return dict(row) if row else None
=======
    :param ID:zum identifizieren des Datensatzes
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Hardware WHERE ID = ?", (ID,))
            row = cur.fetchone()
            return dict(row) if row else None
>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13
    except sqlite3.Error as e:
        return None, "Fehler beim Abrufen des Service-Tags:", str(e)
    finally:
        con.close()

<<<<<<< HEAD
def update_Hardware_by_service_tag(Service_Tag, neue_Ausgeliehen_von=None, neue_beschaedigung=None, neue_Standort=None):
    """
    Aktualisiert bestimmte Felder einer Hardware basierend auf dem `Service_Tag`.
    - Nur die übergebenen Parameter (z. B. neue_Beschädigung) werden geändert.
    - Dynamische Erstellung der SQL-Abfrage.
=======
def update_hardware_by_ID(ID, neue_Ausgeliehen_von=None, neue_beschaedigung=None, neue_Standort=None):
    """
    Aktualisiert bestimmte Felder einer Hardware basierend auf dem `Service_Tag`.
    :param ID: zum identifizieren des Datensatzes
    :param neue_Ausgeliehen_von:falls kein neues, leer lassen und neues Komma setzten
    :param neue_beschaedigung:(falls kein neues, leer lassen und neues Komma setzten)
    :param neue_Standort:(falls kein neues, leer lassen und neues Komma setzten)
>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13
    """
    try:
        con = init_connection()
        cur = con.cursor()
        update_fields = []
        parameters = []

<<<<<<< HEAD
        if neue_Ausgeliehen_von:
            update_fields.append("Ausgeliehen_von = ?")
            parameters.append(neue_Ausgeliehen_von)
        if neue_beschaedigung:
            update_fields.append("Beschaedigung = ?")
            parameters.append(neue_beschaedigung)
        if neue_Standort:
            update_fields.append("Standort = ?")
            parameters.append(neue_Standort)
=======
            if neue_Ausgeliehen_von:
                update_fields.append("Ausgeliehen_von = ?")
                parameters.append(neue_Ausgeliehen_von)
            if neue_beschaedigung:
                update_fields.append("Beschaedigung = ?")
                parameters.append(neue_beschaedigung)
            if neue_Standort:
                update_fields.append("Raum = ?")
                parameters.append(neue_Standort)
>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13

        if not update_fields:
            return "Keine Aktualisierungsdaten vorhanden."

<<<<<<< HEAD
        sql_query = f"UPDATE Hardware SET {', '.join(update_fields)} WHERE Service_Tag = ?"
        parameters.append(Service_Tag)
        cur.execute(sql_query, parameters)
        con.commit()
=======
            sql_query = f"UPDATE Hardware SET {', '.join(update_fields)} WHERE ID = ?"
            parameters.append(ID)
            cur.execute(sql_query, parameters)
            con.commit()
>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13
        return "Hardware erfolgreich aktualisiert."
    except sqlite3.Error as e:
        return "Fehler beim Aktualisieren der Hardware:", str(e)
    finally:
        con.close()

<<<<<<< HEAD
def delete_Hardware_by_service_tag(Service_Tag):
    """
    Löscht einen Hardware-Eintrag aus der Tabelle `Hardware`.
    - Der `Service_Tag` dient als Identifikator.
    """
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM Hardware WHERE Service_Tag = ?", (Service_Tag,))
        con.commit()
=======
def delete_hardware_by_id(ID):
    """
    Löscht einen Hardware-Eintrag aus der Tabelle `Hardware`.
    :param ID:zum idenzifizieren des Datensatzes
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Hardware WHERE ID = ?", (ID,))
            con.commit()
>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13
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
    """
    Fügt eine neue Nutzerrolle mit spezifischen Rechten in die Tabelle `NutzerrollenRechte` ein.
<<<<<<< HEAD
    - Rechte können als Booleans oder Integer-Werte übergeben werden.
=======
    Rollenrechte müssen damit nur noch angehangen werden

>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13
    """
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO NutzerrollenRechte (ANSEHEN,ROLLE_LOESCHBAR,ADMIN_FEATURE,LOESCHEN,BEARBEITEN,ERSTELLEN,GRUPPEN_LOESCHEN,GRUPPEN_ERSTELLEN,GRUPPEN_BEARBEITEN,ROLLEN_ERSTELLEN,ROLLEN_BEARBEITEN,ROLLEN_LOESCHEN) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (ANSEHEN,
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
                     ROLLEN_LOESCHEN)
                    )
        con.close()
        return "Nutzerrolle wurder erfolgreich erstellt."
    except sqlite3.Error as e:
        return "Es ist eine fehler beim erstellen der Rolle aufgetreten", str(e)
    finally:
        con.close()

def read_all_Rollen():
    """
    Ruft alle Rollen aus der Tabelle `NutzerrollenRechte` ab.
    - Gibt eine Liste von Dictionaries zurück.
    """
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM NutzerrollenRechte")
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        return [], "Fehler beim Abrufen der Rollen:", str(e)
    finally:
        con.close()

def read_Rolle(Rolle):
    """
    Ruft die Rolle eines spezifischen Benutzers ab.
    - Der Nutzername dient als Identifikator.
    """
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM NutzerrollenRechte WHERE Rolle = ?", (Rolle,))
        row = cur.fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        return None, "Fehler beim Abrufen der Rollen:", str(e)
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
    """
    Aktualisiert spezifische Rechte einer Rolle in der Tabelle `NutzerrollenRechte`.
    - Dynamische Erstellung der SQL-Abfrage, basierend auf den übergebenen Parametern.
    """
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
    """
    Entfernt eine Rolle aus der Tabelle `NutzerrollenRechte`.
    - Die Rollenbezeichnung dient als Identifikator.
    """
    try:
        con = init_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM NutzerrollenRechte WHERE Rolle = ?", (Rolle,))
        con.commit()
        return "Rolle wurde erfolgreich entfernt."
    except sqlite3.Error as e:
<<<<<<< HEAD
        return "Fehler beim Entfernen der Rolle:", str(e)
    finally:
        con.close()
=======
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
            cur.execute(
                """
                INSERT INTO Ausleih_Historie(Service_Tag, Nutzername, Ausgeliehen_am)
                VALUES (?, ?, ?)
                """,
                (Service_Tag, Nutzername, Ausgeliehen_am)
            )
            con.commit()
            return "Eintrag in der Ausleih-Historie wurde erfolgreich erstellt."
    except sqlite3.Error as e:
        return f"Fehler beim Erstellen des Eintrags: {e}"

def fetch_ausleih_historie():
    """
    Ruft alle Einträge aus der Tabelle `Ausleih-Historie` ab.
    - Gibt eine Liste von Dictionaries mit den Daten zurück.
    """
    try:
        with init_connection() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM Ausleih_Historie")
            rows = cur.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        return f"Fehler beim Abrufen der Historie: {e}"

def fetch_ausleih_historie_by_id(ID):
    """
    Ruft einen spezifischen Eintrag der Tabelle `Ausleih-Historie` anhand der ID ab.
    - Gibt ein Dictionary mit den Daten zurück oder None, falls der Eintrag nicht existiert.
    :param ID: ID muss unbedingt angegeben werden
    """
    try:
        with init_connection() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM Ausleih_Historie WHERE ID = ?", (ID,))
            row = cur.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        return f"Fehler beim Abrufen des Eintrags: {e}"

def delete_ausleih_historie(ID):
     """
     Löscht einen Eintrag aus der Tabelle `Ausleih-Historie` anhand der ID.
     :param ID:ID muss mit angegeben werden
     """
     try:
         with init_connection() as con:
             cur = con.cursor()
             cur.execute("DELETE FROM Ausleih_Historie WHERE ID = ?", (ID,))
             con.commit()
             return "Eintrag erfolgreich gelöscht."
     except sqlite3.Error as e:
         return f"Fehler beim Löschen des Eintrags: {e}"

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
            cur.execute("INSERT INTO Room_Info(Raum, Ort) VALUES (?, ?)", (Raum, Ort))
            con.commit()
            return "Raum wurde erfolgreich erstellt."
    except sqlite3.Error as e:
        return f"Fehler beim Erstellen des Raumes: {e}"
def fetch_all_rooms():
    """
    Mit der Funktion rufen wir alle bis jetzt erstellten Räume in der Datenbank auf
    :return: Gesamte Liste aller Räume in einer Dictionary
    """
    try:
        with init_connection() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM Room_Info")
            rows = cur.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        return f"Fehler beim Abrufen der Räume: {e}"

def search_room(Raum):
    """

    :param Raum (Raumname z.B. E220)
    :return: Gibt nur die Informationen über den einzelnen Raum aus
    """
    try:
        with init_connection() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM Room_Info WHERE Raum = ?", (Raum,))
            row = cur.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        return f"Fehler beim Suchen des Raumes: {e}"

def update_room(Raum, neu_Raum, neu_Ort):
    """
    If Statement schaut nach, was genau geändert werden soll, if not zum absichern damit keine sachen auf NUll gesetzt werden
    Query zum updaten von zu updaten
    :param Raum:hier wird festgelegt welcher Primarykey angesprochen werden soll
    :param neu_Raum:die neue Value für Raum
    :param neu_Ort:die neue Value für Ort
    :returns geänderter Wert:
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            update_fields = []
            parameters = []

            if neu_Raum:
                update_fields.append("Raum = ?")
                parameters.append(neu_Raum)
            if neu_Ort:
                update_fields.append("Ort = ?")
                parameters.append(neu_Ort)

            if not update_fields:
                return "Keine Aktualisierungsdaten vorhanden."

            sql_query = f"UPDATE Room_Info SET {', '.join(update_fields)} WHERE Raum = ?"
            parameters.append(Raum)
            cur.execute(sql_query, parameters)
            con.commit()
            return "Raum erfolgreich aktualisiert."
    except sqlite3.Error as e:
        return f"Fehler beim Aktualisieren des Raumes: {e}"

def delete_room(Raum):
    """
    Funktion zum entfernen von Räumen, bitte nur verwenden wenn nötig.
    :param Raum:
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Room_Info WHERE Raum = ?", (Raum,))
            con.commit()
            return "Raum erfolgreich gelöscht."
    except sqlite3.Error as e:
        return f"Fehler beim Löschen des Raumes: {e}"
>>>>>>> 1304aaf9f02d26d692d6f5ae86e93b93e1c5bf13
