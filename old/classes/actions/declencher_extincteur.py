import pygame
import variables as VAR
from fonctions import *
from constantes import *

import time

class CDeclencher_Extincteur:
    def __init__(self, personnage):
        self.MOTEUR = personnage.MOTEUR
        self.PERSONNAGE = personnage
        
        # --- valeur originale
        self.reference_vitesse_du_joueur = self.PERSONNAGE.vitesse
        
        # --- parametres
        self.endurance = 6
        self.repos = 4
        
        self.couleur1 = (97, 185, 110)
        self.couleur2 = (57, 112, 164)
        
    def demarrer(self):
        if not self.PERSONNAGE.MECANIQUE_ACTION.etape: 
            # --- parametrage
            self.PERSONNAGE.MECANIQUE_ACTION.etape = ENUM_PROGRESSION_ETAT.SE_DECHARGE
            self.PERSONNAGE.MECANIQUE_ACTION.configurer(self.endurance, self.couleur1)  
            
            # --- action       
            self.PERSONNAGE.animation = ENUM_ANIMATION.COURIR
            self.PERSONNAGE.vitesse = self.PERSONNAGE.vitesse * 2
            
    
    def cycle(self):
        pass
    
            
    def terminer(self):        
        # --- parametrage
        if self.PERSONNAGE.MECANIQUE_ACTION.etape == ENUM_PROGRESSION_ETAT.SE_DECHARGE:
            self.PERSONNAGE.MECANIQUE_ACTION.etape = ENUM_PROGRESSION_ETAT.SE_RECHARGE
            self.PERSONNAGE.MECANIQUE_ACTION.configurer(self.repos, self.couleur2)            
        else:
            self.PERSONNAGE.MECANIQUE_ACTION.etape = ENUM_PROGRESSION_ETAT.AUCUN
        
        # --- action       
        self.PERSONNAGE.animation = ENUM_ANIMATION.MARCHER
        self.PERSONNAGE.vitesse = self.reference_vitesse_du_joueur
