from enum import *

# --- Terrain
C_AUCUN = 0
C_OBSTACLE = 1
C_TRAVERSABLE = 2

C_ROOM = 1
C_MODERN = 225
C_INTERIOR = 1073


# --- Joueurs
class ENUM_DIR:
    BAS = 270
    GAUCHE = 0
    DROITE = 180
    HAUT = 90
    AUCUN = None

class ENUM_ANIMATION:
    ARRETER = 0
    IDEAL = 1
    MARCHER = 2
    ASSIS = 4
    JOUER_TELEPHONE = 6
    BOUQUINER = 7
    COURIR = 8
    TOUCHER = 19