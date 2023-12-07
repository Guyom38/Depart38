import pygame
import variables as VAR
from fonctions import *
from constantes import *

import time

class CPourchasser:
    def __init__(self, personnage, joueur):
        self.MOTEUR = personnage.MOTEUR
        self.PERSONNAGE = personnage
        self.MECANIQUE_ACTION = personnage.MECANIQUE_ACTION
        
        self.JOUEUR_CIBLE = joueur
        
        # --- valeur originale
        self.reference_vitesse_du_joueur = self.PERSONNAGE.vitesse
        self.reference_position = self.PERSONNAGE.position_int_x(), self.PERSONNAGE.position_int_y()
        
        # --- parametres
        self.rage = 10
        self.fatiguer = 3
        
        self.couleur1 = (225, 32, 32)
        self.couleur2 = (57, 112, 164)
        
    def demarrer(self):
        if not self.MECANIQUE_ACTION.etape: 
            # --- parametrage
            self.MECANIQUE_ACTION.etape = ENUM_PROGRESSION_ETAT.SE_DECHARGE
            self.MECANIQUE_ACTION.configurer(self.rage, self.couleur1)  
            
            # --- action       
            self.PERSONNAGE.animation = ENUM_ANIMATION.COURIR
            self.PERSONNAGE.vitesse = self.PERSONNAGE.vitesse * 2
            
            # --- mémorise la position du joueur avant la poursuite
            self.reference_position = self.PERSONNAGE.IA.IA_PATHFINDING.pos_pnj
            
    def cycle(self):  
        x, y = int(self.JOUEUR_CIBLE.x), int(self.JOUEUR_CIBLE.y) 
        self.PERSONNAGE.IA.IA_PATHFINDING.traque_calculer_le_chemin_jusqua( (x, y) )  
            
    def terminer(self):   
        # quand la barre de temps est epuisé, il rentre jusqu'a son chemin
             
        # --- parametrage
        if self.MECANIQUE_ACTION.etape == ENUM_PROGRESSION_ETAT.SE_DECHARGE:
            self.MECANIQUE_ACTION.etape = ENUM_PROGRESSION_ETAT.SE_RECHARGE
            self.MECANIQUE_ACTION.configurer(self.fatiguer, self.couleur2)            
        
        else:
            self.MECANIQUE_ACTION.etape = ENUM_PROGRESSION_ETAT.AUCUN
        
        # --- action       
        self.PERSONNAGE.animation = ENUM_ANIMATION.MARCHER
        self.PERSONNAGE.vitesse = self.reference_vitesse_du_joueur
        
        # --- retourne a la position ou le pnj était
        if not self.reference_position == None:
            x, y = self.reference_position
            self.PERSONNAGE.IA.IA_PATHFINDING.traque_calculer_le_chemin_jusqua((x, y))  
            print("Retourner a la maison ...")
        #self.chemin_pathfinding = []
