from hashlib import sha512
import sys, os
sys.path.append(os.getcwd()+'\..')
from typing import Final, List
from typing import Final, List
from Datenbank.sqlite3api import *
# from Datenbank.sqlite3api import read_benutzer, update_benutzer

#enables or disables debugging messages
DEBUG_MODE:bool = True

# __get_user_ptr = read_benutzer
# get_u_ptr = read_benutzer
# update_u_ptr = update_benutzer

fallback_username:Final[str] = 'test'
fallback_password:Final[str] = 'password'

def __hash_password(plain_password:str)->bytearray:
    '''
        hashes a plain password into a byte array using sha512 encryption

        Parameters
        ----------
        :param str plain_password: the plain password that has to be hashed
    '''
    return sha512(plain_password.encode('utf-8')).digest()

def __isInvalidName(name:str)->bool:
    '''
        a shortcut function for checking whether the supplied string is null or empty 

        Parameters
        ----------
        :param str _database_name: the name that has to be checked

        Return
        ------
        :return bool: whether the name is valid
    '''
    return name == None or name ==''

def __comparePassword(plain_password:str, hashed_password:bytearray)->bool:
    '''
        compares a plain with an already hashed password

        Parameters
        ----------
        :param str plain_password: the plain password that has to be compared
        :param bytearray hashed_password: the already hashed password that has to be compared

        Return
        ------
        :return bool: whether the plain password matches the already hashed one after the plain password was hashed
    '''
    #hash the plain password and check if the hash is equal to the given
    return hashed_password == __hash_password(plain_password)

def verifyUser(username:str, plain_password:str)->bool:
    '''
        searches for the user in the table of the database
        if the user exists, hashes the supplied plain password and compares it to the stored one 

        Parameters
        ----------
        :param str username: the name of the user whoes password should be verifyed
        :param str plain_password: the password that is expected to be stored in the database
        :param str _database_name: the name of the database 
        :param str table_name: the name of the table where the user data is stored

        Return
        ------
        :return bool: whether the plain password matches the stored one after the plain password was hashed
    '''

    benutzer = read_benutzer(username)
    try:
        if benutzer:
            # Check if the supplied password matches the stored hash
            if __comparePassword(plain_password,benutzer['hashed_password']):
                if(DEBUG_MODE==True):print(f'[UserSecurity]: user {username} was successfully verified.')
                return True
            else:
                if(DEBUG_MODE==True):print("[UserSecurity]: Incorrect password.")
                return False
        else:
            if(DEBUG_MODE==True):print(f"[UserSecurity]: user '{username}' was not found.")
            return False
    except:
        if(DEBUG_MODE==True):print(f"[UserSecurity]: user '{username}' was not found.")
        return False
    # except:
    #     pass

print(verifyUser('Alex','Alex!123'))
