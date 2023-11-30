import time
import pygame

import variables as VAR

class CObjet:
    def __init__(self, moteur, index, x, y, offX, offY, image, image_mask, etat):
        self.MOTEUR = moteur
        
        self.index = index
        self.x, self.y = x, y
        self.offsetX, self.offsetY = offX, offY
        self.etat = etat
        
        self.tempo = 0
        self.tempoTimer = time.time()
        
        self.image = image
        self.image_mask = image_mask
        
        if image.get_height() > VAR.dim:
            self.offsetY = self.offsetY - (image.get_height() - VAR.dim)
        
        self.rect = image.get_rect()
             
    def position_ecran_x(self):
        return int(round((self.x * VAR.dim) + self.offsetX,0))
    def position_ecran_y(self):
        return int(round((self.y * VAR.dim) + self.offsetY,0))
    
    def position_int_x(self):
        return int(round((self.x * VAR.dim), 0))
    def position_int_y(self):
        return int(round((self.y * VAR.dim), 0))
    
    def afficher(self, fenetre = None):
        if fenetre == None:
            VAR.fenetre.blit(self.image, (self.position_ecran_x(), self.position_ecran_y()))
        else:            
            image_a_utlisee = self.image if self.image_mask == None else self.image_mask
            fenetre.blit(image_a_utlisee, (self.position_ecran_x(), self.position_ecran_y()))