"""
    .
"""
from includes.util.Logging import Logger
import webbrowser

logger:Logger = Logger('SettingsBindings')

def open_url(url:str):
    logger.debug(f'open url: {url}')
    webbrowser.open(url)

def load_user_email(nutzername):
    """
    Lädt die E-Mail-Adresse eines Benutzers aus der Datenbank.

    :param nutzername: Der Benutzername, dessen E-Mail abgerufen werden soll.
    :return: Die E-Mail-Adresse oder ein Fehlerhinweis.
    """
    from includes.sec_data_info.sqlite3api import read_benutzer
    try:
        benutzer_data = read_benutzer(nutzername)
        if benutzer_data and "Email" in benutzer_data:
            return benutzer_data["Email"]
        else:
            return "E-Mail nicht gefunden"
    except Exception as e:
        logger.error(f"Error while trying to load email: {e}")
        return "Error while loading the Email."