import variables as VAR
import objet as OBJ
import pygame
import time

from constantes import *
import fonctions as FCT

# Définition des constantes (index, coeffX, coeffY, traversable)


OBJ_EXTINCTEUR =  (C_INTERIOR + 5213, 1, 2, C_OBSTACLE)
OBJ_ARB1x2_GRIS = (C_INTERIOR + 9713, 1, 3, C_TRAVERSABLE)
OBJ_ARB1x3_GRIS = (C_INTERIOR + 9714, 1, 3, C_TRAVERSABLE)
OBJ_ARB2x3_GRIS = (C_INTERIOR + 9715, 2, 3, C_TRAVERSABLE)
OBJ_ARB1x3_GRIS2 = (C_MODERN + 150, 1, 3, C_TRAVERSABLE)
OBJ_CHAISE_DEV =  (C_MODERN + 177, 1, 2, C_OBSTACLE)
OBJ_CHAISE_DER =  (C_MODERN + 179, 1, 2, C_OBSTACLE)

OBJ_TRACE1 = (17106, 1, 1, C_TRAVERSABLE)
OBJ_TRACE2 = (17105, 1, 1, C_TRAVERSABLE)
# Liste de tous les objets
objets = [OBJ_CHAISE_DEV, OBJ_CHAISE_DER, OBJ_ARB1x2_GRIS, OBJ_ARB1x3_GRIS, OBJ_ARB2x3_GRIS, OBJ_ARB1x3_GRIS2] #, OBJ_TRACE1, OBJ_TRACE2]

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
              
        image, image_mask, etat = VAR.images[index]          
        if (index in LISTE_SCALE_OBJET) or force:  
            if force: etat = C_OBSTACLE                                     
            objet = OBJ.CObjet(self.MOTEUR, index, x, y, 0, 0, image, image_mask, etat)  
                      
        if not objet == None:
            key = "{:04d}{:04d}{:01d}".format((y * VAR.dim) + VAR.dim, x * VAR.dim, couche)
            self.liste[key] = objet 
            
        return objet
    
    
      
    def afficher(self): 
        t = time.time()       
        
        # --- genere une liste de joueurs et de pnjs
        liste_personnages = {}
        for personnage in self.MOTEUR.PERSONNAGES.JOUEURS + self.MOTEUR.PERSONNAGES.PNJS:
            x = personnage.position_int_x() 
            y = personnage.position_int_y()+16
            key = "{:04d}{:04d}{:01d}".format(y, x, 0)
            liste_personnages[key] = personnage
        
        # --- fusionne la liste des objets et des joueurs
        if not ENUM_DEMO.BLOCAGE in VAR.demo:    
            listes_fusionnees = {**self.liste, **liste_personnages}        
        else:
            listes_fusionnees = liste_personnages            
        liste_objets_tries = sorted( listes_fusionnees.items(), key=lambda x: x[0])
        
        
        # --- affiche chaque objets
        FCT.Performance('OBJETS.afficher( - creation liste)', t)  
        i = 0      
        for key, objet in liste_objets_tries:   
            objet.afficher()
                      
            if 2 < objet.x < 10 and 10 < objet.y < 16:
                nombre1 = int(key[0:4])  # Convertit "0123" en entier
                nombre2 = int(key[4:8])  # Convertit "4567" en entier
                nombre3 = int(key[8])    # Convertit "0" en entier

                key1 = "y:" + str(nombre1//VAR.dim)+" x:" + str(nombre2//VAR.dim)+" c:" + str(nombre3)
                key2 = key
                
                txt = key1 + " (" + str(objet.index) +") " + str(key2)
                image_texte = VAR.ecriture.render( txt , True, (255,0,0))
                VAR.fenetre.blit(image_texte, (1400, (i * 18)))     
                i+=1
        FCT.Performance('OBJETS.afficher()', t)