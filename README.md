![ascii-text-art (2)](https://github.com/user-attachments/assets/c5ef3ba3-cc7c-4b30-83e2-1dbabcb4167e)

![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white)![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Windows XP](https://img.shields.io/badge/Windows%20xp-003399?style=for-the-badge&logo=windowsxp&logoColor=white)<a href="https://ko-fi.com/dd_inv" target="_blank">
  <img src="https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white" alt="Ko-Fi"></a>

## Einführung

**DD-inv** (Doomsday-Inventar) ist eine Inventarisierungssoftware, das im Rahmen der Ausbildung der FI24 entwickelt wird. Es soll die Verwaltung und Organisation von Inventargegenständen, wie Peripheriegeräte oder Laptops, erleichtern. Daher bietet das Tool eine intuitive Benutzeroberfläche sowie eine robuste Datenbankanbindung.

## Funktionen

- [x] **Portable** Die Anwendung kann, ohne installiert werden zu müssen, ausgeführt werden. 
- [x] **Inventarverwaltung**<br/> Hinzufügen, Bearbeiten und Löschen von Einträgen im Inventar. Dazu können Details zum jeweiligen Eintrag eingesehen werden, u.a. Ausgeliehen von..., Beschädigungen..., oder Typ.
- [x] **Such- und Filterfunktionen**<br/> Intelligente Suche und Filteroptionen für Inventargegenstände. Darüber hinaus eine Suchhistorie. Speicherung sowie Autofill in der Suchleiste.
- [x] **Login Funktion**<br/> Jeder Nutzer hat seinen eigenen Login mit individuellen Einstellungen. 
- [x] **Benutzerverwaltung**<br/> Unterstützung für die Benutzerrollen Admin, User und Gast. Dazu können mehrere Nutzerrollen erstellt und individuell angepasst werden. 
- [x] **Admin Funktionen**<br/> Erstellen sowie Verwalten von Nutzern, Räumen und Rollen. Dazu einsehen und ändern an Einträgen.
- [x] **Datenexport**<br/> Export von Inventardaten in CSV- und andere Formate möglich.
- [x] **Statistiken**<br/> Anzeige von Statistiken und Berichten zum Inventar. Zum Beispiel einer Ausleihhistorie der jeweiligen Benutzer.
- [x] **Design**<br/> Setzen eines Profilbildes für den jeweilgen Benutzer.
- [x] **Einstellungen**<br/> Setzen einer benutzerdefinierten Auflösung sowie vergrößern oder verkleinern des Inhaltes der App. Desweiteren ist ein DEBUG-Modus für Administratoren über die Einstellungen an- und ausschaltbar.  

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
**Inventarisierungssoftware herunterladen und installieren**
1. Gehe zu den Realeses in diesem Reposetorie.
2. Wähle dort den neuesten Build aus und lade dir die ZIP-Daei oder .exe herunter.
3. Ebenso lade dir die SQLite3 Datenbank herunter und sorge dafür, dass diese für alle im Netzwerk erreichbar ist, insofern gewünscht. Zum Beispiel durch ein Netzlaufwerk.
4. Öffne die .exe Datei mit einem Doppelklick darauf, um das Programm auszuführen. Die ZIP-Datei muss nicht extrahiert werden.
5. Versuche, dich einzuloggen, mit einem Namen und Passwort von deinem Administrator. Sobald das klappt, hast du das Programm erfolgreich installiert.
  > [!CAUTION]
  > Die Datenbank ist für das Ausführen der Inventarisierungssoftware exestiel. Sonst können keine Daten für den Login abgerufen oder Daten gespeichert werden! 
   
## Geplante Funktionen

- [ ] **Design** Anpssen des Hintergrundes der App sowie der Farbe (Darkmode).<br/>
- [ ] **Framework** Ggf. wird in Zukufnt das Framework von tk zu ctk geändert.<br/>

## Projektstatus

Das Projekt ist vorübergehend beendet, daher gibt es nur noch kleine Änderungen oder Erweiterungen. Die aktulle Version ist die 1.0 STABLE. 
In Zukunft könnte es die Möglichkeit geben, dass das Projekt vortgeführt wird durch eine andere Gruppe als der **FI24**. 

## Dokumentationen

- [GUI Dokumentation & Anleitung](https://docs.google.com/document/d/1cw-v-YGeTcAKWmvS_XI-Pzev7BLqxlVeBSGfPffx408/edit?tab=t.0#heading=h.vyzxfk53efur)
- [Datenbank Dokumentation](https://docs.google.com/document/d/1JMGLcfbs8KzxF_zfKBePersd-7iInHD2hQcOE3sAdLk/edit?tab=t.0#heading=h.nhkrx8i5d2i6)
- [Backend-Dokumentation](https://docs.google.com/document/d/1rMJOXEmr451v6wGJ2xgywId04x6mYY_t/edit?usp=sharing&ouid=113027422610141400771&rtpof=true&sd=true)
- [Dokumentation über Sicherheit](https://docs.google.com/document/d/1-MB4UqDj65UzecfNWrAu0PTTA-Bzxx89sGWgj5ZKcxw/edit?tab=t.0#heading=h.kk4ig0v6talh)

## FAQ

- **Wie kann ich die Inventarisierungssoftware herunterladen und installieren?**<br/> Das Tool kann direkt [hier über das Repositorie](https://github.com/peaemer/DD-inv/releases/latest) heruntergeladen werden. Bitte schaue dafür auch in den Bereich "Installation und Ausführung" für genauere Anweisungen. 
- **Wie kann ich mein Passwort ändern?**<br/> Ja. Öffne dazu die Inventarisierungssoftware und logge dich mit deinem Namen und Passwort ein. Drücke anschließend in der rechten oberen Ecke auf dein Profilbild (insofern keins gesetzt ist, ist es ein graues Profilbild). Dort wird dir nach dem Öffnen ein Feld "Passwort ändern" angezeigt. Klicke darauf und folge den Anweisungen im neu geöffneten Fenster. 
- **Was passiert, wenn ich mein Passwort während des Logins nicht mehr weiß?**<br/> Falls du dein Passwort vergessen haben solltest, um dich in der Inventarisierungssoftware einzuloggen, melde dich bei deinem zuständigen Gruppenadministrator, um dein Passwort durch ihn ändern zu lassen. Sobald die Änderung erfolgt ist, logge dich erneut in die Software ein.  
- **Wie kann ich ein Profilbild einfügen?**<br/>Um ein Profilbild einzufügen, öffne die Inventarisierungssoftware. Logge dich mit deinem Benutzernamen und Passwort ein und navigiere anschließend in die Einstellungen.  (rechte obere Ecke auf dein Profilbild klicken (insofern keins gesetzt ist, ist es ein graues Profilbild)). Dort gibt es die Überschrift "Profilbild-URL / Base64 eingeben". Trage unter diese Überschrift in das Feld die URL bzw. deinen [Base64-Text](https://base64.guru/converter/encode/image/png) ein.
- **Kann ich einfach so Administratorrechte erhalten?**<br/> Nein. Administratorrechte sind nur für den Gruppenadmin sowie für die Entwickler des Programmes vorgesehen. 
- **Wie kann ich eine Idee zum Inventartool weitergeben?**<br/> Hierfür gibt es mehrere Möglichkeiten. Entweder du gibst es an deinen Gruppenleiter weiter oder sendest eine [E-Mail an den Ersteller dieses Repositories](mailto:Jack-Mike.Saering@srhk.de).
- **Gibt es eine Anleitung, in welcher die Funktionen des Programmes genau beschrieben sind?**<br/> Ja. Schau dafür in den Abschnitt Dokumentation über diesem FAQ.
- **Warum ist der DEBUG-Modus nur für Administratoren verfügbar?**<br/> Der DEBUG-Modus muss nicht zwingend notwendig von einem Benutzer ohne erweiterte Rechte verfügbar sein, weil dieser nur für erweiterte Fehlersuche und besseres Logging zur Verfügung steht.

## Credits

Dieses Projekt wird von der **FI24** im Rahmen ihrer Ausbildung entwickelt. Mitwirkende sind:

[Peamer (Jack)](https://github.com/peaemer/)

[Alex5X5 (Alex)](https://github.com/Alex5X5)

[GitSchwan (Fabian)](https://github.com/GitSchwan)

[Chauto (Anakin)](https://github.com/Chautoo)

[FemRene (Rene)](https://github.com/FemRene)

[Tam Ngyuen]()

## Unterstützt und gefördert durch 

![srhHeader](https://github.com/user-attachments/assets/7592aeef-c2d3-40f3-b446-e0a64a8f632e)
