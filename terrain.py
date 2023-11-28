from fonctions import *
import variables as VAR
import pygame
import tiled as T

class CTerrain:
    def __init__(self, moteur):         
        self.MOTEUR = moteur
        self.MOTEUR_TILED = T.map_tiled(moteur, ".ressources/map.tmx")
        
        VAR.dimension_x = int(self.MOTEUR_TILED.root.attrib['width'].replace("'","")  )
        VAR.dimension_y = int(self.MOTEUR_TILED.root.attrib['height'].replace("'","")  )
        
        self.preparer_terrain()     
            
    def preparer_terrain(self):    
        self.png_blocage = self.MOTEUR_TILED.generer_png_blocage()               
        self.planche = self.MOTEUR_TILED.generer_map()   
        
        self.recolorier_map_bloquee()  
        self.arrayBlocage = pygame.surfarray.array_blue(self.png_blocage)
        self.maskBlocage = pygame.mask.from_surface(self.png_blocage)        
        
    def recolorier_map_bloquee(self):
        for y in range(0, self.png_blocage.get_height()):
            for x in range(0, self.png_blocage.get_width()):
                couleur = self.png_blocage.get_at((x, y))
                if not couleur == (0, 0, 0, 255):
                    self.png_blocage.set_at((x,y), (176, 84, 105, 255))
                    #self.png_blocage.set_at((x,y), (0, 0, 0, 255))
                #else:
                #    self.png_blocage.set_at((x,y), (0, 255, 255, 0)) 
    
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
 
    
        
    def afficher(self):
        VAR.fenetre.fill((16,16,16))    
        VAR.fenetre.blit(self.planche, (0,0))

   
