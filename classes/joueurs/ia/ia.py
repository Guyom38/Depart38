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
        
        
        self.txt = ""  # Variable pour stocker du texte (utilisation non spécifiée)
         
    # Fonction principale de réflexion de l'IA
    def je_reflechis(self):
        # Si l'IA ne poursuit pas quelqu'un, elle suit son parcours
        if not self.IA_PATHFINDING.il_y_a_t_il_poursuite():
            self.PNJ.changement_equipe(3)
            self.IA_PARCOURS.je_reflechis()
        
        # Sinon, l'IA se réoriente vers son objectif
        else:
            self.PNJ.changement_equipe(4)
            self.IA_PATHFINDING.traque_je_me_reoriente_vers_le_nouveau_point()    

    # Établissement de la direction initiale du PNJ
    def etablir_direction_initiale(self):
        xx, yy = self.PNJ.position_x(), self.PNJ.position_y()  # Position actuelle du PNJ
        directions_possibles = []

        # Vérifie chaque direction possible autour du PNJ
        for direction, offx, offy in [(ENUM_DIR.BAS, 0, 1), (ENUM_DIR.HAUT, 0, -1), (ENUM_DIR.DROITE, 1, 0), (ENUM_DIR.GAUCHE, -1, 0)]:
            if self.MOTEUR.TERRAIN.cellule_est_sur_le_terrain(xx + offx, yy + offy):
                if self.parcours[xx + offx][yy + offy]['CHEMIN']: # Un chemin est-il disponible ?
                    directions_possibles.append(direction)

        # Choix aléatoire d'une direction parmi les possibilités
        if len(directions_possibles) > 0:
            self.PNJ.direction = random.choice(directions_possibles)
        else:
            self.PNJ.direction = ENUM_DIR.AUCUN  # Aucune direction possible

    # Vérifie si le PNJ est au centre de la cellule actuelle
    def est_ce_que_je_suis_au_centre_de_la_cellule(self):
    
        direction = self.PNJ.direction
        #print( str( (round(self.PNJ.x, 2), round(self.PNJ.y, 2), " -- ", (round(self.PNJ.x % 1, 2), round(self.PNJ.y % 1, 2)), " -- ", self.PNJ.direction)) )
        # Vérifie la position du PNJ par rapport à sa direction pour déterminer s'il est au centre
        if direction == ENUM_DIR.BAS and self.PNJ.y % 1 < 0.98:   return False
        elif direction == ENUM_DIR.HAUT and self.PNJ.y % 1 > 0.15:   return False
        elif direction == ENUM_DIR.DROITE and self.PNJ.x % 1 < 0.98:  return False
        elif direction == ENUM_DIR.GAUCHE and self.PNJ.x % 1 > 0.015: return False                      
        return True
