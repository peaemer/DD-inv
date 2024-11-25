from Datenbank.sqlite3api import *

def create_self():
    print("-------Benutzer wird erstellt-------")
    print(create_benutzer("Ralf","#Ralf123","Ralf@srhk.de"))

if __name__ == '__main__':
    create_self()