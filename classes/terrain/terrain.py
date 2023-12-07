import fonctions as FCT
import variables as VAR

from constantes import *

import pygame
import classes.terrain.tiled as T
import time

from classes.terrain.tiled_pnj_parcours import *


class CTerrain:
    def __init__(self, moteur):         
        self.MOTEUR = moteur
        self.MOTEUR_TILED = T.map_tiled(moteur)
        
        self.planche = None
        self.png_blocage = None
        self.arrayBlocage = None
        self.maskBlocage = None
        
    def preparer_terrain(self):  
        self.planche, self.png_blocage = self.MOTEUR_TILED.lecture_du_fichier_Tiled(".ressources/" + VAR.fichier_map + ".tmx")  
        self.preparer_blocage()
        
        
    # --- noir opaque (0,0,0,255) est un obstacle 
    # --- transparent (0,0,0,0) est libre      
    def preparer_blocage(self):
        couleur_obstacle = (0, 0, 0, 255)
        couleur_libre = (0, 0, 0, 0)
        fichier = '.caches/' + VAR.fichier_map + '_' + str(VAR.dim) + '.mask.png'
        if not FCT.existe_fichier(fichier) or ENUM_DEMO.BLOCAGE in VAR.demo:
            for y in range(0, self.png_blocage.get_height()):
                for x in range(0, self.png_blocage.get_width()):
                    couleur = self.png_blocage.get_at((x, y))
                    couleur = couleur_obstacle if (not couleur == (0, 0, 0, 255)) else couleur_libre
                    self.png_blocage.set_at((x,y), couleur) #(176, 84, 105, 255))
                    
            pygame.image.save(self.png_blocage, fichier)
            
        
        self.png_blocage = pygame.image.load(fichier).convert_alpha()        
        self.arrayBlocage = pygame.surfarray.array_alpha(self.png_blocage)
        self.maskBlocage = pygame.mask.from_surface(self.png_blocage)   
    
    
    def preparer_parcours_joueurs(self):
        initialisation_joueurs(self.MOTEUR_TILED) 
         
    def pixel_est_sur_le_terrain(self, int_x, int_y):
        return (    -1 < int_x < self.arrayBlocage.shape[0] and \
                    -1 < int_y < self.arrayBlocage.shape[1]    )       
        
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------
    # Vérifie si une cellule est sur le terrain de jeu
    def cellule_est_sur_le_terrain(self, cellule_x, cellule_y):
        return (    0 <= cellule_x < VAR.dimension_x and \
                    0 <= cellule_y < VAR.dimension_y    )
           
    def afficher(self):
        t = time.time()
        VAR.fenetre.fill((16,16,16))    
        VAR.fenetre.blit(self.planche, (0,0))
        
        if ENUM_DEMO.BLOCAGE in VAR.demo:
            VAR.fenetre.blit(self.png_blocage, (0,0))
        FCT.Performance('TERRAIN.afficher()', t)     
         
         
             
 

    
    
   
 
    
        
    

   
