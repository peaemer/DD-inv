import sqlite3
from hashlib import sha512

def hash_password(plain_password:str)->bytearray:
    """
        hashes a plain password into a byte array using sha512 encryption

        Parameters
        ----------
        :param str plain_password: the plain password that has to be hashed
    """
    return sha512(plain_password.encode('utf-8')).digest()