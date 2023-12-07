import pygame
import fonctions as FCT
import variables as VAR
from constantes import *
import random

from classes.joueurs.ia.ia_parcours import *
from classes.joueurs.ia.ia_pathfinding import *

class CIA:
    # Initialisation de l'instance CIA
    def __init__(self, moteur, personnage):
        self.MOTEUR = moteur  # Référence au moteur de jeu
        self.PNJ = personnage  # Référence au Personnage Non-Joueur (PNJ) associé
        
        # Initialisation des modules de parcours et de pathfinding
        self.IA_PARCOURS = CIA_PARCOURS(self)
        self.IA_PATHFINDING = CIA_PATHFINDING(self)
        
        self.parcours = []  # Liste pour stocker le parcours
        
        self.position_precedente = (-1, -1)  # Mémorisation de la dernière position du PNJ
        self.x, self.y, self.xInt, self.yInt = 0, 0, 0, 0  # Position actuelle et entière du PNJ
        self.txt = ""  # Variable pour stocker du texte (utilisation non spécifiée)
         
    # Fonction principale de réflexion de l'IA
    def je_reflechis(self):
        self.je_recupere_ma_position_sur_le_terrain()  # Mise à jour de la position du PNJ
        
        # Si l'IA ne poursuit pas quelqu'un, elle suit son parcours
        if not self.IA_PATHFINDING.traque_est_ce_que_je_poursuis_quelquun():
            self.PNJ.changement_equipe(3)
            self.IA_PARCOURS.je_reflechis()
        
        # Sinon, l'IA se réoriente vers son objectif
        else:
            self.PNJ.changement_equipe(4)
            self.IA_PATHFINDING.traque_je_me_reoriente_vers_le_nouveau_point()    

    # Établissement de la direction initiale du PNJ
    def etablir_direction_initiale(self):
        self.je_recupere_ma_position_sur_le_terrain()
            
        x, y = self.xInt, self.yInt  # Position actuelle du PNJ
        directions_possibles = []

        # Vérifie chaque direction possible autour du PNJ
        for direction, offx, offy in [(ENUM_DIR.BAS, 0, 1), (ENUM_DIR.HAUT, 0, -1), (ENUM_DIR.DROITE, 1, 0), (ENUM_DIR.GAUCHE, -1, 0)]:
            if self.IA_PARCOURS.est_sur_le_terrain(x + offx, y + offy) and self.parcours[x + offx][y + offy]['CHEMIN']:
                directions_possibles.append(direction)

        # Choix aléatoire d'une direction parmi les possibilités
        if directions_possibles:
            self.PNJ.direction = random.choice(directions_possibles)
        else:
            self.PNJ.direction = ENUM_DIR.AUCUN  # Aucune direction possible

    # Mise à jour de la position du PNJ sur le terrain
    def je_recupere_ma_position_sur_le_terrain(self):
        self.x, self.y = self.PNJ.x, self.PNJ.y
        self.xInt, self.yInt = int(self.PNJ.x), int(self.PNJ.y)   

    # Vérifie si le PNJ est au centre de la cellule actuelle
    def est_ce_que_je_suis_au_centre_de_la_cellule(self):
        direction = self.PNJ.direction

        # Vérifie la position du PNJ par rapport à sa direction pour déterminer s'il est au centre
        if direction == ENUM_DIR.BAS and self.PNJ.y % 1 < 0.48:   return False
        elif direction == ENUM_DIR.HAUT and self.PNJ.y % 1 > 0.48:   return False
        elif direction == ENUM_DIR.DROITE and self.PNJ.x % 1 < 0.015:  return False
        elif direction == ENUM_DIR.GAUCHE and self.PNJ.x % 1 > 0.015: return False                      
        return True
