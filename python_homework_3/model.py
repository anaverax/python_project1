import json
import os
import random
import string

class Book:
    def __init__(self, title, author, year, status="available"):    # Jedes Book hat title, author, year und status ("available" wird als standard hier festgelegt.)
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):      # Wandelt das Book-Objekt in ein Dictionary um, welches dann in JSON gespeichert werden kann.
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):    # Es wird ein neues Book-Objekt aus einem Dictionary gebaut (aus einer JSON-file heraus).
        return Book(data["title"], data["author"], data["year"], data.get("status", "available"))

class BookModel:    # Verwaltung der gesamten Buchdatenbank
    def __init__(self, filepath="lib_default.json"):    # Die Datei lib_default.json wird geladen (oder erstellt), um alle Bücher zu laden.
        self.books = []
        self.filepath = filepath
        self.load_books()

    def add_book(self, title, author, year, status):
        if not title or not author or not year or not status:           # wenn eines der Felder leer ist, dann wird ein Fehler ausgelöst.
            raise ValueError("Alle Felder müssen ausgefüllt sein.")     # man verhindert dadurch, dass unvollständige Datensätze gespeichert werden.
        int(year)                                                       # Das Jahr wird validiert, weil es sich dabei um eine ganze Zahl handeln muss, sonst Fehler.
        self.books.append(Book(title, author, year, status))            # Ein neues Book-Objekt wird jetzt mit den eingegebenen Werten erstellt. Eine Liste self.books wird eingefügt (Datenbank im Speicher).
        self.save_books()                                               # Die methode save_books() schreibt alle Bücher in eine Datei, sodass diese dauerhaft (nicht nur im Arbeitsspeicher) gespeichert sind.

    def add_random_books(self, n, callback=None):                                           # Diese Funktion ist für die Generierung zufälliger Bücher 
        statuses = ["available", "lent out", "missing", "deleted"]                          # Die vier möglichen Zustände, in denen ein Buch sein kann, werden in einer Liste gespeichert. Später wird einer davon zufällig vergeben.
        for i in range(n):                                                                  # Das "n" ist vom Funktionsaufruf (z.B. add_random_books(1_000_000)). Für jedes Buch wird einmal der folgende Block ausgeführt. 
            title = ''.join(random.choices(string.ascii_letters + string.digits, k=10))     # title: zufälliger 10-Zeichen-String (Buchstaben + Zahlen)
            author = ''.join(random.choices(string.ascii_letters + string.digits, k=8))     # author: Zufälliger 8-Zeichen-String 
            year = str(random.randint(1500, 2025))                                          # year: Zufallszahl zwischen 1500 und 2025, als String gespeichert
            status = random.choice(statuses)                                                # status: Zufälliger Eintrag aus der statuses-Liste
            self.books.append(Book(title, author, year, status))                            # Ein neues Book-Objekt wird mit den generierten Daten erstellt und zur Liste hinzugefügt.
            if callback and i % 10000 == 0:                                                 # Hier wird regelmäßg Rückmeldung für die spätere Erzeugung von 1.000.000 Bücher gegeben. Callback ist nicht None (wurde Fortschrittsfunktion übergeben?) und nur bei jedem 10.000sten Buch wird rückgemeldet.
                callback(i, n)                                                              # Zwischenstand: Ich bin bei Buch i von insgestamt n Büchern angekommen.
        self.save_books()                                                                   # Nach dem Erzeugen aller Bücher wird die gesamte Buchliste in die JSON-Datei gespeichert.

    def update_book(self, index, title, author, year, status):  # Aktualisiert ein bestehendes Buch anhand seines Indexes in der Liste self.books
        int(year)                                               # year-Wert muss in Ganzzahl konvertiert sein (wieder eine Validitätsprüfung)
        self.books[index].title = title                         # self.books[index] Greift auf das Buch an der gegebenen Position in der Liste zu. Die Attribute title, author, year, status des Buches werden durch neue Werte ersetzt.
        self.books[index].author = author
        self.books[index].year = year
        self.books[index].status = status
        self.save_books()                                       # Speichert die ganze books-Liste zurück in die JSON-Datei (also lib_default.json), damit die Änderungen dauerhaft sind.

    def delete_book(self, index):                               # Markiert ein Buch mit dem Status "deleted"
        self.books[index].status = "deleted"                    # Das Buch an der gegebenen Position in der Liste wird nicht aus der Liste entfernt. Stattdessen wird sein Status auf "deleted" gesetzt.
        self.save_books()                                       # Die Änderung wird gespeichert – die JSON-Datei wird neu geschrieben, sodass der Status "deleted" dauerhaft gespeichert ist.

    def get_books(self):        # Diese Methode gibt einfach die komplette Liste aller Bücher zurück – ohne Filterung.
        return self.books

    def get_visible_books(self, status_filter=None):
        if status_filter and status_filter != "all":                        # status_filter: Prüft, ob der Filter nicht None ist. status_filter != "all": Stellt sicher, dass wir nicht alle Bücher zurückgeben wollen. 
            return [b for b in self.books if b.status == status_filter]     # Hier wird eine List Comprehension verwendet, um eine neue Liste von Büchern zu erstellen. Sie enthält nur die Bücher, deren status dem übergebenen status_filter entspricht.
        return self.books                                                   # Wenn status_filter None oder "all" ist, wird einfach die gesamte Liste self.books zurückgegeben. So zeigt die Methode alle Bücher an, wenn kein spezifischer Filter angewendet wird.

    def search_books(self, query):  # Dies ist der Suchbegriff, den der Benutzer eingibt, um Bücher zu finden.
        query = query.lower()       # Der Suchbegriff wird in Kleinbuchstaben umgewandelt. Das hilft dabei, Groß- und Kleinschreibung zu ignorieren, sodass die Suche flexibler ist.
        return [b for b in self.books if query in b.title.lower() or query in b.author.lower()]     # Die Bedingung if query in b.title.lower() or query in b.author.lower() prüft: Ob der query-String im Titel (b.title) oder im Autor (b.author) des Buches enthalten ist.

    def save_books(self):
        with open(self.filepath, "w", encoding="utf-8") as f:                               # Datei wird zum Schreiben "w" geöffnet. self.filepath gibt an, wo die Datei gespeichert wird (in deinem Fall lib_default.json). encoding="utf-8" sorgt dafür, dass die Datei in UTF-8 kodiert wird, was besonders wichtig ist, um nicht-englische Zeichen (wie Umlaute) korrekt zu speichern.
            json.dump([b.to_dict() for b in self.books], f, indent=2, ensure_ascii=False)   # json.dump(...) ist eine Methode, die eine Python-Datenstruktur in das JSON-Format umwandelt und sie in die angegebene Datei schreibt. List Comprehension: Diese erstellt eine Liste, indem sie für jedes Buch (b) in self.books die Methode to_dict() aufruft. Das wandelt jedes Book-Objekt in ein Dictionary um. indent=2 formatiert die JSON-Datei so, dass sie leicht lesbar ist (mit Einrückungen von 2 Leerzeichen). 

    def load_books(self):
        if os.path.exists(self.filepath):                                   # prüft, ob die Datei, die im filepath angegeben ist (in deinem Fall lib_default.json), tatsächlich existiert. Wenn die Datei nicht existiert, passiert nichts – dies verhindert Fehler beim Versuch, eine nicht vorhandene Datei zu öffnen.
            with open(self.filepath, "r", encoding="utf-8") as f:           # Wenn die Datei existiert, wird sie im Lese-Modus ("r") geöffnet. Auch hier wird encoding="utf-8" angegeben, um sicherzustellen, dass alle Zeichen korrekt gelesen werden.
                self.books = [Book.from_dict(d) for d in json.load(f)]      # lädt die Daten aus der JSON-Datei und konvertiert sie in eine Liste von Book-Objekten. json.load(f) liest den Inhalt der Datei und wandelt ihn in eine Python-Datenstruktur (in diesem Fall eine Liste von Dictionaries) um.