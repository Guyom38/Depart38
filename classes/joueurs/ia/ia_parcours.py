from constantes import *
import variables as VAR
import random

class CIA_PARCOURS:
    def __init__(self, IA):
        self.IA = IA
        self.PNJ = IA.PNJ
        
        # Objectifs initiaux pour la position du PNJ
        self.objectifx = -1
        self.objectify = -1
    
    def je_reflechis(self):
        self.je_note_mon_passage_si_nouveau_chemin()
        
        if self.est_ce_que_je_suis_arrive_a_une_intersection():
            directions_disponibles = self.quelles_sont_les_directions_disponibles_autour_de_moi()
            direction_retenue = self.quelle_est_la_direction_la_moins_frequentee(directions_disponibles)
                
            self.je_me_reoriente_vers_la_nouvelle_intersection(direction_retenue)
            self.mise_a_jour_des_coordonnnes_de_l_intersection(direction_retenue)   
                
    def je_note_mon_passage_si_nouveau_chemin(self):
        nouvelle_position = not ( (self.IA.xInt, self.IA.yInt) == self.IA.position_precedente )
        if nouvelle_position:
            self.IA.position_precedente = (self.IA.xInt, self.IA.yInt)
            self.IA.parcours[self.IA.xInt][self.IA.yInt]['UTILISE'] += 1
            

    def est_ce_que_je_suis_arrive_a_une_intersection(self):
        xx, yy = int(self.PNJ.x ), int(self.PNJ.y )
            
        # --- atteint que joueur sois bien placé
            
        if not self.IA.est_ce_que_je_suis_au_centre_de_la_cellule():
            return False
                
        intersection_non_definie = ( (self.objectifx, self.objectify) == (-1, -1) )
        arrive_sur_intersection = (self.objectifx == xx and self.objectify == yy)
            
        if arrive_sur_intersection or intersection_non_definie :
            return True
        return False
            
        # ---   
    def quelles_sont_les_directions_disponibles_autour_de_moi(self):
        directions_disponibles = []
        x, y = self.IA.xInt, self.IA.yInt
            
        for direction, offx, offy in [(ENUM_DIR.BAS, 0, 1), (ENUM_DIR.HAUT, 0, -1), (ENUM_DIR.DROITE, 1, 0), (ENUM_DIR.GAUCHE, -1, 0)]:            
            chemin_dans_les_limites = self.est_sur_le_terrain(x + offx, y + offy)
            chemin_possible = self.IA.parcours[x + offx][y + offy]['CHEMIN']
            
            if chemin_dans_les_limites and chemin_possible:
                nombre_de_fois_empreinte = self.IA.parcours[x + offx][y + offy]['UTILISE']
                directions_disponibles.append( (direction, nombre_de_fois_empreinte) )
                    
        return directions_disponibles

    def est_sur_le_terrain(self, x_cellule, y_cellule):
        return (0 <= x_cellule < VAR.dimension_x) and (0 <= y_cellule < VAR.dimension_y) 
                
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
    def mise_a_jour_des_coordonnnes_de_l_intersection(self, direction_retenue):
        x, y = self.IA.xInt, self.IA.yInt  # Position actuelle
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

            chemin_en_dehors_des_limites = not self.est_sur_le_terrain(x_prochain, y_prochain)
            chemin_inexistant = not self.IA.parcours[x_prochain][y_prochain]['CHEMIN']
                
            if chemin_en_dehors_des_limites or chemin_inexistant:
                break  # Arrêter si on atteint les limites ou un obstacle
                
            # Mettre à jour la position actuelle
            x, y = x_prochain, y_prochain
                
            # Vérifier s'il y a un changement de direction possible à la prochaine cellule
            if self.est_ce_une_intersection(x_prochain, y_prochain, direction_retenue):
                break  # S'il y a d'autres directions disponibles, s'arrêter pour réfléchir

        # Retourner les coordonnées du point où il faut changer de direction
        self.objectifx, self.objectify = x, y



    def est_ce_une_intersection(self, x, y, direction_actuelle):
        direction_opposee = self.quelle_est_la_direction_opposee(direction_actuelle)
        for direction, offx, offy in [(ENUM_DIR.BAS, 0, 1), (ENUM_DIR.HAUT, 0, -1), (ENUM_DIR.DROITE, 1, 0), (ENUM_DIR.GAUCHE, -1, 0)]:
            if direction not in [direction_actuelle, direction_opposee] and self.est_sur_le_terrain(x + offx, y + offy) and self.IA.parcours[x + offx][y + offy]['CHEMIN']:
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
        
        else:
            return ENUM_DIR.AUCUN
        
                
    def je_me_reoriente_vers_la_nouvelle_intersection(self, direction_retenue):
        self.PNJ.direction = direction_retenue 
                
