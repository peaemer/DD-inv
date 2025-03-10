import sqlite3
import os
import json
import time
from typing import Any

from includes.util.Paths import app_files_path_string
from .UserSecurity import hash_password
from ..util.Logging import Logger

logger:Logger = Logger('sqlite3api')

# Pfad zur Datenbankdatei
main_path: str = r'M:\Austausch\Azubi\dd-inv\db\DD-invBeispielDatenbank.sqlite3'
__use__fallback_path: bool = True
__fallback_path1:str = r'L:\Austausch\Azubi\dd-inv\db\DD-invBeispielDatenbank.sqlite3'
__fallback_path2: str = app_files_path_string + 'DD-invBeispielDatenbank.sqlite3'

def __extract_entry(unextracted_entry:str) -> tuple[float, str]:
    """
        .
    """
    entry_dict:dict[float:str] = json.loads(unextracted_entry)
    return list(entry_dict.keys())[0], entry_dict[list(entry_dict.keys())[0]]

def extract_entry(unextracted_entry:str) -> tuple[float, str]:
    """
        .
    """
    return __extract_entry(unextracted_entry)

def parse_entry(entry_data:str) -> str:
    """
        takes a string and turns it into a dict with the current time as the key and the data as the value

        :param str entry_data: a string representing the data

        :returns: a string representing the dict with the data and the current time
    """
    time.time()
    return str(dict({str(time.time()): entry_data}))

def init_connection() -> sqlite3.Connection:
    """
        Hilfsfunktion zur Herstellung einer Verbindung mit der SQLite-Datenbank.
        - Überprüft, ob die Datenbankdatei existiert
        - falls die haupt Datenbank nicht existiert, wird nach den beiden fallback-Datenbanken gesucht oder eine Exception geworfen.
        - das row_factory attribut der connection wird auf sqlite3.Row gesetzt, um die Ergebnisse als Dictionaries zurückzugeben.
    """
    path_ = ''

    logger.debug_e(f"""trying to locate main database: "{main_path}" """)
    if os.path.exists(main_path):
        logger.debug_e(f"""successfully located main database: "{main_path}" """)
        path_ = main_path
    elif __use__fallback_path:
        logger.debug_e(f"""failed to locate main database: "{main_path}" """)
        logger.debug_e(f"""trying to locate fallback database 1: "{__fallback_path1}" """)
        if os.path.exists(__fallback_path1):
            logger.debug_e(f"""successfully located fallback database 1: "{__fallback_path1}" """)
            path_ = __fallback_path1
        else:
            logger.debug_e(f"""failed to locate fallback database 1: "{__fallback_path1}" """)
        if os.path.exists(__fallback_path2):
            logger.debug_e(f"""successfully located fallback database 2: "{__fallback_path2}" """)
            path_ = __fallback_path2
        else:
            logger.debug_e(f"""failed to locate fallback database 2: "{__fallback_path2}" """)
    if path_ == '':
        logger.error(f"""failed to locate main database as well as fallback database 1 as well as fallback database 2""")
        raise FileNotFoundError(f"keine mögliche Datenbank gefunden")
    con = sqlite3.connect(path_)
    con.row_factory = sqlite3.Row
    return con


###############################################################
# T A B E L L E N - B E A R B E I T U N G S - E N D P U N K T #
###############################################################

def add_column(table_name:str, column_name:str, data_type:str = 'TEXT') -> str:
    """
        Fügt eine neue spalte zu einer Tabelle hinzu.

        :param str table_name: der name der Tabelle, in die die Spalte eingefügt werden soll.
        :param str column_name: der name der Tabellenspalte, die hizugefügt werden soll.
        :param str data_type: der Datentyp den die Einträge der neuen Spalte haben sollen.

        :return: Erfolgsmeldung oder Fehlerbeschreibung.
    """
    con:sqlite3.Connection
    try:
        with init_connection() as con:
            cur = con.cursor()
            # wir brauchen ein Cursor um SQL Befehle an die Datenbank zu senden
            cur.execute(
                f'ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type}'
            )
            con.commit()
        return f'Tabellenspalte {column_name}  wurde hizugefügt.'
    except sqlite3.Error as e:
        # e.args wird benötigt, um detailliertere Information über die Fehler dazustellen
        return f"Fehler beim Hinzufügen der Tabellenspalte: {e.args[0]}"

