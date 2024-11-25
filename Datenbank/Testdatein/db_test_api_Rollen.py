from Datenbank.sqlite3api import *
def test_database_functions():
    """
    Testet alle CRUD-Operationen für Benutzer, Hardware und Rollen in der Datenbank.
    """
    print("Starte Tests für die Datenbank-Funktionen...\n")

    ##############################
    # T E S T S :   B E N U T Z E R
    ##############################
    print("=== Benutzer Tests ===")

    # Benutzer erstellen
    benutzername = "testuser"
    passwort = "testpass123"
    email = "testuser@example.com"
    print("1. Benutzer erstellen:")
    print(create_benutzer(benutzername, passwort, email))

    # Benutzer lesen
    print("\n2. Benutzer lesen:")
    benutzer_daten = read_benutzer(benutzername)
    print(benutzer_daten)

    # Alle Benutzer lesen
    print("\n3. Alle Benutzer lesen:")
    alle_benutzer = read_all_benutzer()
    print(alle_benutzer)

    # Benutzer aktualisieren
    neues_passwort = "newpass456"
    neue_email = "newemail@example.com"
    neue_rolle = "Admin"
    print("\n4. Benutzer aktualisieren:")
    print(update_benutzer(benutzername, neues_passwort, neue_email, neue_rolle))

    # Benutzer erneut lesen, um Änderungen zu prüfen
    print("\n5. Aktualisierte Benutzer-Daten:")
    benutzer_daten = read_benutzer(benutzername)
    print(benutzer_daten)

    # Benutzer löschen
    print("\n6. Benutzer löschen:")
    print(delete_benutzer(benutzername))

    # Prüfen, ob Benutzer gelöscht wurde
    print("\n7. Benutzer erneut lesen (sollte nicht existieren):")
    print(read_benutzer(benutzername))

    ##############################
    # T E S T S :   H A R D W A R E
    ##############################
    print("\n=== Hardware Tests ===")

    # Hardware erstellen
    service_tag = "HW123456"
    geraetetyp = "Laptop"
    modell = "Dell XPS 15"
    beschaedigung = "Keine"
    ausgeliehen_von = "Mitarbeiter A"
    standort = "Büro 1"
    print("1. Hardware erstellen:")
    print(create_hardware(service_tag, geraetetyp, modell, beschaedigung, ausgeliehen_von, standort))

    # Hardware lesen
    print("\n2. Hardware lesen:")
    hardware_daten = fetch_hardware_by_id(service_tag)
    print(hardware_daten)

    # Alle Hardware-Einträge lesen
    print("\n3. Alle Hardware lesen:")
    alle_hardware = fetch_hardware()
    print(alle_hardware)

    # Hardware aktualisieren
    neue_beschaedigung = "Display-Kratzer"
    neuer_standort = "Werkstatt"
    neue_ausleihe = "Mitarbeiter B"
    print("\n4. Hardware aktualisieren:")
    print(update_hardware_by_service_tag(service_tag, neue_ausleihe, neue_beschaedigung, neuer_standort))

    # Hardware erneut lesen, um Änderungen zu prüfen
    print("\n5. Aktualisierte Hardware-Daten:")
    hardware_daten = fetch_hardware_by_id(service_tag)
    print(hardware_daten)

    # Hardware löschen
    print("\n6. Hardware löschen:")
    print(delete_hardware_by_service_tag(service_tag))

    # Prüfen, ob Hardware gelöscht wurde
    print("\n7. Hardware erneut lesen (sollte nicht existieren):")
    print(fetch_hardware_by_id(service_tag))

    ##############################
    # T E S T S :   R O L L E N
    ##############################
    print("\n=== Rollen Tests ===")

    # Rolle erstellen
    rolle = "Testrolle"
    rechte = {
        "Lesen": True,
        "Schreiben": False,
        "Löschen": False
    }
    print("1. Rolle erstellen:")
    print(create_rolle(rolle, **rechte))

    # Alle Rollen lesen
    print("\n2. Alle Rollen lesen:")
    alle_rollen = read_all_rollen()
    print(alle_rollen)

    # Rolle löschen
    print("\n3. Rolle löschen:")
    print(delete_rolle(rolle))

    # Prüfen, ob Rolle gelöscht wurde
    print("\n4. Alle Rollen erneut lesen:")
    print(read_all_rollen())

    print("\nAlle Tests abgeschlossen!")


# Starte die Tests
if __name__ == "__main__":
    test_database_functions()
