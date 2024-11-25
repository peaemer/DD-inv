from Datenbank.sqlite3api import *

def create_neue_benutzer():
    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Rolf", "#Anna456", "Rolf@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Maximal", "#Max789", "Maximal@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Daniel", "#Lisa321", "Daniel@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Toma", "#Tom654", "Toma@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Sophiar", "#Sophia987", "Sophiar@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Lukassas", "#Lukas112", "Lukassas@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Miathes", "#Mia223", "Miathes@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Jonathan", "#Jonas334", "Jonathan@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Clarana", "#Clara445", "Clarana@srhk.de"))

    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Felixius", "#Felix556", "Felixius@srhk.de"))

def create_neue_rolle():
    # Test für das Erstellen einer Rolle
    print("\n--- Test: Rolle erstellen ---")
    print(create_rolle(
        Rolle="SuperRolle",
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
    create_neue_benutzer()