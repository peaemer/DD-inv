import numbers
import random
import sys, os
from random import Random
import json

import string
from typing import Final

from hashlib import sha512

import main
from main import config_manager
from . import sqlite3api as db
#from main import config_manager as cm
from includes.util.Logging import Logger
from ..util.ConfigManager import Configuration, ConfigManager

sys.path.append(os.path.dirname(__file__) + r'\..')

fallback_username: Final[str] = 'test'
fallback_password: Final[str] = 'password'

SPECIAL_CHARACTERS:Final[list[str]] = [
    '_', '-', ',', '.', '!', '§', '$', '%', '&', '/', '(', ')', '=','?', '+', '#', '~', "'", '<', '>', '|', '°', '^'
]
CAPITAL_LETTERS:Final[list[str]] = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
]
LOWER_LETTERS:Final[list[str]] = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
]
NUMBERS:Final[list[str]] = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
]

logger:Logger = Logger('UserSecurity')


def __hash_password(plain_password: str) -> bytes:
    """
        hashes a plain password into a byte array using sha512 encryption

        :param str plain_password: the plain password that has to be hashed
    """
    return sha512(plain_password.encode('utf-8')).digest()

def __is_invalid_name(name: str) -> bool:
    """
        a shortcut function for checking whether the supplied string is null or empty 

        :param str name: the name that has to be checked

        :return bool: whether the name is valid
    """
    return not name or name == ''


def __compare_password(plain_password: str, hashed_password: bytearray|str) -> bool:
    """
        compares a plain with an already hashed password

        :param str plain_password: the plain password that has to be compared
        :param bytearray hashed_password: the already hashed password that has to be compared

        :return bool: whether the plain password matches the already hashed one after the plain password was hashed
    """
    #hash the plain password and check if the hash is equal to the given
    return hashed_password == str(__hash_password(plain_password))


def __contains(chars:list[str], password:str) -> bool:
    """
        iterates over the array of chars and checks if it's inside the password
        :param list[str] chars:
        :param str password:

        :return: whether at least one of the chars was inside the password
    """
    logger_:Logger = Logger.from_logger(logger,'__contains')
    inside:bool = False
    for char in chars:
        if char in password:
            logger_.debug_e(f"character '{char}' is inside the password")
            inside = True
            break
        else:
            logger_.debug_e(f"character '{char}' is not inside the password")
    if not inside:
        logger_.debug_e(f"none of the characters in list '{chars}' was inside the password")
    return inside


