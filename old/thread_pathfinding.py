import variables as VAR
import time
import classes.joueurs.algos.algo_dijkstra as AD
import queue

class CThread_Pathfinding:
    def __init__(self):
        self.chemin_en_attente = queue.Queue()
        self.grille = None

    def ajouter_un_chemin_a_calculer(self, ia_pnj, depart, arrive, grille):
        if self.grille == None: 
            self.grille = grille
            
        self.chemin_en_attente.put( (ia_pnj, depart, arrive) ) 
        
    def demarrer(self):
        
        while VAR.boucle:
            
            if self.chemin_en_attente.qsize() > 0:
                t = time.time()
                IA_PNJ, depart, arrive = self.chemin_en_attente.get()
               
                chemin_pathfinding, self.ouverte, self.ferme = AD.CDijkstra.algo_dijkstra(depart, arrive, self.grille)
                
                IA_PNJ.chemin = chemin_pathfinding            
                IA_PNJ.index_chemin = 0
                print(str(round(time.time() - t, 3)))
                
            time.sleep(0.0001)