import time
import pygame

import variables as VAR

class CObjet:
    def __init__(self, x, y, offX, offY, image):
        self.x, self.y = x, y
        self.offsetX, self.offsetY = offX, offY
        
        self.tempo = 0
        self.tempoTimer = time.time()
        
        self.image = image
        if image.get_height() > VAR.dim:
            self.offsetY = self.offsetY - VAR.dim
    def position_ecran_x(self):
        return int(round((self.x * VAR.dim) + self.offsetX,0))
    def position_ecran_y(self):
        return int(round((self.y * VAR.dim) + self.offsetY,0))
    
    def position_int_x(self):
        return int(round((self.x * VAR.dim), 0))
    def position_int_y(self):
        return int(round((self.y * VAR.dim), 0))
    
    def afficher(self):
        VAR.fenetre.blit(self.image, (self.position_ecran_x(), self.position_ecran_y()))
        
        key = "{:04d}{:04d}{:01d}".format(self.position_ecran_y(), self.position_ecran_x(), 0)
        ecriture = pygame.font.SysFont('arial', 20) 
        image_texte = ecriture.render( key , True, (0,0,0)) 
        VAR.fenetre.blit(image_texte, (self.position_ecran_x()+50, self.position_ecran_y()))
        