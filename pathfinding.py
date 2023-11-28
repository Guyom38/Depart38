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
    
    def afficher_destinations_possibles(self, depart):
        if not depart in self.ZONES:
            print("Aucune destination")
            return
        
        x1, y1 = depart        
        pygame.draw.rect(VAR.fenetre, (255,0,0), (x1 * VAR.dim, y1 * VAR.dim, VAR.dim, VAR.dim), 0)
        for zone, _ in self.ZONES[depart].items():

            x2, y2 = zone
            pygame.draw.rect(VAR.fenetre, (0,128,128), (x2 * VAR.dim, y2 * VAR.dim, VAR.dim, VAR.dim), 0)
            

                
    def generer_tous_les_parcours(self):
        
        # --- Initialisation des differentes variables
        self.PARCOURS = {}
        self.ZONES = {}
                
        delais, temps = 4, 5
        t = time.time() - delais
        duree=time.time()
      
        index = 1
        ignore_dij = 0
        ignore_deduction = 0  
        nb_deduction = 0 
        maximum = len(self.zones_libres)**2
        texte = ""
        aff, aff2 = True, False  
        
        # --- Boucle principale qui compare le premier avec le dernier
        for indexA, zoneA in enumerate(self.zones_libres):
            for indexB, zoneB in enumerate(self.zones_libres[::-1]):
                chemin = []
                 
                # --- affiche les zones bloquées                
                if aff:
                    VAR.fenetre.fill( (32,32,32) )
                    VAR.fenetre.blit(self.MOTEUR.TERRAIN.png_blocage, (0, 0))
                    self.afficher_destinations_possibles(zoneA)
               
                # vérifie que B n'existe pas dans la dico
                if self.preparation_AB( zoneA, zoneB):
                 
                    # genere le chemin entre zoneA et zoneB
                    chemin, _, _ = self.algo_dijkstra(zoneA, zoneB)
                        
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
                    if aff2:
                        if not zoneA == zoneB:  
                            if zoneA in self.ZONES and zoneB in self.ZONES[zoneA]:  
                                i, d, a, s = self.ZONES[zoneA][zoneB]
                                for x, y in self.PARCOURS[i][d:a:s]:                                
                                    pygame.draw.circle(VAR.fenetre, (255,0,0), ((x * VAR.dim) + 16, (y * VAR.dim)+16), 16, 0)
                            
                    ignore_dij +=1
                
                    if aff:           
                        for zoneE in self.zones_libres:
                            if zoneE in self.ZONES:
                                x, y = zoneE
                                x, y = (x * VAR.dim) , (y * VAR.dim)
                                image_texte = VAR.ecriture.render( str(len(self.ZONES[zoneE])) , True, (0,255,255) if len(self.ZONES[zoneE]) == len(self.zones_libres)-1 else (255,255,255)) 
                                VAR.fenetre.blit(image_texte, (x + ((VAR.dim - image_texte.get_width()) // 2), y + ((VAR.dim - image_texte.get_height()) // 2)))   
                        
                    
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
                    
                    
                    for y, txt in enumerate(texte):
                        image_texte = VAR.ecriture.render( txt, True, (255,255,255)) 
                        VAR.fenetre.blit(image_texte, (10,y*20))   
                    
                    
                    pygame.display.update()
                    time.sleep(0.0001)       
                    
                    
                    if time.time() - t > temps:
                        t = time.time()            

            
        time.sleep(10)       
        pygame.display.update()  
          
        with open('.caches/'+VAR.fichier_map+'.pkl', 'wb') as fichier:
            pickle.dump({'PARCOURS': self.PARCOURS, 'ZONES': self.ZONES}, fichier, protocol=pickle.HIGHEST_PROTOCOL)

        print(texte)
        print("Relancer le jeu, les chemins ont été calculés.")
        quit()
    
    def charger_pathfinding(self):
        fichier = '.caches/' + VAR.fichier_map + '.pkl'
        
        if not FCT.existe_fichier(fichier):
            self.generer_tous_les_parcours()
            return
            
        with open(fichier, 'rb') as fichier:
            donnees = pickle.load(fichier)
            self.PARCOURS = donnees['PARCOURS']
            self.ZONES = donnees['ZONES'] 

            
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
    
    
    
    
    
    
    
    
    
    def course_poursuite_contre_le_joueur(self, nb_joueurs):
        position_joueur = (int(self.MOTEUR.PERSONNAGES.JOUEURS[0].x), int(self.MOTEUR.PERSONNAGES.JOUEURS[0].y)) 
        

        for i, pnj in enumerate(self.MOTEUR.PERSONNAGES.PNJS):
            if i > nb_joueurs:
                return
            
            position_pnj = (int(pnj.x), int(pnj.y))
            
            #if not position_joueur == self.pos_joueur or not position_pnj == self.pos_pnj:
            #    self.pos_joueur, self.pos_pnj = position_joueur, position_pnj     
                
            if 1 == 1:  
                self.chemin, self.ouverte, self.ferme = self.algo_dijkstra( position_pnj, position_joueur)   
            else:
                self.ouverte = []
                self.ferme = []
                    
                if position_joueur in self.ZONES and position_pnj in self.ZONES[position_joueur]:
                    index_chemin, depart_chemin, arrivee_chemin, sens_lecture = self.ZONES[position_pnj][position_joueur]
                    if index_chemin > 0:
                        if sens_lecture == 1:
                            self.chemin = self.PARCOURS[index_chemin][depart_chemin:arrivee_chemin]
                        else:
                            self.chemin = self.PARCOURS[index_chemin][arrivee_chemin:depart_chemin:-1]   
                    else:
                        print("pas de chemin")
                else:
                    self.chemin = []
                    print("pas de chemin calcule")
                    
            if len(self.chemin) > 1:
                pnj.IA.chemin_pathfinding = self.chemin
                pnj.IA.index_chemin = 0
            self.afficher()
   
    
    def afficher(self):     
            
        if ENUM_DEMO.DIJISKRA in VAR.demo and not self.chemin == None:    
            for x, y in self.chemin:
                pygame.draw.circle(VAR.fenetre, (255,255,255), ((x*VAR.dim)+16, (y*VAR.dim)+16), 16, 0)

            if ENUM_DEMO.PATHFINDING_OUVERTFERME in VAR.demo:
                # Dessiner les nœuds
                for noeud in self.ouverte:
                    x, y = noeud.position
                    pygame.draw.circle(VAR.fenetre, (255, 0, 0), ((x * VAR.dim) + 16, (y * VAR.dim) + 16), 8, 0)

                for noeud in self.ferme:
                    x, y = noeud.position
                    pygame.draw.circle(VAR.fenetre, (0, 255, 0), ((x * VAR.dim) + 16, (y * VAR.dim) + 16), 4, 0)