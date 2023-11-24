import fonctions as FCT
import variables as VAR
import pygame
import time
from queue import PriorityQueue

class CNoeud:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position  # position est un tuple (x, y)
        self.g = 0  # Coût depuis le départ
        self.h = 0  # Heuristique jusqu'à l'arrivée
        self.f = 0  # Coût total (g + h)

    def __eq__(self, autre):
        return self.position == autre.position
    

def generer_grille(arrayBlocage):
  
    # Initialiser la grille de présence d'obstacles
    grille_obstacles = []

    # Parcourir le bitmap avec un décalage de 16 et un pas de 32
    for y in range(16, len(arrayBlocage), 32):
        ligne_obstacles = []
        for x in range(16, len(arrayBlocage[y]), 32):
            # Vérifier si la valeur du pixel est supérieure à 0            
            ligne_obstacles.append(arrayBlocage[y][x] )
        grille_obstacles.append(ligne_obstacles)

    # La grille_obstacles contient maintenant la présence d'obstacles
    return grille_obstacles
 
 

def astar(depart, arrivee, grille):
    
     
    # Créer les nœuds de départ et d'arrivée
    noeud_depart = CNoeud(None, depart)
    noeud_arrivee = CNoeud(None, arrivee)

    liste_ouverte = []
    liste_fermee = []

    liste_ouverte.append(noeud_depart)

    while len(liste_ouverte) > 0:
        noeud_actuel = liste_ouverte[0]
        index_actuel = 0
        for index, item in enumerate(liste_ouverte):
            if item.f < noeud_actuel.f:
                noeud_actuel = item
                index_actuel = index

        liste_ouverte.pop(index_actuel)
        liste_fermee.append(noeud_actuel)

        # Si le noeud actuel est le noeud d'arrivée, reconstruire le chemin
        if noeud_actuel == noeud_arrivee:
            chemin = []
            courant = noeud_actuel
            while courant is not None:
                chemin.append(courant.position)
                courant = courant.parent
                
            return chemin[::-1], liste_ouverte, liste_fermee  # Retourne le chemin inverse

        # Générer les enfants (voisins) du noeud actuel
        enfants = []
        for nouvelle_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacentes (haut, bas, gauche, droite)
            position_noeud = (noeud_actuel.position[0] + nouvelle_position[0], noeud_actuel.position[1] + nouvelle_position[1])

            # Assurez-vous que la position est dans la grille et traversable
            if position_noeud[0] > (len(grille) - 1) or position_noeud[0] < 0 or position_noeud[1] > (len(grille[len(grille)-1]) -1) or position_noeud[1] < 0:
                continue
            if grille[position_noeud[0]][position_noeud[1]] != 0:
                continue

            nouveau_noeud = CNoeud(noeud_actuel, position_noeud)
            enfants.append(nouveau_noeud)

        # Parcourir les enfants
        for enfant in enfants:
            # L'enfant est sur la liste fermée
            if len([noeud_ferme for noeud_ferme in liste_fermee if noeud_ferme == enfant]) > 0:
                continue

            # Créer les valeurs f, g et h
            enfant.g = noeud_actuel.g + 1
            enfant.h = abs(enfant.position[0] - noeud_arrivee.position[0]) + abs(enfant.position[1] - noeud_arrivee.position[1])
            enfant.f = enfant.g + enfant.h

            # L'enfant est déjà dans la liste ouverte
            if len([i for i in liste_ouverte if enfant == i and enfant.g > i.g]) > 0:
                continue

            # Ajouter l'enfant à la liste ouverte
            liste_ouverte.append(enfant)

    return None, None, None  # Aucun chemin n'a été trouvé




class CNoeud2:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0  # Coût depuis le départ

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def __lt__(self, other):
        return self.g < other.g

from queue import PriorityQueue

class CNoeud2:
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

def dijkstra(depart, arrivee, grille):
    noeud_depart = CNoeud2(None, depart)
    noeud_depart.g = 0
    noeud_arrivee = CNoeud2(None, arrivee)

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

            if position_noeud[0] > (len(grille) - 1) or position_noeud[0] < 0 or position_noeud[1] > (len(grille[len(grille)-1]) -1) or position_noeud[1] < 0:
                continue
            if grille[position_noeud[0]][position_noeud[1]] != 0:
                continue

            nouveau_noeud = CNoeud2(noeud_actuel, position_noeud)

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

# Exemple d'utilisation avec une grille et des positions de départ et d'arrivée
# grille = [[0, 0, 0, ...], [1, 0, 1, ...], ...]
# depart = (x1, y1)
# arrivee = (x2, y2)
# chemin, ouverte_set, fermee_set = dijkstra(depart, arrivee, grille)

