from constantes import *
import variables as VAR
import random, pygame

class CIA_PARCOURS:
    # Initialisation de la classe CIA_PARCOURS
    def __init__(self, IA):
        self.IA = IA  # Référence à l'objet IA (Intelligence Artificielle)
        self.PNJ = IA.PNJ  # Référence au Personnage Non-Joueur (PNJ) associé à l'IA
        
        # Définit des objectifs initiaux pour la position du PNJ
        self.objectifx = -1
        self.objectify = -1
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------
    # Fonction principale pour la prise de décision de l'IA
    def je_reflechis(self):
        # Enregistre le passage du PNJ si c'est un nouveau chemin
        self.je_note_mon_passage_si_nouveau_chemin()
        
        # Vérifie si le PNJ est arrivé à une intersection et décide de la direction à prendre
        if self.est_ce_que_je_suis_arrive_a_une_intersection():
            directions_disponibles = self.quelles_sont_les_directions_disponibles_autour_de_moi()
            direction_retenue = self.quelle_est_la_direction_la_moins_frequentee(directions_disponibles)
                
            self.je_me_reoriente_vers_la_nouvelle_intersection(direction_retenue)
            self.mise_a_jour_des_coordonnnes_de_l_intersection(direction_retenue)   
        
      
        
        
        
                
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------
    # Enregistre le passage du PNJ pour éviter de repasser par le même chemin
    def je_note_mon_passage_si_nouveau_chemin(self):
        nouvelle_position = not ((self.IA.xInt, self.IA.yInt) == self.IA.position_precedente)
        if nouvelle_position:
            print("nouvelle position" + str((self.IA.xInt, self.IA.yInt)))
            self.IA.position_precedente = (self.IA.xInt, self.IA.yInt)
            self.IA.parcours[self.IA.xInt][self.IA.yInt]['UTILISE'] += 1

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------
    # Vérifie si le PNJ est arrivé à une intersection
    def est_ce_que_je_suis_arrive_a_une_intersection(self):
        xx, yy = int(round(self.PNJ.x,0)), int(round(self.PNJ.y,0))
            
        # Vérifie si le PNJ est positionné au centre de la cellule
        if not self.IA.est_ce_que_je_suis_au_centre_de_la_cellule():
            return False
                
        intersection_non_definie = ((self.objectifx, self.objectify) == (-1, -1))
        arrive_sur_intersection = (self.objectifx == xx and self.objectify == yy)
            
        return arrive_sur_intersection or intersection_non_definie

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------
    # Détermine les directions disponibles autour du PNJ
    def quelles_sont_les_directions_disponibles_autour_de_moi(self):
        directions_disponibles = []
        x, y = self.IA.xInt, self.IA.yInt
            
        # Parcours les directions possibles et les vérifie
        for direction, offx, offy in [(ENUM_DIR.BAS, 0, 1), (ENUM_DIR.HAUT, 0, -1), (ENUM_DIR.DROITE, 1, 0), (ENUM_DIR.GAUCHE, -1, 0)]:            
            chemin_dans_les_limites = self.est_sur_le_terrain(x + offx, y + offy)
            chemin_possible = self.IA.parcours[x + offx][y + offy]['CHEMIN']
            
            if chemin_dans_les_limites and chemin_possible:
                nombre_de_fois_empreinte = self.IA.parcours[x + offx][y + offy]['UTILISE']
                directions_disponibles.append((direction, nombre_de_fois_empreinte))
                    
        return directions_disponibles

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------
    # Vérifie si une cellule est sur le terrain de jeu
    def est_sur_le_terrain(self, x_cellule, y_cellule):
        return (0 <= x_cellule < VAR.dimension_x) and (0 <= y_cellule < VAR.dimension_y)

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------
    # Sélectionne la direction la moins fréquentée parmi les directions disponibles
    def quelle_est_la_direction_la_moins_frequentee(self, directions_disponibles):
        nb_utilise_min = -1
        direction_retenue = ENUM_DIR.AUCUN
            
        for direction, nb_empreinte in directions_disponibles:
            if nb_utilise_min == -1 or nb_empreinte < nb_utilise_min:
                nb_utilise_min = nb_empreinte
                direction_retenue = direction
                    
        return direction_retenue

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------
    # Met à jour les coordonnées de la prochaine intersection
    def mise_a_jour_des_coordonnnes_de_l_intersection(self, direction_retenue):
        x, y = self.IA.xInt, self.IA.yInt
        offx, offy = 0, 0

        # Calcule les décalages en fonction de la direction retenue
        if direction_retenue == ENUM_DIR.BAS:
            offx, offy = 0, 1
        elif direction_retenue == ENUM_DIR.HAUT:
            offx, offy = 0, -1
        elif direction_retenue == ENUM_DIR.DROITE:
            offx, offy = 1, 0
        elif direction_retenue == ENUM_DIR.GAUCHE:
            offx, offy = -1, 0

        # Détermine le prochain objectif en suivant la direction choisie
        while True:
            x_prochain = x + offx
            y_prochain = y + offy

            # Vérifie les limites et les obstacles sur le chemin
            if not self.est_sur_le_terrain(x_prochain, y_prochain) or not self.IA.parcours[x_prochain][y_prochain]['CHEMIN']:
                break
            
            x, y = x_prochain, y_prochain
                
            # Vérifie s'il y a une intersection à la prochaine cellule
            if self.est_ce_une_intersection(x_prochain, y_prochain, direction_retenue):
                break

        self.objectifx, self.objectify = x, y

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------
    # Vérifie si la cellule est une intersection
    def est_ce_une_intersection(self, x, y, direction_actuelle):
        direction_opposee = self.quelle_est_la_direction_opposee(direction_actuelle)
        for direction, offx, offy in [(ENUM_DIR.BAS, 0, 1), (ENUM_DIR.HAUT, 0, -1), (ENUM_DIR.DROITE, 1, 0), (ENUM_DIR.GAUCHE, -1, 0)]:
            if direction not in [direction_actuelle, direction_opposee] and self.est_sur_le_terrain(x + offx, y + offy) and self.IA.parcours[x + offx][y + offy]['CHEMIN']:
                return True

        return False

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------
    # Renvoie la direction opposée à celle donnée
    def quelle_est_la_direction_opposee(self, direction):
        if direction == ENUM_DIR.BAS:
            return ENUM_DIR.HAUT
        elif direction == ENUM_DIR.HAUT:
            return ENUM_DIR.BAS
        elif direction == ENUM_DIR.DROITE:
            return ENUM_DIR.GAUCHE
        elif direction == ENUM_DIR.GAUCHE:
            return ENUM_DIR.DROITE
        else:
            return ENUM_DIR.AUCUN

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------
    # Réoriente le PNJ vers la nouvelle intersection
    def je_me_reoriente_vers_la_nouvelle_intersection(self, direction_retenue):
        self.PNJ.direction = direction_retenue 


    def DEBUG_afficher_parcours_preenregistre(self):
        for y in range(0, VAR.dimension_y):
            for x in range(0, VAR.dimension_x):
                if self.IA.parcours[x][y]['CHEMIN']:
                    pygame.draw.rect(VAR.fenetre, (32,32,32), (x * VAR.dim, y* VAR.dim, VAR.dim, VAR.dim), 0)   
                    
                utilise = self.IA.parcours[x][y]['UTILISE']
                if utilise > 0:
                    pygame.draw.circle(VAR.fenetre, (255 - (utilise * 16),32,32), ((x * VAR.dim)+16, (y* VAR.dim)+16), 8, 0)   