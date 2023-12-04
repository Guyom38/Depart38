from enum import *

# --- Terrain
C_AUCUN = 0
C_OBSTACLE = 1
C_TRAVERSABLE = 2

C_ROOM = 1
C_MODERN = 225
C_INTERIOR = 1073

class ENUM_PROGRESSION_ETAT:
    AUCUN = False
    SE_DECHARGE = 1
    SE_RECHARGE = 2
    OBJECTIF_ATTEINT = 3

class ENUM_DEMO:
    DESACTIVER = 0
    ASTAR = 1
    DIJISKRA = 2
    CHAMP_VISION = 3
    REPERES = 4
    COLLISION = 5
    CHEMIN_VINCENT = 6
    GENERER_PATHFINDING = 7
    PATHFINDING_OUVERTFERME = 8
    BLOCAGE = 9
    
# --- Joueurs
class ENUM_DIR:
    BAS = 270
    GAUCHE = 0
    DROITE = 180
    HAUT = 90
    AUCUN = None

class ENUM_ANIMATION:
    ARRETER = (0, 1)
    IDEAL = (1, 6)
    MARCHER = (2, 6)
    ASSIS = (4, 6)
    JOUER_TELEPHONE = (6, 6)
    BOUQUINER = (7, 6)
    COURIR = (8, 6)
    TOUCHER = (19, 6)
    
class CBouton:
    B_X = 0
    B_A = 1
    B_B = 2
    B_Y = 3
    B_L = 4
    B_R = 5
    B_START = 9
    B_SELECT = 8