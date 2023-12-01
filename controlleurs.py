import pygame
from pygame.locals import *

import time

import variables as VAR
from fonctions import *

from constantes import *
from classes.actions.courrir import *


class CControlleurs:
    def __init__(self, moteur):
        self.MOTEUR = moteur
        self.PERSONNAGES = self.MOTEUR.PERSONNAGES

    def clavier(self):
        self.PERSONNAGES.JOUEURS[0].en_mouvement = False
        # --- récupére l'ensemble des évènements
        for event in pygame.event.get():        
            # --- si l'utilisateur clic sur la croix, ou appuie sur la touche ESCAPE
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                VAR.boucle = False

            if event.type == KEYDOWN:        
                if event.key == K_SPACE:            
                    action_a_entreprendre = CCourir(self.PERSONNAGES.JOUEURS[0])           
                    self.PERSONNAGES.JOUEURS[0].MECANIQUE_ACTION.demarrer(action_a_entreprendre)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] == 1:
            self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.HAUT
            self.PERSONNAGES.JOUEURS[0].en_mouvement = True
        elif keys[pygame.K_DOWN] == 1:
            self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.BAS
            self.PERSONNAGES.JOUEURS[0].en_mouvement = True
        elif keys[pygame.K_LEFT] == 1:
            self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.GAUCHE
            self.PERSONNAGES.JOUEURS[0].en_mouvement = True
        elif keys[pygame.K_RIGHT] == 1:
            self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.DROITE
            self.PERSONNAGES.JOUEURS[0].en_mouvement = True
            
        if keys[pygame.K_SPACE] == 1:
            VAR.demo = [ENUM_DEMO.BLOCAGE]
        else:
            VAR.demo = []

                