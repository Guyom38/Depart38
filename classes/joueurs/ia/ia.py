import pygame
import fonctions as FCT
import variables as VAR
from constantes import *
import random


from classes.joueurs.ia.ia_parcours import *
from classes.joueurs.ia.ia_pathfinding import *

class CIA:
    def __init__(self, moteur, personnage):
        # Initialisation du PNJ avec le moteur de jeu et le personnage
        self.MOTEUR = moteur
        self.PNJ = personnage
        
        
        self.IA_PARCOURS = CIA_PARCOURS(self)
        self.IA_PATHFINDING = CIA_PATHFINDING(self)
        
        self.parcours = []

        
        # Mémorisation de la dernière position du PNJ
        self.position_precedente = (-1, -1)
        #self.champ_vision = 60
       
        self.x, self.y, self.xInt, self.yInt = 0, 0, 0, 0
        self.txt = ""
        
         
    def je_reflechis(self):
        self.je_recupere_ma_position_sur_le_terrain()       
        
        # --- je suis mon parcours ...
        if not self.IA_PATHFINDING.traque_est_ce_que_je_poursuis_quelquun():
            self.IA_PARCOURS.je_reflechis()  
        
        # --- je me rend vers quelques choses
        else:
            self.IA_PATHFINDING.traque_je_me_reoriente_vers_le_nouveau_point()    
           
            
            
             

    def etablir_direction_initiale(self):
        self.je_recupere_ma_position_sur_le_terrain()
            
        x, y = self.xInt, self.yInt  # Position actuelle du PNJ
        directions_possibles = []

        # Vérifier chaque direction autour du PNJ pour les chemins possibles
        for direction, offx, offy in [(ENUM_DIR.BAS, 0, 1), (ENUM_DIR.HAUT, 0, -1), (ENUM_DIR.DROITE, 1, 0), (ENUM_DIR.GAUCHE, -1, 0)]:
            if self.IA_PARCOURS.est_sur_le_terrain(x + offx, y + offy):
                if self.parcours[x + offx][y + offy]['CHEMIN']:
                    directions_possibles.append(direction)

            # Choisir une direction au hasard parmi les directions possibles
        if len(directions_possibles) > 0:
            self.PNJ.direction = random.choice(directions_possibles)
        else:
            self.PNJ.direction = ENUM_DIR.AUCUN  # Aucune direction possible   


 
           
    def je_recupere_ma_position_sur_le_terrain(self):
        self.x, self.y = self.PNJ.x, self.PNJ.y
        self.xInt, self.yInt = int(self.PNJ.x), int(self.PNJ.y)   

    def est_ce_que_je_suis_au_centre_de_la_cellule(self):
        direction = self.PNJ.direction

        if direction   == ENUM_DIR.BAS    and self.PNJ.y % 1 < 0.48:   return False
        elif direction == ENUM_DIR.HAUT   and self.PNJ.y % 1 > 0.48:   return False
        elif direction == ENUM_DIR.DROITE and self.PNJ.x % 1 < 0.015:  return False
        elif direction == ENUM_DIR.GAUCHE and self.PNJ.x % 1 > 0.015 : return False                      
        return True
    
    
                
    

    