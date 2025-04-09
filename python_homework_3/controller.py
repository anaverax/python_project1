class BookController:
    def __init__(self, model, view):    # Hier werden die Model- und View-Instanzen übergeben und in self.model und self.view gespeichert. self.update_list(): Diese Methode wird aufgerufen, um die Buchliste in der GUI beim Start zu aktualisieren.
        self.model = model
        self.view = view
        self.update_list()

    def add_book(self, title, author, year, status):            # Diese Methode ruft die add_book-Methode im Model auf, um ein neues Buch hinzuzufügen.
        try:
            self.model.add_book(title, author, year, status)    # Bei Erfolg zeigt die Methode eine Erfolgsmeldung an und aktualisiert die Liste.
            self.view.show_message("Buch hinzugefügt.")
            self.update_list()
        except Exception as e:                                  # Bei einem Fehler wird eine Fehlermeldung angezeigt.
            self.view.show_error(str(e))

    def add_random_books(self, n):                                          # Diese Methode ruft add_random_books im Model auf, um eine bestimmte Anzahl zufälliger Bücher hinzuzufügen.
        self.model.add_random_books(n)
        self.view.show_message(f"{n} zufällige Bücher hinzugefügt.")        # Erfolgreiche Ausführung zeigt eine Nachricht an und aktualisiert die Liste.
        self.update_list()

    def delete_book(self, index):                               # Löscht ein Buch durch Aufruf der delete_book-Methode im Model.
        self.model.delete_book(index)
        self.view.show_message("Buch als gelöscht markiert.")   # Zeigt eine Nachricht an und aktualisiert die Liste.
        self.update_list()

    def update_book(self, index, title, author, year, status):  # Aktualisiert ein Buch basierend auf dem Index.
        try:
            self.model.update_book(self.get_real_index(index), title, author, year, status)
            self.view.show_message("Buch aktualisiert.")        # Meldung, wenn ein Buch erfolgreich aktualisiert wurde.
            self.update_list()
        except Exception as e:                                  # Wenn ein Fehler auftritt, dann wird eine Fehlermeldung ausgegeben.
            self.view.show_error(str(e))

    def update_status_only(self, index, new_status):        # Diese Methode wird verwendet, um nur den Status eines Buches zu aktualisieren nach einem Doppelklick in der GUI.
        real_index = self.get_real_index(index)
        book = self.model.books[real_index]
        book.status = new_status
        self.model.save_books()
        self.view.show_message("Status aktualisiert.")      # Sie zeigt entsprechende Meldungen an und speichert die Änderungen.
        self.update_list()

    def search_books(self, query):                                  # Führt eine Suche durch, indem die search_books-Methode im Model aufgerufen wird.
        self.view.show_books(self.model.search_books(query))        # Die Ergebnisse werden in der GUI angezeigt.

    def update_list(self):                              # Diese Methode aktualisiert die Anzeige in der GUI, je nach ausgewähltem Statusfilter.
        status_filter = self.view.filter_var.get()      # Sie verwendet get_books() oder get_visible_books() aus dem Model, um die Liste der Bücher zu erhalten.
        if status_filter == "all":
            self.view.show_books(self.model.get_books())
        else:
            self.view.show_books(self.model.get_visible_books([status_filter]))

    def get_visible_books(self):                        # Holt die Bücher basierend auf dem Statusfilter.
        status_filter = self.view.filter_var.get()
        return self.model.get_visible_books([status_filter]) if status_filter != "all" else self.model.get_books()

    def get_real_index(self, visible_index):        # Diese Methode gibt den sichtbaren Index zurück.
        return visible_index