def remove_column(table_name:str, column_name:str) -> str:
    """
        Fügt eine neue spalte zu einer Tabelle hinzu.

        :param str table_name: der name der Tabelle, in die die Spalte eingefügt werden soll.
        :param str column_name: der name der Tabellenspalte, die hinzugefügt werden soll.

        :return: Erfolgsmeldung oder Fehlerbeschreibung.
    """
    con: sqlite3.Connection
    try:
        with init_connection() as con:
            cur = con.cursor()
            # wir brauchen ein Cursor um SQL Befehle an die Datenbank zu senden
            cur.execute(
                f'ALTER TABLE {table_name} DROP COLUMN {column_name}'
            )
            con.commit()
        return f'Tabellenspalte {column_name} wurde entfernt.'
    except sqlite3.Error as e:
        # e.args wird benötigt, um detailliertere Information über die Fehler dazustellen
        return f"Fehler beim Entfernen der Tabellenspalte: {e.args[0]}"

def add_table(table_name:str, new_columns:list[tuple[str, str | None]]) -> str:
    """
        Fügt eine neue Tabelle zur Datenbank hinzu.

        :param str table_name: der name der Tabelle, die hizugefügt werden soll.
        :param list[Tuple(str, str|None)] new_columns: alle Spalten, die die Datenbank am Anfang besitzen soll.
            der erste Eintrag in jedem Tuple gibt den Namen der neuen Spalte an und der zweite den Datentyp.

        :return: Erfolgsmeldung oder Fehlerbeschreibung.
    """
    sql_stmt:str = f'CREATE TABLE {table_name}'
    sql_stmt += ' ('
    if new_columns:
        for single_new_column in new_columns:
            sql_stmt += f'{single_new_column[0]}'
            sql_stmt += f' {single_new_column[1]}'  if single_new_column[1] else ' TEXT'
            sql_stmt += ', '
    sql_stmt = sql_stmt[:-2]
    sql_stmt += ')'
    try:
        with init_connection() as con:
            cur = con.cursor()
            # wir brauchen ein Cursor um SQL Befehle an die Datenbank zu senden
            cur.execute(sql_stmt)
            con.commit()
        return f'Tabelle {table_name} wurde hinzugefügt.'
    except sqlite3.Error as e:
        # e.args wird benötigt, um detailiertere Information über die Fehler dazustellen
        return f"Fehler Erstellen der Tabelle: {e.args[0]}"

