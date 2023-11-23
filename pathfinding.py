class CNoeud:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position  # position est un tuple (x, y)
        self.g = 0  # Coût depuis le départ
        self.h = 0  # Heuristique jusqu'à l'arrivée
        self.f = 0  # Coût total (g + h)

    def __eq__(self, autre):
        return self.position == autre.position
    

def astar(grille, depart, arrivee):
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
            return chemin[::-1]  # Retourne le chemin inverse

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

    return None  # Aucun chemin n'a été trouvé
