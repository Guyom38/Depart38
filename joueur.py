from enum import *
import pygame
import variables as VAR
from fonctions import *
import time

class ENUM_DIR:
    BAS = 270
    GAUCHE = 0
    DROITE = 180
    HAUT = 90
    AUCUN = None

class ENUM_ANIMATION:
    ARRETER = 0
    IDEAL = 1
    MARCHER = 2
    ASSIS = 4
    JOUER_TELEPHONE = 6
    BOUQUINER = 7
    COURIR = 8
    
class CJoueur:
    def __init__(self, moteur, x, y, nom):
        self.MOTEUR = moteur
        
        self.image = pygame.image.load(".ressources/agent.png").convert_alpha()
        self.nom = ["Vincent", "(Director)"]
        
        self.x, self.y = x, y
        self.nom = nom
        self.vitesse = 0.1
        self.direction = ENUM_DIR.AUCUN
        
        self.directionPrecedente = ENUM_DIR.AUCUN
        self.seTourne = 0
        
        self.taille = 10
        self.offsetX, self.offsetY = 0, -8
        
        self.tempo = 0
        self.tempoTimer = time.time()
        
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

        x2 = int(round(self.x * VAR.dim, 0))
        y2 = int(round(self.y * VAR.dim, 0))
                        
        if x2 > -1 and x2 < self.MOTEUR.TERRAIN.arrayBlocage.shape[0] and y2 > -1 and y2 < self.MOTEUR.TERRAIN.arrayBlocage.shape[1] :                
            if self.MOTEUR.TERRAIN.arrayBlocage[x2, y2] == 0 or self.MOTEUR.TERRAIN.arrayBlocage[x2+16, y2+4] == 0:
                self.x, self.y = xo, yo
                self.direction = ENUM_DIR.AUCUN

    
    def coordonnees_image_animee(self):
        if time.time() - self.tempoTimer > 0.1: 
            self.tempo += 1
            self.tempoTimer = time.time()
        
        position_x, position_y, nombre_images = 0, 8, 6
        if self.direction == ENUM_DIR.HAUT: position_x = 1
        elif self.direction == ENUM_DIR.BAS: position_x = 3
        elif self.direction == ENUM_DIR.GAUCHE: position_x = 2
        elif self.direction == ENUM_DIR.DROITE: position_x = 0
        else: position_y, nombre_images = 7, 12
        
        return ( ((position_x * nombre_images)+(self.tempo % nombre_images)) * VAR.dim, (position_y * (VAR.dim *2)), VAR.dim, (VAR.dim *2) )
    
    def afficher(self):   
        joueurX, joueurY = (self.x * VAR.dim) + self.offsetX, (self.y * VAR.dim) + self.offsetY
        
       # ombre = pygame.Surface((16,16), pygame.SRCALPHA)
       # pygame.draw.circle(ombre, (0,0,0, 128), (0,0,16,16)) 
        
       # VAR.fenetre.blit(ombre, (joueurX+6, joueurY+6))
        #pygame.draw.circle(VAR.fenetre, (0,0,0), (joueurX+6, joueurY+6), 16) 
        VAR.fenetre.blit(self.image, (joueurX-10, joueurY-48), self.coordonnees_image_animee())
        
        ecriture = pygame.font.SysFont('arial', 20) 
        image_ombre = ecriture.render( self.nom , True, (0,0,0)) 
        image_texte = ecriture.render( self.nom , True, (255,255,255)) 
        VAR.fenetre.blit(image_ombre, (joueurX-2, joueurY-64-2))
        VAR.fenetre.blit(image_texte, (joueurX, joueurY-64))
        #print(self.tempo)