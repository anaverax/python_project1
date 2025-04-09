import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class BookView(tk.Tk):
    def __init__(self, controller):         # Hauptfenster der Anwendung wird erstellt. controller wird als Attribut gespeichert, um auf die Methoden des Controllers zugreifen zu können.
        super().__init__()
        self.title("Bücherverwaltung")
        self.geometry("700x600")
        self.controller = controller

        # Suche
        ttk.Label(self, text="Suchen:").pack(pady=(10, 0))  # Ein Label und ein Eingabefeld (Entry) für die Suche werden erstellt.
        self.search_entry = ttk.Entry(self)
        self.search_entry.pack(fill="x", padx=10)
        self.search_entry.bind("<KeyRelease>", lambda e: self.controller.search_books(self.search_entry.get())) # Bei jeder Tasteneingabe (<KeyRelease>) wird die Suchmethode im Controller aufgerufen, um die Bücher zu filtern.

        # Filter Dropdown
        self.filter_var = tk.StringVar(value="all")
        filter_frame = ttk.Frame(self)
        filter_frame.pack(pady=5)
        ttk.Label(filter_frame, text="Status filtern:").pack(side="left")
        self.filter_dropdown = ttk.Combobox(filter_frame, textvariable=self.filter_var, state="readonly", values=["all", "available", "lent out", "missing", "deleted"])    # Ein Dropdown-Menü (Combobox) zur Filterung der Bücher nach Status.
        self.filter_dropdown.pack(side="left", padx=5)
        self.filter_dropdown.bind("<<ComboboxSelected>>", lambda e: self.controller.update_list())                                                                          # Bei Auswahl eines Status wird update_list im Controller aufgerufen, um die angezeigten Bücher zu aktualisieren.

        # Eingabeformular
        self.form_frame = ttk.Frame(self)   # Hier wird ein Eingabeformular für die Buchinformationen erstellt (Titel, Autor, Erscheinungsjahr und Status).
        self.form_frame.pack(pady=10)       # Es wird die Methode _create_labeled_entry() für ein konsistentes Layout verwendet.

        self.entry_title = self._create_labeled_entry("Titel:")
        self.entry_author = self._create_labeled_entry("Autor:")
        self.entry_year = self._create_labeled_entry("Erscheinungsjahr:")

        self.status_var = tk.StringVar(value="available")
        ttk.Label(self.form_frame, text="Status:").grid(row=0, column=6, sticky="e")
        self.status_dropdown = ttk.Combobox(self.form_frame, textvariable=self.status_var, state="readonly", values=["available", "lent out", "missing", "deleted"])
        self.status_dropdown.grid(row=0, column=7, padx=5)

        # Buttons
        button_frame = ttk.Frame(self)  # Buttons für Aktionen wie Buch hinzufügen, als gelöscht markieren und zufällige Bücher hinzufügen. Jede Schaltfläche ruft die jeweilige Methode im Controller auf.
        button_frame.pack()

        ttk.Button(button_frame, text="Buch hinzufügen", command=self.add_book).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Buch als gelöscht markieren", command=self.delete_book).pack(side="left", padx=5)
        ttk.Button(button_frame, text="1 Mio. Bücher hinzufügen", command=self.add_random_books).pack(side="left", padx=5)

        # Tabelle
        self.tree = ttk.Treeview(self, columns=("title", "author", "year", "status"), show="headings")  # Eine Treeview-Tabelle zeigt die Liste der Bücher an, mit den Spalten für Titel, Autor, Erscheinungsjahr und Status. Doppelklick auf eine Zeile öffnet die edit_book-Methode, um den Status zu ändern.
        for col in ("title", "author", "year", "status"):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150 if col != "year" else 80, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.edit_book)

    def _create_labeled_entry(self, label_text):    # Erstellt ein Label und ein Eingabefeld (Entry) für die Eingabe von Buchdaten.
        row = self.form_frame.grid_size()[1]
        ttk.Label(self.form_frame, text=label_text).grid(row=row, column=0, sticky="e")
        entry = ttk.Entry(self.form_frame)
        entry.grid(row=row, column=1, columnspan=2, padx=5, pady=2, sticky="ew")
        return entry

    def add_book(self):     # Diese Methode ruft die add_book-Methode im Controller auf und übergibt die Werte aus den Eingabefeldern.
        self.controller.add_book(
            self.entry_title.get(),
            self.entry_author.get(),
            self.entry_year.get(),
            self.status_var.get()
        )

    def add_random_books(self):     # Fügt 1.000.000 zufällige Bücher in einem neuen Thread hinzu, um die GUI reaktionsfähig zu halten.
        threading.Thread(target=self.controller.add_random_books, args=(1_000_000,), daemon=True).start()

    def delete_book(self):  # Löscht das aktuell ausgewählte Buch aus der Tabelle.
        selected = self.tree.selection()
        if selected:
            self.controller.delete_book(int(selected[0]))
        else:
            self.show_error("Bitte wähle ein Buch aus der Liste zum Löschen.")

    def show_books(self, books):    # Zeigt die Bücher in der Tabelle an, indem vorhandene Einträge gelöscht und neue hinzugefügt werden.
        self.tree.delete(*self.tree.get_children())
        for i, b in enumerate(books):
            self.tree.insert("", "end", iid=i, values=(b.title, b.author, b.year, b.status))

    def update_list(self):
        status_filter = self.filter_var.get()
        if status_filter == "all":
            self.show_books(self.controller.model.get_books())
        else:
            self.show_books(self.controller.model.get_visible_books([status_filter]))

    def show_message(self, msg):            # Zeigen Informations- oder Fehlermeldungen in Dialogfeldern an.
        messagebox.showinfo("Info", msg)

    def show_error(self, err):              # Zeigen Informations- oder Fehlermeldungen in Dialogfeldern an.
        messagebox.showerror("Fehler", err)

    def edit_book(self, event):             # Diese Methode öffnet ein neues Fenster, um den Status eines Buchs zu ändern. Der Benutzer kann aus einem Dropdown-Menü den neuen Status auswählen.
        selected = self.tree.selection()
        if not selected:
            return
        index = int(selected[0])
        book = self.controller.get_visible_books()[index]

        popup = tk.Toplevel(self)
        popup.title("Status ändern")
        popup.geometry("250x120")
        popup.transient(self)
        popup.grab_set()

        ttk.Label(popup, text=f"Buch: {book.title}").pack(pady=5)
        status_var = tk.StringVar(value=book.status)

        status_combo = ttk.Combobox(
            popup,
            textvariable=status_var,
            state="readonly",
            values=["available", "lent out", "missing", "deleted"]
        )
        status_combo.pack(pady=5)

        def save():
            new_status = status_var.get()
            self.controller.update_status_only(index, new_status)
            popup.destroy()

        ttk.Button(popup, text="Speichern", command=save).pack(pady=5)