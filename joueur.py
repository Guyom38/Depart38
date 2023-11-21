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
    def __init__(self, moteur, index, x, y, nom):
        self.MOTEUR = moteur
        self.index = index
        self.image = pygame.image.load(".ressources/agent.png").convert_alpha()
        self.nom ="(Director)"
      
        ecriture = pygame.font.SysFont('arial', 20) 
        self.image_ombre = ecriture.render( self.nom , True, (0,0,0)) 
        self.image_texte = ecriture.render( self.nom , True, (255,255,255)) 
        
         
        self.x, self.y = x, y
        self.nom = nom
        self.vitesse = 0.1
        self.direction = ENUM_DIR.AUCUN
        
        self.directionPrecedente = ENUM_DIR.AUCUN
        self.seTourne = 0        
       
        self.offsetX, self.offsetY = 0, -60
        
        self.tempo = 0
        self.tempoTimer = time.time()
        
    def position_ecran_x(self):
        return int(round((self.x * VAR.dim) + self.offsetX,0))
    def position_ecran_y(self):
        return int(round((self.y * VAR.dim) + self.offsetY,0))
    
    def position_int_x(self):
        return int(round((self.x * VAR.dim), 0))
    def position_int_y(self):
        return int(round((self.y * VAR.dim), 0))
        
    def toujours_sur_le_terrain(self):
        return (    self.position_int_x() > -1 and self.position_int_x() < self.MOTEUR.TERRAIN.arrayBlocage.shape[0] \
                    and self.position_int_y() > -1 and self.position_int_y() < self.MOTEUR.TERRAIN.arrayBlocage.shape[1]    )            
    
    def collision_avec_decors(self):
        x2, y2 = self.position_int_x(), self.position_int_y()
        collision_coin1 = (self.MOTEUR.TERRAIN.arrayBlocage[x2+4, y2] > 0)
        collision_coin2 = (self.MOTEUR.TERRAIN.arrayBlocage[x2+26, y2+4] > 0)
        
        #pygame.draw.rect(VAR.fenetre, (255,0,0), (x2+4,y2,22,6), 0)        
        return collision_coin1 or collision_coin2
    
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

        
          
        if self.toujours_sur_le_terrain():                
            if self.collision_avec_decors():
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
        VAR.fenetre.blit(self.image, (self.position_ecran_x(), self.position_ecran_y()), self.coordonnees_image_animee())
        VAR.fenetre.blit(self.image_ombre, (self.position_ecran_x()-2, self.position_ecran_y()-64-2))
        VAR.fenetre.blit(self.image_texte, (self.position_ecran_x(), self.position_ecran_y()-64))

    
        
    