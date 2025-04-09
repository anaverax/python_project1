# Team: louis.braun@stud.th-deg.de, verena.schober@stud.th-deg.de, janine.heinl@stud.th-deg.de

from controller import BookController
from model import BookModel
from view import BookView


def main():
    model = BookModel()                         # Erstellt das Datenmodell. Es lädt (oder erstellt) alle Buch-Daten aus einer JSON-Datei.
    view = BookView(None)                       # Erstellt die Benutzeroberfläche. Hier wird die GUI aufgebaut (Fenster, Eingabefelder, Tabelle, etc.).
    controller = BookController(model, view)    # Der Controller verbindet Model und View. Er enthält die Logik, z. B. was passiert, wenn ein Buch hinzugefügt wird.
    view.controller = controller                # View bekommt den Controller zugewiesen, damit u. a. Buttons die Methoden im Controller aufrufen können.
    view.update_list()                          # Die GUI wird initial mit der aktuellen Buchliste befüllt (z. B. beim Start die JSON-Daten anzeigen).
    view.mainloop()                             # Startet die Haupt-Event-Schleife von Tkinter. Dadurch reagiert das Fenster auf Benutzerinteraktionen.

if __name__ == "__main__":                      # sorgt dafür, dass main() nur dann ausgeführt wird, wenn das Skript direkt gestartet wird nicht aber, wenn z. B. diese Datei importiert wird, um Funktionen oder Klassen daraus zu verwenden.
    main()