import time, random
import pygame

import variables as VAR

class CObjet:
    def __init__(self, moteur, index, x, y, offX, offY, liste_images, image_mask, etat):
        self.MOTEUR = moteur
        
        self.index = index
        self.x, self.y = x, y
        self.offsetX, self.offsetY = offX, offY
        self.etat = etat
        
        self.tempo = 0
        self.tempoTimer = time.time()
        self.tempoRnd = random.randint(0, 100)
        
        self.image = liste_images
        self.image_mask = image_mask
        
        #if self.image[0].get_height() > VAR.dim:
        #    self.offsetY = self.offsetY - (self.image[0].get_height() - VAR.dim)
        
        self.rect = self.image[0].get_rect()
             
    def position_ecran_x(self):
        return int(round((self.x * VAR.dim) + self.offsetX,0))
    def position_ecran_y(self):
        return int(round((self.y * VAR.dim) + self.offsetY,0))
    
    def position_int_x(self):
        return int(round((self.x * VAR.dim), 0))
    def position_int_y(self):
        return int(round((self.y * VAR.dim), 0))
    
    def rythme_animation(self):
        if time.time() - self.tempoTimer > 0.5: 
            self.tempo += 1
            self.tempoTimer = time.time()
            
    def afficher(self):
        self.rythme_animation() 

        index = ((self.tempo + self.tempoRnd) % len(self.image)) 
        VAR.fenetre.blit(self.image[index], (self.position_ecran_x(), self.position_ecran_y()))
            
        