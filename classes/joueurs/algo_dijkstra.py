
from queue import PriorityQueue

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


class CDijkstra:
    def algo_dijkstra(depart, arrivee, grille_obstacles):
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

                if position_noeud[0] > (len(grille_obstacles) - 1) or position_noeud[0] < 0 or position_noeud[1] > (len(grille_obstacles[len(grille_obstacles)-1]) -1) or position_noeud[1] < 0:
                    continue
                
                if grille_obstacles[position_noeud[0]][position_noeud[1]] != 0:
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