def remove_table(table_name:str) -> str:
    """

    :param str table_name:

    :return:

    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            # wir brauchen ein Cursor um SQL Befehle an die Datenbank zusenden
            cur.execute(f'DROP TABLE {table_name}')
            con.commit()
        return f'Tabelle {table_name} wurde entfernt.'
    except sqlite3.Error as e:
        # e.args wird benötigt, um detailliertere Information über die Fehler dazustellen
        return f"Fehler Entfernen der Tabelle: {e.args[0]}"

#####################################
# B E N U T Z E R - E N D P U N K T #
#####################################

def create_benutzer(nutzername:str, passwort:str, email:str) -> str:
    """
        Fügt einen neuen Benutzer zur Tabelle `Benutzer` hinzu.
        Passwort_hashed_value wird genutzt, um Plain_Passwörter in ein Hash wert zu ändern
        {e.args} werden genutzt, um genauere Fehlermeldungen zurückzubekommen

        :param str nutzername: z.B. LukasFa
        :param str passwort: z.B. #Lukas1234 (Wird ihn ein Hashwert umgewandelt)
        :param str email: z.B. Lukas.Fabisch@fabisch.com

        :return: Erfolgsmeldung oder Fehlerbeschreibung.
    """
    try:
        passwort_hashed_value = hash_password(passwort)
        # wird benutzt, um das Passwort in ein Hashwert zu ändern
        con:sqlite3.Connection
        with init_connection() as con:
            cur = con.cursor()
            # wir brauchen ein Cursor um SQL Befehle an die Datenbank zusenden
            # Values werden als "?" - Platzhalter um fehler beim Übergeben der Values vorzubeugen,
            # und um eine Variable übergeben zu können
            cur.execute(
                "INSERT INTO Benutzer (Nutzername, Passwort, Email, Rolle) VALUES (?, ?, ?, 'Guest')",
                (nutzername, passwort_hashed_value, email)
            )
            con.commit()
        return "Benutzer wurde hinzugefügt."
    except sqlite3.Error as e:
        # e.args wird benötigt um detailiertere Information über die Fehler dazustellen
        return f"Fehler beim Hinzufügen des Benutzers: {e.args[0]}"
    finally:
        if con:
            con.close()

def read_all_benutzer() -> list[dict[str, str]]:
    """
        Ruft alle Benutzer aus der Tabelle `Benutzer` ab.
        Fetchall um jeden einzelnen Eintrag zu bekommen
        RuntimeError ist dafür da, um fehler bei der Dictionary vorzubeugen

        :return: eine Liste aus den daten aller Benutzer. Die Nutzerdaten werden in jeweils einem dictionary ausgegeben.
    """
    con: sqlite3.Connection
    data:list[dict[str,Any]]
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Benutzer")
            data = cur.fetchall()
    except sqlite3.Error as e:
        raise RuntimeError(f"Fehler beim Abrufen der Benutzer: {e.args[0]}")
    finally:
        if con:
            con.close()
    #der dict typ ist notwending um die Daten übersichtlicher in einer Tabelle darstellen zu können
    return [dict(row) for row in data]

def read_benutzer(nutzername:str) -> dict[str,str]:
    """
        Ruft die Daten eines spezifischen Benutzers ab.

        :param str nutzername: der name des zu lesenden benutzers

        :return: die Daten des nutzers in Form eines dictionaries
    """
    con:sqlite3.Connection|None = None
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Benutzer WHERE Nutzername = ?", (nutzername,))
            row = cur.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        raise RuntimeError(f"Fehler beim Abrufen des Benutzers: {e.args[0]}")
    finally:
        if con:
            con.close()

def read_benutzer_suchverlauf(nutzername):
    """
       Ruft den Suchverlauf eines spezifischen Benutzers ab.

       :param str nutzername: Der Benutzername, dessen Suchverlauf abgerufen werden soll.

       :return: Der Suchverlauf des Benutzers oder None, falls keiner vorhanden ist.
   """
    con: sqlite3.Connection
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT Suchverlauf FROM Benutzer WHERE Nutzername = ?", (nutzername,))
            row = cur.fetchone()
            return row["Suchverlauf"] if row else None
    except sqlite3.Error as e:
        raise RuntimeError(f"Fehler beim Abrufen des Suchverlaufs: {e.args[0]}")
    finally:
        if con:
            con.close()

def update_benutzer(nutzername:str, neues_passwort:str='', neues_email:str='', neue_rolle:str='', neue_suchverlauf:str='', neue_anwendungseinstellungen:str = '') -> str:
    """
        Aktualisiert die Daten eines Benutzers (Passwort, E-Mail, Rolle, Suchverlauf, Anwendungseinstellungen).

        :param str nutzername: der name des zu lesenden Benutzers.
        :param str neues_passwort:(falls kein neues, leer lassen und neues Komma setzten)
        :param str neues_email:(falls kein neues, leer lassen und neues Komma setzten)
        :param str neue_rolle:(falls kein neues, leer lassen und neues Komma setzten)
        :param str neue_suchverlauf:(falls kein neues, leer lassen und neues Komma setzten)
        :param str neue_anwendungseinstellungen:(falls kein neues, leer lassen und neues Komma setzten)

        :return: Erfolgsmeldung oder Fehlerbeschreibung.
    """
    con: sqlite3.Connection
    try:
        with init_connection() as con:
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
            if neue_suchverlauf:
                update_fields.append("Suchverlauf = ?")
                parameters.append(neue_suchverlauf)
            if neue_anwendungseinstellungen:
                update_fields.append("Application_Data = ?")
                parameters.append(neue_anwendungseinstellungen)

            if not update_fields:
                return "Keine Aktualisierungsdaten vorhanden."

            sql_query = f"UPDATE Benutzer SET {', '.join(update_fields)} WHERE Nutzername = ?"
            parameters.append(nutzername)
            cur.execute(sql_query, parameters)
            con.commit()
        return "Benutzer erfolgreich aktualisiert."
    except sqlite3.Error as e:
        return f"Fehler beim Aktualisieren des Benutzers: {e.args[0]}"
    finally:
        if con:
            con.close()

def delete_benutzer(nutzername:str) -> str:
    """
        Löscht einen Benutzer aus der Tabelle `Benutzer.

        :param str nutzername:
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

def create_hardware(service_tag:str, geraetetyp:str, modell:str, beschaedigung:str, ausgeliehen_von:str, raum:str, metadata:str) -> str:
    """
        Erstellt einen neuen Eintrag in der Tabelle `Hardware`.

        :param str service_tag:
        :param str geraetetyp:
        :param str modell:
        :param str beschaedigung:
        :param str ausgeliehen_von:
        :param str raum:
        :param str metadata:

        :return: Erfolgsmeldung oder Fehlerbeschreibung.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Hardware (Service_Tag, Geraetetype, Modell, Beschaedigung, Ausgeliehen_von, Raum, Metadata) VALUES (?, ?, ?, ?, ?, ?,?)",
                (service_tag, geraetetyp, modell, beschaedigung, ausgeliehen_von, raum, metadata),
            )
            con.commit()
        return "Hardware-Eintrag wurde erstellt."
    except sqlite3.Error as e:
        return f"Fehler beim Erstellen des Hardware-Eintrags: {e.args[0]}"

def fetch_hardware() ->list[dict[str, str]]:
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

def fetch_hardware_by_id(id:int):
    """
        Ruft die Daten einer spezifischen Hardware anhand ihres `Service_Tag` ab.
        :param int id: eine Konstante zum Identifizieren des Datensatzes
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            # ID muss hier mit einem Komma an Ende übergeben werden, um als Tuple zu agieren
            cur.execute("SELECT * FROM Hardware WHERE ID = ?", (id,))
            row = cur.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        raise RuntimeError(f"Fehler beim Abrufen der Hardware: {e.args[0]}")

def update_hardware_by_id(
            id:int,
            neuer_geraetetyp:str = None,
            neues_modell:str = None,
            neuer_service_tag:str = None,
            neue_ausgeliehen_von:str = None,
            neue_beschaedigung:str = None,
            neuer_standort:str = None):
    """
        Aktualisiert bestimmte Felder einer Hardware basierend auf der `ID`.

        :param int id: zum Identifizieren des Datensatzes
        :param str neuer_geraetetyp:
        :param str neues_modell:
        :param str neuer_service_tag:
        :param str neue_ausgeliehen_von: falls kein neues, leer lassen und neues Komma setzten
        :param str neue_beschaedigung: (falls kein neues, leer lassen und neues Komma setzten)
        :param str neuer_standort: (falls kein neues, leer lassen und neues Komma setzten)

    Args:
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            update_fields = []
            parameters = []

            if neue_ausgeliehen_von is not None:
                update_fields.append("Ausgeliehen_von = ?")
                parameters.append(neue_ausgeliehen_von)
            if neuer_service_tag is not None:
                update_fields.append("Service_Tag = ?")
                parameters.append(neuer_service_tag)
            if neue_beschaedigung is not None:
                update_fields.append("Beschaedigung = ?")
                parameters.append(neue_beschaedigung)
            if neuer_standort is not None:
                update_fields.append("Raum = ?")
                parameters.append(neuer_standort)
            if neues_modell is not None:
                update_fields.append("Modell = ?")
                parameters.append(neues_modell)
            if neuer_geraetetyp is not None:
                update_fields.append("Geraetetype = ?")
                parameters.append(neuer_geraetetyp)
            if not update_fields:
                return "Keine Aktualisierungsdaten vorhanden."

            sql_query = f"UPDATE Hardware SET {', '.join(update_fields)} WHERE ID = ?"
            parameters.append(id)
            logger.debug('sql query:'+str(sql_query))
            logger.debug('sql parameters:'+str(parameters))
            cur.execute(sql_query, parameters)
            con.commit()
        return "Hardware erfolgreich aktualisiert."
    except sqlite3.Error as e:
        return f"Fehler beim Aktualisieren der Hardware: {e.args[0]}"

def delete_hardware_by_id(id:int) -> str:
    """
        Löscht einen Hardware-Eintrag aus der Tabelle `Hardware.

        :param int id: eine Konstante zum Identifizieren des Datensatzes

        :return: Erfolgsmeldung oder Fehlerbeschreibung.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Hardware WHERE ID = ?", (id,))
            con.commit()
        return "Hardware-Eintrag wurde erfolgreich entfernt."
    except sqlite3.Error as e:
        return f"Fehler beim Entfernen des Hardware-Eintrags: {e.args[0]}"

