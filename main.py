import pygame as py
import random


SCREEN_WIDTH = 500  # Largeur de la fenêtre
SCREEN_HEIGHT = 500 # Hauteur de la fenêtre
GRID_SIZE = 50      # Taille d'une cellule de la grille
FPS = 60            # Nombre d'images par seconde


# ci-dessous, des constantes qui représentent des couleurs. Si vous voulez utiliser une couleur non présente dans la liste, vous pouvez utiliser un tuple de 3 nombres compris entre 0 et 255, qui représentent les valeurs de rouge, vert et bleu. (c'est le RGB)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


def isCollision(obj1,obj2):
   return obj1.colliderect(obj2)




def load_image(path):
   """
   Une fonction qui charge une image et la retourne.
   Si l'image n'est pas trouvée, une image avec le texte "ERROR" est retournée.
   """
   try:
       return py.image.load(path)
   except:
       fFont = py.font.Font(None, 36)
       health = fFont.render(f"ERROR", True, (255, 255, 0))
       return health


def create_grid():
   """
   Permet de créer une grille de cellules de la taille de la fenêtre.
   """
   grid = []
   for x in list(range(0, SCREEN_WIDTH, GRID_SIZE)):
       for y in list(range(0, SCREEN_HEIGHT, GRID_SIZE)):
           grid.append((x, y))
   return grid


class Projectile:
   """
   Classe qui représente un projectile. (lançé par une tour)
   """
   def __init__(self, x, y):
       self.image_path = "assets/ennemie.png"               # Chemin vers l'image du projectile
       self.image = load_image(self.image_path)                # Chargement de l'image
       font = py.font.Font(None, 36)
       self.image  = font.render("-", True, (0, 0, 0))
       self.image = py.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))   # Redimensionnement de l'image


       self.x = x                                           # Position sur l'axe x du projectile
       self.y = y - self.image.get_rect().height / 2                                                # Position sur l'axe y du projectile
       self.speed = 3                                       # Vitesse du projectile


   def draw(self, screen):
       screen.blit(self.image, (self.x, self.y))


   def update(self):
       self.x += self.speed # On met à jour la position du projectile


class Tower:
   def __init__(self, x, y, price):
       self.health = 100                                                      
       #self.image_path = "assets/flower.png"                                  
       #self.image = load_image(self.image_path)        
       self.price = price                        
       fFont = py.font.Font(None, 36)
       self.image  = fFont.render("X", True, (self.health % 255, 0, 0))
       self.image = py.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))     # Redimensionnement de l'image à la taille d'une cellule de la grille
       self.x = x                                                              # Position sur l'axe x de la tour
       self.y = y                                                              # Position sur l'axe y de la tour
       self.projectile_cooldown = 60 * 2                                           # Temps entre chaque projectile
       self.projectile_timer = 0                                               # Compteur pour le temps entre chaque projectile
       self.projectiles = []                                                   # Liste des projectiles


   def draw(self, screen):
       screen.blit(self.image, (self.x, self.y)) # On dessine l'image de la tour


       for projectile in self.projectiles: # On dessine tout les projectiles de la tour
           projectile.draw(screen)


   def shoot(self):
       """
       Permet de faire tirer une projectile par la tour.
       """
       x = self.x + GRID_SIZE  # On place le projectile à la position de la tour, mais décalé de la taille d'une cellule de la grille en x
       y = self.y + GRID_SIZE // 2  # On place le projectile à la position de la tour, mais décalé de la moitié de la taille d'une cellule de la grille en y
       self.projectiles.append(Projectile(x, y))   # On ajoute le projectile à la liste des projectiles


   def update(self):
       if self.projectile_timer >= self.projectile_cooldown: # Si le compteur est supérieur au temps entre chaque projectile, alors on fait tirer la tour
           self.shoot()
           self.projectile_timer = 0
       else: # Sinon, on incrémente le compteur
           self.projectile_timer += 1


       for projectile in self.projectiles: # On met à jour tout les projectiles de la tour
           projectile.update()
           if projectile.x > SCREEN_WIDTH:
               self.projectiles.remove(projectile)


