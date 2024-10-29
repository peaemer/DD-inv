from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)

# SQL-Datenbank konfigurieren --Nicht dran rumfummeln ist selber einfach kopiert ohne Ahnung
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Datenbank initialisierung
db.init_app(app)

with app.app_context():
    db.create_all() # damit werden die Tabellen nach dem Blueprint ind models.py erstellt falls die noch nicht vorhanden sind


#####################################
# API-Endpunkt für Tabelle "Nutzer" #
#####################################

# GET Operation -damit werden alle Nutzer abgerufen die in der Datenbank verfügbar sind
@app.route('/api/nutzer', methods=['GET'])
def get_nutzer():
    nutzer = Benutzer.query.all()
    return jsonify([{'Nutzername': n.Nutzername, 'Email': n.Email, 'Rolle': n.Rolle} for n in nutzer])

# POST Operation -damit werden neue Nutzer hinzugefügt
@app.route('/api/nutzer', methods=['POST'])
def create_nutzer():
    data = request.get_json()
    neuer_nutzer = Benutzer(
        Nutzername=data['Nutzername'],
        Passwort=data['HASHWERT'],    # @Alex bitte hier hashwert für verschlüsselung anwenden
        email=data['Email'],
        Rolle=data['Rolle', 'User']
    )