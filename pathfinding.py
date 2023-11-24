import variables as VAR
import fonctions as FCT
import pygame
import random
import time
from queue import PriorityQueue
from constantes import *

matrices = []    
matrices.append( ([ [0,0,0,0],
                                 [1,0,0,1],
                                 [1,0,0,1],
                                 [0,0,0,0] ], (2, 1)) )    
            
matrices.append( ([ [1,0,0,1],
                                 [0,0,0,0],
                                 [0,0,0,0],
                                 [1,1,1,1] ], (2, 1)) )    
            
matrices.append( ([ [0,1,2],
                                 [0,0,0],
                                 [0,0,0],
                                 [0,1,0] ], (1, 1)) )   
            
matrices.append( ([ [2,0,0,1],
                                 [1,0,0,0],
                                 [1,0,0,0],
                                 [2,0,0,1] ], (2, 1)) )



class CRepere:
    def __init__(self, moteur, index, position):
        self.moteur = moteur
        self.index = index
        self.x, self.y = position

        self.LISTE_REPERES_VOISINS = {} 


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
        self.REPERES = []        
        self.grille_obstacles = []
        
        self.pos_joueur, self.pos_pnj, self.chemin, self.ouverte, self.ferme = None, None, None, None, None
        
    def generer_matrice_obstacle(self, arrayBlocage):      
        self.grille_obstacles = []

        # Parcourir le bitmap avec un décalage de 16 et un pas de 32
        offset = VAR.dim // 2
        for y in range(offset, len(arrayBlocage), VAR.dim):
            ligne_obstacles = []
            for x in range(offset, len(arrayBlocage[y]), VAR.dim):
                # Vérifier si la valeur du pixel est supérieure à 0            
                ligne_obstacles.append(1 if arrayBlocage[y][x] > 0 else 0)                
            self.grille_obstacles.append(ligne_obstacles)

    
    def chercher_l_intersection(self, matrice, offset, x, y):
        dimx = len(matrice[0])
        dimy = len(matrice)
            
        ox, oy = offset
        if x + dimx >= VAR.dimension_x or y + dimy >= VAR.dimension_y:
            return None
            
        for yy in range(0, dimy):
            for xx in range(0, dimx):
                xxx = x + xx
                yyy = y + yy
                    
                if matrice[yy][xx] != self.grille_obstacles[xxx][yyy] and matrice[yy][xx] != 2:
                    return None
                
        return (x + ox, y + oy)   
        
    def generer_reperes_sur_le_terrain(self):
        self.REPERES = []

        for y in range(3, VAR.dimension_y -1):
            for x in range(0, VAR.dimension_x):

                    for matrice, offset in matrices:
                        intersection = self.chercher_l_intersection(matrice, offset, x, y)
                        
                        if not intersection == None:
                            compteur_reperes = len(self.REPERES)
                            self.REPERES.append( CRepere(self.MOTEUR, compteur_reperes, intersection) )
        
        print("Pathfinding, " + str(len(self.REPERES)) + " trouves.")

    
    def generer_chemin_entre_reperes(self):
        valeur = 70
        pas = (30 / len(self.REPERES)+1)
        i = 0
        for repere1 in self.REPERES:
            i+=1
            pas += 1
            self.MOTEUR.afficher_barre_progression(valeur + pas, 100, "Préparation de la carte routière :" + str(i) +" / "+str(len(self.REPERES)))  
            position1 = (repere1.x, repere1.y)
            
            for repere2 in self.REPERES:
                if not repere1 == repere2:
                    ok1 = not (repere2.index in repere1.LISTE_REPERES_VOISINS)
                    ok2 = not (repere1.index in repere2.LISTE_REPERES_VOISINS)
                    
                    if ok1 or ok2:       
                        position2 = (repere2.x, repere2.y)
                        chemin, _, _ = self.algo_dijkstra(position1, position2)
                    if ok1:
                        repere1.LISTE_REPERES_VOISINS[repere2.index] = chemin
                    if ok2:
                        repere2.LISTE_REPERES_VOISINS[repere1.index] = chemin[::-1]


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

        return None, liste_ouverte_set, liste_fermee_set
    
    
    
    
    
    
    
    
    
    def calculer_pathfinding(self):
        pos_joueur = (int(self.MOTEUR.PERSONNAGES.JOUEURS[0].x), int(self.MOTEUR.PERSONNAGES.JOUEURS[0].y)) 
        pos_pnj = (int(self.MOTEUR.PERSONNAGES.PNJS[0].x), int(self.MOTEUR.PERSONNAGES.PNJS[0].y))
        
        if not pos_joueur == self.pos_joueur or not pos_pnj == self.pos_pnj:
            self.pos_joueur, self.pos_pnj = pos_joueur, pos_pnj     
              
            #self.chemin, self.ouverte, self.ferme = astar( pos_joueur, pos_pnj, self.grille)   
            self.chemin, self.ouverte, self.ferme = self.algo_dijkstra( pos_joueur, pos_pnj)   

    
    def afficher(self):
        c = 4
        for index, repere in self.REPERES[0].LISTE_REPERES_VOISINS.items():
            for points in repere:
                x, y = points            
                pygame.draw.circle(VAR.fenetre, (255, 0, 0), ((x * VAR.dim) + 16, (y * VAR.dim) + 16), 8, c)
            c += 2
            
        if VAR.demo == ENUM_DEMO.DIJISKRA:    
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