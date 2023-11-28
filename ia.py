import pygame
import fonctions as FCT
import variables as VAR
from constantes import *
import random
import pathfinding as PF
import algo_dijkstra as AD


class CIA:
    def __init__(self, moteur, personnage):
        # Initialisation du PNJ avec le moteur de jeu et le personnage
        self.MOTEUR = moteur
        self.PNJ = personnage
        self.PATHFINDING = self.MOTEUR.PERSONNAGES.PATHFINDING
        
        self.parcours = []
        self.chemin_pathfinding = []
        self.index_chemin = 0
        self.coordonnees_cible_a_traquer = None
        self.pos_cible, self.pos_pnj, self.chemin, self.ouverte, self.ferme = None, None, None, None, None
        
        # Objectifs initiaux pour la position du PNJ
        self.objectifx = -1
        self.objectify = -1
        
        # Mémorisation de la dernière position du PNJ
        self.position_precedente = (-1, -1)
        self.champ_vision = 60
       
        self.x, self.y, self.xInt, self.yInt = 0, 0, 0, 0
        self.txt = ""
        
    
    def calculer_le_chemin_jusqua(self, position_cible):
            
            position_pnj = (int(self.PNJ.x), int(self.PNJ.y))
            #position_cible = self.coordonnees_cible_a_traquer
            
            if not position_cible == self.pos_cible or not position_pnj == self.pos_pnj:
                self.pos_cible, self.pos_pnj = position_cible, position_pnj     
                
                if 1 == 2:  
                    self.chemin, self.ouverte, self.ferme = AD.CDijkstra.algo_dijkstra( position_pnj, position_cible, self.PATHFINDING.grille_obstacles)   
                else:
                    self.ouverte = []
                    self.ferme = []
                        
                    if position_cible in self.PATHFINDING.ZONES and position_pnj in self.PATHFINDING.ZONES[position_cible]:
                        index_chemin, depart_chemin, arrivee_chemin, sens_lecture = self.PATHFINDING.ZONES[position_pnj][position_cible]
                        if index_chemin > 0:
                            if sens_lecture == 1:
                                self.chemin = self.PATHFINDING.PARCOURS[index_chemin][depart_chemin:arrivee_chemin]
                            else:
                                self.chemin = self.PATHFINDING.PARCOURS[index_chemin][arrivee_chemin:depart_chemin:-1]   
                        else:
                            print("pas de chemin")
                    else:
                        self.chemin = []
                        print("pas de chemin calcule")
                        
                if len(self.chemin) > 1:
                    self.chemin_pathfinding = self.chemin            
                    self.index_chemin = 0
            self.afficher_chemin_jusqua_cible()
            
            
    def afficher_chemin_jusqua_cible(self):     
            
        if ENUM_DEMO.DIJISKRA in VAR.demo and not self.chemin == None:    
            for x, y in self.chemin_pathfinding:
                pygame.draw.circle(VAR.fenetre, (255,255,255), ((x*VAR.dim)+16, (y*VAR.dim)+16), 16, 0)

            if ENUM_DEMO.PATHFINDING_OUVERTFERME in VAR.demo:
                # Dessiner les nœuds
                for noeud in self.ouverte:
                    x, y = noeud.position
                    pygame.draw.circle(VAR.fenetre, (255, 0, 0), ((x * VAR.dim) + 16, (y * VAR.dim) + 16), 8, 0)

                for noeud in self.ferme:
                    x, y = noeud.position
                    pygame.draw.circle(VAR.fenetre, (0, 255, 0), ((x * VAR.dim) + 16, (y * VAR.dim) + 16), 4, 0)
                    
                            
    def traque_est_ce_que_je_poursuis_quelquun(self):
        return len(self.chemin_pathfinding) > 0 
    
    
    def traque_je_me_reoriente_vers_le_nouveau_point(self):
        # --- est ce que je suis a destination
        if self.index_chemin > len(self.chemin_pathfinding)-1:
            self.PNJ.direction = ENUM_DIR.AUCUN
            return
        
        point_suivant = self.chemin_pathfinding[self.index_chemin]
        x, y = self.xInt, self.yInt  # Position actuelle du PNJ
        xNew, yNew = point_suivant
        
        if xNew > x:
            self.PNJ.direction = ENUM_DIR.DROITE
        if xNew < x:
            self.PNJ.direction = ENUM_DIR.GAUCHE
        if yNew > y:
            self.PNJ.direction = ENUM_DIR.BAS
        if yNew < y:
            self.PNJ.direction = ENUM_DIR.HAUT
        
        self.txt = str(("x: " + str(x), "y: "+str(y), "xNew: "+str(xNew), "yNew: "+str(yNew), "direction: "+str(self.PNJ.direction))) 
      
        if (x, y) == (xNew, yNew):
            self.index_chemin += 1    
    
    
    def est_ce_toujours_sur_le_terrain(self, x, y):
        return (0 <= x < VAR.dimension_x) and (0 <= y < VAR.dimension_y)  

    def est_ce_une_intersection(self, x, y, direction_actuelle):
        direction_opposee = self.quelle_est_la_direction_opposee(direction_actuelle)
        for direction, offx, offy in [(ENUM_DIR.BAS, 0, 1), (ENUM_DIR.HAUT, 0, -1), (ENUM_DIR.DROITE, 1, 0), (ENUM_DIR.GAUCHE, -1, 0)]:
            if direction not in [direction_actuelle, direction_opposee] and self.est_ce_toujours_sur_le_terrain(x + offx, y + offy) and self.parcours[x + offx][y + offy]['CHEMIN']:
                return True  # Il y a une autre direction possible

        return False  # Pas d'autre direction possible

   
    def quelle_est_la_direction_opposee(self, direction):
        if direction == ENUM_DIR.BAS:
            return ENUM_DIR.HAUT
        elif direction == ENUM_DIR.HAUT:
            return ENUM_DIR.BAS
        elif direction == ENUM_DIR.DROITE:
            return ENUM_DIR.GAUCHE
        elif direction == ENUM_DIR.GAUCHE:
            return ENUM_DIR.DROITE
    
    def etablir_direction_initiale(self):
        self.je_recupere_ma_position_sur_le_terrain()
        
        x, y = self.xInt, self.yInt  # Position actuelle du PNJ
        directions_possibles = []

        # Vérifier chaque direction autour du PNJ pour les chemins possibles
        for direction, offx, offy in [(ENUM_DIR.BAS, 0, 1), (ENUM_DIR.HAUT, 0, -1), (ENUM_DIR.DROITE, 1, 0), (ENUM_DIR.GAUCHE, -1, 0)]:
            if self.est_ce_toujours_sur_le_terrain(x + offx, y + offy) and self.parcours[x + offx][y + offy]['CHEMIN']:
                directions_possibles.append(direction)

        # Choisir une direction au hasard parmi les directions possibles
        if directions_possibles:
            self.PNJ.direction = random.choice(directions_possibles)
        else:
            self.PNJ.direction = ENUM_DIR.AUCUN  # Aucune direction possible
        
    def je_reflechis(self):
        self.je_recupere_ma_position_sur_le_terrain()
        
        
        # --- je suis mon parcours ...
        if not self.traque_est_ce_que_je_poursuis_quelquun():
            self.je_note_mon_passage_si_nouveau_chemin()
        
            if self.est_ce_que_je_suis_arrive_a_une_intersection():
                directions_disponibles = self.quelles_sont_les_directions_disponibles_autour_de_moi()
                direction_retenue = self.quelle_est_la_direction_la_moins_frequentee(directions_disponibles)
                
                self.je_me_reoriente_vers_la_nouvelle_intersection(direction_retenue)
                self.objectifx, self.objectify = self.quelles_sont_les_coordonnees_de_l_intersection(direction_retenue)       
        
        # --- je me rend vers quelques choses
        else:
            self.traque_je_me_reoriente_vers_le_nouveau_point()     

   

            
    def je_me_reoriente_vers_la_nouvelle_intersection(self, direction_retenue):
        self.PNJ.direction = direction_retenue 
           
    def je_recupere_ma_position_sur_le_terrain(self):
        self.x, self.y = self.PNJ.x, self.PNJ.y
        self.xInt, self.yInt = int(self.PNJ.x), int(self.PNJ.y)
    
    def je_note_mon_passage_si_nouveau_chemin(self):
        nouvelle_position = not ( (self.xInt, self.yInt) == self.position_precedente )
        if nouvelle_position:
            self.position_precedente = (self.xInt, self.yInt)
            self.parcours[self.xInt][self.yInt]['UTILISE'] += 1

    def est_ce_que_je_suis_arrive_a_une_intersection(self):
        xx, yy = int(self.PNJ.x ), int(self.PNJ.y )
        
        # --- atteint que joueur sois bien placé
        if self.PNJ.x % 1 > 0.1 or self.PNJ.y % 1 > 0.4 :
            return False
        
              
        intersection_non_definie = ( (self.objectifx, self.objectify) == (-1, -1) )
        arrive_sur_intersection = (self.objectifx == xx and self.objectify == yy)
        
        if arrive_sur_intersection or intersection_non_definie :
            return True
        return False
        
    # ---   
    def quelles_sont_les_directions_disponibles_autour_de_moi(self):
        directions_disponibles = []
        x, y = self.xInt, self.yInt
        
        for direction, offx, offy in [(ENUM_DIR.BAS, 0, 1), (ENUM_DIR.HAUT, 0, -1), (ENUM_DIR.DROITE, 1, 0), (ENUM_DIR.GAUCHE, -1, 0)]:            
            chemin_dans_les_limites = self.est_ce_toujours_sur_le_terrain(x + offx, y + offy)
            chemin_possible = self.parcours[x + offx][y + offy]['CHEMIN']
           
            if chemin_dans_les_limites and chemin_possible:
                nombre_de_fois_empreinte = self.parcours[x + offx][y + offy]['UTILISE']
                directions_disponibles.append( (direction, nombre_de_fois_empreinte) )
                
        return directions_disponibles
        
    # ---
    def quelle_est_la_direction_la_moins_frequentee(self, directions_disponibles):
        nb_utilise_min = -1
        direction_retenue = ENUM_DIR.AUCUN
        
        for direction, nb_empreinte in directions_disponibles:
            if nb_utilise_min == -1 or nb_empreinte < nb_utilise_min:
                nb_utilise_min = nb_empreinte
                direction_retenue = direction
                
        return direction_retenue
    
    # ---    
    def quelles_sont_les_coordonnees_de_l_intersection(self, direction_retenue):
        x, y = self.xInt, self.yInt  # Position actuelle
        offx, offy = 0, 0  # Décalages pour la direction choisie

        # Identifier les décalages en fonction de la direction
        if direction_retenue == ENUM_DIR.BAS:
            offx, offy = 0, 1
        elif direction_retenue == ENUM_DIR.HAUT:
            offx, offy = 0, -1
        elif direction_retenue == ENUM_DIR.DROITE:
            offx, offy = 1, 0
        elif direction_retenue == ENUM_DIR.GAUCHE:
            offx, offy = -1, 0

        # Continuer dans la direction choisie jusqu'à devoir changer de direction
        while True:
            x_prochain = x + offx
            y_prochain = y + offy

            chemin_en_dehors_des_limites = not self.est_ce_toujours_sur_le_terrain(x_prochain, y_prochain)
            chemin_inexistant = not self.parcours[x_prochain][y_prochain]['CHEMIN']
            
            if chemin_en_dehors_des_limites or chemin_inexistant:
                break  # Arrêter si on atteint les limites ou un obstacle
            
            # Mettre à jour la position actuelle
            x, y = x_prochain, y_prochain
            
            # Vérifier s'il y a un changement de direction possible à la prochaine cellule
            if self.est_ce_une_intersection(x_prochain, y_prochain, direction_retenue):
                break  # S'il y a d'autres directions disponibles, s'arrêter pour réfléchir

        # Retourner les coordonnées du point où il faut changer de direction
        return x, y
                
    

    