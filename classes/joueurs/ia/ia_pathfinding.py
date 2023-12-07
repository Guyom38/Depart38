from constantes import *
import variables as VAR
import random, pygame
import classes.joueurs.algos.algo_dijkstra as AD

class CIA_PATHFINDING:
    def __init__(self, IA):
        self.IA = IA
        self.PNJ = IA.PNJ
        
        self.PATHFINDING = self.IA.MOTEUR.PERSONNAGES.PATHFINDING
        
        self.index_chemin = 0
        self.chemin_pathfinding = []

        self.pos_cible, self.pos_pnj = None, None
        self.chemin, self.ouverte, self.ferme = None, None, None
        
    def traque_calculer_le_chemin_jusqua(self, position_cible):
        position_pnj = (int(self.PNJ.x), int(self.PNJ.y))
    
        if not position_cible == self.pos_cible or not position_pnj == self.pos_pnj:
            self.pos_cible, self.pos_pnj = position_cible, position_pnj     
                    
            if 1 == 1:  
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
                    self.IA.chemin = []
                    print("pas de chemin calcule")
                            
            if len(self.chemin) > 1:
                self.chemin_pathfinding = self.chemin            
                self.index_chemin = 0
        self.afficher_chemin_jusqua_cible()
                
    def traque_est_ce_que_je_poursuis_quelquun(self):
        return len(self.chemin_pathfinding) > 0 
            
        
    def traque_je_me_reoriente_vers_le_nouveau_point(self):
        # --- est ce que je suis a destination
        if self.index_chemin > len(self.chemin_pathfinding)-1:
            self.PNJ.direction = ENUM_DIR.AUCUN
            return
            
        point_suivant = self.chemin_pathfinding[self.index_chemin]
        x, y = self.IA.xInt, self.IA.yInt  # Position actuelle du PNJ
        xNew, yNew = point_suivant
            
        if self.IA.est_ce_que_je_suis_au_centre_de_la_cellule():
            if xNew > x:
                self.PNJ.direction = ENUM_DIR.DROITE
            if xNew < x:
                self.PNJ.direction = ENUM_DIR.GAUCHE
            if yNew > y:
                self.PNJ.direction = ENUM_DIR.BAS
            if yNew < y:
                self.PNJ.direction = ENUM_DIR.HAUT
                
            if (x, y) == (xNew, yNew):
                self.index_chemin += 1    
                                
    def afficher_chemin_jusqua_cible(self):     
        
        if ENUM_DEMO.DIJISKRA in VAR.demo and len(self.chemin) > 0:  
            for x, y in self.chemin: #_pathfinding:
                pygame.draw.circle(VAR.fenetre, (255,255,255), ((x*VAR.dim)+16, (y*VAR.dim)+16), 8, 0)

            if ENUM_DEMO.PATHFINDING_OUVERTFERME in VAR.demo:
                # Dessiner les nœuds
                for noeud in self.ouverte:
                    x, y = noeud.position
                    pygame.draw.circle(VAR.fenetre, (255, 0, 0), ((x * VAR.dim) + 16, (y * VAR.dim) + 16), 6, 0)

                for noeud in self.ferme:
                    x, y = noeud.position
                    pygame.draw.circle(VAR.fenetre, (0, 255, 0), ((x * VAR.dim) + 16, (y * VAR.dim) + 16), 4, 0)
                    
