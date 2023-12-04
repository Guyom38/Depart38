import time, random
import pygame

import variables as VAR
import fonctions as FCT


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
        if time.time() - self.tempoTimer > 0.05: 
            self.tempo += 1
            self.tempoTimer = time.time()
    
    def generer_ombre_selection(self, rayon):
        ombre = pygame.Surface((rayon,rayon), pygame.SRCALPHA).convert_alpha()        
        dim2 = rayon // 2
        pygame.draw.circle(ombre, (255,255,0, 100), (dim2, dim2), dim2)
        return ombre
    
    def afficher_zone_selection(self):
        objet_x = self.position_pixel_x()
        objet_y = self.position_pixel_y() + self.image[0].get_height()     
        
        joueurs_contact = self.ya_t_il_contact_avec_des_joueurs(objet_x, objet_y) 
        if  len(joueurs_contact) > 0:
            rayon = 1 + (self.tempo % (VAR.dimDiv2)) * 4
            image_ombre = self.generer_ombre_selection(rayon)
            centre = (VAR.dim - image_ombre.get_width()) // 2            
             
            VAR.fenetre.blit(image_ombre, (objet_x + centre, objet_y + centre - VAR.dim))
       

    def ya_t_il_contact_avec_des_joueurs(self, objet_x, objet_y): 
        contacts_joueurs = []
        for xo, yo in [(0, VAR.dim), (-VAR.dim, 0), (VAR.dim, 0), (0, -VAR.dim)]:
            for joueur in self.MOTEUR.PERSONNAGES.JOUEURS:                
             
                offset_x = objet_x + xo - joueur.mask_rect.left 
                offset_y = objet_y + yo - joueur.mask_rect.top 
                
                if not ( VAR.cellule_mask.overlap(joueur.mask, (offset_x, offset_y )) == None):      
                    contacts_joueurs.append(joueur)          
        return contacts_joueurs
    
               
    def afficher(self):
        self.rythme_animation() 

        x, y = self.position_pixel_x(), self.position_pixel_y()
        index = ((self.tempo + self.tempoRnd) % len(self.image)) 
        
        
            
        VAR.fenetre.blit(self.image[index], (x, y))
            
        