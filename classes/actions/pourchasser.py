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
        
        self.IA_PARCOURS = self.PERSONNAGE.IA.IA_PARCOURS
        self.IA_PATHFINDING = self.PERSONNAGE.IA.IA_PATHFINDING
      
        self.JOUEUR_CIBLE = joueur
        
        # --- valeur originale
        self.reference_vitesse_du_joueur = self.PERSONNAGE.vitesse
        self.reference_position = self.PERSONNAGE.position_x(), self.PERSONNAGE.position_y()
        
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
            

    def cycle(self):
        
        if self.MECANIQUE_ACTION.etape == ENUM_PROGRESSION_ETAT.SE_DECHARGE: 
            xx, yy = self.JOUEUR_CIBLE.position_x(), self.JOUEUR_CIBLE.position_y() 
            self.IA_PATHFINDING.traque_calculer_le_chemin_jusqua( (xx, yy) )  
            
        elif self.MECANIQUE_ACTION.etape == ENUM_PROGRESSION_ETAT.OBJECTIF_ATTEINT:   
            # --- reprend le cours de sa vie ...
            if len(self.IA_PATHFINDING.chemin) == self.IA_PATHFINDING.index_chemin:
                self.IA_PATHFINDING.chemin = []
                self.IA_PATHFINDING.index_chemin = 0
                self.MECANIQUE_ACTION.etape = ENUM_PROGRESSION_ETAT.AUCUN

             
        self.DEBUG_afficher_position_initiale()
        
     

                
    def terminer(self):  
        
        # quand la barre de temps est epuisé, il rentre jusqu'a son chemin
             
        # --- parametrage
        if self.MECANIQUE_ACTION.etape == ENUM_PROGRESSION_ETAT.SE_DECHARGE: 
            self.MECANIQUE_ACTION.etape = ENUM_PROGRESSION_ETAT.SE_RECHARGE            
            self.MECANIQUE_ACTION.configurer(self.fatiguer, self.couleur2) 
            
            # --- action       
            self.PERSONNAGE.vitesse = 3            
            # --- retourne a la position ou le pnj était        
            xx, yy = self.IA_PARCOURS.position_precedente
            self.IA_PATHFINDING.traque_calculer_le_chemin_jusqua((xx, yy))  
     
        
        elif self.MECANIQUE_ACTION.etape == ENUM_PROGRESSION_ETAT.SE_RECHARGE:
            self.MECANIQUE_ACTION.etape = ENUM_PROGRESSION_ETAT.OBJECTIF_ATTEINT            
            self.PERSONNAGE.animation = ENUM_ANIMATION.MARCHER
            self.PERSONNAGE.vitesse = self.reference_vitesse_du_joueur
            
        
        
       
       
       
       
       
       
       
       
       
    def DEBUG_afficher_position_initiale(self):   
        # --- affiche le repere avant la chasse
        if ENUM_DEMO.CHEMIN_VINCENT in VAR.demo:
            if not self.reference_position == None:
                xx, yy = self.reference_position
                pygame.draw.circle(VAR.fenetre, (32,32,255), ((xx * VAR.dim) + 12, (yy * VAR.dim) + 12), 8, 0)   