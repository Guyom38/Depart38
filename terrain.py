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
        parcours = self.MOTEUR_TILED.generer_parcours_PNJ()
        
        compteurs_parcours = {}
        for pnj in self.MOTEUR.PNJS:
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

   
