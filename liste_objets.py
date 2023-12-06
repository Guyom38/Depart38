import variables as VAR
from constantes import *

class CListe_Objets:
    def __init__(self):
        self.objets = []
    
    def initialiser_objets(self):
        
        # Définition des constantes (index, coeffX, coeffY, traversable)
        # LISTE_SCALE_OBJET[index] = parametres

        #   - (x, y) = position de l'image sur la plaquette
        #   - obstacle ou traversable
        #   - Animation

        OBJ_EXTINCTEUR =  ((VAR.C_INTERIOR, 5197), (1, 2), C_OBSTACLE, None, True)
        OBJ_ARB1x2_GRIS = ((VAR.C_INTERIOR, 9697), (1, 3), C_TRAVERSABLE, None, False)
        OBJ_ARB1x3_GRIS = ((VAR.C_INTERIOR, 9682), (1, 3), C_TRAVERSABLE, None, False)
        OBJ_ARB2x3_GRIS = ((VAR.C_INTERIOR, 9683), (2, 3), C_TRAVERSABLE, None, False)
        OBJ_ARB1x3_GRIS2 = ((VAR.C_MODERN_OFFICE, 118), (1, 3), C_TRAVERSABLE, None, False)
        OBJ_CHAISE_DEV =  ((VAR.C_MODERN_OFFICE, 161), (1, 2), C_OBSTACLE, None, False)
        OBJ_CHAISE_DER =  ((VAR.C_MODERN_OFFICE, 163), (1, 2), C_OBSTACLE, None, False)
        OBJ_CHAISE2_DER =  ((VAR.C_MODERN_OFFICE, 131), (1, 2), C_OBSTACLE, None, False)

        OBJ_BAIE_INFORMATIQUE = ((VAR.C_INTERIOR, 8409), (1, 3), C_OBSTACLE, True, False)
        OBJ_4x4_MONITEURS = ((VAR.C_INTERIOR, 8372), (4, 3), C_TRAVERSABLE, True, False)

        # Liste de tous les objets
        self.objets = [OBJ_EXTINCTEUR,
                OBJ_CHAISE_DEV, OBJ_CHAISE_DER, OBJ_CHAISE2_DER, OBJ_ARB1x2_GRIS, OBJ_ARB1x3_GRIS, OBJ_ARB2x3_GRIS, OBJ_ARB1x3_GRIS2,
                OBJ_4x4_MONITEURS, OBJ_BAIE_INFORMATIQUE] #, OBJ_TRACE1, OBJ_TRACE2]