###########################################################
# N U T Z E R R O L L E N - R E C H T E - E N D P U N K T #
###########################################################

def create_rolle(rolle:str, **rechte:dict[str,str]) -> str:
    """
        Fügt eine neue Nutzerrolle mit spezifischen Rechten in die Tabelle `NutzerrollenRechte` ein.
        Rollenrechte müssen damit nur noch angehangen werden

        :param str rolle:
        :param dict rechte:

        :return: Erfolgsmeldung oder Fehlerbeschreibung.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            columns = ', '.join(rechte.keys())
            placeholders = ', '.join(['?'] * len(rechte))
            values = list(rechte.values())
            cur.execute(f"INSERT INTO NutzerrollenRechte (Rolle, {columns}) VALUES (?, {placeholders})", [rolle] + values)
            con.commit()
        return "Nutzerrolle wurde erfolgreich erstellt."
    except sqlite3.Error as e:
        return f"Fehler beim Erstellen der Rolle: {e.args[0]}"


def read_all_rollen() -> list[dict[str,str]]:
    """
        Ruft alle Rollen aus der Tabelle `NutzerrollenRechte` ab.

        :return: eine Liste aller in der Datenbank gespeicherten Rollen.
            Die Rechte jeder Rolle werden jeweils in einem dictionary ausgegeben.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM NutzerrollenRechte")
            rows = cur.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        raise RuntimeError(f"Fehler beim Abrufen der Rollen: {e.args[0]}")

