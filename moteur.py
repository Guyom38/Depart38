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
        VAR.ecriture10 = pygame.font.SysFont('arial', 10)    
            
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
        self.PERSONNAGES.JOUEURS.append(CJoueur(self, 0, 2.0, 6.0, "Guyom", False))
                
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
                        pygame.draw.rect(VAR.fenetre, (32,32,32), (x * VAR.dim, y* VAR.dim, VAR.dim, VAR.dim), 0)      
                           
    
    def afficher_performances(self):
        for index, valeurs in enumerate(FCT.perfs.items()):
            x = index // 4
            y = index % 4
                
            key, valeur = valeurs
            resultat = ""
            if ( int(1.0 / valeur[0]) < VAR.fps_max  ):
                resultat = " /!\\"
            vv = "{:.04f}ms, {:.04f}ms, {:.04f}ms".format(round(valeur[0],4), round(valeur[1],4), round(valeur[2] / valeur[3],4)) + resultat
                                
            image_texte = VAR.ecriture.render( key , True, valeur[4])
            VAR.fenetre.blit(image_texte, ((600 * x), (y * 18)-2))     
            image_texte = VAR.ecriture.render( vv , True, valeur[4])
            VAR.fenetre.blit(image_texte, ((600 * x)+300, (y * 18)-2))   
            
                            
    def demarrer(self):       
        VAR.boucle = True
        while VAR.boucle:
            t = time.time()
            self.CONTROLLEURS.clavier()   
                
            self.TERRAIN.afficher()            
            self.PERSONNAGES.se_deplacent()       
            
            if ENUM_DEMO.CHEMIN_VINCENT in VAR.demo:
                self.afficher_parcours_vincent()  
        
            self.PARTICULES.Afficher_Les_Particules()    
            self.ELEMENTS_VISUELS.afficher()   

            #self.afficher_performances()
                
            # --- afficher le résultat
            pygame.display.update()
            FCT.Performance('MOTEUR.boucle()', t, (255,255,255))
            
            self.horloge.tick( VAR.fps_max )

        # --- en sortie de boucle, quitte le programme
        pygame.quit() 