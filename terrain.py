from fonctions import *
import variables as VAR
import pygame
import tiled as T

class CTerrain:
    def __init__(self, moteur):         
        self.MOTEUR = moteur
        self.MOTEUR_TILED = T.map_tiled(moteur, ".ressources/map.tmx")
        self.preparer_terrain()     
            
    def preparer_terrain(self):    
        self.blocage = self.MOTEUR_TILED.generer_blocage() 
        self.planche = self.MOTEUR_TILED.generer_map()         
        
        self.arrayBlocage = pygame.surfarray.array_blue(self.blocage)
       
 

   
