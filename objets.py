import variables as VAR
import objet as OBJ
import pygame

from constantes import *

# Définition des constantes (index, coeffX, coeffY, traversable)


OBJ_EXTINCTEUR =  (C_INTERIOR + 5213, 1, 2, C_OBSTACLE)
OBJ_ARB1x2_GRIS = (C_INTERIOR + 9713, 1, 3, C_TRAVERSABLE)
OBJ_ARB1x3_GRIS = (C_INTERIOR + 9714, 1, 3, C_TRAVERSABLE)
OBJ_ARB2x3_GRIS = (C_INTERIOR + 9715, 2, 3, C_TRAVERSABLE)
OBJ_CHAISE_DEV =  (C_MODERN + 177, 1, 2, C_OBSTACLE)
OBJ_CHAISE_DER =  (C_MODERN + 179, 1, 2, C_OBSTACLE)

OBJ_TRACE1 = (17106, 1, 1, C_TRAVERSABLE)
OBJ_TRACE2 = (17105, 1, 1, C_TRAVERSABLE)
# Liste de tous les objets
objets = [OBJ_EXTINCTEUR, OBJ_ARB1x2_GRIS, OBJ_ARB1x3_GRIS, OBJ_ARB2x3_GRIS, OBJ_CHAISE_DER, OBJ_CHAISE_DEV, OBJ_TRACE1, OBJ_TRACE2]

# Création du dictionnaire avec une boucle for
LISTE_SCALE_OBJET = {}
for objet in objets:
    index = objet[0]
    parametres = objet[1:]
    LISTE_SCALE_OBJET[index] = parametres





class CObjets:        
    def __init__(self, moteur):
        self.MOTEUR = moteur
        self.liste = {}        
        
    def traitement_objet(self, index, x, y, couche, force = False):
        objet = None
        
        image, etat = VAR.images[index]          
        if (index in LISTE_SCALE_OBJET) or force:  
            if force: etat = C_OBSTACLE                                     
            objet = OBJ.CObjet(self.MOTEUR, index, x, y, 0, 0, image, etat)            
            if index == 404:
                print("kk")
        if not objet == None:
            key = "{:04d}{:04d}{:01d}".format(y * VAR.dim, x * VAR.dim, couche)
            self.liste[key] = objet 
            
        return objet
      