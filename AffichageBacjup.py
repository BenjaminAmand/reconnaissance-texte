import random
import string
import tkinter as tk
from PIL import Image
from Network import Network
import os  # Importer os pour accéder aux fichiers du système

WIDTH = 10
HEIGHT = 10

class DrawingInterface(tk.Tk):
    def __init__(self, network):
        super().__init__()

        # Configuration de la fenêtre principale
        self.title("Reconnaissance de Chiffres")
        self.configure(bg="#f0f0f0")

        # Panneau principal
        self.main_panel = tk.Frame(self, bg="#f0f0f0")
        self.main_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panneau gauche pour dessiner
        self.draw_panel = DrawPanel(self, self.main_panel, network)  # Passer self (DrawingInterface) ici
        self.draw_panel.pack(side=tk.LEFT, padx=10, pady=10)

        # Panneau droit pour afficher le chiffre suggéré et les boutons
        self.right_panel = tk.Frame(self.main_panel, bg="#f0f0f0")
        self.right_panel.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        # Label pour afficher le chiffre suggéré
        self.prediction_label = tk.Label(self.right_panel, text="1", font=("Arial", 100), width=5, height=2)
        self.prediction_label.pack(pady=20)

        # Champ de texte pour entrer un caractère
        self.character_label = tk.Label(self.right_panel, text="Entrer un caractère", font=("Arial", 14))
        self.character_label.pack(pady=10)
        self.character_input = tk.Entry(self.right_panel, font=("Arial", 14))
        self.character_input.pack(pady=10)

        # Bouton pour effacer le dessin
        self.clear_button = tk.Button(self.right_panel, text="Effacer", command=self.clear_drawing, font=("Arial", 14), padx=20, pady=10)
        self.clear_button.pack(pady=10)
        
        # Bouton pour sauvegarder l'image
        self.save_button = tk.Button(self.right_panel, text="Save", command=self.draw_panel.save, font=("Arial", 14), padx=20, pady=10)
        self.save_button.pack(pady=20)

        # Label pour afficher le nombre de fichiers dans le dossier
        self.file_count_label = tk.Label(self.right_panel, text="Fichiers sauvegardés: 0", font=("Arial", 14))
        self.file_count_label.pack(pady=10)

    def clear_drawing(self):
        """Effacer le dessin sur le panneau gauche"""
        self.draw_panel.clear()
    
    def apply_network(self, matrix):
        self.network.apply_network(matrix)

class DrawPanel(tk.Canvas):
    def __init__(self, master, parent, network):
        super().__init__(parent, width=WIDTH*40, height=HEIGHT*40, bg="white", bd=2, relief="groove")
        self.master = master  # Référencer l'instance de DrawingInterface
        self.network = network
        self.pack_propagate(False)
        
        # Liste pour enregistrer les coordonnées du dessin
        self.last_x = None
        self.last_y = None
        self.matrix = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

        # Lier les événements de la souris pour dessiner
        self.bind("<B1-Motion>", self.paint)
        self.bind("<ButtonRelease-1>", self.reset)
    
    def save(self):
        # Récupérer le caractère entré dans le champ de texte
        char_input = self.master.character_input.get()

        # Vérifier si le champ est vide ou non
        if not char_input or len(char_input) != 1:
            print("Veuillez entrer un caractère valide.")
            return

        # Créer le répertoire si nécessaire
        directory = f"TrainingModel/{char_input}"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Créer l'image à partir de la matrice
        img = Image.new('1', (10, 10))
        for y in range(10):
            for x in range(10):
                img.putpixel((x, y), 0 if self.matrix[y][x] == 1 else 255)

        # Générer le nom du fichier en utilisant le caractère et un code aléatoire
        random_chars = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
        filename = f"{directory}/{random_chars}.png"

        # Sauvegarder l'image
        img.save(filename, "PNG")
        print(f"Image sauvegardée sous {filename}")

        # Mettre à jour le nombre de fichiers dans le dossier
        self.update_file_count(char_input)

    def update_file_count(self, char_input):
        # Compter les fichiers dans le répertoire
        directory = f"TrainingModel/{char_input}"
        if os.path.exists(directory):
            files = os.listdir(directory)
            file_count = len([f for f in files if f.endswith('.png')])  # Compter les fichiers PNG
        else:
            file_count = 0
        
        # Mettre à jour le label dans l'interface graphique
        self.master.file_count_label.config(text=f"Fichiers sauvegardés: {file_count}")

    def paint(self, event):
        """Dessiner sur le canvas"""
        scale = 40  # Échelle pour agrandir les pixels
        x, y = event.x // scale * scale, event.y // scale * scale
        if 0 <= y // scale < HEIGHT and 0 <= x // scale < WIDTH:
            if self.last_x is not None and self.last_y is not None:
                self.create_rectangle(self.last_x, self.last_y, x + scale, y + scale, width=0, fill="black", outline="black")
                self.matrix[y // scale][x // scale] = 1

            # Afficher la matrice après chaque modification
            self.network.apply_network(self.matrix)

            self.last_x = x
            self.last_y = y

    def reset(self, event):
        """Réinitialiser les coordonnées après que la souris soit relâchée"""
        self.last_x = None
        self.last_y = None

    def clear(self):
        """Effacer le dessin"""
        self.delete("all")
        self.matrix = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    def get_matrix(self):
        """Retourner la matrice du dessin"""
        return self.matrix

    def print_matrix(self):
        """Imprimer la matrice actuelle dans la console"""
        for row in self.matrix:
            print(row)

# Lancer l'application
if __name__ == "__main__":
    app = DrawingInterface(Network([]))
    app.mainloop()
