import time
import pygame

import variables as VAR

class CObjet:
    def __init__(self, moteur, index, x, y, offX, offY, image, etat):
        self.MOTEUR = moteur
        
        self.index = index
        self.x, self.y = x, y
        self.offsetX, self.offsetY = offX, offY
        self.etat = etat
        
        self.tempo = 0
        self.tempoTimer = time.time()
        
        self.image = image
        if image.get_height() > VAR.dim:
            self.offsetY = self.offsetY - (image.get_height() - VAR.dim)
            
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
            fenetre.blit(self.image, (self.position_ecran_x(), self.position_ecran_y()))
        
