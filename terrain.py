from fonctions import *
import variables as VAR
import pygame
import tiled as T

class CTerrain:
    def __init__(self):
        self.MAP =  GenereMat2D(60,30, 0)
        
        self.m = T.map_tiled(".ressources/map.tmx")
        
    
   
            
    def preparer_terrain(self):    
        self.planche = self.m.generer_map() #pygame.image.load(".ressources/maps.png")
        self.blocage = self.m.generer_blocage() #pygame.image.load(".ressources/maps.png")
        
        #self.blocage = pygame.image.load(".ressources/mapb.png").convert_alpha()
        self.arrayBlocage = pygame.surfarray.array_blue(self.blocage)
        #self.blocage = pygame.image.load(".ressources/mapc.png").convert_alpha()
