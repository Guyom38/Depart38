
import pygame
import variables as VAR
from fonctions import *
import time

from ia import *


    
class CJoueur:
    def __init__(self, moteur, index, x, y, nom, is_IA, fonction = -1):
        self.MOTEUR = moteur
                
        self.index = index
        self.nom = nom
        self.x, self.y = x, y
        self.direction = ENUM_DIR.AUCUN
        self.fonction = fonction
        
        self.offsetX, self.offsetY = -16, -56     
        
        if is_IA:
            
            self.IA = CIA(moteur, self)            

            if fonction == 0:
                self.vitesse = 10
                self.distance_vision = 200
                self.image = pygame.image.load(".ressources/agent.png").convert_alpha()
                self.couleur_vision = (193,249,153, VAR.ray_alpha)
            elif fonction == 2:
                self.vitesse = 5
                self.distance_vision = 120
                self.image = pygame.image.load(".ressources/basile.png").convert_alpha()
                self.couleur_vision = (255,255,255, VAR.ray_alpha)
            else:
                self.vitesse = 5
                self.distance_vision = 120
                self.image = pygame.image.load(".ressources/chef.png").convert_alpha()
                self.couleur_vision = (239,231,129, VAR.ray_alpha)
            
            
   
        else:
            self.image = pygame.image.load(".ressources/agent2.png").convert_alpha()
            self.IA = None
            self.vitesse = 20

        self.image_nom = self.generer_image_nom()    
        self.ombre_joueur = self.generer_ombre_joueur()
        
        self.directionPrecedente = ENUM_DIR.AUCUN
        self.seTourne = 0  
        
        self.tempo,self.tempoTimer = 0, time.time()        
        self.timer_particules = time.time()        
        
        # --- Gestion du mask pour les collisions
        image_mask = pygame.Surface((20, 4))
        self.mask = pygame.mask.from_surface(image_mask)
        self.mask_rect = image_mask.get_rect(center = (0,0))
    
    def generer_ombre_joueur(self):
        self.ombre = pygame.Surface((VAR.dim,VAR.dim), pygame.SRCALPHA).convert_alpha()
        
        dim2 = VAR.dim // 2
        pygame.draw.circle(self.ombre, (0,0,0, 60), (dim2, dim2), dim2)
        
    def generer_image_nom(self):
        ecriture = pygame.font.SysFont('arial', 24) 
        image_ombre = ecriture.render( self.nom , True, (0,0,0)) 
        image_texte = ecriture.render( self.nom , True, (255,255,255)) 
        
        image_nom = pygame.Surface( (image_ombre.get_width()+4, image_ombre.get_height()-4) ).convert_alpha()
        
        image_nom.fill( (0, 0, 0, 255) )
        #image_nom.blit(image_ombre, (0, -4))
        image_nom.blit(image_texte, (2, -2))
        
        return image_nom
          
    def get_position(self):
        return (int((self.x * VAR.dim) +16), int((self.y * VAR.dim)))    
               
    def position_int_x(self):
        return round((self.x * VAR.dim))
    def position_int_y(self):
        return round((self.y * VAR.dim))
        
    def toujours_sur_le_terrain(self):
        return (    self.position_int_x() > -1 and self.position_int_x() < self.MOTEUR.TERRAIN.arrayBlocage.shape[0] \
                    and self.position_int_y() > -1 and self.position_int_y() < self.MOTEUR.TERRAIN.arrayBlocage.shape[1]    )            
    
    def collision_avec_decors(self): 
        self.mask_rect.center = self.position_int_x()+16, self.position_int_y() 
       
        offset_x = 0 - self.mask_rect.left 
        offset_y = 0 - self.mask_rect.top 
     
        collision = self.mask.overlap(self.MOTEUR.TERRAIN.maskBlocage, (offset_x, offset_y))
        if collision:
            if ENUM_DEMO.BLOCAGE in VAR.demo :
                pygame.draw.rect(VAR.fenetre, (255,0,0), self.mask_rect, 0)  
                print(("collision", str(collision)))
            return True
        return False
        
     
    
    
                                         
    def afficher_fumee(self):
        # --- particules
        if time.time() - self.timer_particules > (1 / self.vitesse) and self.vitesse > 5:            
            self.MOTEUR.PARTICULES.Ajouter_Particule(self.position_int_x()+16, self.position_int_y(), (255,255,255))
            self.timer_particules = time.time()
    
    def reflechit(self):
        est_ordinateur = (not self.IA == None)        
        # --- Si ordinateur suivre le chemin
        
        if est_ordinateur:
            self.IA.calculer_le_chemin_jusqua((int(self.MOTEUR.PERSONNAGES.JOUEURS[0].x), int(self.MOTEUR.PERSONNAGES.JOUEURS[0].y)))    
            if self.direction == ENUM_DIR.AUCUN:
                self.IA.etablir_direction_initiale()                
            self.IA.je_reflechis()        
                     
                     
    def se_deplace(self):        
           
        xo, yo = self.x, self.y        
        for _ in range(0, self.vitesse):
            if self.direction == ENUM_DIR.GAUCHE:
                self.x -= VAR.pas
            elif self.direction == ENUM_DIR.DROITE:
                self.x += VAR.pas
            elif self.direction == ENUM_DIR.HAUT:
                self.y -= VAR.pas
            elif self.direction == ENUM_DIR.BAS:
                self.y += VAR.pas

            
            est_ordinateur = (not self.IA == None)    
            if not est_ordinateur:
                if self.toujours_sur_le_terrain():                
                    if self.collision_avec_decors():
                        self.x, self.y = xo, yo
                        return
                    
                    #self.direction = ENUM_DIR.AUCUN
    

    
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
    
    
    # --- affiche joueur
    def afficher(self):   
        est_ordinateur = (not self.IA == None)               
        
        # -- affiche ombre du joueur
        

        x, y = self.get_position()
        centre_ombrex, centre_ombrey = x - (self.ombre.get_width() // 2), y - (self.ombre.get_height() // 2)
        VAR.fenetre.blit(self.ombre, (centre_ombrex, centre_ombrey))
        
        if est_ordinateur:
            self.MOTEUR.PERSONNAGES.RAYS.afficher(self)
            
        # --- affiche sprite joueur
        xImg, yImg = x+self.offsetX, y+self.offsetY
        VAR.fenetre.blit(self.image, (xImg, yImg), self.coordonnees_image_animee())
       
            
        # --- affiche nom
        VAR.fenetre.blit(self.image_nom, (xImg, yImg))

        
        
    