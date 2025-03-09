import tkinter as tk

class DrawingInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.title("Reconnaissance de Chiffres")
        self.geometry("800x500")
        self.configure(bg="#f0f0f0")

        # Panneau principal
        self.main_panel = tk.Frame(self, bg="#f0f0f0")
        self.main_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panneau gauche pour dessiner
        self.draw_panel = DrawPanel(self.main_panel)
        self.draw_panel.pack(side=tk.LEFT, padx=10, pady=10)

        # Panneau droit pour afficher le chiffre suggéré et les boutons
        self.right_panel = tk.Frame(self.main_panel, bg="#f0f0f0")
        self.right_panel.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        # Label pour afficher le chiffre suggéré
        self.prediction_label = tk.Label(self.right_panel, text="1", font=("Arial", 100), width=5, height=2)
        self.prediction_label.pack(pady=20)

        # Bouton pour effacer le dessin
        self.clear_button = tk.Button(self.right_panel, text="Effacer", command=self.clear_drawing, font=("Arial", 14), padx=20, pady=10)
        self.clear_button.pack(pady=10)

    def clear_drawing(self):
        """Effacer le dessin sur le panneau gauche"""
        self.draw_panel.clear()

class DrawPanel(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=400, height=400, bg="white", bd=2, relief="groove")
        self.pack_propagate(False)
        
        # Liste pour enregistrer les coordonnées du dessin
        self.last_x = None
        self.last_y = None
        self.matrix = [[0 for _ in range(10)] for _ in range(10)]

        # Lier les événements de la souris pour dessiner
        self.bind("<B1-Motion>", self.paint)
        self.bind("<ButtonRelease-1>", self.reset)

    def paint(self, event):
        """Dessiner sur le canvas"""
        scale = 40  # Échelle pour agrandir les pixels
        x, y = event.x // scale * scale, event.y // scale * scale  # Alignement sur une grille de 10x10 pixels
        if 0 <= y // scale < 10 and 0 <= x // scale < 10:
            if self.last_x is not None and self.last_y is not None:
                self.create_rectangle(self.last_x, self.last_y, x + scale, y + scale, width=0, fill="black", outline="black")
                self.matrix[y // scale][x // scale] = 1

            # Afficher la matrice après chaque modification
            self.print_matrix()

            self.last_x = x
            self.last_y = y

    def reset(self, event):
        """Réinitialiser les coordonnées après que la souris soit relâchée"""
        self.last_x = None
        self.last_y = None

    def clear(self):
        """Effacer le dessin"""
        self.delete("all")
        self.matrix = [[0 for _ in range(10)] for _ in range(10)]

    def get_matrix(self):
        """Retourner la matrice du dessin"""
        return self.matrix

    def print_matrix(self):
        """Imprimer la matrice actuelle dans la console"""
        for row in self.matrix:
            print(row)

# Lancer l'application
if __name__ == "__main__":
    app = DrawingInterface()
    app.mainloop()