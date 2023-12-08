from constantes import *
import variables as VAR
import random, pygame
import classes.joueurs.algos.algo_dijkstra as AD

class CIA_PATHFINDING:
    # Initialisation de la classe CIA_PATHFINDING
    def __init__(self, IA):
        self.IA = IA  # Référence à l'objet IA (Intelligence Artificielle)
        self.PNJ = IA.PNJ  # Référence au Personnage Non-Joueur (PNJ) associé à l'IA
        
        # Accès au système de pathfinding du moteur de jeu
        self.PATHFINDING = self.IA.MOTEUR.PERSONNAGES.PATHFINDING
        
        self.index_chemin = 0  # Index pour suivre la progression sur le chemin trouvé
        self.chemin = []  # Liste pour stocker le chemin calculé

        # Initialisation des variables pour la position de la cible et du PNJ
        self.pos_cible, self.pos_pnj = None, None
        # Listes pour gérer les nœuds ouverts et fermés dans l'algorithme de pathfinding
        self.ouverte, self.ferme = None, None
    
 
    # Méthode pour calculer le chemin jusqu'à une position cible
    def traque_calculer_le_chemin_jusqua(self, position_cible):
        position_pnj = (self.PNJ.position_x(), self.PNJ.position_y())  # Position actuelle du PNJ
        chemin_initialise = False
        
        # Vérifie si la cible ou la position du PNJ a changé
        if not position_cible == self.pos_cible or not position_pnj == self.pos_pnj:
            self.pos_cible, self.pos_pnj = position_cible, position_pnj     
                 
            mode = 2  
            # Utilisation de l'algorithme de Dijkstra pour le pathfinding
            if mode == 1:  # Ce if semble être un placeholder pour une condition future
                if not VAR.THREAD_PATHFINDING == None:
                    VAR.THREAD_PATHFINDING.ajouter_un_chemin_a_calculer(self, position_pnj, position_cible, self.PATHFINDING.grille_obstacles)
                else:
                    print("PROBLEME PAS INITIALISE (traque_calculer_le_chemin_jusqua)")
                    
            elif mode == 2:
                chemin_pathfinding, self.ouverte, self.ferme = AD.CDijkstra.algo_dijkstra(position_pnj, position_cible, self.PATHFINDING.grille_obstacles)   
                chemin_initialise = True
                
            elif mode == 3:
                # Bloc else pour la gestion alternative du pathfinding
                self.ouverte = []
                self.ferme = []
                
                # Vérifie si la cible est dans une zone spécifique et trouve un chemin
                if position_cible in self.PATHFINDING.ZONES and position_pnj in self.PATHFINDING.ZONES[position_cible]:
                    index_chemin, depart_chemin, arrivee_chemin, sens_lecture = self.PATHFINDING.ZONES[position_pnj][position_cible]
                    # Traite le chemin en fonction du sens de lecture
                    if index_chemin > 0:
                        if sens_lecture == 1:
                            chemin_pathfinding = self.PATHFINDING.PARCOURS[index_chemin][depart_chemin:arrivee_chemin]
                        else:
                            chemin_pathfinding = self.PATHFINDING.PARCOURS[index_chemin][arrivee_chemin:depart_chemin:-1]   
                        chemin_initialise = True
                    else:
                        print("pas de chemin")
                else:
                    chemin_pathfinding = []
                    print("pas de chemin calcule")
                            
            # Mise à jour du chemin si un chemin valide est trouvé
            if chemin_initialise and len(chemin_pathfinding) > 1:
                self.chemin = chemin_pathfinding            
                self.index_chemin = 0
                
        # Affiche le chemin calculé pour le debug
        self.DEBUG_afficher_chemin_jusqua_cible()
                
    # Méthode pour vérifier si l'IA poursuit actuellement quelqu'un
    def il_y_a_t_il_poursuite(self):
        return len(self.chemin) > 0 

    # Méthode pour réorienter le PNJ vers le nouveau point sur le chemin
    def traque_je_me_reoriente_vers_le_nouveau_point(self):
        # Vérifie si le PNJ a atteint sa destination
        if self.index_chemin >= len(self.chemin) :
            self.PNJ.direction = ENUM_DIR.AUCUN
            return
            
        point_suivant = self.chemin[self.index_chemin]
        xx, yy = self.PNJ.position_x(), self.PNJ.position_y()  # Position actuelle du PNJ
        xNew, yNew = point_suivant  # Prochain point du chemin
            
        # Réoriente le PNJ si celui-ci est au centre de la cellule
        if self.IA.est_ce_que_je_suis_au_centre_de_la_cellule():
            # Ajustement de la direction du PNJ en fonction de la position du point suivant
            if xNew > xx:
                self.PNJ.direction = ENUM_DIR.DROITE
            if xNew < xx:
                self.PNJ.direction = ENUM_DIR.GAUCHE
            if yNew > yy:
                self.PNJ.direction = ENUM_DIR.BAS
            if yNew < yy:
                self.PNJ.direction = ENUM_DIR.HAUT
                
            # Mise à jour de l'index du chemin si le PNJ atteint le point suivant
            if (xx, yy) == (xNew, yNew):
                self.index_chemin += 1    


                                
    # Méthode de debug pour afficher le chemin jusqu'à la cible
    def DEBUG_afficher_chemin_jusqua_cible(self): 
        if ENUM_DEMO.DIJISKRA in VAR.demo and self.il_y_a_t_il_poursuite():  
            # Dessiner le chemin
            for x, y in self.chemin:
                pygame.draw.circle(VAR.fenetre, (255,255,255), ((x*VAR.dim)+16, (y*VAR.dim)+16), 8, 0)

            if ENUM_DEMO.PATHFINDING_OUVERTFERME in VAR.demo:
                # Dessiner les nœuds ouverts et fermés pour le pathfinding
                for noeud in self.ouverte:
                    x, y = noeud.position
                    pygame.draw.circle(VAR.fenetre, (255, 0, 0), ((x * VAR.dim) + 16, (y * VAR.dim) + 16), 6, 0)

                for noeud in self.ferme:
                    x, y = noeud.position
                    pygame.draw.circle(VAR.fenetre, (0, 255, 0), ((x * VAR.dim) + 16, (y * VAR.dim) + 16), 4, 0)
