from fonctions import *
import variables as VAR
import pygame
import tiled as T

class CTerrain:
    def __init__(self, moteur):         
        self.MOTEUR = moteur
        self.MOTEUR_TILED = T.map_tiled(moteur, ".ressources/map.tmx")
        
   
            
    def preparer_terrain(self):    
        self.planche = self.MOTEUR_TILED.generer_map() #pygame.image.load(".ressources/maps.png")
        self.blocage = self.MOTEUR_TILED.generer_blocage() #pygame.image.load(".ressources/maps.png")
        
        #self.blocage = pygame.image.load(".ressources/mapb.png").convert_alpha()
        self.arrayBlocage = pygame.surfarray.array_blue(self.blocage)
        #self.blocage = pygame.image.load(".ressources/mapc.png").convert_alpha()

   
