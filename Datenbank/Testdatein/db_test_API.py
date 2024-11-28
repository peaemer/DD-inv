import os
from Datenbank.sqlite3api import *

def test_functions():
    print("Starte Tests...")

    # Test Benutzer-Funktionen
    print("\n--- Test Benutzer-Funktionen ---")
    print("Erstelle Benutzer...")
    print(create_benutzer("testuser", "password123", "testuser@example.com"))

    print("\nLese alle Benutzer...")
    benutzer = read_all_benutzer()
    print(benutzer)

    print("\nLese Benutzer 'testuser'...")
    benutzer_detail = read_benutzer("testuser")
    print(benutzer_detail)

    print("\nAktualisiere Benutzer 'testuser'...")
    print(update_benutzer("testuser", neues_passwort="newpassword456", neue_rolle="Admin"))

    print("\nLösche Benutzer 'testuser'...")
    print(delete_benutzer("testuser"))

    # Test Hardware-Funktionen
    print("\n--- Test Hardware-Funktionen ---")
    print("Erstelle Hardware...")
    print(create_hardware("1234-5678", "Laptop", "Dell XPS 13", "Keine", "Max", "Berlin"))

    print("\nLese alle Hardware-Einträge...")
    hardware = fetch_hardware()
    print(hardware)

    print("\nLese Hardware mit Service_Tag '1234-5678'...")
    hardware_detail = fetch_hardware_by_id("1234-5678")
    print(hardware_detail)

    print("\nAktualisiere Hardware '1234-5678'...")
    print(update_Hardware_by_service_tag("1234-5678", neue_Standort="München", neue_beschaedigung="Kratzer"))

    print("\nLösche Hardware mit Service_Tag '1234-5678'...")
    print(delete_Hardware_by_service_tag("1234-5678"))

    print("\nTests abgeschlossen.")

def test_rolle_functions():
    print("Starte Tests für Nutzerrollen-Funktionen...")

    # Test für das Erstellen einer Rolle
    print("\n--- Test: Rolle erstellen ---")
    print(create_Rolle(
        ANSEHEN=True,
        ROLLE_LOESCHBAR=True,
        ADMIN_FEATURE=True,
        LOESCHEN=True,
        BEARBEITEN=True,
        ERSTELLEN=True,
        GRUPPEN_LOESCHEN=True,
        GRUPPEN_ERSTELLEN=True,
        GRUPPEN_BEARBEITEN=True,
        ROLLEN_ERSTELLEN=True,
        ROLLEN_BEARBEITEN=True,
        ROLLEN_LOESCHEN=True
    ))

    # Test für das Abrufen aller Rollen
    print("\n--- Test: Alle Rollen abrufen ---")
    rollen = read_all_Rollen()
    print(rollen)

    # Test für das Abrufen einer bestimmten Rolle
    print("\n--- Test: Einzelne Rolle abrufen ---")
    rolle_detail = read_Rolle("test_rolle")
    print(rolle_detail)

    # Test für das Aktualisieren einer Rolle
    print("\n--- Test: Rolle aktualisieren ---")
    print(update_rolle(
        Rolle="test_rolle",
        neue_ROLLE_LOESCHBAR=False,
        neue_ADMIN_FEATURE=False,
        neue_ERSTELLEN=False
    ))

    # Test für das Löschen einer Rolle
    print("\n--- Test: Rolle löschen ---")
    print(delete_Rolle("test_rolle"))

    print("\nTests für Nutzerrollen-Funktionen abgeschlossen.")

def api_test_raum_info():
    print("-------------- Test: Raum erstellen --------------")
    print(create_room("TestRaum4", "TesGebäude, 1.Etage, Linker Flügel"))

    print("-------------- Test: Raumliste aufrufen --------------")
    print(fetch_all_rooms())

    print("-------------- Test: Raum aufrufen --------------")
    print(search_room("E220"))

    print("-------------- Test: Raum löschen -------------- ")
    print(delete_room("TestRaum4"))

    print("-------------- Test: Raum ändern --------------")
    print(update_room("E220","","Testbeschreibung"))

if __name__ == "__main__":
    api_test_raum_info()
