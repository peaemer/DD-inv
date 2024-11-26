import sys, os
sys.path.append(os.path.dirname(__file__)+'\..')
from Datenbank.sqlite3api import read_benutzer_rolle

print(read_benutzer_rolle('Alex'))