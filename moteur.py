# --- importation des librairies Pygame 
import pygame
from pygame.locals import *

import time

from particules import *

import variables as VAR

from fonctions import *
from terrain import *

from objets import *
from personnages import *
from pathfinding import *
from controlleurs import *


class CMoteur:
    def __init__(self):
        pygame.init()
        VAR.fenetre = pygame.display.set_mode((VAR.resolution_x, VAR.resolution_y), pygame.FULLSCREEN, 32)
        pygame.display.set_caption("No Escape Departement")
        self.horloge = pygame.time.Clock()
        
        self.titre = pygame.image.load(".ressources/titre.jpg")
        self.titre = pygame.transform.scale(self.titre, (VAR.resolution_x, VAR.resolution_y))
        
        VAR.ecriture = pygame.font.SysFont('arial', 20) 
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
        time.sleep(0.01)
        
        
        
        
    def initialiser(self):  
        self.PARTICULES = CParticules(self)
        
        
        self.afficher_barre_progression(30, 100, "Empilage des dossiers ...")        
        self.ELEMENTS_VISUELS = CObjets(self)
        
        self.afficher_barre_progression(40, 100, "Préparation des pauses café ...")  
        self.PERSONNAGES = CPersonnages(self)
        
        self.afficher_barre_progression(50, 100, "Configuration des tapis ...")  
        self.PERSONNAGES.JOUEURS.append(CJoueur(self, 0, 1.0, 5.0, "Guyom", False))
                
        self.PERSONNAGES.PNJS.append(CJoueur(self, 1, 1.0, 5.0, "Vincent", True, 0))
        self.PERSONNAGES.PNJS.append(CJoueur(self, 2, 1.0, 5.0, "Basile", True,2))
        self.PERSONNAGES.PNJS.append(CJoueur(self, 3, 1.0, 5.0, "Luc", True, 2))
        self.PERSONNAGES.PNJS.append(CJoueur(self, 4, 1.0, 5.0, "Emmanuel", True, 2))
        self.PERSONNAGES.PNJS.append(CJoueur(self, 5, 1.0, 5.0, "Stevan", True, 2))
        
        self.afficher_barre_progression(70, 100, "Synchronisation des écrans anti-reflets pour siestes discrètes ...")  
        self.TERRAIN = CTerrain(self) 
        self.TERRAIN.initialisation_joueurs()                
        
        self.PERSONNAGES.PATHFINDING.generer_matrice_obstacles(self.TERRAIN.arrayBlocage)        
        self.PERSONNAGES.PATHFINDING.charger_pathfinding()
        
        self.afficher_barre_progression(100, 100, "Démarrage du jeu")  
        self.grille_traitee = FCT.GenereMat2D(VAR.dimension_x, VAR.dimension_y, 0)            
    
            
        self.CONTROLLEURS = CControlleurs(self)
    


    def afficher_parcours_vincent(self):
        for y in range(0, VAR.dimension_y):
                for x in range(0, VAR.dimension_x):
                    if self.PERSONNAGES.PNJS[0].IA.parcours[x][y]['CHEMIN']:
                        pygame.draw.rect(VAR.fenetre, (32,32,32), (x * 32, y* 32, 32, 32), 0)      
                           
                
    def demarrer(self):       
        ecriture = pygame.font.SysFont('arial', 20)         
        
        VAR.boucle = True
        while VAR.boucle:
         
            self.CONTROLLEURS.clavier()                
            
                
            self.TERRAIN.afficher()            
            self.PERSONNAGES.se_deplacent()       
            
            if ENUM_DEMO.CHEMIN_VINCENT in VAR.demo:
                self.afficher_parcours_vincent()            
            #self.PERSONNAGES.PATHFINDING.afficher_destinations_possibles( ( int(round(self.PERSONNAGES.JOUEURS[0].x)), int(round(self.PERSONNAGES.JOUEURS[0].y))) )
            
        
            self.PARTICULES.Afficher_Les_Particules()           
            
                
            self.ELEMENTS_VISUELS.afficher()           
            

    
            image_texte = ecriture.render( str( (round(self.PERSONNAGES.PNJS[0].x, 2), round(self.PERSONNAGES.PNJS[0].y, 2)) ) , True, (255,0,0)) 
            VAR.fenetre.blit(image_texte, (800, 0))            
            image_texte = ecriture.render( "JOUEUR => ROUND : "+str( (round(self.PERSONNAGES.JOUEURS[0].x, 0), round(self.PERSONNAGES.JOUEURS[0].y, 0))) + " --- INT : "+ str((int(self.PERSONNAGES.JOUEURS[0].x), int(self.PERSONNAGES.JOUEURS[0].y))) , True, (255,0,0))
            VAR.fenetre.blit(image_texte, (800, 20))            
            
            image_texte = ecriture.render( "MECHANT => ROUND : "+str( (round(self.PERSONNAGES.PNJS[0].x, 0), round(self.PERSONNAGES.PNJS[0].y, 0))) + " --- INT : "+ str((int(self.PERSONNAGES.PNJS[0].x), int(self.PERSONNAGES.PNJS[0].y))) , True, (255,0,0))
            VAR.fenetre.blit(image_texte, (800, 40))            
            
            image_texte = ecriture.render( self.PERSONNAGES.PNJS[0].IA.txt , True, (255,0,0))
            VAR.fenetre.blit(image_texte, (0, 0))            
           
            image_texte = ecriture.render( str(self.PERSONNAGES.PNJS[0].IA.chemin_pathfinding) , True, (255,0,0))
            VAR.fenetre.blit(image_texte, (0, 20))            
           
            
                
            # --- afficher le résultat
            pygame.display.update()

            # --- limite la fréquence de raffraichissement a 25 images seconde
            self.horloge.tick(30)

        # --- en sortie de boucle, quitte le programme
        pygame.quit() 