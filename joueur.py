from enum import *
import pygame
import variables as VAR
from fonctions import *

class ENUM_DIR:
    BAS = 270
    GAUCHE = 0
    DROITE = 180
    HAUT = 90
    AUCUN = None
    
class CJoueur:
    def __init__(self, moteur, x, y, nom):
        self.MOTEUR = moteur
        
        self.x, self.y = x, y
        self.nom = nom
        self.vitesse = 0.1
        self.direction = ENUM_DIR.AUCUN
        
        self.directionPrecedente = ENUM_DIR.AUCUN
        self.seTourne = 0
        
        self.taille = 10
        self.offsetX, self.offsetY = ((VAR.dim - self.taille) // 2), ((VAR.dim - self.taille) // 2)
        
    def se_deplace(self):
        xo, yo = self.x, self.y
        if self.direction == ENUM_DIR.GAUCHE:
            self.x = self.x - VAR.pas
        elif self.direction == ENUM_DIR.DROITE:
            self.x = self.x + VAR.pas
        elif self.direction == ENUM_DIR.HAUT:
            self.y = self.y - VAR.pas
        elif self.direction == ENUM_DIR.BAS:
            self.y = self.y + VAR.pas

        x2 = int(round(self.x * VAR.dim, 0))+ self.offsetX
        y2 = int(round(self.y * VAR.dim, 0))+ self.offsetY
                        
        if x2 > -1 and x2 < self.MOTEUR.TERRAIN.arrayBlocage.shape[0] and y2 > -1 and y2 < self.MOTEUR.TERRAIN.arrayBlocage.shape[1] :                
            if self.MOTEUR.TERRAIN.arrayBlocage[x2, y2] == 0:
                self.x, self.y = xo, yo
                d = 0
    
    def afficher(self):
        
        
        joueurX, joueurY = (self.x * VAR.dim) + self.offsetX, (self.y * VAR.dim) + self.offsetY
        pygame.draw.rect(VAR.fenetre, (255,0,255), (joueurX, joueurY, self.taille, self.taille), 4) 
       