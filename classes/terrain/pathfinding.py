import variables as VAR
import fonctions as FCT
import pygame
from pygame.locals import *
import random
import time
import classes.joueurs.algos.algo_dijkstra as AD
from constantes import *

import pickle
    
        
class CPathfinding:
    def __init__(self, moteur):
        self.MOTEUR = moteur
         
        self.grille_obstacles = [] 
        self.zones_libres = []      
        
        self.PARCOURS = {}       
        self.ZONES = []        
        
        self.image_mask = pygame.Surface((VAR.dim, VAR.dim)) # 32 pixel => 20
        self.mask = pygame.mask.from_surface(self.image_mask)
        self.mask_rect = self.image_mask.get_rect(center = (0,0))
        
    def charger_pathfinding(self):
        fichier = '.caches/' + VAR.fichier_map + '.pkl'
        
        if not FCT.existe_fichier(fichier):
            self.generer_tous_les_parcours()
            return
            
        with open(fichier, 'rb') as fichier:
            donnees = pickle.load(fichier)
            self.PARCOURS = donnees['PARCOURS']
            self.ZONES = donnees['ZONES']         
            
            
                        
    def generer_matrice_obstacles(self, arrayBlocage):      
        self.grille_obstacles = []
        self.zones_libres = []
        
        VAR.fenetre.fill( (255, 255, 255) )
        VAR.fenetre.blit(self.MOTEUR.TERRAIN.png_blocage, (0, 0))
              
        
        offset = VAR.dim // 2
        for x in range(0, VAR.dimension_x):        
            ligne_obstacles = []
            for y in range(0, VAR.dimension_y):       
                obstacle = self.obstacle_detecte((x * VAR.dim)+offset, (y * VAR.dim)+offset)
                ligne_obstacles.append(1 if obstacle else 0)    
                if not obstacle:
                    self.zones_libres.append((x, y))   
                
                pygame.draw.rect(VAR.fenetre, (255, 0, 0) if obstacle else (0,255,0), (x * VAR.dim, y * VAR.dim, VAR.dim, VAR.dim), 0 ) 
            pygame.display.update()
            time.sleep(0.0001)
             
                       
            self.grille_obstacles.append(ligne_obstacles)
        print("PATHFINDING, zones libres : " + str(len(self.zones_libres)) + " => " + str(len(self.zones_libres)**2))        
   
    def obstacle_detecte(self, x, y): 
        self.mask_rect.center = x, y 
       
        offset_x = 0 - self.mask_rect.left 
        offset_y = 0 - self.mask_rect.top 
     
        collision = self.mask.overlap(self.MOTEUR.TERRAIN.maskBlocage, (offset_x, offset_y))
        #print(str((x, y, collision)))
        if not collision == None:
            return True
        return False
    
    def preparation_AB(self, zoneA, zoneB):
        if not zoneA == zoneB: 
            # --- si la zone de depart et d'arrivee (x,y) n'ont jamais été initialisées    
            if not zoneA in self.ZONES: 
                self.ZONES[zoneA] = {}
                return True                            
            elif not zoneB in self.ZONES: 
                self.ZONES[zoneB] = {}
                return True
            
            if not zoneB in self.ZONES[zoneA] or not zoneA in self.ZONES[zoneB]: 
                return True
        return False
                
    def generer_tous_les_parcours(self):
        
        # --- Initialisation des differentes variables
        self.PARCOURS = {}
        self.ZONES = {}
                
        t = time.time() 
        duree=time.time()
      
        index = 1
        ignore_dij = 0
        ignore_deduction = 0  
        nb_deduction = 0 
        maximum = len(self.zones_libres)**2
    
        # --- Boucle principale qui compare le premier avec le dernier
        for indexA, zoneA in enumerate(self.zones_libres):
            
            VAR.fenetre.fill( (200,200,200) )
            VAR.fenetre.blit(self.MOTEUR.TERRAIN.png_blocage, (0, 0))
                
            for indexB, zoneB in enumerate(self.zones_libres[::-1]):                
                chemin = []
                 
                # --- affiche les zones bloquées                
                self.afficher_destinations_possibles(zoneA)
               
                # vérifie que B n'existe pas dans la dico

                if self.preparation_AB( zoneA, zoneB):
                    # genere le chemin entre zoneA et zoneB             
                    chemin, _, _ = AD.CDijkstra.algo_dijkstra(zoneA, zoneB, self.grille_obstacles)          
                    
                    # si un chemin a été trouvé
                    if len(chemin) > 0:
                            
                        # ajoute a la liste ce nouveau chemin
                        self.PARCOURS[index] = chemin  

         
                        for depart in range(0, len(chemin)): 
                            zoneC = chemin[depart]     
                            for arrive in range(len(chemin)-1, -1, -1):  
                                zoneD = chemin[arrive]
                                    
                                if self.preparation_AB( zoneC, zoneD):                    
                                    self.ZONES[zoneC][zoneD] = index, depart, arrive, 1
                                    self.ZONES[zoneD][zoneC] = index, depart, arrive, -1
                                    
                                    nb_deduction +=1
                                else:
                                    ignore_deduction +=1    

                        index +=1
                else:   
                    ignore_dij +=1
                
        
                self.afficher_chemins_trouves_sur_zone()
                if time.time() - t > 1:   
                    texte = self.afficher_statistiques(t, duree, index, ignore_dij, maximum, indexA, indexB, nb_deduction)
                    t = time.time()
                pygame.display.update()
                time.sleep(0.0001)

                
        time.sleep(10)       
        pygame.display.update()  
          
        with open('.caches/'+VAR.fichier_map+'.pkl', 'wb') as fichier:
            pickle.dump({'PARCOURS': self.PARCOURS, 'ZONES': self.ZONES}, fichier, protocol=pickle.HIGHEST_PROTOCOL)

        print(texte)
        print("Relancer le jeu, les chemins ont été calculés.")
        quit()
    
    def afficher_chemins_trouves_sur_zone(self):
        for zoneE in self.zones_libres:
            if zoneE in self.ZONES:
                x, y = zoneE
                x, y = (x * VAR.dim) , (y * VAR.dim)
                image_texte = VAR.ecriture10.render( str(len(self.ZONES[zoneE])) , True, (0,255,255) if len(self.ZONES[zoneE]) == len(self.zones_libres)-1 else (255,255,255)) 
                VAR.fenetre.blit(image_texte, (x + ((VAR.dim - image_texte.get_width()) // 2), y + ((VAR.dim - image_texte.get_height()) // 2)))   
        
    def afficher_statistiques(self, t, duree, index, ignore_dij, maximum, indexA, indexB, nb_deduction):
        
        total_secondes = ((time.time() - duree) / (index+ignore_dij)) * maximum # Exemple: 3665 secondes
        heures = int(total_secondes // 3600)  # Convertit les secondes en heures
        minutes = int((total_secondes % 3600) // 60)  # Convertit le reste en minutes
        secondes = int(total_secondes % 60)  # Le reste sont les secondes

        texte = []
        texte.append("IndexA : " + str(indexA) + " / " + "IndexB : " + str(indexB) + " / " + str(len(self.zones_libres)))
        texte.append("Nb Parcours : " + str(index) +"  // Chemins deduis : " + str(nb_deduction))
        texte.append("Ignore Pathfinding : " + str(ignore_dij))
        texte.append("Total : " + str(index+ignore_dij) + " / "+str(maximum))
        texte.append("Estimation : {:03d}h {:02d}m {:02d}s".format(heures,minutes,secondes))
                        
        pygame.draw.rect(VAR.fenetre, (0,0,0), (0,0,500,112))
        for y, txt in enumerate(texte):
            image_texte = VAR.ecriture10.render( txt, True, (255,255,255)) 
            VAR.fenetre.blit(image_texte, (10,y*20))   
                        
        return texte
                        
        
    def afficher_destinations_possibles(self, depart):
        if not depart in self.ZONES:
            print("Aucune destination")
            return
        
        x1, y1 = depart        
        pygame.draw.rect(VAR.fenetre, (255,0,0), (x1 * VAR.dim, y1 * VAR.dim, VAR.dim, VAR.dim), 0)
        for zone, _ in self.ZONES[depart].items():
            x2, y2 = zone
            pygame.draw.rect(VAR.fenetre, (0,128,128), (x2 * VAR.dim, y2 * VAR.dim, VAR.dim, VAR.dim), 0)

            
    
    
    
    
    
    
    
    
    
    
    
   
    
    
    
    
    