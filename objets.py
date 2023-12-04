import variables as VAR
import objet as OBJ
import pygame
import time, os

from constantes import *
import fonctions as FCT

# Définition des constantes (index, coeffX, coeffY, traversable)
# LISTE_SCALE_OBJET[index] = parametres

#   - (x, y) = position de l'image sur la plaquette
#   - obstacle ou traversable
#   - Animation

OBJ_EXTINCTEUR =  ((C_INTERIOR, 5197), (1, 2), C_OBSTACLE, None)
OBJ_ARB1x2_GRIS = ((C_INTERIOR, 9697), (1, 3), C_TRAVERSABLE, None)
OBJ_ARB1x3_GRIS = ((C_INTERIOR, 9682), (1, 3), C_TRAVERSABLE, None)
OBJ_ARB2x3_GRIS = ((C_INTERIOR, 9683), (2, 3), C_TRAVERSABLE, None)
OBJ_ARB1x3_GRIS2 = ((C_MODERN, 118), (1, 3), C_TRAVERSABLE, None)
OBJ_CHAISE_DEV =  ((C_MODERN, 161), (1, 2), C_OBSTACLE, None)
OBJ_CHAISE_DER =  ((C_MODERN, 163), (1, 2), C_OBSTACLE, None)

OBJ_BAIE_INFORMATIQUE = ((C_INTERIOR, 8409), (1, 3), C_OBSTACLE, True)
OBJ_4x4_MONITEURS = ((C_INTERIOR, 8372), (4, 3), C_TRAVERSABLE, True)

OBJ_TRACE1 = ((0, 17106), (1, 1), C_TRAVERSABLE, None)
OBJ_TRACE2 = ((0, 17105), (1, 1), C_TRAVERSABLE, None)

# Liste de tous les objets
objets = [OBJ_CHAISE_DEV, OBJ_CHAISE_DER, OBJ_ARB1x2_GRIS, OBJ_ARB1x3_GRIS, OBJ_ARB2x3_GRIS, OBJ_ARB1x3_GRIS2,
          OBJ_4x4_MONITEURS, OBJ_BAIE_INFORMATIQUE] #, OBJ_TRACE1, OBJ_TRACE2]






class CObjets:        
    def __init__(self, moteur):
        self.MOTEUR = moteur
        self.liste = {}  
        
        for objet in objets:
            index_offset_plaquette, index_sur_plaquette = objet[0]
            index = index_offset_plaquette + index_sur_plaquette
            VAR.DICO_OBJETS_PARTICULIERS[index] = objet
    
    
    
    
       
    def traitement_objet(self, index, x, y, couche, force = False):
        objet = None  
              
        image, image_mask, etat = VAR.images[index]          
        if (index in VAR.DICO_OBJETS_PARTICULIERS) or force:  
            if force: etat = C_OBSTACLE                                     
            objet = OBJ.CObjet(self.MOTEUR, index, x, y, 0, 0, image, image_mask, etat)  
                      
        if not objet == None:
            key = "{:04d}{:04d}{:01d}".format((y * VAR.dim) + image[0].get_height(), (x * VAR.dim) + image[0].get_width(), couche)
            self.liste[key] = objet 
            
        return objet
    
    
   
    
    def fusionne_les_listes_objets_et_personnages(self):
        # --- genere une liste de joueurs et de pnjs
        liste_personnages = {}
        for personnage in self.MOTEUR.PERSONNAGES.JOUEURS + self.MOTEUR.PERSONNAGES.PNJS:
            x = personnage.position_int_x() 
            y = personnage.position_int_y()+(VAR.dim // 2)
            key = "{:04d}{:04d}{:01d}".format(y, x, 0)
            liste_personnages[key] = personnage
        
        # --- fusionne la liste des objets et des joueurs
        if not ENUM_DEMO.BLOCAGE in VAR.demo:    
            listes_fusionnees = {**self.liste, **liste_personnages}        
        else:
            listes_fusionnees = liste_personnages            
        liste_objets_tries = sorted( listes_fusionnees.items(), key=lambda x: x[0])
        return liste_objets_tries
    
    
    
    
            
    def afficher(self):  
        t, i = time.time(), 0

        # --- tri les listes
        liste_objets_tries = self.fusionne_les_listes_objets_et_personnages()
        
        # --- affiche chaque objets
        FCT.Performance('OBJETS.afficher( - creation liste)', t)             
        for key, objet in liste_objets_tries:   
            objet.afficher()    
            
            # // --- test                  
            i = self.afficher_test_priorite(i, key, objet)            
        FCT.Performance('OBJETS.afficher()', t)
        
    
    
    
    def afficher_test_priorite(self, i, key, objet):
        if 2 < objet.x < 15 and 10 < objet.y < 16:
            nombre1 = int(key[0:4])  # Convertit "0123" en entier
            nombre2 = int(key[4:8])  # Convertit "4567" en entier
            nombre3 = int(key[8])    # Convertit "0" en entier

            key1 = "y:" + str(nombre1//VAR.dim)+" x:" + str(nombre2//VAR.dim)+" c:" + str(nombre3)
            key2 = key
                
            txt = key1 + " (" + str(objet.index) +") " + str(key2)
            image_texte = VAR.ecriture.render( txt , True, (255,0,0))
            VAR.fenetre.blit(image_texte, (1400, (i * 18)))
            i+=1
        return i