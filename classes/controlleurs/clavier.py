import pygame
from pygame.locals import *

import time

import variables as VAR
from fonctions import *

from constantes import *
from classes.actions.courrir import *

class CClavier:
    def __init__(self, controlleurs):
        self.MOTEUR = controlleurs.MOTEUR
        self.CONTROLLEURS = controlleurs
        
        self.PERSONNAGES = self.MOTEUR.PERSONNAGES

        
    def gestion_des_evenements(self, event):       

        if event.type == KEYDOWN:        
            if event.key == K_SPACE:            
                self.PERSONNAGES.JOUEURS[0].MECANIQUE_ACTION.demarrer(CCourir(self.PERSONNAGES.JOUEURS[0]))

    def gestion_des_pressions(self):
        joueur_zero_bouge = 0
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP] == 1:
            self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.HAUT
            self.PERSONNAGES.JOUEURS[0].en_mouvement = True
            joueur_zero_bouge += 1
        elif keys[pygame.K_DOWN] == 1:
            self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.BAS
            self.PERSONNAGES.JOUEURS[0].en_mouvement = True
            joueur_zero_bouge += 1
        elif keys[pygame.K_LEFT] == 1:
            self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.GAUCHE
            self.PERSONNAGES.JOUEURS[0].en_mouvement = True
            joueur_zero_bouge += 1
        elif keys[pygame.K_RIGHT] == 1:
            self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.DROITE
            self.PERSONNAGES.JOUEURS[0].en_mouvement = True
            joueur_zero_bouge += 1
            
        return joueur_zero_bouge