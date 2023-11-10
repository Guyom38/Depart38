# --- importation des librairies Pygame 
import pygame
from pygame.locals import *

import time



import variables as VAR
from raytracing import *
from fonctions import *
from terrain import *
from joueur import *

class CMoteur:
    def __init__(self):
        pygame.init()
        VAR.fenetre = pygame.display.set_mode((1400, 768), pygame.DOUBLEBUF, 32)
        pygame.display.set_caption("Espion")
        self.horloge = pygame.time.Clock()
        
        self.initialiser()
        

    def initialiser(self):  
        self.JOUEURS = []
        self.JOUEURS.append(CJoueur(self, 4.0, 4.0, "joueur 1"))
        self.TERRAIN = CTerrain('carte.txt')
        self.MAP = self.TERRAIN.MAP
            
        self.rays = raytracing(self, 300, 1)
        
        
    def demarrer(self):       
        cycle, som_t = 0,0
        self.TERRAIN.preparer_terrain()
        
        boucle = True
        while boucle:
            # --- récupére l'ensemble des évènements
            for event in pygame.event.get():        
                # --- si l'utilisateur clic sur la croix, ou appuie sur la touche ESCAPE
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    boucle = False

                # --- si l'utilisateur presse l'une des fleches de direction
                if event.type == KEYDOWN:  
                    if event.key in [ENUM_DIR.GAUCHE, ENUM_DIR.DROITE, ENUM_DIR.HAUT, ENUM_DIR.BAS]:
                        self.JOUEURS[0].directionPrecedente  = self.JOUEURS[0].direction
                        self.JOUEURS[0].seTourne = True
                        
                    if event.key == K_LEFT:                         
                        self.JOUEURS[0].direction = ENUM_DIR.GAUCHE
                    if event.key == K_RIGHT: 
                        self.JOUEURS[0].direction = ENUM_DIR.DROITE
                    if event.key == K_UP: 
                        self.JOUEURS[0].direction = ENUM_DIR.HAUT
                    if event.key == K_DOWN: 
                        self.JOUEURS[0].direction = ENUM_DIR.BAS
                    if event.key == K_SPACE:
                        self.JOUEURS[0].direction = ENUM_DIR.AUCUN
            

                        
            self.JOUEURS[0].se_deplace()

       
        
            som_t += VAR.t_ray
            cycle += 1
            
            
            VAR.fenetre.fill((16,16,16))    
            VAR.fenetre.blit(self.TERRAIN.planche, (0,0))
            self.rays.afficher(self.JOUEURS[0].x, self.JOUEURS[0].y, 0) 
            VAR.fenetre.blit(self.TERRAIN.blocage, (0,0))
            
            
            
            
            
            self.JOUEURS[0].afficher()
            
            ecriture = pygame.font.SysFont('arial', 40) 
            image_texte = ecriture.render( str(int(VAR.t_ray * 1000)) + "ms" , True, (255,0,0)) 
            VAR.fenetre.blit(image_texte, (50, 550))
            
            
            
            # --- afficher le résultat
            pygame.display.update()

            # --- limite la fréquence de raffraichissement a 25 images seconde
            self.horloge.tick(50)

        # --- en sortie de boucle, quitte le programme
        pygame.quit() 