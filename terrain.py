from fonctions import *
import variables as VAR
import pygame

class CTerrain:
    def importe_calque(self, donnees):
        bob = ""
        x,y = 0, 0
        for d in donnees:            
            if d>0:
                self.MAP[x][y] = 1

            x += 1
            if x > 59: 
                y+=1
                x=0

                
        
                
    def __init__(self, fichier):
        self.MAP =  GenereMat2D(60,30, 0)

   
            
    def preparer_terrain(self):    
        self.planche = pygame.image.load(".ressources/maps.png")
        
        self.blocage = pygame.image.load(".ressources/mapb.png").convert_alpha()
        self.arrayBlocage = pygame.surfarray.array_blue(self.blocage)
        self.blocage = pygame.image.load(".ressources/mapc.png").convert_alpha()
