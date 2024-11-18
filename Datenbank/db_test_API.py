import os
from sqlite3api import (
    create_benutzer, read_all_benutzer, read_benutzer, update_benutzer, delete_benutzer,
    create_hardware, fetch_hardware, fetch_hardware_by_id, update_Hardware_by_service_tag, delete_Hardware_by_service_tag
)

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

if __name__ == "__main__":
    test_functions()
