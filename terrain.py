import fonctions as FCT
import variables as VAR

from constantes import *

import pygame
import tiled as T
import time

class CTerrain:
    def __init__(self, moteur):         
        self.MOTEUR = moteur
        self.MOTEUR_TILED = T.map_tiled(moteur, ".ressources/" + VAR.fichier_map + ".tmx")
        
        VAR.dimension_x = int(self.MOTEUR_TILED.root.attrib['width'].replace("'","")  )
        VAR.dimension_y = int(self.MOTEUR_TILED.root.attrib['height'].replace("'","")  )
        
        self.preparer_terrain()     
            
    def preparer_terrain(self):    
        self.png_blocage = self.MOTEUR_TILED.generer_png_blocage()               
        self.planche = self.MOTEUR_TILED.generer_map()   
        
        self.charger_mask_blocage()  
        self.arrayBlocage = pygame.surfarray.array_alpha(self.png_blocage)
        self.maskBlocage = pygame.mask.from_surface(self.png_blocage)   
         
         
    def afficher(self):
        t = time.time()
        VAR.fenetre.fill((16,16,16))    
        VAR.fenetre.blit(self.planche, (0,0))
        
        if ENUM_DEMO.BLOCAGE in VAR.demo:
            VAR.fenetre.blit(self.png_blocage, (0,0))
        FCT.Performance('TERRAIN.afficher()', t)     
         
         
             
    # --- noir opaque (0,0,0,255) est un obstacle 
    # --- transparent (0,0,0,0) est libre   
    def charger_mask_blocage(self):
        fichier = '.caches/' + VAR.fichier_map + '_' + str(VAR.dim) + '.mask.png'
        if not FCT.existe_fichier(fichier):
            for y in range(0, self.png_blocage.get_height()):
                for x in range(0, self.png_blocage.get_width()):
                    couleur = self.png_blocage.get_at((x, y))
                    if not couleur == (0, 0, 0, 255):
                        self.png_blocage.set_at((x,y), (0,0,0,255)) #(176, 84, 105, 255))
                    else:
                        self.png_blocage.set_at((x,y), (0,0,0,0)) #(176, 84, 105, 255))

            pygame.image.save(self.png_blocage, fichier)
            return
        
        self.png_blocage = pygame.image.load(fichier).convert_alpha()
    
    def initialisation_joueurs(self):
        parcours = self.MOTEUR_TILED.generer_parcours_PNJ()
        
        compteurs_parcours = {}
        for pnj in self.MOTEUR.PERSONNAGES.PNJS:
            id_parcours = 'Chemin_' + str(pnj.fonction)
            if not id_parcours in compteurs_parcours: 
                compteurs_parcours[id_parcours] = 0
            
            x, y = parcours[id_parcours]['DEPART'][compteurs_parcours[id_parcours]]
            pnj.x, pnj.y = x ,y 
            pnj.IA.parcours = parcours[id_parcours]['GRILLE']
            compteurs_parcours[id_parcours] += 1
 
    
        
    

   