class Attacker:
   def __init__(self, x, y, health):
       self.health = health                                                    # Points de vie du attaquant
       # self.image_path = "assets/zombie.png"                                   # Chemin vers l'image du attaquant
       # self.image = load_image(self.image_path)                                # Chargement de l'image
       #self.image = py.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))     # Redimensionnement de l'image à la taille d'une cellule de la grille
       font = py.font.Font(None, 36)
       self.maxHealth = self.health % 255
       self.image = font.render("O", True, (self.health % 255, 0, 0))

       self.x = x                                                              # Position sur l'axe x du attaquant
       self.y = y + self.image.get_rect().height / 2                                                       # Position sur l'axe y du attaquant
       self.speed = 2                                                          # Vitesse de déplacement du attaquant


   def draw(self, screen):
       screen.blit(self.image, (self.x, self.y))


   def update(self):
       self.x -= self.speed # On met à jour la position du attaquant en le déplaçant vers la gauche
  
          


class Game:
   """
   La classe principale du jeu, qui gère les événements, la logique et le rendu.
   """
   def __init__(self):
       """
       Constructeur de la classe Game.
       Cette fonction est appelée lorsqu'on crée un objet de type Game, et elle initialise les attributs de la classe à leur valeur par défaut.
       """
       self.screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # Création de la fenêtre, avec une taille de 500x500 pixels (largeur x hauteur)
       py.display.set_caption("Plants vs. Zombies")                        # Définition du titre de la fenêtre
       self.running = True        
       self.health = 100                                        
       self.money = 30                                                   
       self.towers = []                                                  
       self.attackers = []                                                 # Liste des zombies
       self.selected_cell = None                                           # Cellule sélectionnée par le joueur (pour placer une tour)
       self.zombie_spawn_timer = 0                                         # Compteur pour l'apparition des zombies
       self.grid = create_grid()                                           # Création de la grille
       self.fps = py.time.Clock()                                          # Création d'un objet qui permet de gérer les IPS (images par seconde)
       self.round = 1
       self.appearedZombie = 0
       self.nbrOfRounds = 100
   def events(self):
       """
       Cette fonction gère les événements enrégistrés par Pygame, comme le clic de la souris ou la fermeture de la fenêtre.
       """
       for event in py.event.get():
           if event.type == py.QUIT: # Si dans les evenements pygame, il y a un événement de type QUIT, alors on arrête le jeu
               self.stop()
           x, y = py.mouse.get_pos()
           if event.type == py.MOUSEBUTTONDOWN: # Si dans les evenements pygame, il y a un événement de type MOUSEBUTTONDOWN, et que l'on passe tout les checks, alors on place une tour
               for cell in self.grid:
                   cell_x, cell_y = cell # c'est une tuple de 2 nombres, le premier est la position en x, le deuxième est la position en y
                   mouseRect = py.Rect(x,y,1,1)
                   cellRect = py.Rect(cell_x, cell_y, GRID_SIZE, GRID_SIZE)
                   if (mouseRect.colliderect(cellRect)): # Ici, on vérifie si les coordonnées de la cellule et les coordonnées de la souris se chevauchent
                       cell_occupied = False
                       for tower in self.towers:
                           if tower.x == cell_x and tower.y == cell_y:
                               cell_occupied = True
                          
                          
                       if not cell_occupied and self.money >= 10: # Placer une tour coûte 10 points et on ne peut pas placer une tour sur une cellule déjà occupée
                          
                           tower = Tower(cell_x, cell_y, 10)
                           self.towers.append(tower)
                           self.money -= tower.price


   def update(self):
       """
       Cette fonction met à jour la logique du jeu, comme la position des zombies, des tours, etc.
       """


       for tower in self.towers: # Mise à jour des tours
           tower.update()


       for attacker in self.attackers: # Mise à jour des zombies
           attacker.update()


       for attacker in self.attackers: # Ici l'on gère les collisions naïvement, en vérifiant si les coordonnées de tout les zombies avec toutes les tours
           for tower in self.towers:
               attackerRect = py.Rect(attacker.x, attacker.y, GRID_SIZE, GRID_SIZE)
               towerRect = py.Rect(tower.x, tower.y, GRID_SIZE, GRID_SIZE) 
               for projectile in tower.projectiles:
                   projectileRect = py.Rect(projectile.x, projectile.y, GRID_SIZE, GRID_SIZE)
                   if isCollision(projectileRect, attackerRect):
                       attacker.health -= 50
                       tower.projectiles.remove(projectile)
                       if attacker.health == 0:
                           self.money += attacker.maxHealth * 0.05
                           self.attackers.remove(attacker)
                          
               if isCollision(attackerRect, towerRect): # Ici, on vérifie si les coordonnées de la tour et du attaquant qu'on compare se chevauchent
                   self.towers.remove(tower)
                   if self.attackers.index(attacker):
                    self.attackers.remove(attacker)

                    self.health -=  40
           if attacker.x < GRID_SIZE:
               self.attackers.remove(attacker)
               self.health -= attacker.health * 0.25


       self.zombie_spawn_timer += 1
       if self.zombie_spawn_timer > 60 * (3 / self.round): # On fait apparaître un attaquant toutes les 5 secondes (possible grace à la limite de 60 images par seconde)
           self.attackers.append(Attacker(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT / GRID_SIZE) * GRID_SIZE, random.randint(1, self.round + 1) * 100))
           self.zombie_spawn_timer = 0
           self.appearedZombie += 1
           if self.appearedZombie % 4 == 1:
               self.round += 1
              


       # Ajouter ici, toute la logique supplémentaire nécessaire pour mettre à jour le jeu et permettre son bon fonctionnement
       # -La collision entre les projectiles et les attaquants
       # -La collision entre tours et attaquants
       # -L'arrivée des attaquants à la fin de l'écran (dans un tower defense, c'est la fin de la partie)
       # -La gestion du score
       # -Quand un attaquant meurt, il doit être retiré de la liste des attaquants idem pour les tours
       # -etc.


   def draw(self):
       """
       Ici l'on dessine tout les éléments du jeu sur la fenêtre.
       L'order dans lequel les éléments sont dessinés est important, car il détermine l'ordre dans lequel les éléments sont affichés : les éléments dessinés en dernier sont affichés au dessus des autres.
       """
       self.screen.fill(WHITE) # Appelé en premier pour avoir un fond blanc


       for x in list(range(0, SCREEN_WIDTH,GRID_SIZE)): # Dessin de la grille avec des rectangles
           for y in list(range(0, SCREEN_HEIGHT,GRID_SIZE)):
               py.draw.rect(self.screen, GREEN, (x, y, GRID_SIZE, GRID_SIZE), 1)


       for tower in self.towers: # Dessin les tours
           tower.draw(self.screen)


       for attacker in self.attackers: # Dessin les attaquants
           attacker.draw(self.screen)


       # Dessin du score
       fHealth = py.font.Font(None, 32)
       fMoney = py.font.Font(None, 16)
       fRound = py.font.Font(None, 16)
       fMessage = py.font.Font(None, 32)

       money_text = fHealth.render(f"{self.money}$", True, (255, 255, 0))
       health_text = fHealth.render(f"{self.health}%", True, (0, 255, 0))
       round_text = fRound.render(f"{self.round} / {self.nbrOfRounds}", True, (0, 0, 0))
       result_text = fMessage.render(f"Vous avez gagner, score : {self.health}", True, (0, 0, 0))
       perdu_text = fMessage.render(f"Vous avez perdu !", True, (0, 0, 0))

       money_text_rect = money_text.get_rect()
       health_text_rect = health_text.get_rect()
       round_text_rect = round_text.get_rect()
       result_text_rect = result_text.get_rect()
       perdu_text_rect = perdu_text.get_rect()
       
       self.screen.blit(round_text, ((SCREEN_WIDTH / 4) - round_text_rect.width / 2, 20))
       self.screen.blit(health_text, (SCREEN_WIDTH  - health_text_rect.width * 2 , 20))
       self.screen.blit(money_text, (0, 0))
      
      
       if self.round >= self.nbrOfRounds:
           self.clear()
           self.screen.blit(result_text, ((SCREEN_WIDTH / 2) - result_text_rect.width / 2, (SCREEN_HEIGHT / 2) - result_text_rect.height))
       if self.health < 0:
           self.clear()
           self.screen.blit(perdu_text, ((SCREEN_WIDTH / 2) - perdu_text_rect.width / 2, (SCREEN_HEIGHT / 2) - perdu_text_rect.height)), ((SCREEN_WIDTH / 2) - perdu_text_rect.width / 2, (SCREEN_HEIGHT / 2) - perdu_text_rect.height)
          


       py.display.flip()


   def clear (self):
       self.attackers.clear()
       self.towers.clear()
       self.round = self.round
      
   def stop(self):
       self.running = False


def main():
   py.init()
   game = Game()


   while game.running:
       game.fps.tick(FPS) # On limite le nombre d'images par seconde à 60, pour que la vitesse du jeu soit la même sur tout les ordinateurs et ne soit pas dépendante de la puissance de l'ordinateur
       game.events()
       game.update()
       game.draw()


   py.quit()




if __name__ == "__main__":
   main()




