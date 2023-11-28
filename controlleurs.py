import pygame
from pygame.locals import *

import time

import variables as VAR
from fonctions import *

from constantes import *


class CControlleurs:
    def __init__(self, moteur):
        self.MOTEUR = moteur
        self.PERSONNAGES = self.MOTEUR.PERSONNAGES

    def clavier(self):
        # --- récupére l'ensemble des évènements
        for event in pygame.event.get():        
            # --- si l'utilisateur clic sur la croix, ou appuie sur la touche ESCAPE
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                VAR.boucle = False

            # --- si l'utilisateur presse l'une des fleches de direction
            if event.type == KEYDOWN:  
                if event.key in [ENUM_DIR.GAUCHE, ENUM_DIR.DROITE, ENUM_DIR.HAUT, ENUM_DIR.BAS]:
                    self.PERSONNAGES.JOUEURS[0].directionPrecedente  = self.PERSONNAGES.JOUEURS[0].direction
                    self.PERSONNAGES.JOUEURS[0].seTourne = True
                        
                if event.key == K_LEFT:                         
                    self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.GAUCHE
                if event.key == K_RIGHT: 
                    self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.DROITE
                if event.key == K_UP: 
                    self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.HAUT
                if event.key == K_DOWN: 
                    self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.BAS
                if event.key == K_SPACE:
                    self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.AUCUN 