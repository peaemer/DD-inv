from flask_sqlalchemy import SQLAlchemy

# Datenbank von SQLLib initialising
db = SQLAlchemy()

# Für jede Tabelle muss eine Klasse erstellt werden mit den dazugehörigen

# Modell für die Nutzer Tabelle
class Benutzer(db.Model):
    __tablename__ = "Benutzer"
    Nutzername = db.Column(db.String, primary_key=True)
    Passwort = db.Column(db.String, nullable=False)
    Email = db.Column(db.String)
    Rolle = db.Column(db.String)

    #rolle = db.relationship("NutzerrollenRechte, backref="Benutzer")


# Modell für die Hardware Tabelle
class Hardware(db.Model):
    __tablename__ = "Hardware"
    Service_Tag = db.Column(db.String, primary_key=True)
    Geraetetyp = db.Column(db.String, nullable=False)
    Modell = db.Column(db.String, nullable=False)
    Beschaedigung = db.Column(db.String)
    Ausgeliehen_von = db.Column(db.String, db.ForeignKey('Benutzer.Nutzername'))
    Standort = db.Column(db.String, nullable=False)

    # Die Beziehung von Benutzer auf Nutzer herstellen -Muss vielleicht geändert werden
    nutzer = db.relationship("Benutzer", backref="Hardware")
