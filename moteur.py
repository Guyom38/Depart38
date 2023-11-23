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
        VAR.fenetre = pygame.display.set_mode((VAR.resolution_x, VAR.resolution_y), pygame.FULLSCREEN, 32)
        pygame.display.set_caption("No Escape Departement")
        self.horloge = pygame.time.Clock()
        
        self.titre = pygame.image.load(".ressources/titre.jpg")
        self.titre = pygame.transform.scale(self.titre, (VAR.resolution_x, VAR.resolution_y))
        
       
        VAR.fenetre.blit(self.titre, (0, 0))
        pygame.display.flip()
        
        
        
        self.initialiser()
        
        
    def afficher_barre_progression(self, valeur, maximum, texte):
        dimx = 800
        dimy = 64
        
        x = (VAR.resolution_x - dimx) // 2
        y = VAR.resolution_y - dimy - 20
        
        dim_valeur = int((dimx / maximum) * valeur)
        pygame.draw.rect(VAR.fenetre, (0,0,0), (x, y, dimx, dimy), 0) 
        pygame.draw.rect(VAR.fenetre, (255,0,0), (x, y, dim_valeur, dimy), 0)   
        pygame.draw.rect(VAR.fenetre, (255,255,255), (x, y, dimx, dimy), 4)   
         
        ecriture = pygame.font.SysFont('arial', 30) 
        image_texte = ecriture.render(texte , True, (255,255,255)) 
        posx = (VAR.resolution_x - image_texte.get_width()) //2
        posy = y + int((dimy - image_texte.get_height()) // 2)
        VAR.fenetre.blit(image_texte, (posx, posy))            
    
        pygame.display.flip()
        #time.sleep(0.3)
        
        
        
        
    def initialiser(self):  
        
        
        self.afficher_barre_progression(30, 100, "Empilage des dossiers ...")        
        self.ELEMENTS_VISUELS = CObjets(self)
        
        self.afficher_barre_progression(40, 100, "Préparation des pauses café ...")  
        self.PERSONNAGES = CPersonnages(self)
        
        self.afficher_barre_progression(50, 100, "Configuration des tapis ...")  
        self.PERSONNAGES.JOUEURS.append(CJoueur(self, 0, 1.0, 5.0, "Guyom", False))
                
        self.PERSONNAGES.PNJS.append(CJoueur(self, 0, 1.0, 5.0, "Vincent", True, 0))
        self.PERSONNAGES.PNJS.append(CJoueur(self, 0, 1.0, 5.0, "Basile", True,2))
        self.PERSONNAGES.PNJS.append(CJoueur(self, 0, 1.0, 5.0, "Luc", True, 2))
        self.PERSONNAGES.PNJS.append(CJoueur(self, 0, 1.0, 5.0, "Emmanuel", True, 2))
        self.PERSONNAGES.PNJS.append(CJoueur(self, 0, 1.0, 5.0, "Stevan", True, 2))
        
        self.afficher_barre_progression(70, 100, "Synchronisation des écrans anti-reflets pour siestes discrètes ...")  
        self.TERRAIN = CTerrain(self) 
        self.TERRAIN.initialisation_joueurs()  
              
        self.afficher_barre_progression(90, 100, "Optimisation des réseaux Wi-Fi pour transmissions télépathiques ...")  
        self.PERSONNAGES.rays[0] = CRaytracing(self, 200, 20)
        self.PERSONNAGES.rays[1] = CRaytracing(self, 128, 20)
        self.PERSONNAGES.rays[2] = CRaytracing(self, 128, 20)
        
        self.afficher_barre_progression(100, 100, "Démarrage du jeu")  
                    
            
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
            image_texte = ecriture.render( str(int(VAR.timer_ray * 1000)) + "ms, elements dynamiques : " + str(len(self.ELEMENTS_VISUELS.liste)) , True, (255,0,0)) 
            VAR.fenetre.blit(image_texte, (50, 10))            
    
            image_texte = ecriture.render( str( (round(self.PERSONNAGES.PNJS[0].x, 2), round(self.PERSONNAGES.PNJS[0].y, 2)) ) , True, (255,0,0)) 
            VAR.fenetre.blit(image_texte, (50, 30))            
        
            image_texte = ecriture.render( str( (self.PERSONNAGES.PNJS[0].IA.objectifx, self.PERSONNAGES.PNJS[0].IA.objectify) ) , True, (255,0,0)) 
            VAR.fenetre.blit(image_texte, (50, 50))
            
            cercle = self.PERSONNAGES.rays[0].calculer_points_cercle(500,500,400)
            for index, xx, yy in cercle:
                ligne = bresenham((500, 500), (xx, yy), 10).path
                for xxx, yyy in ligne:
                    pygame.draw.circle(VAR.fenetre, (255,255,0), (xxx, yyy), 2)
                    
                pygame.draw.circle(VAR.fenetre, (255,0,0), (xx, yy), 2)
            # --- afficher le résultat
            pygame.display.update()

            # --- limite la fréquence de raffraichissement a 25 images seconde
            self.horloge.tick(30)
            som_t += VAR.timer_ray
            cycle += 1

        # --- en sortie de boucle, quitte le programme
        pygame.quit() 