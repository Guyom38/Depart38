# --- importation des librairies Pygame 
import pygame
from pygame.locals import *

import time



import variables as VAR

from fonctions import *
from terrain import *

from objets import *
from personnages import *


class CMoteur:
    def __init__(self):
        pygame.init()
        VAR.fenetre = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN, 32)
        pygame.display.set_caption("No Escape Departement")
        self.horloge = pygame.time.Clock()
        
        self.initialiser()
        

    def initialiser(self):          
        self.ELEMENTS_VISUELS = CObjets(self)
        self.PERSONNAGES = CPersonnages(self)
        
      
        self.PERSONNAGES.JOUEURS.append(CJoueur(self, 0, 1.0, 5.0, "Guyom", False))
                
        self.PERSONNAGES.PNJS.append(CJoueur(self, 0, 1.0, 5.0, "Vincent", True, 0))
        self.PERSONNAGES.PNJS.append(CJoueur(self, 0, 1.0, 5.0, "Basile", True,2))
        self.PERSONNAGES.PNJS.append(CJoueur(self, 0, 1.0, 5.0, "Luc", True, 2))
        self.PERSONNAGES.PNJS.append(CJoueur(self, 0, 1.0, 5.0, "Emmanuel", True, 2))
        self.PERSONNAGES.PNJS.append(CJoueur(self, 0, 1.0, 5.0, "Stevan", True, 2))
        
        self.TERRAIN = CTerrain(self) 
        self.TERRAIN.initialisation_joueurs()        
        
        self.PERSONNAGES.rays[0] = raytracing(self, 200, 10)
        self.PERSONNAGES.rays[1] = raytracing(self, 128, 5)
        self.PERSONNAGES.rays[2] = raytracing(self, 128, 5)
        
   
            
    def clavier(self):
        # --- récupére l'ensemble des évènements
        for event in pygame.event.get():        
            # --- si l'utilisateur clic sur la croix, ou appuie sur la touche ESCAPE
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                VAR.boucle = False

            # --- si l'utilisateur presse l'une des fleches de direction
            if event.type == KEYDOWN:  
                if event.key in [ENUM_DIR.GAUCHE, ENUM_DIR.DROITE, ENUM_DIR.HAUT, ENUM_DIR.BAS]:
                    self.PERSONNAGES.JOUEURS[0].directionPrecedente  = self.PERSONNAGES.JOUEURS[0].direction
                    self.PERSONNAGES.JOUEURS[0].seTourne = True
                        
                if event.key == K_LEFT:                         
                    self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.GAUCHE
                if event.key == K_RIGHT: 
                    self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.DROITE
                if event.key == K_UP: 
                    self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.HAUT
                if event.key == K_DOWN: 
                    self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.BAS
                if event.key == K_SPACE:
                    self.PERSONNAGES.JOUEURS[0].direction = ENUM_DIR.AUCUN 
                
    def demarrer(self):       
        cycle, som_t = 0,0
         
        VAR.boucle = True
        while VAR.boucle:
         
            self.clavier()                
            
            self.PERSONNAGES.se_deplacent()           
            self.TERRAIN.afficher()
            
            #if self.JOUEURS[0].direction == ENUM_DIR.AUCUN:
            #    VAR.fenetre.blit(self.TERRAIN.blocage, (0,0))
                 
            self.PERSONNAGES.afficher_visions()            
            self.ELEMENTS_VISUELS.afficher()
            
            ecriture = pygame.font.SysFont('arial', 20) 
            image_texte = ecriture.render( str(int(VAR.t_ray * 1000)) + "ms, elements dynamiques : " + str(len(self.ELEMENTS_VISUELS.liste)) , True, (255,0,0)) 
            VAR.fenetre.blit(image_texte, (50, 10))            
    
            image_texte = ecriture.render( str( (round(self.PERSONNAGES.PNJS[0].x, 2), round(self.PERSONNAGES.PNJS[0].y, 2)) ) , True, (255,0,0)) 
            VAR.fenetre.blit(image_texte, (50, 30))            
        
            image_texte = ecriture.render( str( (self.PERSONNAGES.PNJS[0].IA.objectifx, self.PERSONNAGES.PNJS[0].IA.objectify) ) , True, (255,0,0)) 
            VAR.fenetre.blit(image_texte, (50, 50))
            
            
            # --- afficher le résultat
            pygame.display.update()

            # --- limite la fréquence de raffraichissement a 25 images seconde
            self.horloge.tick(30)
            som_t += VAR.t_ray
            cycle += 1

        # --- en sortie de boucle, quitte le programme
        pygame.quit() 