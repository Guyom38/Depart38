import variables as VAR
import fonctions as FCT
import pygame
import random
import time
import classes.joueurs.algo_dijkstra as AD
from constantes import *

import pickle
    
        
class CPathfinding:
    def __init__(self, moteur):
        self.MOTEUR = moteur
         
        self.grille_obstacles = [] 
        self.zones_libres = []      
        
        self.PARCOURS = {}       
        self.ZONES = []        
        
        
    def charger_pathfinding(self):
        if VAR.phase_dans_le_jeu == ENUM_PHASE.SALLE_ATTENTE:
            return
        
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
              
        offset = VAR.dim // 2
        for x in range(0, VAR.dimension_x):        
            ligne_obstacles = []
            for y in range(0, VAR.dimension_y):       
                xx, yy = (x * VAR.dim) + offset, (y * VAR.dim) + offset                  
                 
                ligne_obstacles.append(1 if arrayBlocage[xx][yy] == 255 else 0)    
                if arrayBlocage[xx][yy] == 0:
                    self.zones_libres.append((x, y))        
                       
            self.grille_obstacles.append(ligne_obstacles)
        print("PATHFINDING, zones libres : " + str(len(self.zones_libres)) + " => " + str(len(self.zones_libres)**2))        
   
   
    
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
        aff = True  
        
        # --- Boucle principale qui compare le premier avec le dernier
        for indexA, zoneA in enumerate(self.zones_libres):
            if aff:
                VAR.fenetre.fill( (200,200,200) )
                VAR.fenetre.blit(self.MOTEUR.TERRAIN.png_blocage, (0, 0))
                
            for indexB, zoneB in enumerate(self.zones_libres[::-1]):
                chemin = []
                 
                # --- affiche les zones bloquées                
                if aff:
                    self.afficher_destinations_possibles(zoneA)
               
                # vérifie que B n'existe pas dans la dico
                if self.preparation_AB( zoneA, zoneB):
                 
                    # genere le chemin entre zoneA et zoneB
                    chemin, _, _ = AD.CDijkstra.algo_dijkstra(zoneA, zoneB, self.grille_obstacles)
                        
                    if aff:                    
                        for x, y in chemin:                                
                            pygame.draw.circle(VAR.fenetre, (0,255,0), ((x * VAR.dim) + 16, (y * VAR.dim)+16), 16, 0)
                                
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
                
                    if aff:           
                        for zoneE in self.zones_libres:
                            if zoneE in self.ZONES:
                                x, y = zoneE
                                x, y = (x * VAR.dim) , (y * VAR.dim)
                                image_texte = VAR.ecriture.render( str(len(self.ZONES[zoneE])) , True, (0,255,255) if len(self.ZONES[zoneE]) == len(self.zones_libres)-1 else (255,255,255)) 
                                VAR.fenetre.blit(image_texte, (x + ((VAR.dim - image_texte.get_width()) // 2), y + ((VAR.dim - image_texte.get_height()) // 2)))   
                    
                    if time.time() - t > 0.5:
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
                            image_texte = VAR.ecriture.render( txt, True, (255,255,255)) 
                            VAR.fenetre.blit(image_texte, (10,y*20))   
                        
                        pygame.display.update()
                        t = time.time()    
            
        time.sleep(10)       
        pygame.display.update()  
          
        with open('.caches/'+VAR.fichier_map+'.pkl', 'wb') as fichier:
            pickle.dump({'PARCOURS': self.PARCOURS, 'ZONES': self.ZONES}, fichier, protocol=pickle.HIGHEST_PROTOCOL)

        print(texte)
        print("Relancer le jeu, les chemins ont été calculés.")
        quit()
    
    def afficher_destinations_possibles(self, depart):
        if not depart in self.ZONES:
            print("Aucune destination")
            return
        
        x1, y1 = depart        
        pygame.draw.rect(VAR.fenetre, (255,0,0), (x1 * VAR.dim, y1 * VAR.dim, VAR.dim, VAR.dim), 0)
        for zone, _ in self.ZONES[depart].items():

            x2, y2 = zone
            pygame.draw.rect(VAR.fenetre, (0,128,128), (x2 * VAR.dim, y2 * VAR.dim, VAR.dim, VAR.dim), 0)

            
    
    
    
    
    
    
    
    
    
    
    
   
    
    
    
    
    