def check_password_requirements(new_password:str) -> str|None:
    """
        gets the password rules that every new password has to follow from the config and checks
        whether at least on of each of the required characters is inside the new password

        :param str new_password:

        :return: an error message why the password doesn't follow the rules
    """

    #config:Configuration = cm.generate_configuration('Regeln fuer neue Passwoerter')
    config = config_manager.generate_configuration('Regeln fuer neue Passwoerter')
    if config.read_parameter('Sonderzeichen', generate_if_missing = True, gen_initial_value = 'True') == 'True':
        logger.debug(f"""special characters {config.read_parameter('Sonderzeichen')} required""")
        if not __contains(SPECIAL_CHARACTERS, new_password):
            return 'Das Passwort muss mindestens\nein Sonderzeichen enthalten!'
    if config.read_parameter('Zahlen', generate_if_missing = True, gen_initial_value = 'True') == 'True':
        logger.debug(f"""numbers {config.read_parameter('Zahlen')} required""")
        if not __contains(NUMBERS, new_password):
            return 'Das Passwort muss mindestens\neine Ziffer enthalten!'
    if config.read_parameter('Grossbuchstaben', generate_if_missing = True, gen_initial_value = 'True') == 'True':
        logger.debug(f"""capital letters {config.read_parameter('Grossbuchstaben')} required""")
        if not __contains(CAPITAL_LETTERS, new_password):
            return 'Das Passwort muss mindestens\neinen Großbuchstaben enthalten!'
    if config.read_parameter('Kleinbuchstaben', generate_if_missing = True, gen_initial_value = 'True') =='True':
        logger.debug(f"""lower letters {config.read_parameter('Kleinbuchstaben')} required""")
        if not __contains(LOWER_LETTERS, new_password):
            return 'Das Passwort muss mindestens\neinen Kleinbuchstaben enthalten!'
    if not len(new_password) >= int(config.read_parameter('Laenge', generate_if_missing = True, gen_initial_value = '4')):
        logger.debug(f"""len {config.read_parameter('Laenge')} required""")
        return f"""Das Passwort muss mindestens {int(config.read_parameter('Laenge', generate_if_missing = True, gen_initial_value = '4'))} Zeichen lang sein!"""
    return None


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

        :param str username: the name of the user whose password should be verified
        :param str plain_password: the password that is expected to be stored in the database

        :return bool: whether the plain password matches the stored one after the plain password was hashed
    """
    benutzer = db.read_benutzer(username)
    logger_:Logger = Logger.from_logger(logger,'verify user')
    logger_.debug(f"database password: {benutzer['Passwort'] if benutzer else 'null'}, entered password: {__hash_password(plain_password)}")
    try:
        if benutzer:
            # Check if the supplied password matches the stored hash
            if __compare_password(plain_password, benutzer['Passwort']):
                logger_.debug(f"User {username} was successfully verified.")
                return True
            else:
                logger_.error("Incorrect password.")
                return False
        else:
            logger_.error(f"User '{username}' was not found.")
            return False
    except RuntimeError:
        logger_.error(f"User '{username}' was not found.")
        return False


def generate_password() -> str:
    """
        generates a new password with the rules that are defined inside the config file

        :return: the new password
    """
    new_password = ''
    config = config_manager.generate_configuration('Regeln fuer neue Passwoerter')
    required_len:int = int(config.read_parameter('Laenge', generate_if_missing = True, gen_initial_value = '8'))
    while len(new_password) < required_len:
        rd:int = random.randint(1,4)
        if rd == 1:
            new_password += NUMBERS[random.randint(0,len(NUMBERS)-1)]
        elif rd == 2:
            new_password += CAPITAL_LETTERS[random.randint(0,len(CAPITAL_LETTERS)-1)]
        elif rd == 3:
            new_password += LOWER_LETTERS[random.randint(0,len(LOWER_LETTERS)-1)]
        elif rd == 4:
            new_password += SPECIAL_CHARACTERS[random.randint(0,len(SPECIAL_CHARACTERS)-1)]
    if not check_password_requirements(new_password):
        generate_password()
    logger.debug(f'generated password: {new_password}')
    return new_password


def set_password(username:str, new_password_: str | None, confirm_password: str | None, randomize_password:bool = False) -> str | None:
    """
        checks whether both passwords are the same and valid.
        if the password are the same, hashes the new password and overwrites the users' password inside the database.

        :param str username: the name of the user whose password should be changed
        :param str new_password_: the new password that the user wants to set
        :param str confirm_password: has to be the same as new_password
        :param bool randomize_password: whether to chose 8 random letters or numbers as the new password
    """
    new_password:str = ''
    hashed_new_password:bytes = bytes(0x0)
    if randomize_password:
        new_password:str = generate_password()
        hashed_new_password = __hash_password(new_password)
    else:
        if __is_invalid_name(new_password_):
            logger.error(f"""password "{new_password_}" is an invalid password""")
            return None
        if __is_invalid_name(confirm_password):
            logger.error(f"""confirmation password "{confirm_password}" is an invalid password""")
            return None
        if new_password_ != confirm_password:
            logger.error(f"""passwords "{str(new_password_)}" and "{str(confirm_password)}" don't match""")
            return None
        new_password = new_password_
        hashed_new_password = __hash_password(new_password)

    logger.debug(f"""new password is: "{new_password}" """)
    logger.debug(f"""hashed password is: "{hashed_new_password}" """)

    try:
        logger.debug(f"updating password of user {username} to {str(hashed_new_password)}")
        if db.update_benutzer(username, neues_passwort=str(hashed_new_password)) != 'Benutzer erfolgreich aktualisiert.':
            logger.error(f"""failed to update password "{hashed_new_password}" for user "{username}" """)
        else:
            logger.debug(f"""password "{hashed_new_password}" was updated successfully.""")
            logger.debug(f"""reloaded password is "{str(db.read_benutzer(username)['Passwort'])}" """)
            return new_password
    except RuntimeError:
        logger.error(f"User '{username}' was not found.")
    return None