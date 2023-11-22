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
        self.blocage = self.MOTEUR_TILED.generer_blocage() 
        self.planche = self.MOTEUR_TILED.generer_map()         
        self.arrayBlocage = pygame.surfarray.array_blue(self.blocage)
    
    def initialisation_joueurs(self):
        self.parcours = self.MOTEUR_TILED.generer_parcours_PNJ()
        x, y = self.parcours['Chemin_Directeur']['DEPART']
        
        self.MOTEUR.PNJS[0].x, self.MOTEUR.PNJS[0].y = x , y 
        self.MOTEUR.PNJS[0].parcours = self.parcours['Chemin_Directeur']['GRILLE']
 

   
