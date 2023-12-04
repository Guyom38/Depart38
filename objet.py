import time, random
import pygame

import variables as VAR



class CObjet:
    def __init__(self, moteur, index, x, y, offX, offY, liste_images, image_mask, etat, parametres_objet):
        self.MOTEUR = moteur
        
        self.index = index
        self.x, self.y = x, y
        self.offsetX, self.offsetY = offX, offY
        self.etat = etat
        
        self.objet_utilisable = (False if parametres_objet == None else parametres_objet[4])
        
        self.tempo = 0
        self.tempoTimer = time.time()
        self.tempoRnd = random.randint(0, 100)
        
        self.image = liste_images
        self.image_mask = image_mask
                
        self.rect = self.image[0].get_rect()
             
    def position_pixel_x(self):
        return int(round((self.x * VAR.dim) + self.offsetX,0))
    def position_pixel_y(self):
        return int(round((self.y * VAR.dim) + self.offsetY,0))
    
    def position_cellule_x(self):
        return int(round((self.x * VAR.dim), 0))
    def position_cellule_y(self):
        return int(round((self.y * VAR.dim), 0))
    
    def rythme_animation(self):
        if time.time() - self.tempoTimer > 0.5: 
            self.tempo += 1
            self.tempoTimer = time.time()
    
    def afficher_zone_selection(self, x, y):
        i = 0
        for xo, yo in [(0, VAR.dim), (-VAR.dim, 0), (VAR.dim, 0), (0, -VAR.dim)]:
            pas_collision = (self.collision_avec_decors(x + xo , y + yo) == None)
            if pas_collision :                
                pygame.draw.rect(VAR.fenetre, (0, 255, 0), (x + xo, y + yo, VAR.dim, VAR.dim), 0)
                i += 1
                
        if i > 0:
            pygame.draw.rect(VAR.fenetre, (0, 255, 0), (x, y, VAR.dim, VAR.dim), 0)
            
            
    
    

    def collision_avec_decors(self): 
        x, y = self.position_pixel_x(), self.position_pixel_y() + self.image[0].get_height() - VAR.dim        
        VAR.cellule_rect.center = x+VAR.dimDiv2, y+VAR.dimDiv2        
            
        offset_x = 0 - VAR.cellule_rect.left 
        offset_y = 0 - VAR.cellule_rect.top 
         
        collision = VAR.cellule_mask.overlap(self.MOTEUR.TERRAIN.maskBlocage, (offset_x, offset_y ))        
        return collision
    
               
    def afficher(self):
        self.rythme_animation() 

        x, y = self.position_pixel_x(), self.position_pixel_y()
        index = ((self.tempo + self.tempoRnd) % len(self.image)) 
        
        
            
        VAR.fenetre.blit(self.image[index], (x, y))
            
        