def delete_rolle(rolle:str) -> str:
    """
        Entfernt eine bestimmte Rolle aus der Tabelle `NutzerrollenRechte`.

        :param str rolle:

        :return: Erfolgsmeldung oder Fehlerbeschreibung.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM NutzerrollenRechte WHERE Rolle = ?", (rolle,))
            con.commit()
        return "Rolle wurde erfolgreich entfernt."
    except sqlite3.Error as e:
        return f"Fehler beim Entfernen der Rolle: {e.args[0]}"

def update_role(rolle: str, **rechte:str) -> str:
    """
        Aktualisiert die Rechte einer bestimmten Nutzerrolle in der Tabelle `NutzerrollenRechte`.
        Die Rechte werden als benannte Argumente übergeben (z.B. Column1=value1, Column2=value2).

        :param str rolle: die Rolle, deren Rechte aktualisiert werden sollen.
        :param rechte: die zu aktualisierenden Rechte als benannte Argumente.

        :return: Erfolgsmeldung oder Fehlerbeschreibung.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()

            # Dynamische Erstellung der SET-Klausel: Spaltennamen und Platzhalter
            columns = ', '.join([f"{col} = ?" for col in rechte.keys()])

            # Werte aus den benannten Argumenten (rechte)
            values = list(rechte.values())

            # SQL-Update-Abfrage
            cur.execute(f"UPDATE NutzerrollenRechte SET {columns} WHERE Rolle = ?", values + [rolle])

            # Änderungen in der Datenbank übernehmen
            con.commit()

        return "Nutzerrolle wurde erfolgreich aktualisiert."

    except sqlite3.Error as e:
        return f"Fehler beim Aktualisieren der Rolle: {e.args[0]}"

#######################################################
# A U S L E I H - H I S T O R I E - E N D P U N K T E #
#######################################################

def create_ausleih_historie(hardware_id:str, nutzername:str, ausgeliehen_am:str) -> str:
    """
        Erstellt einen neuen Eintrag in der Tabelle `Ausleih-Historie`.

        :param int hardware_id: Fremdschlüssel zur Hardware-Tabelle.
        :param str nutzername: Fremdschlüssel zur Benutzer-Tabelle.
        :param str ausgeliehen_am:können Ausleihdatum und Rückgabedatum angegeben werden.

        :return: Erfolgsmeldung oder Fehlerbeschreibung.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute(
                """
                INSERT INTO Ausleih_Historie(Hardware_ID, Nutzername, Ausgeliehen_am)
                VALUES (?, ?, ?)
                """,
                (hardware_id, nutzername, ausgeliehen_am)
            )
            con.commit()
            return "Eintrag in der Ausleih-Historie wurde erfolgreich erstellt."
    except sqlite3.Error as e:
        return f"Fehler beim Erstellen des Eintrags: {e}"

def fetch_ausleih_historie() -> list[dict[str, str]]|str:
    """
        Ruft alle Einträge aus der Tabelle `Ausleih-Historie` ab.

        :return: eine Liste von Dictionaries mit den Daten oder eine Fehlerbeschreibung.
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

