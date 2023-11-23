# --- importation des librairies Pygame 
import pygame
from pygame.locals import *

import time



import variables as VAR
from raytracing import *
from fonctions import *
from terrain import *
from joueur import *
from objets import *


class CMoteur:
    def __init__(self):
        pygame.init()
        VAR.fenetre = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN, 32)
        pygame.display.set_caption("Espion")
        self.horloge = pygame.time.Clock()
        
        self.initialiser()
        

    def initialiser(self):          
        self.OBJETS = CObjets(self)
        
        self.JOUEURS = []
        self.JOUEURS.append(CJoueur(self, 0, 1.0, 5.0, "Guyom", False))
        
        self.PNJS = []
        self.PNJS.append(CJoueur(self, 0, 1.0, 5.0, "Directeur1", True))
        self.PNJS.append(CJoueur(self, 0, 1.0, 5.0, "Directeur2", True))
        
        self.TERRAIN = CTerrain(self) 
        self.TERRAIN.initialisation_joueurs()
             
        self.rays = raytracing(self, 200, 1)
        
    def afficher_elements(self):
        
        liste_personnages = {}
        for personnage in self.JOUEURS + self.PNJS:
            x = personnage.position_int_x() 
            y = personnage.position_int_y() - 1
            key = "{:04d}{:04d}{:01d}".format(y, x, 9)
            liste_personnages[key] = personnage
            
        listes_fusionnees = {**self.OBJETS.liste, **liste_personnages}
        
        liste_objets_tries = sorted( listes_fusionnees.items(), key=lambda x: x[0])
        for cle_coordonnees, objet in liste_objets_tries:   
            objet.afficher()
            
          
                
    def demarrer(self):       
        cycle, som_t = 0,0
         
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
                        
            
            som_t += VAR.t_ray
            cycle += 1
            
            
            for personnage in self.JOUEURS + self.PNJS:
                personnage.se_deplace()
          
            
            VAR.fenetre.fill((16,16,16))    
            VAR.fenetre.blit(self.TERRAIN.planche, (0,0))
           
            
            
            #if self.JOUEURS[0].direction == ENUM_DIR.AUCUN:
            #    VAR.fenetre.blit(self.TERRAIN.blocage, (0,0))
            
            for pnj in self.PNJS:
                self.rays.afficher(pnj) 
                
            self.afficher_elements()
                        
            ecriture = pygame.font.SysFont('arial', 20) 
            image_texte = ecriture.render( str(int(VAR.t_ray * 1000)) + "ms, " + str(len(self.OBJETS.liste)) , True, (255,0,0)) 
            VAR.fenetre.blit(image_texte, (50, 10))
            
            ecriture = pygame.font.SysFont('arial', 20) 
            image_texte = ecriture.render( str( (round(self.PNJS[0].x, 2), round(self.PNJS[0].y, 2)) ) , True, (255,0,0)) 
            VAR.fenetre.blit(image_texte, (50, 30))
            
            ecriture = pygame.font.SysFont('arial', 20) 
            image_texte = ecriture.render( str( (self.PNJS[0].IA.objectifx, self.PNJS[0].IA.objectify) ) , True, (255,0,0)) 
            VAR.fenetre.blit(image_texte, (50, 50))
            
            
            # --- afficher le résultat
            pygame.display.update()

            # --- limite la fréquence de raffraichissement a 25 images seconde
            self.horloge.tick(25)

        # --- en sortie de boucle, quitte le programme
        pygame.quit() 