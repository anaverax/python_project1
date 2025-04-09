# Team: louis.braun@stud.th-deg.de, verena.schober@stud.th-deg.de, janine.heinl@stud.th-deg.de

import json
import tkinter as tk
from tkinter import messagebox

# Standarddatei
LIBRARY_FILENAME = "test1.json"

# Funktion zum Laden der Bibliothek
def load_library():
    try:
        with open(LIBRARY_FILENAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Funktion zum Speichern der Bibliothek
def save_library(library):
    with open(LIBRARY_FILENAME, "w") as file:
        json.dump(library, file, indent=4)

# Funktion zum Hinzufügen eines Buchs
def add_book():
    author = author_entry.get().strip()
    title = title_entry.get().strip()
    year = year_entry.get().strip()
    
    if not author or not title or not year:
        messagebox.showwarning("Warnung", "Alle Felder müssen ausgefüllt sein!")
        return
    
    library.append({"author": author, "title": title, "year": year})
    save_library(library)
    update_book_list()
    author_entry.delete(0, tk.END)
    title_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    messagebox.showinfo("Erfolg", "Buch hinzugefügt!")

# Funktion zum Löschen eines Buchs
def delete_book():
    try:
        selected_index = book_listbox.curselection()[0]
        del library[selected_index]
        save_library(library)
        update_book_list()
        messagebox.showinfo("Erfolg", "Buch gelöscht!")
    except IndexError:
        messagebox.showwarning("Warnung", "Bitte ein Buch auswählen!")

# Funktion zum Aktualisieren der Buchliste
def update_book_list():
    book_listbox.delete(0, tk.END)
    for book in library:
        book_listbox.insert(tk.END, f"{book['title']} von {book['author']} ({book['year']})")

# GUI erstellen
root = tk.Tk()
root.title("Buchverwaltung")

# Bibliothek laden
library = load_library()

# Widgets erstellen
frame = tk.Frame(root)
frame.pack(pady=10)

book_listbox = tk.Listbox(frame, width=100, height=20)
book_listbox.pack(side=tk.LEFT, padx=10)
scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=book_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
book_listbox.config(yscrollcommand=scrollbar.set)

update_book_list()

author_label = tk.Label(root, text="Autor:")
author_label.pack()
author_entry = tk.Entry(root, width=40)
author_entry.pack()

title_label = tk.Label(root, text="Titel:")
title_label.pack()
title_entry = tk.Entry(root, width=40)
title_entry.pack()

year_label = tk.Label(root, text="Erscheinungsjahr:")
year_label.pack()
year_entry = tk.Entry(root, width=40)
year_entry.pack()

add_button = tk.Button(root, text="Buch hinzufügen", command=add_book)
add_button.pack(pady=5)

delete_button = tk.Button(root, text="Buch löschen", command=delete_book)
delete_button.pack(pady=5)

exit_button = tk.Button(root, text="Beenden", command=root.quit)
exit_button.pack(pady=5)

root.mainloop()
