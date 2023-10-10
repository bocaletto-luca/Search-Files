# Nome del software: Search Files
# Autore: Luca Bocaletto
# Sito Web: https://www.elektronoide.it
# Licenza: GPLv3

# Importa le librerie necessarie
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

# Funzione per cercare i file
def search_files():
    # Ottieni il nome del file e la directory dalla GUI
    file_name = entry_filename.get()
    directory = entry_directory.get()

    # Verifica se il nome del file è vuoto
    if not file_name:
        result_tree.delete(*result_tree.get_children())
        result_tree.insert("", "end", values=("Inserisci un nome di file valido.", ""))
        return

    # Verifica se la directory esiste
    if not os.path.exists(directory):
        result_tree.delete(*result_tree.get_children())
        result_tree.insert("", "end", values=("La directory selezionata non esiste.", ""))
        return

    # Avvia la barra di avanzamento
    progress_bar.start()

    # Pulisce i risultati precedenti nella tabella
    result_tree.delete(*result_tree.get_children())

    # Crea una lista per memorizzare i file trovati
    found_files = []

    # Utilizza os.walk per esplorare la directory e i suoi sotto-directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Verifica se il nome del file cercato è presente nel nome del file corrente
            if file_name in file:
                file_path = os.path.join(root, file)
                found_files.append((file, file_path))

    # Arresta la barra di avanzamento
    progress_bar.stop()

    # Mostra i risultati nella tabella
    if not found_files:
        result_tree.insert("", "end", values=("Nessun file trovato.", ""))
    else:
        for file, file_path in found_files:
            result_tree.insert("", "end", values=(file, file_path))

# Funzione per sfogliare e selezionare una directory
def browse_directory():
    directory = filedialog.askdirectory()
    entry_directory.delete(0, tk.END)
    entry_directory.insert(0, directory)

# Funzione per aprire il file selezionato
def open_file():
    selected_item = result_tree.selection()
    if selected_item:
        item = result_tree.item(selected_item, "values")
        file_path = item[1]
        if os.path.isfile(file_path):
            os.startfile(file_path)

# Creazione della finestra principale dell'app
app = tk.Tk()
app.title("Cerca File")

# Etichetta per il nome del file
label_filename = tk.Label(app, text="Nome del file:")
label_filename.pack()

# Campo di input per il nome del file
entry_filename = tk.Entry(app)
entry_filename.pack()

# Etichetta per la directory
label_directory = tk.Label(app, text="Directory:")
label_directory.pack()

# Campo di input per la directory
entry_directory = tk.Entry(app)
entry_directory.pack()

# Pulsante per la selezione della directory
browse_button = tk.Button(app, text="Sfoglia", command=browse_directory)
browse_button.pack()

# Pulsante per avviare la ricerca
search_button = tk.Button(app, text="Cerca", command=search_files)
search_button.pack()

# Barra di avanzamento
progress_bar = ttk.Progressbar(app, mode="indeterminate")
progress_bar.pack()

# Creazione di una tabella per i risultati con colonne "File" e "Percorso"
result_tree = ttk.Treeview(app, columns=("File", "Percorso"), show="headings")
result_tree.heading("File", text="File")
result_tree.heading("Percorso", text="Percorso")

# Posiziona la tabella nella finestra
result_tree.pack(fill="both", expand=True)

# Pulsante per aprire il file selezionato
open_button = tk.Button(app, text="Apri File", command=open_file)
open_button.pack()

# Avvia l'applicazione
app.mainloop()
