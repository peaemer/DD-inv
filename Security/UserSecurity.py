from hashlib import sha512
import sqlite3
from sqlite3 import Connection as SqlConnection
from typing import Final, List
import warnings

class UserSecurity:

    #enables or disables debugging messages
    DEBUG_MODE:bool = True

    #define some values that are used if invalid parameters are passed to any method so that these parameters are nonull
    fallback_database_name:Final[str] = 'database.db'
    initial_database_name:str = fallback_database_name
    fallback_table_name:Final[str] = 'user'
    initial_table_name:str = fallback_table_name
    fallback_username:Final[str] = 'test'
    initial_username:str = fallback_username
    fallback_password:Final[str] = 'password'
    initial_password:str = fallback_password

    def __hash_password(self, plain_password:str)->bytearray:
        '''
            hashes a plain password into a byte array using sha512 encryption

            Parameters
            ----------
            :param str plain_password: the plain password that has to be hashed
        '''
        return sha512(plain_password.encode('utf-8')).digest()
    
    def __isInvalidName(self, name:str)->bool:
        '''
            a shortcut function for checking whether the supplied string is null or empty 

            Parameters
            ----------
            :param str _database_name: the name that has to be checked

            Return
            ------
            :return bool: whether the name is valid
        '''
        #return name == None or name ==''or not name.__class__ == str.__class__
        return name == None or name ==''
    
    def __pickDatabaseName(self, _database_name:str)->str:
        '''
            a shortcut function for deciding between the supplied string, this object's initial_database_name or
            the fallback_database_name as the file name of the database

            Parameters
            ----------
            :param str _database_name: the string that should be checked

            Return
            ------
            :return bool: which string was choosen
        '''
        return \
            self.fallback_database_name if self.__isInvalidName(_database_name) and self.__isInvalidName(self.initial_database_name) else \
            self.initial_database_name if (self.__isInvalidName(_database_name)) else \
            _database_name
    
    def __pickTableName(self, _table_name:str)->str:
        '''
            a shortcut function for deciding between the supplied string, this object's initial_table_name or
            the fallback_table_name as the name of the table

            Parameters
            ----------
            :param str _table_name: the string that should be checked

            Return
            ------
            :return str: which string was choosen
        '''
        return \
            self.fallback_table_name if self.__isInvalidName(_table_name) and self.__isInvalidName(self.initial_table_name) else \
            self.initial_table_name if (self.__isInvalidName(_table_name)) else \
            _table_name
    """
    def __connect(self, _database_name:str = '')->sqlite3.Connection:
        '''
            a shortcut function for opening a connection to the supplied database

            Parameters
            ----------
            :param str _database_name: the name of the database to which the connection has to be created

            Return
            ------
            :return sqlite3.Connection: a conection to the database with the given name
        '''
        return sqlite3.Connection(
           self.__pickDatabaseName(_database_name)
        )
    
    def __readDatabaseEntry(self, database_name:str, table_name:str, column_name:str, conditions:List[str] = [])->List[str]:
        '''
            reads an entry from the given table of the given database

            Parameters
            ----------
            :param List[str] conditions: a list of conditions for the qerrying of the result with the pattern 'variable = value'
        '''
        command:str = f"from {table_name} select {column_name}"
        if len(conditions)>0 :
            for condition in conditions:
                command += 'WHERE'
                command += condition
        if(self.DEBUG_MODE==True):print(f"[UserSecurity]: created command '{command}'")

    def __writeDatabaseEntry(database_name:str = '', table_name:str = '', )->str:
        
        pass
    """
    def __comparePassword(self, plain_password:str, hashed_password:bytearray)->bool:
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
        return hashed_password == UserSecurity.__hash_password(plain_password)

    """
    def createTable(self, _database_name:str = '', _table_name:str = '')->None:
        '''
            creates a table with the supplied name in the supplied database the fields 'id', 'username' and 'password_hash'

            Parameters
            ----------
            :param str _database_name: the name of the database where the table should be created, uses the stored data of the object if no addditional data is supplied
            :param str _table_name: the name of the table where the user data should be stored, uses the stored data of the object if no addditional data is supplied
        '''
        warnings.warn("This method may break the original structre of the supplied database",category=UserWarning,stacklevel=2)
        # return
        try:
            #open a connectionn to the supplied database
            connection:SqlConnection = self.__connect(_database_name)
            #create a cursor to the database of the connection
            cursor = connection.cursor()
            #create a table withe the supplied name and the  the columns 'id', 'username' and 'password_hash'
            cursor.execute(
                    #make sure that the table does not exist in the database so far
                    #id increments automatically for each new record
                    #each username in the table has to be unique and not empty
                    #the hashed password cannot be empty
                    f'''CREATE TABLE IF NOT EXISTS {self.__pickTableName(_table_name)} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL
                    )'''
            )
        except sqlite3.IntegrityError as e:
            if(self.DEBUG_MODE==True):print(f'table {self.__pickTableName(_table_name)} exists already')
        except Exception as e:
            print(e)
        finally:
            connection.close
    """
    def verifyUser(self, username:str, plain_password:str, _database_name:str='', _table_name:str='')->bool:
        '''
            searches for the user in the table of the database
            if the user exists, hashes the supplied plain password and compares it to the stored one 

            Parameters
            ----------
            :param str username: the n  ame of the user whoes password should be verifyed
            :param str plain_password: the password that is expected to be stored in the database
            :param str _database_name: the name of the database 
            :param str table_name: the name of the table where the user data is stored

            Return
            ------
            :return bool: whether the plain password matches the stored one after the plain password was hashed
        '''

        try:
            #open a connnection to the database
            connection:SqlConnection = self.__connect(_database_name)
            cursor = connection.cursor()
            #read the hashed password from the record with the supplied username
            cursor.execute(f'SELECT password_hash FROM {self.__pickTableName(_table_name)} WHERE username = ?', (username))
            connection.commit()
            result = cursor.fetchone()
            #check whether the user is stored in the database
            if result:
                # Check if the supplied password matches the stored hash
                if self.__comparePassword(plain_password,result[0]):
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
    
    def sudoAddUser(self, username:str, plain_password:str, _database_name:str='', _table_name:str=''):
        '''
            checks if an entry for the given user exists in the user table of the database of the connection
            if it doesn't, creates a new entry for the given user with the hash of the supplied password

            Parameters
            ----------
            :param str username: the name of the user who should be added to the database
            :param str password: the plain password that will be hashed and stored as the new user's initial password
            :param sqlite3.Connection connection: a connection to the database where the user's data should be stored
        '''
        try:
            connection:SqlConnection = self.__connect(_database_name)
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO {self.__pickTableName(_table_name)} (username, password_hash) VALUES (?, ?)",
                (username, self.__hash_password(plain_password))
            )
            connection.commit()
            if(self.DEBUG_MODE==True):print(f"[UserSecurity][addUser()]: User '{username}' added successfully")
        except sqlite3.IntegrityError as e:
            if(self.DEBUG_MODE==True):print(f"[UserSecurity][addUser()]: IntegrityError: {e}")

        finally:
            # Close the database connection
            connection.close()
    
    def addUser(self, username:str, plain_password:str, _database_name:str='', _table_name:str=''):
        '''
            checks if an entry for the given user exists in the user table of the database of the connection
            if it doesn't, creates a new entry for the given user with the hash of the supplied password

            Parameters
            ----------
            :param str username: the name of the user who should be added to the database
            :param str password: the plain password that will be hashed and stored as the new user's initial password
            :param sqlite3.Connection connection: a connection to the database where the user's data should be stored
        '''
        try:
            connection:SqlConnection = self.__connect(self.__pickDatabaseName(_database_name))
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO {self.__pickTableName(_table_name)} (username, password_hash) VALUES (?, ?)",
                (username, self.__hash_password(plain_password))
            )
            connection.commit()
            if(self.DEBUG_MODE==True):print(f"[UserSecurity][addUser()]: User '{username}' added successfully")
        except sqlite3.IntegrityError as e:
            if(self.DEBUG_MODE==True):print(f"[UserSecurity][addUser()]: IntegrityError: {e}")
        finally:
            # Close the database connection
            connection.close()

    def sudoModifyUserRights(self, username:str , _database_name:str = '', _table_name:str = '', right:str ='', state:str = 'True'):
        try:
            connection:SqlConnection = self.__connect(self.__pickDatabaseName(_database_name))
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO {self.__pickTableName(_table_name)} WHERE username = {username} (right, ) VALUES (?, ?)",
                (right, state)
            )
            connection.commit()
            if(self.DEBUG_MODE==True):print(f"[UserSecurity][sudoModifyUserRight()]: successfully set {right} of user {username} to {state}")
        except sqlite3.IntegrityError as e:
            if(self.DEBUG_MODE==True):print(f"[UserSecurity][sudoModifyUserRight()]: IntegrityError: {e}")
        except sqlite3.OperationalError as e:
            if(self.DEBUG_MODE==True):print(f"[UserSecurity][sudoModifyUserRight()]: OperationalError: {e}")
        finally:
            # Close the database connection
            connection.close()
    
    def modifyUserRights(
              self,
              executor_username:str, 
              executor_plain_password:str,
              affected_username:str,
              affected_right_name:str, 
              affected_right_state:str, 
              _database_name:str, 
              _table_name:str):
        if(self.verifyUser(executor_plain_password,executor_plain_password,_database_name,_table_name)==True):
            pass
    
    def __init__(self, _database_name:str=fallback_database_name, _table_name:str=fallback_table_name):
        '''
            initializes the database name and the table name of the user data for the new object 

            Parameters
            ----------
            :param str _database_name: the name of the database where the table should be created, uses the stored name of the object if not supplied
            :param str _table_name: the name of the table where the user data should be stored, uses the stored name of the object if not supplied
        '''
        self.initial_database_name = _database_name
        self.initial_table_name = _table_name


# us:UserSecurity = UserSecurity('test.db', 'user')
# us.createTable('test.db','user')
# us.sudoAddUser('TestUser2','passwort','test.db','user')
# us.addUser('TestUser','password','test.db','user')
# us.sudoModifyUserRights('TestUser','test.db','user','bla','True')
