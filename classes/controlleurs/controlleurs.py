import pygame
from pygame.locals import *

import time

import variables as VAR
from fonctions import *

from constantes import *
from classes.actions.courrir import *
from classes.controlleurs.clavier import *

class CControlleurs:
    def __init__(self, moteur):
        self.MOTEUR = moteur

        self.CLAVIER = CClavier(self.MOTEUR)
        
    def gestion_des_commandes_utilisateurs(self):
        self.CLAVIER.gestion_clavier()

    
            
