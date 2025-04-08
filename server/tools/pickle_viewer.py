import tkinter as tk
from tkinter import filedialog, messagebox
import pickle

# Fonction pour ouvrir un fichier Pickle et charger son contenu
def open_pickle_file():
    file_path = filedialog.askopenfilename(filetypes=[("Pickle Files", "*.pkl")], initialdir=".")
    if not file_path:
        return
    
    try:
        with open(file_path, 'rb') as file:
            content = pickle.load(file)
            text_box.delete(1.0, tk.END)  # Effacer le contenu actuel de la zone de texte
            text_box.insert(tk.END, str(content))  # Afficher le contenu du Pickle dans la zone de texte
            text_box.file_path = file_path  # Stocker le chemin du fichier pour la sauvegarde
            file_label.config(text=f"Fichier actuel : {file_path}")  # Afficher le chemin du fichier
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de charger le fichier Pickle : {e}")

# Fonction pour sauvegarder le contenu modifié dans le fichier Pickle
def save_pickle_file():
    if not hasattr(text_box, 'file_path') or not text_box.file_path:
        messagebox.showerror("Erreur", "Aucun fichier Pickle ouvert")
        return
    
    try:
        content = eval(text_box.get(1.0, tk.END))  # Evaluer le contenu de la zone de texte en un objet Python
        with open(text_box.file_path, 'wb') as file:
            pickle.dump(content, file)
        messagebox.showinfo("Succès", "Fichier Pickle sauvegardé avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de sauvegarder le fichier Pickle : {e}")

# Interface graphique avec Tkinter
root = tk.Tk()
root.title("Éditeur Pickle")
root.geometry("800x600")

# Frame principal pour organiser l'interface
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Label pour afficher le fichier actuel
file_label = tk.Label(main_frame, text="Aucun fichier ouvert", anchor="w", width=80)
file_label.pack(fill=tk.X, padx=10, pady=5)

# Zone de texte pour afficher et éditer le contenu Pickle
text_box = tk.Text(main_frame, width=60, height=20)
text_box.pack(padx=10, pady=10)

# Frame pour les boutons
button_frame = tk.Frame(main_frame)
button_frame.pack(fill=tk.X, padx=10, pady=5)

# Boutons pour ouvrir et sauvegarder le fichier Pickle
open_button = tk.Button(button_frame, text="Ouvrir Pickle", command=open_pickle_file, width=20)
open_button.pack(side=tk.LEFT, padx=10, pady=5)

save_button = tk.Button(button_frame, text="Sauvegarder Pickle", command=save_pickle_file, width=20)
save_button.pack(side=tk.LEFT, padx=10, pady=5)

root.mainloop()