def fetch_ausleih_historie_by_id(id:int) -> dict[str,str]|str|None:
    """
        Ruft einen spezifischen Eintrag der Tabelle `Ausleih-Historie` anhand der ID ab.

        :param int id: eine Konstante zum Identifizieren des Datensatzes

        :return: ein Dictionary mit der Ausleih-historie dieses Hardwareobjekts. None, falls der Eintrag nicht existiert, oder eine Fehlerbeschreibung.
    """
    try:
        with init_connection() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM Ausleih_Historie WHERE ID = ?", (id,))
            row = cur.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        return f"Fehler beim Abrufen des Eintrags: {e}"

def delete_ausleih_historie(id:int) -> str:
    """
         Löscht einen Eintrag aus der Tabelle `Ausleih-Historie` anhand der ID.

         :param int id: eine Konstante zum Identifizieren des Datensatzes.

         :return: Erfolgsmeldung oder Fehlerbeschreibung.
     """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Ausleih_Historie WHERE ID = ?", (id,))
            con.commit()
            return "Eintrag erfolgreich gelöscht."
    except sqlite3.Error as e:
        return f"Fehler beim Löschen des Eintrags: {e}"

#########################################
# R O O M _ I N F O - E N D P U N K T E #
#########################################

def create_room(raum:str, ort:str)->str:
    """
        Wird zum Erstellen von neuen Räumen benutzt

        :param str raum: (Raumname z.B. E220)
        :param str ort: (Ortsname z.B. Haus E 1. Etage)

        :return: Erfolgsmeldung oder Fehlerbeschreibung.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Room_Info(Raum, Ort) VALUES (?, ?)", (raum, ort))
            con.commit()
            return "Raum wurde erfolgreich erstellt."
    except sqlite3.Error as e:
        return f"Fehler beim Erstellen des Raumes: {e}"

def fetch_all_rooms() -> list[dict[str,str]] | str:
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

def search_room(raum:str) -> dict[str,str] | str:
    """
        :param str raum: (Raumname z.B. E220)

        :return: die Daten dieses einzelnen Raums aus
    """
    try:
        with init_connection() as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM Room_Info WHERE Raum = ?", (raum,))
            row = cur.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        return f"Fehler beim Suchen des Raumes: {e}"

def update_room(raum:str, neu_raum:str, neu_ort:str) -> str:
    """
        If Statement schaut nach, was genau geändert werden soll, if not zum absichern damit keine sachen auf NUll gesetzt werden
        Query zum updaten von zu updaten

        :param str raum: hier wird festgelegt welcher Primarykey angesprochen werden soll
        :param str neu_raum: die neue Value für Raum
        :param neu_ort: die neue Value für Ort

        :returns geänderter Wert:
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            update_fields = []
            parameters = []

            if neu_raum:
                update_fields.append("Raum = ?")
                parameters.append(neu_raum)
            if neu_ort:
                update_fields.append("Ort = ?")
                parameters.append(neu_ort)

            if not update_fields:
                return "Keine Aktualisierungsdaten vorhanden."

            sql_query = f"UPDATE Room_Info SET {', '.join(update_fields)} WHERE Raum = ?"
            parameters.append(raum)
            cur.execute(sql_query, parameters)
            con.commit()
            return "Raum erfolgreich aktualisiert."
    except sqlite3.Error as e:
        return f"Fehler beim Aktualisieren des Raumes: {e}"

def delete_room(raum:str)->str:
    """
        Funktion zum entfernen von Räumen, bitte nur verwenden wenn nötig.

        :param str raum:

        :return: Erfolgsmeldung oder Fehlerbeschreibung
    """
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Room_Info WHERE Raum = ?", (raum,))
            con.commit()
            return "Raum erfolgreich gelöscht."
    except sqlite3.Error as e:
        return f"Fehler beim Löschen des Raumes: {e}"

