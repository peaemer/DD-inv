from hashlib import sha512
import sqlite3
from sqlite3 import Connection as SqlConnection

class UserSecurity:

    DEBUG_MODE:bool = True
    initial_database_name:str = "database.db"
    initial_table_name:str = "user"

    @staticmethod
    def hash_password(plain_password:str)->bytearray:
        """
            hashes a plain password into a byte array using sha512 encryption

            Parameters
            ----------
            :param str plain_password: the plain password that has to be hashed
        """
        return sha512(plain_password.encode('utf-8')).digest()
    
    def __connect(self, _database_name:str=initial_database_name)->sqlite3.Connection:
        """
            a shortcut function for getting a cursor to the supplied database and the supplied table
            if arguments are missing, use the data of this UserSecurity object

            Parameters
            ----------
            :param str _database_name: the name of the database for which the cursor has to be created
        """
        if(not _database_name):
            _database_name = self.initial_database_name
        return sqlite3.Connection(_database_name)
    
    def __init__(self, _database_name:str='database.db', _table_name:str='user'):
        """
            initializes the database name and the table name of the user data for the new object 

            Parameters
            ----------
            :param str _database_name: the name of the database where the table should be created, uses the stored name of the object if not supplied
            :param str _table_name: the name of the table where the user data should be stored, uses the stored name of the object if not supplied
        """
        self.initial_database_name = _database_name
        self.initial_table_name = _table_name

    def createTable(self, supplied_database_name:str = initial_database_name, supplied_table_name:str = initial_table_name)->None:
        """
            creates a table with the supplied name in the supplied database the fields 'id', 'username' and 'password_hash'

            Parameters
            ----------
            :param str _database_name: the name of the database where the table should be created, uses the stored data of the object if no addditional data is supplied
            :param str _table_name: the name of the table where the user data should be stored, uses the stored data of the object if no addditional data is supplied
        """
        try:
            #open a connectionn to the supplied database
            connection:SqlConnection = self.__connect(supplied_database_name)
            #create a cursor to the database of the connection
            cursor = connection.cursor()
            #create a table withe the supplied name and the  the columns 'id', 'username' and 'password_hash'
            cursor.execute(
                    #make sure that the table does not exist in the database so far
                    #id increments automatically for each new record
                    #each username in the table has to be unique and not empty
                    #the hashed password cannot be empty
                    '''CREATE TABLE IF NOT EXISTS ? (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL
                    )''',
                    (supplied_table_name)
            )
        except:
            if(self.DEBUG_MODE==True):print(f'table {supplied_table_name} exists already')
        finally:
            connection.close
    
    def compare_password(self, plain_password:str, hashed_password:bytearray)->bool:
        """
            compares a plain with an already hashed password

            Parameters
            ----------
            :param str plain_password: the plain password that has to be compared
            :param bytearray hashed_password: the already hashed password that has to be compared

            Return
            ------
            :return bool: whether the plain password matches the already hashed one after the plain password was hashed
        """
        #hash the plain password and check if the hash is equal to the given
        return hashed_password == UserSecurity.hash_password(plain_password)
    
    def add_user(self, username:str, password:str, _database_name:str=None, _table_name:str=None):
        """
            checks if an entry for the given user exists in the user table of the database of the connection
            if it doesn't, creates a new entry for the given user with the hash of the supplied password

            Parameters
            ----------
            :param str username: the name of the user who should be added to the database
            :param str password: the plain password that will be hashed and stored as the new user's initial password
            :param sqlite3.Connection connection: a connection to the database where the user's data should be stored
        """
        #open a connection to the database and 
        connection:SqlConnection = self.__connect(_database_name)
        cursor = connection.cursor()

        # Insert the new user into the table
        try:
            cursor.execute("INSERT INTO ? (username, password_hash) VALUES (?, ?)", (_table_name,username, UserSecurity.hash_password(password)))
            connection.commit()
            if(self.DEBUG_MODE==True):print(f"User '{username}' added successfully.")
        except sqlite3.IntegrityError:
            if(self.DEBUG_MODE==True):print(f"Error: User '{username}' already exists.")
        finally:
            # Close the database connection
            connection.close()

    def verify_user(self, username:str, plain_password:str, _database_name:str=initial_database_name, _table_name:str=initial_table_name)->bool:
        """
            searches for the user in the table of the cursor
            if the user exists, hashes the supplied plain password and compares it to the stored one 

            Parameters
            ----------
            :param str user_name: the name of the user whoes password should be verifyed
            :param str plain_password: the password that is expected to be stored in the database
            :param sqlite3.Connection connection: a connection to the database where the user data is stored
            :param str table_name: the name of the table where the user data is stored

            Return
            ------
            :return bool: whether the plain password matches the stored one after the plain password was hashed
        """

        try:
            #open a connnection to the database
            connection:SqlConnection = SqlConnection(_database_name, _table_name)
            cursor = connection.cursor()
            #read the hashed password from the record with the supplied username
            cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username))
            result = cursor.fetchone()

            if result:
                # Check if the provided password matches the stored hash
                if self.compare_password(plain_password,result[0]):
                    if(self.DEBUG_MODE==True):print(f'[UserSecurity]: user {username} was successfully verified.')
                    return True
                else:
                    if(self.DEBUG_MODE==True):print("[UserSecurity]: Incorrect password.")
                    return False
            else:
                if(self.DEBUG_MODE==True):print(f"[UserSecurity]: user '{username}' was not found.")
                return False
        except:
            pass
        finally:
            connection.close

UserSecurity().createTable()
us:UserSecurity = UserSecurity('test.db', 'bla')
us.createTable()
us.add_user('TestUser','password')