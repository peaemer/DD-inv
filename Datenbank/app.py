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
        Rolle=data['Rolle']
    )
    db.session.add(neuer_nutzer)
    db.session.commit()
    return jsonify({'message': 'Nutzer hinzugefügt'}), 201

# PUT Operation -damit werden bestehende Nutzer editiert
@app.route('/api/nutzer/<string:nutzername>', methods=['PUT'])
def update_nutzer(nutzername):
    nutzer = Benutzer.query.get(nutzername)
    if nutzer:
        data = request.get_json()
        nutzer.Email = data.get('Email', nutzer.Email)
        nutzer.Rolle = data.get('Rolle', nutzer.Rolle)
        db.session.commit()
        return jsonify({'message': 'Nutzer aktualisiert'})
    else:
        return jsonify({'message': 'Nutzer nicht gefunden'}), 404


# DELETE Operation -damit werden Nutzer gelöscht
@app.route('/api/nutzer/<string:nutzername>', methods=['DELETE'])
def delete_nutzer(nutzername):
    nutzer = Benutzer.query.get(nutzername)
    if nutzer:
        db.session.delete(nutzer)
        db.session.commit()
        return jsonify({'message': 'Nutzer wurde entfernt'})
    else:
        return jsonify({'message': 'Nutzer nicht gefunden'}), 404


#######################################
# API-Endpunkt für Tabelle "Hardware" #
#######################################


# GET Operation -damit werden alle Nutzer abgerufen die in der Datenbank verfügbar sind
@app.route('/api/hardware', methods=['GET'])
def get_hardware():
    hardware = Hardware.query.all()
    return jsonify([{'Service_Tag': h.Service_Tag, 'Gerätetyp': h.Gerätetyp, 'Modell': h.Modell, 'Standort': h.Standort} for h in hardware])

# POST Operation -damit werden neue Nutzer hinzugefügt
@app.route('/api/hardware', methods=['POST'])
def create_hardware():
    data = request.get.json()
    neue_hardware = Hardware(
        Service_Tag=data['Service_Tag'],
        Geraetetyp=data['Geraetetyp'],
        Modell=data['Modell'],
        Beschaedigung=data['Beschaedigung'],
        Ausgeliehen_von=data['Ausgeliehen_von'],
        Standort=data['Standort']
    )
    db.session.add(neue_hardware)
    db.session.commit()
    return jsonify({'message': 'Hardware hinzugefügt'}), 201


# PUT Operation -damit werden bestehende Nutzer editiert
@app.route('/api/hardware', methods=['PUT'])
def update_hardware():
    hardware = Hardware.query.all()
    if hardware:
        data = request.get_json()
        hardware.Modell = data.get('Modell', hardware.Modell)
        hardware.Standort = data.get('Standort', hardware.Standort)
        hardware.Beschaedigung = data.get('Beschaedigung', hardware.Beschaedigung)
        db.session.commit()
        return jsonify({'message': 'Hardware aktualisiert'})
    else:
        return jsonify({'error': 'Hardware nicht gefunden'}), 404