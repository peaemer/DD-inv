import os
from Datenbank.sqlite3api import *
def test_rolle_functions():
    print("Starte Tests für Nutzerrollen-Funktionen...")

    # Test für das Erstellen einer Rolle
    print("\n--- Test: Rolle erstellen ---")
    print(create_Rolle(
        ANSEHEN="True",
        ROLLE_LOESCHBAR="True",
        ADMIN_FEATURE="True",
        LOESCHEN="True",
        BEARBEITEN="True",
        ERSTELLEN="True",
        GRUPPEN_LOESCHEN="True",
        GRUPPEN_ERSTELLEN="True",
        GRUPPEN_BEARBEITEN="True",
        ROLLEN_ERSTELLEN="True",
        ROLLEN_BEARBEITEN="True",
        ROLLEN_LOESCHEN="True"
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
        neue_ROLLE_LOESCHBAR="False",
        neue_ADMIN_FEATURE="False",
        neue_ERSTELLEN="False"
    ))

    # Test für das Löschen einer Rolle
    print("\n--- Test: Rolle löschen ---")
    print(delete_Rolle("test_rolle"))

    print("\nTests für Nutzerrollen-Funktionen abgeschlossen.")

if __name__ == "__main__":
    test_rolle_functions()
