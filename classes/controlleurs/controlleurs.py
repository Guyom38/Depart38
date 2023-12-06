import pygame
from pygame.locals import *

import time

import variables as VAR
from fonctions import *

from constantes import *
from classes.actions.courrir import *
from classes.controlleurs.clavier import *
from classes.controlleurs.manettes import *

class CControlleurs:
    def __init__(self, moteur):
        self.MOTEUR = moteur

        self.ASSOC_MANETTE_JOUEUR = {}
        self.CLAVIER = CClavier(self)
        self.MANETTES = CManettes(self)
    
    def initialiser(self):
        self.MANETTES.initialiser()
        
    def gestion_des_commandes_utilisateurs(self):
        #
        joueur_zero_bouge = 0
        # --- récupére l'ensemble des évènements
        for event in pygame.event.get():        
            # --- si l'utilisateur clic sur la croix, ou appuie sur la touche ESCAPE
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                VAR.boucle = False
                
            
            
            if event.type in (pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
                joueur_zero_bouge += self.MANETTES.gestion_des_evenements(event)
            else:
                self.CLAVIER.gestion_des_evenements(event)
                
        joueur_zero_bouge += self.CLAVIER.gestion_des_pressions()
        
        if joueur_zero_bouge == 0:
            self.MOTEUR.PERSONNAGES.JOUEURS[0].en_mouvement = False
            
        
    
            
