from Datenbank.sqlite3api import *

def create_neue_benutzer():
    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Anna", "#Anna456", "Anna@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Max", "#Max789", "Max@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Lisa", "#Lisa321", "Lisa@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Tom", "#Tom654", "Tom@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Sophia", "#Sophia987", "Sophia@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Lukas", "#Lukas112", "Lukas@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Mia", "#Mia223", "Mia@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Jonas", "#Jonas334", "Jonas@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Clara", "#Clara445", "Clara@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Felix", "#Felix556", "Felix@srhk.de"))

def create_neue_rolle():
    # Test für das Erstellen einer Rolle
    print("\n--- Test: Rolle erstellen ---")
    print(create_rolle(
        Rolle="Test-Rolle",
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


if __name__ == '__main__':
    create_neue_rolle()