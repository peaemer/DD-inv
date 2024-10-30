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
    return jsonify([{'Nutzername': n.Nutzername,
                     'Email': n.Email,
                     'Rolle': n.Rolle}
                    for n in nutzer])

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
        return jsonify({'error': 'Nutzer nicht gefunden'}), 404


# DELETE Operation -damit werden Nutzer gelöscht
@app.route('/api/nutzer/<string:nutzername>', methods=['DELETE'])
def delete_nutzer(nutzername):
    nutzer = Benutzer.query.get(nutzername)
    if nutzer:
        db.session.delete(nutzer)
        db.session.commit()
        return jsonify({'message': 'Nutzer wurde entfernt'})
    else:
        return jsonify({'error': 'Nutzer nicht gefunden'}), 404


#######################################
# API-Endpunkt für Tabelle "Hardware" #
#######################################

# GET Operation -damit werden alle Hardware einträge eingetragen

@app.route('/api/hardware', methods=['GET'])
def get_hardware():
    hardware = Hardware.query.all()
    return jsonify([{'Service_Tag': h.Service_Tag,
                     'Gerätetyp': h.Gerätetyp,
                     'Modell': h.Modell,
                     'Standort': h.Standort}
                    for h in hardware])

# POST Operation -damit werden Hardware-Einträge hinzugefügt
@app.route('/api/hardware', methods=['POST'])
def create_hardware():
    data = request.get_json()
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


# PUT Operation -damit Hardware-Einträge editiert
@app.route('/api/hardware', methods=['PUT'])
def update_hardware():
    hardware = Hardware.query.all()
    if hardware:
        data = request.get_json()
        hardware.Modell = data.get('Modell', hardware.Modell)
        hardware.Standort = data.get('Standort', hardware.Standort)
        hardware.Beschaedigung = data.get('Beschaedigung', hardware.Beschaedigung)
        hardware.Ausgeliehen_von = data.get('Ausgeliehen_von', hardware.Ausgeliehen_von)
        db.session.commit()
        return jsonify({'message': 'Hardware aktualisiert'})
    else:
        return jsonify({'error': 'Hardware nicht gefunden'}), 404

# DELETE Operation -damit werden Hardware-Einträge gelöscht
@app.route('/api/hardware', methods=['DELETE'])
def delete_hardware(service_tag):
    hardware = Hardware.query.all()
    if hardware:
        db.session.delete(hardware)
        db.session.commit()
        return jsonify({'message': 'Hardware Eintrag geloscht'})
    else:
        return jsonify({'error': 'Hardware nicht gefunden'}), 404


#################################################
# API-Endpunkt für Tabelle "NutzerrollenRechte" #
#################################################

# GET Operation -damit werden alle Hardware einträge eingetragen
@app.route('/api/nutzerrechteRollen', methods=['GET'])
def get_nutzerrechteRollen():
    nutzerrechteRollen =  NutzerrollenRechte.query.all()
    return jsonify([{'Rolle': n.Rolle,
                     'ANSEHEN': n.ANSEHEN,
                     'ROLLEN_LOESCHBAR': n.ROLLEN_LOESCHBAR,
                     'ADMIN_FEATURE': n.ADMIN_FEATURE,
                     'LOESCHEN': n.LOESCHEN,
                     'BEARBEITEN': n.BEARBEITEN,
                     'ERSTELLEN': n.ERSTELLEN,
                     'GRUPPEN_LOESCHEN': n.GRUPPEN_LOESCHEN,
                     'GRUPPEN_ERSTELLEN': n.GRUPPEN_ERSTELLEN,
                     'GRUPPEN_BEARBEITEN': n.GRUPPEN_BEARBEITEN,
                     'ROLLEN_ERSTELLEN': n.ROLLEN_ERSTELLEN,
                     'ROLLEN_BEARBEITEN': n.ROLLEN_BEARBEITEN,
                     'ROLLEN_LOESCHEN': n.ROLLEN_LOESCHEN}
                    for n in nutzerrechteRollen])

