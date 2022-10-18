# Projektgruppe

## Projekt importieren
### Section 1 - Personal Access Token generieren 
1. Auf euer Profilbild oben rechts gehen
2. Edit profile auswählen
3. Rechts auf Access Tokens klicken
4. Dem Token einen Namen geben
5. Das Ablaufdatum auf irgendwann nächstes Jahr setzen
6. Unter Select scopes write_repository auswählen
7. Unten auf Create personal access token klicken
8. Access Token unbedingt irgendwo lokal auf eurem Rechner speichern

### Section 2 - Repository klonen
1. Das Repository Projektgruppe auswählen
2. Auf Clone klicken (der farbige Button rechts)
3. Unter Open in your IDE -> Visual Studio Code (HTTPS) auswählen
4. In Visual Studio Code einen Ordner auswählen in dem das Projekt leben soll
5. Euren Nutzernamen eingeben (Findet ihr wieder oben rechts auf GitLab, steht unter eurem Bild hinter dem @)
6. Das Passwort eingeben (das Passwort ist in diesem Fall der Personal Access Token aus Schritt 1)

### Section 3 - Das Projekt initialisieren (noch nicht nötig da wir bis jetzt keine Dependencies haben)
Alle Befehle werden in der Konsole im Projektverzeichnis eingegeben.
1. virtualenv env
2. source env/bin/activate
3. pip install -r requirements.txt
4. Zum Beenden der virtualenv: deactivate

### Section 4 - Dependencies installieren
1. source env/bin/activate
2. pip install [options] [package name]
3. pip freeze > requirements.txt
4. deactivate

### Section 5 - Mit SSH verbinden
In der Konsole:
1. ssh-keygen -t ed25519
2. Jetzt werdet ihr nach einigen Parametern gefragt, drückt einfach Enter bis ihr durch seid
3. Navigiert in das Verzeichnis, in dem der Key gespeichert wurde mit cd /home/__Nutzername__/.ssh
4. cat id_ed25519.pub
5. Kopiert die gesamte Ausgabe des cat Befehls

Auf der Gitlab Seite:
1. Geht auf euer Bild und dann *preferences*
2. An der Seite steht ein Reiter *SSH Keys*
3. Fügt dort unter Key die Ausgabe von cat ein
4. Drückt auf *Add key*