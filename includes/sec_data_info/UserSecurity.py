from hashlib import sha512
import sys, os

from . import sqlite3api as db
from ..pages.Searchbar.Logging import Logger

sys.path.append(os.path.dirname(__file__) + r'\..')
from typing import Final

fallback_username: Final[str] = 'test'
fallback_password: Final[str] = 'password'

logger:Logger = Logger('UserSecurity')


def __hash_password(plain_password: str) -> bytearray:
    """
        hashes a plain password into a byte array using sha512 encryption

        :param str plain_password: the plain password that has to be hashed
    """
    return bytearray(sha512(plain_password.encode('utf-8')).digest())

def __is_invalid_name(name: str) -> bool:
    """
        a shortcut function for checking whether the supplied string is null or empty 

        :param str name: the name that has to be checked

        :return bool: whether the name is valid
    """
    return not name or name == ''


def __compare_password(plain_password: str, hashed_password: bytearray) -> bool:
    """
        compares a plain with an already hashed password

        :param str plain_password: the plain password that has to be compared
        :param bytearray hashed_password: the already hashed password that has to be compared

        :return bool: whether the plain password matches the already hashed one after the plain password was hashed
    """
    #hash the plain password and check if the hash is equal to the given
    return hashed_password == str(__hash_password(plain_password))


def hash_password(plain_password: str) -> str:
    """
        hashes a given password and returns the hash formatted as a string

        :param str plain_password: the plain password that has to be hashed

        :return string: the hashed and formatted string
    """
    if __is_invalid_name(plain_password):
        raise Exception('invalid password')
    return str(__hash_password(plain_password))


def verify_user(username: str, plain_password: str) -> bool:
    """
        searches for the user in the table of the database
        if the user exists, hashes the supplied plain password and compares it to the stored one

        :param str username: the name of the user whoes password should be verifyed
        :param str plain_password: the password that is expected to be stored in the database

        :return bool: whether the plain password matches the stored one after the plain password was hashed
    """

    benutzer = db.read_benutzer(username)
    try:
        if benutzer:
            # Check if the supplied password matches the stored hash
            if __compare_password(plain_password, benutzer['Passwort']):
                logger.debug(f'User {username} was successfully verified.')
                return True
            else:
                logger.debug("Incorrect password.")
                return False
        else:
            logger.debug(f"User '{username}' was not found.")
            return False
    except RuntimeError:
        logger.debug(f"User '{username}' was not found.")
        return False


def set_password(username:str, new_password:str, confirm_password:str) -> None:
    """
        checks whether both passwords are the same.
        if the password are the same, hashes the new password and overwrites the users password inside the database.

        :param str username: the name of the user whoes password should be verifyed
        :param str new_password: the new password that the user wants to set
        :param str confirm_password: has to be the same as new_password
    """

    if __is_invalid_name(new_password):
        return
    if __is_invalid_name(confirm_password):
        return
    hashed_password = __hash_password(new_password)
    if new_password != confirm_password:
        logger.debug(f"""passwords "{hashed_password}" and "{hash_password(confirm_password)}" don't match.""")
        return
    try:
        if db.update_benutzer(username, neues_passwort=str(hashed_password)) != 'Benutzer erfolgreich aktualisiert':
            logger.error(f"""failed to update password "{hashed_password}" for user "{username}" """)
    except RuntimeError:
        logger.debug(f"User '{username}' was not found.")