# POST Operation -damit werden Rollen erstellt
@app.route('/api/nutzerrechteRollen', methods=['POST'])
def create_nutzerrechteRollen():
    data = request.get_json()
    neue_nutzerrechteRolle = Hardware(
        Rolle=data['Rolle'],
        ANSEHEN=data['ANSEHEN'],
        ROLLEN_LOESCHBAR=data['ROLLEN_LOESCHBAR'],
        ADMIN_FEATURE=data['ADMIN_FEATURE'],
        LOESCHEN=data['LOESCHEN'],
        BEARBEITEN=data['BEARBEITEN'],
        ERSTELLEN=data['ERSTELLEN'],
        GRUPPEN_LOESCHEN=data['GRUPPEN_LOESCHEN'],
        GRUPPEN_ERSTELLEN=data['GRUPPEN_ERSTELLEN'],
        GRUPPEN_BEARBEITEN=data['GRUPPEN_BEARBEITEN'],
        ROLLEN_ERSTELLEN=data['ROLLEN_ERSTELLEN'],
        ROLLEN_BEARBEITEN=data['ROLLEN_BEARBEITEN'],
        ROLLEN_LOESCHEN=data['ROLLEN_LOESCHEN']
    )
    db.session.add(neue_nutzerrechteRolle)
    db.session.commit()
    return jsonify({'message': 'Hardware hinzugefügt'}), 201


# PUT - Bestehende Rollen bearbeiten
@app.route('/api/nutzerrollenRechte', methods=['PUT'])
def update_nutzerrollenRechte():
    nutzerrechteRollen = NutzerrollenRechte.query.all()
    if nutzerrechteRollen:
        data = request.get_json()
        nutzerrechteRollen.Rolle = data.get('Rolle', nutzerrechteRollen.Rolle)
        nutzerrechteRollen.ANSEHEN = data.get('ANSEHEN', nutzerrechteRollen.ANSEHEN)
        nutzerrechteRollen.ROLLEN_LOESCHBAR = data.get('ROLLEN_LOESCHBAR', nutzerrechteRollen.ROLLEN_LOESCHBAR)
        nutzerrechteRollen.ADMIN_FEATURE = data.get('ADMIN_FEATURE', nutzerrechteRollen.ADMIN_FEATURE)
        nutzerrechteRollen.LOESCHEN = data.get('LOESCHEN', nutzerrechteRollen.LOESCHEN)
        nutzerrechteRollen.BEARBEITEN = data.get('BEARBEITEN', nutzerrechteRollen.BEARBEITEN)
        nutzerrechteRollen.ERSTELLEN = data.get('ERSTELLEN', nutzerrechteRollen.ERSTELLEN)
        nutzerrechteRollen.GRUPPEN_LOESCHEN = data.get('GRUPPEN_LOESCHEN', nutzerrechteRollen.GRUPPEN_LOESCHEN)
        nutzerrechteRollen.GRUPPEN_ERSTELLEN = data.get('GRUPPEN_ERSTELLEN', nutzerrechteRollen.GRUPPEN_ERSTELLEN)
        nutzerrechteRollen.GRUPPEN_BEARBEITEN = data.get('GRUPPEN_BEARBEITEN', nutzerrechteRollen.GRUPPEN_BEARBEITEN)
        nutzerrechteRollen.ROLLEN_ERSTELLEN = data.get('ROLLEN_ERSTELLEN', nutzerrechteRollen.ROLLEN_ERSTELLEN)
        nutzerrechteRollen.ROLLEN_BEARBEITEN = data.get('ROLLEN_BEARBEITEN', nutzerrechteRollen.ROLLEN_BEARBEITEN)
        nutzerrechteRollen.ROLLEN_LOESCHEN = data.get('ROLLEN_LOESCHEN', nutzerrechteRollen.ROLLEN_LOESCHEN)
        db.session.commit()
        return jsonify({'message': 'Rolle aktualisiert'})
    else:
        return jsonify({'error': 'Rolle nicht gefunden'}), 404


# DELETE Operation -damit werden Rollen gelöscht
def delete_nutzerrollenRechte(rolle):
    nutzerrollenRechte = NutzerrollenRechte.query.all()
    if nutzerrollenRechte:
        db.session.delete(nutzerrollenRechte)
        db.session.commit()
        return jsonify({'message': 'Rolle geloscht'})
    else:
        return jsonify({'error': 'Rolle nicht gefunden'}), 404

# Main loop
if __name__ == '__main__':
    app.run(debug=True)
