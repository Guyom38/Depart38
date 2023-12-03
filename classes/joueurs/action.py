
import pygame
import variables as VAR
from fonctions import *
from constantes import *
import time

class CAction:
    def __init__(self, personnage):
        self.MOTEUR = personnage.MOTEUR
        self.PERSONNAGE = personnage
        self.ACTION = None
        
        self.timer = time.time()
        self.temps = 10
        self.etape = ENUM_PROGRESSION_ETAT.AUCUN
        
        self.couleur_cadre_bordure = (200,200,200)
        self.couleur_cadre_fond = (32,32,32)
        self.couleur = (255,0,0)
        
        self.hauteur_cadre = VAR.dim // 3
    
    
    
    def configurer(self, temps, couleur):  
        self.timer = time.time()
        self.temps = temps
        self.couleur = couleur        
             
    def demarrer(self, action):  
        if not self.etape:
            self.ACTION = action 
            self.ACTION.demarrer()
                 
    def arreter(self):
        self.ACTION = None
        self.etape = ENUM_PROGRESSION_ETAT.AUCUN
        
        
        
    def calcul_largeur_barre_progression(self):
         # --- calcul le temps passé
        if self.etape == ENUM_PROGRESSION_ETAT.SE_DECHARGE:
            position = self.temps - (time.time() - self.timer)
            est_arrive_au_bout = (position < 0)
            
        elif self.etape == ENUM_PROGRESSION_ETAT.SE_RECHARGE:
            position = (time.time() - self.timer)
            est_arrive_au_bout = (position >= self.temps)
            
        return position, est_arrive_au_bout
    
    def traitement(self):
        # --- cycle de l'action
        if not self.ACTION == None:
            self.ACTION.cycle()
        
        position, est_arrive_au_bout = self.calcul_largeur_barre_progression()
        
        # --- action terminée              
        if est_arrive_au_bout:                        
            if not self.ACTION == None:
                self.ACTION.terminer()                
            self.timer = time.time()
            
        return position
    
    
    def afficher(self,x ,y):
        # --- sort si il n'y a pas de progression dans le temps
        if not self.etape:
            return        
        
        position_progressîon = self.traitement()
            
        # --- déduit les valeurs pour le graphisme
        dimx = self.PERSONNAGE.image_nom.get_width()
        valeurx = int((dimx / self.temps) * position_progressîon)
        y -= self.hauteur_cadre
        
        # --- dessine fond du cadre   
        pygame.draw.rect(VAR.fenetre, self.couleur_cadre_fond, (x, y, dimx, self.hauteur_cadre), 0)
        # --- dessine progression dans le cadre
        pygame.draw.rect(VAR.fenetre, self.couleur, (x, y, valeurx, self.hauteur_cadre), 0)