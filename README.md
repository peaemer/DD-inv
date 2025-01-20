# DD-inv

![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white)![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Windows XP](https://img.shields.io/badge/Windows%20xp-003399?style=for-the-badge&logo=windowsxp&logoColor=white)<a href="https://ko-fi.com/dd_inv" target="_blank">
  <img src="https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white" alt="Ko-Fi"></a>

## Einführung

**DD-inv** (Doomsday-Inventar) ist ein Inventarisierungstool, das im Rahmen der Ausbildung der FI24 entwickelt wird. Es soll die Verwaltung und Organisation von Inventargegenständen, wie Pheriphere oder Laptops erleichtern. Daher bietet das Tool eine intuitive Benutzeroberfläche sowie eine robuste Datenbankanbindung.

Das Projekt befindet sich derzeit in der **Entwicklung** und wird kontinuierlich durch Funktionen erweitert.. 

## Funktionen

- [x] **Inventarverwaltung**<br/> Hinzufügen, Bearbeiten und Löschen von Einträgen im Inventar. Dazu können Details zum jeweiligen Eintrag eingesehen werden, u.a. Ausgeliehen von..., Beschädigungen..., oder Typ.
- [x] **Such- und Filterfunktionen**<br/> Intelligente Suche und Filteroptionen für Inventargegenstände. Darüberhinaus eine Suchhistorie. Speicherung sowie Autofill in der Suchleiste.
- [x] **Login Funktion**<br/> Jeder Nutzer hat seinen eigenen Login mit individuellen Einstellungen. 
- [x] **Benutzerverwaltung**<br/> Unterstützung für die Benutzerrollen Admin, User und Gast. Dazu können mehrere Nutzerrollen erstellt und individuell angepasst werden. 
- [x] **Admin Funktionen**<br/> Erstellen sowie Verwalten von Nutzern, Räumen und Rollen. Dazu einsehen und ändern an Einträgen.
- [x] **Datenexport**<br/> Export von Inventardaten in CSV- und andere Formate möglich.
- [x] **Statistiken**<br/> Anzeige von Statistiken und Berichten zum Inventar. Zum Beispiel einer Ausleihistorie der jeweiligen Benutezr.
- [x] **Design**<br/> Setzen eines Profilbildes für den jeweilgen Benutzer.
- [x] **Einstellungen**<br/> Setzen einer benutzerdefinierten Auflösung. 

## Voraussetzungen

> [!TIP]
> Falls du unseren Sourcecode verändern oder ansehen möchtest empfehlen wir dir eine Entwicklungsumgebung (IDE) wie [PyCharm](https://www.jetbrains.com/de-de/pycharm/) oder [Visual Studio Code](https://code.visualstudio.com/).

[**Python 3.10+**](https://www.python.org/downloads/windows/)<br/>
[**SQLite 3**](https://www.sqlite.org/) (Standardmäßig integriert, andere Datenbanken werden optional unterstützt)<br/>
[**Pip**](https://pypi.org/project/pip/) zur Verwaltung von Abhängigkeiten, wie PIL, CTK, etc.<br/>
[**tkinter**](https://docs.python.org/3/library/tkinter.html) / [**customtkinter**](https://customtkinter.tomschimansky.com/) / [**Figma**](https://www.figma.com/) zum erstellen der GUI

## Installation und Ausführung

**Repository klonen**
   ```bash
   git clone https://github.com/peaemer/DD-inv.git
   cd DD-inv
   `````````
   
## Geplante Funktionen

- [ ] **Portable version** Datenbank soll ohne installation überall auf Standard geräten nutzbar sein.<br/>
- [ ] **Design** Anapssen des Hintergrundes der App sowie der Farbe.<br/>
- [ ] **System** Anpassen der Auflösung in den Einstellungen sowie der größe des Inhalts.<br/> 
- [ ] **Datenbank** Einbinden der Datenbank in die App.
- [ ] **Einstellungen** Ändern der Zoomstufe des Inhaltes der Apps. 

## Projektstatus

> [!WARNING]
> Diese Projekt wird aktiv durch die **FI24** weiterentwickelt und ist noh nicht komplett ausgereift. Der Aktuelle Build ist eine **BETA**.

## Dokumentationen

- [GUI Dokumentation & Anleitung](https://docs.google.com/document/d/1cw-v-YGeTcAKWmvS_XI-Pzev7BLqxlVeBSGfPffx408/edit?tab=t.0#heading=h.vyzxfk53efur)
- [Datenbank Dokumentation](https://docs.google.com/document/d/1JMGLcfbs8KzxF_zfKBePersd-7iInHD2hQcOE3sAdLk/edit?tab=t.0#heading=h.nhkrx8i5d2i6)
- [Backend Dokumenatation](https://docs.google.com/document/d/1rMJOXEmr451v6wGJ2xgywId04x6mYY_t/edit?usp=sharing&ouid=113027422610141400771&rtpof=true&sd=true)
- [Dokumentation über Sicherheit]()

## FAQ

- **Wie kann ich mein Passwort ändern?**<br/> Ja. Öffne dazu das Inventariesierungstool und logge dich mit deinem Namen und Passwort ein. Drücke anschließdend in der rechten oberen Ecke auf dein Profilbild (Insofern keiens gesetzt ist es ein "A"). Dort wird dier nach dem öffnenen ein Feld "Passwort ändern" angezeigt. Klicke darauf und folge den Anweisungen im neuen geöffnetem Fenster. 
- **Was passiert, wenn ich mein Passwort während des Logins nicht mehr weiß?**<br/> Falls du dein Passwort vergessen haben solltest um dich in das Inventariesierungstool einzuloggen, melde dich bei deinem Zuständigen Gruppen Administrator um dein Passwort durch ihn ändern zu lassen. Sobald die Änderung erfolgt ist, logge dich erneut in dAS 
- **Wie kann ich ein Profilbild einfügen?**<br/> Um ein Profilbild einzufügen öffne das Inventariesierungstool. Logge dich mit deinem Benutzernamen und Passwort ein und naviegiere Anschließend in die Einstellungen.  (rechte obere Ecke auf dein Profilbild klicken (Insofern keiens gesetzt, ist es ein "A")). Dort gibt es die Überschrift "Profilbild-URL / Base64 eingeben". Trage unter diese Überschrift in das Feld die URL bzw. deinen [Base64-Text](https://base64.guru/converter/encode/image/png) ein.
- **Kann ich einfach so Administratorrechte erhalten?**<br/> Nein. Administratorrechten ist nur für den Gruppenadmin sowie für die Entwickler des Programmes vorgesehen. 
- **Wie kann ich eine Idee zum Inventartool weitergeben?**<br/> Hierfür gibt es mehrere Möglichkeiten. Entweder du gibst es an deinen Gruppenleiter weiter oder sendest eine [E-Mail an den Ersteller dieses Repositories](mailto:Jack-Mike.Saering@srhk.de).
- **Gibt es eine Anleitung, in welcher die Funktionen des Programmes genau beschrieben sind?**<br/> Ja. Schaue dafür in den Abschnitt Dokumentation über diesem FAQ. 

## Credits

Dieses Projekt wird von der **FI24** im Rahmen ihrer Ausbildung entwickelt. Mitwirkende sind:

[Peamer (Jack)](https://github.com/peaemer/)

[Alex5X5 (Alex)](https://github.com/Alex5X5)

[GitSchwan (Fabian)](https://github.com/GitSchwan)

[Chauto (Anakin)](https://github.com/Chautoo)

[FemRene (Rene)](https://github.com/FemRene)

[Tam Ngyuen]()

## Unterstüzt und Gefödert durch 

![srhHeader](https://github.com/user-attachments/assets/7592aeef-c2d3-40f3-b446-e0a64a8f632e)