###########################################################
# A V A T A R _ I N F O R M A T I O N - E N D P U N K T E #
###########################################################

def upsert_avatar(nutzername:str, avatar_link:str) -> str:
    """
        Erstellt ein neues Avatar in der Datenbank.
        Wenn bereits ein Avatar mit dem gleichen Nutzername existiert,
        wird dieser gelöscht und durch den neuen Avatar ersetzt.

        :param str nutzername: Der Name des Nutzers.
        :param str avatar_link: Der Link zum Avatar des Nutzers.

        :return: Erfolgsmeldung oder Fehlerbeschreibung
    """
    try:
        with init_connection() as con:
            cur = con.cursor()

            # Optional: Delete the old entry explicitly
            cur.execute("DELETE FROM Avatar_information WHERE Nutzername = ?", (nutzername,))

            # Insert the new entry (this automatically replaces any existing entry)
            cur.execute("INSERT INTO Avatar_information (Nutzername, Avatar_link) VALUES (?, ?)",
                        (nutzername, avatar_link))

            con.commit()
            return "Avatar erfolgreich erstellt."
    except sqlite3.Error as e:
        return f"Fehler beim erstellen des Avatars: {e}"

def get_avatar_info(nutzername:str) -> dict[str, str]|None:
    """
        Holt die Avatar-Informationen für eine gegebene Avatar_id aus der Tabelle `Avatar_Informationen`.

        :param str nutzername:
        :return: Ein Dictionary mit den Avatar-Daten oder eine Fehlermeldung, falls keine Daten gefunden wurden.
    """
    try:
        with init_connection() as con:
            cur = con.cursor()

            # SQL-Abfrage, um Avatar-Informationen zu erhalten
            cur.execute("SELECT Nutzername, Avatar_link FROM Avatar_information WHERE Nutzername = ?", (nutzername,))

            # Einzeln abgerufene Zeile
            row = cur.fetchone()

            if row:
                # Wenn die Zeile gefunden wurde, als Dictionary zurückgeben
                return row[1]
            else:
                # Falls keine Zeile gefunden wird
                return None
    except sqlite3.Error:
        return None

######################################################
# A N W E N D U N G S - D A T E N - E N D P U N K T  #
######################################################

def __is_valid_application_data_entry(entry: dict[str, str]) -> bool:
    try:
        if not entry['']:
            return False
        if not entry[' ']:
            return False
    except KeyError:
        return False
    return True


def update_application_data(nutzername:str, property_name:str, value:str='') -> str:
    """
        :param str nutzername: Der Name des Nutzers.
        :param str property_name: Der Name der Einstellung.
        :param value:

        :return: Erfolgsmeldung oder Fehlerbeschreibung
    """
    data:dict[str,str]
    try:
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT Application_Data FROM Benutzer WHERE Nutzername = ?", (nutzername,))
            row: dict[str, str] = dict[str, str](cur.fetchone())
            try:
                data = json.loads(row['Application_Data'])
                data[property_name] = value
                cur.execute(f"""UPDATE Benutzer SET Application_Data = ? WHERE Nutzername = ?""",(json.dumps(data),nutzername,))
            except KeyError as e:
                print(e)
                return f"Fehler beim aktualisieren der Daten: {e}"
    except sqlite3.Error as e:
        print(e)
        return f"Fehler beim aktualisieren der Daten: {e}"
    return 'Daten erfolgreich aktualisiert.'


def get_application_data(nutzername:str, property_name:str) -> str | None:
    """
        :param str nutzername: Der Name des Nutzers.
        :param str property_name: Der Name der Einstellung.

        :return: Der in der Datenbank gespeicherte Wert
    """
    try:
        data: dict[str,str]
        with init_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT Application_Data FROM Benutzer WHERE Nutzername = ?", (nutzername,))
            row: dict[str, str] = dict[str, str](cur.fetchone())
            try:
                data = json.loads(row['Application_Data'])
            except KeyError as e:
                print(e)
                return f"Fehler beim aktualisieren der Daten: {e}"
        return data[property_name]
    except sqlite3.Error as e:
        print(e)
        return f"Fehler beim aktualisieren der Daten: {e}"