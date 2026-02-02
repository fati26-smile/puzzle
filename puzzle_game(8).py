import tkinter as tk
from tkinter import messagebox
import random
import math

class PuzzleGame:
    """
    Jeu de puzzle 3x3 avec trois niveaux de difficulté
    """
    
    def __init__(self, root):
        """Initialise le jeu"""
        self.root = root
        self.root.title("Jeu de Puzzle 3x3")
        self.root.geometry("650x700")
        self.root.configure(bg="#2c3e50")
        
        # Variables de jeu
        self.difficulty = None
        self.board = []
        self.empty_pos = None
        self.time_limit = 0
        self.moves_limit = 0
        self.moves_count = 0
        self.remaining_time = 0
        self.game_running = False
        self.timer_id = None
        self.buttons = []
        
        self.show_menu()
    
    def show_menu(self):
        """Affiche le menu principal"""
        self.clear_window()
        
        # Titre
        title = tk.Label(
            self.root,
            text="JEU DE PUZZLE 3×3",
            font=("Arial", 28, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        title.pack(pady=30)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # === SECTION CLASSIQUE ===
        classic_frame = tk.Frame(
            main_frame,
            bg="#1a252f",
            relief=tk.RAISED,
            borderwidth=3
        )
        classic_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        classic_title = tk.Label(
            classic_frame,
            text="🎯 CLASSIQUE",
            font=("Arial", 18, "bold"),
            bg="#1a252f",
            fg="#27ae60"
        )
        classic_title.pack(pady=20)
        
        classic_desc = tk.Label(
            classic_frame,
            text="Mode standard\nsans contraintes",
            font=("Arial", 11),
            bg="#1a252f",
            fg="#95a5a6",
            justify=tk.CENTER
        )
        classic_desc.pack(pady=10)
        
        # Bouton Facile
        easy_btn = tk.Button(
            classic_frame,
            text="FACILE",
            font=("Arial", 16, "bold"),
            bg="#27ae60",
            fg="white",
            width=15,
            height=2,
            command=lambda: self.start_game("facile"),
            cursor="hand2",
            relief=tk.RAISED
        )
        easy_btn.pack(pady=15)
        
        easy_info = tk.Label(
            classic_frame,
            text="⏱️ Temps: 1 minute\n♾️ Coups: illimités",
            font=("Arial", 11),
            bg="#1a252f",
            fg="#bdc3c7",
            justify=tk.CENTER
        )
        easy_info.pack(pady=5)
        
        # === SECTION SPÉCIAL ===
        special_frame = tk.Frame(
            main_frame,
            bg="#2d1f1f",
            relief=tk.RAISED,
            borderwidth=3
        )
        special_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        special_title = tk.Label(
            special_frame,
            text="⚡ SPÉCIAL",
            font=("Arial", 18, "bold"),
            bg="#2d1f1f",
            fg="#e74c3c"
        )
        special_title.pack(pady=20)
        
        special_desc = tk.Label(
            special_frame,
            text="Modes avec défis\net chiffres fixés",
            font=("Arial", 11),
            bg="#2d1f1f",
            fg="#95a5a6",
            justify=tk.CENTER
        )
        special_desc.pack(pady=10)
        
        # Bouton Moyen
        medium_btn = tk.Button(
            special_frame,
            text="MOYEN",
            font=("Arial", 14, "bold"),
            bg="#f39c12",
            fg="white",
            width=15,
            height=2,
            command=lambda: self.start_game("moyen"),
            cursor="hand2",
            relief=tk.RAISED
        )
        medium_btn.pack(pady=10)
        
        medium_info = tk.Label(
            special_frame,
            text="⏱️ Temps: 50 secondes\n🎯 Coups: 20 maximum\n🔄 Le 3 et 4 s'échangent quand proches",
            font=("Arial", 10),
            bg="#2d1f1f",
            fg="#bdc3c7",
            justify=tk.CENTER
        )
        medium_info.pack(pady=5)
        
        # Bouton Difficile
        hard_btn = tk.Button(
            special_frame,
            text="DIFFICILE",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white",
            width=15,
            height=2,
            command=lambda: self.start_game("difficile"),
            cursor="hand2",
            relief=tk.RAISED
        )
        hard_btn.pack(pady=10)
        
        hard_info = tk.Label(
            special_frame,
            text="⏱️ Temps: 30 secondes\n🎯 Coups: 15 maximum\n🔄 Le 5 et 6 s'échangent quand proches",
            font=("Arial", 10),
            bg="#2d1f1f",
            fg="#bdc3c7",
            justify=tk.CENTER
        )
        hard_info.pack(pady=5)
    
    def start_game(self, difficulty):
        """Démarre une nouvelle partie"""
        self.difficulty = difficulty
        self.moves_count = 0
        self.game_running = True
        
        # Configuration selon la difficulté
        if difficulty == "facile":
            self.time_limit = 60  # 1 minute
            self.moves_limit = float('inf')
            self.swap_3_4_when_adjacent = False
            self.swap_5_6_when_adjacent = False
        elif difficulty == "moyen":
            self.time_limit = 50
            self.moves_limit = 20
            self.swap_3_4_when_adjacent = True  # Contrainte : 3 et 4 s'échangent quand proches
            self.swap_5_6_when_adjacent = False
        else:  # difficile
            self.time_limit = 30
            self.moves_limit = 15
            self.swap_3_4_when_adjacent = False
            self.swap_5_6_when_adjacent = True  # Contrainte : 5 et 6 s'échangent quand proches
        
        self.remaining_time = self.time_limit
        self.initialize_board()
        self.show_game_board()
        self.start_timer()
    
    def initialize_board(self):
        """
        Initialise le plateau avec un mélange garantissant une solution
        """
        # État résolu
        solved = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.board = solved.copy()
        self.empty_pos = 8
        
        print(f"DEBUG: Début initialisation - Niveau: {self.difficulty}")
        
        # Mélanger avec des mouvements valides
        for _ in range(100):
            neighbors = self.get_neighbors(self.empty_pos)
            if neighbors:
                neighbor = random.choice(neighbors)
                self.board[self.empty_pos], self.board[neighbor] = \
                    self.board[neighbor], self.board[self.empty_pos]
                self.empty_pos = neighbor
        
        print(f"DEBUG: Après mélange - Plateau: {self.board}")
        print(f"DEBUG: Position de la case vide: {self.empty_pos}")
    
    def count_inversions(self):
        """Compte le nombre d'inversions dans le plateau (pour vérifier la résolvabilité)"""
        inv_count = 0
        arr = [x for x in self.board if x != 0]
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] > arr[j]:
                    inv_count += 1
        return inv_count
    
    def get_neighbors(self, pos):
        """Retourne les positions voisines valides"""
        row, col = pos // 3, pos % 3
        neighbors = []
        
        if row > 0:
            neighbors.append(pos - 3)
        if row < 2:
            neighbors.append(pos + 3)
        if col > 0:
            neighbors.append(pos - 1)
        if col < 2:
            neighbors.append(pos + 1)
        
        return neighbors
    
    def show_game_board(self):
        """Affiche le plateau de jeu"""
        self.clear_window()
        
        # Informations
        info_frame = tk.Frame(self.root, bg="#2c3e50")
        info_frame.pack(pady=15)
        
        level_label = tk.Label(
            info_frame,
            text=f"Niveau: {self.difficulty.upper()}",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        level_label.grid(row=0, column=0, columnspan=2, pady=5)
        
        # Temps
        self.time_label = tk.Label(
            info_frame,
            text=f"⏱️ Temps: {self.remaining_time}s",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="#3498db"
        )
        self.time_label.grid(row=1, column=0, padx=20)
        
        # Coups
        if self.moves_limit != float('inf'):
            self.moves_label = tk.Label(
                info_frame,
                text=f"🎯 Coups: {self.moves_count}/{self.moves_limit}",
                font=("Arial", 14, "bold"),
                bg="#2c3e50",
                fg="#e74c3c"
            )
        else:
            self.moves_label = tk.Label(
                info_frame,
                text=f"🎯 Coups: {self.moves_count}",
                font=("Arial", 14, "bold"),
                bg="#2c3e50",
                fg="#95a5a6"
            )
        self.moves_label.grid(row=1, column=1, padx=20)
        
        # Plateau de jeu
        game_frame = tk.Frame(self.root, bg="#2c3e50")
        game_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(9):
            row, col = i // 3, i % 3
            
            if self.board[i] == 0:
                # Case vide - bien visible et désactivée
                btn = tk.Button(
                    game_frame,
                    text="",
                    font=("Arial", 28, "bold"),
                    width=5,
                    height=2,
                    bg="#34495e",
                    relief=tk.SUNKEN,
                    state=tk.DISABLED,
                    disabledforeground="white"
                )
            else:
                # Case avec chiffre - TOUTES sont mobiles et cliquables
                btn = tk.Button(
                    game_frame,
                    text=str(self.board[i]),
                    font=("Arial", 28, "bold"),
                    width=5,
                    height=2,
                    bg="#3498db",
                    fg="white",
                    relief=tk.RAISED,
                    activebackground="#2980b9",
                    cursor="hand2"
                )
                # IMPORTANT: Attacher la commande APRÈS la création du bouton
                btn.config(command=lambda pos=i: self.move_tile(pos))
            
            btn.grid(row=row, column=col, padx=4, pady=4)
            self.buttons.append(btn)
        
        print(f"DEBUG: Plateau créé - Case vide à position {self.empty_pos}")
        print(f"DEBUG: État du plateau: {self.board}")
        
        # Boutons de contrôle
        controls_frame = tk.Frame(self.root, bg="#2c3e50")
        controls_frame.pack(pady=20)
        
        shuffle_btn = tk.Button(
            controls_frame,
            text="🔀 Mélanger",
            font=("Arial", 12, "bold"),
            bg="#9b59b6",
            fg="white",
            width=12,
            command=self.shuffle_board,
            cursor="hand2"
        )
        shuffle_btn.grid(row=0, column=0, padx=8)
        
        restart_btn = tk.Button(
            controls_frame,
            text="🔄 Redémarrer",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=12,
            command=self.restart_game,
            cursor="hand2"
        )
        restart_btn.grid(row=0, column=1, padx=8)
        
        quit_btn = tk.Button(
            controls_frame,
            text="🏠 Menu",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=12,
            command=self.back_to_menu,
            cursor="hand2"
        )
        quit_btn.grid(row=0, column=2, padx=8)
    
    def move_tile(self, pos):
        """Déplace une tuile si possible"""
        if not self.game_running:
            print(f"DEBUG: Jeu non actif")
            return
        
        # Vérifier si adjacent à la case vide
        neighbors = self.get_neighbors(self.empty_pos)
        print(f"DEBUG: Clic sur position {pos} (valeur: {self.board[pos]})")
        print(f"DEBUG: Case vide à position {self.empty_pos}")
        print(f"DEBUG: Voisins de la case vide: {neighbors}")
        
        if pos not in neighbors:
            print(f"DEBUG: Position {pos} n'est PAS adjacente à la case vide!")
            return
        
        print(f"DEBUG: Mouvement VALIDE! Déplacement de {self.board[pos]}")
        
        # Effectuer le déplacement - TOUTES les tuiles peuvent bouger
        self.board[pos], self.board[self.empty_pos] = \
            self.board[self.empty_pos], self.board[pos]
        self.empty_pos = pos
        self.moves_count += 1
        
        # Vérifier et appliquer les contraintes d'échange
        self.check_and_swap_special_numbers()
        
        # Mettre à jour l'affichage
        self.update_board()
        
        # Vérifier victoire
        if self.check_win():
            self.game_running = False
            self.stop_timer()
            self.show_flower_explosion()
            self.root.after(2000, lambda: [
                messagebox.showinfo("Victoire!", "Félicitations pour le travail!"),
                self.back_to_menu()
            ])
        # Vérifier défaite par coups
        elif self.moves_count >= self.moves_limit:
            self.game_running = False
            self.stop_timer()
            messagebox.showwarning("Coups épuisés", "Réfléchissez avant d'agir!")
            self.back_to_menu()
    
    def check_and_swap_special_numbers(self):
        """
        Vérifie si certains chiffres sont adjacents et les échange automatiquement
        - Niveau moyen : échange 3 et 4 s'ils sont proches
        - Niveau difficile : échange 5 et 6 s'ils sont proches
        """
        # Pour le niveau moyen : vérifier 3 et 4
        if self.swap_3_4_when_adjacent:
            pos_3 = self.board.index(3) if 3 in self.board else -1
            pos_4 = self.board.index(4) if 4 in self.board else -1
            
            if pos_3 != -1 and pos_4 != -1:
                # Vérifier s'ils sont adjacents
                if pos_4 in self.get_neighbors(pos_3):
                    print(f"DEBUG: 3 et 4 sont adjacents ! Échange automatique...")
                    self.board[pos_3], self.board[pos_4] = self.board[pos_4], self.board[pos_3]
                    print(f"DEBUG: Nouveau plateau après échange: {self.board}")
        
        # Pour le niveau difficile : vérifier 5 et 6
        if self.swap_5_6_when_adjacent:
            pos_5 = self.board.index(5) if 5 in self.board else -1
            pos_6 = self.board.index(6) if 6 in self.board else -1
            
            if pos_5 != -1 and pos_6 != -1:
                # Vérifier s'ils sont adjacents
                if pos_6 in self.get_neighbors(pos_5):
                    print(f"DEBUG: 5 et 6 sont adjacents ! Échange automatique...")
                    self.board[pos_5], self.board[pos_6] = self.board[pos_6], self.board[pos_5]
                    print(f"DEBUG: Nouveau plateau après échange: {self.board}")
    
    def update_board(self):
        """Met à jour l'affichage du plateau"""
        print(f"DEBUG UPDATE: Plateau actuel: {self.board}, Case vide: {self.empty_pos}")
        
        for i in range(9):
            if self.board[i] == 0:
                self.buttons[i].config(text="", bg="#34495e", state=tk.DISABLED)
            else:
                # Toutes les tuiles sont bleues et mobiles
                self.buttons[i].config(
                    text=str(self.board[i]),
                    bg="#3498db",
                    fg="white",
                    state=tk.NORMAL
                )
                # Réattacher la commande au cas où
                self.buttons[i].config(command=lambda pos=i: self.move_tile(pos))
        
        # Mettre à jour les coups
        if self.moves_limit != float('inf'):
            self.moves_label.config(text=f"🎯 Coups: {self.moves_count}/{self.moves_limit}")
        else:
            self.moves_label.config(text=f"🎯 Coups: {self.moves_count}")
    
    def start_timer(self):
        """Démarre le chronomètre"""
        self.update_timer()
    
    def update_timer(self):
        """Met à jour le chronomètre chaque seconde"""
        if not self.game_running:
            return
        
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.time_label.config(text=f"⏱️ Temps: {self.remaining_time}s")
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            # Temps écoulé
            self.game_running = False
            if self.moves_count < self.moves_limit:
                messagebox.showwarning("Temps écoulé", "Soyez plus rapide prochainement!")
            else:
                messagebox.showinfo("Temps écoulé", "Temps écoulé!")
            self.back_to_menu()
    
    def stop_timer(self):
        """Arrête le chronomètre"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def check_win(self):
        """Vérifie si le puzzle est résolu"""
        return self.board == [1, 2, 3, 4, 5, 6, 7, 8, 0]
    
    def show_flower_explosion(self):
        """Animation d'explosion de fleurs"""
        canvas = tk.Canvas(
            self.root,
            width=650,
            height=700,
            bg="#2c3e50",
            highlightthickness=0
        )
        canvas.place(x=0, y=0)
        
        flowers = []
        colors = ["#ff69b4", "#ff1493", "#ffc0cb", "#ff6347", "#ffd700", 
                  "#ffb6c1", "#ff4500", "#ff8c00", "#ffa500", "#ffff00"]
        
        center_x, center_y = 325, 350
        
        for i in range(60):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(4, 10)
            color = random.choice(colors)
            size = random.randint(10, 25)
            
            flower_parts = []
            
            # Centre de la fleur
            center = canvas.create_oval(
                center_x - 4, center_y - 4,
                center_x + 4, center_y + 4,
                fill="#ffff00", outline=""
            )
            flower_parts.append(center)
            
            # Pétales
            for j in range(6):
                petal_angle = j * (2 * math.pi / 6)
                px = center_x + 10 * math.cos(petal_angle)
                py = center_y + 10 * math.sin(petal_angle)
                petal = canvas.create_oval(
                    px - size//2, py - size//2,
                    px + size//2, py + size//2,
                    fill=color, outline=""
                )
                flower_parts.append(petal)
            
            flowers.append({
                'parts': flower_parts,
                'vx': speed * math.cos(angle),
                'vy': speed * math.sin(angle),
                'gravity': 0.3,
                'life': 70
            })
        
        def animate_flowers(frame=0):
            if frame > 120:
                canvas.destroy()
                return
            
            for flower in flowers:
                if flower['life'] > 0:
                    flower['vy'] += flower['gravity']
                    
                    for part in flower['parts']:
                        canvas.move(part, flower['vx'], flower['vy'])
                    
                    flower['life'] -= 1
                    
                    if flower['life'] < 25:
                        try:
                            for part in flower['parts']:
                                canvas.itemconfig(part, state='hidden' if flower['life'] < 8 else 'normal')
                        except:
                            pass
            
            self.root.after(30, lambda: animate_flowers(frame + 1))
        
        text = canvas.create_text(
            325, 120,
            text="🎉 BRAVO! 🎉",
            font=("Arial", 45, "bold"),
            fill="#ffd700"
        )
        
        animate_flowers()
    
    def shuffle_board(self):
        """Remélange le plateau"""
        if not self.game_running:
            return
        self.initialize_board()
        self.update_board()
    
    def restart_game(self):
        """Redémarre la partie"""
        if not self.game_running:
            return
        self.stop_timer()
        self.start_game(self.difficulty)
    
    def back_to_menu(self):
        """Retourne au menu"""
        self.game_running = False
        self.stop_timer()
        self.show_menu()
    
    def clear_window(self):
        """Efface la fenêtre"""
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    game = PuzzleGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
