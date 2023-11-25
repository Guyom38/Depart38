import variables as VAR
import fonctions as FCT
import pygame
import random
import time
from queue import PriorityQueue
from constantes import *

import pickle




class CNoeud:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = float("inf")

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def __lt__(self, other):
        return self.g < other.g
        
        
class CPathfinding:
    def __init__(self, moteur):
        self.MOTEUR = moteur
         
        self.grille_obstacles = []
        
        self.ZONES = []
        self.zones_libres = []      
        self.pos_joueur, self.pos_pnj, self.chemin, self.ouverte, self.ferme = None, None, None, None, None
        
        
    def generer_matrice_obstacle2(self, arrayBlocage):      
        self.grille_obstacles = []

        # Parcourir le bitmap avec un décalage de 16 et un pas de 32
        offset = VAR.dim // 2
        for y in range(offset, len(arrayBlocage), VAR.dim):
            ligne_obstacles = []
            for x in range(offset, len(arrayBlocage[y]), VAR.dim):
                # Vérifier si la valeur du pixel est supérieure à 0            
                ligne_obstacles.append(1 if arrayBlocage[y][x] > 0 else 0)                
            self.grille_obstacles.append(ligne_obstacles)
    
   
                        
    def generer_matrice_obstacle(self, arrayBlocage):      
        self.grille_obstacles = []
        self.zones_libres = []
              
        offset = VAR.dim // 2
        for x in range(0, VAR.dimension_x):        
            ligne_obstacles = []
            for y in range(0, VAR.dimension_y):       
                xx, yy = (x * VAR.dim) + offset, (y * VAR.dim) + offset                  
                 
                ligne_obstacles.append(1 if arrayBlocage[xx][yy] > 0 else 0)    
                
                if arrayBlocage[xx][yy] == 0:
                    self.zones_libres.append((x, y))        
                       
            self.grille_obstacles.append(ligne_obstacles)

        print("PATHFINDING, zones libres : " + str(len(self.zones_libres)) + " => " + str(len(self.zones_libres)**2))
        

    def generer_tous_les_parcours(self):
        self.PARCOURS = {}
        self.ZONES = {}
        
        index = 1
        nb_ignores = 0
        
        delais, temps = 4, 5
        t = time.time() - delais
  
        j = 0
        for zoneA in self.zones_libres:
            i = 0
            for zoneB in self.zones_libres[::-1]:
                aff = (time.time() - t > delais)
                
                if aff:
                    VAR.fenetre.fill( (32,32,32) )
                    VAR.fenetre.blit(self.MOTEUR.TERRAIN.png_blocage, (0, 0))
                
                chemin = []
                if not zoneA == zoneB: 
                    if not zoneA in self.ZONES: self.ZONES[zoneA] = {}
                    if not zoneB in self.ZONES: self.ZONES[zoneB] = {}

                    chemin, _, _ = self.algo_dijkstra(zoneA, zoneB)
                    
                    if aff:                    
                        for z in chemin:
                            x, y = z
                            pygame.draw.circle(VAR.fenetre, (255,255,0), ((x * VAR.dim) + 16, (y * VAR.dim)+16), 16, 0)
                    
                    if len(chemin) > 0:
                        self.PARCOURS[index] = chemin     
                        self.ZONES[zoneA][zoneB] = index
                        self.ZONES[zoneB][zoneA] = -index
                        index += 1      
                    else:
                        nb_ignores +=1                   
                  
                else :
                    nb_ignores +=1
                
                i+= 1
                
                if aff:           
                    for zoneC in self.zones_libres:
                        if zoneC in self.ZONES:
                            x, y = zoneC
                            x, y = (x * VAR.dim) , (y * VAR.dim)
                            image_texte = VAR.ecriture.render( str(len(self.ZONES[zoneC])) , True, (255,255,255)) 
                            VAR.fenetre.blit(image_texte, (x + ((VAR.dim - image_texte.get_width()) // 2), y + ((VAR.dim - image_texte.get_height()) // 2)))   
                    
                    time.sleep(0.0001)       
                    pygame.display.update()
                    
                    if time.time() - t > temps:
                        t = time.time()
            
            j += 1
            if j > 10:
                break
            
            
        with open('parcours_zones_data.pkl', 'wb') as fichier:
            pickle.dump({'PARCOURS': self.PARCOURS, 'ZONES': self.ZONES}, fichier, protocol=pickle.HIGHEST_PROTOCOL)

            
        print("parfait")
        quit()
                
    def afficher_zones(self, zone):
        matrice = self.ZONES[zone]
        
        for yy in range (0, VAR.dimension_y):
            txt = ""
            for xx in range (0, VAR.dimension_x):
                if (xx, yy) in matrice:
                    txt += "{:02d}".format(matrice[(xx,yy)])
                else:
                    txt += "--"
            print(txt)
            
    def algo_dijkstra(self, depart, arrivee):
        noeud_depart = CNoeud(None, depart)
        noeud_depart.g = 0
        noeud_arrivee = CNoeud(None, arrivee)

        liste_ouverte = PriorityQueue()
        liste_ouverte.put((noeud_depart.g, noeud_depart))
        liste_ouverte_set = {noeud_depart}  # Pour visualisation

        liste_fermee_set = set()  # Pour visualisation

        while not liste_ouverte.empty():
            _, noeud_actuel = liste_ouverte.get()
            liste_ouverte_set.remove(noeud_actuel)
            liste_fermee_set.add(noeud_actuel)

            if noeud_actuel == noeud_arrivee:
                chemin = []
                courant = noeud_actuel
                while courant is not None:
                    chemin.append(courant.position)
                    courant = courant.parent
                return chemin[::-1], liste_ouverte_set, liste_fermee_set

            for nouvelle_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                position_noeud = (noeud_actuel.position[0] + nouvelle_position[0], noeud_actuel.position[1] + nouvelle_position[1])

                if position_noeud[0] > (len(self.grille_obstacles) - 1) or position_noeud[0] < 0 or position_noeud[1] > (len(self.grille_obstacles[len(self.grille_obstacles)-1]) -1) or position_noeud[1] < 0:
                    continue
                if self.grille_obstacles[position_noeud[0]][position_noeud[1]] != 0:
                    continue

                nouveau_noeud = CNoeud(noeud_actuel, position_noeud)

                if nouveau_noeud in liste_fermee_set:
                    continue

                cout_potentiel = noeud_actuel.g + 1
                if cout_potentiel < nouveau_noeud.g:
                    nouveau_noeud.g = cout_potentiel
                    nouveau_noeud.parent = noeud_actuel
                    if nouveau_noeud not in liste_ouverte_set:
                        liste_ouverte.put((nouveau_noeud.g, nouveau_noeud))
                        liste_ouverte_set.add(nouveau_noeud)

        return [], liste_ouverte_set, liste_fermee_set
    
    
    
    
    
    
    
    
    
    def calculer_pathfinding(self):
        pos_joueur = (int(self.MOTEUR.PERSONNAGES.JOUEURS[0].x), int(self.MOTEUR.PERSONNAGES.JOUEURS[0].y)) 
        pos_pnj = (int(self.MOTEUR.PERSONNAGES.PNJS[0].x), int(self.MOTEUR.PERSONNAGES.PNJS[0].y))
        
        if not pos_joueur == self.pos_joueur or not pos_pnj == self.pos_pnj:
            self.pos_joueur, self.pos_pnj = pos_joueur, pos_pnj     
              
            #self.chemin, self.ouverte, self.ferme = astar( pos_joueur, pos_pnj, self.grille)   
            self.chemin, self.ouverte, self.ferme = self.algo_dijkstra( pos_joueur, pos_pnj)   

    
    def afficher(self):     
            
        if VAR.demo == ENUM_DEMO.DIJISKRA and not self.chemin == None:    
            VAR.ecriture = pygame.font.SysFont('arial', 20) 
            for x, y in self.chemin:
                pygame.draw.circle(VAR.fenetre, (255,255,255), ((x*VAR.dim)+16, (y*VAR.dim)+16), 16, 0)
                    #image_texte = ecriture.render( ""  , True, (255,0,0)) 
                    #VAR.fenetre.blit(image_texte, ((x*VAR.dim)+16, (y*VAR.dim)+16))           
                
                # Dessiner les nœuds
            for noeud in self.ouverte:
                x, y = noeud.position
                pygame.draw.circle(VAR.fenetre, (255, 0, 0), ((x * VAR.dim) + 16, (y * VAR.dim) + 16), 8, 0)

            for noeud in self.ferme:
                x, y = noeud.position
                pygame.draw.circle(VAR.fenetre, (0, 255, 0), ((x * VAR.dim) + 16, (y * VAR.dim) + 16), 4, 0)